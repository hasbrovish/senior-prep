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
    """)
    conn.commit()
    conn.close()


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
    query = "SELECT * FROM experiences WHERE 1=1"
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
    stats["sources"] = conn.execute("SELECT source, COUNT(*) as cnt FROM experiences GROUP BY source").fetchall()
    stats["recent"] = conn.execute(
        "SELECT company, role, overall_result, date_scraped FROM experiences ORDER BY date_scraped DESC LIMIT 5"
    ).fetchall()
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


# Initialize DB on import
init_db()
