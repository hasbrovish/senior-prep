"""
Regex-based question extractor for raw interview experience posts.
Zero dependencies — no LLM or API key needed.
"""

import re
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional


# ─── Known LeetCode / interview problem names ─────────────────────────────────

LEETCODE_PROBLEMS = [
    "LRU Cache", "LFU Cache", "Two Sum", "Three Sum", "Valid Parentheses",
    "Merge Intervals", "Word Break", "Word Search", "Number of Islands",
    "Clone Graph", "Course Schedule", "Longest Substring Without Repeating",
    "Longest Common Subsequence", "Edit Distance", "Coin Change",
    "House Robber", "Jump Game", "Container With Most Water",
    "Trapping Rain Water", "Sliding Window Maximum", "Median of Two Sorted Arrays",
    "Binary Tree Level Order Traversal", "Serialize and Deserialize Binary Tree",
    "Lowest Common Ancestor", "Diameter of Binary Tree", "Path Sum",
    "Flatten Binary Tree to Linked List", "Construct Binary Tree",
    "Kth Largest Element", "Top K Frequent Elements", "Find Median from Data Stream",
    "Meeting Rooms", "Task Scheduler", "First Missing Positive",
    "Evaluate Reverse Polish Notation", "Decode Ways", "Unique Paths",
    "Minimum Path Sum", "Regular Expression Matching", "Wildcard Matching",
    "Max Points on a Line", "Skyline Problem", "Random Pick with Weight",
    "Design Twitter", "Design TinyURL", "Design Hit Counter",
    "Design Search Autocomplete System", "Design Tic-Tac-Toe",
    "Min Stack", "Max Stack", "Implement Queue using Stacks",
    "Implement Stack using Queues", "Design HashMap", "Design HashSet",
    "Alien Dictionary", "Accounts Merge", "Redundant Connection",
    "Network Delay Time", "Cheapest Flights Within K Stops",
    "Word Ladder", "Pacific Atlantic Water Flow", "Surrounded Regions",
    "Rotting Oranges", "01 Matrix", "Shortest Path in Binary Matrix",
    "Robot Room Cleaner", "Partition Equal Subset Sum",
    "Burst Balloons", "Strange Printer", "Minimum Window Substring",
    "Substring with Concatenation of All Words", "Permutation in String",
    "Reconstruct Itinerary", "Critical Connections in a Network",
    "All Nodes Distance K in Binary Tree", "Binary Tree Right Side View",
    "Vertical Order Traversal of a Binary Tree",
    "Maximum Frequency Stack", "Insert Delete GetRandom O(1)",
    "Read N Characters Given Read4", "Move Zeroes", "Next Permutation",
    "Rotate Image", "Spiral Matrix", "Set Matrix Zeroes",
    "Search a 2D Matrix", "Sort Colors", "Remove Duplicates from Sorted Array",
]

# ─── Regex patterns ────────────────────────────────────────────────────────────

# Numbered questions: "1. Design a ...", "Q1. ...", "Question 1:", "Problem 1:"
NUMBERED_RE = re.compile(
    r'(?:^|\n)\s*(?:Q(?:uestion)?\s*\d+[\.\:\)]\s*|Problem\s*\d+[\.\:\)]\s*|\d+[\.\)]\s+)(.{20,300})',
    re.IGNORECASE | re.MULTILINE,
)

# Round labels: "Round 1:", "Round 2 (DSA):", "Technical Round:", "Coding Round:"
ROUND_LABEL_RE = re.compile(
    r'(?:^|\n)\s*(?:Round\s*\d+\s*(?:\([^)]+\))?\s*[\:\-]|(?:Technical|Coding|System\s*Design|LLD|HR|Bar\s*Raiser|Behavioral|Culture|Onsite)\s*Round\s*[\:\-])\s*(.{15,300})',
    re.IGNORECASE | re.MULTILINE,
)

# System design: "Design X at scale", "How would you design...", "Design a ..."
SYSTEM_DESIGN_RE = re.compile(
    r'(?:How\s+would\s+you\s+design\b.{10,200}|Design\s+(?:a\s+)?(?:scalable\s+)?(?:distributed\s+)?[A-Z][a-zA-Z\s]{5,80}(?:at\s+scale|system|service|platform|API)?)',
    re.IGNORECASE,
)

