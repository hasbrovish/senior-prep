"""
Reddit interview experience scraper.

Works in two modes:
  1. With REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET → OAuth2 (recommended, works on cloud)
  2. Without credentials → public .json endpoints (works locally, blocked on Railway)

Setup:
  1. Go to reddit.com/prefs/apps → create "script" app
  2. Set env vars: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
  3. Add to Railway variables panel → redeploy

Improvements over v1 (inspired by last30days-skill):
  - Comment enrichment: fetches top comments for high-signal posts (questions live there)
  - Targeted company searches: 15 company-specific query pairs
  - Score filtering: skips low-quality posts (score < 2)
  - Better relevance: title + flair + body keyword weighting
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import base64
import time
import re
import os
from datetime import datetime

from intel.config import REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT


# ── Subreddits + generic search terms ────────────────────────────────────────

SUBREDDITS = {
    "leetcode":           ["interview experience", "offer", "got hired",
                           "system design round", "rejected after"],
    "cscareerquestions":  ["interview experience", "SDE interview", "system design",
                           "offer negotiation", "coding round"],
    "leetcodedesi":       ["interview", "offer", "LPA", "experience", "selected",
                           "system design", "coding round"],
    "ExperiencedDevs":    ["interview experience", "offer", "senior engineer",
                           "system design interview"],
    "developersIndia":    ["interview", "offer", "LPA", "ctc", "selected",
                           "Razorpay", "PhonePe", "Flipkart", "CRED"],
    "IndiaTechies":       ["interview experience", "offer", "system design"],
    "cscareerquestions":  ["interview experience India", "SDE-2 offer"],
}

# ── Targeted company + query pairs (searched across all relevant subreddits) ─

COMPANY_QUERIES = [
    ("Amazon",     "Amazon SDE-2 interview experience"),
    ("Amazon",     "Amazon SDE-3 system design round"),
    ("Google",     "Google L4 L5 interview experience"),
    ("Flipkart",   "Flipkart SDE-2 machine coding round"),
    ("Razorpay",   "Razorpay SDE-2 interview experience"),
    ("PhonePe",    "PhonePe SDE-2 interview"),
    ("CRED",       "CRED interview experience SDE"),
    ("Microsoft",  "Microsoft SDE-2 interview experience India"),
    ("Swiggy",     "Swiggy SDE interview experience"),
    ("Goldman",    "Goldman Sachs SDE interview"),
    ("Stripe",     "Stripe software engineer interview"),
    ("Meta",       "Meta E4 E5 interview experience"),
    ("Atlassian",  "Atlassian SDE interview"),
    ("Adobe",      "Adobe MTS interview experience"),
    ("Uber",       "Uber SDE-2 interview experience"),
]

TARGET_SUBS_FOR_COMPANY = ["developersIndia", "leetcodedesi", "cscareerquestions",
                            "leetcode", "IndiaTechies"]

KNOWN_COMPANIES = [
    "google", "amazon", "microsoft", "meta", "facebook", "apple", "netflix",
    "flipkart", "uber", "adobe", "goldman sachs", "walmart", "oracle",
    "razorpay", "phonepe", "cred", "swiggy", "zomato", "paytm", "meesho",
    "makemytrip", "juspay", "salesforce", "intuit", "atlassian",
    "stripe", "coinbase", "airbnb", "bytedance", "doordash", "samsara",
    "bloomberg", "deutsche bank", "nvidia", "tesla",
    "zerodha", "ola", "dream11", "groww", "nykaa", "dunzo", "sharechat",
    "infosys", "tcs", "wipro", "thoughtworks", "media.net", "samsung",
    "lenskart", "udaan", "myntra",
]

# ── OAuth state ───────────────────────────────────────────────────────────────

_oauth_token = None
_token_expiry = 0


def _get_oauth_token():
    global _oauth_token, _token_expiry

    if _oauth_token and time.time() < _token_expiry - 60:
        return _oauth_token

    if not REDDIT_CLIENT_ID or not REDDIT_SECRET:
        return None

    credentials = base64.b64encode(
        f"{REDDIT_CLIENT_ID}:{REDDIT_SECRET}".encode()
    ).decode()

    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token",
        data=data,
        headers={
            "Authorization": f"Basic {credentials}",
            "User-Agent": REDDIT_USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            _oauth_token = result.get("access_token")
            _token_expiry = time.time() + result.get("expires_in", 3600)
            return _oauth_token
    except Exception as e:
        print(f"  ⚠️  Reddit OAuth failed: {e}")
        return None


def _fetch_json(url, use_oauth=True):
    """Fetch Reddit JSON with OAuth if available, fallback to public API."""
    token = _get_oauth_token() if use_oauth else None

    if token:
        oauth_url = url.replace("https://www.reddit.com/", "https://oauth.reddit.com/")
        headers = {"Authorization": f"Bearer {token}", "User-Agent": REDDIT_USER_AGENT}
    else:
        oauth_url = url
        headers = {"User-Agent": REDDIT_USER_AGENT}

    for attempt in range(3):
        try:
            req = urllib.request.Request(oauth_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                remaining = resp.headers.get("X-Ratelimit-Remaining", "99")
                reset_secs = resp.headers.get("X-Ratelimit-Reset", "0")
                try:
                    if float(remaining) < 5:
                        wait = min(int(reset_secs) + 1, 30)
                        time.sleep(wait)
                except (ValueError, TypeError):
                    pass
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = int(e.headers.get("X-Ratelimit-Reset", "60")) + 1
                print(f"  ⏳ Reddit 429 — waiting {wait}s")
                time.sleep(wait)
            elif e.code == 403 and token:
                global _oauth_token
                _oauth_token = None
                return None
            elif attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  ⚠️  Reddit HTTP {e.code} for {url[:60]}")
                return None
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  ⚠️  Reddit fetch failed {url[:60]}: {e}")
                return None
    return None


def _parse_posts(data):
    posts = []
    for child in (data or {}).get("data", {}).get("children", []):
        p = child.get("data", {})
        posts.append({
            "id":           p.get("id"),
            "title":        p.get("title", ""),
            "selftext":     p.get("selftext", ""),
            "author":       p.get("author", ""),
            "score":        p.get("score", 0),
            "created":      p.get("created_utc"),
            "url":          f"https://reddit.com{p.get('permalink', '')}",
            "flair":        p.get("link_flair_text", ""),
            "num_comments": p.get("num_comments", 0),
            "subreddit":    p.get("subreddit", ""),
        })
    return posts


def fetch_subreddit_posts(subreddit, sort="new", limit=25):
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    data = _fetch_json(url)
    return _parse_posts(data) if data else []


def search_subreddit(subreddit, query, limit=15, sort="new", time_filter="month"):
    encoded_q = urllib.parse.quote(query)
    url = (f"https://www.reddit.com/r/{subreddit}/search.json"
           f"?q={encoded_q}&restrict_sr=on&sort={sort}&t={time_filter}&limit={limit}")
    data = _fetch_json(url)
    return _parse_posts(data) if data else []


def fetch_post_comments(subreddit, post_id, max_comments=8):
    """
    Fetch top comments for a post — this is where interviewers describe rounds/questions.
    Returns list of {author, score, text} dicts.
    """
    url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}/.json?limit={max_comments}"
    data = _fetch_json(url)
    if not data or not isinstance(data, list) or len(data) < 2:
        return []

    comments = []
    for child in data[1].get("data", {}).get("children", []):
        c = child.get("data", {})
        body = (c.get("body") or "").strip()
        if not body or body in ("[deleted]", "[removed]") or len(body) < 20:
            continue
        comments.append({
            "author": c.get("author", ""),
            "score":  c.get("score", 0),
            "text":   body[:600],
        })
    # Sort by score — top comments first
    return sorted(comments, key=lambda x: x["score"], reverse=True)[:max_comments]


def is_interview_experience(post):
    """Heuristic: is this post an actual interview experience report?"""
    title = post.get("title", "").lower()
    text  = post.get("selftext", "").lower()
    flair = (post.get("flair") or "").lower()
    score = post.get("score", 0)

    # Skip very low quality
    if score < -5:
        return False

    if "interview" in flair or "experience" in flair or "offer" in flair:
        return True

    title_keywords = [
        "interview experience", "got offer", "got hired", "rejected",
        "interview round", "coding round", "system design round",
        "onsite interview", "phone screen", "final round",
        "offer letter", "lpa", "ctc", "compensation", "cleared",
        "interview questions", "asked me", "rounds at",
    ]
    if sum(1 for kw in title_keywords if kw in title) >= 1:
        return True

    body_keywords = [
        "round 1", "round 2", "coding round", "system design",
        "behavioral round", "hr round", "offer", "rejected",
        "interviewer asked", "was asked to", "dsa round",
        "technical round", "machine coding",
    ]
    if sum(1 for kw in body_keywords if kw in text) >= 2:
        return True

    return False


def extract_company(text):
    text_lower = text.lower()
    for company in KNOWN_COMPANIES:
        if company in text_lower:
            return company.title().replace("Jp Morgan", "JP Morgan")
    match = re.search(
        r'(?:@|at|join(?:ed)?|offer from|interviewing at|interview(?:ed)? at)\s+'
        r'([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)',
        text
    )
    if match:
        return match.group(1)
    return None


def extract_role(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["sde-3", "sde3", "l5", "senior sde", "staff", "e5", "e6"]):
        return "SDE-3"
    if any(w in text_lower for w in ["sde-2", "sde2", "l4", "e4", "sde ii"]):
        return "SDE-2"
    if any(w in text_lower for w in ["sde-1", "sde1", "l3", "new grad", "fresher", "entry level"]):
        return "SDE-1"
    return "SDE-2"


def extract_result(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["got offer", "got the offer", "accepted offer",
                                      "selected", "offer letter", "joining", "cleared all"]):
        return "offer"
    if any(w in text_lower for w in ["rejected", "reject", "didn't clear",
                                      "not selected", "ghosted", "no offer"]):
        return "reject"
    return "unknown"


def _build_experience(post, comment_text="", company_hint=None):
    """Merge post + comments into a single experience dict."""
    combined_title = post["title"] + " " + post["selftext"]
    combined_all   = combined_title + " " + comment_text

    company = extract_company(combined_all)
    if not company and company_hint:
        company = company_hint

    # Append enriched comment text to body_raw
    body_raw = post["selftext"]
    if comment_text:
        body_raw = body_raw + "\n\n--- TOP COMMENTS ---\n" + comment_text

    ts = post.get("created")
    return {
        "source":         f"reddit_{post.get('subreddit', 'reddit')}",
        "source_id":      post["id"],
        "company":        company,
        "role":           extract_role(combined_all),
        "date_posted":    datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts else None,
        "title":          post["title"],
        "body_raw":       body_raw[:5000],
        "overall_result": extract_result(combined_all),
        "url":            post["url"],
        "rounds":         [],
    }


def scrape(subreddits=None, max_per_sub=25, enrich_comments=True):
    """
    Main scraper: fetch + normalize Reddit interview experiences.

    - Fetches newest posts from each subreddit
    - Runs targeted company searches across key subreddits
    - Enriches top posts with comment text (questions are often in comments)
    """
    if subreddits is None:
        subreddits = list(SUBREDDITS.keys())

    has_oauth = bool(REDDIT_CLIENT_ID and REDDIT_SECRET)
    if has_oauth:
        token = _get_oauth_token()
        print(f"  {'🔑 Reddit OAuth active' if token else '⚠️  Reddit OAuth failed — check env vars'}")
    else:
        print(f"  ℹ️  No Reddit API keys — using public endpoints (may be rate-limited)")

    all_results = []
    seen_ids = set()

    # ── Phase 1: newest posts from each subreddit ─────────────────────────────
    for sub in subreddits:
        posts = fetch_subreddit_posts(sub, sort="new", limit=max_per_sub)
        time.sleep(0.8)

        # Also pull "top" posts from last month for high-quality experiences
        top_posts = fetch_subreddit_posts(sub, sort="top", limit=10)
        time.sleep(0.8)

        for post in posts + top_posts:
            pid = post.get("id")
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)
            if is_interview_experience(post):
                all_results.append(post)

        # Keyword search (first 2 terms to avoid rate limits)
        for term in SUBREDDITS.get(sub, [])[:2]:
            search_posts = search_subreddit(sub, term, limit=10)
            for post in search_posts:
                pid = post.get("id")
                if pid and pid not in seen_ids and is_interview_experience(post):
                    seen_ids.add(pid)
                    all_results.append(post)
            time.sleep(1)

    # ── Phase 2: targeted company searches ───────────────────────────────────
    for company, query in COMPANY_QUERIES:
        for sub in TARGET_SUBS_FOR_COMPANY[:3]:
            posts = search_subreddit(sub, query, limit=10, sort="relevance", time_filter="year")
            for post in posts:
                pid = post.get("id")
                if pid and pid not in seen_ids:
                    seen_ids.add(pid)
                    if is_interview_experience(post):
                        all_results.append(post)
            time.sleep(0.8)

    # ── Phase 3: enrich top posts with comments ───────────────────────────────
    final = []
    # Sort by num_comments (most discussed = richest in round details)
    sorted_posts = sorted(all_results, key=lambda p: p.get("num_comments", 0), reverse=True)
    enrich_limit = 15 if enrich_comments else 0
    enriched_ids = set()

    for i, post in enumerate(sorted_posts):
        pid = post["id"]
        comment_text = ""

        if enrich_comments and i < enrich_limit and pid not in enriched_ids:
            sub = post.get("subreddit", "")
            comments = fetch_post_comments(sub, pid, max_comments=6)
            if comments:
                comment_text = "\n".join(f"• {c['text']}" for c in comments)
            enriched_ids.add(pid)
            time.sleep(0.5)

        final.append(_build_experience(post, comment_text=comment_text))

    print(f"  🔴 Reddit: {len(final)} experiences fetched ({len(enriched_ids)} enriched with comments)")
    return final


if __name__ == "__main__":
    r = scrape()
    for x in r[:3]:
        print(x.get("company"), "|", x["title"][:60])
