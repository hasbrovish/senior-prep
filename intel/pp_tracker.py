"""
Programming Pathshala Course Tracker.

Tracks progress through the warplan-aligned PP watch order
(DSA -> LLD -> Java Springboot -> System Design, 26 weeks).

Usage:
  from intel.pp_tracker import run_pp_command
  run_pp_command(args)           # dispatches: today / list / progress / week N / done X

  from intel.pp_tracker import get_week_module, PP_WATCH_ORDER
"""

import json
from datetime import date
from pathlib import Path

BASE      = Path(__file__).parent.parent
PP_FILE   = BASE / "data" / "programming_pathshala_courses.json"
PROG_FILE = BASE / "logs" / "progress.json"
START     = date(2026, 3, 19)

# --- PP Watch Order (from MASTER_16H_WARPLAN.md) ------------------------------
# Keys are tuples of week numbers that share the same module focus.
PP_WATCH_ORDER = {
    (1, 2):         {"course": "DSA",            "module": "Module 3",  "focus": "Binary Search, Sorting, Two Pointers",                     "hrs": "4 hrs/week"},
    (3, 4):         {"course": "DSA",            "module": "Module 4",  "focus": "Hashing, Stacks, Linked Lists, Binary Trees",              "hrs": "6 hrs/week"},
    (5, 6):         {"course": "DSA",            "module": "Module 5",  "focus": "Graphs: BFS/DFS/Dijkstra/Topo",                            "hrs": "5 hrs/week"},
    (7, 8):         {"course": "DSA",            "module": "Module 6",  "focus": "DP: all classical",                                        "hrs": "6 hrs/week"},
    (9, 10):        {"course": "DSA",            "module": "Module 6",  "focus": "Heaps, Greedy",                                            "hrs": "4 hrs/week"},
    (11, 12):       {"course": "LLD",            "module": "Module 7",  "focus": "SOLID + 5 Design Patterns",                                "hrs": "5 hrs/week"},
    (13,):          {"course": "LLD",            "module": "Module 8",  "focus": "Case Studies: Parking Lot, Chess, ATM",                    "hrs": "5 hrs"},
    (14, 15, 16):   {"course": "LLD",            "module": "Module 8",  "focus": "Concurrency - race conditions, locks, producer-consumer",  "hrs": "6 hrs/week"},
    (17, 18):       {"course": "Java Springboot","module": "Module 11", "focus": "IoC, Spring MVC, Hibernate, JDBC",                        "hrs": "5 hrs/week"},
    (19, 20):       {"course": "System Design",  "module": "Module 9",  "focus": "OS fundamentals: scheduling, memory, paging",              "hrs": "4 hrs/week"},
    (21, 22):       {"course": "Java Springboot","module": "Module 11", "focus": "Transactions, Security, Projects",                        "hrs": "5 hrs/week"},
    (23, 24):       {"course": "LLD",            "module": "Module 8",  "focus": "Case Studies: Elevator, E-Commerce, Stock Trading",        "hrs": "4 hrs/week"},
    (25, 26):       {"course": "Review",         "module": "All",       "focus": "Weak areas only",                                         "hrs": "2 hrs/week"},
}


# --- Helpers ------------------------------------------------------------------

