"""
Database layer for interview experiences, trends, and company intelligence.
Uses SQLite — zero setup, ships with Python.
"""

import sqlite3
import json
from datetime import datetime, date
from pathlib import Path
from .config import DB_PATH


def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create all tables. Safe to call multiple times."""
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS experiences (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        source      TEXT NOT NULL,          -- leetcode_discuss, reddit, blind, enginebogie
        source_id   TEXT,                   -- unique ID from source (URL/post_id)
        company     TEXT NOT NULL,
        role        TEXT DEFAULT 'SDE-2',   -- SDE-1, SDE-2, SDE-3, etc.
        date_posted TEXT,                   -- ISO date
        date_scraped TEXT NOT NULL,
        title       TEXT,
        body_raw    TEXT,                   -- original text
        body_summary TEXT,                  -- AI-generated summary
        overall_result TEXT,                -- offer, reject, ghosted, pending
        tc_offered  TEXT,                   -- CTC if mentioned
        prep_duration TEXT,                 -- how long they prepped
        resources_used TEXT,               -- JSON array of resources mentioned
        tips        TEXT,                   -- extracted tips
        url         TEXT,                   -- link to original
        UNIQUE(source, source_id)
    );

    CREATE TABLE IF NOT EXISTS experience_rounds (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        experience_id  INTEGER NOT NULL REFERENCES experiences(id),
        round_num      INTEGER,
        round_type     TEXT NOT NULL,       -- dsa, system_design, lld, behavioral, hr, machine_coding
        question       TEXT,
        difficulty     TEXT,                -- easy, medium, hard
        topics         TEXT,                -- JSON array: ["graphs", "dfs", "topological_sort"]
        key_insights   TEXT,
        outcome        TEXT,                -- pass, fail, unknown
        duration_mins  INTEGER
    );

    CREATE TABLE IF NOT EXISTS company_intel (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        company     TEXT NOT NULL,
        updated_at  TEXT NOT NULL,
        process     TEXT,                   -- JSON: interview process description
        common_questions TEXT,              -- JSON array of frequently asked questions
        dsa_difficulty TEXT,                -- easy, medium, hard, very_hard
        sd_topics   TEXT,                   -- JSON array of common SD topics
        lld_topics  TEXT,                   -- JSON array of common LLD topics
        behavioral_focus TEXT,              -- what they look for (LP, Googleyness, etc.)
        tc_range    TEXT,
        tips        TEXT,                   -- JSON array of aggregated tips
        success_patterns TEXT,              -- what worked for people who got offers
        failure_patterns TEXT,              -- common rejection reasons
        UNIQUE(company)
    );

    CREATE TABLE IF NOT EXISTS trending_topics (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date_logged TEXT NOT NULL,
        company     TEXT,                   -- NULL = overall trend
        topic_type  TEXT NOT NULL,          -- dsa, sd, lld, behavioral
        topic       TEXT NOT NULL,
        frequency   INTEGER DEFAULT 1,     -- how many times seen in last 30 days
        examples    TEXT                    -- JSON array of question examples
    );

    -- ─── JD Analysis ─────────────────────────────────────────────────────────
    CREATE TABLE IF NOT EXISTS jd_descriptions (
        id                  TEXT PRIMARY KEY,
        company             TEXT NOT NULL,
        role                TEXT NOT NULL,
        level               TEXT,                   -- SDE-1, SDE-2, SDE-3, etc.
        raw_jd              TEXT,
        required_skills     TEXT,                  -- JSON: ["Kafka", "Java"]
        preferred_skills    TEXT,                  -- JSON array
        skill_depth_required TEXT,                 -- JSON: {"Kafka": 9, "Java": 7}
        estimated_difficulty TEXT,                 -- junior, mid, senior, staff
        years_experience    INTEGER,
        predicted_questions  TEXT,                 -- JSON: {system_design: [], behavioral: []}
        created_at          TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS jd_skill_analysis (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        jd_id               TEXT NOT NULL REFERENCES jd_descriptions(id),
        skill_name          TEXT NOT NULL,
        importance_score    REAL,                  -- 1-10
        frequency           INTEGER DEFAULT 1,    -- how many times mentioned
        typical_questions   TEXT,                  -- JSON array of sample questions
        depth_required      INTEGER,               -- 1-10 scale
        created_at          TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS jd_analyses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date_done   TEXT NOT NULL,
        company     TEXT NOT NULL,
        role        TEXT NOT NULL,
        jd_text     TEXT,
        required_skills TEXT,               -- JSON: extracted skills
        gap_analysis TEXT,                  -- JSON: your gaps vs requirements
        study_plan  TEXT,                   -- AI-generated study plan
        similar_experiences TEXT            -- JSON: IDs of similar interview experiences
    );

    CREATE TABLE IF NOT EXISTS resource_log (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date_added  TEXT NOT NULL,
        name        TEXT NOT NULL,
        category    TEXT NOT NULL,           -- dsa, sd, lld, behavioral, java, full
        url         TEXT,
        source_type TEXT,                    -- book, course, github, youtube, blog, platform
        priority    TEXT DEFAULT 'P1',       -- P0, P1, P2
        notes       TEXT,
        completed   INTEGER DEFAULT 0,
        rating      INTEGER                  -- 1-5 personal rating after using
    );

    -- ─── Drill sessions ────────────────────────────────────────────────────────
    CREATE TABLE IF NOT EXISTS drill_sessions (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        date_done    TEXT NOT NULL,
        problem_name TEXT NOT NULL,
        time_mins    INTEGER DEFAULT 0,
        struggled    INTEGER DEFAULT 0,   -- 0/1 bool
        language     TEXT DEFAULT 'java'  -- java, cpp, python
    );

    -- ─── Mock round sessions ──────────────────────────────────────────────────
    CREATE TABLE IF NOT EXISTS mock_sessions (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        date_done       TEXT NOT NULL,
        company         TEXT NOT NULL,
        round_type      TEXT NOT NULL,       -- dsa, system_design, lld, behavioral
        score           REAL NOT NULL,       -- 1.0–5.0
        questions_json  TEXT,               -- JSON array of question strings
        time_mins       INTEGER DEFAULT 0,
        notes           TEXT,
        hire_verdict    TEXT                -- hire / no_hire
    );

    -- ─── LLD practice sessions ───────────────────────────────────────────────
    CREATE TABLE IF NOT EXISTS lld_sessions (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        date_done    TEXT NOT NULL,
        problem_key  TEXT NOT NULL,
        score        INTEGER NOT NULL,   -- 1–5
        time_mins    INTEGER DEFAULT 0,
        notes        TEXT
    );

    -- User Tips
    CREATE TABLE IF NOT EXISTS user_tips (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        company     TEXT,
        round_type  TEXT,
        tip         TEXT NOT NULL,
        author      TEXT DEFAULT 'me',
        created_at  TEXT DEFAULT (datetime('now'))
    );

    -- Indexes for fast queries
    CREATE INDEX IF NOT EXISTS idx_drill_date ON drill_sessions(date_done);
    CREATE INDEX IF NOT EXISTS idx_mock_company ON mock_sessions(company);
    CREATE INDEX IF NOT EXISTS idx_mock_date ON mock_sessions(date_done);
    CREATE INDEX IF NOT EXISTS idx_lld_date ON lld_sessions(date_done);
    CREATE INDEX IF NOT EXISTS idx_exp_company ON experiences(company);
    CREATE INDEX IF NOT EXISTS idx_exp_date ON experiences(date_scraped);
    CREATE INDEX IF NOT EXISTS idx_exp_source ON experiences(source);
    CREATE INDEX IF NOT EXISTS idx_rounds_type ON experience_rounds(round_type);
    CREATE INDEX IF NOT EXISTS idx_rounds_topics ON experience_rounds(topics);
    CREATE INDEX IF NOT EXISTS idx_trending_date ON trending_topics(date_logged);
    CREATE INDEX IF NOT EXISTS idx_trending_company ON trending_topics(company);
    CREATE INDEX IF NOT EXISTS idx_jd_company ON jd_descriptions(company);
    CREATE INDEX IF NOT EXISTS idx_jd_skill ON jd_skill_analysis(skill_name);
    CREATE INDEX IF NOT EXISTS idx_jd_skill_jd ON jd_skill_analysis(jd_id);
    CREATE INDEX IF NOT EXISTS idx_tips_company ON user_tips(company);
    """)
    conn.commit()

    # Schema migrations (idempotent)
    _run_migrations(conn)
    conn.close()


