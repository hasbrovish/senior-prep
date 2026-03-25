"""
Reddit interview experience scraper.

Works in two modes:
  1. With REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET → OAuth2 (recommended, works on cloud)
  2. Without credentials → public .json endpoints (works locally, blocked on Railway)

Setup:
  1. Go to reddit.com/prefs/apps → create "script" app
  2. Set env vars: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
  3. Add to Railway variables panel → redeploy
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import base64
import time
import os
from datetime import datetime

from intel.config import REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT


SUBREDDITS = {
    "leetcode":           ["interview experience", "offer", "got hired",
                           "system design round", "rejected after"],
    "cscareerquestions":  ["interview experience", "SDE interview", "system design"],
    "leetcodedesi":       ["interview", "offer", "LPA", "experience", "selected"],
    "ExperiencedDevs":    ["interview experience", "offer", "senior engineer"],
    "developersIndia":    ["interview", "offer", "LPA", "ctc"],
    "IndiaTechies":       ["interview experience", "offer"],
}

_oauth_token = None
_token_expiry = 0


def _get_oauth_token():
    """Get Reddit OAuth2 bearer token using client credentials."""
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
        # Use OAuth API endpoint
        oauth_url = url.replace("https://www.reddit.com/", "https://oauth.reddit.com/")
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": REDDIT_USER_AGENT,
        }
    else:
        # Fallback: public .json endpoint
        oauth_url = url
        headers = {"User-Agent": REDDIT_USER_AGENT}

    for attempt in range(3):
        try:
            req = urllib.request.Request(oauth_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 403 and token:
                # OAuth blocked — force token refresh
                global _oauth_token
                _oauth_token = None
                return None
            if attempt < 2:
                time.sleep(2 ** attempt)
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  ⚠️  Reddit fetch failed {url[:60]}: {e}")
                return None
    return None


def fetch_subreddit_posts(subreddit, sort="new", limit=25):
    """Fetch latest posts from a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    data = _fetch_json(url)
    if not data:
        return []

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        posts.append({
            "id":        post.get("id"),
            "title":     post.get("title", ""),
            "selftext":  post.get("selftext", ""),
            "author":    post.get("author", ""),
            "score":     post.get("score", 0),
            "created":   post.get("created_utc"),
            "url":       f"https://reddit.com{post.get('permalink', '')}",
            "flair":     post.get("link_flair_text", ""),
            "num_comments": post.get("num_comments", 0),
            "subreddit": subreddit,
        })
    return posts


def search_subreddit(subreddit, query, limit=10):
    """Search a subreddit for specific terms."""
    encoded_q = urllib.parse.quote(query)
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={encoded_q}&restrict_sr=on&sort=new&limit={limit}"
    data = _fetch_json(url)
    if not data:
        return []

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        posts.append({
            "id":        post.get("id"),
            "title":     post.get("title", ""),
            "selftext":  post.get("selftext", ""),
            "author":    post.get("author", ""),
            "score":     post.get("score", 0),
            "created":   post.get("created_utc"),
            "url":       f"https://reddit.com{post.get('permalink', '')}",
            "flair":     post.get("link_flair_text", ""),
            "subreddit": subreddit,
        })
    return posts


def is_interview_experience(post):
    """Heuristic: is this post an interview experience?"""
    title = post.get("title", "").lower()
    text  = post.get("selftext", "").lower()
    flair = (post.get("flair") or "").lower()

    if "interview" in flair or "experience" in flair:
        return True

    exp_keywords = [
        "interview experience", "got offer", "got hired", "rejected",
        "interview round", "coding round", "system design round",
        "onsite interview", "phone screen", "final round",
        "offer letter", "lpa", "ctc", "compensation", "cleared"
    ]
    if sum(1 for kw in exp_keywords if kw in title) >= 1:
        return True

    body_keywords = [
        "round 1", "round 2", "coding round", "system design",
        "behavioral", "hr round", "offer", "rejected",
        "interviewer asked", "was asked to design", "dsa round"
    ]
    if sum(1 for kw in body_keywords if kw in text) >= 2:
        return True

    return False


def extract_company(text):
    """Extract company name from post text."""
    known = [
        "google", "amazon", "microsoft", "meta", "facebook", "apple", "netflix",
        "flipkart", "uber", "adobe", "goldman sachs", "walmart", "oracle",
        "razorpay", "phonepe", "cred", "swiggy", "zomato", "paytm", "meesho",
        "makemytrip", "juspay", "salesforce", "intuit", "atlassian",
        "stripe", "coinbase", "airbnb", "bytedance", "doordash", "samsara",
        "bloomberg", "deutsche bank", "nvidia", "tesla", "xai", "anthropic", "openai",
        "zerodha", "ola", "dream11", "groww", "nykaa", "dunzo", "sharechat",
        "infosys", "tcs", "wipro", "thoughtworks", "media.net", "samsung",
    ]
    text_lower = text.lower()
    for company in known:
        if company in text_lower:
            return company.title()

    import re
    match = re.search(r'(?:@|at|join|joined|offer from)\s+([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)', text)
    if match:
        return match.group(1)
    return "Unknown"


def extract_role(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["sde-3", "sde3", "l5", "senior sde", "staff", "e5", "e6"]):
        return "SDE-3"
    if any(w in text_lower for w in ["sde-2", "sde2", "l4", "e4", "sde ii"]):
        return "SDE-2"
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


def scrape(subreddits=None, max_per_sub=25):
    """Main scraper: fetch and normalize Reddit interview experiences."""
    if subreddits is None:
        subreddits = list(SUBREDDITS.keys())

    # Check if OAuth is configured
    has_oauth = bool(REDDIT_CLIENT_ID and REDDIT_SECRET)
    if has_oauth:
        token = _get_oauth_token()
        if token:
            print(f"  🔑 Reddit OAuth active")
        else:
            print(f"  ⚠️  Reddit OAuth failed — check REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET")
    else:
        print(f"  ℹ️  No Reddit API keys — using public endpoints (may be rate-limited)")

    all_results = []
    seen_ids = set()

    for sub in subreddits:
        search_terms = SUBREDDITS.get(sub, ["interview experience"])

        # Fetch newest posts
        posts = fetch_subreddit_posts(sub, sort="new", limit=max_per_sub)
        time.sleep(1)

        # Search for interview-specific content (first 2 terms only to avoid rate limits)
        for term in search_terms[:2]:
            search_posts = search_subreddit(sub, term, limit=10)
            posts.extend(search_posts)
            time.sleep(1)

        for post in posts:
            pid = post.get("id")
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)

            if not is_interview_experience(post):
                continue

            combined = post["title"] + " " + post["selftext"]
            ts = post.get("created")
            all_results.append({
                "source":         f"reddit_{sub}",
                "source_id":      pid,
                "company":        extract_company(combined),
                "role":           extract_role(combined),
                "date_posted":    datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts else None,
                "title":          post["title"],
                "body_raw":       post["selftext"][:5000],
                "overall_result": extract_result(combined),
                "url":            post["url"],
                "rounds":         [],
            })

    return all_results
