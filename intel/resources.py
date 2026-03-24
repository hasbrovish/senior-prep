"""
Curated resource index — ranked by impact for SDE-2/SDE-3 prep.

Every resource has been researched and categorized.
Used by: prep resources <category>
"""

RESOURCES = {
    # ── DSA ────────────────────────────────────────────────────────────────────
    "dsa": [
        {"name": "NeetCode 150",                     "type": "problems",  "priority": "P0", "url": "https://neetcode.io/practice",
         "note": "Pattern-based curated list. Do this FIRST."},
        {"name": "Grind 75",                         "type": "problems",  "priority": "P0", "url": "https://www.techinterviewhandbook.org/grind75",
         "note": "Time-optimized version of Blind 75. By yangshun."},
        {"name": "Striver A2Z DSA Sheet",            "type": "problems",  "priority": "P0", "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2",
         "note": "450+ problems, comprehensive. India-focused. Follow alongside NeetCode."},
        {"name": "LeetCode Premium",                 "type": "platform",  "priority": "P0", "url": "https://leetcode.com/subscribe/",
         "note": "Company-tagged questions. MUST HAVE for targeted prep."},
        {"name": "EPI Java (Elements of Programming Interviews)", "type": "book", "priority": "P1", "url": "https://elementsofprogramminginterviews.com/",
         "note": "Hard problems with Java focus. Best for Hard LC prep."},
        {"name": "Effective Java (Joshua Bloch)",     "type": "book",     "priority": "P1", "url": "",
         "note": "Java idioms. Read items on Collections, Concurrency, Generics."},
        {"name": "Programming Pathshala Renaissance", "type": "course",   "priority": "P1", "url": "https://www.programmingpathshala.com/",
         "note": "Your enrolled course. Do DSA track on Saturdays."},
        {"name": "AlgoZenith",                        "type": "course",   "priority": "P2", "url": "https://www.algozenith.com/",
         "note": "Contest-level problems. Good for Hard problem practice."},
        {"name": "codestorywithMIK (YouTube)",        "type": "youtube",  "priority": "P1", "url": "https://www.youtube.com/@codestorywithMIK",
         "note": "Best for intuition when stuck on a pattern."},
        {"name": "takeUforward / Striver (YouTube)",  "type": "youtube",  "priority": "P0", "url": "https://www.youtube.com/@takeUforward",
         "note": "Most complete DSA curriculum. Follow A2Z sheet."},
    ],

    # ── System Design ─────────────────────────────────────────────────────────
    "system_design": [
        {"name": "Hello Interview Premium",           "type": "platform", "priority": "P0", "url": "https://www.hellointerview.com/",
         "note": "AI-guided SD practice. BEST tool for SD prep. Guided Practice + answer keys."},
        {"name": "Alex Xu - System Design Vol 1 & 2", "type": "book",    "priority": "P0", "url": "",
         "note": "30 system designs with walkthroughs. You have the PDFs."},
        {"name": "ByteByteGo Newsletter",             "type": "newsletter","priority": "P0","url": "https://blog.bytebytego.com/",
         "note": "Visual SD concepts weekly. Subscribe and read every Sunday."},
        {"name": "DDIA (Designing Data-Intensive Applications)", "type": "book", "priority": "P1", "url": "",
         "note": "Deep distributed systems understanding. Read chapters 1-9 for interviews."},
        {"name": "donnemartin/system-design-primer",   "type": "github",  "priority": "P0", "url": "https://github.com/donnemartin/system-design-primer",
         "note": "270K+ stars. The canonical SD reference. Start here for concepts."},
        {"name": "ashishps1/awesome-system-design-resources", "type": "github", "priority": "P1", "url": "https://github.com/ashishps1/awesome-system-design-resources",
         "note": "Curated SD links. Use as a lookup reference."},
        {"name": "ByteByteGo/system-design-101",       "type": "github",  "priority": "P1", "url": "https://github.com/ByteByteGo/system-design-101",
         "note": "Visual explanations of SD concepts."},
        {"name": "karanpratapsingh/system-design",     "type": "github",  "priority": "P1", "url": "https://github.com/karanpratapsingh/system-design",
         "note": "Full SD course as a GitHub repo."},
        {"name": "InterviewReady/system-design-resources", "type": "github", "priority": "P1", "url": "https://github.com/InterviewReady/system-design-resources",
         "note": "By Gaurav Sen (ex-Google). Curated list."},
        {"name": "Gaurav Sen (YouTube)",               "type": "youtube",  "priority": "P1", "url": "https://www.youtube.com/@gaboraugurabsen",
         "note": "Visual SD explanations. Thursday afternoon slot."},
        {"name": "Arpit Bhayani (YouTube + Blog)",     "type": "youtube",  "priority": "P1", "url": "https://www.youtube.com/@AsliEngineering",
         "note": "Deep microservices dives. Friday evening slot."},
        {"name": "IGotAnOffer SD Guides",              "type": "guide",    "priority": "P0", "url": "https://igotanoffer.com/blogs/tech/system-design-interviews",
         "note": "Company-specific SD guides (Meta, Amazon, Google). Free."},
        {"name": "enginebogie.com/u/anomaly2104",      "type": "platform", "priority": "P1", "url": "https://enginebogie.com/u/anomaly2104",
         "note": "Udit Agarwal (Amazon EM). SD masterclasses. BookMyShow schema is gold."},
        {"name": "checkcheckzz/system-design-interview","type": "github", "priority": "P2", "url": "https://github.com/checkcheckzz/system-design-interview",
         "note": "Systematic approach to SD interviews."},
        {"name": "shashank88/system_design",           "type": "github",  "priority": "P2", "url": "https://github.com/shashank88/system_design",
         "note": "Links + approach for SD prep."},
    ],

    # ── LLD ───────────────────────────────────────────────────────────────────
    "lld": [
        {"name": "Hello Interview LLD",               "type": "platform", "priority": "P0", "url": "https://www.hellointerview.com/learn/low-level-design",
         "note": "Guided LLD practice with AI feedback."},
        {"name": "Refactoring Guru",                   "type": "website",  "priority": "P0", "url": "https://refactoring.guru/design-patterns",
         "note": "Pattern catalog with code examples. Bookmark this."},
        {"name": "ashishps1/awesome-low-level-design", "type": "github",  "priority": "P0", "url": "https://github.com/ashishps1/awesome-low-level-design",
         "note": "LLD problems with solutions. Do: Parking Lot, Elevator, Chess, Snake."},
        {"name": "Head First Design Patterns",         "type": "book",    "priority": "P1", "url": "",
         "note": "Pattern intuition building. Read Strategy, Observer, Factory, Decorator."},
        {"name": "Techie Content (YouTube)",           "type": "youtube",  "priority": "P1", "url": "https://www.youtube.com/@TechieContent",
         "note": "LLD playlist. Wednesday evening slot."},
        {"name": "Shrayansh Jain LLD+HLD (YouTube)",   "type": "youtube",  "priority": "P1", "url": "https://www.youtube.com/@ShrayanshJain",
         "note": "Bridges LLD and System Design."},
    ],

    # ── Behavioral ────────────────────────────────────────────────────────────
    "behavioral": [
        {"name": "IGotAnOffer Behavioral Guides",      "type": "guide",   "priority": "P0", "url": "https://igotanoffer.com/blogs/tech",
         "note": "Company-specific behavioral prep (Amazon LP, Meta values, Google)."},
        {"name": "Amazon Leadership Principles",       "type": "framework","priority": "P0", "url": "https://www.amazon.jobs/content/en/our-workplace/leadership-principles",
         "note": "16 LPs. Map every STAR story to 2-3 LPs. Ownership + Dive Deep are most tested."},
        {"name": "Hello Interview Behavioral",         "type": "platform", "priority": "P1", "url": "https://www.hellointerview.com/learn/behavioral",
         "note": "AI behavioral mock interviews."},
        {"name": "Dan Croitor (YouTube)",              "type": "youtube",  "priority": "P1", "url": "https://www.youtube.com/@DanCroitor",
         "note": "Amazon LP prep specifically. Very detailed."},
        {"name": "Exponent (YouTube)",                 "type": "youtube",  "priority": "P2", "url": "https://www.youtube.com/@tryexponent",
         "note": "Mock interview videos for behavioral rounds."},
    ],

    # ── Interview Experiences ─────────────────────────────────────────────────
    "experiences": [
        {"name": "LeetCode Discuss",                   "type": "forum",   "priority": "P0", "url": "https://leetcode.com/discuss/interview-experience",
         "note": "Largest collection. Filter by company tag. Read before every interview."},
        {"name": "Reddit r/leetcode",                  "type": "forum",   "priority": "P0", "url": "https://www.reddit.com/r/leetcode",
         "note": "Active community. Interview experience flair."},
        {"name": "Reddit r/leetcodedesi",              "type": "forum",   "priority": "P1", "url": "https://www.reddit.com/r/leetcodedesi",
         "note": "India-specific. TC discussions in LPA. Very relevant for your targets."},
        {"name": "Blind / TeamBlind",                  "type": "forum",   "priority": "P1", "url": "https://www.teamblind.com",
         "note": "Anonymous experiences. TC negotiations. Filter by company."},
        {"name": "enginebogie.com Experiences",        "type": "platform","priority": "P1", "url": "https://enginebogie.com/interview/experiences",
         "note": "Structured round-by-round experiences. Indian companies well-covered."},
        {"name": "Glassdoor Interview Reviews",        "type": "platform","priority": "P2", "url": "https://www.glassdoor.co.in",
         "note": "Older but useful for process understanding."},
        {"name": "levels.fyi",                         "type": "platform","priority": "P1", "url": "https://www.levels.fyi",
         "note": "Compensation data + level mapping. Use for negotiation."},
    ],

    # ── Full Prep / Meta-Resources ────────────────────────────────────────────
    "full_prep": [
        {"name": "jwasham/coding-interview-university","type": "github",  "priority": "P1", "url": "https://github.com/jwasham/coding-interview-university",
         "note": "300K+ stars. Multi-month CS study plan."},
        {"name": "yangshun/tech-interview-handbook",   "type": "github",  "priority": "P1", "url": "https://github.com/yangshun/tech-interview-handbook",
         "note": "By Blind 75 creator. End-to-end prep guide."},
        {"name": "kdn251/interviews",                  "type": "github",  "priority": "P1", "url": "https://github.com/kdn251/interviews",
         "note": "63K+ stars. Categorized coding problems."},
        {"name": "binhnguyennus/awesome-scalability",  "type": "github",  "priority": "P2", "url": "https://github.com/binhnguyennus/awesome-scalability",
         "note": "55K+ stars. Scalability patterns and case studies."},
        {"name": "bhartik021/SDE-Interview-Materials",  "type": "github",  "priority": "P2", "url": "https://github.com/bhartik021/SDE-Interview-Materials",
         "note": "Notes + sheets + interview questions collection."},
    ],
}

