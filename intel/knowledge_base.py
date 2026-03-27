"""
Document Knowledge Base — lightweight RAG for AI Coach.

Indexes markdown, PDF, DOCX, and XLSX files into SQLite.
Retrieval is keyword-based (no vectors needed for this size corpus).

Flow:
  init_kb()          → index all doc files → stored in kb_chunks table
  search_kb(query)   → keyword match → returns top-N relevant chunks
  get_coach_context(query, context_type) → assembled system context string

Indexed documents:
  Interview_Answers/  — 23 markdown files: Java, Spring, Microservices, SD, LLD, GSTN, STAR, company Qs
  docs/               — Question bank, company analysis, interview patterns, war plan
  docs/books/         — Alex Xu SD Vol1 + Vol2, Spring PDF, Java/Spring DOCX guide
  trackers-docs/      — Java, SD, LLD, DB/OS/CN interview sheets (XLSX), prep programmes (DOCX)
  02_Resumes/files/   — Supplementary prep guides (DOCX)
  01_Career_Interview_Prep/ — interview master sheet, SDE2 analysis (DOCX)
"""

import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Optional

BASE = Path(__file__).parent.parent
DB_PATH = BASE / "data" / "interviews.db"

# Files to index — (folder, filename, category, source_key, max_pdf_pages)
# max_pdf_pages=0 means all pages; set a limit for huge PDFs to cap indexing time
KNOWLEDGE_SOURCES = [
    # ─── Markdown: Direct Interview Content ───────────────────────────────────
    ("Interview_Answers", "Amazon_LP_STAR_Bank.md",          "behavioral",      "amazon_lp",       0),
    ("Interview_Answers", "Section_01_Java_Core.md",          "java",            "java_core",        0),
    ("Interview_Answers", "Section_02_Spring_Boot.md",        "java",            "spring_boot",      0),
    ("Interview_Answers", "Section_04_05_06_Microservices_Kafka_Redis.md", "java", "microservices",  0),
    ("Interview_Answers", "Section_07_08_Database_DistributedSystems.md", "system_design", "databases", 0),
    ("Interview_Answers", "Section_21_SystemDesign_DeepDive_With_Answers.md", "system_design", "sd_deep", 0),
    ("Interview_Answers", "GSTN_Architecture_Reference.md",   "system_design",   "gstn_arch",        0),
    ("Interview_Answers", "GSTN_Complete_SDE2_SDE3_InterviewPrep.md", "general", "gstn_prep",       0),
    ("Interview_Answers", "Company_Questions_Phase1.md",      "general",         "company_q1",       0),
    ("Interview_Answers", "Company_Questions_Phase2.md",      "general",         "company_q2",       0),
    ("Interview_Answers", "Section_20_FAANG_SDE2_SDE3_Advanced.md", "general",  "faang_adv",        0),
    ("Interview_Answers", "Section_LLD_Complete.md",          "lld",             "lld_complete",     0),
    ("Interview_Answers", "Section_DSA_Java_Patterns.md",     "dsa",             "dsa_patterns",     0),
    ("Interview_Answers", "Section_Modern_Java_Observability_CQRS.md", "java",   "modern_java",      0),
    ("Interview_Answers", "Section_Behavioral_DB_Golang.md",  "behavioral",      "behavioral_go",    0),
    ("Interview_Answers", "Section_SD_Consumer_Products.md",  "system_design",   "sd_consumer",      0),
    ("Interview_Answers", "OA_Patterns_MockInterviews_RevisionGuide.md", "dsa",  "oa_patterns",      0),
    ("Interview_Answers", "Section_API_Design_SQL_Practice.md", "system_design", "api_sql",          0),
    # ─── Markdown: Reference Docs ─────────────────────────────────────────────
    ("docs",              "GSTN_Interview_QuestionBank_296Q.md", "general",      "qbank_296",        0),
    ("docs",              "COMPANY_ANALYSIS.md",                "general",       "company_analysis", 0),
    ("docs",              "DEEP_RESEARCH_INTERVIEW_PATTERNS_2025_2026.md", "general", "patterns_2026", 0),
    ("docs",              "CPP_to_Java_DSA_CheatSheet.md",      "dsa",           "dsa_cheat",        0),
    ("docs",              "Interview_exp.txt",                   "general",       "real_experiences", 0),
    ("docs",              "MASTER_16H_WARPLAN.md",               "general",       "war_plan",         0),
    # ─── PDF: Books (Alex Xu System Design — core chapters only) ────────────
    # Vol1: 280 pages — cap at 250 to skip appendix
    ("docs/books",        "Alex_Xu_SystemDesign_Vol1.pdf",      "system_design", "alex_xu_vol1",   250),
    # Vol2: ~400 pages — cap at 350
    ("docs/books",        "Alex_Xu_SystemDesign_Vol2.pdf",      "system_design", "alex_xu_vol2",   350),
    ("docs/books",        "springpdf.pdf",                       "java",          "spring_pdf",       0),
    # ─── DOCX: Interview Guides ───────────────────────────────────────────────
    ("docs/books",        "Java_SpringBoot_Microservices_Interview_Guide.docx", "java", "java_guide_docx", 0),
    ("trackers-docs",     "The_Badass_Senior_Developer_Programme.docx", "general", "badass_sde",    0),
    ("trackers-docs",     "The_Comeback_Protocol_6Month_Roadmap.docx",  "general", "comeback_proto", 0),
    ("02_Resumes/files",  "Supplementary_Prep_Guide_Complete.docx",     "general", "supp_prep",     0),
    ("02_Resumes/files",  "Top_1_Percent_Engineer_Preparation_Blueprint.docx", "general", "top1pct", 0),
    ("01_Career_Interview_Prep", "THRIVING_PLAN_SDE2_SDE3.docx",        "general", "thriving_plan", 0),
    ("01_Career_Interview_Prep", "INTERVIEW_MASTER_SHEET.docx",          "general", "interview_master", 0),
    ("01_Career_Interview_Prep", "SDE2_Preparation_Analysis_January2026.docx", "general", "sde2_analysis", 0),
    # ─── XLSX: Interview Q&A Sheets (high signal — curated Q&A with answers) ─
    ("trackers-docs",     "Java_SpringBoot_Master_Interview_Sheet.xlsx", "java",   "java_sheet_xl", 0),
    ("trackers-docs",     "System_Design_Master_Interview_Sheet.xlsx",   "system_design", "sd_sheet_xl", 0),
    ("trackers-docs",     "LLD_Master_Interview_Sheet_v2.xlsx",          "lld",    "lld_sheet_xl",  0),
    ("trackers-docs",     "DB_OS_CN_Master_Interview_Sheet_v2.xlsx",     "system_design", "db_sheet_xl", 0),
    ("trackers-docs",     "Tech_Stack_Skills_Evaluation_Matrix.xlsx",    "general", "tech_matrix_xl", 0),
]