def _run_migrations(conn) -> None:
    """Apply schema migrations that can't be in CREATE TABLE IF NOT EXISTS."""
    existing_cols = {
        row[1] for row in conn.execute("PRAGMA table_info(jd_descriptions)").fetchall()
    }
    if "predicted_questions" not in existing_cols:
        conn.execute(
            "ALTER TABLE jd_descriptions ADD COLUMN predicted_questions TEXT"
        )
    conn.commit()


# ─── Experience CRUD ──────────────────────────────────────────────────────────

def insert_experience(data: dict) -> int:
    """Insert an interview experience. Returns the ID."""
    conn = get_conn()
    cur = conn.execute("""
        INSERT OR IGNORE INTO experiences
        (source, source_id, company, role, date_posted, date_scraped,
         title, body_raw, body_summary, overall_result, tc_offered,
         prep_duration, resources_used, tips, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("source"), data.get("source_id"),
        data.get("company", "Unknown"), data.get("role", "SDE-2"),
        data.get("date_posted"), str(date.today()),
        data.get("title"), data.get("body_raw"), data.get("body_summary"),
        data.get("overall_result"), data.get("tc_offered"),
        data.get("prep_duration"),
        json.dumps(data.get("resources_used", [])),
        data.get("tips"),
        data.get("url"),
    ))
    exp_id = cur.lastrowid
    conn.commit()

    # Insert rounds if provided
    for rnd in data.get("rounds", []):
        conn.execute("""
            INSERT INTO experience_rounds
            (experience_id, round_num, round_type, question, difficulty,
             topics, key_insights, outcome, duration_mins)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            exp_id, rnd.get("round_num"), rnd.get("round_type", "unknown"),
            rnd.get("question"), rnd.get("difficulty"),
            json.dumps(rnd.get("topics", [])),
            rnd.get("key_insights"), rnd.get("outcome"),
            rnd.get("duration_mins"),
        ))
    conn.commit()
    conn.close()
    return exp_id


