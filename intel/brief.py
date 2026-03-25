"""
Daily Morning Brief — push notification to phone via ntfy.sh.

ntfy.sh is free, no account needed, works on Android/iOS.
Install: https://ntfy.sh  (or use web push at ntfy.sh/<topic>)

Setup (one time):
  1. Install ntfy app on phone
  2. Subscribe to topic: senior_prep_sde2  (e.g. senior_prep_sde2)
  3. Add to ~/.zshrc:  export NTFY_TOPIC=senior_prep_sde2
  4. Optional: export NTFY_TOKEN=<token>  (only needed for private topics)

What the brief contains:
  - Today's 3 Java DSA problems
  - Trending topic (what companies asked yesterday)
  - Current week theme + today's focus
  - Streak status
  - One behavioral story reminder

Usage:
  from intel.brief import send_morning_brief, generate_brief_text
"""

import json
import os
import urllib.request
import urllib.error
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).parent.parent
NTFY_BASE = "https://ntfy.sh"


def generate_brief_text(verbose: bool = False) -> dict:
    """Generate the morning brief content."""
    brief = {
        "title": "",
        "body":  "",
        "sections": {},
    }

    # ── Prep state ──────────────────────────────────────────────────────────
    prog_file = BASE / "logs" / "progress.json"
    try:
        p = json.loads(prog_file.read_text())
    except Exception:
        p = {}

    lc_sync   = p.get("lc_sync", {})
    streak    = lc_sync.get("streak", 0)
    total_lc  = lc_sync.get("total", 0)
    java_cnt  = lc_sync.get("java_problems", 0)
    today_sub = lc_sync.get("today_submissions", 0)

    # Week calc
    start = date(2026, 3, 19)
    delta = (date.today() - start).days
    wk    = min(max(1, delta // 7 + 1), 26)
    dn    = delta + 1

    # ── Load week plan ───────────────────────────────────────────────────────
    try:
        import sys
        sys.path.insert(0, str(BASE))
        from prep import WEEKS
        w = WEEKS.get(wk, WEEKS[26])
        theme = w.get("theme", "")
        dsa_topic = w.get("dsa", "")
    except Exception:
        theme = "Interview Prep"
        dsa_topic = "DSA Practice"

    # ── Today's drill problems ───────────────────────────────────────────────
    try:
        from intel.drill import get_drill
        drill = get_drill(week_num=wk, java_count=java_cnt, limit=3)
        drill_lines = [f"  #{p['lc_id']} {p['name']} [{p['difficulty']}] — {p['java_tip']}" for p in drill]
    except Exception:
        drill_lines = ["  Run: prep drill  to see today's problems"]

    # ── Trending from DB ─────────────────────────────────────────────────────
    trending_note = ""
    try:
        from intel.db import get_conn
        conn = get_conn()
        yesterday = str(date.today() - timedelta(days=1))
        rows = conn.execute("""
            SELECT e.company, er.round_type, er.topics
            FROM experience_rounds er
            JOIN experiences e ON er.experience_id = e.id
            WHERE e.date_scraped >= ?
            ORDER BY e.date_scraped DESC LIMIT 20
        """, (yesterday,)).fetchall()
        conn.close()

        company_counts = {}
        for row in rows:
            company_counts[row[0]] = company_counts.get(row[0], 0) + 1
        if company_counts:
            top_company = max(company_counts, key=company_counts.get)
            trending_note = f"🔥 {top_company} — {company_counts[top_company]} new exp yesterday"
    except Exception:
        trending_note = "Run: prep scrape  to get latest intel"

    # ── Behavioral reminder ──────────────────────────────────────────────────
    behavioral_story = _get_weakest_lp_story()

    # ── Build brief ──────────────────────────────────────────────────────────
    day_name = date.today().strftime("%A")
    streak_icon = "🔥" * min(streak, 3) if streak > 0 else "❌"

    brief["title"] = f"PrepForge Brief — {day_name}  D{dn}/184  W{wk}/26"
    brief["sections"] = {
        "streak": f"Streak: {streak}d {streak_icon} | LC: {total_lc} ({java_cnt} Java) | Today: {today_sub} done",
        "week": f"Week {wk}: {theme}  │  DSA: {dsa_topic}",
        "drill": "TODAY'S JAVA DRILL:\n" + "\n".join(drill_lines),
        "intel": f"INTEL: {trending_note}" if trending_note else "",
        "behavioral": f"BEHAVIORAL: {behavioral_story}" if behavioral_story else "",
    }

    # Short body for push notification (limited chars)
    brief["body"] = (
        f"Streak {streak}d {streak_icon} | LC {total_lc} ({java_cnt}J)\n"
        f"Today: {dsa_topic}\n"
        f"Drill: {drill_lines[0].strip() if drill_lines else 'prep drill'}"
    )

    return brief


def _get_weakest_lp_story() -> str:
    """Get the LP with the fewest stories for a reminder."""
    try:
        from intel.behavioral import run_lp_check
        result = run_lp_check()
        critical = result.get("critical", [])
        if critical:
            lp_key = critical[0]
            evaluation = result.get("evaluation", {})
            lp = evaluation.get(lp_key, {})
            return f"Review: {lp.get('name', lp_key)} — 0 stories ready"
        high = result.get("high_risk", [])
        if high:
            lp_key = high[0]
            lp = result.get("evaluation", {}).get(lp_key, {})
            return f"Strengthen: {lp.get('name', lp_key)} story"
    except Exception:
        pass
    return ""


def send_morning_brief(topic: str = None, verbose: bool = False) -> bool:
    """
    Send morning brief to ntfy.sh topic.

    Args:
        topic: ntfy.sh topic name (default: NTFY_TOPIC env var)
        verbose: print brief to stdout as well
    """
    topic = topic or os.environ.get("NTFY_TOPIC", "")
    if not topic:
        if verbose:
            print("\n  ⚠️  NTFY_TOPIC not set. Set it to enable push notifications:")
            print("    export NTFY_TOPIC=prepforge-yourname")
            print("  Then install ntfy app and subscribe to that topic.\n")
        return False

    brief = generate_brief_text(verbose=verbose)

    if verbose:
        print_brief(brief)

    try:
        token = os.environ.get("NTFY_TOKEN", "")

        # HTTP headers must be ASCII strings — strip/replace non-ASCII chars
        # Replace common non-ASCII chars before ASCII encoding
        safe_title = (brief["title"]
            .replace("—", "-").replace("–", "-")   # em/en dash -> -
            .replace("│", "|").replace("’", "'")   # box-draw, smart quote
            .encode("ascii", errors="ignore").decode("ascii"))

        # Build rich notification body: full sections, not just the short body
        full_body = "\n\n".join(filter(None, [
            brief.get("body", ""),
            brief["sections"].get("week", ""),
            brief["sections"].get("drill", ""),
            brief["sections"].get("intel", ""),
            brief["sections"].get("behavioral", ""),
        ])).strip()
        full_body = full_body[:4000]  # ntfy.sh 4096-char limit

        headers = {
            "Title":        safe_title,
            "Content-Type": "text/plain; charset=utf-8",
            "Priority":     "default",
            "Tags":         "books,computer",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        req = urllib.request.Request(
            f"{NTFY_BASE}/{topic}",
            data=full_body.encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10):
            pass
        return True
    except Exception as e:
        if verbose:
            print(f"  ⚠️  ntfy.sh push failed: {e}")
        return False


def print_brief(brief: dict = None):
    """Print the morning brief to terminal."""
    if brief is None:
        brief = generate_brief_text()

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  {brief['title'][:54]:<54}║
  ╚══════════════════════════════════════════════════════════╝
""")
    for key, content in brief["sections"].items():
        if content:
            print(f"  {content}")
            print()

    topic = os.environ.get("NTFY_TOPIC", "")
    if topic:
        print(f"  📱 Push sent to ntfy.sh/{topic}")
    else:
        print(f"  💡 Set NTFY_TOPIC=prepforge-yourname to get this on your phone")
    print()


def setup_ntfy_instructions():
    """Print setup instructions for ntfy.sh."""
    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  PUSH NOTIFICATIONS SETUP — ntfy.sh (FREE)             ║
  ╚══════════════════════════════════════════════════════════╝

  1. Install ntfy app on your phone:
     Android: https://play.google.com/store/apps/details?id=io.heckel.ntfy
     iOS:     https://apps.apple.com/us/app/ntfy/id1625396347

  2. Choose a topic name (it's like a channel):
     Example: senior_prep_sde2
     (Pick something unique — anyone who knows the name can subscribe)

  3. In the app: tap "+" → enter topic name → Subscribe

  4. Add to ~/.zshrc:
     export NTFY_TOPIC=senior_prep_sde2

  5. Test it:
     prep brief --send

  6. Automatic daily delivery at 8 AM IST is already configured
     (runs when PrepForge portal is running: prep portal)

  Optional: Private topic (password-protected)
     ntfy.sh → Sign up → Create private topic → set NTFY_TOKEN
""")
