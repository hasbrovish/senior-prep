# INTELLIGENCE ENGINE — Setup & Usage Guide
# Extends prep.py with real-time interview intelligence + AI coaching
# Last updated: March 24, 2026

---

## WHAT THIS ADDS

Your `prep.py` now has an **intelligence layer** that:

1. **Scrapes interview experiences** from LeetCode Discuss, Reddit (4 subreddits), enginebogie.com
2. **Stores everything** in a local SQLite database (`data/interviews.db`)
3. **Detects trends** — what companies are actually asking right now
4. **Analyzes your gaps** — compares your progress against SDE-2/SDE-3 expectations
5. **AI coaching** — JD analysis, answer evaluation, STAR story generation, mock questions
6. **Curated resources** — 50+ researched resources indexed by category and priority

All new commands integrate into the existing `prep` CLI. Zero breaking changes.

---

## QUICK START (2 minutes)

```bash
# Step 1: Make sure you're in the repo
cd ~/Documents/dev/senior-prep

# Step 2: Initialize the intelligence DB (happens automatically)
python3 -c "from intel.db import init_db; init_db(); print('DB ready')"

# Step 3: Fetch interview experiences
prep scrape

# Step 4: See what's trending
prep trending
prep trending google

# Step 5: Check your readiness
prep readiness

# Step 6: Browse curated resources
prep resources
```

---

## SETUP — AI FEATURES (optional but powerful)

For AI-powered features (JD analysis, answer evaluation, STAR stories, AI mock interviews):

```bash
# Get your API key from: https://console.anthropic.com/settings/keys
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Add to your shell permanently:
echo 'export ANTHROPIC_API_KEY=sk-ant-api03-...' >> ~/.zshrc
source ~/.zshrc
```

**Cost:** ~₹800-2500/month depending on usage. Each AI call costs ~₹2-8.

---

## ALL NEW COMMANDS

### Data Aggregation
```bash
prep scrape                    # Scrape ALL sources (LeetCode, Reddit, enginebogie)
prep scrape reddit             # Scrape only Reddit
prep scrape leetcode_discuss   # Scrape only LeetCode Discuss
prep scrape enginebogie        # Scrape only enginebogie.com
prep add-experience            # Manually log experience from Blind/Medium/Discord
prep intel-status              # Show DB dashboard (how many experiences, by source)
```

### Interview Intelligence
```bash
prep trending                  # What's being asked across all companies (last 30 days)
prep trending google           # What Google is asking this month
prep trending amazon 60        # Amazon trends, last 60 days
prep experiences               # Browse all aggregated experiences
prep experiences google        # Filter by company
prep experiences amazon sde3   # Filter by company + role
prep company google            # Full company intelligence profile
prep company razorpay          # Company profile with DB data + static intel
```

### AI Coaching (requires ANTHROPIC_API_KEY)
```bash
prep jd-analyze                # Paste a JD → AI gap analysis + study plan
prep evaluate                  # Paste question + your answer → hire/no-hire rubric score
prep story                     # Describe raw experience → polished STAR story
prep story "caching"           # Generate STAR story about specific topic
prep readiness                 # Multi-dimensional readiness assessment (SDE-2)
prep readiness sde3            # Readiness assessment for SDE-3 level
prep ai-mock sd                # AI generates a system design interview question
prep ai-mock dsa               # AI generates a DSA question
prep ai-mock behavioral amazon # Amazon-style behavioral question
prep ai-mock sd google hard    # Google-style hard SD question
```

### Curated Resources
```bash
prep resources                 # Full curated resource index (50+ resources)
prep resources dsa             # DSA: NeetCode, Grind75, Striver, EPI, etc.
prep resources system_design   # SD: Hello Interview, Alex Xu, DDIA, GitHub repos
prep resources lld             # LLD: Refactoring Guru, awesome-low-level-design
prep resources behavioral      # Behavioral: IGotAnOffer, Dan Croitor, Amazon LPs
prep resources experiences     # Where to find interview experiences
prep resources full_prep       # Full prep: coding-interview-university, etc.
```

