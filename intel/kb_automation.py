"""
KB Automation Engine — self-enriching knowledge base for interview prep.

Automated flows:
  1. kb_enrich_from_logs()   — After you log an activity (prep log, prep lc, prep bug),
                                Claude generates Q&A content from your learnings and appends to KB files.
  2. kb_generate_from_jd()   — Paste a JD → auto-generates targeted Q&A for that company/role.
  3. kb_learn_from_mock()    — After a mock interview, extracts questions and generates ideal answers.
  4. kb_fill_gaps()          — Analyzes KB coverage vs your weak areas → auto-generates missing content.
  5. kb_refresh_trending()   — Scrapes trending interview topics → generates fresh Q&A for hot topics.
  6. kb_digest_notes()       — Converts raw study notes/highlights into structured Q&A format.
  7. kb_reindex()            — Re-indexes all KB files into SQLite (wrapper around init_kb).

CLI commands (add to prep.py):
  prep kb status             → KB health check (coverage, freshness, gaps)
  prep kb enrich             → Generate new content from today's activity logs
  prep kb fill               → Auto-fill detected knowledge gaps
  prep kb generate "topic"   → Generate Q&A for a specific topic
  prep kb jd "company"       → Generate company-targeted Q&A from a JD
  prep kb digest             → Convert clipboard/notes into KB format
  prep kb reindex            → Re-index all files into SQLite
  prep kb trending           → Generate Q&A from trending interview topics

Requires: ANTHROPIC_API_KEY env var
"""

import json
import os
import re
import sqlite3
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

BASE = Path(__file__).parent.parent
DB_PATH = BASE / "data" / "interviews.db"
KB_DIR = BASE / "Interview_Answers"
LOGS_DIR = BASE / "logs"
PROG_FILE = LOGS_DIR / "progress.json"

# ─── Claude API helper ───────────────────────────────────────────────────────

def _call_claude(system_prompt: str, user_message: str, max_tokens: int = 4096) -> str:
    """Call Claude API. Returns response text or error string."""
    import urllib.request, urllib.error

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        # Try config_local
        try:
            from intel.config import ANTHROPIC_API_KEY
            api_key = ANTHROPIC_API_KEY
        except Exception:
            pass
    if not api_key:
        return "[ERROR] Set ANTHROPIC_API_KEY env var"

    model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")
    payload = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
            return data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return f"[API Error {e.code}] {body[:500]}"
    except Exception as e:
        return f"[Error] {e}"


# ─── Profile context (shared across all generators) ─────────────────────────

PROFILE_CONTEXT = """
CANDIDATE: Jayanti Vishnoi | 5.5 YOE | GSTN (Specialist Programmer L2) → targeting SDE-2/3
PROJECT: GSTN — India's goods & services tax network. 14M taxpayers, 100K concurrent, 3B+ invoices/year, 45+ microservices.
STACK: Java, Spring Boot, Hibernate, Golang, Kafka, Redis, MySQL, MongoDB, HBase, Docker, Kubernetes, AWS.
STRENGTHS: Distributed caching (JBoss DataGrid + EhCache → DistCacheUtil), Kafka exactly-once + DLQ,
           XA transactions (Atomikos), Strategy+Factory workflow engine, HBase+MySQL ledger, 500 filings/sec.
WEAK AREAS: Java DSA depth, Hard LeetCode, LLD practice, FAANG SD framing, Golang channels.
TARGETS: Phase 1 (30-40L): Razorpay/CRED/PhonePe/Juspay | Phase 2 (45-75L): Amazon/Google/Goldman/Flipkart
CP: CodeChef 4-star, TCS CodeVita Top 1%, Google Code Jam qualifier.
"""

KB_FORMAT_INSTRUCTIONS = """
OUTPUT FORMAT — Strict rules:
1. Use markdown with ## for topic headers, ### for questions, #### for follow-ups.
2. Every answer must be in FIRST PERSON interview voice ("At GSTN, we..." or "I implemented...").
3. Include real numbers from GSTN: 14M users, 100K concurrent, 300Cr+ invoices, 33K peak QPS, etc.
4. Every question must have 1-2 follow-up questions with answers.
5. Keep each Q&A block 200-500 words (optimal for RAG chunking).
6. Separate Q&A blocks with --- (horizontal rule) for clean chunk boundaries.
7. Do NOT use generic textbook answers. Every answer must show DEPTH + EXPERIENCE.
"""


# ─── File mapping: which KB file to append to ────────────────────────────────

