#!/usr/bin/env python3
"""
generate_calendar.py — Generate ICS calendar for Jayanti's 6-month SDE Prep

Creates ~404 calendar events:
  • 10  milestone events  (Phase deadlines, key week starts)
  • 26  weekly overview   (Monday of each week — full week plan in description)
  • 184 morning DSA       (6:00–7:00 AM — today's problem + topic)
  • 184 evening study     (8:00–9:00 PM — tonight's study task)

Usage:
  python3 generate_calendar.py          → generates SDE_Prep_Calendar.ics
  python3 generate_calendar.py --open   → generates + opens in Notion Calendar / Google Calendar
  python3 generate_calendar.py --lite   → weekly + milestones only (no daily blocks)
"""

import sys, uuid
from datetime import date, datetime, timedelta
from pathlib import Path

BASE   = Path(__file__).parent
START  = date(2026, 3, 19)
OUTPUT = BASE / "SDE_Prep_Calendar.ics"

# ── Import weekly plan from prep.py ───────────────────────────────────────────
sys.path.insert(0, str(BASE))
try:
    from prep import WEEKS
except ImportError:
    print("❌ Could not import WEEKS from prep.py. Make sure prep.py is in the same folder.")
    sys.exit(1)

LITE = "--lite" in sys.argv

# ─── ICS Helpers ──────────────────────────────────────────────────────────────

def new_uid():
    return f"{uuid.uuid4().hex.upper()}@preptracker"

def esc(s):
    """Escape special characters for ICS."""
    return str(s).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n").replace("\r", "")

def fold(line, width=75):
    """Fold long lines per RFC 5545 — fold at character boundary to avoid breaking emoji."""
    chunks = []
    while len(line.encode("utf-8")) > width:
        # Find safe split point (don't break multi-byte chars)
        cut = width
        while len(line[:cut].encode("utf-8")) > width:
            cut -= 1
        chunks.append(line[:cut])
        line = " " + line[cut:]
    chunks.append(line)
    return "\r\n".join(chunks)

def fmt_date(d):
    return d.strftime("%Y%m%d")

def fmt_dt(d, h, m=0):
    """Floating local time (device timezone used — correct for IST)."""
    return d.strftime(f"%Y%m%dT{h:02d}{m:02d}00")

CRLF = "\r\n"

class ICS:
    def __init__(self):
        self.parts = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Jayanti Prep Tracker//SDE 6M Plan//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:SDE Prep 6M Plan 🎯",
            "X-WR-CALDESC:Jayanti Vishnoi — SDE-2/SDE-3 Interview Prep (Mar–Sep 2026)",
        ]
        self.count = 0

    def add_allday(self, d_start, d_end, summary, description=""):
        self.parts += [
            "BEGIN:VEVENT",
            f"DTSTART;VALUE=DATE:{fmt_date(d_start)}",
            f"DTEND;VALUE=DATE:{fmt_date(d_end)}",
            f"SUMMARY:{esc(summary)}",
            f"DESCRIPTION:{esc(description)}",
            f"UID:{new_uid()}",
            "END:VEVENT",
        ]
        self.count += 1

    def add_timed(self, d, h_start, h_end, summary, description=""):
        self.parts += [
            "BEGIN:VEVENT",
            f"DTSTART:{fmt_dt(d, h_start)}",
            f"DTEND:{fmt_dt(d, h_end)}",
            f"SUMMARY:{esc(summary)}",
            f"DESCRIPTION:{esc(description)}",
            f"UID:{new_uid()}",
            "END:VEVENT",
        ]
        self.count += 1

    def write(self, path):
        self.parts.append("END:VCALENDAR")
        raw = CRLF.join(fold(p) for p in self.parts)
        Path(path).write_text(raw, encoding="utf-8")

# ─── Build Calendar ───────────────────────────────────────────────────────────
cal = ICS()

