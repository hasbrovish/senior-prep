# PrepForge — Deployment Guide

## Architecture Overview

```
senior-prep/
├── app/                    ← FastAPI server (production-grade)
│   ├── main.py            ← App entry point, middleware, security
│   ├── scheduler.py       ← Background jobs (daily scrape, LC sync)
│   └── routers/           ← API endpoints
│       ├── progress.py    ← /api/progress, /api/gaps
│       ├── intel_routes.py← /api/intel/* (trending, experiences, scrape)
│       ├── coach.py       ← /api/coach, /api/jd-analyze, /api/evaluate
│       └── career.py      ← /api/career/* (ladder, skill-map, weekly-plan)
├── intel/                  ← Intelligence engine
│   ├── db.py              ← SQLite database
│   ├── coach.py           ← Claude API integration
│   ├── analyzer.py        ← Gap analysis, trending
│   ├── scraper.py         ← Experience aggregator
│   └── sources/           ← LeetCode, Reddit, HN scrapers
├── portal/                 ← Web dashboard
│   ├── index.html         ← Full UI (offline-capable)
│   └── server.py          ← Fallback basic server
├── prep.py                 ← CLI (all 60+ commands)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Option A — Run Locally (Development)

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Set API key (get new key from console.anthropic.com)
export ANTHROPIC_API_KEY=sk-ant-YOUR-KEY

# 3. Start portal
prep portal
# OR: python3 -m uvicorn app.main:app --reload --port 5555

# 4. Open browser
open http://localhost:5555
# API docs: http://localhost:5555/docs

# 5. Populate intel DB (run once)
prep scrape
```

---

## Option B — Deploy to Railway.app (FREE, Recommended)

Railway gives $5/month free credit — enough for this app (uses ~$2/month).
**No domain required** — Railway gives you a free `.railway.app` subdomain.

### Steps:

**1. Push to GitHub (if not already)**
```bash
git add .
git commit -m "PrepForge production ready"
git push origin main
```

**2. Deploy to Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli   # OR: brew install railway

# Login and deploy
railway login
railway init                  # creates a new project
railway up                    # deploys from current directory
```

**3. Set environment variables in Railway dashboard**
```
ANTHROPIC_API_KEY = sk-ant-YOUR-KEY
ENV = production
PORTAL_SECRET = (optional: a password to protect the portal)
```

**4. Get your URL**
Railway gives you: `https://your-project.railway.app`

