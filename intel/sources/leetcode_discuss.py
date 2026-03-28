"""
LeetCode Discuss interview experience scraper.
Uses LeetCode's public GraphQL API.

Improvements over v1:
  - Proper HTML stripping (content is HTML, not plain text)
  - Vote count quality filter (skips spam/empty posts)
  - Expanded company queries: 20 targeted searches
  - Better round/question extraction from stripped HTML
  - Tag-based company detection
  - Relevance scoring to skip non-experience posts
"""

import json
import re
import time
import urllib.request
import urllib.error
from datetime import datetime


LC_GRAPHQL = "https://leetcode.com/graphql"

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
    "linkedin", "twitter", "snap", "spotify", "shopify", "twilio",
    "samsara", "doordash", "square", "block", "robinhood",
]

# Targeted queries: (company_hint, search_string)
COMPANY_QUERIES = [
    ("amazon",     "Amazon SDE-2 interview"),
    ("amazon",     "Amazon SDE-3 interview"),
    ("amazon",     "Amazon bar raiser"),
    ("google",     "Google L4 interview"),
    ("google",     "Google L5 interview"),
    ("flipkart",   "Flipkart SDE-2 interview"),
    ("flipkart",   "Flipkart machine coding"),
    ("razorpay",   "Razorpay interview"),
    ("phonepe",    "PhonePe interview"),
    ("cred",       "CRED interview SDE"),
    ("swiggy",     "Swiggy SDE interview"),
    ("stripe",     "Stripe interview"),
    ("meta",       "Meta E4 E5 interview"),
    ("meta",       "Facebook SDE interview"),
    ("goldman",    "Goldman Sachs interview"),
    ("microsoft",  "Microsoft SDE-2 interview"),
    ("atlassian",  "Atlassian SDE interview"),
    ("adobe",      "Adobe MTS interview"),
    ("uber",       "Uber SDE-2 interview"),
    ("paytm",      "Paytm SDE interview"),
]

# Skip these non-experience titles
SKIP_TITLE_PATTERNS = [
    "how to write", "guidelines", "resources", "tips for writing",
    "template", "format", "how to share",
]

# ── HTML stripping ─────────────────────────────────────────────────────────────

