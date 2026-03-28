"""
Reddit interview experience scraper.

Priority order:
  1. ScrapeCreators API (SCRAPECREATORS_API_KEY) — no 403s, works on Railway/cloud
  2. Reddit OAuth (REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET) — requires app setup
  3. Public .json endpoints — works locally, blocked on Railway

ScrapeCreators: https://api.scrapecreators.com/v1/reddit
  - No Reddit app needed, paid API key (user already has it from last30days skill)
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

from intel.config import (
    REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT, SCRAPECREATORS_API_KEY
)

SCRAPECREATORS_BASE = "https://api.scrapecreators.com/v1/reddit"

# ── Target subreddits + search terms ─────────────────────────────────────────

SUBREDDITS = {
    "developersIndia":    ["interview experience", "offer", "LPA", "ctc",
                           "Razorpay", "PhonePe", "Flipkart", "CRED", "system design"],
    "leetcodedesi":       ["interview", "offer", "LPA", "experience", "selected",
                           "system design", "coding round"],
    "leetcode":           ["interview experience", "offer", "got hired",
                           "system design round", "rejected after"],
    "cscareerquestions":  ["interview experience", "SDE interview", "system design",
                           "offer negotiation", "coding round"],
    "ExperiencedDevs":    ["interview experience", "offer", "senior engineer",
                           "system design interview"],
    "IndiaTechies":       ["interview experience", "offer", "system design"],
}

COMPANY_QUERIES = [
    # FAANG/Big Tech
    ("Amazon",      "Amazon SDE-2 interview experience India"),
    ("Amazon",      "Amazon SDE-3 system design round"),
    ("Google",      "Google L4 L5 interview experience India"),
    ("Meta",        "Meta E4 E5 interview experience"),
    ("Microsoft",   "Microsoft SDE-2 interview experience India"),
    ("Apple",       "Apple SDE interview experience"),
    # Top Indian product companies (levels.fyi top paying)
    ("Flipkart",    "Flipkart SDE-2 machine coding round"),
    ("Razorpay",    "Razorpay SDE-2 interview experience"),
    ("PhonePe",     "PhonePe SDE-2 interview experience"),
    ("CRED",        "CRED interview experience SDE"),
    ("Swiggy",      "Swiggy SDE interview experience"),
    ("Zomato",      "Zomato SDE interview experience"),
    ("Meesho",      "Meesho SDE-2 interview experience"),
    ("Dream11",     "Dream11 SDE interview experience"),
    ("Groww",       "Groww SDE interview experience"),
    ("Zerodha",     "Zerodha SDE interview experience"),
    ("Juspay",      "Juspay SDE interview experience"),
    ("Navi",        "Navi SDE interview experience"),
    ("Slice",       "Slice SDE interview experience"),
    # Global high-paying
    ("Goldman Sachs","Goldman Sachs SDE interview India"),
    ("Stripe",      "Stripe software engineer interview"),
    ("Atlassian",   "Atlassian SDE interview India"),
    ("Adobe",       "Adobe MTS interview experience India"),
    ("Uber",        "Uber SDE-2 interview experience India"),
    ("LinkedIn",    "LinkedIn SDE interview India"),
    ("Salesforce",  "Salesforce SDE interview India"),
    ("Databricks",  "Databricks SDE interview experience"),
    ("Confluent",   "Confluent SDE interview experience"),
    ("Walmart",     "Walmart Labs SDE interview India"),
    # Finance/Fintech
    ("JP Morgan",   "JP Morgan SDE interview India"),
    ("Morgan Stanley","Morgan Stanley SDE interview India"),
    ("Deutsche Bank","Deutsche Bank SDE interview India"),
    # Other good companies
    ("Freshworks",  "Freshworks SDE interview experience"),
    ("BrowserStack","BrowserStack SDE interview experience"),
    ("Hashedin",    "Hashedin SDE interview experience"),
    ("MakeMyTrip",  "MakeMyTrip SDE interview experience"),
    ("Paytm",       "Paytm SDE interview experience"),
]

TARGET_SUBS_FOR_COMPANY = ["developersIndia", "leetcodedesi", "cscareerquestions",
                            "leetcode", "IndiaTechies"]

KNOWN_COMPANIES = [
    # FAANG + Big Tech
    "google", "amazon", "microsoft", "meta", "facebook", "apple", "netflix",
    "nvidia", "tesla", "uber", "airbnb", "linkedin", "twitter", "x",
    "tiktok", "bytedance", "snap", "snapchat", "discord", "reddit",
    "twitch", "youtube", "whatsapp", "instagram", "oculus",
    # AI
    "openai", "anthropic", "perplexity", "mistral", "cohere", "xai",
    "deepmind", "google deepmind", "cognition", "elevenlabs", "harvey",
    "midjourney", "cursor", "replit", "langchain", "scale ai",
    # Top Indian product
    "flipkart", "swiggy", "razorpay", "phonepe", "cred", "zomato",
    "meesho", "dream11", "groww", "zerodha", "juspay", "paytm",
    "navi", "slice", "jar", "jupiter", "mobikwik", "nykaa", "myntra",
    "makemytrip", "ola", "dunzo", "sharechat", "truecaller", "freshworks",
    "zoho", "browserstack", "hashedin", "media.net", "moengage", "clevertap",
    "pubmatic", "inmobi", "reliance retail", "jio", "lenskart", "udaan",
    "directi", "werise", "gameberry",
    # Global high-paying tech
    "stripe", "atlassian", "adobe", "salesforce", "intuit", "servicenow",
    "databricks", "snowflake", "confluent", "twilio", "datadog", "splunk",
    "crowdstrike", "palo alto networks", "sentinelone", "okta",
    "figma", "canva", "notion", "vercel", "webflow", "airtable",
    "asana", "monday", "slack", "zoom", "hubspot", "zendesk",
    "intercom", "mixpanel", "amplitude", "braze",
    "shopify", "etsy", "wayfair", "chewy", "instacart", "doordash",
    "lyft", "grubhub", "deliveroo", "booking.com", "expedia", "agoda",
    "opendoor", "redfin", "zillow",
    "spotify", "duolingo", "coursera", "roblox", "unity",
    "samsara", "waymo", "cruise", "nuro", "lucid",
    "plaid", "brex", "robinhood", "chime", "affirm", "klarna",
    "coinbase", "ripple", "opensea", "paxos",
    "gitlab", "github", "hashicorp", "mongodb", "elastic",
    "sentry", "launchdarkly", "retool", "rippling", "deel", "gusto",
    "calendly", "loom", "grammarly", "docusign", "box", "dropbox",
    "algolia", "fullstory",
    # Finance
    "goldman sachs", "goldman", "morgan stanley", "jp morgan", "jpmorgan",
    "jp morgan chase", "barclays", "deutsche bank", "hsbc", "citi",
    "bank of america", "wells fargo", "charles schwab", "blackrock",
    "jane street", "citadel", "two sigma", "hudson river trading",
    "capital one", "american express", "mastercard", "visa", "paypal",
    "square", "block", "revolut", "wise", "nubank", "sofi",
    # Enterprise / Cloud
    "oracle", "ibm", "sap", "cisco", "qualcomm", "intel", "amd",
    "samsung", "sony", "vmware", "workday", "walmart labs", "walmart",
    "target", "ebay", "shopee", "aws",
    # Others from levels.fyi list
    "palantir", "anduril", "lockheed martin", "disney", "electronic arts",
    "activision", "zynga", "quora", "pinterest", "tinder",
    "deloitte", "accenture", "mckinsey", "bcg", "pwc",
    "infosys", "tcs", "wipro", "cognizant", "epam", "thoughtworks",
    "bloomberg", "lseg", "tekion", "samsara",
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


# ── ScrapeCreators API ────────────────────────────────────────────────────────

def _sc_get(path, params):
    """Call ScrapeCreators Reddit API."""
    url = f"{SCRAPECREATORS_BASE}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"x-api-key": SCRAPECREATORS_API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f"  ⚠️  ScrapeCreators {e.code} for {path}: {body}")
        return None
    except Exception as e:
        print(f"  ⚠️  ScrapeCreators error {path}: {e}")
        return None


def _sc_parse_posts(data):
    """Parse ScrapeCreators response into normalized post dicts."""
    posts = []
    if not data:
        return posts
    # Response shape: {"data": {"children": [...]}} or {"posts": [...]}
    children = (data.get("data") or {}).get("children") or data.get("posts") or []
    for child in children:
        p = child.get("data") or child  # ScrapeCreators may skip the "data" wrapper
        if not p:
            continue
        posts.append({
            "id":           p.get("id", ""),
            "title":        p.get("title", ""),
            "selftext":     p.get("selftext", "") or p.get("body", ""),
            "author":       p.get("author", ""),
            "score":        p.get("score", 0) or p.get("ups", 0),
            "created":      p.get("created_utc") or p.get("created"),
            "url":          (f"https://reddit.com{p['permalink']}"
                             if p.get("permalink") else p.get("url", "")),
            "flair":        p.get("link_flair_text", "") or "",
            "num_comments": p.get("num_comments", 0),
            "subreddit":    p.get("subreddit", ""),
        })
    return posts


def _sc_fetch_subreddit(subreddit, query="interview experience", sort="new", timeframe="month", limit=25):
    # ScrapeCreators only supports subreddit/search (not bare listing)
    data = _sc_get("subreddit/search", {
        "subreddit": subreddit, "query": query,
        "sort": sort, "timeframe": timeframe,
    })
    posts = _sc_parse_posts(data)
    return posts[:limit]


def _sc_global_search(query, sort="relevance", timeframe="month"):
    data = _sc_get("search", {"query": query, "sort": sort, "timeframe": timeframe})
    return _sc_parse_posts(data)


def _sc_fetch_comments(post_url, max_comments=6):
    data = _sc_get("post/comments", {"url": post_url})
    if not data:
        return []
    comments = []
    raw = data.get("comments") or (data.get("data") or {}).get("children") or []
    for c in raw:
        cd = c.get("data") or c
        body = (cd.get("body") or "").strip()
        if not body or body in ("[deleted]", "[removed]") or len(body) < 20:
            continue
        comments.append({
            "author": cd.get("author", ""),
            "score":  cd.get("score", 0) or cd.get("ups", 0),
            "text":   body[:600],
        })
    return sorted(comments, key=lambda x: x["score"], reverse=True)[:max_comments]


# ── Public/OAuth Reddit API (fallback) ────────────────────────────────────────

def _fetch_json(url):
    token = _get_oauth_token()
    if token:
        url = url.replace("https://www.reddit.com/", "https://oauth.reddit.com/")
        headers = {"Authorization": f"Bearer {token}", "User-Agent": REDDIT_USER_AGENT}
    else:
        headers = {"User-Agent": REDDIT_USER_AGENT}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = int(e.headers.get("X-Ratelimit-Reset", "60")) + 1
                print(f"  ⏳ Reddit 429 — waiting {wait}s")
                time.sleep(wait)
            elif attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  ⚠️  Reddit HTTP {e.code} for {url[:60]}")
                return None
        except Exception:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return None
    return None


def _fetch_json_posts(url):
    data = _fetch_json(url)
    if not data:
        return []
    posts = []
    for child in data.get("data", {}).get("children", []):
        p = child.get("data", {})
        posts.append({
            "id":           p.get("id", ""),
            "title":        p.get("title", ""),
            "selftext":     p.get("selftext", ""),
            "author":       p.get("author", ""),
            "score":        p.get("score", 0),
            "created":      p.get("created_utc"),
            "url":          f"https://reddit.com{p.get('permalink', '')}",
            "flair":        p.get("link_flair_text", "") or "",
            "num_comments": p.get("num_comments", 0),
            "subreddit":    p.get("subreddit", ""),
        })
    return posts


# ── Parsing helpers ────────────────────────────────────────────────────────────

def is_interview_experience(post):
    title = post.get("title", "").lower()
    text  = post.get("selftext", "").lower()
    flair = (post.get("flair") or "").lower()
    score = post.get("score", 0)
    if score < -5:
        return False
    if any(w in flair for w in ["interview", "experience", "offer"]):
        return True
    title_kws = [
        "interview experience", "got offer", "got hired", "rejected",
        "interview round", "coding round", "system design round",
        "onsite interview", "phone screen", "final round",
        "offer letter", "lpa", "ctc", "cleared", "interview questions",
        "asked me", "rounds at",
    ]
    if any(kw in title for kw in title_kws):
        return True
    body_kws = [
        "round 1", "round 2", "coding round", "system design",
        "behavioral round", "hr round", "offer", "rejected",
        "interviewer asked", "was asked to", "dsa round",
        "technical round", "machine coding",
    ]
    if sum(1 for kw in body_kws if kw in text) >= 2:
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
    return match.group(1) if match else None


def extract_role(text):
    t = text.lower()
    if any(w in t for w in ["sde-3", "sde3", "l5", "senior sde", "staff", "e5", "e6"]):
        return "SDE-3"
    if any(w in t for w in ["sde-2", "sde2", "l4", "e4", "sde ii"]):
        return "SDE-2"
    if any(w in t for w in ["sde-1", "sde1", "l3", "new grad", "fresher", "entry level"]):
        return "SDE-1"
    return "SDE-2"


def extract_result(text):
    t = text.lower()
    if any(w in t for w in ["got offer", "got the offer", "accepted offer",
                             "selected", "offer letter", "joining", "cleared all"]):
        return "offer"
    if any(w in t for w in ["rejected", "reject", "didn't clear",
                             "not selected", "ghosted", "no offer"]):
        return "reject"
    return "unknown"


def _build_experience(post, comment_text="", company_hint=None):
    combined_title = post["title"] + " " + post["selftext"]
    combined_all   = combined_title + " " + comment_text
    company = extract_company(combined_all) or company_hint
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


# ── Main scraper ──────────────────────────────────────────────────────────────

def scrape(subreddits=None, max_per_sub=25, enrich_comments=True):
    """
    Fetch Reddit interview experiences.
    Uses ScrapeCreators API if key present (recommended),
    falls back to Reddit OAuth → public endpoints.
    """
    if subreddits is None:
        subreddits = list(SUBREDDITS.keys())

    use_sc = bool(SCRAPECREATORS_API_KEY)
    has_oauth = bool(REDDIT_CLIENT_ID and REDDIT_SECRET)

    if use_sc:
        print(f"  🟢 Reddit via ScrapeCreators API (no 403 issues)")
    elif has_oauth:
        print(f"  🔑 Reddit via OAuth")
    else:
        print(f"  ℹ️  Reddit via public endpoints (may 403 on Railway)")

    all_posts = []
    seen_ids = set()

    # ── Phase 1: per-subreddit fetch ──────────────────────────────────────────
    for sub in subreddits:
        if use_sc:
            posts = _sc_fetch_subreddit(sub, sort="new", timeframe="month", limit=max_per_sub)
            time.sleep(0.5)
            top_posts = _sc_fetch_subreddit(sub, sort="top", timeframe="month", limit=10)
            time.sleep(0.5)
            # Search for interview keywords
            for term in SUBREDDITS.get(sub, [])[:3]:
                s_posts = _sc_fetch_subreddit(sub, query=term, sort="relevance",
                                               timeframe="month", limit=10)
                for p in s_posts:
                    pid = p.get("id")
                    if pid and pid not in seen_ids and is_interview_experience(p):
                        seen_ids.add(pid)
                        all_posts.append(p)
                time.sleep(0.4)
        else:
            posts = _fetch_json_posts(
                f"https://www.reddit.com/r/{sub}/new.json?limit={max_per_sub}")
            time.sleep(0.8)
            top_posts = _fetch_json_posts(
                f"https://www.reddit.com/r/{sub}/top.json?limit=10")
            time.sleep(0.8)
            for term in SUBREDDITS.get(sub, [])[:2]:
                eq = urllib.parse.quote(term)
                s_posts = _fetch_json_posts(
                    f"https://www.reddit.com/r/{sub}/search.json"
                    f"?q={eq}&restrict_sr=on&sort=new&t=month&limit=10")
                for p in s_posts:
                    pid = p.get("id")
                    if pid and pid not in seen_ids and is_interview_experience(p):
                        seen_ids.add(pid)
                        all_posts.append(p)
                time.sleep(1)

        for post in posts + top_posts:
            pid = post.get("id")
            if pid and pid not in seen_ids and is_interview_experience(post):
                seen_ids.add(pid)
                all_posts.append(post)

    # ── Phase 2: targeted company searches ───────────────────────────────────
    for company, query in COMPANY_QUERIES:
        if use_sc:
            # Global search across all Reddit
            posts = _sc_global_search(query, sort="relevance", timeframe="year")
            time.sleep(0.5)
        else:
            posts = []
            for sub in TARGET_SUBS_FOR_COMPANY[:3]:
                eq = urllib.parse.quote(query)
                sub_posts = _fetch_json_posts(
                    f"https://www.reddit.com/r/{sub}/search.json"
                    f"?q={eq}&restrict_sr=on&sort=relevance&t=year&limit=10")
                posts.extend(sub_posts)
                time.sleep(0.8)

        for post in posts:
            pid = post.get("id")
            if pid and pid not in seen_ids:
                seen_ids.add(pid)
                if is_interview_experience(post):
                    all_posts.append(post)

    # ── Phase 3: enrich top posts with comments ───────────────────────────────
    final = []
    sorted_posts = sorted(all_posts, key=lambda p: p.get("num_comments", 0), reverse=True)
    enrich_limit = 20 if enrich_comments else 0
    enriched = set()

    for i, post in enumerate(sorted_posts):
        pid = post["id"]
        comment_text = ""
        if enrich_comments and i < enrich_limit and pid not in enriched and post.get("url"):
            if use_sc:
                comments = _sc_fetch_comments(post["url"], max_comments=6)
            else:
                sub = post.get("subreddit", "")
                url = (f"https://www.reddit.com/r/{sub}/comments/{pid}/.json?limit=6")
                data = _fetch_json(url)
                comments = []
                if data and isinstance(data, list) and len(data) >= 2:
                    for child in data[1].get("data", {}).get("children", []):
                        c = child.get("data", {})
                        body = (c.get("body") or "").strip()
                        if body and body not in ("[deleted]", "[removed]") and len(body) > 20:
                            comments.append({"score": c.get("score", 0),
                                             "text": body[:600]})
                    comments = sorted(comments, key=lambda x: x["score"], reverse=True)[:6]

            if comments:
                comment_text = "\n".join(f"• {c['text']}" for c in comments)
            enriched.add(pid)
            time.sleep(0.3)

        final.append(_build_experience(post, comment_text=comment_text))

    mode = "ScrapeCreators" if use_sc else ("OAuth" if has_oauth else "public")
    print(f"  🔴 Reddit ({mode}): {len(final)} experiences fetched ({len(enriched)} enriched)")
    return final


if __name__ == "__main__":
    r = scrape(max_per_sub=10, enrich_comments=False)
    for x in r[:5]:
        print(x.get("company"), "|", x["title"][:60])
