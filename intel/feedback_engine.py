"""
Feedback Engine — structured logging + LLM-powered adaptive planning.

Flow:
  1. User logs activities (LC solve, mock, curriculum, LLD, notes)
  2. Engine aggregates logs + progress + intel trends
  3. Claude analyzes → generates adaptive daily/weekly plan
  4. Plan adjusts based on: velocity, weak areas, trending interview topics

Tables:
  activity_log  — structured activity events
  llm_plans     — cached AI-generated plans (daily + weekly)
"""

import json
import os
import sqlite3
import time
from datetime import datetime, date, timedelta
from pathlib import Path

BASE = Path(__file__).parent.parent
DB_PATH = BASE / "data" / "interviews.db"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


# ─── DB helpers ───────────────────────────────────────────────────────────────

def _conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_feedback_tables():
    """Create activity_log and llm_plans tables. Safe to call multiple times."""
    with _conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            logged_at     TEXT DEFAULT (datetime('now')),
            date          TEXT NOT NULL,          -- YYYY-MM-DD
            activity_type TEXT NOT NULL,          -- lc, mock, curriculum, lld, jqa, system_design, behavioral, notes, drill
            title         TEXT,                   -- problem name, topic, lesson title
            details       TEXT,                   -- JSON blob (extra context)
            duration_mins INTEGER DEFAULT 0,
            difficulty    TEXT,                   -- easy, medium, hard
            outcome       TEXT,                   -- solved, struggled, failed, watched, practiced, skipped
            confidence    INTEGER DEFAULT 3,      -- 1 (no clue) to 5 (nailed it)
            notes         TEXT                    -- free-form note
        );

        CREATE TABLE IF NOT EXISTS llm_plans (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at      TEXT DEFAULT (datetime('now')),
            date            TEXT NOT NULL,        -- YYYY-MM-DD the plan is for
            period          TEXT NOT NULL,        -- daily, weekly
            plan_text       TEXT,                 -- markdown plan from LLM
            analysis_text   TEXT,                 -- LLM analysis of progress
            context_summary TEXT,                 -- what context was sent to LLM
            UNIQUE(date, period)
        );
        """)


# ─── Logging ──────────────────────────────────────────────────────────────────

def log_activity(
    activity_type: str,
    title: str,
    duration_mins: int = 0,
    difficulty: str = "",
    outcome: str = "",
    confidence: int = 3,
    notes: str = "",
    details: dict = None,
    log_date: str = None,
) -> int:
    """Insert an activity log entry. Returns the new row id."""
    init_feedback_tables()
    today = log_date or date.today().isoformat()
    with _conn() as conn:
        cur = conn.execute(
            """INSERT INTO activity_log
               (date, activity_type, title, duration_mins, difficulty, outcome, confidence, notes, details)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (today, activity_type, title, duration_mins, difficulty, outcome,
             confidence, notes, json.dumps(details or {}))
        )
        return cur.lastrowid


def get_recent_logs(days: int = 7) -> list[dict]:
    """Fetch activity logs from the last N days."""
    init_feedback_tables()
    since = (date.today() - timedelta(days=days)).isoformat()
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM activity_log WHERE date >= ? ORDER BY date DESC, id DESC",
            (since,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_daily_summary(target_date: str = None) -> dict:
    """Aggregate stats for a single day."""
    init_feedback_tables()
    d = target_date or date.today().isoformat()
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM activity_log WHERE date = ?", (d,)
        ).fetchall()
    logs = [dict(r) for r in rows]
    return {
        "date": d,
        "total_items": len(logs),
        "total_mins": sum(r["duration_mins"] or 0 for r in logs),
        "by_type": _group_by(logs, "activity_type"),
        "struggled": [r["title"] for r in logs if r["outcome"] in ("struggled", "failed")],
        "solved": [r["title"] for r in logs if r["outcome"] == "solved"],
        "avg_confidence": round(sum(r["confidence"] or 3 for r in logs) / max(len(logs), 1), 1),
        "logs": logs,
    }


def _group_by(rows: list, key: str) -> dict:
    result = {}
    for r in rows:
        k = r.get(key, "other")
        result[k] = result.get(k, 0) + 1
    return result


# ─── Context builder ──────────────────────────────────────────────────────────

