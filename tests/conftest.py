"""
Shared fixtures for PrepForge API tests.

Creates a test-specific FastAPI app that skips the heavy lifespan
(git clone, KB indexing, scheduler) and redirects all file/DB paths
to temp directories so tests never touch real data.
"""

import json
import shutil
import sqlite3
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _init_test_db(db_path: Path):
    """Initialize a fresh SQLite DB with all required tables."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    conn.executescript("""
    CREATE TABLE IF NOT EXISTS experiences (
        id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL,
        source_id TEXT, company TEXT NOT NULL, role TEXT DEFAULT 'SDE-2',
        date_posted TEXT, date_scraped TEXT NOT NULL, title TEXT,
        body_raw TEXT, body_summary TEXT, overall_result TEXT,
        tc_offered TEXT, prep_duration TEXT, resources_used TEXT,
        tips TEXT, url TEXT, UNIQUE(source, source_id)
    );
    CREATE TABLE IF NOT EXISTS experience_rounds (
        id INTEGER PRIMARY KEY AUTOINCREMENT, experience_id INTEGER NOT NULL,
        round_num INTEGER, round_type TEXT NOT NULL, question TEXT,
        difficulty TEXT, topics TEXT, key_insights TEXT, outcome TEXT,
        duration_mins INTEGER
    );
    CREATE TABLE IF NOT EXISTS company_intel (
        id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT NOT NULL,
        updated_at TEXT NOT NULL, process TEXT, common_questions TEXT,
        dsa_difficulty TEXT, sd_topics TEXT, lld_topics TEXT,
        behavioral_focus TEXT, tc_range TEXT, tips TEXT,
        success_patterns TEXT, failure_patterns TEXT, UNIQUE(company)
    );
    CREATE TABLE IF NOT EXISTS trending_topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date_logged TEXT NOT NULL,
        company TEXT, topic_type TEXT NOT NULL, topic TEXT NOT NULL,
        frequency INTEGER DEFAULT 1, examples TEXT
    );
    CREATE TABLE IF NOT EXISTS jd_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date_done TEXT NOT NULL,
        company TEXT NOT NULL, role TEXT NOT NULL, jd_text TEXT,
        required_skills TEXT, gap_analysis TEXT, study_plan TEXT,
        similar_experiences TEXT
    );
    CREATE TABLE IF NOT EXISTS resource_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date_added TEXT NOT NULL,
        name TEXT NOT NULL, category TEXT NOT NULL, url TEXT,
        source_type TEXT, priority TEXT DEFAULT 'P1', notes TEXT,
        completed INTEGER DEFAULT 0, rating INTEGER
    );
    CREATE TABLE IF NOT EXISTS drill_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date_done TEXT NOT NULL,
        problem_name TEXT NOT NULL, time_mins INTEGER DEFAULT 0,
        struggled INTEGER DEFAULT 0, language TEXT DEFAULT 'java'
    );
    CREATE TABLE IF NOT EXISTS mock_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date_done TEXT NOT NULL,
        company TEXT NOT NULL, round_type TEXT NOT NULL, score REAL NOT NULL,
        questions_json TEXT, time_mins INTEGER DEFAULT 0, notes TEXT,
        hire_verdict TEXT
    );
    CREATE TABLE IF NOT EXISTS lld_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date_done TEXT NOT NULL,
        problem_key TEXT NOT NULL, score INTEGER NOT NULL,
        time_mins INTEGER DEFAULT 0, notes TEXT
    );
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        logged_at TEXT DEFAULT (datetime('now')), date TEXT NOT NULL,
        activity_type TEXT NOT NULL, title TEXT, details TEXT,
        duration_mins INTEGER DEFAULT 0, difficulty TEXT, outcome TEXT,
        confidence INTEGER DEFAULT 3, notes TEXT
    );
    CREATE TABLE IF NOT EXISTS llm_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now')), date TEXT NOT NULL,
        period TEXT NOT NULL, plan_text TEXT, analysis_text TEXT,
        context_summary TEXT, UNIQUE(date, period)
    );
    CREATE INDEX IF NOT EXISTS idx_exp_company ON experiences(company);
    CREATE INDEX IF NOT EXISTS idx_exp_source ON experiences(source);
    CREATE INDEX IF NOT EXISTS idx_rounds_exp ON experience_rounds(experience_id);
    CREATE INDEX IF NOT EXISTS idx_drill_date ON drill_sessions(date_done);
    CREATE INDEX IF NOT EXISTS idx_mock_date ON mock_sessions(date_done);
    CREATE INDEX IF NOT EXISTS idx_lld_date ON lld_sessions(date_done);
    CREATE INDEX IF NOT EXISTS idx_activity_date ON activity_log(date);
    """)
    conn.close()


@pytest.fixture(autouse=True)
def _isolate_data(tmp_path, monkeypatch):
    """Redirect all data/log paths to tmp_path so tests are fully isolated."""
    logs_dir = tmp_path / "logs"
    data_dir = tmp_path / "data"
    portal_dir = tmp_path / "portal"
    logs_dir.mkdir()
    data_dir.mkdir()
    portal_dir.mkdir()
    (data_dir / "cache").mkdir()

    prog_file = logs_dir / "progress.json"
    prog_file.write_text("{}", encoding="utf-8")

    portal_data = data_dir / "portal_data.json"
    portal_data.write_text("{}", encoding="utf-8")

    for fname in ("hellointerviewcourse.json", "programming_pathshala_courses.json"):
        src = ROOT / "data" / fname
        if src.exists():
            shutil.copy(src, data_dir / fname)

    db_path = data_dir / "interviews.db"
    _init_test_db(db_path)

    def _test_get_conn():
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    # Patch intel.config (imported by many modules)
    monkeypatch.setattr("intel.config.BASE_DIR", tmp_path)
    monkeypatch.setattr("intel.config.DATA_DIR", data_dir)
    monkeypatch.setattr("intel.config.DB_PATH", db_path)
    monkeypatch.setattr("intel.config.CACHE_DIR", data_dir / "cache")
    monkeypatch.setattr("intel.config.LOGS_DIR", logs_dir)

    # Patch intel.db connection
    monkeypatch.setattr("intel.db.DB_PATH", db_path)
    monkeypatch.setattr("intel.db.get_conn", _test_get_conn)

    # Patch feedback_engine
    monkeypatch.setattr("intel.feedback_engine.DB_PATH", db_path)
    monkeypatch.setattr("intel.feedback_engine.BASE", tmp_path)

    def _test_fb_conn():
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    monkeypatch.setattr("intel.feedback_engine._conn", _test_fb_conn)

    # Patch router-level paths
    monkeypatch.setattr("app.routers.progress.BASE", tmp_path)
    monkeypatch.setattr("app.routers.progress.PROG_FILE", prog_file)
    monkeypatch.setattr("app.routers.progress.PORTAL_DATA", portal_data)
    monkeypatch.setattr("app.routers.career.BASE", tmp_path)
    monkeypatch.setattr("app.routers.practice.BASE", tmp_path)

    # Patch main module paths
    monkeypatch.setattr("app.main.BASE", tmp_path)
    monkeypatch.setattr("app.main.PORTAL_DIR", portal_dir)
    monkeypatch.setattr("app.main.PROG_FILE", prog_file)
    monkeypatch.setattr("app.main.PORTAL_DATA", portal_data)

    yield


@pytest.fixture()
def client(tmp_path):
    """FastAPI TestClient with a no-op lifespan (heavy init already done by fixture)."""
    from fastapi.testclient import TestClient
    from app.main import app

    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def _noop_lifespan(app):
        yield

    app.router.lifespan_context = _noop_lifespan
    try:
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c
    finally:
        app.router.lifespan_context = original_lifespan


@pytest.fixture()
def seed_progress(tmp_path):
    """Helper to seed progress.json with test data."""
    prog_file = tmp_path / "logs" / "progress.json"

    def _seed(data: dict):
        prog_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    return _seed


@pytest.fixture()
def read_progress(tmp_path):
    """Helper to read current progress.json contents."""
    prog_file = tmp_path / "logs" / "progress.json"

    def _read() -> dict:
        return json.loads(prog_file.read_text(encoding="utf-8"))

    return _read