# ── 1. MILESTONE EVENTS ───────────────────────────────────────────────────────
milestones = [
    (
        START,
        "🚀 SDE Prep Day 1 — 6 Months to Dream Offer",
        "Phase 1 starts today.\nGoal: First offer by June 19, 2026.\n"
        "Phase 2: Dream offer by September 19, 2026.\n\n"
        "Run: prep\nGuide: open GUIDE.md"
    ),
    (
        START + timedelta(weeks=1),
        "📝 Week 2: Java Core Internals",
        "Study: Section_01_Java_Core.md (Q1-Q25)\n"
        "Focus: HashMap internals, ConcurrentHashMap, CompletableFuture, GC types.\n"
        "DSA: Two Pointers, Sliding Window"
    ),
    (
        START + timedelta(weeks=3),
        "📬 Applications Open — Start Applying Now (Week 4)",
        "FROM THIS WEEK: Apply to Phase 1 companies daily.\n\n"
        "Targets: Razorpay, Juspay, CRED, MakeMyTrip, Meesho, Paytm\n\n"
        "Run: prep apply \"Company Name\"\n"
        "Goal: 10+ applications by end of this week."
    ),
    (
        START + timedelta(weeks=5),
        "🎭 Mock Interview Week — Week 6",
        "Do all 5 mock interview rounds this week.\n"
        "Record yourself. Watch back. Fix top 3 weak points.\n\n"
        "Round 1: Java Deep Dive (45 min timed)\n"
        "Round 3: System Design (pick from must-know list)\n"
        "Round 4: Past Work Deep Dive (record + watch)\n\n"
        "Reference: GSTN_Complete Part 3"
    ),
    (
        START + timedelta(weeks=10),
        "🔥 Interview Blitz Peak — Close First Offer",
        "Active interviews should be happening now.\n"
        "Log every question within 1 hour of each interview.\n"
        "Fix gaps immediately. Push for final rounds.\n\n"
        "Run: prep review\nRun: prep check"
    ),
    (
        date(2026, 6, 19),
        "🎯 PHASE 1 DEADLINE — First Offer Target",
        "TARGET: First job offer accepted by today.\n\n"
        "If offer received: Negotiate. Accept only if meets minimum bar. START PHASE 2.\n"
        "If not received: Diagnose. Expand list. Don't panic.\n\n"
        "Run: prep check\nRun: prep status"
    ),
    (
        date(2026, 6, 20),
        "🚀 Phase 2 Begins — Dream Role Prep",
        "Phase 2 starts NOW regardless of Phase 1 status.\n\n"
        "From today: 2 hours DSA daily (not 1). Hard problems mode.\n"
        "Targets: Amazon, Flipkart, Goldman Sachs, PhonePe, Google\n\n"
        "Run: prep plan"
    ),
    (
        START + timedelta(weeks=22),
        "🎯 Dream Applications Push — Week 23",
        "Apply to ALL dream companies this week.\n\n"
        "Amazon, Flipkart, Goldman, PhonePe, Swiggy, Google, Microsoft\n\n"
        "Get referrals: Find GSTN alumni on LinkedIn at target companies.\n"
        "Referral doubles callback rate.\n\n"
        "Run: prep status"
    ),
    (
        date(2026, 9, 14),
        "📊 Final Review — 5 Days to Programme End",
        "5 days left.\n\n"
        "Run: prep status → full programme review\n"
        "Run: prep check → final health check\n\n"
        "Sleep well before every final round.\n"
        "8 hours sleep > 1 more practice problem at this stage."
    ),
    (
        date(2026, 9, 19),
        "🏆 PHASE 2 DEADLINE — Dream Offer Target",
        "TARGET: Dream offer signed by today.\n\n"
        "The 6-month journey is complete.\n"
        "The habits built over 184 days compound for your entire career.\n\n"
        "Run: prep status → see the full journey"
    ),
]

for d, summary, desc in milestones:
    cal.add_allday(d, d + timedelta(days=1), summary, desc)

print(f"  ✅ {len(milestones)} milestone events added")

# ── 2. WEEKLY OVERVIEW EVENTS (Monday all-day, full plan in description) ──────
for wk in range(1, 27):
    w      = WEEKS[wk]
    monday = START + timedelta(weeks=wk - 1)
    sunday = monday + timedelta(days=6)

    tasks  = "\n".join(f"{i+1}. {t}" for i, t in enumerate(w["tasks"]))
    probs  = " | ".join(w["lc_problems"][:5])
    if len(w["lc_problems"]) > 5:
        probs += " ..."

    desc = (
        f"PHASE {w['phase']}  |  MONTH {w['month']}\n"
        f"{'━'*40}\n\n"
        f"📊 DSA TOPIC: {w['dsa']}  [{w['diff']}]\n"
        f"📊 WEEKLY TARGET: {w['lc_target']} problems\n"
        f"📊 PROBLEMS: {probs}\n\n"
        f"📚 STUDY TASKS:\n{tasks}\n\n"
        f"⚡ TIP: {w['tip']}\n\n"
        f"Run: prep plan  →  today's full plan\n"
        f"Run: prep check →  health check"
    )

    summary = f"Week {wk}/26 [{w['phase']}]: {w['theme']}"
    cal.add_allday(monday, sunday + timedelta(days=1), summary, desc)