ALL_CATEGORIES = list(RESOURCES.keys())


def get_resources(category=None, priority=None):
    """Get resources, optionally filtered."""
    if category and category in RESOURCES:
        items = RESOURCES[category]
    else:
        items = [r for cat_items in RESOURCES.values() for r in cat_items]

    if priority:
        items = [r for r in items if r["priority"] == priority]

    return items


def print_resources(category=None):
    """Print resources to stdout."""
    cats = [category] if category and category in RESOURCES else ALL_CATEGORIES

    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  CURATED RESOURCES INDEX                                ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")

    for cat in cats:
        items = RESOURCES[cat]
        cat_label = cat.replace("_", " ").upper()
        print(f"\n  ── {cat_label} {'─' * (52 - len(cat_label))}")

        for r in items:
            p_icon = {"P0": "🔴", "P1": "🟡", "P2": "⚪"}.get(r["priority"], "⚪")
            type_tag = f"[{r['type']}]"
            print(f"  {p_icon} {r['priority']} {r['name']}")
            print(f"       {type_tag} {r['note']}")
            if r.get("url"):
                print(f"       → {r['url']}")

    print(f"\n  Legend: 🔴 P0 = Must use  🟡 P1 = Highly recommended  ⚪ P2 = Nice to have")
    print(f"  Usage: prep resources dsa | prep resources system_design | prep resources lld\n")
