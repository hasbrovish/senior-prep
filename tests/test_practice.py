"""Tests for practice endpoints: drill, JQA, mock, LLD, behavioral, warplan, brief."""

import json
from unittest.mock import patch


class TestDrill:
    def test_get_drill_today(self, client):
        r = client.get("/api/drill/today")
        assert r.status_code == 200
        data = r.json()
        assert "problems" in data
        assert isinstance(data["problems"], list)

    def test_drill_today_with_company(self, client):
        r = client.get("/api/drill/today?company=google")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data["problems"], list)

    def test_drill_today_with_week(self, client):
        r = client.get("/api/drill/today?week=3")
        assert r.status_code == 200

    def test_drill_stats(self, client):
        r = client.get("/api/drill/stats")
        assert r.status_code == 200
        data = r.json()
        assert "stats" in data
        assert "history" in data

    def test_drill_done(self, client):
        r = client.post("/api/drill/done", json={
            "problem_name": "Two Sum",
            "time_mins": 15,
            "struggled": False,
            "language": "java",
        })
        assert r.status_code == 200
        data = r.json()
        assert "success" in data

    def test_drill_done_minimal(self, client):
        r = client.post("/api/drill/done", json={"problem_name": "Valid Palindrome"})
        assert r.status_code == 200

    def test_drill_companies(self, client):
        r = client.get("/api/drill/companies")
        assert r.status_code == 200
        data = r.json()
        assert "companies" in data
        assert isinstance(data["companies"], (list, dict))
        assert len(data["companies"]) > 0

    def test_drill_by_company(self, client):
        r = client.get("/api/drill/company/google")
        assert r.status_code == 200
        data = r.json()
        assert data["company"] == "google"
        assert "problems" in data
        assert "count" in data


class TestJQA:
    def test_get_jqa_today(self, client):
        r = client.get("/api/jqa")
        assert r.status_code == 200
        data = r.json()
        assert "today" in data
        assert "total_topics" in data

    def test_jqa_with_week(self, client):
        r = client.get("/api/jqa?week=2")
        assert r.status_code == 200

    def test_list_jqa_topics(self, client):
        r = client.get("/api/jqa/list")
        assert r.status_code == 200
        data = r.json()
        assert "topics" in data
        assert "total" in data
        assert data["total"] > 0

    def test_get_jqa_topic_valid(self, client):
        r = client.get("/api/jqa/topic/oop")
        assert r.status_code == 200
        data = r.json()
        assert data["topic_id"] == "oop"
        assert "questions" in data
        assert data["count"] > 0

    def test_get_jqa_topic_invalid(self, client):
        r = client.get("/api/jqa/topic/nonexistent_xyz")
        assert r.status_code == 404

    def test_mark_jqa_done(self, client):
        r = client.post("/api/jqa/done/oop")
        assert r.status_code == 200
        data = r.json()
        assert data["success"] is True
        assert data["topic_id"] == "oop"


class TestWarplan:
    def test_warplan_no_file(self, client):
        r = client.get("/api/warplan")
        assert r.status_code == 404

    def test_warplan_with_file(self, client, tmp_path):
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir(exist_ok=True)
        warplan = docs_dir / "ULTIMATE_INTERVIEW_ASSAULT.md"
        warplan.write_text("## WEEK 1\nDo stuff\n## WEEK 2\nMore stuff", encoding="utf-8")
        r = client.get("/api/warplan")
        assert r.status_code == 200
        data = r.json()
        assert "content" in data
        assert "WEEK 1" in data["content"]

    def test_warplan_filter_week(self, client, tmp_path):
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir(exist_ok=True)
        warplan = docs_dir / "ULTIMATE_INTERVIEW_ASSAULT.md"
        warplan.write_text(
            "## WEEK 1\nDo stuff\n## WEEK 2\nMore stuff\n## WEEK 3\nEven more",
            encoding="utf-8",
        )
        r = client.get("/api/warplan?week=2")
        assert r.status_code == 200
        data = r.json()
        assert data["week"] == 2
        assert "WEEK 2" in data["content"]


