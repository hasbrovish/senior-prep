"""
AI Coaching Engine — powered by Claude API.

Provides:
  - JD Analyzer: paste a JD → get gap analysis + study plan
  - Answer Evaluator: evaluate your answer to any question
  - STAR Story Generator: convert raw experience → polished stories
  - Trend Analyzer: analyze aggregated data for patterns
  - Readiness Scorer: multi-dimensional confidence assessment
  - AI Mock Interviewer: interactive mock interviews with feedback

Requires: ANTHROPIC_API_KEY env var or in config_local.py
"""

import json
import urllib.request
import urllib.error
import os

from .config import ANTHROPIC_API_KEY, CLAUDE_MODEL, CLAUDE_MAX_TOKENS, PROFILE, TARGET_COMPANIES, LEVEL_EXPECTATIONS


def _call_claude(system_prompt, user_message, max_tokens=None):
    """Call Claude API and return the text response."""
    api_key = ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "[ERROR] Set ANTHROPIC_API_KEY env var first:\n  export ANTHROPIC_API_KEY=sk-ant-..."

    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": max_tokens or CLAUDE_MAX_TOKENS,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
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
            return data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return f"[API Error {e.code}] {body[:500]}"
    except Exception as e:
        return f"[Error] {e}"


def _profile_context():
    """Build a context string about Jayanti's profile for AI prompts."""
    return f"""
CANDIDATE PROFILE:
- Name: {PROFILE['name']}
- YOE: {PROFILE['yoe']} years
- Current: {PROFILE['current']}
- Project: {PROFILE['project']} — {PROFILE['scale']}
- Tech Stack: {', '.join(PROFILE['stack'])}
- Key Strengths: {'; '.join(PROFILE['strengths'])}
- Known Weak Areas: {'; '.join(PROFILE['weak_areas'])}
- Target Companies: {', '.join(PROFILE['targets'])}
- CP Background: {PROFILE['cp_badges']}
- LeetCode: {PROFILE['lc_user']} — 155 solved (151 C++, 4 Java) — transitioning to Java
"""


# ─── JD Analyzer ──────────────────────────────────────────────────────────────

def analyze_jd(jd_text, company="", role=""):
    """Analyze a job description and return gap analysis + study plan."""

    system = f"""You are an expert SDE interview coach specializing in Indian tech market (25-50 LPA range).
{_profile_context()}

Analyze the given JD and provide:
1. REQUIRED SKILLS: Extract every technical skill mentioned
2. GAP ANALYSIS: For each skill, rate the candidate's readiness (Strong/Moderate/Weak/Missing)
   based on their profile above
3. INTERVIEW PREDICTION: What rounds to expect, likely questions based on this JD
4. PRIORITY STUDY PLAN: Top 5 things to study, ordered by impact, with specific resources
5. GSTN STORIES TO PREPARE: Which GSTN experiences map to this JD's requirements
6. TIME ESTIMATE: How many days of focused prep needed

Be specific and actionable. Reference concrete resources (LeetCode problems, system design topics, etc.)."""

    user = f"Company: {company}\nRole: {role}\n\nJOB DESCRIPTION:\n{jd_text}"
    return _call_claude(system, user)


# ─── Answer Evaluator ─────────────────────────────────────────────────────────

def evaluate_answer(question, answer, round_type="general", company=""):
    """Evaluate an interview answer on a hire/no-hire rubric."""

    company_context = ""
    if company.lower() in TARGET_COMPANIES:
        tc = TARGET_COMPANIES[company.lower()]
        company_context = f"\nCompany: {company} | Level: {tc['level']} | Focus: {tc['focus']}"

    system = f"""You are a senior SDE-3 interviewer at a top tech company.
{_profile_context()}{company_context}

Evaluate the candidate's answer using this rubric:

For DSA: Correctness | Time/Space Complexity | Code Quality | Communication | Edge Cases
For System Design: Requirements | Architecture | Deep Dive | Tradeoffs | Scalability
For Behavioral: STAR Structure | Specificity (numbers) | Impact | Leadership Signal | Communication
For LLD: SOLID Compliance | Extensibility | Patterns | Testing | Production-readiness

Provide:
1. SCORE: X/10 with breakdown per criteria
2. VERDICT: Strong Hire / Hire / Lean Hire / Lean No Hire / No Hire
3. WHAT WAS GOOD: 2-3 specific strengths
4. WHAT WAS MISSING: 2-3 specific gaps (these are what cost you the round)
5. REWRITTEN "HIRE LEVEL" ANSWER: Show what a 9/10 answer looks like
6. SIMILAR QUESTIONS TO PRACTICE: 3 related questions to drill"""

    user = f"Round Type: {round_type}\n\nQUESTION:\n{question}\n\nCANDIDATE'S ANSWER:\n{answer}"
    return _call_claude(system, user)


# ─── STAR Story Generator ────────────────────────────────────────────────────

def generate_star_story(raw_experience, target_company="", target_principle=""):
    """Convert raw experience description into a polished STAR story."""

    system = f"""You are a behavioral interview coach who has helped 500+ engineers land FAANG offers.
{_profile_context()}

Convert the raw experience into a polished STAR story optimized for interview delivery.

Format:
SITUATION (2-3 sentences): Set the context with scale/stakes
TASK (1-2 sentences): Your specific responsibility
ACTION (4-6 sentences): What YOU did (not the team), technical details, decisions made
RESULT (2-3 sentences): Quantified impact with numbers

Rules:
- Include specific numbers: users, requests/sec, latency reduction, % improvement
- Show decision-making: "I chose X over Y because..."
- Show ownership: "I" not "we" for your specific contributions
- End with learning: what you'd do differently
- Keep total length: 90-120 seconds spoken (~250 words)
{f'- Optimize for: {target_company} {target_principle}' if target_company else ''}"""

    user = f"Raw experience:\n{raw_experience}"
    return _call_claude(system, user)


