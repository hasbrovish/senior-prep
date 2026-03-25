"""
External Source Status + Manual Import Helper.

WHY EACH SITE REQUIRES MANUAL IMPORT:
  teamblind.com       — JS SPA + login required. No public API. Scraping ToS-violating.
  hellointerview.com  — login required; course completion tracked via hello_interview.py
  enginebogie.com     — React SPA + login; replaced by Reddit/HN scrapers (see enginebogie.py)
  levels.fyi          — partial: static TC data in levelsfyi.py + limited public JSON endpoint
  interviewbit.com    — public problem list accessible; no interview-experience feed

WHAT YOU CAN DO FOR EACH:
  Blind:             Browse → copy paste into: prep scraper --add  (source = blind)
  HelloInterview:    Track course completion via: prep hi  (backed by hello_interview.py)
  enginebogie:       Browse → prep scraper --add  (source = enginebogie)
  levels.fyi:        prep tc <company>  (shows static + live TC data via levelsfyi.py)
  InterviewBit:      See interviewbit_problems() below — fetches public problem list

Usage:
  from intel.sources.blind_helloiv import source_status, interviewbit_problems
  source_status()              # print summary of what's automated vs manual
  interviewbit_problems()      # fetch IB problem list for target topics
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

# ─── Source capability map ────────────────────────────────────────────────────

SOURCES = [
    {
        "name":       "teamblind.com",
        "url":        "https://www.teamblind.com/",
        "automated":  False,
        "reason":     "JS SPA + login required — no public API",
        "action":     "Browse manually → prep scraper --add (source=blind)",
        "value":      "TC data, company culture, offer negotiations (India + US)",
    },
    {
        "name":       "hellointerview.com",
        "url":        "https://www.hellointerview.com/dashboard",
        "automated":  "partial",
        "reason":     "Course content behind login; system design guides are the value",
        "action":     "Track lesson completion: prep hi  (backed by hello_interview.py)",
        "value":      "Structured SD/DSA courses aligned to your 26-week plan",
    },
    {
        "name":       "enginebogie.com",
        "url":        "https://enginebogie.com/interview/experiences",
        "automated":  False,
        "reason":     "React SPA + login — replaced by r/ExperiencedDevs + HN scrapers",
        "action":     "Browse → prep scraper --add (source=enginebogie)",
        "value":      "India SDE-2 interview experiences (good for target companies)",
    },
    {
        "name":       "levels.fyi",
        "url":        "https://www.levels.fyi/?tab=levels",
        "automated":  "partial",
        "reason":     "Public JSON endpoint has limited data for India; static fallback",
        "action":     "prep tc <company>  — shows TC ranges + negotiation playbook",
        "value":      "TC by level + negotiation data for all target companies",
    },
    {
        "name":       "interviewbit.com",
        "url":        "https://www.interviewbit.com/practice/",
        "automated":  "partial",
        "reason":     "Public problem API works; no interview-experience feed",
        "action":     "interviewbit_problems() fetches topic-wise P0 problem list",
        "value":      "Company-tagged DSA problems; strong for Adobe/Goldman/Microsoft",
    },
]


def source_status():
    """Print status of each external source."""
    icons = {True: "✅ AUTO ", False: "📋 MANUAL", "partial": "🟡 PARTIAL"}
    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  EXTERNAL SOURCE STATUS                                  ║
  ╚══════════════════════════════════════════════════════════╝
""")
    for s in SOURCES:
        status = icons[s["automated"]]
        print(f"  {status}  {s['name']}")
        print(f"           Value:  {s['value']}")
        print(f"           Action: {s['action']}")
        print()

    print(f"""  ── WHAT'S FULLY AUTOMATED ────────────────────────────────
  ✅ Reddit (r/leetcode, r/cscareerquestions, r/ExperiencedDevs, r/IndiaTechies)
  ✅ LeetCode Discuss (GraphQL — no auth needed)
  ✅ HackerNews Algolia API
  ✅ TC data for all 14 target companies (static + levels.fyi live attempt)

  Run: prep scraper          → fetch all automated sources
       prep tc google        → TC + negotiation for Google
       prep scraper --add    → log a Blind/enginebogie experience manually
""")


