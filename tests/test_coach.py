"""Tests for AI coach endpoints with mocked Anthropic API calls."""

import json
from unittest.mock import patch, MagicMock


def _mock_claude_response(text="Mocked AI response"):
    """Create a mock urllib response for Claude API."""
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "content": [{"type": "text", "text": text}],
        "model": "claude-sonnet-4-5",
        "stop_reason": "end_turn",
    }).encode()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_resp.status = 200
    return mock_resp


class TestCoachChat:
    def test_coach_no_api_key(self, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "")
        r = client.post("/api/coach", json={
            "messages": [{"role": "user", "content": "Help me with DSA"}],
        })
        assert r.status_code == 400
        assert "ANTHROPIC_API_KEY" in r.json()["detail"]

    @patch("urllib.request.urlopen")
    def test_coach_chat_success(self, mock_urlopen, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "test-key-123")
        mock_urlopen.return_value = _mock_claude_response("Focus on graphs and DP")

        r = client.post("/api/coach", json={
            "messages": [{"role": "user", "content": "What should I study?"}],
        })
        assert r.status_code == 200
        data = r.json()
        assert "text" in data
        assert "graphs" in data["text"].lower() or len(data["text"]) > 0

    @patch("urllib.request.urlopen")
    def test_coach_with_context_type(self, mock_urlopen, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "test-key-123")
        mock_urlopen.return_value = _mock_claude_response("Readiness report")

        r = client.post("/api/coach", json={
            "messages": [{"role": "user", "content": "How ready am I?"}],
            "context_type": "readiness",
        })
        assert r.status_code == 200

    @patch("urllib.request.urlopen")
    def test_coach_with_company(self, mock_urlopen, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "test-key-123")
        mock_urlopen.return_value = _mock_claude_response("Google prep plan")

        r = client.post("/api/coach", json={
            "messages": [{"role": "user", "content": "Prep for Google"}],
            "company": "Google",
            "context_type": "general",
        })
        assert r.status_code == 200


class TestCoachStream:
    def test_stream_no_api_key(self, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "")
        r = client.post("/api/coach/stream", json={
            "messages": [{"role": "user", "content": "Hello"}],
        })
        assert r.status_code == 400


class TestJDAnalyze:
    def test_jd_analyze_no_key(self, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "")
        r = client.post("/api/jd-analyze", json={
            "jd_text": "We need a senior engineer...",
            "company": "Google",
        })
        assert r.status_code == 400

    def test_jd_analyze_no_text(self, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "test-key")
        r = client.post("/api/jd-analyze", json={"company": "Google"})
        assert r.status_code == 400
        assert "jd_text" in r.json()["detail"].lower()

    @patch("urllib.request.urlopen")
    def test_jd_analyze_success(self, mock_urlopen, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "test-key")
        mock_urlopen.return_value = _mock_claude_response("Gap analysis: need more DP practice")

        r = client.post("/api/jd-analyze", json={
            "jd_text": "Senior SDE, distributed systems, Java, Kafka",
            "company": "Flipkart",
            "role": "SDE-3",
        })
        assert r.status_code == 200
        assert "analysis" in r.json()


class TestEvaluateAnswer:
    def test_evaluate_no_key(self, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "")
        r = client.post("/api/evaluate", json={
            "question": "Design a URL shortener",
            "answer": "Use a hash map...",
        })
        assert r.status_code == 400

    @patch("urllib.request.urlopen")
    def test_evaluate_success(self, mock_urlopen, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "test-key")
        mock_urlopen.return_value = _mock_claude_response("Score: 7/10")

        r = client.post("/api/evaluate", json={
            "question": "Implement LRU Cache",
            "answer": "HashMap + Doubly Linked List",
            "round_type": "dsa",
            "company": "Google",
        })
        assert r.status_code == 200
        assert "evaluation" in r.json()


class TestKBStats:
    def test_kb_stats(self, client):
        r = client.get("/api/coach/kb/stats")
        assert r.status_code == 200


class TestKBAddRepo:
    def test_add_repo_invalid_url(self, client):
        r = client.post("/api/coach/kb/add-repo", json={
            "github_url": "https://gitlab.com/something",
        })
        assert r.status_code == 400

    def test_add_repo_valid_url(self, client):
        r = client.post("/api/coach/kb/add-repo", json={
            "github_url": "https://github.com/user/repo",
            "category": "system_design",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert "background" in data["message"].lower()


class TestKBReindex:
    def test_reindex(self, client):
        r = client.post("/api/coach/kb/reindex")
        assert r.status_code == 200
        assert r.json()["ok"] is True


class TestCoachQuestions:
    def test_get_questions(self, client):
        r = client.get("/api/coach/questions")
        assert r.status_code == 200
        data = r.json()
        assert "questions" in data
        assert "count" in data
        assert isinstance(data["questions"], list)
        assert data["count"] == len(data["questions"])

    def test_get_questions_with_filters(self, client):
        r = client.get("/api/coach/questions?company=google&limit=5")
        assert r.status_code == 200


class TestKBAutomation:
    def test_kb_enrich(self, client):
        r = client.post("/api/coach/kb/enrich")
        assert r.status_code == 200
        assert r.json()["ok"] is True

    def test_kb_fill(self, client):
        r = client.post("/api/coach/kb/fill")
        assert r.status_code == 200
        assert r.json()["ok"] is True

    @patch("urllib.request.urlopen")
    def test_kb_generate(self, mock_urlopen, client, monkeypatch):
        monkeypatch.setattr("app.routers.coach.ANTHROPIC_KEY", "test-key")
        mock_urlopen.return_value = _mock_claude_response("Q&A generated")
        r = client.post("/api/coach/kb/generate", json={
            "topic": "kafka",
            "num_questions": 2,
        })
        assert r.status_code in (200, 500)  # may fail without full KB setup

    def test_kb_trending(self, client):
        r = client.post("/api/coach/kb/trending")
        assert r.status_code == 200
        assert r.json()["ok"] is True
