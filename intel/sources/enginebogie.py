"""
Interview experience scrapers for India-specific sources.
enginebogie.com requires auth (React SPA) — replaced with:
  1. Reddit r/ExperiencedDevs (global SDE-2/3 experiences)
  2. HackerNews "Ask HN: Who's hiring" threads (free, no auth)
  3. GitHub job boards (levels.fyi public data)
"""

import json
import urllib.request
import urllib.error
import re
import time
from datetime import datetime

KNOWN_COMPANIES = [
    "google", "amazon", "microsoft", "meta", "facebook", "apple", "netflix",
    "flipkart", "uber", "adobe", "goldman sachs", "walmart", "oracle",
    "razorpay", "phonepe", "cred", "swiggy", "paytm", "meesho",
    "makemytrip", "juspay", "salesforce", "intuit", "atlassian",
    "stripe", "coinbase", "airbnb", "zomato", "dream11", "groww",
    "zerodha", "nykaa", "dunzo", "myntra", "samsung", "directi",
    "jp morgan", "morgan stanley", "deutsche bank",
]


def _fetch(url, headers=None, timeout=15):
    h = {"User-Agent": "Mozilla/5.0 (PrepForge interview aggregator)", "Accept": "application/json"}
    if headers:
        h.update(headers)
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ⚠️  Fetch error {url[:50]}: {e}")
        return ""


def extract_company(text):
    text_lower = text.lower()
    for company in KNOWN_COMPANIES:
        if company in text_lower:
            return company.title().replace("Jp Morgan", "JP Morgan")
    match = re.search(r'(?:@|at|join|joined)\s+([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)', text)
    if match:
        return match.group(1)
    return "Unknown"


def extract_role(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["sde-3", "sde3", "l5", "senior sde", "staff", "e5", "e6", "principal"]):
        return "SDE-3"
    if any(w in text_lower for w in ["sde-2", "sde2", "l4", "e4", "mid-level", "sde ii"]):
        return "SDE-2"
    return "SDE-2"


def extract_result(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["got offer", "offer letter", "accepted", "joining", "selected", "cleared all"]):
        return "offer"
    if any(w in text_lower for w in ["rejected", "reject", "failed", "ghosted", "not selected"]):
        return "reject"
    return "unknown"


# ─── Source 1: Reddit r/ExperiencedDevs ───────────────────────────────────────

def scrape_experienced_devs(limit=25):
    """Scrape r/ExperiencedDevs for senior engineer interview experiences."""
    results = []
    search_terms = ["interview experience", "offer", "sde-2", "senior engineer", "system design round"]

    for term in search_terms[:2]:
        encoded = urllib.request.quote(term)
        url = f"https://www.reddit.com/r/ExperiencedDevs/search.json?q={encoded}&restrict_sr=on&sort=new&limit={limit}"
        raw = _fetch(url, headers={"User-Agent": "PrepForge/1.0 interview aggregator"})
        if not raw:
            continue
        try:
            data = json.loads(raw)
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                title = post.get("title", "")
                body = post.get("selftext", "")
                combined = title + " " + body

                if not any(kw in combined.lower() for kw in ["interview", "offer", "coding round", "system design", "sde"]):
                    continue

                results.append({
                    "source":         "reddit_expdevs",
                    "source_id":      post.get("id", ""),
                    "company":        extract_company(combined),
                    "role":           extract_role(combined),
                    "date_posted":    datetime.fromtimestamp(post["created_utc"]).strftime("%Y-%m-%d") if post.get("created_utc") else None,
                    "title":          title,
                    "body_raw":       body[:5000],
                    "overall_result": extract_result(combined),
                    "url":            f"https://reddit.com{post.get('permalink', '')}",
                    "rounds":         [],
                })
        except (json.JSONDecodeError, KeyError):
            pass
        time.sleep(1)

    return results


# ─── Source 2: HackerNews — interview experiences via Algolia ─────────────────

def scrape_hn_interviews(limit=20):
    """Scrape HackerNews for interview experience posts via Algolia API."""
    results = []

    for query in ["interview experience offer", "system design interview India", "SDE-2 interview"]:
        encoded = urllib.request.quote(query)
        url = f"https://hn.algolia.com/api/v1/search?query={encoded}&tags=story&hitsPerPage={limit}&numericFilters=created_at_i>1700000000"
        raw = _fetch(url)
        if not raw:
            continue
        try:
            data = json.loads(raw)
            for hit in data.get("hits", []):
                title = hit.get("title", "")
                body = hit.get("story_text") or ""
                combined = title + " " + body

                if not any(kw in combined.lower() for kw in ["interview", "offer", "hired", "system design", "coding"]):
                    continue

                results.append({
                    "source":         "hackernews",
                    "source_id":      str(hit.get("objectID", "")),
                    "company":        extract_company(combined),
                    "role":           extract_role(combined),
                    "date_posted":    hit.get("created_at", "")[:10],
                    "title":          title,
                    "body_raw":       body[:5000],
                    "overall_result": extract_result(combined),
                    "url":            hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "rounds":         [],
                })
        except (json.JSONDecodeError, KeyError):
            pass
        time.sleep(0.5)

    return results


# ─── Source 3: Reddit r/cscareerquestions India ───────────────────────────────

def scrape_india_career(limit=20):
    """Scrape India-specific career subreddits for interview experiences."""
    results = []
    subs = ["IndiaTechies", "developersIndia"]

    for sub in subs:
        url = f"https://www.reddit.com/r/{sub}/search.json?q=interview+experience&restrict_sr=on&sort=new&limit={limit}"
        raw = _fetch(url, headers={"User-Agent": "PrepForge/1.0"})
        if not raw:
            continue
        try:
            data = json.loads(raw)
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                title = post.get("title", "")
                body = post.get("selftext", "")
                combined = title + " " + body

                if not any(kw in combined.lower() for kw in ["interview", "offer", "hiring", "lpa", "ctc"]):
                    continue

                results.append({
                    "source":         f"reddit_{sub.lower()}",
                    "source_id":      post.get("id", ""),
                    "company":        extract_company(combined),
                    "role":           extract_role(combined),
                    "date_posted":    datetime.fromtimestamp(post["created_utc"]).strftime("%Y-%m-%d") if post.get("created_utc") else None,
                    "title":          title,
                    "body_raw":       body[:5000],
                    "overall_result": extract_result(combined),
                    "url":            f"https://reddit.com{post.get('permalink', '')}",
                    "rounds":         [],
                })
        except (json.JSONDecodeError, KeyError):
            pass
        time.sleep(1)

    return results


def scrape(max_experiences=60):
    """Main scraper: combine all sources."""
    results = []
    results.extend(scrape_experienced_devs(limit=20))
    time.sleep(1)
    results.extend(scrape_hn_interviews(limit=20))
    time.sleep(1)
    results.extend(scrape_india_career(limit=20))
    return results[:max_experiences]