**5. Persist your data** (IMPORTANT — Railway's filesystem resets on redeploy)
- Go to Railway Dashboard → Add Volume → Mount at `/app/data`
- This keeps your `interviews.db` and `portal_data.json` across deploys

---

## Option C — Deploy to Render.com (FREE, Simple)

```bash
# render.yaml (create this file)
services:
  - type: web
    name: prepforge
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false  # Set manually in dashboard
      - key: ENV
        value: production
```

**Free tier limitation**: Render spins down after 15 minutes of inactivity.
For a personal prep app this is fine — it wakes up when you open it.

---

## Option D — Self-host on VPS (DigitalOcean $4/month, Full Control)

```bash
# On your VPS:
git clone https://github.com/YOUR_USERNAME/senior-prep.git
cd senior-prep
pip3 install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# Run with systemd (keeps alive after reboot)
sudo nano /etc/systemd/system/prepforge.service
```

```ini
[Unit]
Description=PrepForge Intelligence Engine
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/senior-prep
Environment=ANTHROPIC_API_KEY=sk-ant-YOUR-KEY
Environment=ENV=production
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable prepforge
sudo systemctl start prepforge
```

---

## Domain Name (Optional but Recommended for Portfolio)

### Do you need a domain?
- **For personal prep only**: NO — Railway/Render free URL is fine
- **For portfolio**: YES — looks professional, easy to share

### Recommended registrars (cheap):
- **Namecheap**: `.dev` domain ~$10/year, `.me` ~$5/year
- **Cloudflare Registrar**: At-cost pricing, ~$9/year for `.com`
- **Porkbun**: Often cheapest — `.dev` ~$7/year first year

### Suggested domain names:
- `prepforge.dev`
- `jayanti.dev`
- `yourname-prep.dev`

### Connect domain to Railway:
1. Railway Dashboard → Your Project → Settings → Domains → Add Custom Domain
2. Add CNAME record at your registrar pointing to Railway URL
3. Railway auto-provisions SSL certificate (HTTPS free)

---

## Personal Portfolio Integration

Your portfolio site can **embed PrepForge** or **link to it**:

```html
<!-- Option 1: Embed as iframe on portfolio -->
<iframe src="https://prepforge.railway.app" width="100%" height="800px"></iframe>

<!-- Option 2: Link with a "Live Project" badge -->
<a href="https://prepforge.railway.app" target="_blank">
  View PrepForge Live Demo
</a>
```

**Portfolio talking points for PrepForge:**
- "Built a personal career intelligence platform with RAG-powered AI coaching"
- "Aggregates 100+ daily interview experiences from LeetCode, Reddit, HN via custom scrapers"
- "FastAPI backend with background scheduling, rate limiting, CORS security"
- "Claude API integration for JD analysis, answer evaluation, STAR story generation"
- "Deployed on Railway with persistent storage and automated daily data pipeline"

---

## Security Checklist

- [x] API keys in env vars (never in code)
- [x] `.env` in `.gitignore`
- [x] Rate limiting: 5 req/min on AI endpoints, 60/min on others
- [x] CORS locked to specific origins
- [x] Non-root Docker user
- [x] No raw scraped text exposed via API (body_raw stripped)
- [x] No PII fields in AI prompts (scrubbed before sending)
- [x] No copyright text stored — only summaries + links
- [ ] Optional: Add PORTAL_SECRET env var to password-protect portal

---

## Free Database Options (if you outgrow local SQLite)

| Service | Free Tier | Best For |
|---------|-----------|----------|
| **Turso** (SQLite-compatible) | 500 DBs, 9GB, 1B reads/month | Drop-in SQLite replacement |
| **Supabase** (PostgreSQL) | 500MB, 50K rows | If you add auth/users |
| **Neon** (PostgreSQL) | 512MB, 3GB storage | Serverless, scales to 0 |
| **PlanetScale** (MySQL) | 1 DB, 1GB | If you prefer MySQL |

**Migration to Turso** (when needed):
```bash
pip install libsql-experimental
# Change DB_PATH in intel/config.py to:
# "libsql://YOUR-DB.turso.io?authToken=YOUR_TOKEN"
```

---

## RAG + MCP Enhancement (Advanced)

**RAG (Retrieval-Augmented Generation)** — ALREADY BUILT:
- `app/routers/coach.py` → `_get_rag_context()` pulls relevant experiences from SQLite before each AI call
- Before every AI coach response, it retrieves matching interview experiences for that company and injects them into the prompt
- This makes the AI coaching highly specific and current (based on real interviews from the last 30 days)

**To make RAG stronger** (Phase 2):
```bash
# Add vector embeddings with Qdrant (free cloud tier: 1 cluster, 1GB)
pip install qdrant-client sentence-transformers
# Then: embed each experience and do semantic search instead of keyword search
```

**MCP (Model Context Protocol)** — for Claude.ai integration:
- MCP lets you connect PrepForge data directly to Claude.ai conversations
- Your prep data becomes available in every Claude.ai chat
- Setup: ~2 hours, not needed for the standalone app but useful for Claude.ai integration
- Worth adding in Phase 2 once the app is stable

---

## Quick Commands Summary

```bash
# Local development
prep portal              # Start FastAPI server at localhost:5555
prep scrape              # Populate intel DB with fresh experiences
prep trending google     # See what Google is asking this month
prep readiness           # Gap analysis with real DB data
prep company amazon      # Amazon intel (rounds, questions, TC)

# Deployment
railway up               # Deploy to Railway
railway logs             # View server logs
railway open             # Open deployed app in browser
```