# ─── Trend Analyzer ──────────────────────────────────────────────────────────

def analyze_trends(experiences_data, company=None):
    """Analyze aggregated interview experiences to find patterns."""

    system = f"""You are an interview intelligence analyst. Analyze the provided interview experience data
and identify actionable patterns.

Provide:
1. MOST ASKED TOPICS (last 30 days): DSA topics, SD questions, behavioral themes
2. DIFFICULTY TREND: Is it getting harder? Easier? New formats?
3. NEW PATTERNS: Anything unusual (new round types, AI-coding rounds, take-home assignments)
4. PREP RECOMMENDATIONS: Based on these patterns, what should the candidate focus on THIS WEEK
5. RED FLAGS: Companies that seem to be hiring less, or have changed their process

Be data-driven. Reference specific questions/topics from the data."""

    # Summarize the data for the prompt
    summary = json.dumps(experiences_data[:50], indent=2, default=str)  # Limit to avoid token overflow
    user_msg = f"{'Company filter: ' + company if company else 'All companies'}\n\nINTERVIEW DATA:\n{summary}"
    return _call_claude(system, user_msg)


# ─── Readiness Scorer ─────────────────────────────────────────────────────────

def score_readiness(progress_data, target_level="sde2"):
    """Multi-dimensional readiness assessment."""

    expectations = LEVEL_EXPECTATIONS.get(target_level, LEVEL_EXPECTATIONS["sde2"])

    system = f"""You are an interview readiness assessment engine.
{_profile_context()}

TARGET LEVEL EXPECTATIONS:
{json.dumps(expectations, indent=2)}

Based on the candidate's progress data, provide a readiness assessment:

1. OVERALL READINESS: X% with one-line summary
2. DSA: X% — analysis of problem count, difficulty distribution, Java conversion status
3. SYSTEM DESIGN: X% — how many designs practiced, depth level
4. LLD: X% — patterns known, problems practiced
5. BEHAVIORAL: X% — STAR stories prepared, articulation quality
6. PER-COMPANY READINESS: For each target company, estimate % readiness
7. BIGGEST GAPS: Top 3 things to fix THIS WEEK
8. TIMELINE: Estimated weeks until interview-ready for mid-tier vs top-tier

Output as a structured report. Be honest — overconfidence kills interview performance."""

    user = f"Level: {target_level}\n\nPROGRESS DATA:\n{json.dumps(progress_data, indent=2, default=str)}"
    return _call_claude(system, user)


# ─── AI Mock Interview (Interactive) ─────────────────────────────────────────

def mock_interview_question(round_type, company="", difficulty="medium", context=""):
    """Generate a single mock interview question with evaluation criteria."""

    company_ctx = ""
    if company.lower() in TARGET_COMPANIES:
        tc = TARGET_COMPANIES[company.lower()]
        company_ctx = f"\nCompany: {company} | Style: {tc['focus']} | Rounds: {', '.join(tc['rounds'])}"

    system = f"""You are a senior interviewer conducting a {round_type} round.
{company_ctx}

Generate ONE realistic interview question that would be asked at {company or 'a top tech company'}
for an SDE-2/SDE-3 candidate with 5.5 YOE in Java/distributed systems.

Provide:
1. THE QUESTION (exactly as an interviewer would ask it)
2. WHAT THEY'RE REALLY TESTING (hidden evaluation criteria)
3. FOLLOW-UP QUESTIONS the interviewer would ask (3 probing questions)
4. EVALUATION RUBRIC (what "hire" vs "no hire" looks like)
5. HINTS (for when the candidate is stuck — progressive hints)

Difficulty: {difficulty}
Context: {context or 'General ' + round_type + ' round'}"""

    user = f"Generate a {difficulty} {round_type} question for {company or 'a FAANG company'}"
    return _call_claude(system, user)


# ─── Company Intel Generator ─────────────────────────────────────────────────

def generate_company_intel(company, experiences=None):
    """Generate comprehensive company intelligence from aggregated data."""

    system = f"""You are an interview intelligence analyst specializing in the Indian tech market.
{_profile_context()}

Generate a comprehensive company intelligence report:

1. INTERVIEW PROCESS: Typical rounds, timeline, format
2. CULTURE & VALUES: What they optimize for in hiring
3. COMMON QUESTIONS: Top 5 DSA, top 3 SD, top 3 behavioral questions
4. DIFFICULTY LEVEL: Compared to FAANG baseline
5. YOUR ADVANTAGE: How GSTN experience maps to their problems
6. YOUR RISK: What might trip you up specifically
7. PREP CHECKLIST: 10 must-do items before interviewing here
8. SALARY NEGOTIATION: TC range, negotiation tips, competing offer strategy

Be specific to the candidate's profile. No generic advice."""

    exp_context = ""
    if experiences:
        exp_context = f"\n\nRECENT INTERVIEW DATA:\n{json.dumps(experiences[:20], indent=2, default=str)}"

    user = f"Company: {company}{exp_context}"
    return _call_claude(system, user)
