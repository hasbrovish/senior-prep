"""
Behavioral Gap Detector.

Reads Amazon_LP_STAR_Bank.md, evaluates coverage, story quality,
and generates Bar Raiser probing questions.

Usage:
  from intel.behavioral import run_lp_check, print_lp_check
"""

import re
from pathlib import Path

BASE = Path(__file__).parent.parent

AMAZON_LPS = {
    "customer-obsession":        {"name": "Customer Obsession",           "frequency": "very_high", "bar_raiser_weight": 5},
    "ownership":                 {"name": "Ownership",                    "frequency": "very_high", "bar_raiser_weight": 5},
    "invent-simplify":           {"name": "Invent and Simplify",          "frequency": "high",      "bar_raiser_weight": 4},
    "are-right-a-lot":           {"name": "Are Right, A Lot",             "frequency": "medium",    "bar_raiser_weight": 3},
    "learn-be-curious":          {"name": "Learn and Be Curious",         "frequency": "medium",    "bar_raiser_weight": 3},
    "hire-develop-best":         {"name": "Hire and Develop the Best",    "frequency": "medium",    "bar_raiser_weight": 3},
    "insist-highest-standards":  {"name": "Insist on Highest Standards",  "frequency": "high",      "bar_raiser_weight": 4},
    "think-big":                 {"name": "Think Big",                    "frequency": "medium",    "bar_raiser_weight": 3},
    "bias-for-action":           {"name": "Bias for Action",              "frequency": "high",      "bar_raiser_weight": 4},
    "frugality":                 {"name": "Frugality",                    "frequency": "low",       "bar_raiser_weight": 2},
    "earn-trust":                {"name": "Earn Trust",                   "frequency": "high",      "bar_raiser_weight": 4},
    "dive-deep":                 {"name": "Dive Deep",                    "frequency": "very_high", "bar_raiser_weight": 5},
    "have-backbone":             {"name": "Have Backbone; Disagree and Commit", "frequency": "high", "bar_raiser_weight": 4},
    "deliver-results":           {"name": "Deliver Results",              "frequency": "very_high", "bar_raiser_weight": 5},
}

# Bar Raiser probing questions per LP
LP_PROBES = {
    "customer-obsession": [
        "What data did you use to validate that this was the right thing for users?",
        "How did you balance customer needs with technical constraints?",
        "What was the user feedback mechanism after you shipped this?",
        "Tell me about a time you pushed back on a feature because it wasn't good for customers.",
    ],
    "ownership": [
        "Who else could have owned this? Why did you?",
        "What happened after the project was done — did you follow up?",
        "What would you have done differently if you had more resources?",
        "Tell me about a time you took ownership of something outside your job scope.",
    ],
    "invent-simplify": [
        "What alternatives did you consider before this solution?",
        "What was the simplest version you could have shipped? Why did you go further?",
        "How did you know this was innovative vs just different?",
        "What external ideas influenced your design?",
    ],
    "dive-deep": [
        "How did you know that was actually the root cause?",
        "Walk me through your debugging process step by step.",
        "What metrics did you look at to confirm your hypothesis?",
        "What did you find in the code/data that others had missed?",
    ],
    "deliver-results": [
        "What was the metric that proved success?",
        "Were there blockers? How did you unblock yourself?",
        "What did you cut to meet the deadline?",
        "How did you communicate progress to stakeholders?",
    ],
    "earn-trust": [
        "How did you handle a situation where someone disagreed with your technical decision?",
        "Tell me about a time you had to admit you were wrong.",
        "How did you build trust with a skeptical team member?",
        "Tell me about a time you proactively gave difficult feedback.",
    ],
    "bias-for-action": [
        "What would have happened if you had waited longer to decide?",
        "How did you make the decision with incomplete information?",
        "What was the reversibility of this decision?",
        "Tell me about a time you acted too slowly. What did you learn?",
    ],
    "insist-highest-standards": [
        "Where did you draw the line — what was 'good enough'?",
        "Who raised the bar in this situation — you or someone else?",
        "Tell me about a time you sent something back because it didn't meet your standard.",
        "How did you ensure code quality on a tight deadline?",
    ],
    "have-backbone": [
        "What was their counter-argument? How did you address it?",
        "How did you ultimately commit once the decision was made against you?",
        "What data did you use to support your position?",
        "Tell me about a time you were wrong after pushing back.",
    ],
    "think-big": [
        "What was the 3-year vision for this initiative?",
        "How did your solution enable future growth?",
        "What constraint did you challenge that others accepted?",
        "How did you get buy-in for a non-obvious long-term bet?",
    ],
    "frugality": [
        "Could you have achieved the same result with fewer resources?",
        "What did you NOT build to save cost/time?",
        "How did you measure the ROI of this investment?",
    ],
    "hire-develop-best": [
        "How did you identify that this person had potential?",
        "What specific thing did you do to help them grow?",
        "Tell me about a time you had to make a tough call on underperformance.",
    ],
    "learn-be-curious": [
        "What was the last technical book or paper you read?",
        "How did you learn this technology — formal training or self-taught?",
        "What's a domain outside your expertise that you've explored recently?",
    ],
    "are-right-a-lot": [
        "What information sources do you use to form opinions?",
        "Tell me about a time your first instinct was wrong.",
        "How do you update your view when new evidence emerges?",
    ],
}


