"""
AI Coach endpoints — Claude-powered analysis, STAR stories, readiness, mocks.
All endpoints stream or return structured responses.
Includes RAG: retrieves relevant interview experiences before prompting Claude.
"""

import os, json, sys
from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

BASE = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE))

router = APIRouter()

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

try:
    from intel.config import CLAUDE_MODEL, CLAUDE_MAX_TOKENS
except ImportError:
    CLAUDE_MODEL      = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")
    CLAUDE_MAX_TOKENS = 4096

PROFILE_CONTEXT = """
CANDIDATE: Jayanti Vishnoi | 5.5 YOE | GSTN (14M users, 100K+ concurrent, 3B+ invoices/year)
STACK: Java, Spring Boot, Hibernate, Kafka, Redis, MySQL, MongoDB, HBase, Golang, Docker, K8s, AWS
STRENGTHS: Distributed caching (JBoss DataGrid), Kafka exactly-once+DLQ, XA transactions (Atomikos),
           Strategy+Factory workflow engine, HBase+MySQL ledger, 500 GST filings/sec
GAPS: Java DSA (4/155 in Java — CRITICAL), Hard LeetCode, LLD depth, FAANG SD framing, Golang channels
TARGETS: Google L4/L5 | Amazon SDE-2/3 | Goldman Sachs | Flipkart | Razorpay | PhonePe
CP: CodeChef 4-star, CodeVita Top 1%, Google Code Jam qualifier
"""


class CoachMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str

class CoachRequest(BaseModel):
    messages: List[CoachMessage]
    system: Optional[str] = None
    context_type: Optional[str] = None   # "jd", "answer_eval", "star", "readiness", "mock", "general"
    company: Optional[str] = None
    round_type: Optional[str] = None


def _get_rag_context(query: str,
                     context_type: str = "general",
                     company: Optional[str] = None,
                     limit: int = 5) -> str:
    """
    Full RAG context = knowledge base (your prep docs) + scraped interview experiences.
    """
    ctx_parts = []

    # 1. Knowledge base — your Interview_Answers/ + docs/ files
    try:
        from intel.knowledge_base import get_coach_context
        kb_ctx = get_coach_context(query, context_type=context_type, company=company)
        if kb_ctx:
            ctx_parts.append(kb_ctx)
    except Exception:
        pass

    # 2. Scraped interview experiences (from DB)
    try:
        from intel.db import search_experiences
        from intel.exp_extractor import get_enriched_questions
        # First try LLM-enriched questions
        enriched_qs = get_enriched_questions(company=company, limit=8)
        if enriched_qs:
            lines = ["\n--- REAL INTERVIEW QUESTIONS (LLM-extracted from scraped posts) ---"]
            for q in enriched_qs[:5]:
                lines.append(f"[{q['company']} | {q['round_type']} | {q['difficulty']}] {q['question']}")
                if q.get("key_insight"):
                    lines.append(f"  → Insight: {q['key_insight']}")
            ctx_parts.append("\n".join(lines))

        # Also include experience summaries
        results = search_experiences(company=company, limit=limit)
        if results:
            lines = ["\n--- INTERVIEW EXPERIENCE SUMMARIES ---"]
            for r in results[:3]:
                lines.append(f"[{r['company']} {r['role']}] {r['title']}")
                if r.get("body_summary"):
                    lines.append(f"  Summary: {r['body_summary'][:200]}")
            ctx_parts.append("\n".join(lines))
    except Exception:
        pass

    return "\n".join(ctx_parts)


