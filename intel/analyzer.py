"""
Trend Analyzer + Gap Analysis.

Analyzes aggregated interview data to surface:
  - What companies are asking right now
  - Your personal gaps vs. target level
  - Topic frequency heatmaps
  - Difficulty calibration
"""

import json
from datetime import date, timedelta
from collections import Counter

from . import db
from .config import PROFILE, TARGET_COMPANIES, LEVEL_EXPECTATIONS


# ─── Trend Detection ─────────────────────────────────────────────────────────

def get_trending_topics(company=None, days=30, top_n=10):
    """Analyze DB for most frequently asked topics in recent experiences."""
    conn = db.get_conn()
    cutoff = str(date.today() - timedelta(days=days))

    if company:
        rows = conn.execute("""
            SELECT er.round_type, er.topics, er.question, er.difficulty, e.company
            FROM experience_rounds er
            JOIN experiences e ON er.experience_id = e.id
            WHERE LOWER(e.company) LIKE ? AND e.date_scraped >= ?
        """, (f"%{company.lower()}%", cutoff)).fetchall()
    else:
        rows = conn.execute("""
            SELECT er.round_type, er.topics, er.question, er.difficulty, e.company
            FROM experience_rounds er
            JOIN experiences e ON er.experience_id = e.id
            WHERE e.date_scraped >= ?
        """, (cutoff,)).fetchall()
    conn.close()

    # Aggregate
    round_type_counts = Counter()
    topic_counts = Counter()
    difficulty_counts = Counter()
    question_samples = {}  # round_type -> [questions]

    for row in rows:
        rt = row["round_type"] or "unknown"
        round_type_counts[rt] += 1
        difficulty_counts[row["difficulty"] or "unknown"] += 1

        # Parse topics JSON
        try:
            topics = json.loads(row["topics"]) if row["topics"] else []
        except json.JSONDecodeError:
            topics = []
        for t in topics:
            topic_counts[t.lower()] += 1

        # Collect question samples
        if row["question"]:
            question_samples.setdefault(rt, []).append(row["question"])

    return {
        "period_days": days,
        "company": company or "ALL",
        "total_rounds": len(rows),
        "round_types": dict(round_type_counts.most_common(10)),
        "top_topics": dict(topic_counts.most_common(top_n)),
        "difficulty_dist": dict(difficulty_counts),
        "sample_questions": {k: v[:5] for k, v in question_samples.items()},
    }


def get_company_summary(company):
    """Build a summary profile for a company from DB data."""
    conn = db.get_conn()

    # Get experience count
    exp_count = conn.execute(
        "SELECT COUNT(*) FROM experiences WHERE LOWER(company) LIKE ?",
        (f"%{company.lower()}%",)
    ).fetchone()[0]

    # Get results distribution
    results = conn.execute("""
        SELECT overall_result, COUNT(*) as cnt
        FROM experiences WHERE LOWER(company) LIKE ?
        GROUP BY overall_result
    """, (f"%{company.lower()}%",)).fetchall()

    # Get round types
    rounds = conn.execute("""
        SELECT er.round_type, COUNT(*) as cnt
        FROM experience_rounds er
        JOIN experiences e ON er.experience_id = e.id
        WHERE LOWER(e.company) LIKE ?
        GROUP BY er.round_type
        ORDER BY cnt DESC
    """, (f"%{company.lower()}%",)).fetchall()

    # Get recent questions
    questions = conn.execute("""
        SELECT er.round_type, er.question, er.difficulty
        FROM experience_rounds er
        JOIN experiences e ON er.experience_id = e.id
        WHERE LOWER(e.company) LIKE ? AND er.question IS NOT NULL
        ORDER BY e.date_scraped DESC LIMIT 20
    """, (f"%{company.lower()}%",)).fetchall()

    conn.close()

    # Merge with static config
    static = TARGET_COMPANIES.get(company.lower(), {})

    return {
        "company": company,
        "experiences_in_db": exp_count,
        "results": {r["overall_result"]: r["cnt"] for r in results},
        "round_distribution": {r["round_type"]: r["cnt"] for r in rounds},
        "recent_questions": [
            {"type": q["round_type"], "question": q["question"], "difficulty": q["difficulty"]}
            for q in questions
        ],
        "static_info": static,
    }


# ─── Gap Analysis ─────────────────────────────────────────────────────────────

