"""
Document Knowledge Base — lightweight RAG for AI Coach.

Indexes markdown/text files from Interview_Answers/ and docs/ into SQLite.
Retrieval is keyword-based (no vectors needed for this size corpus).

Flow:
  init_kb()          → index all doc files → stored in kb_chunks table
  search_kb(query)   → keyword match → returns top-N relevant chunks
  get_coach_context(query, context_type) → assembled system context string

Indexed documents (all markdown):
  Interview_Answers/  — 23 files: Java, Spring, Microservices, SD, LLD, GSTN, STAR, company Qs
  docs/               — Question bank, company analysis, interview patterns, war plan
  docs/Interview_exp.txt — real interview experiences

PDFs/Excel/DOCX are skipped (need extra libs — convert to markdown manually to include).
"""

import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Optional

BASE = Path(__file__).parent.parent
DB_PATH = BASE / "data" / "interviews.db"

# Files to index — ordered by priority (most useful first)
KNOWLEDGE_SOURCES = [
    # ─── High Priority: Direct Interview Content ───────────────────────────────
    ("Interview_Answers", "Amazon_LP_STAR_Bank.md",          "behavioral",      "amazon_lp"),
    ("Interview_Answers", "Section_01_Java_Core.md",          "java",            "java_core"),
    ("Interview_Answers", "Section_02_Spring_Boot.md",        "java",            "spring_boot"),
    ("Interview_Answers", "Section_04_05_06_Microservices_Kafka_Redis.md", "java", "microservices"),
    ("Interview_Answers", "Section_07_08_Database_DistributedSystems.md", "system_design", "databases"),
    ("Interview_Answers", "Section_21_SystemDesign_DeepDive_With_Answers.md", "system_design", "sd_deep"),
    ("Interview_Answers", "GSTN_Architecture_Reference.md",   "system_design",   "gstn_arch"),
    ("Interview_Answers", "GSTN_Complete_SDE2_SDE3_InterviewPrep.md", "general", "gstn_prep"),
    ("Interview_Answers", "Company_Questions_Phase1.md",      "general",         "company_q1"),
    ("Interview_Answers", "Company_Questions_Phase2.md",      "general",         "company_q2"),
    ("Interview_Answers", "Section_20_FAANG_SDE2_SDE3_Advanced.md", "general",  "faang_adv"),
    ("Interview_Answers", "Section_LLD_Complete.md",          "lld",             "lld_complete"),
    ("Interview_Answers", "Section_DSA_Java_Patterns.md",     "dsa",             "dsa_patterns"),
    ("Interview_Answers", "Section_Modern_Java_Observability_CQRS.md", "java",   "modern_java"),
    ("Interview_Answers", "Section_Behavioral_DB_Golang.md",  "behavioral",      "behavioral_go"),
    ("Interview_Answers", "Section_SD_Consumer_Products.md",  "system_design",   "sd_consumer"),
    ("Interview_Answers", "OA_Patterns_MockInterviews_RevisionGuide.md", "dsa",  "oa_patterns"),
    # ─── Medium Priority: Reference Docs ─────────────────────────────────────
    ("docs",              "GSTN_Interview_QuestionBank_296Q.md", "general",      "qbank_296"),
    ("docs",              "COMPANY_ANALYSIS.md",                "general",       "company_analysis"),
    ("docs",              "DEEP_RESEARCH_INTERVIEW_PATTERNS_2025_2026.md", "general", "patterns_2026"),
    ("docs",              "CPP_to_Java_DSA_CheatSheet.md",      "dsa",           "dsa_cheat"),
    ("docs",              "Interview_exp.txt",                   "general",       "real_experiences"),
    ("docs",              "MASTER_16H_WARPLAN.md",               "general",       "war_plan"),
]

CHUNK_SIZE = 1200       # chars per chunk (≈300 tokens)
CHUNK_OVERLAP = 150     # overlap chars between chunks


# ─── DB helpers ───────────────────────────────────────────────────────────────

