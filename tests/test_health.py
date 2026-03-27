"""Tests for /health, SPA catch-all, and curriculum endpoints."""


class TestHealth:
    def test_health_returns_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert "time" in data
        assert "env" in data

    def test_health_env_default(self, client):
        data = client.get("/health").json()
        assert data["env"] == "development"


class TestSPACatchAll:
    def test_unknown_path_serves_portal_or_404(self, client, tmp_path):
        portal = tmp_path / "portal" / "index.html"
        portal.write_text("<html><body>PrepForge</body></html>", encoding="utf-8")
        r = client.get("/some/react/route")
        assert r.status_code == 200
        assert "PrepForge" in r.text

    def test_catch_all_without_index_returns_404(self, client):
        r = client.get("/some/react/route")
        assert r.status_code == 404
        assert "npm run build" in r.text

    def test_api_paths_not_caught_by_spa(self, client):
        r = client.get("/api/nonexistent-endpoint-xyz")
        assert r.status_code in (404, 405, 422)

    def test_docs_not_caught_by_spa(self, client):
        r = client.get("/docs")
        assert r.status_code == 200  # FastAPI docs page


class TestCurriculum:
    def test_hi_curriculum_returns_data_or_error(self, client):
        r = client.get("/api/hi-curriculum")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, dict)

    def test_curriculum_returns_items(self, client):
        r = client.get("/api/curriculum")
        assert r.status_code == 200
        data = r.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
        assert data["total"] == len(data["items"])

    def test_curriculum_items_have_required_fields(self, client):
        r = client.get("/api/curriculum")
        data = r.json()
        if data["items"]:
            item = data["items"][0]
            for field in ("id", "category", "source", "week_start", "title", "url"):
                assert field in item, f"Missing field: {field}"

    def test_curriculum_not_shadowed_by_catch_all(self, client):
        """Regression: curriculum endpoints were unreachable due to catch-all ordering."""
        r1 = client.get("/api/hi-curriculum")
        r2 = client.get("/api/curriculum")
        assert r1.status_code != 404 or "error" in r1.json()
        assert r2.status_code == 200
