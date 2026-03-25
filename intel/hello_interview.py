"""
Hello Interview Course Tracker.

Maps hellointerview.com course structure to Jayanti's 26-week prep plan.
Tracks lesson completion in progress.json.

Usage:
  from intel.hello_interview import get_week_lessons, mark_done, get_progress
  print_hi_week(week_num)
"""

import json
from pathlib import Path

BASE         = Path(__file__).parent.parent
HI_JSON      = BASE / "data" / "hellointerviewcourse.json"
PROG_FILE    = BASE / "logs" / "progress.json"
HI_BASE_URL  = "https://www.hellointerview.com"

# ── Week assignments per (course_id, section_name) ───────────────────────────
# Aligned with MASTER_6MONTH_PROGRAMME.md phase/week themes
# Format: (start_week, end_week) — lessons distributed evenly across range

SECTION_WEEKS = {
    # ── DSA (weeks 1–10) ─────────────────────────────────────────────────────
    ("dsa", "Two Pointers"):                (1, 1),
    ("dsa", "Sliding Window"):              (1, 2),
    ("dsa", "Intervals"):                   (2, 2),
    ("dsa", "Stack"):                       (2, 3),
    ("dsa", "Linked List"):                 (3, 3),
    ("dsa", "Binary Search"):               (3, 4),
    ("dsa", "Heap"):                        (4, 5),
    ("dsa", "Depth-First Search (DFS)"):    (5, 6),
    ("dsa", "Breadth-First Search (BFS)"): (6, 7),
    ("dsa", "Backtracking"):                (7, 8),
    ("dsa", "Graphs"):                      (8, 9),
    ("dsa", "Dynamic Programming"):         (9, 11),
    ("dsa", "Greedy Algorithms"):           (11, 11),
    ("dsa", "Trie"):                        (11, 12),
    ("dsa", "Prefix Sum"):                  (12, 12),
    ("dsa", "Matrices"):                    (12, 12),

    # ── Low Level Design (weeks 4–13) ────────────────────────────────────────
    ("low-level-design", "In a Hurry"):         (4, 5),
    ("low-level-design", "Concurrency"):        (5, 6),
    ("low-level-design", "Problem Breakdowns"): (10, 13),

    # ── System Design (weeks 1–26) ───────────────────────────────────────────
    ("system-design", "In a Hurry"):                  (1, 2),
    ("system-design", "Core Concepts"):               (9, 12),
    ("system-design", "Patterns"):                    (12, 14),
    ("system-design", "Key Technologies (Deep Dives)"): (13, 16),
    ("system-design", "Advanced Topics"):             (16, 17),
    ("system-design", "Question Breakdowns"):         (14, 26),

    # ── Behavioral (weeks 1–26, ongoing) ─────────────────────────────────────
    ("behavioral", "Course"):         (1, 5),
    ("behavioral", "Story Builder"):  (4, 26),
}

# Course display order (ML System Design skipped — not relevant for SDE-2/3)
COURSE_ORDER   = ["system-design", "dsa", "low-level-design", "behavioral"]
COURSE_COLORS  = {
    "system-design":    "🏗️",
    "dsa":              "⌗",
    "low-level-design": "◆",
    "behavioral":       "◇",
}
DIFF_ICON = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴", "": "◦"}


# ── Data loading ──────────────────────────────────────────────────────────────

def load_courses() -> list:
    if not HI_JSON.exists():
        return []
    return json.loads(HI_JSON.read_text(encoding="utf-8"))["courses"]