TOPIC_TO_FILE = {
    "java":           "Section_01_Java_Core.md",
    "java-core":      "Section_01_Java_Core.md",
    "spring":         "Section_02_Spring_Boot.md",
    "spring-boot":    "Section_02_Spring_Boot.md",
    "hibernate":      "Section_02_Spring_Boot.md",
    "microservices":  "Section_04_05_06_Microservices_Kafka_Redis.md",
    "kafka":          "Section_04_05_06_Microservices_Kafka_Redis.md",
    "redis":          "Section_04_05_06_Microservices_Kafka_Redis.md",
    "database":       "Section_07_08_Database_DistributedSystems.md",
    "distributed":    "Section_07_08_Database_DistributedSystems.md",
    "system-design":  "Section_21_SystemDesign_DeepDive_With_Answers.md",
    "sd":             "Section_21_SystemDesign_DeepDive_With_Answers.md",
    "lld":            "Section_LLD_Complete.md",
    "patterns":       "Section_LLD_Complete.md",
    "dsa":            "Section_DSA_Java_Patterns.md",
    "behavioral":     "Section_Behavioral_DB_Golang.md",
    "star":           "Amazon_LP_STAR_Bank.md",
    "golang":         "Section_Behavioral_DB_Golang.md",
    "cloud":          "Section_Modern_Java_Observability_CQRS.md",
    "aws":            "Section_Modern_Java_Observability_CQRS.md",
    "genai":          "Section_Modern_Java_Observability_CQRS.md",
    "faang":          "Section_20_FAANG_SDE2_SDE3_Advanced.md",
    "advanced":       "Section_20_FAANG_SDE2_SDE3_Advanced.md",
}


def _get_target_file(topic: str) -> Path:
    """Resolve topic to the correct KB file path."""
    topic_key = topic.lower().strip().replace(" ", "-")
    filename = TOPIC_TO_FILE.get(topic_key, "Section_20_FAANG_SDE2_SDE3_Advanced.md")
    return KB_DIR / filename


def _append_to_kb_file(filepath: Path, content: str, source_tag: str = "auto-generated"):
    """Append content to a KB file with metadata header."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    header = f"\n\n---\n\n<!-- Auto-generated: {timestamp} | Source: {source_tag} -->\n\n"
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(header + content.strip() + "\n")


# ─── Flow 1: Enrich from activity logs ──────────────────────────────────────

def kb_enrich_from_logs(days: int = 1) -> dict:
    """
    Read recent activity logs → generate Q&A for topics you studied/struggled with.
    Runs daily (can be scheduled).
    """
    # Get recent activities from activity_log table
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cutoff = (date.today() - timedelta(days=days)).isoformat()

    try:
        rows = conn.execute(
            """SELECT activity_type, title, details, difficulty, outcome, confidence, notes
               FROM activity_log WHERE date >= ? ORDER BY logged_at DESC LIMIT 20""",
            (cutoff,)
        ).fetchall()
    except Exception:
        rows = []
    finally:
        conn.close()

    # Also check progress.json for daily_logs
    try:
        prog = json.loads(PROG_FILE.read_text())
        daily_logs = prog.get("daily_logs", {})
        recent_logs = []
        for d in range(days):
            day_str = (date.today() - timedelta(days=d)).isoformat()
            if day_str in daily_logs:
                recent_logs.extend(daily_logs[day_str])
    except Exception:
        recent_logs = []

    if not rows and not recent_logs:
        return {"status": "no_activity", "message": "No recent activities to enrich from."}

    # Build activity summary
    activities = []
    for row in rows:
        activities.append({
            "type": row["activity_type"],
            "title": row["title"],
            "outcome": row["outcome"],
            "confidence": row["confidence"],
            "notes": row["notes"],
        })

    activity_text = json.dumps(activities, indent=2, default=str)
    if recent_logs:
        activity_text += "\n\nDaily log entries:\n" + "\n".join(f"- {l}" for l in recent_logs[:10])

    system = f"""{PROFILE_CONTEXT}

You are a knowledge base enrichment engine. Given the candidate's recent study activities,
generate 2-3 high-quality Q&A entries for topics they studied or struggled with.

Focus on topics where confidence was LOW (1-3) or outcome was "struggled" or "failed" —
these are the areas that need the most KB content.

{KB_FORMAT_INSTRUCTIONS}