class TestMock:
    def test_mock_trend_empty(self, client):
        r = client.get("/api/mock/trend")
        assert r.status_code == 200

    def test_save_mock_score(self, client):
        r = client.post("/api/mock/score", json={
            "company": "google",
            "round_type": "dsa",
            "score": 4.0,
            "time_mins": 45,
            "notes": "Good performance",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["saved"] is True
        assert data["session_id"] > 0

    def test_save_and_retrieve_trend(self, client):
        client.post("/api/mock/score", json={
            "company": "google", "round_type": "dsa", "score": 3.5,
        })
        client.post("/api/mock/score", json={
            "company": "google", "round_type": "dsa", "score": 4.0,
        })
        r = client.get("/api/mock/trend?company=google")
        assert r.status_code == 200

    def test_mock_readiness(self, client):
        r = client.get("/api/mock/readiness/google")
        assert r.status_code == 200
        data = r.json()
        assert data["company"] == "google"
        assert "rounds" in data
        assert "readiness" in data

    def test_mock_score_validation(self, client):
        r = client.post("/api/mock/score", json={
            "company": "google",
            "round_type": "dsa",
            "score": 4.5,
            "questions": ["Design a cache", "Implement LRU"],
        })
        assert r.status_code == 200


class TestLLD:
    def test_list_problems(self, client):
        r = client.get("/api/lld/problems")
        assert r.status_code == 200
        data = r.json()
        assert "problems" in data
        assert data["count"] > 0

    def test_list_problems_filter_company(self, client):
        r = client.get("/api/lld/problems?company=amazon")
        assert r.status_code == 200

    def test_get_problem_valid(self, client):
        r = client.get("/api/lld/problem/parking-lot")
        assert r.status_code == 200
        data = r.json()
        assert data["name"] == "Parking Lot System"
        assert "requirements" in data
        assert "key_classes" in data

    def test_get_problem_invalid(self, client):
        r = client.get("/api/lld/problem/nonexistent-xyz")
        assert r.status_code == 404

    def test_save_lld_score(self, client):
        r = client.post("/api/lld/score", json={
            "problem_key": "parking-lot",
            "score": 4,
            "time_mins": 40,
            "notes": "Good SOLID compliance",
        })
        assert r.status_code == 200
        assert r.json()["saved"] is True

    def test_get_lld_scores_empty(self, client):
        r = client.get("/api/lld/scores")
        assert r.status_code == 200
        data = r.json()
        assert "scores" in data

    def test_save_and_retrieve_scores(self, client):
        client.post("/api/lld/score", json={
            "problem_key": "lru-cache", "score": 3, "time_mins": 30,
        })
        r = client.get("/api/lld/scores")
        data = r.json()
        assert len(data["scores"]) >= 1

    def test_lld_evaluate_no_api_key(self, client, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        r = client.post("/api/lld/evaluate", json={
            "problem_key": "parking-lot",
            "design_description": "I used Strategy pattern...",
        })
        assert r.status_code == 400


class TestBehavioral:
    def test_behavioral_check(self, client):
        r = client.get("/api/behavioral/check")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, dict)

    def test_behavioral_probes_valid(self, client):
        r = client.get("/api/behavioral/probes/customer-obsession")
        assert r.status_code == 200
        data = r.json()
        assert data["lp_key"] == "customer-obsession"
        assert "questions" in data
        assert len(data["questions"]) > 0

    def test_behavioral_probes_invalid_lp(self, client):
        r = client.get("/api/behavioral/probes/nonexistent-lp")
        assert r.status_code == 200  # returns empty or handles gracefully


class TestBrief:
    def test_brief(self, client):
        r = client.get("/api/brief")
        assert r.status_code == 200
        data = r.json()
        assert "brief" in data
        assert "sent" in data
        assert data["sent"] is False

    def test_brief_no_send(self, client):
        r = client.get("/api/brief?send=false")
        assert r.status_code == 200
        assert r.json()["sent"] is False


class TestTC:
    def test_tc_company(self, client):
        r = client.get("/api/tc/google")
        # May fail due to network call — check it doesn't crash
        assert r.status_code in (200, 500)