# Behavioral: "Tell me about a time when...", "Describe a situation...", "LP:"
BEHAVIORAL_RE = re.compile(
    r'(?:Tell\s+me\s+about\s+a\s+time\s+(?:when\s+)?.{10,200}|Describe\s+a\s+(?:situation|time|project)\s+.{10,200}|What\s+(?:would\s+you|did\s+you)\s+do\s+when\s+.{10,150}|LP\s*:\s*.{10,200}|Have\s+you\s+ever\s+.{10,150})',
    re.IGNORECASE,
)

# Inline patterns: "Asked me to ...", "Was given ...", "Had to solve ..."
INLINE_RE = re.compile(
    r'(?:(?:asked|told)\s+(?:me\s+)?to\s+(?:implement|design|solve|write|build|code|find|create)\b.{10,200}|(?:given|was\s+given)\s+(?:a\s+)?(?:problem|question|task)\s*(?:to|of)\s*.{10,200}|had\s+to\s+(?:implement|design|solve|write|build|code|find|create)\b.{10,200}|(?:implement|code|write)\s+(?:a\s+)?(?:function|class|system|algorithm)\s+(?:to|for|that)\s+.{10,200})',
    re.IGNORECASE,
)

# Question-mark sentences (standalone lines ending in ?)
QUESTION_MARK_RE = re.compile(
    r'(?:^|\n)\s*([A-Z][^?\n]{20,200}\?)',
    re.MULTILINE,
)

# Round type keywords to classify extracted questions
ROUND_TYPE_KEYWORDS = {
    "system_design": [
        "design", "scale", "distributed", "microservice", "architecture",
        "hld", "high level", "api design", "database design", "capacity",
        "throughput", "latency", "availability", "consistency",
    ],
    "lld": [
        "lld", "low level", "class diagram", "object oriented", "ood",
        "implement", "parking lot", "chess", "elevator", "hotel booking",
        "library management", "machine coding",
    ],
    "dsa": [
        "array", "string", "tree", "graph", "dp", "dynamic programming",
        "binary search", "linked list", "stack", "queue", "heap",
        "sort", "search", "subsequence", "substring", "sum", "path",
        "matrix", "grid", "backtrack", "recursion", "algorithm",
        "complexity", "o(n", "o(log", "leetcode",
    ],
    "behavioral": [
        "tell me", "describe a", "time when", "situation", "challenge",
        "conflict", "leadership", "initiative", "failure", "success",
        "team", "stakeholder", "priorit", "lp:", "bar raiser",
    ],
}

DIFFICULTY_KEYWORDS = {
    "easy":   ["easy", "simple", "basic", "trivial", "straightforward"],
    "medium": ["medium", "moderate", "intermediate"],
    "hard":   ["hard", "difficult", "tough", "tricky", "complex", "advanced"],
}


# ─── Core extraction logic ─────────────────────────────────────────────────────

def _classify_round_type(text: str) -> str:
    text_lower = text.lower()
    scores = {rtype: 0 for rtype in ROUND_TYPE_KEYWORDS}
    for rtype, keywords in ROUND_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[rtype] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "dsa"


def _classify_difficulty(text: str) -> Optional[str]:
    text_lower = text.lower()
    for diff, keywords in DIFFICULTY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return diff
    return None


def _clean_text(text: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'\s{3,}', '  ', text)
    return text.strip()


def _is_real_question(text: str) -> bool:
    """Filter out noise — only keep lines that look like actual interview questions."""
    if len(text) < 25:
        return False
    # Skip meta lines like "Round 1:" alone or "Interview experience"
    noise = re.compile(
        r'^(round|interview|experience|company|role|result|offer|reject|introduction|profile|background)\s*[\d:\-]',
        re.IGNORECASE,
    )
    if noise.match(text.strip()):
        return False
    return True