def _conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _init_table(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS kb_chunks (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        source_key  TEXT NOT NULL,          -- e.g. "java_core"
        source_file TEXT NOT NULL,          -- relative path
        category    TEXT,                   -- java, dsa, system_design, lld, behavioral, general
        chunk_idx   INTEGER,
        chunk_hash  TEXT,                   -- sha1 of content for dedup
        heading     TEXT,                   -- nearest ## heading above chunk
        content     TEXT NOT NULL,
        keywords    TEXT                    -- space-separated extracted keywords
    );
    CREATE INDEX IF NOT EXISTS idx_kb_category ON kb_chunks(category);
    CREATE INDEX IF NOT EXISTS idx_kb_source    ON kb_chunks(source_key);
    """)


# ─── Indexing ─────────────────────────────────────────────────────────────────

def _extract_keywords(text: str) -> str:
    """Extract important keywords from a chunk for fast keyword search.
    Enhanced with domain-specific term boosting and bigrams.
    """
    # Remove markdown symbols
    clean = re.sub(r"[#*`_\[\]()>|]", " ", text)
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", clean)  # min 3 chars (was 4)
    # Count frequency
    freq = {}
    for w in words:
        w = w.lower()
        freq[w] = freq.get(w, 0) + 1
    # Top 50 words by frequency, excluding stopwords
    stops = {"that","this","with","from","have","will","been","they","were","your",
             "when","what","which","more","some","such","than","then","also","into",
             "only","each","both","over","here","time","very","well","just","like",
             "make","need","used","using","code","data","type","value","class","object",
             "interface","return","method","function","public","private","static","void","string","list","array",
             "example","answer","follow","question","explain","would","should","could"}

    # Domain-specific high-value terms (boost weight)
    DOMAIN_BOOST = {
        "kafka","redis","spring","hibernate","jpa","gstn","microservices","kubernetes",
        "docker","concurrenthashmap","hashmap","treemap","volatile","synchronized",
        "threadlocal","completablefuture","transactional","cacheable","profiles","actuator",
        "logback","slf4j","reactor","webflux","circuit","breaker","saga","cqrs","avro",
        "goroutine","channels","golang","hbase","elasticsearch","raft","paxos","sharding",
        "replication","idempotent","idempotency","deadlock","threadpool","executor",
        "immutable","singleton","strategy","factory","observer","decorator","builder",
        "lru","treeify","loadfactor","garbagecollection","younggen","oldgen","metaspace",
        "jit","bytecode","classloader","serialization","reflection","generics","erasure",
        "stream","optional","records","sealed","virtual","bedrock","genai","llm",
        "star","behavioral","leadership","ownership","customer","obsession",
        "dlq","backoff","retry","partition","offset","consumer","producer","broker",
        "index","btree","lsm","wal","mvcc","isolation","acid","atomikos",
        "rate","limiter","token","bucket","sliding","window","caffeine","ehcache",
        "gstin","filing","taxpayer","validation","notification","ledger","audit",
        "binary","search","heap","stack","queue","tree","graph","dynamic","programming",
        "greedy","backtracking","recursion","memoization","tabulation"
    }

    ranked = []
    for w, c in freq.items():
        if w in stops or len(w) < 3:
            continue
        score = c
        if w in DOMAIN_BOOST:
            score *= 3  # boost domain terms
        ranked.append((w, score))

    ranked.sort(key=lambda x: -x[1])

    # Also extract important bigrams (e.g., "spring boot", "rate limiter")
    lowered = clean.lower()
    IMPORTANT_BIGRAMS = [
        "spring boot","spring security","spring profiles","spring actuator",
        "kafka consumer","kafka producer","dead letter","rate limiter","token bucket",
        "sliding window","circuit breaker","thread pool","connection pool","thread safety",
        "garbage collection","memory leak","heap dump","cache stampede","cache aside",
        "event sourcing","eventual consistency","strong consistency","distributed transaction",
        "system design","binary search","dynamic programming","two pointers","monotonic stack",
        "union find","topological sort","load balancer","api gateway","service discovery",
        "read replica","write ahead","log replication","virtual threads","pattern matching",
        "functional interface","concurrent hashmap","completable future",
        "star story","behavioral question","leadership principle",
        "gstn architecture","filing service","notification service"
    ]
    bigram_hits = [bg.replace(" ", "_") for bg in IMPORTANT_BIGRAMS if bg in lowered]

    return " ".join([w for w, _ in ranked[:50]] + bigram_hits)


def _chunk_text(text: str) -> list[tuple[int, str, str]]:
    """
    Split text into overlapping chunks.
    Returns list of (chunk_idx, heading, chunk_text).
    """
    chunks = []
    current_heading = ""
    pos = 0
    idx = 0

    while pos < len(text):
        chunk = text[pos:pos + CHUNK_SIZE]
        # Find nearest heading before this position
        heading_matches = list(re.finditer(r"^#{1,3} .+$", text[:pos + CHUNK_SIZE], re.MULTILINE))
        if heading_matches:
            current_heading = heading_matches[-1].group(0).strip("# ").strip()

        chunks.append((idx, current_heading, chunk))
        idx += 1
        pos += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def _file_hash(content: str) -> str:
    return hashlib.sha1(content.encode("utf-8", errors="replace")).hexdigest()[:12]


def _index_file(conn, folder: str, filename: str, category: str, source_key: str) -> int:
    """Index one file into kb_chunks. Returns number of chunks added."""
    path = BASE / folder / filename
    if not path.exists():
        return 0

    content = path.read_text(encoding="utf-8", errors="replace")
    if len(content) < 100:
        return 0

    source_file = f"{folder}/{filename}"
    file_h = _file_hash(content)

    # Check if already indexed with same content
    existing = conn.execute(
        "SELECT COUNT(*) FROM kb_chunks WHERE source_key=? AND chunk_hash=?",
        (source_key, file_h)
    ).fetchone()[0]
    if existing > 0:
        return 0  # already up to date

    # Delete old chunks for this source
    conn.execute("DELETE FROM kb_chunks WHERE source_key=?", (source_key,))

    chunks = _chunk_text(content)
    added = 0
    for idx, heading, chunk_text in chunks:
        if len(chunk_text.strip()) < 50:
            continue
        keywords = _extract_keywords(chunk_text)
        conn.execute(
            """INSERT INTO kb_chunks
                 (source_key, source_file, category, chunk_idx, chunk_hash, heading, content, keywords)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (source_key, source_file, category, idx, file_h, heading, chunk_text, keywords)
        )
        added += 1

    conn.commit()
    return added


