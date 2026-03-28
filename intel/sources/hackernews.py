"""
HackerNews interview experience scraper.

Uses the Algolia HN Search API — completely free, no authentication needed.
Inspired by last30days-skill's hackernews.py approach.

API docs: https://hn.algolia.com/api
"""

import json
import re
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta


HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"
HN_SEARCH_BY_DATE_URL = "https://hn.algolia.com/api/v1/search_by_date"
HN_ITEMS_URL = "https://hn.algolia.com/api/v1/items"


# Queries most likely to return interview experiences
INTERVIEW_QUERIES = [
    "software engineer interview experience India",
    "SDE2 SDE3 interview experience",
    "Amazon SDE interview experience",
    "Google L4 L5 interview experience",
    "Flipkart SDE interview",
    "Razorpay PhonePe interview experience",
    "system design interview questions asked",
    "coding interview experience offer",
    "FAANG interview experience India",
    "startup interview experience India SDE",
]

# For "Ask HN: Who is hiring" style threads
ASK_HN_QUERIES = [
    "Ask HN: Who got an interesting interview",
    "Ask HN: Interview",
    "Tell HN interview experience",
]

KNOWN_COMPANIES = [
    "google", "amazon", "microsoft", "meta", "facebook", "apple", "netflix",
    "flipkart", "uber", "adobe", "goldman sachs", "walmart", "oracle",
    "razorpay", "phonepe", "cred", "swiggy", "paytm", "meesho",
    "makemytrip", "juspay", "salesforce", "intuit", "atlassian",
    "stripe", "coinbase", "airbnb", "bytedance", "doordash",
    "infosys", "tcs", "wipro", "thoughtworks", "media.net",
    "zomato", "ola", "dream11", "groww", "zerodha", "nykaa",
    "jp morgan", "jpmorgan", "morgan stanley", "deutsche bank",
    "samsung", "qualcomm", "nvidia", "directi", "sharechat", "myntra",
    "dunzo", "lenskart", "udaan",
]


def _fetch_json(url, params=None, timeout=15):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "PrepForge/1.0 (interview prep research bot)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"  ⚠️  HN fetch error {url[:60]}: {e}")
        return None


def _strip_html(text):
    """Remove HTML tags from HN comment text."""
    if not text:
        return ""
    text = re.sub(r"<p>", "\n", text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"&#x27;", "'", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_company(text):
    text_lower = text.lower()
    for company in KNOWN_COMPANIES:
        if company in text_lower:
            return company.title().replace("Jp Morgan", "JP Morgan")
    match = re.search(
        r'(?:at|@|joined|offer from|interviewing at|interview at)\s+([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)',
        text
    )
    if match:
        return match.group(1)
    return None


def _extract_role(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["sde-3", "sde3", "l5", "senior engineer", "staff", "e5", "e6"]):
        return "SDE-3"
    if any(w in text_lower for w in ["sde-2", "sde2", "l4", "e4", "sde ii"]):
        return "SDE-2"
    if any(w in text_lower for w in ["sde-1", "sde1", "l3", "new grad", "fresher", "entry"]):
        return "SDE-1"
    return "SDE-2"


def _extract_result(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["got offer", "got the offer", "accepted", "selected",
                                      "joining", "cleared all rounds", "offer letter"]):
        return "offer"
    if any(w in text_lower for w in ["rejected", "didn't get", "no offer", "failed",
                                      "ghosted", "not selected"]):
        return "reject"
    return "unknown"


def _is_interview_experience(title, story_text=""):
    """Is this HN story actually an interview experience?"""
    combined = (title + " " + story_text).lower()
    must_have = ["interview", "experience", "hiring", "offer", "rejected",
                 "coding round", "system design", "dsa round", "technical round",
                 "onsite", "hired", "job search"]
    return any(kw in combined for kw in must_have)


def _fetch_story_comments(story_id, max_comments=5):
    """Fetch top-level comments for a story — often contain round details."""
    data = _fetch_json(f"{HN_ITEMS_URL}/{story_id}")
    if not data:
        return []

    comments = []
    for child in (data.get("children") or [])[:max_comments]:
        text = _strip_html(child.get("text") or "")
        if not text or len(text) < 20:
            continue
        comments.append({
            "author": child.get("author", ""),
            "score":  child.get("points") or 0,
            "text":   text[:500],
        })
    return comments


def search_hackernews(query, days_back=90, limit=20):
    """Search HN stories for a query, return normalised experience dicts."""
    from_ts = int((datetime.now() - timedelta(days=days_back)).timestamp())

    data = _fetch_json(HN_SEARCH_BY_DATE_URL, params={
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{from_ts}",
        "hitsPerPage": limit,
    })
    if not data:
        return []

    results = []
    for hit in data.get("hits", []):
        title      = hit.get("title") or ""
        story_text = hit.get("story_text") or ""
        story_text = _strip_html(story_text)

        if not _is_interview_experience(title, story_text):
            continue

        story_id = hit.get("objectID", "")
        ts = hit.get("created_at_i")
        combined = title + " " + story_text

        results.append({
            "story_id":    story_id,
            "title":       title,
            "story_text":  story_text[:5000],
            "author":      hit.get("author", ""),
            "points":      hit.get("points", 0),
            "num_comments": hit.get("num_comments", 0),
            "url":         hit.get("url") or f"https://news.ycombinator.com/item?id={story_id}",
            "date_ts":     ts,
            "company":     _extract_company(combined),
            "role":        _extract_role(combined),
            "result":      _extract_result(combined),
        })
    return results


def _enrich_with_comments(stories, enrich_limit=5):
    """Append top comments to story body_raw for top N stories."""
    # Sort by points, enrich top ones
    top = sorted(stories, key=lambda s: s.get("points", 0), reverse=True)[:enrich_limit]
    for s in top:
        comments = _fetch_story_comments(s["story_id"], max_comments=5)
        if comments:
            comment_text = "\n\n".join(f"[Comment] {c['text']}" for c in comments)
            s["story_text"] = (s.get("story_text") or "") + "\n\n" + comment_text
        time.sleep(0.5)
    return stories


def _normalize(story):
    """Convert enriched story dict → intel DB experience dict."""
    ts = story.get("date_ts")
    body = (story.get("story_text") or "").strip()
    return {
        "source":         "hackernews",
        "source_id":      str(story["story_id"]),
        "company":        story.get("company"),
        "role":           story.get("role", "SDE-2"),
        "date_posted":    datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts else None,
        "title":          story["title"],
        "body_raw":       body[:5000],
        "overall_result": story.get("result", "unknown"),
        "url":            story["url"],
        "rounds":         [],
    }


def scrape(days_back=365, max_per_query=15):
    """
    Main scraper: search HN for interview experiences and normalize results.
    No API key needed — uses public Algolia HN Search API.
    """
    all_stories = []
    seen_ids = set()

    for query in INTERVIEW_QUERIES:
        stories = search_hackernews(query, days_back=days_back, limit=max_per_query)
        for s in stories:
            sid = s["story_id"]
            if sid and sid not in seen_ids:
                seen_ids.add(sid)
                all_stories.append(s)
        time.sleep(0.3)

    # Enrich top stories with comment text (where real round details live)
    all_stories = _enrich_with_comments(all_stories, enrich_limit=8)

    results = [_normalize(s) for s in all_stories]
    print(f"  📰 HackerNews: {len(results)} stories fetched")
    return results


if __name__ == "__main__":
    r = scrape()
    for x in r[:3]:
        print(x["company"], "|", x["title"][:60])