IMPORTANT: Only generate content for topics that were actually studied. Don't make up activities."""

    user = f"Recent activities (last {days} day(s)):\n{activity_text}\n\nGenerate Q&A entries for the weakest areas."
    result = _call_claude(system, user)

    if result.startswith("[ERROR]") or result.startswith("[API Error"):
        return {"status": "error", "message": result}

    # Determine which file to append to based on activity types
    topic_counts = {}
    for a in activities:
        t = a.get("type", "general")
        topic_counts[t] = topic_counts.get(t, 0) + 1

    primary_topic = max(topic_counts, key=topic_counts.get) if topic_counts else "general"
    target_file = _get_target_file(primary_topic)
    _append_to_kb_file(target_file, result, source_tag=f"enrich_from_logs_{date.today()}")

    # Re-index
    from intel.knowledge_base import init_kb
    init_kb(force=False)

    return {
        "status": "success",
        "topic": primary_topic,
        "file": str(target_file.name),
        "activities_processed": len(activities) + len(recent_logs),
        "preview": result[:200] + "...",
    }


# ─── Flow 2: Generate from JD ───────────────────────────────────────────────

def kb_generate_from_jd(jd_text: str, company: str = "", role: str = "") -> dict:
    """
    Paste a job description → generates targeted Q&A for that company's likely questions.
    """
    system = f"""{PROFILE_CONTEXT}

You are an interview question predictor. Given a job description, generate 5-8 high-quality
Q&A entries covering the MOST LIKELY technical questions this company will ask.

{KB_FORMAT_INSTRUCTIONS}

Additional rules:
- Predict questions from JD keywords and required skills
- For each question, provide the answer AS THE CANDIDATE WOULD GIVE IT (using GSTN experience)
- Include company-specific framing (e.g., if Stripe, focus on payment reliability; if Google, focus on scale)
- Tag each Q&A with the interview round it's likely for: [DSA], [System Design], [Java Deep Dive], [Behavioral]"""

    user = f"Company: {company or 'Unknown'}\nRole: {role or 'SDE-2/SDE-3'}\n\nJD:\n{jd_text}"
    result = _call_claude(system, user)

    if result.startswith("[ERROR]") or result.startswith("[API Error"):
        return {"status": "error", "message": result}

    # Save to company-specific file or Phase1/Phase2
    if company:
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', company)
        target_file = KB_DIR / f"Company_Questions_{safe_name}.md"
        if not target_file.exists():
            target_file.write_text(f"# {company} — Interview Questions\n\n")
    else:
        target_file = KB_DIR / "Company_Questions_Phase1.md"

    _append_to_kb_file(target_file, result, source_tag=f"jd_{company}_{date.today()}")

    from intel.knowledge_base import init_kb
    init_kb(force=False)

    return {"status": "success", "company": company, "file": target_file.name, "preview": result[:200] + "..."}


# ─── Flow 3: Learn from mock interview ──────────────────────────────────────

def kb_learn_from_mock(questions, your_answers,
                       round_type: str = "general", company: str = "") -> dict:
    """
    After a mock interview, extracts questions and generates ideal answers.
    """
    qa_pairs = []
    for i, q in enumerate(questions):
        a = your_answers[i] if i < len(your_answers) else "(no answer given)"
        qa_pairs.append(f"Q{i+1}: {q}\nYour Answer: {a}")

    system = f"""{PROFILE_CONTEXT}

You are an interview answer improver. For each mock interview question:
1. Rate the candidate's answer (1-10)
2. Identify what was missing
3. Write the IDEAL answer (as the candidate should deliver it, using their GSTN experience)
4. Add 1-2 follow-up questions the interviewer would ask, with ideal answers

{KB_FORMAT_INSTRUCTIONS}

Round type: {round_type}
Company: {company or 'General'}"""

    user = "Mock interview Q&A:\n\n" + "\n\n".join(qa_pairs)
    result = _call_claude(system, user)

    if result.startswith("[ERROR]"):
        return {"status": "error", "message": result}

    target_file = _get_target_file(round_type)
    _append_to_kb_file(target_file, result, source_tag=f"mock_{round_type}_{company}_{date.today()}")

    from intel.knowledge_base import init_kb
    init_kb(force=False)

    return {"status": "success", "questions": len(questions), "file": target_file.name}


# ─── Flow 4: Fill knowledge gaps ────────────────────────────────────────────