def init_kb(force: bool = False) -> dict:
    """
    Index all knowledge sources into SQLite.
    Skips files already indexed (hash-based dedup).
    Returns stats.
    """
    with _conn() as conn:
        _init_table(conn)

        if force:
            conn.execute("DELETE FROM kb_chunks")
            conn.commit()

        stats = {"indexed": 0, "skipped": 0, "missing": 0, "total_chunks": 0}
        for folder, filename, category, source_key in KNOWLEDGE_SOURCES:
            path = BASE / folder / filename
            if not path.exists():
                stats["missing"] += 1
                continue
            added = _index_file(conn, folder, filename, category, source_key)
            if added > 0:
                stats["indexed"] += 1
                stats["total_chunks"] += added
            else:
                stats["skipped"] += 1

        total = conn.execute("SELECT COUNT(*) FROM kb_chunks").fetchone()[0]
        stats["total_chunks_in_db"] = total
        return stats


# ─── Retrieval ────────────────────────────────────────────────────────────────

def search_kb(query: str,
              category: Optional[str] = None,
              source_key: Optional[str] = None,
              limit: int = 6) -> list[dict]:
    """
    Keyword-based search over kb_chunks.
    Scores each chunk by how many query words appear in keywords + content.
    Enhanced with bigram matching and heading boost.
    """
    if not query:
        return []

    # Normalize query → search terms
    query_lower = query.lower()
    query_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", query_lower))
    stops = {"the","and","for","that","this","with","from","have","will","been","what","when",
             "how","can","are","not","its","use","get","set","run","explain","describe","tell"}
    query_words -= stops
    if not query_words:
        return []

    # Generate bigram search terms from query
    query_bigrams = set()
    qwords_list = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", query_lower)
    for i in range(len(qwords_list) - 1):
        bigram = f"{qwords_list[i]}_{qwords_list[i+1]}"
        query_bigrams.add(bigram)

    with _conn() as conn:
        # First check table exists
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='kb_chunks'"
        ).fetchone()
        if not exists:
            return []

        conditions = []
        params = []
        if category:
            conditions.append("category = ?")
            params.append(category)
        if source_key:
            conditions.append("source_key = ?")
            params.append(source_key)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        rows = conn.execute(
            f"SELECT id, source_key, source_file, category, heading, content, keywords FROM kb_chunks {where}",
            params
        ).fetchall()

        # Score rows
        scored = []
        for row in rows:
            kw_text = (row["keywords"] or "").lower()
            content_lower = row["content"].lower()
            heading_lower = (row["heading"] or "").lower()
            score = 0
            for w in query_words:
                if w in kw_text:
                    score += 3  # keyword match = strong signal
                if w in content_lower:
                    score += 1  # content match = weaker
                if w in heading_lower:
                    score += 5  # heading match = strongest signal
            # Bigram matching (e.g., "spring_boot" in keywords)
            for bg in query_bigrams:
                if bg in kw_text:
                    score += 6  # bigram in keywords = very strong
            if score > 0:
                scored.append((score, row))

        scored.sort(key=lambda x: -x[0])
        out = []
        seen_keys = set()
        for score, row in scored[:limit * 2]:
            # Deduplicate consecutive chunks from same source
            dedup_key = (row["source_key"], row["heading"])
            if dedup_key in seen_keys:
                continue
            seen_keys.add(dedup_key)
            out.append({
                "source": row["source_file"],
                "category": row["category"],
                "heading": row["heading"],
                "content": row["content"],
                "score": score,
            })
            if len(out) >= limit:
                break
        return out