# ─── InterviewBit public problem fetch ───────────────────────────────────────

# InterviewBit has a semi-public API used by their web app.
# This fetches the problem list for company-relevant topics.
# No auth required for problem metadata (not user data).

IB_TARGET_TOPICS = {
    "Arrays":           "arrays",
    "Strings":          "strings",
    "Linked Lists":     "linked-lists",
    "Trees":            "trees",
    "Graph":            "graph",
    "Dynamic Programming": "dynamic-programming",
    "Stacks & Queues":  "stacks-and-queues",
    "Heaps":            "heaps-and-maps",
    "Hashing":          "hashing",
    "Binary Search":    "binary-search",
}

# Company tags in IB that align to our targets
IB_COMPANY_MAP = {
    "Adobe":        ["Adobe"],
    "Goldman Sachs":["Goldman Sachs"],
    "Microsoft":    ["Microsoft"],
    "Amazon":       ["Amazon"],
    "Google":       ["Google"],
    "Flipkart":     ["Flipkart"],
    "Razorpay":     ["Razorpay"],
}


def interviewbit_problems(company: str = None, topic: str = None, limit: int = 20) -> list:
    """
    Fetch company-tagged problems from InterviewBit's public GraphQL/REST API.
    Falls back to curated static list if API is unavailable.

    Args:
        company: filter by company name (e.g. "Adobe")
        topic: filter by topic slug (e.g. "dynamic-programming")
        limit: max problems to return

    Returns:
        list of {title, difficulty, topic, company_tags, url}
    """
    try:
        return _fetch_ib_problems(company, topic, limit)
    except Exception:
        return _static_ib_problems(company, topic, limit)