def _parse_star_bank() -> dict:
    """Parse Amazon_LP_STAR_Bank.md into LP → stories mapping.

    Handles formats:
      - ## 1. CUSTOMER OBSESSION  (numbered LP headers)
      - ### Story A — Title       (story headers under LP)
      - **S:** / **R:**           (inline STAR markers)
      - SITUATION: / RESULT:      (full-word STAR markers)
    """
    star_file = BASE / "Interview_Answers" / "Amazon_LP_STAR_Bank.md"
    if not star_file.exists():
        return {}

    content = star_file.read_text(encoding="utf-8", errors="replace")
    stories = {}
    current_lp = None
    in_story = False

    # LP name keywords for fuzzy matching (ordered by length desc to avoid partial matches)
    lp_keywords = [
        ("customer-obsession",       ["customer obsession", "customer"]),
        ("ownership",                ["ownership"]),
        ("invent-simplify",          ["invent and simplify", "invent & simplify", "simplify"]),
        ("are-right-a-lot",          ["are right, a lot", "right, a lot"]),
        ("learn-be-curious",         ["learn and be curious", "learn & be curious", "be curious"]),
        ("hire-develop-best",        ["hire and develop", "hire & develop", "develop the best"]),
        ("insist-highest-standards", ["insist on highest", "highest standards"]),
        ("think-big",                ["think big"]),
        ("bias-for-action",          ["bias for action"]),
        ("frugality",                ["frugality"]),
        ("earn-trust",               ["earn trust"]),
        ("dive-deep",                ["dive deep"]),
        ("have-backbone",            ["have backbone", "disagree and commit"]),
        ("deliver-results",          ["deliver results"]),
    ]

    for line in content.splitlines():
        # Detect LP section headers: ## N. LP NAME  or  ## LP NAME
        h2_match = re.match(r"^##\s+(?:\d+\.\s+)?(.+?)(?:\s*\(.*\))?\s*$", line)
        if h2_match:
            header_text = h2_match.group(1).strip().lower()
            matched_lp = None
            for lp_key, keywords in lp_keywords:
                if any(kw in header_text for kw in keywords):
                    matched_lp = lp_key
                    break
            if matched_lp:
                current_lp = matched_lp
                in_story = False
                stories.setdefault(current_lp, [])
                continue

        if not current_lp:
            continue

        # Detect story start: ### Story A — Title  or  ### Title
        if re.match(r"^###\s+Story\s+[A-Z]", line, re.I):
            stories[current_lp].append({"has_situation": True})
            in_story = True
            continue

        # Detect STAR markers in current story
        if in_story and stories.get(current_lp):
            current_story = stories[current_lp][-1]

            # R: / **R:** / RESULT: markers
            is_result = (
                re.match(r"^\*?\*?R\s*[:：]", line) or
                re.match(r"^\*?\*?RESULT\s*[:：]", line, re.I)
            )
            if is_result:
                current_story["has_result"] = True
                # Check for quantified numbers
                if re.search(
                    r"\d+[%xX]?|\d+\s*(ms|sec|min|hr|M|K|LPA|cr|lakh|TB|GB|MB|users|req|team|month|day|week|filing)",
                    line
                ):
                    current_story["has_quantified_result"] = True

    return stories


def _evaluate_coverage(stories: dict) -> dict:
    """Evaluate LP coverage and story quality."""
    evaluation = {}

    for lp_key, lp_meta in AMAZON_LPS.items():
        lp_stories = stories.get(lp_key, [])
        count = len(lp_stories)
        quantified = sum(1 for s in lp_stories if s.get("has_quantified_result"))

        # Risk assessment
        freq = lp_meta["frequency"]
        weight = lp_meta["bar_raiser_weight"]

        if count == 0:
            risk = "critical" if freq in ("very_high", "high") else "high"
        elif count == 1:
            risk = "medium" if freq in ("very_high", "high") else "low"
            if quantified == 0:
                risk = "high"  # Single story without numbers is fragile
        else:
            risk = "low" if quantified > 0 else "medium"

        evaluation[lp_key] = {
            "name":      lp_meta["name"],
            "stories":   count,
            "quantified": quantified,
            "frequency": freq,
            "weight":    weight,
            "risk":      risk,
        }

    return evaluation


def run_lp_check() -> dict:
    """Run behavioral gap analysis and return results."""
    stories = _parse_star_bank()
    evaluation = _evaluate_coverage(stories)

    critical = [k for k, v in evaluation.items() if v["risk"] == "critical"]
    high_risk = [k for k, v in evaluation.items() if v["risk"] == "high"]
    medium    = [k for k, v in evaluation.items() if v["risk"] == "medium"]
    low       = [k for k, v in evaluation.items() if v["risk"] == "low"]

    total_stories = sum(v["stories"] for v in evaluation.values())
    coverage_pct  = len([k for k, v in evaluation.items() if v["stories"] > 0]) / len(AMAZON_LPS) * 100

    return {
        "evaluation": evaluation,
        "critical":   critical,
        "high_risk":  high_risk,
        "medium":     medium,
        "low":        low,
        "total_stories": total_stories,
        "coverage_pct":  round(coverage_pct),
        "file_found": bool(stories),
    }