def _build_context(period: str = "daily") -> str:
    """Assemble all context: progress + logs + intel trends."""
    lines = []

    # ── Progress state ──
    try:
        prog = json.loads((BASE / "logs" / "progress.json").read_text())
    except Exception:
        prog = {}

    lc = prog.get("lc_sync", {})
    lines.append("## Current Progress")
    lines.append(f"- LeetCode: {lc.get('total', 0)} solved (Java: {lc.get('java_problems', 0)}, C++: {lc.get('cpp_problems', 0)})")
    lines.append(f"- Streak: {lc.get('streak', 0)} days")
    lines.append(f"- Applications: {len(prog.get('applications', []))}")
    lines.append(f"- Topics studied: {len(prog.get('topics_done', []))}")

    # Current week
    start = date(2026, 3, 19)
    wk = min(max(1, (date.today() - start).days // 7 + 1), 26)
    lines.append(f"- Current week: {wk}/26")

    # ── Activity logs ──
    days = 7 if period == "weekly" else 3
    logs = get_recent_logs(days=days)
    lines.append(f"\n## Activity Log (last {days} days, {len(logs)} entries)")
    by_day: dict = {}
    for log in logs:
        by_day.setdefault(log["date"], []).append(log)
    for day_str in sorted(by_day.keys(), reverse=True)[:days]:
        day_logs = by_day[day_str]
        total_mins = sum(l["duration_mins"] or 0 for l in day_logs)
        lines.append(f"\n### {day_str} ({total_mins} min)")
        for l in day_logs:
            outcome_tag = f" [{l['outcome']}]" if l.get("outcome") else ""
            conf_tag = f" conf:{l['confidence']}/5" if l.get("confidence") else ""
            lines.append(f"  - [{l['activity_type']}] {l['title']}{outcome_tag}{conf_tag}")
            if l.get("notes"):
                lines.append(f"    note: {l['notes']}")

    # ── Weak areas (struggled/failed) ──
    struggled = [l for l in logs if l.get("outcome") in ("struggled", "failed")]
    if struggled:
        lines.append("\n## Weak Areas (struggled/failed recently)")
        for l in struggled[:10]:
            lines.append(f"  - {l['title']} ({l['activity_type']}, {l['date']})")

    # ── Mock scores ──
    try:
        mock_conn = _conn()
        mock_rows = mock_conn.execute(
            """SELECT company, round_type, score, date_done
               FROM mock_sessions ORDER BY date_done DESC LIMIT 10"""
        ).fetchall()
        if mock_rows:
            lines.append("\n## Recent Mock Scores")
            for r in mock_rows:
                lines.append(f"  - {r['company']} {r['round_type']}: {r['score']}/10 ({r['date_done'][:10]})")
        mock_conn.close()
    except Exception:
        pass

    # ── Intel trends from scraped data ──
    try:
        intel_conn = _conn()
        trend_rows = intel_conn.execute(
            """SELECT topic, company, frequency FROM trending_topics
               ORDER BY date_logged DESC, frequency DESC LIMIT 20"""
        ).fetchall()
        if trend_rows:
            lines.append("\n## Trending Interview Topics (from scraped data)")
            for r in trend_rows:
                lines.append(f"  - {r['topic']} @ {r['company'] or 'all'} (seen {r['frequency']}x)")
        intel_conn.close()
    except Exception:
        pass

    # ── Recent experiences from target companies ──
    try:
        exp_conn = _conn()
        exp_rows = exp_conn.execute(
            """SELECT company, role, overall_result, title, date_posted
               FROM experiences
               WHERE company IN ('Razorpay','PhonePe','Flipkart','Amazon','Google','Goldman','CRED','Swiggy','Stripe')
               ORDER BY date_scraped DESC LIMIT 8"""
        ).fetchall()
        if exp_rows:
            lines.append("\n## Recent Target Company Interview Experiences")
            for r in exp_rows:
                lines.append(f"  - {r['company']} ({r['role']}): {r['overall_result'] or 'unknown'} — {r['title'] or ''}")
        exp_conn.close()
    except Exception:
        pass

    # ── War plan week context ──
    lines.append(f"\n## War Plan Context")
    week_themes = {
        1: "Arrays, Two Pointers, Sliding Window",
        2: "Linked Lists, Recursion",
        3: "Stacks, Queues",
        4: "Binary Trees (apply opens this week!)",
        5: "BST, Heap, Machine Coding starts",
        6: "Graphs, Kafka deep dive",
        7: "Backtracking, Concurrency basics",
        8: "Dynamic Programming Part 1",
        9: "Dynamic Programming Part 2",
        10: "Tries, Advanced Trees",
        11: "Greedy, Bit Manipulation",
        12: "MOCK WEEK — Phase 1 Simulation",
        13: "Polish Week — fix weak areas",
    }
    lines.append(f"  Week {wk} theme: {week_themes.get(wk, 'Advanced prep')}")
    lines.append(f"  Phase: {'1 (first offer: Razorpay/PhonePe/CRED)' if wk <= 13 else '2 (dream role: Amazon/Google/Goldman)'}")

    return "\n".join(lines)


# ─── LLM analysis ─────────────────────────────────────────────────────────────

def _call_claude(prompt: str, max_tokens: int = 1500) -> str:
    """Call Claude API directly via urllib (no SDK needed)."""
    if not ANTHROPIC_API_KEY:
        return "⚠️ ANTHROPIC_API_KEY not set — cannot generate AI plan."

    import urllib.request
    import urllib.error

    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",  # fast + cheap for planning
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        return f"⚠️ Claude API error {e.code}: {body}"
    except Exception as e:
        return f"⚠️ Claude call failed: {e}"


def generate_daily_plan(force: bool = False) -> dict:
    """Generate (or return cached) today's adaptive daily plan."""
    init_feedback_tables()
    today = date.today().isoformat()

    # Return cached plan if fresh (generated today)
    if not force:
        with _conn() as conn:
            row = conn.execute(
                "SELECT * FROM llm_plans WHERE date = ? AND period = 'daily'", (today,)
            ).fetchone()
            if row:
                return {"plan": row["plan_text"], "analysis": row["analysis_text"], "cached": True, "date": today}

    context = _build_context("daily")
    prompt = f"""You are a senior tech interview coach for Jayanti Vishnoi (5.5 YOE, Java/Spring Boot, targeting SDE-2/SDE-3 at product companies, 30-75 LPA).

{context}

Generate a CONCRETE, ACTIONABLE daily plan for today based on:
1. What was done recently (avoid repeating)
2. Current weak areas and struggles
3. Trending interview topics at target companies
4. War plan week theme

Format:
## Today's Analysis (2-3 sentences on progress + main risk)

## Today's Priority Tasks (max 5, ordered by importance)
1. [Category] Task — why it matters, exact approach
2. ...

## Focus Time Blocks
- Morning (2h): ...
- Afternoon (3h): ...
- Evening (2h): ...

## Watch For
- 1-2 specific warnings about current gaps

Be direct and specific — name exact LeetCode problems, topics, or companies. No fluff."""

    plan_text = _call_claude(prompt, max_tokens=800)
    analysis_text = ""

    # Cache it
    with _conn() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO llm_plans (date, period, plan_text, analysis_text, context_summary)
               VALUES (?, 'daily', ?, ?, ?)""",
            (today, plan_text, analysis_text, context[:500])
        )

    return {"plan": plan_text, "analysis": analysis_text, "cached": False, "date": today}


def generate_weekly_plan(force: bool = False) -> dict:
    """Generate (or return cached) this week's adaptive plan."""
    init_feedback_tables()
    # Key by Monday of current week
    today = date.today()
    monday = (today - timedelta(days=today.weekday())).isoformat()

    if not force:
        with _conn() as conn:
            row = conn.execute(
                "SELECT * FROM llm_plans WHERE date = ? AND period = 'weekly'", (monday,)
            ).fetchone()
            if row:
                return {"plan": row["plan_text"], "analysis": row["analysis_text"], "cached": True, "week_start": monday}

    context = _build_context("weekly")
    prompt = f"""You are a senior tech interview coach for Jayanti Vishnoi (5.5 YOE, Java/Spring Boot, targeting SDE-2/SDE-3 at Razorpay/PhonePe/CRED/Flipkart/Amazon/Google, 30-75 LPA).

{context}

Generate a WEEKLY ADAPTIVE PLAN and DEEP ANALYSIS.

Format:
## Weekly Analysis
- Velocity: (are they on track?)
- Biggest gap this week
- What the intel data suggests about what companies are asking

## This Week's Adjusted Focus
(How to shift the war plan based on actual progress and trends)

## Daily Breakdown (Mon–Sun)
- Mon: ...
- Tue: ...
- Wed: ...
- Thu: ...
- Fri: ...
- Sat: LLD/Mock day — ...
- Sun: Review + next week prep

## Key Risks to Address
(Top 3 things that could derail Phase 1 goal)

## Recommended Adjustments to War Plan
(Specific changes if any — e.g. "spend extra day on DP before moving to graphs")

Be specific, data-driven from the logs, and actionable."""

    plan_text = _call_claude(prompt, max_tokens=1200)

    with _conn() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO llm_plans (date, period, plan_text, analysis_text, context_summary)
               VALUES (?, 'weekly', ?, ?, ?)""",
            (monday, plan_text, "", context[:500])
        )

    return {"plan": plan_text, "analysis": "", "cached": False, "week_start": monday}


def get_progress_analysis() -> dict:
    """Quick stats summary for the feedback dashboard."""
    logs_7d = get_recent_logs(days=7)
    logs_today = [l for l in logs_7d if l["date"] == date.today().isoformat()]

    by_type_7d = _group_by(logs_7d, "activity_type")
    struggled_7d = [l["title"] for l in logs_7d if l.get("outcome") in ("struggled", "failed")]
    total_mins_7d = sum(l["duration_mins"] or 0 for l in logs_7d)

    return {
        "today_count": len(logs_today),
        "today_mins": sum(l["duration_mins"] or 0 for l in logs_today),
        "week_count": len(logs_7d),
        "week_mins": total_mins_7d,
        "by_type_7d": by_type_7d,
        "struggled_recently": struggled_7d[:5],
        "avg_confidence_7d": round(sum(l.get("confidence") or 3 for l in logs_7d) / max(len(logs_7d), 1), 1),
    }
