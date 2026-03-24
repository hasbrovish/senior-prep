#!/usr/bin/env python3
"""
PrepForge Portal Server
Serves the web UI and provides API endpoints that read/write the SAME data as prep.py.

Usage:
  python3 portal/server.py              # start on port 5555
  python3 portal/server.py 8080         # custom port

Or via prep.py:
  prep portal                           # starts server + opens browser
"""

import json, sys, os, urllib.request, urllib.error, mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import date, datetime, timedelta

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE        = Path(__file__).parent.parent
PORTAL_DIR  = Path(__file__).parent
PROG_FILE   = BASE / "logs" / "progress.json"
PORTAL_DATA = BASE / "data" / "portal_data.json"
DB_PATH     = BASE / "data" / "interviews.db"

# Ensure dirs
(BASE / "logs").mkdir(exist_ok=True)
(BASE / "data").mkdir(exist_ok=True)


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, default=str, ensure_ascii=False), encoding="utf-8")


def load_portal_data():
    return load_json(PORTAL_DATA, {
        "resources": [], "notes": [], "goals": [], "career": {},
        "coach_history": [], "sessions": [],
    })


def save_portal_data(data):
    save_json(PORTAL_DATA, data)


# ─── Intel DB helpers (if intel module available) ─────────────────────────────
def get_db_stats():
    try:
        sys.path.insert(0, str(BASE))
        from intel import db
        return db.get_overall_stats()
    except Exception:
        return None


def search_db_experiences(company=None, role=None, limit=20):
    try:
        sys.path.insert(0, str(BASE))
        from intel import db
        return db.search_experiences(company=company, role=role, limit=limit)
    except Exception:
        return []


def get_db_company_trends(company, days=30):
    try:
        sys.path.insert(0, str(BASE))
        from intel import db
        return db.get_company_trends(company, days=days)
    except Exception:
        return []


def run_scraper(source=None):
    try:
        sys.path.insert(0, str(BASE))
        from intel.scraper import run_scraper as _run
        return _run(source_name=source, verbose=False)
    except Exception as e:
        return {"error": str(e)}


def get_gap_analysis(progress, level="sde2"):
    try:
        sys.path.insert(0, str(BASE))
        from intel.analyzer import compute_gap_analysis, readiness_percentage
        gaps = compute_gap_analysis(progress, level)
        score = readiness_percentage(progress, level)
        return {"gaps": gaps, "readiness": score}
    except Exception as e:
        return {"gaps": [], "readiness": 0, "error": str(e)}


def get_trending(company=None, days=30):
    try:
        sys.path.insert(0, str(BASE))
        from intel.analyzer import get_trending_topics
        return get_trending_topics(company=company, days=days)
    except Exception:
        return {}


def get_resources_index(category=None):
    try:
        sys.path.insert(0, str(BASE))
        from intel.resources import get_resources
        return get_resources(category=category)
    except Exception:
        return []


# ─── Claude API proxy ─────────────────────────────────────────────────────────
def call_claude(messages, system_prompt):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY=sk-ant-..."}

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2000,
        "system": system_prompt,
        "messages": messages,
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            text = data.get("content", [{}])[0].get("text", "")
            return {"text": text}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"API {e.code}: {body[:300]}"}
    except Exception as e:
        return {"error": str(e)}


# ─── HTTP Handler ─────────────────────────────────────────────────────────────
class PortalHandler(BaseHTTPRequestHandler):

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str, ensure_ascii=False).encode("utf-8"))

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]

        # ── API endpoints ─────────────────────────────────────────
        if path == "/api/progress":
            self._json_response(load_json(PROG_FILE, {}))

        elif path == "/api/portal-data":
            self._json_response(load_portal_data())

        elif path == "/api/gaps":
            progress = load_json(PROG_FILE, {})
            level = self.path.split("level=")[1] if "level=" in self.path else "sde2"
            self._json_response(get_gap_analysis(progress, level))

        elif path == "/api/intel/stats":
            stats = get_db_stats()
            self._json_response(stats or {"error": "Intel DB not available"})

        elif path.startswith("/api/intel/experiences"):
            company = self.path.split("company=")[1].split("&")[0] if "company=" in self.path else None
            self._json_response(search_db_experiences(company=company))

        elif path.startswith("/api/intel/trending"):
            company = self.path.split("company=")[1].split("&")[0] if "company=" in self.path else None
            self._json_response(get_trending(company=company))

        elif path == "/api/intel/resources":
            cat = self.path.split("cat=")[1].split("&")[0] if "cat=" in self.path else None
            self._json_response(get_resources_index(cat))

        # ── Static files ──────────────────────────────────────────
        elif path == "/" or path == "/index.html":
            self._serve_file(PORTAL_DIR / "index.html")

        elif path.startswith("/"):
            file_path = PORTAL_DIR / path.lstrip("/")
            if file_path.is_file():
                self._serve_file(file_path)
            else:
                self.send_error(404)

    def do_POST(self):
        path = self.path

        if path == "/api/portal-data":
            data = self._read_body()
            save_portal_data(data)
            self._json_response({"ok": True})

        elif path == "/api/progress":
            data = self._read_body()
            save_json(PROG_FILE, data)
            self._json_response({"ok": True})

        elif path == "/api/coach":
            body = self._read_body()
            messages = body.get("messages", [])
            system = body.get("system", "You are a helpful interview coach.")
            result = call_claude(messages, system)
            self._json_response(result)

        elif path == "/api/intel/scrape":
            body = self._read_body()
            source = body.get("source")
            result = run_scraper(source=source)
            self._json_response(result)

        else:
            self.send_error(404)

    def do_PUT(self):
        self.do_POST()

    def _serve_file(self, filepath):
        try:
            content = filepath.read_bytes()
            mime = mimetypes.guess_type(str(filepath))[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", len(content))
            self._cors()
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

    def log_message(self, fmt, *args):
        # Quieter logging
        if "/api/" in (args[0] if args else ""):
            return
        super().log_message(fmt, *args)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5555
    server = HTTPServer(("127.0.0.1", port), PortalHandler)
    url = f"http://localhost:{port}"

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  PREPFORGE PORTAL                                       ║
  ╚══════════════════════════════════════════════════════════╝

  Server running at: {url}

  Data sources:
    progress.json:  {PROG_FILE}
    portal data:    {PORTAL_DATA}
    intel DB:       {DB_PATH}

  API endpoints:
    GET  /api/progress        → prep.py progress data
    GET  /api/portal-data     → portal resources, notes, goals
    GET  /api/gaps?level=sde2 → gap analysis from intel/analyzer
    GET  /api/intel/stats     → interview DB dashboard
    GET  /api/intel/trending  → trending topics
    GET  /api/intel/experiences?company=google
    POST /api/coach           → Claude AI proxy
    POST /api/intel/scrape    → run scrapers
    POST /api/portal-data     → save portal data
    POST /api/progress        → save progress data

  Press Ctrl+C to stop.
""")

    # Try to open browser
    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Portal stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