def get_coach_context(query: str,
                      context_type: str = "general",
                      company: Optional[str] = None,
                      max_chars: int = 6000) -> str:
    """
    Build a context string for the AI coach system prompt.
    Searches KB with query + category hint, returns formatted excerpts.
    """
    # Map context_type to category hint
    cat_map = {
        "jd": None,           # search all
        "answer_eval": None,
        "star": "behavioral",
        "behavioral": "behavioral",
        "dsa": "dsa",
        "lld": "lld",
        "system_design": "system_design",
        "mock": None,
        "general": None,
    }
    category = cat_map.get(context_type)

    # Build search query from user query + company
    search_query = query
    if company:
        search_query += f" {company}"

    chunks = search_kb(search_query, category=category, limit=6)
    if not chunks:
        return ""

    # For STAR/behavioral, always include Amazon LP bank
    if context_type in ("star", "behavioral") and not any(c["source"].endswith("Amazon_LP_STAR_Bank.md") for c in chunks):
        lp_chunks = search_kb("STAR story leadership principle", source_key="amazon_lp", limit=2)
        chunks = (lp_chunks + chunks)[:6]

    # For company-specific queries, add company analysis
    if company:
        co_chunks = search_kb(company, source_key="company_analysis", limit=2)
        co_chunks += search_kb(company, source_key="company_q1", limit=2)
        co_chunks += search_kb(company, source_key="company_q2", limit=2)
        chunks = (co_chunks + chunks)[:7]

    lines = ["\n\n--- KNOWLEDGE BASE CONTEXT (from your prep documents) ---"]
    total = 0
    for c in chunks:
        header = f"\n[{c['source']} | {c['heading']}]"
        body = c["content"].strip()
        needed = len(header) + len(body) + 2
        if total + needed > max_chars:
            break
        lines.append(header)
        lines.append(body)
        total += needed

    lines.append("--- END OF KNOWLEDGE BASE CONTEXT ---\n")
    return "\n".join(lines)


def get_kb_stats() -> dict:
    """Return stats about the knowledge base."""
    try:
        with _conn() as conn:
            exists = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='kb_chunks'"
            ).fetchone()
            if not exists:
                return {"total": 0, "by_category": {}, "by_source": {}}

            total = conn.execute("SELECT COUNT(*) FROM kb_chunks").fetchone()[0]
            by_cat = {r[0]: r[1] for r in conn.execute(
                "SELECT category, COUNT(*) FROM kb_chunks GROUP BY category"
            ).fetchall()}
            by_src = {r[0]: r[1] for r in conn.execute(
                "SELECT source_key, COUNT(*) FROM kb_chunks GROUP BY source_key ORDER BY COUNT(*) DESC LIMIT 20"
            ).fetchall()}
            return {"total": total, "by_category": by_cat, "by_source": by_src}
    except Exception:
        return {"total": 0, "by_category": {}, "by_source": {}}


if __name__ == "__main__":
    import sys
    if "--init" in sys.argv:
        force = "--force" in sys.argv
        print(f"Indexing knowledge base (force={force})...")
        stats = init_kb(force=force)
        print(f"Done: {stats}")
    elif "--search" in sys.argv:
        idx = sys.argv.index("--search")
        q = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "kafka consumer"
        results = search_kb(q, limit=3)
        for r in results:
            print(f"\n[{r['source']} | {r['heading']}] score={r['score']}")
            print(r["content"][:300])
    elif "--stats" in sys.argv:
        stats = get_kb_stats()
        print(json.dumps(stats, indent=2))
    else:
        print("Usage: python -m intel.knowledge_base --init [--force] | --search <query> | --stats")
