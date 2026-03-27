"""Tests for career endpoints: ladder, skill-map, weekly-plan."""


class TestCareerLadder:
    def test_career_ladder(self, client):
        r = client.get("/api/career/ladder")
        assert r.status_code == 200
        data = r.json()
        assert "transitions" in data
        assert len(data["transitions"]) > 0
        assert data["transitions"][0]["from"] == "SDE-2"
        assert data["transitions"][0]["to"] == "SDE-3"

    def test_ladder_has_technical_bar(self, client):
        data = client.get("/api/career/ladder").json()
        bar = data["transitions"][0]["technical_bar"]
        for area in ("dsa", "system_design", "lld", "behavioral"):
            assert area in bar

    def test_ladder_has_your_progress(self, client):
        data = client.get("/api/career/ladder").json()
        assert "your_progress" in data
        assert data["your_progress"]["current_level"] == "SDE-2"


class TestSkillMap:
    def test_skill_map(self, client):
        r = client.get("/api/career/skill-map")
        assert r.status_code == 200
        data = r.json()
        assert "strong" in data
        assert "gaps" in data
        assert len(data["strong"]) > 0
        assert len(data["gaps"]) > 0

    def test_skills_have_company_tags(self, client):
        data = client.get("/api/career/skill-map").json()
        for skill in data["strong"]:
            assert "skill" in skill
            assert "companies" in skill

    def test_gaps_have_urgency(self, client):
        data = client.get("/api/career/skill-map").json()
        for gap in data["gaps"]:
            assert "urgency" in gap
            assert gap["urgency"] in ("CRITICAL", "HIGH", "MEDIUM", "LOW")


class TestWeeklyPlan:
    def test_weekly_plan(self, client):
        r = client.get("/api/career/weekly-plan")
        assert r.status_code == 200
        data = r.json()
        assert "week" in data
        assert isinstance(data["week"], int)
        assert 1 <= data["week"] <= 26