def print_lp_check():
    """Print behavioral gap analysis."""
    result = run_lp_check()

    if not result["file_found"]:
        print("\n  ❌ Could not find Interview_Answers/Amazon_LP_STAR_Bank.md")
        print("  Create it with your STAR stories to enable gap analysis.\n")
        return

    evaluation = result["evaluation"]
    risk_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "✅"}
    freq_label = {"very_high": "VH", "high": "H", "medium": "M", "low": "L"}

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  BEHAVIORAL GAP DETECTOR — AMAZON LP ANALYSIS          ║
  ╚══════════════════════════════════════════════════════════╝

  Coverage: {result['coverage_pct']}%  │  Total stories: {result['total_stories']}  │  LPs: {len(AMAZON_LPS)}

  {'LP NAME':<34} {'STORIES':>7}  {'QUANT':>6}  {'FREQ':>5}  RISK
  {'─'*65}""")

    # Sort by risk severity then frequency
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    sorted_lps = sorted(evaluation.items(), key=lambda x: (order[x[1]["risk"]], -x[1]["weight"]))

    for lp_key, v in sorted_lps:
        icon = risk_icon[v["risk"]]
        freq = freq_label[v["frequency"]]
        quant_str = f"{v['quantified']}/{v['stories']}" if v["stories"] > 0 else "─"
        print(f"  {icon} {v['name']:<32}  {v['stories']:>7}  {quant_str:>6}  {freq:>5}")

    print(f"\n  Legend: VH=Very High freq | H=High | M=Medium | L=Low")
    print(f"  Quant = stories with quantified results (numbers)")

    # Critical gaps
    if result["critical"]:
        print(f"\n  🔴 CRITICAL GAPS — prepare BEFORE any Amazon round:")
        for k in result["critical"]:
            v = evaluation[k]
            print(f"     • {v['name']} — 0 stories, asked in {v['frequency']} frequency rounds")

    if result["high_risk"]:
        print(f"\n  🟠 HIGH RISK — thin coverage:")
        for k in result["high_risk"]:
            v = evaluation[k]
            reason = "0 stories" if v["stories"] == 0 else f"{v['stories']} story but no quantified results"
            print(f"     • {v['name']} — {reason}")

    # Top probing questions for weakest LPs
    worst_lps = result["critical"] + result["high_risk"]
    if worst_lps:
        print(f"\n  ── BAR RAISER PROBES FOR YOUR WEAKEST LPs ──────────────")
        for lp_key in worst_lps[:3]:
            v = evaluation[lp_key]
            probes = LP_PROBES.get(lp_key, [])[:2]
            print(f"\n  [{v['name']}]")
            for q in probes:
                print(f"    → {q}")

    # Action plan
    print(f"""
  ── ACTION PLAN ─────────────────────────────────────────
  1. For each CRITICAL LP: write a full STAR story from GSTN
  2. For QUANTIFIED gaps: add numbers (users, %, ms, TC savings)
  3. Practice: prep question behavioral  OR  prep mock behavioral
  4. Record yourself — aim for 90-120 seconds per story

  Your strongest GSTN stories (by LP):
  • Ownership → Kafka DLQ + exactly-once pipeline
  • Dive Deep → HBase row key design, GSTN ledger root cause
  • Deliver Results → 500 GST filings/sec, XA transaction fix
  • Customer Obsession → GST filing UX improvement, 14M users
  • Invent & Simplify → DistCacheUtil replacing JBoss DataGrid
""")


def get_probing_questions(lp_key: str, count: int = 3) -> list[str]:
    """Get probing questions for a specific LP."""
    return LP_PROBES.get(lp_key, [])[:count]


def generate_star_gap_questions_with_ai(lp_name: str) -> str:
    """Use AI to generate tailored probing questions for your stories."""
    try:
        from intel.coach import _call_claude, _profile_context
        system = f"""You are an Amazon Bar Raiser.
{_profile_context()}

Generate 5 PROBING follow-up questions for the Leadership Principle: {lp_name}

The candidate has 5.5 YOE at GSTN. Questions should:
1. Test if the story is real and deep (not rehearsed surface)
2. Probe for ownership vs team credit
3. Ask for data and metrics
4. Test what they would do differently
5. Probe for scale/impact

Return 5 questions only, numbered 1-5. Each on one line. No preamble."""

        return _call_claude(system, f"LP: {lp_name}\nGenerate probing questions.")
    except Exception as e:
        return "\n".join(LP_PROBES.get(
            next((k for k, v in AMAZON_LPS.items() if v["name"].lower() in lp_name.lower()), ""),
            []
        )[:5])
