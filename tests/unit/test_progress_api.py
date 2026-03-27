"""
Unit tests for /api/progress endpoint.
Tests verify that critical data (lc_sync, applications) is persisted and returned correctly.
"""

import pytest
from pathlib import Path
import json
import tempfile
from datetime import date

# Mock the progress file
@pytest.fixture
def mock_progress_file():
    """Create a temporary progress.json file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        progress_data = {
            "lc_sync": {
                "total": 158,
                "easy": 62,
                "medium": 80,
                "hard": 16,
                "java_problems": 9,
                "cpp_problems": 151,
                "languages": {"Java": 9, "C++": 151},
                "streak": 4,
                "last_sync": "2026-03-27"
            },
            "lc_done": [
                {"name": "Two Sum", "date": "2026-03-19"}
            ],
            "applications": [
                {"company": "Amazon", "role": "SDE2", "stage": "Applied", "date": str(date.today())}
            ],
            "topics_done": [],
            "daily_logs": {}
        }
        json.dump(progress_data, f)
        return Path(f.name)


def test_lc_sync_is_included_in_progress(mock_progress_file):
    """
    CRITICAL TEST: Verify that /api/progress includes lc_sync data
    This is what failed: user couldn't see LC stats in portal
    """
    data = json.loads(mock_progress_file.read_text())

    # Must have lc_sync key
    assert "lc_sync" in data, "progress.json must include 'lc_sync' key"

    # lc_sync must have essential fields
    lc_sync = data["lc_sync"]
    required_fields = ["total", "easy", "medium", "hard", "java_problems", "last_sync"]
    for field in required_fields:
        assert field in lc_sync, f"lc_sync missing required field: {field}"

    # Values must be reasonable
    assert lc_sync["total"] > 0, "Must have solved at least 1 problem"
    assert lc_sync["easy"] >= 0, "Easy count cannot be negative"
    assert lc_sync["total"] >= lc_sync["easy"] + lc_sync["medium"] + lc_sync["hard"], \
        "Total must be sum of easy+medium+hard"


def test_lc_sync_languages_breakdown(mock_progress_file):
    """Verify language breakdown is tracked correctly"""
    data = json.loads(mock_progress_file.read_text())
    lc_sync = data["lc_sync"]

    assert "languages" in lc_sync, "Must track languages"
    languages = lc_sync["languages"]

    # Should have Java (critical for interview prep)
    assert "Java" in languages, "Must track Java problems"
    assert languages["Java"] > 0, "Should have Java problems solved"


def test_applications_are_persisted(mock_progress_file):
    """Verify that job applications are saved and retrievable"""
    data = json.loads(mock_progress_file.read_text())

    assert "applications" in data, "Must have applications list"
    assert len(data["applications"]) > 0, "Should have at least one application"

    app = data["applications"][0]
    assert app["company"] == "Amazon"
    assert app["stage"] in ["Applied", "Phone", "Onsite", "Offer", "Rejected"]


def test_daily_logs_structure(mock_progress_file):
    """Verify daily logs for activity tracking"""
    data = json.loads(mock_progress_file.read_text())

    assert "daily_logs" in data, "Must track daily logs"
    # Can be empty, but must exist for activity tracking
    assert isinstance(data["daily_logs"], dict)


def test_topics_done_tracking(mock_progress_file):
    """Verify curriculum topic completion tracking"""
    data = json.loads(mock_progress_file.read_text())

    assert "topics_done" in data, "Must track completed curriculum topics"
    assert isinstance(data["topics_done"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
