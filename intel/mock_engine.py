"""
Mock Round Simulator with Score Tracking.

Tracks mock scores over time to show weekly improvement trends.
Uses intel DB for persistence. Integrates with AI coach for question generation.

Usage:
  from intel.mock_engine import save_mock_score, get_score_trend, print_score_trend
  from intel.mock_engine import get_readiness_by_company, print_company_readiness
"""

from datetime import date, timedelta
import json


COMPANY_ROUND_MAP = {
    "google":       ["dsa", "dsa", "system_design", "behavioral"],
    "amazon":       ["dsa", "dsa", "system_design", "lld", "behavioral", "behavioral"],
    "microsoft":    ["dsa", "dsa", "dsa", "system_design", "behavioral"],
    "adobe":        ["dsa", "dsa", "lld", "system_design", "behavioral"],
    "flipkart":     ["dsa", "dsa", "machine_coding", "system_design", "behavioral"],
    "goldman":      ["dsa", "dsa", "system_design", "behavioral"],
    "phonepe":      ["dsa", "dsa", "system_design", "lld", "behavioral"],
    "swiggy":       ["dsa", "dsa", "system_design", "machine_coding", "behavioral"],
    "razorpay":     ["dsa", "system_design", "lld", "cultural"],
    "cred":         ["dsa", "system_design", "lld", "cultural"],
    "mock":         ["dsa", "system_design", "behavioral"],
}

ROUND_DURATION = {
    "dsa":           45,
    "system_design": 45,
    "lld":           45,
    "machine_coding": 60,
    "behavioral":    30,
    "cultural":      30,
}

HIRE_THRESHOLD = {
    "dsa":           3.5,
    "system_design": 3.5,
    "lld":           3.5,
    "machine_coding": 3.5,
    "behavioral":    3.5,
    "cultural":      3.5,
}


def get_score_trend(company: str = None, round_type: str = None,
                    weeks: int = 8) -> dict:
    """
    Get score trend over last N weeks.
    Returns weekly averages for progress tracking.
    """
    try:
        from intel.db import get_conn
        conn = get_conn()
        cutoff = str(date.today() - timedelta(weeks=weeks))
        query = """
            SELECT date_done, round_type, score, company
            FROM mock_sessions
            WHERE date_done >= ?
        """
        params = [cutoff]
        if company:
            query += " AND LOWER(company) LIKE ?"
            params.append(f"%{company.lower()}%")
        if round_type:
            query += " AND round_type = ?"
            params.append(round_type)
        query += " ORDER BY date_done ASC"

        rows = conn.execute(query, params).fetchall()
        conn.close()

        if not rows:
            return {"weeks": {}, "trend": "no_data", "improvement": 0}

        # Group by week
        weekly = {}
        for row in rows:
            d = date.fromisoformat(row[0])
            wk_start = str(d - timedelta(days=d.weekday()))  # Monday
            weekly.setdefault(wk_start, []).append(row[2])

        week_avgs = {wk: sum(scores)/len(scores) for wk, scores in sorted(weekly.items())}

        # Calculate trend
        avgs = list(week_avgs.values())
        if len(avgs) >= 2:
            improvement = avgs[-1] - avgs[0]
            trend = "improving" if improvement > 0.3 else ("declining" if improvement < -0.3 else "stable")
        else:
            improvement = 0
            trend = "insufficient_data"

        return {
            "weeks": week_avgs,
            "trend": trend,
            "improvement": round(improvement, 2),
            "latest_avg": avgs[-1] if avgs else 0,
            "first_avg": avgs[0] if avgs else 0,
        }
    except Exception as e:
        return {"weeks": {}, "trend": "error", "improvement": 0, "error": str(e)}