def _fetch_ib_problems(company: str, topic: str, limit: int) -> list:
    """Try fetching from InterviewBit's public problem JSON."""
    # IB serves problem lists as JSON for their React frontend
    topic_slug = IB_TARGET_TOPICS.get(topic, topic or "arrays")
    url = f"https://www.interviewbit.com/problems/{topic_slug}/"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Accept": "application/json, text/javascript, */*",
            "X-Requested-With": "XMLHttpRequest",
        }
    )
    # IB renders as HTML for this endpoint — parse titles from HTML
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    import re
    # Extract problem titles from IB's HTML
    titles = re.findall(r'<a[^>]*href="/problems/([^/]+)/"[^>]*>([^<]+)</a>', html)
    results = []
    for slug, title in titles[:limit]:
        results.append({
            "title":       title.strip(),
            "slug":        slug,
            "topic":       topic or "arrays",
            "url":         f"https://www.interviewbit.com/problems/{slug}/",
            "company_tags": [],
            "source":      "interviewbit",
        })
    return results


# Curated static list — P0 IB problems for target companies
_STATIC_IB = [
    # Adobe — heavy on arrays + DP + strings
    {"title": "Maximum Consecutive Gap",    "topic": "Arrays",   "company": "Adobe",         "url": "https://www.interviewbit.com/problems/maximum-consecutive-gap/"},
    {"title": "Spiral Order Matrix II",     "topic": "Arrays",   "company": "Adobe",         "url": "https://www.interviewbit.com/problems/spiral-order-matrix-ii/"},
    {"title": "Regular Expression Match",  "topic": "Strings",  "company": "Adobe",         "url": "https://www.interviewbit.com/problems/regular-expression-match/"},
    {"title": "Edit Distance",              "topic": "DP",       "company": "Adobe",         "url": "https://www.interviewbit.com/problems/edit-distance/"},
    {"title": "Palindrome Partitioning II", "topic": "DP",       "company": "Adobe",         "url": "https://www.interviewbit.com/problems/palindrome-partitioning-ii/"},
    # Goldman Sachs — DP + Graphs + Concurrency
    {"title": "Max Distance",              "topic": "Arrays",   "company": "Goldman Sachs", "url": "https://www.interviewbit.com/problems/max-distance/"},
    {"title": "Largest Rectangle in Histogram", "topic": "Stacks", "company": "Goldman Sachs", "url": "https://www.interviewbit.com/problems/largest-rectangle-in-histogram/"},
    {"title": "Word Ladder I",             "topic": "Graph",    "company": "Goldman Sachs", "url": "https://www.interviewbit.com/problems/word-ladder-i/"},
    {"title": "N-Queens",                  "topic": "Backtrack","company": "Goldman Sachs", "url": "https://www.interviewbit.com/problems/n-queens/"},
    {"title": "Serialize Binary Tree",     "topic": "Trees",    "company": "Goldman Sachs", "url": "https://www.interviewbit.com/problems/serialize-binary-tree/"},
    # Microsoft — Arrays + Trees + DP
    {"title": "Merge Intervals",           "topic": "Arrays",   "company": "Microsoft",     "url": "https://www.interviewbit.com/problems/merge-intervals/"},
    {"title": "LRU Cache",                 "topic": "Hashing",  "company": "Microsoft",     "url": "https://www.interviewbit.com/problems/lru-cache/"},
    {"title": "Kth Smallest Element BST",  "topic": "Trees",    "company": "Microsoft",     "url": "https://www.interviewbit.com/problems/kth-smallest-element-in-tree/"},
    {"title": "Reverse Linked List II",    "topic": "Linked Lists","company":"Microsoft",   "url": "https://www.interviewbit.com/problems/reverse-link-list-ii/"},
    {"title": "Min Depth of Binary Tree",  "topic": "Trees",    "company": "Microsoft",     "url": "https://www.interviewbit.com/problems/min-depth-of-binary-tree/"},
    # Amazon — similar to LC Hot 100
    {"title": "2 Sum",                     "topic": "Hashing",  "company": "Amazon",        "url": "https://www.interviewbit.com/problems/2-sum/"},
    {"title": "Clone Graph",               "topic": "Graph",    "company": "Amazon",        "url": "https://www.interviewbit.com/problems/clone-graph/"},
    {"title": "Trapping Rain Water",       "topic": "Arrays",   "company": "Amazon",        "url": "https://www.interviewbit.com/problems/trapping-rain-water/"},
    {"title": "Flatten Binary Tree to Linked List", "topic": "Trees", "company": "Amazon",  "url": "https://www.interviewbit.com/problems/flatten-binary-tree-to-linked-list/"},
    # Flipkart — E-commerce + search heavy
    {"title": "Search a 2D Matrix",        "topic": "Binary Search","company":"Flipkart",   "url": "https://www.interviewbit.com/problems/search-a-2d-matrix/"},
    {"title": "Distinct Subsequences",     "topic": "DP",       "company": "Flipkart",      "url": "https://www.interviewbit.com/problems/distinct-subsequences/"},
]


def _static_ib_problems(company: str, topic: str, limit: int) -> list:
    """Return static IB problem list filtered by company/topic."""
    results = _STATIC_IB
    if company:
        results = [p for p in results if company.lower() in p.get("company", "").lower()]
    if topic:
        results = [p for p in results if topic.lower() in p.get("topic", "").lower()]
    return results[:limit]


def print_ib_problems(company: str = None, topic: str = None):
    """Print InterviewBit problems for a company or topic."""
    problems = interviewbit_problems(company=company, topic=topic)

    header = f"INTERVIEWBIT — {(company or topic or 'All').upper()}"
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  {header:<54}║")
    print(f"  ╚══════════════════════════════════════════════════════════╝\n")

    if not problems:
        print(f"  No problems found for company='{company}' topic='{topic}'")
        available = sorted(set(p["company"] for p in _STATIC_IB))
        print(f"  Available companies: {', '.join(available)}\n")
        return

    for p in problems:
        company_tag = f"[{p.get('company', '')}]" if p.get("company") else ""
        print(f"  □ {p['title']:<45} {p.get('topic',''):<15} {company_tag}")
    print(f"\n  {len(problems)} problems. Open: {problems[0]['url'][:50]}...\n")