CHUNK_SIZE = 1200       # chars per chunk (≈300 tokens)
CHUNK_OVERLAP = 150     # overlap chars between chunks


def _discover_dynamic_sources():
    """Auto-discover new .md files in Interview_Answers/ not in KNOWLEDGE_SOURCES.
    Catches auto-generated Company_Questions_<CompanyName>.md files from kb_automation."""
    known_files = {entry[1] for entry in KNOWLEDGE_SOURCES}
    dynamic = []
    ia_dir = BASE / "Interview_Answers"
    if ia_dir.exists():
        for f in ia_dir.glob("*.md"):
            if f.name not in known_files:
                name_lower = f.name.lower()
                if "company" in name_lower or "jd" in name_lower:
                    cat = "general"
                elif "star" in name_lower or "behavioral" in name_lower:
                    cat = "behavioral"
                elif "dsa" in name_lower or "pattern" in name_lower:
                    cat = "dsa"
                elif "system" in name_lower or "design" in name_lower:
                    cat = "system_design"
                elif "lld" in name_lower:
                    cat = "lld"
                else:
                    cat = "general"
                source_key = "dynamic_" + re.sub(r"[^a-z0-9]", "_", f.stem.lower())[:30]
                dynamic.append(("Interview_Answers", f.name, cat, source_key, 0))
    return dynamic


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

# Domain-specific high-signal terms — boosted 5× during keyword extraction
# so searches for these terms strongly prefer chunks that mention them
_DOMAIN_BOOST = {
    # System Design
    "kafka","redis","sharding","replication","consistent","hashing","rate","limiter",
    "circuit","breaker","saga","cqrs","event","sourcing","eventual","consistency",
    "partition","tolerance","availability","latency","throughput","idempotent",
    "distributed","microservice","load","balancer","caching","database","nosql",
    "leader","election","consensus","raft","paxos","zookeeper","fanout","webhook",
    "debounce","throttle","backpressure","dlq","deadletter","exactly","once",
    "transaction","acid","base","cap","theorem","gossip","protocol","heartbeat",
    "snapshot","checkpoint","wal","write","ahead","log","bloom","filter","lsm",
    "btree","index","shard","replica","quorum","vector","clock","lamport",
    # Java / Spring
    "volatile","synchronized","reentrantlock","threadpool","executorservice",
    "completablefuture","reactive","webflux","springboot","hibernate","jpa",
    "transactional","autowired","dependency","injection","aop","aspect","bean",
    "singleton","prototype","garbage","collection","jvm","heap","stack","classloader",
    "concurrenthashmap","blockingqueue","semaphore","countdownlatch","cyclicbarrier",
    "streamapi","optional","lambda","functional","interface","generics","reflection",
    # DSA
    "dynamic","programming","memoization","tabulation","backtracking","greedy",
    "dijkstra","bellman","floyd","topological","sort","binary","search","trie",
    "segment","tree","fenwick","union","find","sliding","window","two","pointer",
    "monotonic","stack","bitmask","recursion","complexity",
    # LLD
    "design","pattern","factory","singleton","observer","strategy","decorator",
    "adapter","facade","proxy","command","iterator","template","method","solid",
    "srp","ocp","lsp","isp","dip","coupling","cohesion","inheritance","polymorphism",
    # Behavioral
    "leadership","principle","star","situation","task","action","result",
    "ownership","bias","action","deliver","results","invent","simplify","hire",
    "develop","best","frugal","learn","curious","disagree","commit","insist",
}


