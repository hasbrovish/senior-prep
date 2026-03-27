"""Tests for all progress endpoints (13 endpoints in app/routers/progress.py)."""

import time


class TestGetProgress:
    def test_empty_progress(self, client):
        r = client.get("/api/progress")
        assert r.status_code == 200
        assert r.json() == {}

    def test_returns_seeded_data(self, client, seed_progress):
        seed_progress({"lc_done": [{"name": "Two Sum"}], "current_week": 3})
        r = client.get("/api/progress")
        data = r.json()
        assert data["current_week"] == 3
        assert len(data["lc_done"]) == 1


class TestSaveProgress:
    def test_save_and_retrieve(self, client):
        payload = {"lc_done": [], "current_week": 5, "custom": "value"}
        r = client.post("/api/progress", json=payload)
        assert r.status_code == 200
        assert r.json()["ok"] is True

        data = client.get("/api/progress").json()
        assert data["current_week"] == 5
        assert data["custom"] == "value"

    def test_save_overwrites_previous(self, client):
        client.post("/api/progress", json={"a": 1})
        client.post("/api/progress", json={"b": 2})
        data = client.get("/api/progress").json()
        assert "a" not in data
        assert data["b"] == 2


class TestPortalData:
    def test_get_empty_portal_data(self, client):
        r = client.get("/api/portal-data")
        assert r.status_code == 200

    def test_save_and_get_portal_data(self, client):
        payload = {"notes": ["note1"], "goals": ["goal1"]}
        r = client.post("/api/portal-data", json=payload)
        assert r.status_code == 200

        data = client.get("/api/portal-data").json()
        assert data["notes"] == ["note1"]


class TestGaps:
    def test_gaps_empty_progress(self, client):
        r = client.get("/api/gaps")
        assert r.status_code == 200
        data = r.json()
        assert "gaps" in data
        assert "readiness" in data
        assert "level" in data

    def test_gaps_custom_level(self, client):
        r = client.get("/api/gaps?level=sde3")
        assert r.status_code == 200
        data = r.json()
        assert data["level"] == "sde3"


class TestLogLCProblem:
    def test_log_basic(self, client, read_progress):
        r = client.post("/api/progress/lc", json={"name": "Two Sum"})
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert data["total"] == 1

        progress = read_progress()
        assert len(progress["lc_done"]) == 1
        assert progress["lc_done"][0]["name"] == "Two Sum"

    def test_log_with_all_fields(self, client, read_progress):
        r = client.post("/api/progress/lc", json={
            "name": "Trapping Rain Water",
            "pattern": "two-pointers",
            "time_mins": 35,
            "hard": True,
            "date": "2026-03-27",
        })
        assert r.status_code == 200

        entry = read_progress()["lc_done"][0]
        assert entry["pattern"] == "two-pointers"
        assert entry["time_mins"] == 35
        assert entry["hard"] is True
        assert entry["date"] == "2026-03-27"

    def test_log_multiple_appends(self, client):
        client.post("/api/progress/lc", json={"name": "P1"})
        client.post("/api/progress/lc", json={"name": "P2"})
        r = client.post("/api/progress/lc", json={"name": "P3"})
        assert r.json()["total"] == 3


class TestLogApplication:
    def test_log_application(self, client, read_progress):
        r = client.post("/api/progress/apply", json={
            "company": "Google",
            "role": "SDE-3",
            "link": "https://careers.google.com/123",
            "stage": "Applied",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert data["id"] > 0

        apps = read_progress()["applications"]
        assert len(apps) == 1
        assert apps[0]["company"] == "Google"
        assert apps[0]["role"] == "SDE-3"

    def test_log_application_defaults(self, client, read_progress):
        r = client.post("/api/progress/apply", json={"company": "Amazon"})
        app = read_progress()["applications"][0]
        assert app["stage"] == "Applied"
        assert app["role"] == ""


class TestUpdateApplication:
    def test_update_stage(self, client, read_progress):
        r = client.post("/api/progress/apply", json={"company": "Google"})
        app_id = r.json()["id"]

        r = client.patch(f"/api/progress/applications/{app_id}", json={"stage": "Phone Screen"})
        assert r.status_code == 200

        apps = read_progress()["applications"]
        assert apps[0]["stage"] == "Phone Screen"

    def test_update_nonexistent_id(self, client):
        r = client.patch("/api/progress/applications/99999", json={"stage": "Offer"})
        assert r.status_code == 200  # gracefully succeeds (no match found)


class TestLogBug:
    def test_log_bug(self, client, read_progress):
        r = client.post("/api/progress/bug", json={
            "description": "Off-by-one in binary search",
            "category": "dsa",
            "context": "LC 704",
        })
        assert r.status_code == 200
        assert r.json()["ok"] is True

        bugs = read_progress()["bug_journal"]
        assert len(bugs) == 1
        assert bugs[0]["description"] == "Off-by-one in binary search"
        assert bugs[0]["category"] == "dsa"

    def test_bug_defaults(self, client, read_progress):
        client.post("/api/progress/bug", json={"description": "some bug"})
        bug = read_progress()["bug_journal"][0]
        assert bug["category"] == "other"


class TestLogRetro:
    def test_log_retro(self, client, read_progress):
        r = client.post("/api/progress/retro", json={
            "what_went_well": "Solved medium in 20 min",
            "what_to_improve": "Edge cases",
            "action_items": ["Practice more edge cases"],
        })
        assert r.status_code == 200
        assert r.json()["ok"] is True

        retros = read_progress()["retros"]
        assert len(retros) == 1
        assert retros[0]["what_went_well"] == "Solved medium in 20 min"


class TestLogFailure:
    def test_log_failure(self, client, read_progress):
        r = client.post("/api/progress/failure", json={
            "type": "mock_interview",
            "details": "Failed system design — forgot to discuss trade-offs",
        })
        assert r.status_code == 200

        failures = read_progress()["failures"]
        assert len(failures) == 1


class TestSRReview:
    def test_review_existing_item(self, client, seed_progress, read_progress):
        item_id = 12345
        seed_progress({
            "spaced_repetition": [
                {"id": item_id, "topic": "Kafka", "confidence": 2, "reviews": 1}
            ]
        })
        r = client.post("/api/progress/sr/review", json={
            "id": item_id,
            "confidence": 4,
        })
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert "next_review" in data

        sr = read_progress()["spaced_repetition"]
        item = [i for i in sr if i["id"] == item_id][0]
        assert item["confidence"] == 4
        assert item["reviews"] == 2

    def test_review_nonexistent_item(self, client):
        r = client.post("/api/progress/sr/review", json={"id": 99999, "confidence": 3})
        assert r.status_code == 200  # gracefully succeeds


class TestSRAdd:
    def test_add_sr_item(self, client, read_progress):
        r = client.post("/api/progress/sr/add", json={
            "topic": "Binary Search patterns",
            "category": "dsa",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert data["id"] > 0

        sr = read_progress()["spaced_repetition"]
        assert len(sr) == 1
        assert sr[0]["topic"] == "Binary Search patterns"
        assert sr[0]["confidence"] == 0
        assert sr[0]["reviews"] == 0

    def test_add_multiple_sr_items(self, client, read_progress):
        client.post("/api/progress/sr/add", json={"topic": "T1"})
        client.post("/api/progress/sr/add", json={"topic": "T2"})
        sr = read_progress()["spaced_repetition"]
        assert len(sr) == 2