def save_mock_score(company: str, round_type: str, score: float,
                    questions: list = None, time_mins: int = 0,
                    notes: str = "") -> int:
    """Save a mock session score to DB. Returns session ID."""
    try:
        from intel.db import get_conn
        conn = get_conn()
        cur = conn.execute("""
            INSERT INTO mock_sessions
            (date_done, company, round_type, score, questions_json,
             time_mins, notes, hire_verdict)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(date.today()), company.lower(), round_type.lower(),
            score, json.dumps(questions or []),
            time_mins, notes,
            "hire" if score >= HIRE_THRESHOLD.get(round_type, 3.5) else "no_hire"
        ))
        conn.commit()
        session_id = cur.lastrowid
        conn.close()
        return session_id
    except Exception:
        return 0


def print_score_trend(company: str = None, round_type: str = None):
    """Print a visual score trend chart."""
    trend_data = get_score_trend(company=company, round_type=round_type)
    weeks = trend_data.get("weeks", {})

    label = f"{company or 'All Companies'}"
    if round_type:
        label += f" — {round_type.replace('_', ' ').title()}"

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  MOCK SCORE TREND — {label:<36}║
  ╚══════════════════════════════════════════════════════════╝
""")

    if not weeks:
        print("  No mock sessions recorded yet.")
        print("  Run: prep mock-round <company> <round>  to start tracking.")
        print()
        return

    # ASCII bar chart
    print(f"  {'WEEK':<12}  {'SCORE':>6}  CHART")
    print(f"  {'─'*50}")

    sorted_weeks = sorted(weeks.items())
    for wk, avg in sorted_weeks:
        bar_len = int(avg / 5 * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        hire_icon = "✅" if avg >= 3.5 else ("⚠️" if avg >= 2.5 else "❌")
        print(f"  {wk:<12}  {avg:>5.1f}  {bar} {hire_icon}")

    improvement = trend_data.get("improvement", 0)
    trend = trend_data.get("trend", "stable")
    trend_icon = "📈" if trend == "improving" else ("📉" if trend == "declining" else "➡️")
    print(f"\n  {trend_icon} Trend: {trend.title()}  ({improvement:+.1f} over {len(weeks)} week(s))")

    latest = trend_data.get("latest_avg", 0)
    if latest >= 4.0:
        print(f"  ✅ Score {latest:.1f} — interview ready for this round type")
    elif latest >= 3.5:
        print(f"  ⚠️  Score {latest:.1f} — borderline hire, needs consistency")
    else:
        print(f"  ❌ Score {latest:.1f} — needs more practice")

    print()


def get_readiness_by_company(company: str) -> dict:
    """
    Compute readiness % per round type for a company.
    Returns dict: {round_type: readiness_pct}
    """
    rounds = COMPANY_ROUND_MAP.get(company.lower(), ["dsa", "system_design", "behavioral"])
    readiness = {}

    for rt in set(rounds):
        trend = get_score_trend(company=company, round_type=rt, weeks=4)
        latest = trend.get("latest_avg", 0)
        pct = min(int(latest / 5 * 100), 100)
        readiness[rt] = pct

    return readiness


def print_company_readiness(company: str):
    """Print readiness breakdown for a specific company."""
    rounds = COMPANY_ROUND_MAP.get(company.lower(), ["dsa", "system_design", "behavioral"])
    readiness = get_readiness_by_company(company)

    print(f"""
  ── MOCK READINESS: {company.upper()} ─────────────────────────────
  Expected rounds: {', '.join(rounds)}

  {'ROUND TYPE':<20} {'READINESS':>10}  CHART
  {'─'*50}""")

    overall_scores = []
    for rt in sorted(set(rounds)):
        pct = readiness.get(rt, 0)
        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
        icon = "✅" if pct >= 70 else ("⚠️" if pct >= 50 else "❌")
        rt_label = rt.replace("_", " ").title()
        print(f"  {rt_label:<20} {pct:>9}%  {bar} {icon}")
        if pct > 0:
            overall_scores.append(pct)

    if overall_scores:
        overall = int(sum(overall_scores) / len(overall_scores))
        print(f"\n  Overall readiness: {overall}%")
        if overall >= 70:
            print(f"  ✅ Ready to apply for {company}!")
        elif overall >= 50:
            print(f"  ⚠️  Getting there — 2-3 more weeks of mock practice")
        else:
            print(f"  ❌ Need 4-6 weeks of targeted practice first")
    else:
        print(f"\n  No mock data yet. Start with: prep mock-round {company} dsa")

    print()