def search_experiences(company=None, role=None, round_type=None,
                       source=None, limit=20, days=90):
    """Search interview experiences with filters."""
    conn = get_conn()
    query = "SELECT * FROM experiences WHERE company IS NOT NULL AND LOWER(company) != 'unknown' AND company != ''"
    params = []

    if company:
        query += " AND LOWER(company) LIKE ?"
        params.append(f"%{company.lower()}%")
    if role:
        query += " AND LOWER(role) LIKE ?"
        params.append(f"%{role.lower()}%")
    if source:
        query += " AND source = ?"
        params.append(source)
    if days:
        from datetime import timedelta
        cutoff = str(date.today() - timedelta(days=days))
        query += " AND date_scraped >= ?"
        params.append(cutoff)

    query += " ORDER BY date_scraped DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_rounds_for_experience(exp_id):
    """Get all rounds for a specific experience."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM experience_rounds WHERE experience_id = ? ORDER BY round_num",
        (exp_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_company_trends(company, days=30):
    """Get trending topics for a company in last N days."""
    conn = get_conn()
    cutoff = str(date.today() - __import__('datetime').timedelta(days=days))
    rows = conn.execute("""
        SELECT round_type, topics, question, difficulty
        FROM experience_rounds er
        JOIN experiences e ON er.experience_id = e.id
        WHERE LOWER(e.company) LIKE ? AND e.date_scraped >= ?
        ORDER BY e.date_scraped DESC
    """, (f"%{company.lower()}%", cutoff)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_overall_stats():
    """Dashboard stats."""
    conn = get_conn()
    stats = {}
    stats["total_experiences"] = conn.execute("SELECT COUNT(*) FROM experiences").fetchone()[0]
    stats["companies"] = conn.execute("SELECT COUNT(DISTINCT company) FROM experiences").fetchone()[0]
    stats["sources"] = [dict(row) for row in conn.execute("SELECT source, COUNT(*) as cnt FROM experiences GROUP BY source").fetchall()]
    stats["recent"] = [dict(row) for row in conn.execute(
        "SELECT company, role, overall_result, date_scraped FROM experiences ORDER BY date_scraped DESC LIMIT 5"
    ).fetchall()]
    conn.close()
    return stats


# ─── Company Intel ────────────────────────────────────────────────────────────

def upsert_company_intel(company, data):
    conn = get_conn()
    conn.execute("""
        INSERT INTO company_intel (company, updated_at, process, common_questions,
            dsa_difficulty, sd_topics, lld_topics, behavioral_focus,
            tc_range, tips, success_patterns, failure_patterns)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(company) DO UPDATE SET
            updated_at=excluded.updated_at,
            process=excluded.process,
            common_questions=excluded.common_questions,
            dsa_difficulty=excluded.dsa_difficulty,
            sd_topics=excluded.sd_topics,
            lld_topics=excluded.lld_topics,
            behavioral_focus=excluded.behavioral_focus,
            tc_range=excluded.tc_range,
            tips=excluded.tips,
            success_patterns=excluded.success_patterns,
            failure_patterns=excluded.failure_patterns
    """, (
        company, str(datetime.now()),
        json.dumps(data.get("process")),
        json.dumps(data.get("common_questions", [])),
        data.get("dsa_difficulty"),
        json.dumps(data.get("sd_topics", [])),
        json.dumps(data.get("lld_topics", [])),
        data.get("behavioral_focus"),
        data.get("tc_range"),
        json.dumps(data.get("tips", [])),
        json.dumps(data.get("success_patterns", [])),
        json.dumps(data.get("failure_patterns", [])),
    ))
    conn.commit()
    conn.close()


def get_company_intel(company):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM company_intel WHERE LOWER(company) LIKE ?",
        (f"%{company.lower()}%",)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ─── JD Analysis Log ─────────────────────────────────────────────────────────

def save_jd_analysis(company, role, jd_text, analysis):
    conn = get_conn()
    conn.execute("""
        INSERT INTO jd_analyses (date_done, company, role, jd_text,
            required_skills, gap_analysis, study_plan, similar_experiences)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(date.today()), company, role, jd_text,
        json.dumps(analysis.get("required_skills", [])),
        json.dumps(analysis.get("gap_analysis", [])),
        analysis.get("study_plan", ""),
        json.dumps(analysis.get("similar_experiences", [])),
    ))
    conn.commit()
    conn.close()


