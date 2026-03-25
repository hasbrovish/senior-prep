"""
LLM-powered interview experience extractor.

Problem: scrapers pull raw Reddit/LeetCode posts — regex parsing is too noisy.
Solution: send raw post body to Claude Haiku, extract structured JSON with:
  - company, role, result, rounds (type, question, difficulty, topics)
  - prep tips, time_at_company, resources_used

Usage:
  from intel.exp_extractor import extract_experience, enrich_pending_experiences
  data = extract_experience(raw_title, raw_body, company_hint=None)
  enrich_pending_experiences(limit=20)  # batch-enrich DB rows with no summary
"""

import json
import os
import re
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
DB_PATH = BASE / "data" / "interviews.db"
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Use cheapest model — experiences are short, extraction is mechanical
EXTRACT_MODEL = "claude-haiku-4-5-20251001"

EXTRACT_SYSTEM = """\
You extract structured interview experience data from raw social media posts.
Return ONLY valid JSON — no markdown, no explanation.

JSON schema:
{
  "company": "string (company name, or null if unclear)",
  "role": "SDE-1|SDE-2|SDE-3|Senior|Staff|Principal|Unknown",
  "result": "offer|reject|ghosted|pending|unknown",
  "yoe": "number or null (years of experience mentioned)",
  "prep_duration_weeks": "number or null",
  "rounds": [
    {
      "round_num": 1,
      "round_type": "dsa|system_design|lld|behavioral|hr|machine_coding|unknown",
      "questions": ["exact question text if mentioned"],
      "topics": ["topic1", "topic2"],
      "difficulty": "easy|medium|hard|unknown",
      "outcome": "cleared|failed|unknown",
      "duration_mins": null or number,
      "key_insight": "one-sentence insight for prep"
    }
  ],
  "resources_used": ["LeetCode", "System Design Primer", ...],
  "prep_tips": ["tip 1", "tip 2"],
  "body_summary": "2-3 sentence summary of the full experience"
}

Rules:
- Extract REAL questions asked verbatim when possible
- If a question is paraphrased, clean it up but mark as approximate
- rounds[] can be empty if no round details given
- company must be a recognizable tech company name (Google, Amazon, Flipkart, Razorpay, etc.)
- Focus on Indian market companies when relevant
"""


