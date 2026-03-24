"""
Configuration for PrepForge Intelligence Engine.

Setup:
  1. Copy this file: cp intel/config.py intel/config_local.py
  2. Add your API keys to config_local.py
  3. config_local.py is gitignored — never commit secrets
"""

from pathlib import Path
import os

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent.parent
DATA_DIR     = BASE_DIR / "data"
DB_PATH      = DATA_DIR / "interviews.db"
CACHE_DIR    = DATA_DIR / "cache"
LOGS_DIR     = BASE_DIR / "logs"

# Ensure dirs exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# ─── API Keys (set via env vars or config_local.py) ──────────────────────────
ANTHROPIC_API_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
REDDIT_CLIENT_ID   = os.environ.get("REDDIT_CLIENT_ID", "")
REDDIT_SECRET      = os.environ.get("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT  = "PrepForge/1.0 (SDE interview prep bot)"

# ─── Claude API ───────────────────────────────────────────────────────────────
CLAUDE_MODEL        = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-20250514")
CLAUDE_MODEL_FAST   = os.environ.get("CLAUDE_MODEL_FAST", "claude-haiku-4-5-20251001")  # for cheap calls
CLAUDE_MAX_TOKENS   = 4096
CLAUDE_STREAM_TOKENS = 2048

# ─── Your Profile (used by AI coach + gap analysis) ──────────────────────────
PROFILE = {
    "name":       "Jayanti Vishnoi",
    "yoe":        5.5,
    "current":    "Specialist Programmer L2 @ Infosys",
    "project":    "GSTN (Goods and Services Tax Network)",
    "scale":      "14M users, 100K+ concurrent, 300Cr+ invoices",
    "stack":      ["Java", "Spring Boot", "Hibernate", "Golang", "Angular",
                   "Kafka", "Redis", "MySQL", "MongoDB", "HBase",
                   "Docker", "Kubernetes", "AWS"],
    "strengths":  ["Distributed caching (JBoss DataGrid + EhCache)",
                   "Kafka exactly-once with DLQ",
                   "XA transactions (Atomikos JTA)",
                   "Strategy + Factory pattern workflow engine",
                   "HBase + MySQL ledger at 14M user scale"],
    "weak_areas": ["Java DSA (only 4 of 155 in Java)",
                   "Hard LeetCode problems",
                   "LLD practice depth",
                   "FAANG system design framing",
                   "Golang goroutines/channels"],
    "targets":    ["Google L4/L5", "Amazon SDE-2/3", "Microsoft 62-64",
                   "Adobe MTS-2/3", "Flipkart SDE-2/3", "Goldman Sachs VP"],
    "lc_user":    "hasbrovish95",
    "cp_badges":  "CodeChef 4-star, CodeVita Top 1%, Google Code Jam qualifier",
}

# ─── Interview Experience Sources ─────────────────────────────────────────────
SOURCES = {
    "leetcode_discuss": {
        "name":     "LeetCode Discuss",
        "url":      "https://leetcode.com/discuss/interview-experience",
        "api":      "https://leetcode.com/graphql",
        "type":     "graphql",
        "freq":     "daily",
        "priority": 1,  # 1=critical, 2=high, 3=medium
    },
    "reddit_leetcode": {
        "name":     "Reddit r/leetcode",
        "url":      "https://www.reddit.com/r/leetcode",
        "type":     "reddit_api",
        "freq":     "6h",
        "priority": 1,
        "subreddit": "leetcode",
        "search_terms": ["interview experience", "offer", "got the job",
                         "system design", "rejected", "interview questions"],
    },
    "reddit_cscareer": {
        "name":     "Reddit r/cscareerquestions",
        "url":      "https://www.reddit.com/r/cscareerquestions",
        "type":     "reddit_api",
        "freq":     "daily",
        "priority": 2,
        "subreddit": "cscareerquestions",
        "search_terms": ["interview experience", "offer negotiation", "SDE"],
    },
    "reddit_leetcodedesi": {
        "name":     "Reddit LeetcodeDesi",
        "url":      "https://www.reddit.com/r/leetcodedesi",
        "type":     "reddit_api",
        "freq":     "daily",
        "priority": 2,
        "subreddit": "leetcodedesi",
        "search_terms": ["interview", "offer", "India", "LPA"],
    },
    "enginebogie": {
        "name":     "enginebogie.com",
        "url":      "https://enginebogie.com/interview/experiences",
        "type":     "scrape",
        "freq":     "daily",
        "priority": 2,
    },
}

# ─── Target Companies ─────────────────────────────────────────────────────────
TARGET_COMPANIES = {
    "google":       {"level": "L4/L5",    "tc_range": "35-55 LPA",  "tier": 1,
                     "rounds": ["DSA x2", "System Design x1-2", "Behavioral (Googleyness)", "Project Deep Dive"],
                     "focus": "DSA precision + SD depth + Googleyness signals"},
    "amazon":       {"level": "SDE-2/3",  "tc_range": "30-50 LPA",  "tier": 1,
                     "rounds": ["DSA x2", "System Design x1", "LLD x1", "Behavioral (LP) x2", "Bar Raiser"],
                     "focus": "Leadership Principles + Ownership stories + Scale"},
    "microsoft":    {"level": "62-64",    "tc_range": "28-45 LPA",  "tier": 1,
                     "rounds": ["DSA x2-4", "System Design x1", "Behavioral x1"],
                     "focus": "Clean code + Design + Growth mindset"},
    "adobe":        {"level": "MTS-2/3",  "tc_range": "25-40 LPA",  "tier": 1,
                     "rounds": ["DSA x2", "LLD x1", "System Design x1", "Behavioral x1"],
                     "focus": "LLD depth + Java mastery + Design patterns"},
    "flipkart":     {"level": "SDE-2/3",  "tc_range": "30-48 LPA",  "tier": 1,
                     "rounds": ["DSA x2", "Machine Coding x1", "System Design x1", "Behavioral x1"],
                     "focus": "Machine coding round + E-commerce scale design"},
    "goldman_sachs":{"level": "VP",       "tc_range": "35-55 LPA",  "tier": 1,
                     "rounds": ["DSA x2", "System Design x1", "Behavioral x1", "HackerRank OA"],
                     "focus": "Strong DSA + Finance domain knowledge"},
    "razorpay":     {"level": "SDE-2",    "tc_range": "25-35 LPA",  "tier": 2,
                     "rounds": ["DSA x1-2", "System Design x1", "LLD x1", "Cultural Fit"],
                     "focus": "Payment systems + Distributed transactions"},
    "cred":         {"level": "SDE-2",    "tc_range": "28-40 LPA",  "tier": 2,
                     "rounds": ["DSA x1-2", "System Design x1", "LLD x1", "Culture Round"],
                     "focus": "Clean architecture + Product thinking"},
    "phonepe":      {"level": "SDE-2",    "tc_range": "28-42 LPA",  "tier": 1,
                     "rounds": ["DSA x2", "System Design x1", "LLD x1", "Behavioral x1"],
                     "focus": "Payments + Scale + Java depth"},
    "swiggy":       {"level": "SDE-2/3",  "tc_range": "28-45 LPA",  "tier": 1,
                     "rounds": ["DSA x2", "System Design x1", "Machine Coding x1", "Behavioral x1"],
                     "focus": "Real-time systems + Location services + Scale"},
    "paytm":        {"level": "SDE-2",    "tc_range": "22-32 LPA",  "tier": 2,
                     "rounds": ["DSA x2", "System Design x1", "Managerial"],
                     "focus": "Fintech domain + Transaction systems"},
    "meesho":       {"level": "SDE-2",    "tc_range": "25-38 LPA",  "tier": 2,
                     "rounds": ["DSA x2", "System Design x1", "LLD x1", "Culture"],
                     "focus": "E-commerce scale + Social commerce design"},
    "makemytrip":   {"level": "SDE-2",    "tc_range": "22-30 LPA",  "tier": 2,
                     "rounds": ["DSA x1-2", "System Design x1", "Managerial"],
                     "focus": "Booking systems + Search + Availability"},
}

# ─── SDE Level Expectations (used by gap analyzer) ───────────────────────────
LEVEL_EXPECTATIONS = {
    "sde2": {
        "dsa":       {"easy": 90, "medium": 70, "hard": 30,
                      "min_java": 100, "topics": "all NeetCode patterns"},
        "sd":        {"count": 15, "depth": "cover basics well, discuss 2-3 tradeoffs",
                      "capacity_est": "basic", "deep_dive": "1 component"},
        "lld":       {"count": 5, "level": "SOLID + 5 patterns + UML"},
        "behavioral":{"stories": 8, "framework": "STAR", "focus": "ownership + execution"},
        "bar":       "Independent execution, clean code, basic design, clear communication",
    },
    "sde3": {
        "dsa":       {"easy": 95, "medium": 85, "hard": 50,
                      "min_java": 200, "topics": "all patterns + optimization variants"},
        "sd":        {"count": 25, "depth": "deep dives into components, metrics-driven",
                      "capacity_est": "detailed with calculations", "deep_dive": "3+ components"},
        "lld":       {"count": 10, "level": "production-grade, extensibility, testing strategy"},
        "behavioral":{"stories": 15, "framework": "STAR + leadership signals",
                      "focus": "cross-team influence, technical decision-making, mentoring"},
        "bar":       "Drive design decisions, cross-team impact, mentor others, handle ambiguity",
    },
}

# ─── GitHub Repos Index ──────────────────────────────────────────────────────
GITHUB_REPOS = [
    {"name": "system-design-primer",          "author": "donnemartin",   "stars": "270K+", "cat": "SD",   "url": "https://github.com/donnemartin/system-design-primer"},
    {"name": "coding-interview-university",   "author": "jwasham",      "stars": "300K+", "cat": "Full", "url": "https://github.com/jwasham/coding-interview-university"},
    {"name": "tech-interview-handbook",       "author": "yangshun",     "stars": "120K+", "cat": "Full", "url": "https://github.com/yangshun/tech-interview-handbook"},
    {"name": "awesome-system-design-resources","author": "ashishps1",   "stars": "20K+",  "cat": "SD",   "url": "https://github.com/ashishps1/awesome-system-design-resources"},
    {"name": "awesome-scalability",           "author": "binhnguyennus","stars": "55K+",  "cat": "SD",   "url": "https://github.com/binhnguyennus/awesome-scalability"},
    {"name": "system-design-resources",       "author": "InterviewReady","stars": "15K+", "cat": "SD",   "url": "https://github.com/InterviewReady/system-design-resources"},
    {"name": "System-Design-Interview-Questions","author": "sid24rane", "stars": "3K+",   "cat": "SD",   "url": "https://github.com/sid24rane/System-Design-Interview-Questions"},
    {"name": "awesome-low-level-design",      "author": "ashishps1",   "stars": "10K+",  "cat": "LLD",  "url": "https://github.com/ashishps1/awesome-low-level-design"},
    {"name": "interviews",                    "author": "kdn251",      "stars": "63K+",  "cat": "DSA",  "url": "https://github.com/kdn251/interviews"},
    {"name": "SDE-Interview-Materials",       "author": "bhartik021",  "stars": "2K+",   "cat": "Full", "url": "https://github.com/bhartik021/SDE-Interview-Materials"},
]
