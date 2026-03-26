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
    """Extract important keywords from a chunk for fast keyword search."""
    # Remove markdown symbols
    clean = re.sub(r"[#*`_\[\]()>|]", " ", text)
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{3,}\b", clean)
    # Count frequency
    freq = {}
    for w in words:
        w = w.lower()
        freq[w] = freq.get(w, 0) + 1
    # Top 40 words by frequency, excluding stopwords
    stops = {"that","this","with","from","have","will","been","they","were","your",
             "when","what","which","more","some","such","than","then","also","into",
             "only","each","both","over","here","time","very","well","just","like",
             "make","need","used","using","code","data","type","value","class","object",
             "interface","return","method","function","public","private","static","void","string","list","array"}
    ranked = sorted([(w, c) for w, c in freq.items() if w not in stops and len(w) > 3],
                    key=lambda x: -x[1])
    return " ".join(w for w, _ in ranked[:40])


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
        for entry in KNOWLEDGE_SOURCES:
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
    """
    if not query:
        return []

    # Normalize query → search terms
    query_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", query.lower()))
    stops = {"the","and","for","that","this","with","from","have","will","been","what","when",
             "how","can","are","not","its","use","get","set","run"}
    query_words -= stops
    if not query_words:
        return []

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
            score = 0
            for w in query_words:
                if w in kw_text:
                    score += 3  # keyword match = strong signal
                if w in content_lower:
                    score += 1  # content match = weaker
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