---

## HOW IT WORKS

### Architecture
```
prep.py (your existing CLI)
  ├── All existing commands (unchanged)
  └── New commands → intel/
      ├── config.py        → Sources, company profiles, level expectations
      ├── db.py            → SQLite: experiences, rounds, trends, JD analyses
      ├── scraper.py       → Orchestrator: runs all source scrapers
      ├── coach.py         → Claude API: JD analysis, evaluation, stories, mocks
      ├── analyzer.py      → Trend detection, gap analysis, company profiles
      ├── resources.py     → Curated resource index (50+ resources)
      └── sources/
          ├── leetcode_discuss.py  → LeetCode GraphQL API scraper
          ├── reddit.py            → Reddit JSON API (no API key needed)
          └── enginebogie.py       → enginebogie.com HTML scraper
```

### Database Schema (SQLite — data/interviews.db)
```
experiences         → Interview experience posts (source, company, role, result, text)
experience_rounds   → Individual interview rounds (type, question, difficulty, topics)
company_intel       → Aggregated company intelligence
trending_topics     → Topic frequency tracking
jd_analyses         → JD analysis history
resource_log        → Personal resource usage tracking
```

---

## DAILY WORKFLOW (with intelligence)

```
MORNING:
  prep                         # Today's plan (unchanged)
  prep trending google         # What Google asked this week (30 sec read)

STUDY TIME:
  prep resources sd            # Find the right SD resource for today's topic
  prep quiz system-design      # Active recall

AFTER STUDYING:
  prep evaluate                # Score your answer to a question you practiced

EVENING:
  prep ai-mock sd google       # AI generates a Google-style SD question
  prep story "kafka dlq"       # Polish a STAR story about your Kafka work

WEEKLY:
  prep scrape                  # Refresh experience DB (5 min, run on Sunday)
  prep readiness               # Check your progress vs. target
  prep company [target]        # Deep intel on your next interview target
```

---

## ADDING MORE SOURCES

To add a new scraper (e.g., Blind, Medium blogs):

1. Create `intel/sources/blind.py` with a `scrape()` function that returns a list of dicts
2. Each dict must have: `source`, `source_id`, `company`, `role`, `title`, `body_raw`
3. Add it to `SCRAPERS` dict in `intel/scraper.py`
4. Run `prep scrape blind`

The schema is flexible — partial data is fine. The AI can fill in gaps during analysis.

---

## COMPANIES COVERED

**Tier 1 (Target):** Google, Amazon, Microsoft, Adobe, Flipkart, Goldman Sachs, PhonePe, Swiggy
**Tier 2 (Safety):** Razorpay, CRED, Paytm, Meesho, MakeMyTrip

Each has: level mapping, TC range, typical rounds, focus areas, and prep checklists.

---

## FAQ

**Q: Does scraping require API keys?**
A: No. Reddit uses public JSON endpoints. LeetCode uses their public GraphQL. enginebogie is scraped.
   API keys (Reddit PRAW) are optional for better rate limits.

**Q: How much does the AI coaching cost?**
A: Claude Sonnet costs ~$3/M input tokens. A typical jd-analyze call costs ~₹5-10.
   Budget ₹1500-2500/month for daily usage.

**Q: Can I use this offline?**
A: `prep trending`, `prep experiences`, `prep readiness`, `prep resources` all work offline
   after you've done at least one `prep scrape`. Only AI features need internet + API key.

**Q: Will this break my existing prep.py?**
A: No. All existing commands work exactly the same. Intel commands are purely additive.
   If `intel/` doesn't exist, you just get "Intel module not found" — nothing crashes.

---

*This system doesn't just prepare you for interviews. It makes you think like the engineer
that Google wants to hire. The interviews are just the proof.*

*Built for: Jayanti Vishnoi | Target: Google L5 | March–September 2026*