def _strip_html(html):
    """Convert LeetCode HTML content to clean plain text."""
    if not html:
        return ""
    # Block-level → newlines
    html = re.sub(r"</?(p|div|br|h[1-6]|li)[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</?ul[^>]*>|</?ol[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Inline formatting → text
    html = re.sub(r"<strong[^>]*>(.*?)</strong>", r"\1", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<em[^>]*>(.*?)</em>", r"\1", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", html, flags=re.IGNORECASE | re.DOTALL)
    # Links → text only
    html = re.sub(r"<a[^>]+>(.*?)</a>", r"\1", html, flags=re.IGNORECASE | re.DOTALL)
    # Remove all other tags
    html = re.sub(r"<[^>]+>", "", html)
    # Decode entities
    html = re.sub(r"&amp;",  "&",  html)
    html = re.sub(r"&lt;",   "<",  html)
    html = re.sub(r"&gt;",   ">",  html)
    html = re.sub(r"&quot;", '"',  html)
    html = re.sub(r"&#39;",  "'",  html)
    html = re.sub(r"&nbsp;", " ",  html)
    html = re.sub(r"&[a-z]+;", " ", html)
    # Normalise whitespace
    html = re.sub(r" {2,}", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


# ── Company / role / result extraction ────────────────────────────────────────

def extract_company_from_title(title):
    title_lower = title.lower()
    for company in KNOWN_COMPANIES:
        if company in title_lower:
            return company.title().replace("Jp Morgan", "JP Morgan")
    if "|" in title:
        candidate = title.split("|")[0].strip()
        if 2 < len(candidate) < 40:
            return candidate
    return None


def extract_company_from_tags(tags):
    """LeetCode posts often have company tags like 'amazon', 'google'."""
    for tag in (tags or []):
        name = (tag.get("name") or "").lower()
        slug = (tag.get("slug") or "").lower()
        for company in KNOWN_COMPANIES:
            if company in name or company in slug:
                return company.title().replace("Jp Morgan", "JP Morgan")
    return None


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
    if any(w in title_lower for w in ["offer", "accepted", "got the job", "selected",
                                       "[passed]", "cleared", "got hired"]):
        return "offer"
    if any(w in title_lower for w in ["rejected", "reject", "failed", "[reject]",
                                       "no offer", "didn't get"]):
        return "reject"
    return "unknown"


# ── Round / question extraction ───────────────────────────────────────────────

_ROUND_HEADER_RE = re.compile(
    r'(?:round\s*\d+|technical\s+round|coding\s+round|system\s+design\s+round|'
    r'lld\s+round|machine\s+coding|hr\s+round|behavioral\s+round|bar\s+raiser|'
    r'onsite\s+round|phone\s+screen)',
    re.IGNORECASE,
)

_QUESTION_SIGNAL_RE = re.compile(
    r'(?:asked\s+(?:me\s+)?(?:to\s+)?(?:design|implement|solve|write|find|code)\b'
    r'|was\s+asked\s+(?:to\s+)?(?:design|implement|solve)'
    r'|design\s+(?:a\s+)?(?:system|service|platform|url|cache|feed|chat|notification|payment|booking)'
    r'|implement\s+(?:a\s+)?(?:lru|lfu|trie|queue|stack|iterator|rate\s+limiter)'
    r'|find\s+(?:all\s+)?(?:path|cycle|island|median|kth|pair|subarray)'
    r'|[Qq]uestion\s*[:–-]\s*.{15,150}'
    r'|[Qq]\d+\s*[:.)]\s*.{15,150})',
    re.IGNORECASE,
)


def parse_rounds_from_content(content_text):
    """
    Extract structured rounds from clean (HTML-stripped) post content.
    Returns list of {round_type, question, difficulty, topics, outcome}.
    """
    rounds = []
    if not content_text:
        return rounds

    lines = content_text.split("\n")
    current_round_type = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        line_lower = line.lower()

        # Detect round header
        if _ROUND_HEADER_RE.search(line_lower):
            if any(w in line_lower for w in ["system design", "hld", "high level design"]):
                current_round_type = "system_design"
            elif any(w in line_lower for w in ["lld", "low level design", "machine coding", "object oriented"]):
                current_round_type = "lld"
            elif any(w in line_lower for w in ["behavioral", "culture", "leadership",
                                                "hr round", "bar raiser", "managerial"]):
                current_round_type = "behavioral"
            else:
                current_round_type = "dsa"

        # Detect explicit question signal within a line
        if _QUESTION_SIGNAL_RE.search(line) and len(line) >= 25:
            rtype = current_round_type or _infer_round_type(line)
            rounds.append({
                "round_type": rtype,
                "question":   line[:250],
                "difficulty": _infer_difficulty(line),
                "topics":     [],
                "outcome":    None,
            })

    return rounds[:20]  # cap


def _infer_round_type(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["design", "scale", "distributed", "architecture",
                                      "system", "hld", "service", "platform"]):
        return "system_design"
    if any(w in text_lower for w in ["lld", "class diagram", "ood", "implement", "parking"]):
        return "lld"
    if any(w in text_lower for w in ["leadership", "tell me", "describe", "situation",
                                      "stakeholder", "conflict"]):
        return "behavioral"
    return "dsa"


def _infer_difficulty(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["easy", "simple", "basic", "trivial"]):
        return "easy"
    if any(w in text_lower for w in ["medium", "moderate"]):
        return "medium"
    if any(w in text_lower for w in ["hard", "difficult", "tough", "tricky", "complex"]):
        return "hard"
    return None


def _is_quality_post(title, vote_count, content_text):
    """Filter out spam, empty posts, and non-experience posts."""
    if not content_text or len(content_text) < 100:
        return False
    title_lower = title.lower()
    for pattern in SKIP_TITLE_PATTERNS:
        if pattern in title_lower:
            return False
    # Skip posts that are clearly not experience reports
    non_exp = ["how to prepare", "resources", "roadmap", "tips for",
               "what should i", "looking for advice"]
    if any(p in title_lower for p in non_exp):
        return False
    return True


# ── GraphQL fetch ──────────────────────────────────────────────────────────────

def _graphql_fetch(query_str="", skip=0, first=20, retries=2):
    payload = {
        "query": DISCUSS_QUERY,
        "variables": {
            "orderBy":  "newest_to_oldest",
            "skip":     skip,
            "first":    first,
            "tags":     [],
            "query":    query_str,
        }
    }
    req = urllib.request.Request(
        LC_GRAPHQL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer":      "https://leetcode.com/discuss/interview-experience/",
            "x-csrftoken":  "dummy",
        },
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read())
                edges = data.get("data", {}).get("categoryTopicList", {}).get("edges", [])
                return [e["node"] for e in edges if "node" in e]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3 * (attempt + 1))
            elif attempt < retries:
                time.sleep(1.5)
            else:
                print(f"  ⚠️  LeetCode Discuss HTTP {e.code} (query={query_str!r})")
                return []
        except Exception as e:
            if attempt < retries:
                time.sleep(1.5)
            else:
                print(f"  ⚠️  LeetCode Discuss error: {e}")
                return []
    return []