def _build_curriculum() -> list:
    """Return flat ordered list of all lessons with week assignments."""
    courses_by_id = {c["id"]: c for c in load_courses()}
    curriculum = []

    for course_id in COURSE_ORDER:
        course = courses_by_id.get(course_id)
        if not course:
            continue

        for section in course.get("sections", []):
            section_name = section["section"]
            key = (course_id, section_name)
            start_w, end_w = SECTION_WEEKS.get(key, (13, 20))
            is_problem = section.get("type") == "problem_breakdowns"

            lessons = [l for l in section.get("lessons", []) if l.get("url")]
            n = len(lessons)
            for i, lesson in enumerate(lessons):
                if n > 1 and end_w > start_w:
                    week = start_w + round(i * (end_w - start_w) / (n - 1))
                else:
                    week = start_w

                curriculum.append({
                    "week":       week,
                    "course_id":  course_id,
                    "course":     course["title"],
                    "section":    section_name,
                    "title":      lesson["title"],
                    "url":        HI_BASE_URL + lesson["url"],
                    "key":        lesson["url"],          # relative URL as stable key
                    "difficulty": lesson.get("difficulty", ""),
                    "type":       "problem" if is_problem else lesson.get("type", "lesson"),
                })

    return sorted(curriculum, key=lambda x: (x["week"], COURSE_ORDER.index(x["course_id"])))


# Cache after first call
_CURRICULUM: list = []

def get_curriculum() -> list:
    global _CURRICULUM
    if not _CURRICULUM:
        _CURRICULUM = _build_curriculum()
    return _CURRICULUM


# ── Progress persistence ───────────────────────────────────────────────────────

