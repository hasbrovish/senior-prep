"""Tests for intel endpoints: stats, experiences, trending, resources, company, import."""


class TestIntelStats:
    def test_stats_empty_db(self, client):
        r = client.get("/api/intel/stats")
        assert r.status_code == 200
        data = r.json()
        assert "total_experiences" in data

    def test_stats_returns_numbers(self, client):
        data = client.get("/api/intel/stats").json()
        assert isinstance(data.get("total_experiences", 0), int)


class TestExperiences:
    def test_experiences_empty(self, client):
        r = client.get("/api/intel/experiences")
        assert r.status_code == 200
        data = r.json()
        assert "experiences" in data
        assert data["count"] == 0

    def test_experiences_with_limit(self, client):
        r = client.get("/api/intel/experiences?limit=5")
        assert r.status_code == 200

    def test_experiences_with_company_filter(self, client):
        r = client.get("/api/intel/experiences?company=google")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data["experiences"], list)


class TestTrending:
    def test_trending_empty_db(self, client):
        r = client.get("/api/intel/trending")
        assert r.status_code == 200

    def test_trending_with_company(self, client):
        r = client.get("/api/intel/trending?company=amazon")
        assert r.status_code == 200

    def test_trending_with_days(self, client):
        r = client.get("/api/intel/trending?days=7")
        assert r.status_code == 200


class TestResources:
    def test_resources_all(self, client):
        r = client.get("/api/intel/resources")
        assert r.status_code == 200
        data = r.json()
        assert "resources" in data
        assert len(data["resources"]) > 0

    def test_resources_by_category(self, client):
        r = client.get("/api/intel/resources?cat=dsa")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data["resources"], list)


class TestCompanyProfile:
    def test_company_profile(self, client):
        r = client.get("/api/intel/company/google")
        assert r.status_code == 200

    def test_unknown_company(self, client):
        r = client.get("/api/intel/company/unknowncorp123")
        assert r.status_code == 200  # returns empty profile, not 404


class TestManualImport:
    def test_import_experience(self, client):
        r = client.post("/api/intel/import", json={
            "source": "blind",
            "company": "razorpay",
            "role": "SDE-2",
            "title": "Razorpay SDE-2 interview experience",
            "body": "Round 1: DSA - Two Sum variant. Round 2: System Design - Payment gateway.",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["company"] == "razorpay"

    def test_import_and_find(self, client):
        client.post("/api/intel/import", json={
            "source": "enginebogie",
            "company": "flipkart",
            "title": "Flipkart SDE-2 2026",
            "body": "Three rounds of DSA + one system design.",
        })
        r = client.get("/api/intel/experiences?company=flipkart")
        data = r.json()
        assert data["count"] >= 1
        assert any("flipkart" in e.get("company", "").lower() for e in data["experiences"])

    def test_import_missing_required_field(self, client):
        r = client.post("/api/intel/import", json={
            "source": "blind",
            "title": "Missing company field",
            "body": "Some text",
        })
        assert r.status_code == 422  # Pydantic validation error


class TestImportGuide:
    def test_import_guide(self, client):
        r = client.get("/api/intel/import/guide")
        assert r.status_code == 200
        data = r.json()
        for source in ("blind", "enginebogie", "reddit", "leetcode_discuss"):
            assert source in data

    def test_guide_has_steps(self, client):
        data = client.get("/api/intel/import/guide").json()
        assert "steps" in data["blind"]
        assert len(data["blind"]["steps"]) > 0


class TestScrape:
    def test_trigger_scrape(self, client):
        r = client.post("/api/intel/scrape")
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert "background" in data["message"].lower()

    def test_trigger_scrape_specific_source(self, client):
        r = client.post("/api/intel/scrape?source=reddit")
        assert r.status_code == 200
        assert "reddit" in r.json()["message"]


class TestEnrich:
    def test_enrich_endpoint(self, client):
        r = client.post("/api/intel/enrich")
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