def _extract_keywords(text: str) -> str:
    """
    Extract keywords from a chunk with:
    1. Bigram extraction — "consistent hashing", "rate limiter" stored as single tokens
    2. Domain boost — technical terms appear multiple times to increase match score
    3. Standard unigram frequency ranking
    """
    clean = re.sub(r"[#*`_\[\]()>|]", " ", text)
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", clean.lower())

    stops = {"that","this","with","from","have","will","been","they","were","your",
             "when","what","which","more","some","such","than","then","also","into",
             "only","each","both","over","here","time","very","well","just","like",
             "make","need","used","using","code","data","type","value","class","object",
             "interface","return","method","public","private","static","void","string",
             "list","array","true","false","null","example","above","below","following"}

    # Unigram frequency with domain boost
    freq = {}
    for w in words:
        if w in stops or len(w) < 3:
            continue
        boost = 5 if w in _DOMAIN_BOOST else 1
        freq[w] = freq.get(w, 0) + boost

    # Bigrams — extract meaningful two-word phrases
    bigrams = []
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        if a not in stops and b not in stops and len(a) > 2 and len(b) > 2:
            bigram = f"{a}_{b}"
            # Only keep bigrams where at least one word is domain-specific
            if a in _DOMAIN_BOOST or b in _DOMAIN_BOOST:
                bigrams.append(bigram)

    ranked = sorted(freq.items(), key=lambda x: -x[1])
    top_unigrams = [w for w, _ in ranked[:35]]
    # Deduplicate bigrams
    top_bigrams = list(dict.fromkeys(bigrams))[:20]

    return " ".join(top_unigrams + top_bigrams)


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


def _index_file(conn, folder: str, filename: str, category: str,
                source_key: str, max_pdf_pages: int = 0) -> int:
    """Index one file into kb_chunks. Returns number of chunks added."""
    path = BASE / folder / filename
    if not path.exists():
        return 0

    ext = path.suffix.lower()
    if ext in (".pdf", ".docx", ".xlsx", ".xls"):
        try:
            from intel.doc_extractor import extract_file
            content = extract_file(path, max_pdf_pages=max_pdf_pages)
        except Exception:
            return 0
    else:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return 0

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


def index_github_repo(repo_path, category: str, source_prefix: str,
                      conn=None, skip_langs=None) -> dict:
    """
    Walk a cloned GitHub repo directory and index all .md / .txt files.
    Skips translated files (README-zh, README-ja, etc.) and binary files.

    repo_path : absolute Path or str to repo root
    category  : 'system_design', 'dsa', 'java', 'lld', 'general', 'behavioral'
    source_prefix : short prefix for source_key, e.g. 'sdp' or 'grokking'
    skip_langs: list of lang suffixes to skip, default ['zh', 'ja', 'tw', 'ko', 'pt', 'es']
    """
    repo_path = Path(repo_path)
    skip_langs = skip_langs or ["zh", "ja", "tw", "ko", "pt", "es", "ru", "de", "fr"]
    skip_dirs = {".git", "images", "img", "assets", "bin", "__pycache__", "node_modules"}

    stats = {"indexed": 0, "skipped": 0, "total_chunks": 0}
    close_conn = conn is None
    if conn is None:
        conn = _conn()
        _init_table(conn)

    try:
        md_files = []
        for f in sorted(repo_path.rglob("*.md")):
            # Skip translation files
            stem = f.stem.lower()
            if any(f"-{lang}" in stem for lang in skip_langs):
                continue
            # Skip hidden dirs and media dirs
            if any(part in skip_dirs for part in f.parts):
                continue
            md_files.append(f)

        # Also grab .txt files at root
        for f in sorted(repo_path.glob("*.txt")):
            md_files.append(f)

        for md_path in md_files:
            # Build a stable source_key from relative path
            rel = md_path.relative_to(repo_path)
            key_parts = list(rel.parts)
            # Remove .md extension from last part
            key_parts[-1] = key_parts[-1].replace(".md", "").replace(".txt", "")
            source_key = f"{source_prefix}_" + "_".join(key_parts)[:50]
            source_key = re.sub(r"[^a-zA-Z0-9_]", "_", source_key)

            try:
                content = md_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                stats["skipped"] += 1
                continue

            if len(content) < 100:
                stats["skipped"] += 1
                continue

            # Use relative path as source_file label
            rel_from_base = str(md_path.relative_to(BASE)) if md_path.is_relative_to(BASE) else str(rel)

            file_h = _file_hash(content)
            existing = conn.execute(
                "SELECT COUNT(*) FROM kb_chunks WHERE source_key=? AND chunk_hash=?",
                (source_key, file_h)
            ).fetchone()[0]
            if existing > 0:
                stats["skipped"] += 1
                continue

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
                    (source_key, rel_from_base, category, idx, file_h, heading, chunk_text, keywords)
                )
                added += 1

            if added > 0:
                stats["indexed"] += 1
                stats["total_chunks"] += added
                conn.commit()
            else:
                stats["skipped"] += 1

    finally:
        if close_conn:
            conn.close()

    return stats