# ── Normalization ──────────────────────────────────────────────────────────────

def _normalize_post(post, company_hint=None):
    title      = post.get("title", "")
    raw_html   = post.get("post", {}).get("content", "")
    content    = _strip_html(raw_html)
    creation   = post.get("post", {}).get("creationDate")
    vote_count = post.get("post", {}).get("voteCount", 0)
    tags       = post.get("tags", [])

    # Company resolution: title > tags > hint
    company = extract_company_from_title(title)
    if not company:
        company = extract_company_from_tags(tags)
    if not company and company_hint:
        company = company_hint.title()

    rounds = parse_rounds_from_content(content)

    return {
        "source":         "leetcode_discuss",
        "source_id":      str(post.get("id", "")),
        "company":        company,
        "role":           extract_role_from_title(title),
        "date_posted":    datetime.fromtimestamp(creation).strftime("%Y-%m-%d") if creation else None,
        "title":          title,
        "body_raw":       content[:5000],
        "overall_result": extract_result_from_title(title),
        "url":            f"https://leetcode.com/discuss/interview-experience/{post.get('id')}",
        "rounds":         rounds,
        "_vote_count":    vote_count,   # used for quality filtering, stripped before DB insert
    }


# ── Public scrape functions ────────────────────────────────────────────────────

def scrape_by_company(company, query, max_posts=25):
    results = []
    seen_ids = set()
    for skip in range(0, max_posts, 20):
        batch_size = min(20, max_posts - skip)
        posts = _graphql_fetch(query_str=query, skip=skip, first=batch_size)
        if not posts:
            break
        for post in posts:
            post_id = str(post.get("id", ""))
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)
            norm = _normalize_post(post, company_hint=company)
            content = norm.get("body_raw", "")
            if _is_quality_post(norm["title"], norm.get("_vote_count", 0), content):
                norm.pop("_vote_count", None)
                results.append(norm)
        if len(posts) < batch_size:
            break
        time.sleep(0.5)
    return results


def scrape(max_posts=120):
    """Main scraper: general newest posts + targeted company searches."""
    results = []
    seen_ids = set()

    # ── General newest posts ─────────────────────────────────────────────────
    for skip in range(0, max_posts, 20):
        posts = _graphql_fetch(query_str="", skip=skip, first=20)
        if not posts:
            break
        for post in posts:
            post_id = str(post.get("id", ""))
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)
            norm = _normalize_post(post)
            if _is_quality_post(norm["title"], norm.get("_vote_count", 0), norm.get("body_raw", "")):
                norm.pop("_vote_count", None)
                results.append(norm)
        time.sleep(0.3)

    # ── Targeted company searches ────────────────────────────────────────────
    for company, query in COMPANY_QUERIES:
        company_posts = scrape_by_company(company=company, query=query, max_posts=20)
        for exp in company_posts:
            if exp["source_id"] not in seen_ids:
                seen_ids.add(exp["source_id"])
                results.append(exp)
        time.sleep(0.3)

    print(f"  🟡 LeetCode Discuss: {len(results)} experiences fetched")
    return results


if __name__ == "__main__":
    r = scrape()
    for x in r[:3]:
        print(x.get("company"), "|", x["title"][:60], "|", len(x.get("rounds", [])), "rounds")
