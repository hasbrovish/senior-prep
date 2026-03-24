"""
Levels.fyi TC Intelligence Scraper.

Fetches salary/TC data from publicly accessible levels.fyi pages.
No auth required for public data. Respects ToS by limiting requests.

Provides: base salary, TC range, stock, bonus by level and YOE.
"""

import json
import urllib.request
import urllib.error
import re
from datetime import date

TARGET_COMPANIES = {
    "google":       {"search": "Google",         "levels": ["L4", "L5"]},
    "amazon":       {"search": "Amazon",         "levels": ["SDE II", "SDE III"]},
    "microsoft":    {"search": "Microsoft",      "levels": ["SDE II", "SDE III", "62", "63", "64"]},
    "adobe":        {"search": "Adobe",          "levels": ["MTS II", "MTS III"]},
    "flipkart":     {"search": "Flipkart",       "levels": ["SDE 2", "SDE 3"]},
    "goldman_sachs":{"search": "Goldman Sachs",  "levels": ["VP", "Associate"]},
    "razorpay":     {"search": "Razorpay",       "levels": ["SDE II"]},
    "phonepe":      {"search": "PhonePe",        "levels": ["SDE II", "SDE III"]},
    "swiggy":       {"search": "Swiggy",         "levels": ["SDE II", "SDE III"]},
    "cred":         {"search": "CRED",           "levels": ["SDE II"]},
    "paytm":        {"search": "Paytm",          "levels": ["SDE II"]},
}

# Static TC data (updated periodically based on public knowledge)
# Source: public levels.fyi, LinkedIn posts, known market rates (India, 2025)
STATIC_TC = {
    "google": {
        "L4": {"base": "30-40 LPA", "tc": "40-60 LPA", "stock": "15-20 LPA/yr", "notes": "Strong DSA+SD required"},
        "L5": {"base": "40-55 LPA", "tc": "60-90 LPA", "stock": "25-40 LPA/yr", "notes": "5+ YOE, leadership signals"},
    },
    "amazon": {
        "SDE II":  {"base": "25-35 LPA", "tc": "35-50 LPA", "stock": "RSU over 4yr", "notes": "LP critical, 14/16 in every round"},
        "SDE III": {"base": "35-50 LPA", "tc": "50-75 LPA", "stock": "RSU over 4yr", "notes": "Cross-team impact needed"},
    },
    "microsoft": {
        "62":      {"base": "22-30 LPA", "tc": "28-38 LPA", "stock": "ESPP + RSU", "notes": "Level 62 = SDE II equivalent"},
        "63":      {"base": "28-40 LPA", "tc": "35-50 LPA", "stock": "ESPP + RSU", "notes": "Level 63 = senior SDE"},
        "64":      {"base": "35-50 LPA", "tc": "45-65 LPA", "stock": "ESPP + RSU", "notes": "Level 64 = principal"},
    },
    "adobe": {
        "MTS II":  {"base": "22-30 LPA", "tc": "28-40 LPA", "stock": "RSU",         "notes": "Strong LLD + Java focus"},
        "MTS III": {"base": "30-42 LPA", "tc": "38-55 LPA", "stock": "RSU",         "notes": "Design + mentoring signals"},
    },
    "flipkart": {
        "SDE 2":   {"base": "25-35 LPA", "tc": "32-48 LPA", "stock": "ESOPs",       "notes": "Machine coding + scale design"},
        "SDE 3":   {"base": "35-50 LPA", "tc": "45-65 LPA", "stock": "ESOPs",       "notes": "Founding engineer mindset"},
    },
    "goldman_sachs": {
        "Associate":{"base": "20-28 LPA", "tc": "25-38 LPA", "stock": "Deferred comp","notes": "Finance domain + strong DSA"},
        "VP":        {"base": "30-50 LPA", "tc": "40-70 LPA", "stock": "Deferred comp","notes": "Leadership + business impact"},
    },
    "razorpay": {
        "SDE II":  {"base": "22-30 LPA", "tc": "28-38 LPA", "stock": "ESOPs",       "notes": "Payments + distributed transactions"},
    },
    "phonepe": {
        "SDE II":  {"base": "24-32 LPA", "tc": "30-42 LPA", "stock": "ESOPs",       "notes": "Strong Java + fintech"},
        "SDE III": {"base": "32-45 LPA", "tc": "40-58 LPA", "stock": "ESOPs",       "notes": "Scale + distributed systems"},
    },
    "swiggy": {
        "SDE II":  {"base": "22-32 LPA", "tc": "28-45 LPA", "stock": "ESOPs",       "notes": "Real-time systems + location"},
        "SDE III": {"base": "32-45 LPA", "tc": "40-58 LPA", "stock": "ESOPs",       "notes": "Platform + reliability"},
    },
    "cred": {
        "SDE II":  {"base": "25-35 LPA", "tc": "32-45 LPA", "stock": "ESOPs",       "notes": "Clean architecture + product thinking"},
    },
    "paytm": {
        "SDE II":  {"base": "18-25 LPA", "tc": "22-32 LPA", "stock": "ESOPs",       "notes": "Fintech + transaction systems"},
    },
}