def compute_gap_analysis(progress_data, target_level="sde2"):
    """Compare current progress against target level expectations."""
    expectations = LEVEL_EXPECTATIONS.get(target_level, LEVEL_EXPECTATIONS["sde2"])

    lc_sync = progress_data.get("lc_sync", {})
    total_lc = lc_sync.get("total", 0)
    java_lc = lc_sync.get("java_problems", 0)
    easy = lc_sync.get("easy", 0)
    medium = lc_sync.get("medium", 0)
    hard = lc_sync.get("hard", 0)
    apps = len(progress_data.get("applications", []))
    interviews = len(progress_data.get("interviews", []))
    bugs = len(progress_data.get("bug_journal", []))
    sr_topics = len(progress_data.get("spaced_repetition", {}))

    # Expected values
    exp_dsa = expectations["dsa"]
    exp_sd = expectations["sd"]
    exp_lld = expectations["lld"]
    exp_beh = expectations["behavioral"]

    gaps = []

    # DSA gaps
    if java_lc < exp_dsa["min_java"]:
        severity = "CRITICAL" if java_lc < 20 else "HIGH"
        gaps.append({
            "area": "Java DSA",
            "severity": severity,
            "current": f"{java_lc} problems in Java",
            "target": f"{exp_dsa['min_java']} problems in Java",
            "action": "Switch ALL LeetCode to Java immediately. Run: prep java",
            "priority": 1,
        })

    if hard < exp_dsa["hard"]:
        gaps.append({
            "area": "Hard Problems",
            "severity": "HIGH" if hard < 10 else "MEDIUM",
            "current": f"{hard} hard problems",
            "target": f"{exp_dsa['hard']}+ hard problems",
            "action": "Add 1 Hard per week starting now. Focus: DP, Graphs, Sliding Window",
            "priority": 2,
        })

    if total_lc < 200:
        gaps.append({
            "area": "Total DSA Volume",
            "severity": "MEDIUM",
            "current": f"{total_lc} total",
            "target": "200+ for SDE-2, 350+ for SDE-3",
            "action": "Maintain 7-10 problems/week pace",
            "priority": 3,
        })

    # System Design gaps (estimated from SR data)
    sd_studied = sum(1 for k, v in progress_data.get("spaced_repetition", {}).items()
                     if "system" in k or "sd" in k or "distributed" in k)
    if sd_studied < exp_sd["count"]:
        gaps.append({
            "area": "System Design Practice",
            "severity": "HIGH",
            "current": f"~{sd_studied} SD topics studied",
            "target": f"{exp_sd['count']} full designs practiced",
            "action": "1 design/week on Hello Interview. Start with: Rate Limiter, URL Shortener, Chat System",
            "priority": 2,
        })

    # LLD gaps
    lld_studied = sum(1 for k, v in progress_data.get("spaced_repetition", {}).items()
                      if "lld" in k or "pattern" in k)
    if lld_studied < exp_lld["count"]:
        gaps.append({
            "area": "LLD Practice",
            "severity": "MEDIUM",
            "current": f"~{lld_studied} LLD topics",
            "target": f"{exp_lld['count']} LLD problems solved",
            "action": "Practice: Parking Lot, Elevator, Chess, Snake. Use refactoring.guru for patterns",
            "priority": 3,
        })

    # Behavioral gaps
    beh_logs = sum(1 for k, v in progress_data.get("spaced_repetition", {}).items()
                   if "behav" in k or "star" in k or "behavioral" in k)
    if beh_logs < 3:
        gaps.append({
            "area": "Behavioral Stories",
            "severity": "HIGH",
            "current": f"~{beh_logs} behavioral topics practiced",
            "target": f"{exp_beh['stories']} STAR stories ready",
            "action": "Write 5 STAR stories THIS WEEK. Run: prep story for AI-polished versions",
            "priority": 2,
        })

    # Application pace
    if apps < 5:
        gaps.append({
            "area": "Application Pipeline",
            "severity": "HIGH",
            "current": f"{apps} applications",
            "target": "15+ by Week 6, 30+ by Week 13",
            "action": "Dedicate 1 hour this weekend to apply to 5 companies. Use referrals.",
            "priority": 2,
        })

    # Sort by priority
    gaps.sort(key=lambda g: g["priority"])
    return gaps


def readiness_percentage(progress_data, target_level="sde2"):
    """Quick numerical readiness score (0-100)."""
    gaps = compute_gap_analysis(progress_data, target_level)
    if not gaps:
        return 85  # No gaps detected = fairly ready

    severity_weights = {"CRITICAL": 25, "HIGH": 15, "MEDIUM": 8, "LOW": 3}
    total_penalty = sum(severity_weights.get(g["severity"], 5) for g in gaps)
    score = max(5, 100 - total_penalty)
    return score