def _load_progress() -> dict:
    try:
        return json.loads(PROG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _save_progress(prog: dict):
    PROG_FILE.parent.mkdir(exist_ok=True)
    PROG_FILE.write_text(json.dumps(prog, indent=2, default=str, ensure_ascii=False), encoding="utf-8")

def _hi_state() -> dict:
    return _load_progress().get("hi_course", {"done": [], "skipped": []})

def _save_hi_state(state: dict):
    prog = _load_progress()
    prog["hi_course"] = state
    _save_progress(prog)


# ── Core API ──────────────────────────────────────────────────────────────────

def get_week_lessons(week: int) -> list:
    """Return all lessons assigned to a given week."""
    return [l for l in get_curriculum() if l["week"] == week]


def get_undone_lessons(week: int) -> list:
    """Return lessons for the week that are not yet done."""
    done_keys = set(_hi_state().get("done", []))
    return [l for l in get_week_lessons(week) if l["key"] not in done_keys]


def get_today_lesson(week: int):
    """Return the first undone lesson for this week (the daily target)."""
    undone = get_undone_lessons(week)
    return undone[0] if undone else None


def mark_done(lesson_key: str) -> bool:
    """Mark a lesson as done by its relative URL key."""
    state = _hi_state()
    if lesson_key not in state["done"]:
        state["done"].append(lesson_key)
        _save_hi_state(state)
        return True
    return False


def mark_done_by_index(week: int, idx: int = 0) -> dict:
    """Mark the idx-th undone lesson for the week as done. Returns the lesson."""
    undone = get_undone_lessons(week)
    if not undone or idx >= len(undone):
        return {}
    lesson = undone[idx]
    mark_done(lesson["key"])
    return lesson


def get_progress() -> dict:
    """Return overall progress stats per course."""
    curriculum    = get_curriculum()
    done_keys     = set(_hi_state().get("done", []))
    total         = len(curriculum)
    total_done    = len([l for l in curriculum if l["key"] in done_keys])

    by_course = {}
    for l in curriculum:
        cid = l["course_id"]
        if cid not in by_course:
            by_course[cid] = {"course": l["course"], "total": 0, "done": 0, "problems": 0, "problems_done": 0}
        by_course[cid]["total"] += 1
        if l["key"] in done_keys:
            by_course[cid]["done"] += 1
        if l["type"] == "problem":
            by_course[cid]["problems"] += 1
            if l["key"] in done_keys:
                by_course[cid]["problems_done"] += 1

    return {
        "total":        total,
        "total_done":   total_done,
        "pct":          round(total_done / max(total, 1) * 100),
        "by_course":    by_course,
    }


def get_week_summary(week: int) -> dict:
    """Return a summary of lessons/problems for a week with done status."""
    curriculum = get_week_lessons(week)
    done_keys  = set(_hi_state().get("done", []))
    lessons    = []
    for l in curriculum:
        lessons.append({**l, "done": l["key"] in done_keys})
    done_count  = sum(1 for l in lessons if l["done"])
    return {
        "week":   week,
        "total":  len(lessons),
        "done":   done_count,
        "pct":    round(done_count / max(len(lessons), 1) * 100),
        "lessons": lessons,
    }


# ── Terminal display ──────────────────────────────────────────────────────────

def print_hi_week(week: int):
    """Print this week's Hello Interview study plan."""
    summary = get_week_summary(week)
    prog    = get_progress()
    today   = get_today_lesson(week)

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  HELLO INTERVIEW — WEEK {week:<2} STUDY PLAN                  ║
  ╚══════════════════════════════════════════════════════════╝

  Overall: {prog['total_done']}/{prog['total']} lessons done ({prog['pct']}%)
  This week: {summary['done']}/{summary['total']} done ({summary['pct']}%)
""")

    if today:
        icon = COURSE_COLORS.get(today["course_id"], "◦")
        diff = DIFF_ICON.get(today["difficulty"], "◦")
        print(f"  ▶ TODAY'S LESSON: {icon} [{today['section']}]")
        print(f"    {diff} {today['title']}")
        print(f"    {today['url']}")
        print()

    # Group by course
    by_course: dict = {}
    for l in summary["lessons"]:
        cid = l["course_id"]
        by_course.setdefault(cid, []).append(l)

    for cid in COURSE_ORDER:
        lessons = by_course.get(cid, [])
        if not lessons:
            continue
        icon  = COURSE_COLORS.get(cid, "◦")
        done  = sum(1 for l in lessons if l["done"])
        print(f"  {icon} {lessons[0]['course']}  [{done}/{len(lessons)}]")
        for l in lessons:
            status = "✅" if l["done"] else "  ○"
            diff   = f" {DIFF_ICON[l['difficulty']]}" if l["difficulty"] else ""
            print(f"    {status} {l['title']}{diff}")
        print()

    print(f"  Mark done: prep hi done")
    print(f"  Progress:  prep hi progress\n")


def print_hi_progress():
    """Print overall Hello Interview course progress."""
    prog = get_progress()

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  HELLO INTERVIEW — OVERALL PROGRESS                     ║
  ╚══════════════════════════════════════════════════════════╝

  Total: {prog['total_done']}/{prog['total']} ({prog['pct']}%)
""")

    for cid in COURSE_ORDER:
        v    = prog["by_course"].get(cid)
        if not v:
            continue
        icon = COURSE_COLORS.get(cid, "◦")
        pct  = round(v["done"] / max(v["total"], 1) * 100)
        bar  = "█" * (pct // 5) + "░" * (20 - pct // 5)
        print(f"  {icon} {v['course']:<38} {v['done']:>3}/{v['total']:<3} [{bar}] {pct}%")
        if v["problems"] > 0:
            print(f"     └ Problems: {v['problems_done']}/{v['problems']} solved")
    print()


def list_week_range(start: int = 1, end: int = 26):
    """Print high-level curriculum map across all weeks."""
    print(f"\n  HELLO INTERVIEW — 26-WEEK CURRICULUM MAP\n  {'─'*55}")
    curriculum = get_curriculum()
    done_keys  = set(_hi_state().get("done", []))

    for week in range(start, end + 1):
        lessons = [l for l in curriculum if l["week"] == week]
        if not lessons:
            continue
        done   = sum(1 for l in lessons if l["key"] in done_keys)
        groups: dict = {}
        for l in lessons:
            groups.setdefault(l["section"], 0)
            groups[l["section"]] += 1
        topics = ", ".join(f"{s}({n})" for s, n in groups.items())
        print(f"  Week {week:>2}  {done}/{len(lessons):>2}  {topics}")
    print()
