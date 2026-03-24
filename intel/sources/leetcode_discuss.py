"""
LeetCode Discuss interview experience scraper.
Uses LeetCode's public GraphQL API — updated for 2025 API format.
"""

import json
import urllib.request
import urllib.error
import re
from datetime import datetime


LC_GRAPHQL = "https://leetcode.com/graphql"

# Updated query using 'edges' format (LeetCode API changed in 2024)
DISCUSS_QUERY = """
query categoryTopicList($orderBy: TopicSortingOption, $skip: Int, $first: Int, $query: String, $tags: [String!]) {
  categoryTopicList(
    orderBy: $orderBy
    skip: $skip
    first: $first
    query: $query
    tags: $tags
    categories: ["interview-experience"]
  ) {
    totalNum
    edges {
      node {
        id
        title
        post {
          id
          content
          creationDate
          voteCount
        }
        viewCount
        tags {
          name
          slug
        }
      }
    }
  }
}
"""

KNOWN_COMPANIES = [
    "google", "amazon", "microsoft", "meta", "facebook", "apple", "netflix",
    "flipkart", "uber", "adobe", "goldman sachs", "walmart", "oracle",
    "razorpay", "phonepe", "cred", "swiggy", "paytm", "meesho",
    "makemytrip", "juspay", "salesforce", "intuit", "atlassian",
    "stripe", "coinbase", "airbnb", "bytedance", "tiktok",
    "infosys", "tcs", "wipro", "thoughtworks", "medianet",
    "zomato", "ola", "dream11", "groww", "zerodha", "nykaa",
    "jp morgan", "jpmorgan", "morgan stanley", "deutsche bank",
    "dunzo", "lenskart", "udaan", "sharechat", "myntra",
    "samsung", "qualcomm", "nvidia", "directi", "media.net",
]


def fetch_discuss_posts(skip=0, first=20):
    """Fetch interview experience posts from LeetCode Discuss."""
    payload = {
        "query": DISCUSS_QUERY,
        "variables": {
            "orderBy": "newest_to_oldest",
            "skip": skip,
            "first": first,
            "tags": [],
            "query": "",
        }
    }

    req = urllib.request.Request(
        LC_GRAPHQL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://leetcode.com/discuss/interview-experience/",
            "x-csrftoken": "dummy",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
            edges = data.get("data", {}).get("categoryTopicList", {}).get("edges", [])
            return [e["node"] for e in edges if "node" in e]
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        print(f"  ⚠️  LeetCode Discuss fetch error: {e}")
        return []


def extract_company_from_title(title):
    title_lower = title.lower()
    for company in KNOWN_COMPANIES:
        if company in title_lower:
            return company.title().replace("Jp Morgan", "JP Morgan")
    if "|" in title:
        return title.split("|")[0].strip()
    return "Unknown"


def extract_role_from_title(title):
    title_lower = title.lower()
    for pattern in ["sde-3", "sde3", "l5", "senior", "staff", "e5", "e6", "sde 3", "mts-3"]:
        if pattern in title_lower:
            return "SDE-3"
    for pattern in ["sde-2", "sde2", "l4", "e4", "sde ii", "sde 2", "mts-2"]:
        if pattern in title_lower:
            return "SDE-2"
    for pattern in ["sde-1", "sde1", "l3", "e3", "junior", "new grad", "entry", "fresher"]:
        if pattern in title_lower:
            return "SDE-1"
    return "SDE-2"


def extract_result_from_title(title):
    title_lower = title.lower()
    if any(w in title_lower for w in ["offer", "accepted", "got the job", "selected", "[passed]"]):
        return "offer"
    if any(w in title_lower for w in ["rejected", "reject", "failed", "[reject]", "no offer"]):
        return "reject"
    return "unknown"


def parse_post_for_rounds(content):
    rounds = []
    if not content:
        return rounds
    lines = content.split("\n")
    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower:
            continue
        round_type = None
        if any(w in line_lower for w in ["system design", "hld", "high level design"]):
            round_type = "system_design"
        elif any(w in line_lower for w in ["lld", "low level design", "machine coding", "object oriented"]):
            round_type = "lld"
        elif any(w in line_lower for w in ["behavioral", "culture", "leadership", "hr round", "bar raiser", "managerial"]):
            round_type = "behavioral"
        elif any(w in line_lower for w in ["coding round", "dsa", "algorithm", "data structure", "leetcode"]):
            round_type = "dsa"
        if round_type:
            rounds.append({
                "round_type": round_type,
                "question": line.strip()[:200],
                "topics": [],
                "difficulty": None,
                "outcome": None,
            })
    return rounds


def scrape(max_posts=50):
    """Main scraper: fetch and normalize LeetCode Discuss experiences."""
    results = []
    for skip in range(0, max_posts, 20):
        posts = fetch_discuss_posts(skip=skip, first=20)
        if not posts:
            break
        for post in posts:
            title = post.get("title", "")
            content = post.get("post", {}).get("content", "")
            creation = post.get("post", {}).get("creationDate")

            # Skip pinned/meta posts
            if "how to write" in title.lower() or "guidelines" in title.lower():
                continue

            exp = {
                "source":         "leetcode_discuss",
                "source_id":      str(post.get("id", "")),
                "company":        extract_company_from_title(title),
                "role":           extract_role_from_title(title),
                "date_posted":    datetime.fromtimestamp(creation).strftime("%Y-%m-%d") if creation else None,
                "title":          title,
                "body_raw":       content[:5000] if content else "",
                "overall_result": extract_result_from_title(title),
                "url":            f"https://leetcode.com/discuss/interview-experience/{post.get('id')}",
                "rounds":         parse_post_for_rounds(content),
            }
            results.append(exp)
    return results