def extract_questions(raw_text: str) -> List[Dict]:
    """
    Extract real interview questions from raw post text.

    Returns a list of dicts:
        {question, round_type, difficulty, source_line}
    """
    if not raw_text:
        return []

    text = _clean_text(raw_text)
    seen = set()
    results = []

    def _add(q_text: str, source_label: str):
        q_text = q_text.strip()
        # Truncate overly long matches
        if len(q_text) > 250:
            q_text = q_text[:247] + "..."
        if not _is_real_question(q_text):
            return
        # Deduplicate by normalised lower form
        key = re.sub(r'\s+', ' ', q_text.lower())[:80]
        if key in seen:
            return
        seen.add(key)
        results.append({
            "question":    q_text,
            "round_type":  _classify_round_type(q_text),
            "difficulty":  _classify_difficulty(q_text),
            "source_line": source_label,
        })

    # 1. Numbered questions
    for m in NUMBERED_RE.finditer(text):
        _add(m.group(1), "numbered")

    # 2. Round-label questions
    for m in ROUND_LABEL_RE.finditer(text):
        _add(m.group(1), "round_label")

    # 3. System design patterns
    for m in SYSTEM_DESIGN_RE.finditer(text):
        _add(m.group(0), "system_design_pattern")

    # 4. Behavioral patterns
    for m in BEHAVIORAL_RE.finditer(text):
        _add(m.group(0), "behavioral_pattern")

    # 5. Inline action patterns
    for m in INLINE_RE.finditer(text):
        _add(m.group(0), "inline_pattern")

    # 6. Known LeetCode problem names appearing in text
    for prob in LEETCODE_PROBLEMS:
        if re.search(re.escape(prob), text, re.IGNORECASE):
            _add(prob, "leetcode_problem_name")

    # 7. Question-mark sentences (standalone questions)
    for m in QUESTION_MARK_RE.finditer(text):
        _add(m.group(1), "question_mark")

    return results


# ─── Bulk DB extraction ────────────────────────────────────────────────────────

def bulk_extract_from_db(limit: int = 500) -> Dict:
    """
    Run question extraction on all experiences that have body_raw but whose
    experience_rounds rows still have the raw full-post text as the question
    (i.e. question length > 500 chars, which indicates un-extracted content),
    OR experiences that have body_raw but zero rounds at all.

    Updates experience_rounds with extracted questions and also inserts new
    round rows for experiences that had no rounds extracted at scrape time.

    Returns a summary dict.
    """
    from intel.db import get_conn
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")

    total_processed = 0
    total_questions_inserted = 0
    total_rounds_updated = 0

    try:
        # ── 1. Experiences with NO rounds yet ────────────────────────────────
        no_rounds = conn.execute("""
            SELECT e.id, e.body_raw
            FROM experiences e
            LEFT JOIN experience_rounds er ON er.experience_id = e.id
            WHERE e.body_raw IS NOT NULL AND e.body_raw != ''
              AND er.id IS NULL
            LIMIT ?
        """, (limit,)).fetchall()

        for row in no_rounds:
            exp_id = row["id"]
            questions = extract_questions(row["body_raw"] or "")
            for i, q in enumerate(questions, start=1):
                conn.execute("""
                    INSERT INTO experience_rounds
                    (experience_id, round_num, round_type, question, difficulty,
                     topics, key_insights, outcome, duration_mins)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    exp_id, i, q["round_type"], q["question"],
                    q["difficulty"], json.dumps([]), None, None, None,
                ))
                total_questions_inserted += 1
            if questions:
                total_processed += 1

        # ── 2. Rounds where question is clearly the raw full-post (too long) ─
        raw_rounds = conn.execute("""
            SELECT er.id, er.experience_id, er.question, e.body_raw
            FROM experience_rounds er
            JOIN experiences e ON er.experience_id = e.id
            WHERE LENGTH(er.question) > 500
            LIMIT ?
        """, (limit,)).fetchall()

        for row in raw_rounds:
            questions = extract_questions(row["body_raw"] or "")
            if questions:
                # Update this round with the first relevant question of the same type
                first_q = questions[0]
                conn.execute("""
                    UPDATE experience_rounds
                    SET question = ?, round_type = ?, difficulty = ?
                    WHERE id = ?
                """, (first_q["question"], first_q["round_type"],
                      first_q["difficulty"], row["id"]))
                total_rounds_updated += 1

                # Insert remaining questions as new rounds
                for q in questions[1:]:
                    conn.execute("""
                        INSERT INTO experience_rounds
                        (experience_id, round_num, round_type, question, difficulty,
                         topics, key_insights, outcome, duration_mins)
                        VALUES (?, NULL, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row["experience_id"], q["round_type"], q["question"],
                        q["difficulty"], json.dumps([]), None, None, None,
                    ))
                    total_questions_inserted += 1

        conn.commit()
    finally:
        conn.close()

    return {
        "status": "ok",
        "experiences_processed": total_processed,
        "rounds_updated": total_rounds_updated,
        "new_questions_inserted": total_questions_inserted,
    }


if __name__ == "__main__":
    result = bulk_extract_from_db()
    print(result)