# GitHub repos to auto-index on startup
GITHUB_REPOS = [
    # (repo_dir_relative_to_BASE, category, source_prefix)
    ("docs/github/system-design-primer", "system_design", "sdp"),
    ("docs/github/Grokking-System-Design", "system_design", "grokking"),
]


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

        # ── Static + dynamically discovered files ─────────────────────────────
        all_sources = list(KNOWLEDGE_SOURCES) + _discover_dynamic_sources()
        for entry in all_sources:
            folder, filename, category, source_key = entry[0], entry[1], entry[2], entry[3]
            max_pages = entry[4] if len(entry) > 4 else 0
            path = BASE / folder / filename
            if not path.exists():
                stats["missing"] += 1
                continue
            added = _index_file(conn, folder, filename, category, source_key, max_pdf_pages=max_pages)
            if added > 0:
                stats["indexed"] += 1
                stats["total_chunks"] += added
            else:
                stats["skipped"] += 1

        # ── GitHub repos (walk all markdown files) ────────────────────────────
        for repo_rel, category, prefix in GITHUB_REPOS:
            repo_path = BASE / repo_rel
            if not repo_path.exists():
                stats["missing"] += 1
                continue
            r = index_github_repo(repo_path, category, prefix, conn=conn)
            stats["indexed"] += r["indexed"]
            stats["skipped"] += r["skipped"]
            stats["total_chunks"] += r["total_chunks"]

        total = conn.execute("SELECT COUNT(*) FROM kb_chunks").fetchone()[0]
        stats["total_chunks_in_db"] = total
        return stats


# ─── Retrieval ────────────────────────────────────────────────────────────────

def search_kb(query: str,
              category: Optional[str] = None,
              source_key: Optional[str] = None,
              limit: int = 6) -> list[dict]:
    """
    Keyword search with 3-tier scoring:
      +10 per word matched in heading  (strongest — heading = topic declaration)
      +3  per word matched in keywords (strong — domain-boosted at index time)
      +1  per word matched in content  (weak — broad match)
    Also matches bigrams: "rate limiter" → checks for "rate_limiter" in keywords.
    """
    if not query:
        return []

    stops = {"the","and","for","that","this","with","from","have","will","been","what","when",
             "how","can","are","not","its","use","get","set","run","does","this","should","would"}

    query_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", query.lower())) - stops
    if not query_words:
        return []

    # Build bigrams from query for bigram matching
    qwords_list = [w for w in re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", query.lower()) if w not in stops]
    query_bigrams = {f"{qwords_list[i]}_{qwords_list[i+1]}" for i in range(len(qwords_list)-1)}

    with _conn() as conn:
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

        scored = []
        for row in rows:
            kw_text  = (row["keywords"] or "").lower()
            heading  = (row["heading"]  or "").lower()
            content  = row["content"].lower()
            score    = 0

            for w in query_words:
                if w in heading:
                    score += 10   # heading match = this chunk IS about this topic
                if w in kw_text:
                    score += 3    # indexed keyword match
                if w in content:
                    score += 1    # broad content match

            # Bigram bonus — "consistent hashing" beats chunks with only "consistent" or "hashing"
            for bg in query_bigrams:
                if bg in kw_text:
                    score += 6

            if score > 0:
                scored.append((score, row))

        scored.sort(key=lambda x: -x[0])
        out = []
        seen_keys = set()
        for score, row in scored[:limit * 3]:
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