def current_week() -> int:
    delta = (date.today() - START).days
    return min(max(1, delta // 7 + 1), 26)


def get_week_module(week_num: int) -> dict:
    """Return the PP phase info for a given programme week."""
    for weeks, info in PP_WATCH_ORDER.items():
        if week_num in weeks:
            return info
    return {"course": "Review", "module": "All", "focus": "Revision", "hrs": "2 hrs/week"}


def module_key(info: dict) -> str:
    return f"{info['course']} {info['module']}"


def _load_progress() -> dict:
    try:
        return json.loads(PROG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_progress(prog: dict) -> None:
    PROG_FILE.write_text(
        json.dumps(prog, indent=2, default=str, ensure_ascii=False),
        encoding="utf-8",
    )


def _load_course_data() -> dict:
    if PP_FILE.exists():
        try:
            return json.loads(PP_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


# --- Sub-commands -------------------------------------------------------------

def cmd_done(module_name: str) -> None:
    prog = _load_progress()
    pp_done: list = prog.get("pp_modules_done", [])
    if module_name not in pp_done:
        pp_done.append(module_name)
        prog["pp_modules_done"] = pp_done
        _save_progress(prog)
    print(f"\n  Marked as watched: {module_name}")
    print(f"     Total PP modules watched: {len(pp_done)}\n")


def cmd_today(wk: int, pp_done: list) -> None:
    info = get_week_module(wk)
    key = module_key(info)
    status = "DONE" if key in pp_done else "IN PROGRESS"
    print(f"\n  PP TODAY -- Week {wk}")
    print(f"  {status}: {info['course']} -- {info['module']}")
    print(f"  Focus: {info['focus']}")
    print(f"  Time:  {info['hrs']}")
    print(f"\n  When done: prep pp done \"{key}\"")
    print(f"  All modules: prep pp list")
    print(f"  Progress:    prep pp progress\n")


def cmd_list(pp_done: list) -> None:
    print(f"\n  PROGRAMMING PATHSHALA -- OPTIMISED WATCH ORDER\n")
    seen: set = set()
    for weeks, info in PP_WATCH_ORDER.items():
        key = module_key(info)
        if key in seen:
            continue
        seen.add(key)
        wk_range = f"Wk {min(weeks)}-{max(weeks)}" if len(weeks) > 1 else f"Wk {weeks[0]}"
        done_marker = "[done]" if key in pp_done else "      "
        print(f"  {done_marker} [{wk_range:<8}] {info['course']} {info['module']}: {info['focus']}")
        print(f"              -> {info['hrs']}")
    print(f"\n  Total watched: {len(pp_done)} module phases")
    print(f"  Mark done:    prep pp done \"DSA Module 3\"\n")


def cmd_progress(wk: int, pp_done: list) -> None:
    total = len(PP_WATCH_ORDER)
    done_count = sum(
        1 for weeks, info in PP_WATCH_ORDER.items()
        if module_key(info) in pp_done
    )
    pct = int(done_count / total * 100) if total else 0
    bar = "X" * (pct // 5) + "." * (20 - pct // 5)
    print(f"\n  PP Course Progress: [{bar}] {pct}%  ({done_count}/{total} phases)\n")
    current = get_week_module(wk)
    print(f"  Current week ({wk}): {current['course']} {current['module']}")
    print(f"  Focus: {current['focus']}")
    print(f"  Time:  {current['hrs']}\n")


def cmd_week(target_wk: int) -> None:
    info = get_week_module(target_wk)
    print(f"\n  Week {target_wk} -- {info['course']} {info['module']}")
    print(f"  Focus: {info['focus']}")
    print(f"  Time:  {info['hrs']}\n")
    data = _load_course_data()
    mod_num = info["module"].replace("Module ", "").strip()
    for course in data.get("courses", []):
        if info["course"].lower() in course.get("course_name", "").lower():
            for mod in course.get("modules", []):
                if str(mod.get("module_number", "")) == mod_num:
                    print(f"  Topics in {info['module']}:")
                    for t in mod.get("topics", []):
                        print(f"    - {t.get('topic_name', 'Unknown')}  ({t.get('estimated_duration', '')})")
                    break


# --- Dispatcher ---------------------------------------------------------------

def run_pp_command(args: list) -> None:
    """Entry point called by prep.py cmd_pp."""
    if not PP_FILE.exists():
        print("\n  programming_pathshala_courses.json not found at project root.\n")
        return

    prog    = _load_progress()
    pp_done = prog.get("pp_modules_done", [])
    wk      = current_week()
    sub     = args[0].lower() if args else "today"

    if sub in ("done", "d") and len(args) > 1:
        cmd_done(" ".join(args[1:]))
    elif sub in ("list", "all", "modules"):
        cmd_list(pp_done)
    elif sub in ("progress", "prog", "p"):
        cmd_progress(wk, pp_done)
    elif sub in ("week", "w"):
        target = int(args[1]) if len(args) > 1 and args[1].isdigit() else wk
        cmd_week(target)
    else:
        cmd_today(wk, pp_done)