print(f"  ✅ 26 weekly overview events added")

# ── 3. DAILY MORNING DSA BLOCKS (6:00–7:00 AM) ────────────────────────────────
if not LITE:
    for day_idx in range(184):
        d   = START + timedelta(days=day_idx)
        wk  = min(26, day_idx // 7 + 1)
        w   = WEEKS[wk]

        probs      = w.get("lc_problems", [w["dsa"]])
        prob_today = probs[day_idx % len(probs)]
        day_in_wk  = day_idx % 7 + 1

        summary = f"☀️ DSA: {prob_today}  [{w['diff']}]"
        desc    = (
            f"Day {day_idx+1}/184  |  Week {wk}/26  |  Day {day_in_wk}/7\n\n"
            f"Topic: {w['dsa']}\n"
            f"Problem: {prob_today}\n"
            f"Difficulty: {w['diff']}\n"
            f"Weekly target: {w['lc_target']} problems\n\n"
            f"After solving:\n"
            f"  prep lc \"{prob_today}\"\n\n"
            f"LeetCode: https://leetcode.com/u/hasbrovish95"
        )
        cal.add_timed(d, 6, 7, summary, desc)

    print(f"  ✅ 184 morning DSA blocks added (6:00–7:00 AM)")

# ── 4. DAILY EVENING STUDY BLOCKS (8:00–9:00 PM) ─────────────────────────────
if not LITE:
    for day_idx in range(184):
        d   = START + timedelta(days=day_idx)
        wk  = min(26, day_idx // 7 + 1)
        w   = WEEKS[wk]

        task_today = w["tasks"][day_idx % len(w["tasks"])]
        day_in_wk  = day_idx % 7 + 1

        # Vary the evening focus by day of week
        day_name  = d.strftime("%A")
        focus_map = {
            "Monday":    "New topic — first read",
            "Tuesday":   "Deep dive — code examples",
            "Wednesday": "Q&A — question bank practice",
            "Thursday":  "System Design or LLD practice",
            "Friday":    "Weak area review",
            "Saturday":  "Mock interview or full system design",
            "Sunday":    "prep review → plan next week",
        }
        focus = focus_map.get(day_name, "Study session")

        summary = f"📚 Study: {w['theme'][:40]}"
        desc    = (
            f"Day {day_idx+1}/184  |  Week {wk}/26  |  {day_name}\n\n"
            f"Today's focus: {focus}\n\n"
            f"Tonight's task:\n{task_today}\n\n"
            f"All tasks this week:\n" +
            "\n".join(f"• {t}" for t in w["tasks"]) +
            f"\n\nAfter studying:\n  prep log"
        )
        cal.add_timed(d, 20, 21, summary, desc)

    print(f"  ✅ 184 evening study blocks added (8:00–9:00 PM)")

# ── Write ICS file ─────────────────────────────────────────────────────────────
cal.write(OUTPUT)
size_kb = OUTPUT.stat().st_size // 1024

print()
print("╔══════════════════════════════════════════════════════════╗")
print("║              CALENDAR GENERATED SUCCESSFULLY!           ║")
print("╚══════════════════════════════════════════════════════════╝")
print()
print(f"  File:    {OUTPUT}")
print(f"  Events:  {cal.count} total")
print(f"  Size:    {size_kb} KB")
print()
print("  HOW TO IMPORT:")
print()
print("  Option A — Notion Calendar (your app):")
print("    1. Open Notion Calendar")
print("    2. Settings → Calendars → Import")
print("    3. Select SDE_Prep_Calendar.ics")
print()
print("  Option B — Google Calendar (via browser):")
print("    1. calendar.google.com → Settings (gear) → Import & Export")
print("    2. Import → Select SDE_Prep_Calendar.ics")
print("    3. Choose which calendar to add to → Import")
print()
print("  Option C — Auto-open now:")
print("    python3 generate_calendar.py --open")
print()
print("  Option D — Lite version (weekly + milestones only, no daily blocks):")
print("    python3 generate_calendar.py --lite")
print()

# ── Open in default calendar app if --open ────────────────────────────────────
if "--open" in sys.argv:
    import subprocess
    print("  Opening SDE_Prep_Calendar.ics...")
    subprocess.run(["open", str(OUTPUT)])
    print("  → Approve the import when prompted in the app.")
    print()