def kb_fill_gaps() -> dict:
    """
    Analyzes current KB coverage vs weak areas and trending topics.
    Generates content to fill the biggest gaps.
    """
    from intel.knowledge_base import get_kb_stats, search_kb

    stats = get_kb_stats()

    # Detect gaps: topics with low chunk count
    category_counts = stats.get("by_category", {})
    weak_categories = [cat for cat, count in category_counts.items() if count < 15]

    # Check known weak areas
    KNOWN_WEAK = [
        "SLF4J Logback configuration spring boot",
        "Spring Profiles activation methods",
        "@Value annotation gotchas static field",
        "binary search on answer pattern",
        "graph algorithms Dijkstra Bellman-Ford",
        "AWS VPC IAM policies deep dive",
        "Anthropic interview AI safety alignment",
        "LLD elevator system state pattern",
        "system design estimation back-of-envelope",
    ]

    gaps = []
    for topic in KNOWN_WEAK:
        results = search_kb(topic, limit=2)
        max_score = max((r["score"] for r in results), default=0)
        if max_score < 10:  # weak coverage
            gaps.append(topic)

    if not gaps and not weak_categories:
        return {"status": "no_gaps", "message": "Knowledge base coverage looks solid!"}

    system = f"""{PROFILE_CONTEXT}

You are a knowledge base gap filler. Generate high-quality Q&A content for the following
topics that have WEAK or MISSING coverage in the candidate's prep system.

{KB_FORMAT_INSTRUCTIONS}

Generate 2-3 Q&A entries per gap topic. Prioritize the first 3 gaps listed."""

    gap_text = "Weak categories (low chunk count): " + ", ".join(weak_categories) + "\n\n"
    gap_text += "Specific topic gaps:\n" + "\n".join(f"- {g}" for g in gaps[:5])

    result = _call_claude(system, gap_text)

    if result.startswith("[ERROR]"):
        return {"status": "error", "message": result}

    # Append to the most relevant file for the first gap
    if gaps:
        first_gap_words = gaps[0].lower().split()
        topic_guess = first_gap_words[0] if first_gap_words else "general"
        target_file = _get_target_file(topic_guess)
    else:
        target_file = _get_target_file("faang")

    _append_to_kb_file(target_file, result, source_tag=f"gap_fill_{date.today()}")

    from intel.knowledge_base import init_kb
    init_kb(force=False)

    return {
        "status": "success",
        "gaps_found": len(gaps),
        "weak_categories": weak_categories,
        "file": target_file.name,
        "preview": result[:200] + "...",
    }


# ─── Flow 5: Generate from trending topics ──────────────────────────────────

def kb_refresh_trending() -> dict:
    """
    Pulls trending interview topics from scraped data → generates fresh Q&A.
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    try:
        # Get recent trending topics
        rows = conn.execute(
            """SELECT topic, frequency FROM trending_topics
               ORDER BY frequency DESC LIMIT 10"""
        ).fetchall()
    except Exception:
        rows = []
    finally:
        conn.close()

    if not rows:
        return {"status": "no_data", "message": "No trending topics found. Run 'prep sync' first."}

    topics = [{"topic": r["topic"], "frequency": r["frequency"]} for r in rows]

    system = f"""{PROFILE_CONTEXT}

You are an interview trend analyzer. Given the most frequently asked topics in recent
interviews, generate fresh Q&A entries that prepare the candidate for these trending questions.

{KB_FORMAT_INSTRUCTIONS}

Focus on topics that appeared 3+ times. Generate content that's different from standard
textbook answers — show depth and real-world experience."""

    user = f"Trending interview topics (last 30 days):\n{json.dumps(topics, indent=2)}"
    result = _call_claude(system, user)

    if result.startswith("[ERROR]"):
        return {"status": "error", "message": result}

    target_file = KB_DIR / "Section_20_FAANG_SDE2_SDE3_Advanced.md"
    _append_to_kb_file(target_file, result, source_tag=f"trending_{date.today()}")

    from intel.knowledge_base import init_kb
    init_kb(force=False)

    return {"status": "success", "trending_topics": len(topics), "file": target_file.name}


# ─── Flow 6: Digest raw notes ───────────────────────────────────────────────

def kb_digest_notes(raw_notes: str, topic: str = "general") -> dict:
    """
    Convert raw study notes/highlights into structured Q&A format.
    """
    system = f"""{PROFILE_CONTEXT}

You are a note-to-Q&A converter. Transform the candidate's raw study notes into
structured interview Q&A entries that are ready for the knowledge base.

{KB_FORMAT_INSTRUCTIONS}

Rules:
- Extract the key concepts from the notes
- Frame each as a question an interviewer would ask
- Write the answer in the candidate's interview voice (first person, with GSTN examples)
- If the notes mention a bug/issue/learning → frame as "Tell me about a time you..." behavioral Q"""

    user = f"Topic: {topic}\n\nRaw notes:\n{raw_notes}"
    result = _call_claude(system, user)

    if result.startswith("[ERROR]"):
        return {"status": "error", "message": result}

    target_file = _get_target_file(topic)
    _append_to_kb_file(target_file, result, source_tag=f"notes_{topic}_{date.today()}")

    from intel.knowledge_base import init_kb
    init_kb(force=False)

    return {"status": "success", "topic": topic, "file": target_file.name, "preview": result[:200] + "..."}


# ─── Flow 7: Generate Q&A for a specific topic ──────────────────────────────

def kb_generate_topic(topic: str, depth: str = "sde3", num_questions: int = 3) -> dict:
    """
    Generate Q&A for a specific topic on demand.
    """
    system = f"""{PROFILE_CONTEXT}