def _call_haiku(raw_title: str, raw_body: str):
    """Call Claude Haiku to extract structured data from a raw post."""
    if not API_KEY:
        return None

    prompt = f"TITLE: {raw_title}\n\nBODY:\n{raw_body[:4000]}"

    payload = json.dumps({
        "model": EXTRACT_MODEL,
        "max_tokens": 1200,
        "system": EXTRACT_SYSTEM,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            text = data["content"][0]["text"].strip()
            # strip markdown code fences if model adds them
            text = re.sub(r"^```[a-z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
            return json.loads(text)
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, KeyError):
        return None


def extract_experience(title: str, body: str, company_hint = None):
    """
    Extract structured data from a raw interview post.
    Returns dict matching the JSON schema above, or None if extraction failed.
    """
    result = _call_haiku(title, body)
    if not result:
        return None
    # Patch company from hint if LLM returned null
    if not result.get("company") and company_hint:
        result["company"] = company_hint
    return result


def _conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def enrich_pending_experiences(limit: int = 30) -> dict:
    """
    Find experiences in DB with no body_summary, run LLM extraction,
    update the row + insert/update experience_rounds.

    Returns stats: {processed, enriched, failed, skipped}
    """
    if not API_KEY:
        return {"processed": 0, "enriched": 0, "failed": 0, "skipped": 0, "reason": "no API key"}

    stats = {"processed": 0, "enriched": 0, "failed": 0, "skipped": 0}

    with _conn() as conn:
        rows = conn.execute(
            """SELECT id, company, title, body_raw FROM experiences
               WHERE (body_summary IS NULL OR body_summary = '')
                 AND (body_raw IS NOT NULL AND body_raw != '')
               LIMIT ?""",
            (limit,)
        ).fetchall()

        for row in rows:
            stats["processed"] += 1
            exp_id = row["id"]
            raw_body = row["body_raw"] or ""
            if len(raw_body) < 80:
                stats["skipped"] += 1
                continue

            extracted = _call_haiku(row["title"] or "", raw_body)
            if not extracted:
                stats["failed"] += 1
                continue

            summary = extracted.get("body_summary", "")
            tips_json = json.dumps(extracted.get("prep_tips", []))
            resources_json = json.dumps(extracted.get("resources_used", []))
            company = extracted.get("company") or row["company"]
            role = extracted.get("role", "")
            result_val = extracted.get("result", "unknown")
            yoe = extracted.get("yoe")
            prep_weeks = extracted.get("prep_duration_weeks")

            conn.execute(
                """UPDATE experiences SET
                     body_summary = ?,
                     company = ?,
                     role = ?,
                     overall_result = ?,
                     prep_duration = ?,
                     resources_used = ?,
                     tips = ?
                   WHERE id = ?""",
                (summary, company, role, result_val,
                 f"{prep_weeks} weeks" if prep_weeks else None,
                 resources_json, tips_json, exp_id)
            )

            # Upsert rounds
            rounds = extracted.get("rounds", [])
            for i, r in enumerate(rounds, 1):
                questions = r.get("questions", [])
                question_text = " | ".join(questions) if questions else ""
                topics_json = json.dumps(r.get("topics", []))

                # Check if round exists
                existing = conn.execute(
                    "SELECT id FROM experience_rounds WHERE experience_id=? AND round_num=?",
                    (exp_id, r.get("round_num", i))
                ).fetchone()

                if existing:
                    conn.execute(
                        """UPDATE experience_rounds SET
                             round_type=?, question=?, difficulty=?, topics=?,
                             key_insights=?, outcome=?, duration_mins=?
                           WHERE id=?""",
                        (r.get("round_type", "unknown"), question_text,
                         r.get("difficulty", "unknown"), topics_json,
                         r.get("key_insight", ""), r.get("outcome", "unknown"),
                         r.get("duration_mins"), existing["id"])
                    )
                else:
                    conn.execute(
                        """INSERT INTO experience_rounds
                             (experience_id, round_num, round_type, question, difficulty,
                              topics, key_insights, outcome, duration_mins)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (exp_id, r.get("round_num", i), r.get("round_type", "unknown"),
                         question_text, r.get("difficulty", "unknown"), topics_json,
                         r.get("key_insight", ""), r.get("outcome", "unknown"),
                         r.get("duration_mins"))
                    )

            conn.commit()
            stats["enriched"] += 1

    return stats


def get_enriched_questions(company=None, round_type=None, limit: int = 50):
    """
    Return real interview questions extracted by LLM, optionally filtered.
    Only returns rows where question field is non-empty (LLM-extracted).
    """
    with _conn() as conn:
        conditions = ["er.question != ''", "er.question IS NOT NULL"]
        params = []
        if company:
            conditions.append("LOWER(e.company) = LOWER(?)")
            params.append(company)
        if round_type:
            conditions.append("er.round_type = ?")
            params.append(round_type)
        params.append(limit)

        rows = conn.execute(
            f"""SELECT e.company, e.role, e.overall_result, e.date_posted,
                       er.round_num, er.round_type, er.question, er.difficulty,
                       er.topics, er.key_insights, er.outcome
                FROM experience_rounds er
                JOIN experiences e ON e.id = er.experience_id
                WHERE {' AND '.join(conditions)}
                ORDER BY e.date_posted DESC
                LIMIT ?""",
            params
        ).fetchall()

        out = []
        for r in rows:
            topics = []
            try:
                topics = json.loads(r["topics"] or "[]")
            except Exception:
                pass
            out.append({
                "company": r["company"],
                "role": r["role"],
                "result": r["overall_result"],
                "round_type": r["round_type"],
                "question": r["question"],
                "difficulty": r["difficulty"],
                "topics": topics,
                "key_insight": r["key_insights"],
                "date": r["date_posted"],
            })
        return out


if __name__ == "__main__":
    import sys
    if "--enrich" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--enrich") + 1]) if sys.argv.index("--enrich") + 1 < len(sys.argv) else 20
        print(f"Enriching up to {limit} pending experiences...")
        stats = enrich_pending_experiences(limit=limit)
        print(f"Done: {stats}")
    else:
        print("Usage: python -m intel.exp_extractor --enrich [limit]")