# ─── Portal Functions ─────────────────────────────────────────────────────────

def get_questions_bank(round_type=None, company=None, limit=100, min_length=20):
    """Aggregate all real questions from experience_rounds, joined with experiences.
    Returns list of dicts with: id, question, round_type, difficulty, company, role,
    source, experience_id, frequency (count of how many times question appears).
    """
    conn = get_conn()
    sql = """
        SELECT
            er.id,
            er.question,
            er.round_type,
            er.difficulty,
            e.company,
            e.role,
            e.source,
            e.id       AS experience_id,
            e.date_scraped,
            COUNT(*)   AS frequency
        FROM experience_rounds er
        JOIN experiences e ON er.experience_id = e.id
        WHERE LENGTH(COALESCE(er.question, '')) >= ?
          AND LENGTH(COALESCE(er.question, '')) <= 500
          AND er.question NOT LIKE '[%'
          AND e.company IS NOT NULL
          AND LOWER(e.company) != 'unknown'
          AND e.company != ''
    """
    params = [min_length]

    if round_type:
        sql += " AND er.round_type = ?"
        params.append(round_type)
    if company:
        sql += " AND LOWER(e.company) LIKE ?"
        params.append(f"%{company.lower()}%")

    sql += " GROUP BY LOWER(TRIM(er.question)) ORDER BY frequency DESC, e.date_scraped DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_company_profile(company):
    """Get full company profile: experiences, rounds breakdown, top questions, tips."""
    conn = get_conn()

    exp_rows = conn.execute("""
        SELECT id, title, overall_result, date_scraped, role, source, body_summary, tips, tc_offered, url
        FROM experiences
        WHERE LOWER(company) LIKE ?
        ORDER BY date_scraped DESC
        LIMIT 20
    """, (f"%{company.lower()}%",)).fetchall()

    exp_ids = [r["id"] for r in exp_rows]
    experiences = [dict(r) for r in exp_rows]

    rounds = []
    round_type_counts = {}
    top_questions = []
    if exp_ids:
        placeholders = ",".join("?" * len(exp_ids))
        round_rows = conn.execute(f"""
            SELECT round_type, question, difficulty, key_insights, outcome
            FROM experience_rounds
            WHERE experience_id IN ({placeholders})
        """, exp_ids).fetchall()
        rounds = [dict(r) for r in round_rows]
        for r in rounds:
            rt = r.get("round_type") or "unknown"
            round_type_counts[rt] = round_type_counts.get(rt, 0) + 1
        # Top questions: non-null, length > 20
        seen = set()
        for r in rounds:
            q = (r.get("question") or "").strip()
            if q and len(q) >= 20 and q.lower() not in seen:
                seen.add(q.lower())
                top_questions.append({
                    "question": q,
                    "round_type": r.get("round_type"),
                    "difficulty": r.get("difficulty"),
                })
            if len(top_questions) >= 10:
                break

    # Tips from company_intel
    intel_row = conn.execute(
        "SELECT tips, dsa_difficulty, tc_range, process FROM company_intel WHERE LOWER(company) LIKE ?",
        (f"%{company.lower()}%",)
    ).fetchone()

    conn.close()

    return {
        "company": company,
        "experience_count": len(experiences),
        "experiences": experiences,
        "round_type_counts": round_type_counts,
        "top_questions": top_questions,
        "intel": dict(intel_row) if intel_row else {},
    }


