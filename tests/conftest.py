"""
Shared fixtures for PrepForge API tests.

Patches all file/DB paths to use temp directories so tests never touch real data.
"""

import json
import os
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def _isolate_data(tmp_path, monkeypatch):
    """Redirect all data/log paths to tmp_path so tests are fully isolated."""
    logs_dir = tmp_path / "logs"
    data_dir = tmp_path / "data"
    portal_dir = tmp_path / "portal"
    logs_dir.mkdir()
    data_dir.mkdir()
    portal_dir.mkdir()

    # Write empty progress.json
    prog_file = logs_dir / "progress.json"
    prog_file.write_text("{}", encoding="utf-8")

    # Write empty portal_data.json
    portal_data = data_dir / "portal_data.json"
    portal_data.write_text("{}", encoding="utf-8")

    # Copy real curriculum data files if they exist (for curriculum endpoint tests)
    for fname in ("hellointerviewcourse.json", "programming_pathshala_courses.json"):
        src = ROOT / "data" / fname
        if src.exists():
            shutil.copy(src, data_dir / fname)

    db_path = data_dir / "interviews.db"

    # Patch intel.config paths before anything imports them
    monkeypatch.setattr("intel.config.BASE_DIR", tmp_path)
    monkeypatch.setattr("intel.config.DATA_DIR", data_dir)
    monkeypatch.setattr("intel.config.DB_PATH", db_path)
    monkeypatch.setattr("intel.config.CACHE_DIR", data_dir / "cache")
    (data_dir / "cache").mkdir(exist_ok=True)
    monkeypatch.setattr("intel.config.LOGS_DIR", logs_dir)

    # Patch feedback_engine DB path
    monkeypatch.setattr("intel.feedback_engine.DB_PATH", db_path)
    monkeypatch.setattr("intel.feedback_engine.BASE", tmp_path)

    # Patch router-level BASE and file constants
    for mod_path in (
        "app.routers.progress",
        "app.routers.career",
        "app.routers.practice",
    ):
        try:
            monkeypatch.setattr(f"{mod_path}.BASE", tmp_path)
        except AttributeError:
            pass

    # Patch progress router file paths
    monkeypatch.setattr("app.routers.progress.PROG_FILE", prog_file)
    monkeypatch.setattr("app.routers.progress.PORTAL_DATA", portal_data)

    # Patch main module paths
    monkeypatch.setattr("app.main.BASE", tmp_path)
    monkeypatch.setattr("app.main.PORTAL_DIR", portal_dir)
    monkeypatch.setattr("app.main.PROG_FILE", prog_file)
    monkeypatch.setattr("app.main.PORTAL_DATA", portal_data)

    # Init database tables in the temp DB
    from intel.db import get_conn, init_db

    # Temporarily patch get_conn to use our temp DB
    original_get_conn = get_conn.__wrapped__ if hasattr(get_conn, "__wrapped__") else None

    import sqlite3

    def _test_get_conn():
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    monkeypatch.setattr("intel.db.get_conn", _test_get_conn)
    monkeypatch.setattr("intel.db.DB_PATH", db_path)

    init_db()
    from intel.feedback_engine import init_feedback_tables
    init_feedback_tables()

    yield


@pytest.fixture()
def client():
    """FastAPI TestClient that skips lifespan (DB already initialized by fixture)."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


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
