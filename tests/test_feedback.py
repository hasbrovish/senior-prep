"""Tests for feedback/logging endpoints: activity log, daily/weekly plans, stats."""


class TestLogActivity:
    def test_log_basic_activity(self, client):
        r = client.post("/api/log", json={
            "activity_type": "lc",
            "title": "Two Sum",
            "duration_mins": 15,
            "difficulty": "easy",
            "outcome": "solved",
            "confidence": 5,
        })
        assert r.status_code == 200
        data = r.json()
        assert data["logged"] is True
        assert data["id"] > 0

    def test_log_minimal_activity(self, client):
        r = client.post("/api/log", json={
            "activity_type": "notes",
            "title": "Quick review",
        })
        assert r.status_code == 200
        assert r.json()["logged"] is True

    def test_log_with_details(self, client):
        r = client.post("/api/log", json={
            "activity_type": "mock",
            "title": "Google SD mock",
            "duration_mins": 45,
            "outcome": "practiced",
            "confidence": 3,
            "notes": "Need to improve trade-off discussion",
            "details": {"company": "google", "round": "system_design"},
        })
        assert r.status_code == 200

    def test_log_missing_required_fields(self, client):
        r = client.post("/api/log", json={"title": "No type"})
        assert r.status_code == 422  # activity_type is required

    def test_log_all_activity_types(self, client):
        types = ["lc", "mock", "curriculum", "lld", "jqa", "drill",
                 "system_design", "behavioral", "notes"]
        for t in types:
            r = client.post("/api/log", json={
                "activity_type": t,
                "title": f"Test {t}",
            })
            assert r.status_code == 200, f"Failed for type: {t}"


class TestRecentLogs:
    def test_recent_logs_empty(self, client):
        r = client.get("/api/log/recent")
        assert r.status_code == 200
        data = r.json()
        assert "logs" in data
        assert data["count"] == 0

    def test_recent_logs_after_logging(self, client):
        client.post("/api/log", json={"activity_type": "lc", "title": "P1"})
        client.post("/api/log", json={"activity_type": "lc", "title": "P2"})

        r = client.get("/api/log/recent")
        data = r.json()
        assert data["count"] >= 2

    def test_recent_logs_with_days_param(self, client):
        r = client.get("/api/log/recent?days=3")
        assert r.status_code == 200

    def test_recent_logs_capped_at_30(self, client):
        r = client.get("/api/log/recent?days=100")
        assert r.status_code == 200


class TestTodaySummary:
    def test_today_summary_empty(self, client):
        r = client.get("/api/log/today")
        assert r.status_code == 200

    def test_today_summary_after_logging(self, client):
        client.post("/api/log", json={
            "activity_type": "lc",
            "title": "Two Sum",
            "duration_mins": 20,
        })
        r = client.get("/api/log/today")
        assert r.status_code == 200


class TestDailyPlan:
    def test_get_daily_plan(self, client):
        r = client.get("/api/plan/daily")
        assert r.status_code == 200

    def test_refresh_daily_plan(self, client):
        r = client.post("/api/plan/daily/refresh")
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert "background" in data["message"].lower()


class TestWeeklyPlan:
    def test_get_weekly_plan(self, client):
        r = client.get("/api/plan/weekly")
        assert r.status_code == 200

    def test_refresh_weekly_plan(self, client):
        r = client.post("/api/plan/weekly/refresh")
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True


class TestPlanStats:
    def test_plan_stats(self, client):
        r = client.get("/api/plan/stats")
        assert r.status_code == 200