def get_portal_stats():
    """Master stats for the Experiences Portal."""
    conn = get_conn()
    total_experiences = conn.execute("SELECT COUNT(*) FROM experiences").fetchone()[0]
    total_questions = conn.execute(
        "SELECT COUNT(*) FROM experience_rounds WHERE LENGTH(COALESCE(question, '')) >= 20"
    ).fetchone()[0]
    companies_covered = conn.execute(
        "SELECT COUNT(DISTINCT company) FROM experiences WHERE company IS NOT NULL AND LOWER(company) != 'unknown' AND company != ''"
    ).fetchone()[0]
    rounds_extracted = conn.execute("SELECT COUNT(*) FROM experience_rounds").fetchone()[0]
    tips_shared = conn.execute("SELECT COUNT(*) FROM user_tips").fetchone()[0]

    recent = [dict(r) for r in conn.execute("""
        SELECT company, role, overall_result, date_scraped, source
        FROM experiences
        WHERE company IS NOT NULL AND LOWER(company) != 'unknown'
        ORDER BY date_scraped DESC LIMIT 5
    """).fetchall()]

    # Top questions by frequency
    hot_questions = [dict(r) for r in conn.execute("""
        SELECT
            er.id,
            er.question,
            er.round_type,
            er.difficulty,
            e.company,
            e.date_scraped,
            COUNT(*) AS frequency
        FROM experience_rounds er
        JOIN experiences e ON er.experience_id = e.id
        WHERE LENGTH(COALESCE(er.question,'')) >= 20
        GROUP BY LOWER(TRIM(er.question))
        ORDER BY frequency DESC
        LIMIT 6
    """).fetchall()]

    # Company heatmap: experience count + dominant round type
    heatmap = [dict(r) for r in conn.execute("""
        SELECT e.company, COUNT(DISTINCT e.id) AS exp_count
        FROM experiences e
        WHERE e.company IS NOT NULL AND LOWER(e.company) != 'unknown' AND e.company != ''
        GROUP BY LOWER(e.company)
        ORDER BY exp_count DESC
        LIMIT 20
    """).fetchall()]

    conn.close()
    return {
        "total_experiences": total_experiences,
        "total_questions": total_questions,
        "companies_covered": companies_covered,
        "rounds_extracted": rounds_extracted,
        "tips_shared": tips_shared,
        "recent_experiences": recent,
        "hot_questions": hot_questions,
        "company_heatmap": heatmap,
    }


def save_user_tip(company, round_type, tip_text, author="me"):
    """Save a user-submitted tip to user_tips table."""
    conn = get_conn()
    cur = conn.execute("""
        INSERT INTO user_tips (company, round_type, tip, author)
        VALUES (?, ?, ?, ?)
    """, (company, round_type, tip_text, author))
    tip_id = cur.lastrowid
    conn.commit()
    conn.close()
    return tip_id


def delete_user_tip(tip_id):
    """Delete a user tip by ID."""
    conn = get_conn()
    conn.execute("DELETE FROM user_tips WHERE id = ?", (tip_id,))
    conn.commit()
    conn.close()


def get_user_tips(company=None, round_type=None):
    """Retrieve user-submitted tips, optionally filtered."""
    conn = get_conn()
    sql = "SELECT * FROM user_tips WHERE 1=1"
    params = []
    if company:
        sql += " AND LOWER(company) LIKE ?"
        params.append(f"%{company.lower()}%")
    if round_type:
        sql += " AND round_type = ?"
        params.append(round_type)
    sql += " ORDER BY created_at DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Initialize DB on import
init_db()