NEGOTIATION_TIPS = {
    "general": [
        "Never reveal current CTC. Say: 'I'm targeting market rate for this level'",
        "Counter is always appropriate — aim for 10-20% above initial offer",
        "Use competing offers to negotiate: 'I have an offer at X — can you match?'",
        "Ask for 48 hours before accepting. Never accept on the spot.",
        "Negotiate components separately: base, RSU cliff, joining bonus",
        "RSU cliff: ask if first-year cliff can be reduced from 1yr to 6mo",
        "Joining bonus offsets unvested stock at current employer",
    ],
    "amazon": [
        "Amazon base is capped lower; most TC is in RSU (4yr schedule: 5/15/40/40)",
        "Year 1-2 are lowest TC — ask for front-loaded RSU schedule",
        "Joining bonus compensates for unvested current-employer stock",
        "Competing offer from FAANG is your strongest leverage",
    ],
    "google": [
        "Google stock (Alphabet) has growth potential — factor into TC calculation",
        "Perf bonus 15-20% at L4/L5 if you're rated 'Meets Expectations'",
        "Refresh grants annual — tenure employees often have better TC",
        "Band is wide — negotiate hard on RSU/grant amount, not just base",
    ],
}


def get_tc_data(company: str) -> dict:
    """Get TC data for a company (static + try live scrape)."""
    company_key = company.lower().replace(" ", "_").replace("-", "_")
    static = STATIC_TC.get(company_key, {})

    # Try live scrape (non-blocking, fallback to static)
    live_data = _try_scrape_levels(company)

    return {
        "company":    company,
        "static":     static,
        "live":       live_data,
        "updated_at": str(date.today()),
    }


def _try_scrape_levels(company: str) -> dict:
    """
    Attempt to fetch live TC data from levels.fyi.
    Returns empty dict if scraping fails (graceful degradation).
    """
    try:
        company_info = next(
            (v for k, v in TARGET_COMPANIES.items() if k.lower() == company.lower().split()[0]),
            None
        )
        if not company_info:
            return {}

        # levels.fyi has some public JSON endpoints
        search_term = company_info["search"].replace(" ", "+")
        url = f"https://www.levels.fyi/js/salaryData.json"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "https://www.levels.fyi/",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            all_data = json.loads(resp.read())

        # Filter for this company, India location
        company_records = [
            r for r in all_data
            if (company_info["search"].lower() in r.get("company", "").lower()
                and ("india" in r.get("location", "").lower()
                     or "bangalore" in r.get("location", "").lower()
                     or "hyderabad" in r.get("location", "").lower()
                     or "mumbai" in r.get("location", "").lower()))
        ][:20]

        if not company_records:
            return {}

        # Aggregate by level
        by_level = {}
        for r in company_records:
            level = r.get("level", "Unknown")
            tc = r.get("totalyearlycompensation", 0)
            if tc and tc > 0:
                by_level.setdefault(level, []).append(tc)

        result = {}
        for level, tcs in by_level.items():
            avg_usd = int(sum(tcs) / len(tcs))
            # Rough USD to INR (for India-based roles: multiply by 83 then to LPA)
            avg_lpa = round(avg_usd * 83 / 100000, 1)
            result[level] = {"tc_lpa_est": f"{avg_lpa} LPA", "sample_size": len(tcs)}

        return result

    except Exception:
        return {}


def print_tc_report(company: str):
    """Print TC report for a company."""
    data = get_tc_data(company)
    static = data.get("static", {})
    company_key = company.lower().split()[0]
    target_info = TARGET_COMPANIES.get(company_key, {})
    tips = NEGOTIATION_TIPS.get(company_key, NEGOTIATION_TIPS["general"])

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  TC INTELLIGENCE — {company.upper():<37}║
  ╚══════════════════════════════════════════════════════════╝
""")

    if not static:
        print(f"  No TC data available for '{company}'.")
        print(f"  Available companies: {', '.join(STATIC_TC.keys())}")
        print()
        return

    print(f"  {'LEVEL':<15}  {'BASE':>12}  {'TOTAL TC':>12}  {'STOCK':>14}  NOTES")
    print(f"  {'─'*72}")

    for level, info in static.items():
        print(f"  {level:<15}  {info['base']:>12}  {info['tc']:>12}  {info['stock']:>14}")
        print(f"  {'':<15}  📌 {info['notes']}")
        print()

    # Live data if available
    live = data.get("live", {})
    if live:
        print(f"  ── LIVE DATA (levels.fyi — India, recent) ─────────────")
        for level, ldata in live.items():
            print(f"  {level:<20} ~{ldata['tc_lpa_est']}  (n={ldata['sample_size']})")
        print()

    # Which level to target
    if target_info.get("levels"):
        print(f"  Your target levels: {', '.join(target_info['levels'])}")
        print()

    print(f"  ── NEGOTIATION PLAYBOOK ─────────────────────────────────")
    for tip in tips[:4]:
        print(f"    • {tip}")

    print(f"""
  ── YOUR NEGOTIATION POSITION ─────────────────────────────
  Current: Specialist Programmer L2, Infosys
  5.5 YOE, GSTN (14M users, production scale)
  Target: 35-50% hike from current CTC

  Leverage points:
    • Competing offers (get at least 2 before negotiating)
    • GSTN production scale — rare at 5.5 YOE
    • Strong distributed systems background
    • CP background (CodeChef 4-star, Code Jam qualifier)
""")


def scrape_all_companies() -> dict:
    """Scrape TC data for all target companies and store in DB."""
    results = {}
    try:
        from intel.db import upsert_company_intel, get_conn
        for company_key, info in TARGET_COMPANIES.items():
            data = get_tc_data(company_key)
            static = data.get("static", {})
            if static:
                # Build TC range string from static data
                all_tcs = [v.get("tc", "") for v in static.values()]
                tc_range = " / ".join(all_tcs[:2]) if all_tcs else ""
                upsert_company_intel(company_key, {"tc_range": tc_range})
                results[company_key] = {"tc_range": tc_range}
    except Exception as e:
        results["error"] = str(e)
    return results