You are an expert interviewer generating {depth.upper()}-level questions on: {topic}

Generate {num_questions} interview Q&A entries with full answers.

{KB_FORMAT_INSTRUCTIONS}

Make these HARD questions — the kind that separate SDE-2 from SDE-3.
Include edge cases, tradeoffs, and "what if" follow-ups."""

    user = f"Generate {num_questions} {depth}-level Q&A entries on: {topic}"
    result = _call_claude(system, user)

    if result.startswith("[ERROR]"):
        return {"status": "error", "message": result}

    target_file = _get_target_file(topic)
    _append_to_kb_file(target_file, result, source_tag=f"generate_{topic}_{date.today()}")

    from intel.knowledge_base import init_kb
    init_kb(force=False)

    return {"status": "success", "topic": topic, "questions": num_questions, "file": target_file.name}


# ─── KB Health Check ─────────────────────────────────────────────────────────

def kb_status() -> dict:
    """
    Comprehensive KB health check: coverage, freshness, gaps, recommendations.
    """
    from intel.knowledge_base import get_kb_stats

    stats = get_kb_stats()

    # Check file freshness
    file_info = []
    if KB_DIR.exists():
        for f in sorted(KB_DIR.glob("*.md")):
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            age_days = (datetime.now() - mtime).days
            lines = len(f.read_text(encoding="utf-8", errors="replace").splitlines())
            file_info.append({
                "file": f.name,
                "lines": lines,
                "size_kb": f.stat().st_size // 1024,
                "last_modified": mtime.strftime("%Y-%m-%d"),
                "age_days": age_days,
                "stale": age_days > 14,
            })

    # Coverage analysis
    categories = stats.get("by_category", {})
    total_chunks = stats.get("total", 0)

    # Recommendations
    recommendations = []
    if categories.get("behavioral", 0) < 15:
        recommendations.append("Add more STAR stories (behavioral category is thin)")
    if categories.get("lld", 0) < 15:
        recommendations.append("Add more LLD problems with full implementations")
    if categories.get("dsa", 0) < 25:
        recommendations.append("Add more DSA pattern explanations and Java templates")
    stale_files = [f for f in file_info if f["stale"]]
    if stale_files:
        recommendations.append(f"{len(stale_files)} file(s) haven't been updated in 14+ days — run 'prep kb enrich'")
    if total_chunks < 300:
        recommendations.append("KB has <300 chunks — run 'prep kb fill' to auto-generate gap content")

    return {
        "total_chunks": total_chunks,
        "categories": categories,
        "files": file_info,
        "stale_files": len(stale_files),
        "recommendations": recommendations,
    }


# ─── Wrapper: reindex ────────────────────────────────────────────────────────

def kb_reindex(force: bool = True) -> dict:
    """Re-index all KB files into SQLite."""
    from intel.knowledge_base import init_kb
    return init_kb(force=force)


# ─── CLI entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        result = kb_status()
        print(json.dumps(result, indent=2))

    elif cmd == "enrich":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        result = kb_enrich_from_logs(days=days)
        print(json.dumps(result, indent=2))

    elif cmd == "fill":
        result = kb_fill_gaps()
        print(json.dumps(result, indent=2))

    elif cmd == "generate":
        topic = sys.argv[2] if len(sys.argv) > 2 else "java"
        result = kb_generate_topic(topic)
        print(json.dumps(result, indent=2))

    elif cmd == "trending":
        result = kb_refresh_trending()
        print(json.dumps(result, indent=2))

    elif cmd == "reindex":
        result = kb_reindex()
        print(json.dumps(result, indent=2))

    elif cmd == "digest":
        topic = sys.argv[2] if len(sys.argv) > 2 else "general"
        print("Paste your notes (Ctrl+D when done):")
        notes = sys.stdin.read()
        result = kb_digest_notes(notes, topic)
        print(json.dumps(result, indent=2))

    else:
        print("""
Usage: python -m intel.kb_automation <command>

Commands:
  status              KB health check
  enrich [days]       Generate Q&A from recent activity logs
  fill                Auto-fill knowledge gaps
  generate <topic>    Generate Q&A for a topic (java, kafka, sd, etc.)
  trending            Generate Q&A from trending interview topics
  reindex             Re-index all files into SQLite
  digest <topic>      Convert pasted notes into Q&A format
""")