def _call_claude_stream(system_prompt: str, messages: list):
    """Stream Claude response via SSE."""
    import urllib.request, urllib.error

    payload = json.dumps({
        "model": CLAUDE_MODEL,
        "max_tokens": CLAUDE_MAX_TOKENS,
        "stream": True,
        "system": system_prompt,
        "messages": messages,
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            for line in resp:
                line = line.decode("utf-8").strip()
                if line.startswith("data:"):
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        if chunk.get("type") == "content_block_delta":
                            text = chunk.get("delta", {}).get("text", "")
                            if text:
                                yield f"data: {json.dumps({'text': text})}\n\n"
                    except json.JSONDecodeError:
                        pass
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


def _call_claude(system_prompt: str, messages: list) -> str:
    """Non-streaming Claude call."""
    import urllib.request, urllib.error

    payload = json.dumps({
        "model": CLAUDE_MODEL,
        "max_tokens": CLAUDE_MAX_TOKENS,
        "system": system_prompt,
        "messages": messages,
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise HTTPException(502, f"AI API error {e.code}: {body[:200]}")
    except Exception as e:
        raise HTTPException(500, str(e))


def _build_system(context_type: str, company: str = "", rag_ctx: str = "") -> str:
    base = f"You are PrepForge AI Coach — a FAANG-level interview mentor.\n{PROFILE_CONTEXT}"

    templates = {
        "jd": f"""{base}
Analyze the job description. Provide:
1. REQUIRED SKILLS — extracted technical requirements
2. GAP ANALYSIS — for each skill: Strong/Moderate/Weak/Missing (based on candidate profile)
3. INTERVIEW PREDICTION — expected rounds and likely questions
4. PRIORITY STUDY PLAN — top 5 things to study, ordered by impact
5. GSTN STORY MAPPING — which GSTN experiences map to this JD
6. TIME ESTIMATE — days of focused prep needed
Be specific. Reference exact GSTN systems when relevant.{rag_ctx}""",

        "answer_eval": f"""{base}
Evaluate the candidate's answer. Return:
1. SCORE: X/10 with breakdown (correctness, complexity, communication, edge cases)
2. VERDICT: Strong Hire / Hire / Lean Hire / Lean No Hire / No Hire
3. STRENGTHS: 2-3 specific positives
4. MISSING: 2-3 specific gaps that cost points
5. HIRE-LEVEL ANSWER: Show what a 9/10 answer looks like
6. PRACTICE: 3 related questions to drill{rag_ctx}""",

        "star": f"""{base}
Convert the raw experience into a polished STAR story (90-120 seconds spoken).
Format: SITUATION → TASK → ACTION (what YOU did, with technical depth) → RESULT (quantified)
Rules: Use specific numbers, show decision-making "I chose X over Y because...",
       ownership "I" not "we", end with learning.
{"Optimize for: " + company if company else ""}{rag_ctx}""",

        "readiness": f"""{base}
Assess interview readiness. Return structured report:
1. OVERALL: X% — one-line summary
2. DSA: X% — Java problems count, difficulty distribution, gap
3. SYSTEM DESIGN: X% — designs practiced, depth
4. LLD: X% — patterns known, problems practiced
5. BEHAVIORAL: X% — STAR stories ready
6. PER-COMPANY: For each target, estimate readiness %
7. TOP 3 GAPS: What to fix THIS WEEK
8. TIMELINE: Weeks until interview-ready for mid-tier vs top-tier
Be honest. Overconfidence kills interview performance.{rag_ctx}""",

        "mock": f"""{base}
Generate ONE realistic interview question for an SDE-2/SDE-3 with 5.5 YOE in Java/distributed systems.
{"Company: " + company if company else "Company: top tech company"}
Include:
1. THE QUESTION (exactly as asked in an interview)
2. WHAT THEY'RE TESTING (hidden evaluation criteria)
3. FOLLOW-UP QUESTIONS (3 probing questions)
4. EVALUATION RUBRIC (hire vs no-hire criteria)
5. PROGRESSIVE HINTS (for when candidate is stuck)""",

        "general": f"""{base}
You are a direct, actionable interview coach. No fluff. Give concrete next steps.
Reference GSTN experience in advice — it's the candidate's biggest asset.
When analyzing gaps, be brutally honest. When celebrating progress, be warm.{rag_ctx}""",
    }

    return templates.get(context_type, templates["general"])


@router.post("/coach")
async def coach_chat(body: CoachRequest):
    """Non-streaming AI coach. For chat interactions."""
    if not ANTHROPIC_KEY:
        raise HTTPException(400, "ANTHROPIC_API_KEY not configured")

    ctx_type = body.context_type or "general"
    rag = _get_rag_context(
        body.messages[-1].content if body.messages else "",
        context_type=ctx_type,
        company=body.company
    )
    system = body.system or _build_system(ctx_type, body.company or "", rag)
    messages = [{"role": m.role, "content": m.content} for m in body.messages]

    text = _call_claude(system, messages)
    return {"text": text}


@router.post("/coach/stream")
async def coach_stream(body: CoachRequest):
    """Streaming AI coach — returns SSE stream for real-time typing effect."""
    if not ANTHROPIC_KEY:
        raise HTTPException(400, "ANTHROPIC_API_KEY not configured")

    ctx_type = body.context_type or "general"
    rag = _get_rag_context(
        body.messages[-1].content if body.messages else "",
        context_type=ctx_type,
        company=body.company
    )
    system = body.system or _build_system(ctx_type, body.company or "", rag)
    messages = [{"role": m.role, "content": m.content} for m in body.messages]

    return StreamingResponse(
        _call_claude_stream(system, messages),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/jd-analyze")
async def analyze_jd(body: dict):
    if not ANTHROPIC_KEY:
        raise HTTPException(400, "ANTHROPIC_API_KEY not configured")
    jd = body.get("jd_text", "")
    company = body.get("company", "")
    if not jd:
        raise HTTPException(400, "jd_text required")
    rag = _get_rag_context(jd, context_type="jd", company=company)
    system = _build_system("jd", company, rag)
    result = _call_claude(system, [{"role": "user", "content": f"Company: {company}\n\nJD:\n{jd}"}])
    # Save to DB
    try:
        from intel.db import save_jd_analysis
        save_jd_analysis(company, body.get("role", "SDE-2"), jd, {"study_plan": result})
    except Exception:
        pass
    return {"analysis": result}


@router.post("/evaluate")
async def evaluate_answer(body: dict):
    if not ANTHROPIC_KEY:
        raise HTTPException(400, "ANTHROPIC_API_KEY not configured")
    question = body.get("question", "")
    answer   = body.get("answer", "")
    round_type = body.get("round_type", "general")
    company  = body.get("company", "")
    rag = _get_rag_context(question, context_type="answer_eval", company=company)
    system = _build_system("answer_eval", company, rag)
    prompt = f"Round: {round_type}\nQuestion: {question}\nAnswer: {answer}"
    result = _call_claude(system, [{"role": "user", "content": prompt}])
    return {"evaluation": result}


@router.get("/coach/kb/stats")
async def kb_stats():
    """Knowledge base statistics — how many chunks indexed from which documents."""
    try:
        from intel.knowledge_base import get_kb_stats
        return get_kb_stats()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/coach/kb/add-repo")
async def kb_add_repo(background_tasks: BackgroundTasks, body: dict):
    """
    Clone a public GitHub repo and index all its markdown files.
    Body: { "github_url": "https://github.com/owner/repo", "category": "system_design" }
    Runs in background — check /api/coach/kb/stats after ~30s.
    """
    import re as _re
    github_url = body.get("github_url", "").strip()
    category = body.get("category", "system_design")

    if not github_url.startswith("https://github.com/"):
        raise HTTPException(400, "github_url must start with https://github.com/")

    # Only allow public repos (no credentials passed)
    import subprocess, os
    from pathlib import Path

    BASE = Path(__file__).parent.parent.parent
    github_dir = BASE / "docs" / "github"
    github_dir.mkdir(parents=True, exist_ok=True)

    repo_name = github_url.rstrip("/").split("/")[-1]
    repo_name = _re.sub(r"[^a-zA-Z0-9_\-]", "_", repo_name)
    clone_path = github_dir / repo_name
    prefix = _re.sub(r"[^a-zA-Z0-9]", "_", repo_name)[:12]

    def _do():
        try:
            if clone_path.exists():
                subprocess.run(["git", "-C", str(clone_path), "pull", "--depth=1"],
                               capture_output=True, timeout=120)
            else:
                subprocess.run(["git", "clone", "--depth=1", github_url, str(clone_path)],
                               capture_output=True, timeout=120)
            from intel.knowledge_base import index_github_repo
            index_github_repo(clone_path, category=category, source_prefix=prefix)
        except Exception:
            pass

    background_tasks.add_task(_do)
    return {
        "ok": True,
        "repo": repo_name,
        "clone_path": str(clone_path),
        "message": f"Cloning + indexing {github_url} in background. Check /api/coach/kb/stats in ~30s."
    }


@router.post("/coach/kb/reindex")
async def kb_reindex(background_tasks: BackgroundTasks, force: bool = False):
    """Re-index all documents into the knowledge base (runs in background)."""
    def _do():
        try:
            from intel.knowledge_base import init_kb
            init_kb(force=force)
        except Exception:
            pass
    background_tasks.add_task(_do)
    return {"ok": True, "message": "Re-indexing knowledge base in background"}


@router.get("/coach/questions")
async def get_real_questions(company: Optional[str] = None,
                              round_type: Optional[str] = None,
                              limit: int = 30):
    """Real interview questions extracted by LLM from scraped posts."""
    try:
        from intel.exp_extractor import get_enriched_questions
        questions = get_enriched_questions(company=company, round_type=round_type, limit=limit)
        return {"questions": questions, "count": len(questions)}
    except Exception as e:
        raise HTTPException(500, str(e))
