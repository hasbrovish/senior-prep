"""
Reddit interview experience scraper.
Works in two modes:
  1. With PRAW (pip install praw) + API keys → full access
  2. Without API keys → uses Reddit's public .json endpoints (rate-limited)
"""

import json
import urllib.request
import urllib.error
import time
from datetime import datetime


# Subreddits to scrape for interview experiences
SUBREDDITS = {
    "leetcode":           {"search": ["interview experience", "offer", "got hired",
                                      "system design round", "rejected after"],
                           "flairs": ["Interview Experience", "Interview Question"]},
    "cscareerquestions":  {"search": ["interview experience", "offer negotiation",
                                      "SDE interview", "system design"],
                           "flairs": []},
    "leetcodedesi":       {"search": ["interview", "offer", "LPA", "compensation",
                                      "experience", "selected"],
                           "flairs": []},
    "ExperiencedDevs":    {"search": ["interview", "system design", "senior engineer"],
                           "flairs": []},
}


def _fetch_json(url, retries=2):
    """Fetch Reddit JSON endpoint with retry."""
    headers = {
        "User-Agent": "PrepForge/1.0 (Interview prep aggregator)",
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                print(f"  ⚠️  Reddit fetch failed for {url}: {e}")
                return None


def fetch_subreddit_posts(subreddit, sort="new", limit=25):
    """Fetch posts from a subreddit using public JSON API."""
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
    encoded_q = urllib.request.quote(query)
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
    text = post.get("selftext", "").lower()
    flair = (post.get("flair") or "").lower()

    # Flair check
    if "interview" in flair or "experience" in flair:
        return True

    # Keyword density in title
    exp_keywords = ["interview experience", "got offer", "got hired", "rejected",
                    "interview round", "coding round", "system design round",
                    "onsite interview", "phone screen", "final round",
                    "offer letter", "lpa", "ctc", "compensation"]
    title_hits = sum(1 for kw in exp_keywords if kw in title)
    if title_hits >= 1:
        return True

    # Body keyword density
    body_keywords = ["round 1", "round 2", "coding round", "system design",
                     "behavioral", "hr round", "offer", "rejected",
                     "interviewer asked", "was asked to design"]
    body_hits = sum(1 for kw in body_keywords if kw in text)
    if body_hits >= 2:
        return True

    return False


def extract_company(text):
    """Extract company name from post text."""
    known = [
        "google", "amazon", "microsoft", "meta", "facebook", "apple", "netflix",
        "flipkart", "uber", "adobe", "goldman sachs", "walmart", "oracle",
        "razorpay", "phonepe", "cred", "swiggy", "paytm", "meesho",
        "makemytrip", "juspay", "salesforce", "intuit", "atlassian",
        "stripe", "coinbase", "airbnb", "bytedance", "tiktok",
        "zomato", "ola", "dream11", "groww", "zerodha", "nykaa",
        "infosys", "tcs", "wipro", "thoughtworks", "media.net",
        "dunzo", "lenskart", "springrole", "udaan", "sharechat",
        "myntra", "samsung", "qualcomm", "nvidia", "directi",
    ]
    text_lower = text.lower()
    for company in known:
        if company in text_lower:
            return company.title()

    # Check for "@ Company" or "at Company" patterns
    import re
    match = re.search(r'(?:@|at)\s+([A-Z][a-zA-Z]+)', text)
    if match:
        return match.group(1)

    return "Unknown"


def extract_role(text):
    """Extract role level."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["sde-3", "sde3", "l5", "senior sde", "staff", "e5", "e6"]):
        return "SDE-3"
    if any(w in text_lower for w in ["sde-2", "sde2", "l4", "e4", "sde ii"]):
        return "SDE-2"
    if any(w in text_lower for w in ["sde-1", "sde1", "l3", "e3", "new grad", "fresher"]):
        return "SDE-1"
    return "SDE-2"


def extract_result(text):
    """Extract interview result."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["got offer", "got the offer", "accepted offer", "selected",
                                      "offer letter", "joining"]):
        return "offer"
    if any(w in text_lower for w in ["rejected", "reject", "didn't clear", "didn't make",
                                      "not selected", "ghosted"]):
        return "reject"
    return "unknown"


def scrape(subreddits=None, max_per_sub=25):
    """Main scraper: fetch and normalize Reddit interview experiences."""
    if subreddits is None:
        subreddits = list(SUBREDDITS.keys())

    all_results = []
    seen_ids = set()

    for sub in subreddits:
        config = SUBREDDITS.get(sub, {"search": ["interview experience"]})

        # Method 1: Fetch newest posts
        posts = fetch_subreddit_posts(sub, sort="new", limit=max_per_sub)
        time.sleep(1)  # Rate limiting

        # Method 2: Search for interview-related posts
        for term in config.get("search", [])[:3]:
            search_posts = search_subreddit(sub, term, limit=10)
            posts.extend(search_posts)
            time.sleep(1)

        # Filter and normalize
        for post in posts:
            if post["id"] in seen_ids:
                continue
            seen_ids.add(post["id"])

            if not is_interview_experience(post):
                continue

            combined = post["title"] + " " + post["selftext"]
            exp = {
                "source":         f"reddit_{sub}",
                "source_id":      post["id"],
                "company":        extract_company(combined),
                "role":           extract_role(combined),
                "date_posted":    datetime.fromtimestamp(post["created"]).strftime("%Y-%m-%d") if post["created"] else None,
                "title":          post["title"],
                "body_raw":       post["selftext"][:5000],
                "overall_result": extract_result(combined),
                "url":            post["url"],
                "rounds":         [],  # TODO: parse rounds from body
            }
            all_results.append(exp)

    return all_results
