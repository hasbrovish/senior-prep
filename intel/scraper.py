"""
Scraper orchestrator — runs all sources, normalizes data, stores in DB.

Usage:
  python -m intel.scraper                  # scrape all sources
  python -m intel.scraper --source reddit  # scrape specific source
  python -m intel.scraper --company google # scrape + filter for company
"""

import sys
import time
from datetime import datetime

from . import db
from .sources import leetcode_discuss, reddit, enginebogie, hackernews


SCRAPERS = {
    "leetcode_discuss": {"fn": leetcode_discuss.scrape, "label": "LeetCode Discuss"},
    "reddit":           {"fn": reddit.scrape,           "label": "Reddit (6 subs + comments)"},
    "hackernews":       {"fn": hackernews.scrape,       "label": "HackerNews (Algolia)"},
    "enginebogie":      {"fn": enginebogie.scrape,      "label": "enginebogie.com"},
}


def run_scraper(source_name=None, verbose=True):
    """Run scrapers and store results in DB.

    Args:
        source_name: specific source to scrape, or None for all
        verbose: print progress to stdout

    Returns:
        dict with counts per source
    """
    db.init_db()
    stats = {}

    sources = {source_name: SCRAPERS[source_name]} if source_name and source_name in SCRAPERS else SCRAPERS

    for key, src in sources.items():
        if verbose:
            print(f"\n  ⏳ Scraping {src['label']}...", end=" ", flush=True)

        start = time.time()
        try:
            experiences = src["fn"]()
        except Exception as e:
            if verbose:
                print(f"❌ Error: {e}")
            stats[key] = {"fetched": 0, "inserted": 0, "error": str(e)}
            continue

        elapsed = time.time() - start
        inserted = 0

        for exp in experiences:
            try:
                exp_id = db.insert_experience(exp)
                if exp_id:
                    inserted += 1
            except Exception as e:
                pass  # Duplicate or DB error — skip silently

        stats[key] = {"fetched": len(experiences), "inserted": inserted, "time": f"{elapsed:.1f}s"}
        if verbose:
            print(f"✅ {len(experiences)} fetched, {inserted} new ({elapsed:.1f}s)")

    return stats


def print_summary():
    """Print a summary of what's in the DB."""
    stats = db.get_overall_stats()

    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║       INTERVIEW INTELLIGENCE DATABASE                    ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    print(f"\n  Total experiences:  {stats['total_experiences']}")
    print(f"  Unique companies:   {stats['companies']}")

    if stats.get("sources"):
        print(f"\n  By source:")
        for row in stats["sources"]:
            print(f"    {row['source']:<25} {row['cnt']} experiences")

    if stats.get("recent"):
        print(f"\n  Most recent:")
        for row in stats["recent"]:
            result_icon = "✅" if row["overall_result"] == "offer" else ("❌" if row["overall_result"] == "reject" else "❔")
            print(f"    {result_icon} {row['company']:<18} {row['role']:<8} {row['date_scraped']}")
    print()


def manual_add_experience():
    """Interactively add an interview experience you found."""
    print(f"\n  ── ADD INTERVIEW EXPERIENCE ──────────────────────────────")
    print(f"  Found an experience on Blind/Medium/Discord? Log it here.\n")

    try:
        source   = input("  Source (blind/medium/discord/other): ").strip() or "manual"
        company  = input("  Company: ").strip()
        role     = input("  Role (SDE-1/SDE-2/SDE-3): ").strip() or "SDE-2"
        result   = input("  Result (offer/reject/unknown): ").strip() or "unknown"
        url_link = input("  URL (optional): ").strip()
        notes    = input("  Notes (key questions, tips): ").strip()

        # Rounds
        rounds = []
        print("  Add rounds (blank to finish):")
        r_num = 1
        while True:
            r_type = input(f"    Round {r_num} type (dsa/sd/lld/behavioral/blank to stop): ").strip()
            if not r_type:
                break
            r_q = input(f"    Round {r_num} question/topic: ").strip()
            r_diff = input(f"    Round {r_num} difficulty (easy/medium/hard): ").strip()
            rounds.append({
                "round_num": r_num, "round_type": r_type,
                "question": r_q, "difficulty": r_diff,
                "topics": [], "outcome": None,
            })
            r_num += 1

        exp = {
            "source": source, "source_id": f"manual_{int(time.time())}",
            "company": company, "role": role,
            "title": f"{company} {role} Interview",
            "body_raw": notes, "overall_result": result,
            "url": url_link, "rounds": rounds,
            "tips": notes,
        }

        exp_id = db.insert_experience(exp)
        print(f"\n  ✅ Saved experience #{exp_id}: {company} {role}")
        print(f"     {len(rounds)} round(s) logged.")

    except (EOFError, KeyboardInterrupt):
        print("\n  Cancelled.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--source" in args:
        idx = args.index("--source")
        src = args[idx + 1] if idx + 1 < len(args) else None
        run_scraper(source_name=src)
    elif "--add" in args:
        manual_add_experience()
    elif "--stats" in args:
        print_summary()
    else:
        run_scraper()
        print_summary()