# ─── Formatted Output ─────────────────────────────────────────────────────────

def print_trending(company=None, days=30):
    """Print trending topics to stdout."""
    data = get_trending_topics(company=company, days=days)

    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  TRENDING INTERVIEW TOPICS — {data['company']:<26} ║")
    print(f"  ║  Last {data['period_days']} days │ {data['total_rounds']} rounds analyzed{' ' * 20}║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")

    if data["total_rounds"] == 0:
        print(f"\n  No data yet. Run: prep scrape  to fetch interview experiences.")
        print(f"  Or: prep add-experience  to manually log one.\n")
        return

    if data["round_types"]:
        print(f"\n  Round Types:")
        for rt, cnt in data["round_types"].items():
            bar_len = min(cnt * 2, 30)
            print(f"    {rt:<20} {'█' * bar_len} {cnt}")

    if data["top_topics"]:
        print(f"\n  Hot Topics:")
        for topic, cnt in data["top_topics"].items():
            bar_len = min(cnt * 2, 30)
            print(f"    {topic:<20} {'▓' * bar_len} {cnt}")

    if data["difficulty_dist"]:
        print(f"\n  Difficulty Distribution:")
        for diff, cnt in data["difficulty_dist"].items():
            print(f"    {diff:<12} {cnt}")

    if data["sample_questions"]:
        print(f"\n  Recent Questions:")
        for rt, qs in data["sample_questions"].items():
            print(f"    [{rt}]")
            for q in qs[:3]:
                print(f"      • {q[:80]}")

    print()


def print_gap_analysis(progress_data, target_level="sde2"):
    """Print gap analysis to stdout."""
    gaps = compute_gap_analysis(progress_data, target_level)
    score = readiness_percentage(progress_data, target_level)

    level_label = "SDE-2" if target_level == "sde2" else "SDE-3"

    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  GAP ANALYSIS — Target: {level_label:<32} ║")
    print(f"  ║  Readiness: {score}%{' ' * 42}║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")

    if not gaps:
        print(f"\n  ✅ No major gaps detected! You're in good shape.")
        print(f"  Focus on mock interviews and maintaining your pace.\n")
        return

    sev_icons = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}

    for i, gap in enumerate(gaps, 1):
        icon = sev_icons.get(gap["severity"], "⚪")
        print(f"\n  {icon} Gap {i}: {gap['area']}  [{gap['severity']}]")
        print(f"     Current:  {gap['current']}")
        print(f"     Target:   {gap['target']}")
        print(f"     Action:   {gap['action']}")

    print(f"\n  ── WEEKLY FOCUS ORDER ─────────────────────────────────────")
    for i, gap in enumerate(gaps[:3], 1):
        print(f"  {i}. {gap['area']} — {gap['action']}")

    print()


def print_company_profile(company):
    """Print company intelligence from DB + static config."""
    data = get_company_summary(company)
    static = data.get("static_info", {})

    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  COMPANY INTEL: {company.upper():<40} ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")

    if static:
        print(f"\n  Level:          {static.get('level', '?')}")
        print(f"  TC Range:       {static.get('tc_range', '?')}")
        print(f"  Tier:           {'Tier ' + str(static.get('tier', '?'))}")
        print(f"  Focus:          {static.get('focus', '?')}")
        if static.get("rounds"):
            print(f"  Typical Rounds: {', '.join(static['rounds'])}")

    print(f"\n  In your DB:     {data['experiences_in_db']} experience(s)")

    if data["results"]:
        print(f"  Results:        ", end="")
        for result, cnt in data["results"].items():
            icon = "✅" if result == "offer" else ("❌" if result == "reject" else "❔")
            print(f"{icon} {result}: {cnt}  ", end="")
        print()

    if data["round_distribution"]:
        print(f"\n  Round Frequency:")
        for rt, cnt in data["round_distribution"].items():
            print(f"    {rt:<20} {cnt} round(s)")

    if data["recent_questions"]:
        print(f"\n  Recent Questions Asked:")
        for q in data["recent_questions"][:10]:
            diff_tag = f" [{q['difficulty']}]" if q["difficulty"] else ""
            print(f"    [{q['type']}]{diff_tag} {q['question'][:70]}")

    if not data["experiences_in_db"]:
        print(f"\n  💡 No experiences in DB for {company}.")
        print(f"     Run: prep scrape  then: prep trending {company.lower()}")
        print(f"     Or:  prep add-experience  to manually log one you found")

    print()
