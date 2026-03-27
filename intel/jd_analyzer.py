"""
JD Analyzer — Phases 1, 2, 3.

Phase 1: Extract skills from JD + predict questions (stored in DB)
Phase 2: Skill gap analysis (user skills vs JD requirements)
Phase 3: Prep roadmap generation (week-by-week plan)

Uses urllib.request for Anthropic calls (no SDK required).
"""

import json
import os
import re
import urllib.request
import urllib.error
from datetime import datetime, date
from collections import Counter

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
_CLAUDE_MODEL = "claude-haiku-4-5-20251001"


# ─── Anthropic helper ─────────────────────────────────────────────────────────

def _call_claude(prompt: str, max_tokens: int = 1500) -> str:
    """Call Claude via raw HTTP. Returns text or error message."""
    if not ANTHROPIC_API_KEY:
        return ""

    payload = json.dumps({
        "model": _CLAUDE_MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"__error__:{e.code}:{e.read().decode()[:200]}"
    except Exception as e:
        return f"__error__:{e}"


def _parse_json_from_llm(text: str):
    """Strip markdown fences and parse JSON from LLM response."""
    if not text or text.startswith("__error__"):
        return None
    t = text.strip()
    t = re.sub(r'^```(?:json)?\s*', '', t)
    t = re.sub(r'\s*```$', '', t)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return None


# ─── Company knowledge (from research) ────────────────────────────────────────

COMPANY_BEHAVIORAL_DATA = {
    "amazon": {
        "framework": "16 Leadership Principles",
        "format": "STAR stories — 2 LP questions per round, every round",
        "key_principles": [
            "Customer Obsession — Start with the customer, work backward",
            "Ownership — Never say 'that's not my job'",
            "Invent and Simplify — Drive innovation, reduce complexity",
            "Are Right, A Lot — Good judgment, seek diverse perspectives",
            "Bias for Action — Speed matters; calculated risk-taking",
            "Dive Deep — Stay connected to details, audit frequently",
            "Have Backbone; Disagree and Commit — Challenge respectfully then commit",
            "Deliver Results — Focus on key inputs, deliver with quality",
            "Earn Trust — Self-critical, benchmark against the best",
        ],
        "tips": [
            "Prepare 12–15 STAR stories mapping across multiple LPs",
            "Bar Raiser round = dedicated behavioral (most rigorous)",
            "Cover all 16 LPs including the 2 newer ones",
            "End every answer with the result and what you learned",
        ],
        "top_questions": [
            "Tell me about a time you had a conflict with a coworker",
            "Describe a project you owned end-to-end",
            "Tell me about your biggest professional failure",
            "How do you prioritize when you have multiple competing tasks?",
            "Describe a time you pushed back on a stakeholder",
            "Tell me about a time you solved a customer pain point",
            "Describe a time you went beyond your job scope",
        ],
        "tc_range": "INR 38–55 LPA (SDE-2) | 55–85 LPA (SDE-3)",
        "stack": "Java, Python, AWS, distributed systems",
    },
    "google": {
        "framework": "Googleyness (20–30% of evaluation)",
        "format": "5 rounds: 2 coding + 1 system design + 1 Googleyness + 1 general",
        "key_principles": [
            "Thriving in Ambiguity — Comfortable when things are undefined",
            "Valuing Feedback — Receive and act on feedback gracefully",
            "Challenging the Status Quo — Question assumptions productively",
            "Doing the Right Thing — Ethical decisions, user-first",
        ],
        "tips": [
            "Show growth mindset, humility, self-awareness about failures",
            "Take responsibility — don't blame others or circumstances",
            "Intellectual curiosity is a key signal at all levels",
            "L5 requires cross-team influence and technical leadership stories",
        ],
        "top_questions": [
            "Tell me about a time you worked in a highly ambiguous environment",
            "Describe a time you received harsh feedback. How did you respond?",
            "Tell me about the most challenging technical problem you solved",
            "What's a mistake you made that you'd handle differently today?",
            "Describe a time you challenged the status quo",
        ],
        "tc_range": "INR 55–88 LPA (L4) | 90–149 LPA (L5)",
        "stack": "Python, C++, Java, Go (language-agnostic in interviews)",
    },
    "stripe": {
        "framework": "Operating Principles (assessed in EVERY round)",
        "format": "8 rounds: phone screen + coding + system design + behavioral + team match",
        "key_principles": [
            "Clear Thinking & Communication — Muddled communication is a red flag",
            "User Empathy — How does your work affect developers using Stripe's APIs?",
            "Rigor Without Rigidity — Thorough but pragmatic; over-engineering is bad",
            "Humility & Intellectual Honesty — Admit uncertainty, ask good questions",
            "Bias Toward Impact — Prioritize high-impact work, ship effectively",
        ],
        "tips": [
            "Behavioral is NOT a separate round — assessed in EVERY round",
            "Written feedback on principles goes to hiring committee",
            "Writing culture — communicate with precision in technical discussions",
            "API design expertise is heavily tested",
        ],
        "top_questions": [
            "Tell me about a time you simplified a complex system or process",
            "Describe a time you made a technical decision with incomplete data",
            "How do you decide what NOT to build?",
            "Tell me about a time you had a conflict with a superior",
            "Describe a time you moved fast and broke something",
        ],
        "tc_range": "INR 45–80 LPA (estimated)",
        "stack": "Java, Ruby, JavaScript, Scala, Go; strong API design",
    },
    "flipkart": {
        "framework": "Ownership & Execution (startup speed at scale)",
        "format": "4–5 rounds: coding + system design + behavioral + hiring manager",
        "key_principles": [
            "Ownership — Take end-to-end responsibility for your feature/system",
            "Startup Speed at Scale — Execute fast even with 100M+ users",
            "Data-Driven Decisions — Back your choices with metrics",
            "Collaboration — Work well across teams in a complex org",
        ],
        "tips": [
            "Focus on e-commerce scale experience and system design",
            "Strong Java + Spring Boot + Kafka stack expected",
            "Demonstrate you can own features from ideation to production",
        ],
        "top_questions": [
            "Describe a project you owned end-to-end",
            "Tell me about debugging a complex production issue",
            "How did you improve a process or system significantly?",
            "Tell me about a time you used data to drive a decision",
            "Describe handling a production incident",
        ],
        "tc_range": "INR 30–44 LPA (SDE-2) | 55–70 LPA (SDE-3)",
        "stack": "Java, Spring Boot, microservices, Kafka",
    },
    "razorpay": {
        "framework": "Fintech Ownership (speed + domain + ownership)",
        "format": "3–4 rounds: coding + system design + behavioral",
        "key_principles": [
            "Deep Domain Knowledge — Understand payments, reconciliation, fintech",
            "Speed of Execution — Move fast in a high-stakes financial domain",
            "Ownership — Own reliability of financial transactions",
            "Technical Depth — Distributed transactions, idempotency, consistency",
        ],
        "tips": [
            "Know payments domain: UPI, reconciliation, idempotency, retry logic",
            "System design heavily focused on high-throughput transaction systems",
            "Go knowledge is a differentiator (alongside Java)",
        ],
        "top_questions": [
            "How would you design a payment reconciliation system?",
            "Tell me about a time you improved system reliability",
            "Describe handling distributed transaction failures",
            "How do you ensure idempotency in payment APIs?",
        ],
        "tc_range": "INR 26–43 LPA (SDE-2)",
        "stack": "Java, Go, Ruby, distributed systems, payments",
    },
    "phonepe": {
        "framework": "High-Throughput Ownership",
        "format": "3–4 rounds: DSA + system design + behavioral",
        "key_principles": [
            "Ownership Culture — Similar to Flipkart's intense ownership model",
            "High-Throughput Systems — Billions of transactions, zero downtime",
            "Technical Excellence — Spring Boot, Kafka, Redis mastery expected",
        ],
        "tips": [
            "Know Kafka consumer patterns, partition rebalancing, DLQ",
            "Redis caching patterns critical — understand eviction policies",
            "Show experience with high-concurrency Java",
        ],
        "top_questions": [
            "Design a high-throughput payment processing system",
            "How would you handle idempotency at scale?",
            "Tell me about a time you improved system performance",
            "Describe your experience with Kafka consumer group design",
        ],
        "tc_range": "INR 25–40 LPA (SDE-2)",
        "stack": "Java, Spring Boot, Kafka, Redis",
    },
    "swiggy": {
        "framework": "Execution Speed + Data-Driven",
        "format": "3–4 rounds: DSA + system design + behavioral",
        "key_principles": [
            "Execution Speed — Real-time logistics demands fast decision-making",
            "Data-Driven — Every decision backed by data/metrics",
            "Real-Time Systems — Low latency, high availability expertise",
        ],
        "tips": [
            "Real-time system design is the core differentiator",
            "Go knowledge valued alongside Java",
            "Show examples of data-driven optimization",
        ],
        "top_questions": [
            "Design a real-time delivery tracking system",
            "How would you optimize restaurant matching algorithms?",
            "Tell me about using data to drive a system improvement",
        ],
        "tc_range": "INR 25–38 LPA (SDE-2)",
        "stack": "Java, Go, real-time systems, microservices",
    },
    "cred": {
        "framework": "Design-First Culture",
        "format": "3–4 rounds with strong emphasis on design quality",
        "key_principles": [
            "Design Sensibility — Clean architecture, product taste expected",
            "Clean Code — Code quality is a first-class signal",
            "Product Thinking — Engineers contribute to product decisions",
        ],
        "tips": [
            "Kotlin preferred; strong Java also acceptable",
            "Show genuine interest in CRED's premium product experience",
            "Clean architecture patterns (SOLID, clean code) will be discussed",
        ],
        "top_questions": [
            "How would you design a credit card rewards system?",
            "Tell me about a system you refactored for clean architecture",
            "Describe a product decision you influenced as an engineer",
        ],
        "tc_range": "INR 25–40 LPA (estimated)",
        "stack": "Kotlin, Java, clean architecture",
    },
    "doordash": {
        "framework": "Engineering Values (Grit + Humility + Ownership)",
        "format": "Phone screen + coding + system design + behavioral + team match",
        "key_principles": [
            "Make Room at the Table — Inclusive leadership",
            "One Percent Better Every Day — Continuous improvement",
            "Grit & Humility — Persist through challenges; credit others",
            "Accountability & Ownership — Own failures, not just successes",
        ],
        "tips": [
            "Show genuine grit stories — times you pushed through failure",
            "DoorDash values humility — don't oversell individual achievement",
            "US-focused company; limited India roles",
        ],
        "top_questions": [
            "Tell me about a time you moved fast and broke something",
            "When did you push back on a stakeholder?",
            "Describe your biggest professional failure",
            "Tell me about leading a team through a difficult situation",
        ],
        "tc_range": "~$275K USD (E4)",
        "stack": "Kotlin, Java, Python, SQL, distributed systems",
    },
    "microsoft": {
        "framework": "Growth Mindset",
        "format": "4–5 rounds: coding + design + behavioral + hiring manager",
        "key_principles": [
            "Growth Mindset — Learn from failures; intellectual humility",
            "Cross-Team Collaboration — Work across diverse teams",
            "Customer Impact — How does your work affect end users?",
        ],
        "tips": [
            "Growth mindset stories valued above all else",
            "Azure ecosystem knowledge is a plus",
        ],
        "top_questions": [
            "Tell me about a time you failed and what you learned",
            "How do you juggle multiple projects with tight deadlines?",
            "Describe mentoring someone and what the outcome was",
        ],
        "tc_range": "INR 35–55 LPA (SDE-2)",
        "stack": "C#/.NET, Java, Python, Azure",
    },
    "bloomberg": {
        "framework": "Mission Fit + Communication = Technical",
        "format": "4–5 rounds; communication weighted EQUALLY to technical",
        "key_principles": [
            "Genuine Mission Interest — Financial data transparency matters",
            "Communication Clarity — Explain technical decisions precisely",
            "Legacy Code Respect — DO NOT criticize legacy C++",
            "Intellectual Rigor — Deep CS fundamentals required",
        ],
        "tips": [
            "NEVER mention competitor interviews — signals disinterest",
            "Show genuine passion for Bloomberg's financial data mission",
            "Communication is weighted equally to technical ability",
            "C++ proficiency (even basic) is a strong differentiator",
        ],
        "top_questions": [
            "Why do you want to work at Bloomberg specifically?",
            "Tell me about a technical decision you made and what failed",
            "How do you prioritize when you have multiple competing tasks?",
            "Describe debugging a complex production issue",
        ],
        "tc_range": "$204K–$316K USD",
        "stack": "C++ (primary), Java, Python; financial data systems",
    },
}

# Universal behavioral questions (when company not found)
UNIVERSAL_BEHAVIORAL_QUESTIONS = [
    "Tell me about the most challenging technical problem you solved",
    "Describe a time you had a conflict with a coworker",
    "Tell me about your biggest professional failure",
    "How do you prioritize when you have multiple competing tasks?",
    "Describe a project you owned end-to-end",
    "Tell me about a time you made a wrong technical decision",
    "Describe a time you worked in a highly ambiguous environment",
    "Tell me about a time you led a team through a difficult situation",
    "Describe a time you had to influence others without direct authority",
    "Tell me about a time you moved fast and broke something",
]


# ─── Prep time estimation ──────────────────────────────────────────────────────

_SKILL_PREP_HOURS = {
    "kafka": 12, "system design": 20, "distributed systems": 20,
    "java": 15, "spring boot": 10, "spring": 10,
    "redis": 8, "sql": 8, "database": 8,
    "kubernetes": 10, "docker": 6,
    "golang": 15, "go": 15, "python": 10,
    "lld": 15, "low level design": 15,
    "behavioral": 8, "data structures": 12, "algorithms": 12,
    "dsa": 12, "multithreading": 10, "concurrency": 10,
    "microservices": 8, "api design": 6, "rest": 4,
    "kafka consumer": 8, "kafka producer": 6,
}

def _estimate_prep_hours(skill: str, gap: int) -> int:
    """Estimate prep hours for a skill based on the gap size."""
    base = _SKILL_PREP_HOURS.get(skill.lower(), 8)
    multiplier = gap / 10.0
    return max(1, round(base * multiplier))


# ─── Phase 1: Extract skills + predict questions ───────────────────────────────

def extract_skills_from_jd(jd_text: str, company: str, role: str = "SDE") -> dict:
    """
    Extract technical skills from a JD using Claude (or return empty if no API key).

    Returns:
        {
            "required_skills": [{"name": "Kafka", "importance": 9, "context": "..."}],
            "preferred_skills": [...],
            "years_experience": 5,
            "key_technologies": {"Kafka": 9, "Java": 8},
            "estimated_difficulty": "senior",
            "estimated_prep_hours": 80
        }
    """
    prompt = f"""You are an expert technical recruiter analyzing job descriptions.

Extract and analyze skills from this {company} {role} JD:

{jd_text[:4000]}

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "required_skills": [
    {{"name": "Kafka", "importance": 9, "context": "Stream processing for 1M events/day"}},
    {{"name": "Java", "importance": 8, "context": "Main backend language"}},
    {{"name": "System Design", "importance": 9, "context": "Scale to 1M RPS"}}
  ],
  "preferred_skills": [
    {{"name": "Golang", "importance": 6}},
    {{"name": "Kubernetes", "importance": 5}}
  ],
  "years_experience": 5,
  "key_technologies": {{"Kafka": 9, "Java": 8, "System Design": 9}},
  "estimated_difficulty": "senior",
  "estimated_prep_hours": 80
}}"""

    raw = _call_claude(prompt, max_tokens=1500)
    parsed = _parse_json_from_llm(raw)

    if parsed and isinstance(parsed, dict):
        return parsed

    # Fallback: keyword-based extraction when no API key
    return _extract_skills_keyword_fallback(jd_text, company)


def _extract_skills_keyword_fallback(jd_text: str, company: str) -> dict:
    """Keyword-based skill extraction when LLM is unavailable."""
    text_lower = jd_text.lower()
    skill_keywords = {
        "Java": 9, "Spring Boot": 8, "Spring": 7, "Kafka": 8,
        "Redis": 7, "SQL": 7, "MySQL": 7, "PostgreSQL": 7, "MongoDB": 6,
        "Kubernetes": 6, "Docker": 6, "AWS": 7, "GCP": 6,
        "Python": 7, "Golang": 7, "Go": 6,
        "System Design": 9, "Distributed Systems": 8,
        "Microservices": 7, "REST API": 6, "gRPC": 6,
        "LLD": 7, "Multithreading": 7, "Concurrency": 7,
        "DSA": 8, "Algorithms": 7,
    }
    found_required = []
    key_techs = {}
    for skill, importance in skill_keywords.items():
        if skill.lower() in text_lower:
            found_required.append({"name": skill, "importance": importance, "context": ""})
            key_techs[skill] = importance

    years = 3
    for m in re.findall(r'(\d+)\+?\s*years?', jd_text):
        years = max(years, int(m))

    return {
        "required_skills": found_required[:10],
        "preferred_skills": [],
        "years_experience": years,
        "key_technologies": key_techs,
        "estimated_difficulty": "senior" if years >= 5 else "mid",
        "estimated_prep_hours": 60,
    }


def predict_interview_questions(jd_text: str, company: str, required_skills: list) -> dict:
    """
    Predict 15–20 interview questions from the JD.

    Returns:
        {
            "system_design": [{"q": "...", "importance": 9, "topics": [...]}],
            "behavioral": [...],
            "technical": [...]
        }
    """
    skills_str = ", ".join([
        (s["name"] if isinstance(s, dict) else s)
        for s in required_skills[:5]
    ])

    prompt = f"""For this {company} JD requiring {skills_str}:

{jd_text[:3000]}

Predict 15-20 interview questions they WILL ask.
Return ONLY valid JSON:
{{
  "system_design": [
    {{"q": "Design Kafka-based event streaming for 1M events/day", "importance": 9, "topics": ["kafka", "scalability"]}},
    {{"q": "How would you handle 1M RPS?", "importance": 8, "topics": ["scalability", "load-balancing"]}}
  ],
  "behavioral": [
    {{"q": "Tell about handling a production incident", "importance": 8, "topics": ["problem-solving"]}},
    {{"q": "Conflict with a team member?", "importance": 7, "topics": ["teamwork"]}}
  ],
  "technical": [
    {{"q": "Explain distributed transactions", "importance": 8, "topics": ["transactions"]}},
    {{"q": "Java concurrent collections?", "importance": 6, "topics": ["java"]}}
  ],
  "lld": [
    {{"q": "Design a Rate Limiter", "importance": 8, "topics": ["lld", "design-patterns"]}}
  ]
}}"""

    raw = _call_claude(prompt, max_tokens=2000)
    parsed = _parse_json_from_llm(raw)

    if parsed and isinstance(parsed, dict):
        return parsed

    # Fallback: company-based questions from our data
    return _predict_questions_fallback(company, required_skills)


def _predict_questions_fallback(company: str, required_skills: list) -> dict:
    """Return relevant predicted questions when LLM unavailable."""
    company_lower = company.lower()
    behavioral_qs = []
    for c_key, c_data in COMPANY_BEHAVIORAL_DATA.items():
        if c_key in company_lower or company_lower in c_key:
            behavioral_qs = [
                {"q": q, "importance": 8, "topics": ["behavioral"]}
                for q in c_data.get("top_questions", [])
            ]
            break

    if not behavioral_qs:
        behavioral_qs = [
            {"q": q, "importance": 7, "topics": ["behavioral"]}
            for q in UNIVERSAL_BEHAVIORAL_QUESTIONS[:5]
        ]

    skill_names = [
        s["name"] if isinstance(s, dict) else s
        for s in required_skills[:3]
    ]

    sd_questions = [
        {"q": f"Design a scalable {skill_names[0] if skill_names else 'backend'} system",
         "importance": 9, "topics": ["system-design"]},
        {"q": "Design a URL shortener at scale", "importance": 7, "topics": ["system-design"]},
        {"q": "Design a distributed rate limiter", "importance": 8, "topics": ["system-design"]},
    ]
    tech_questions = [
        {"q": f"Explain {skill} internals and best practices", "importance": 7, "topics": [skill.lower()]}
        for skill in skill_names[:3]
    ]

    return {
        "system_design": sd_questions,
        "behavioral": behavioral_qs,
        "technical": tech_questions,
        "lld": [
            {"q": "Design a Parking Lot system", "importance": 8, "topics": ["lld"]},
            {"q": "Design a Notification System", "importance": 7, "topics": ["lld"]},
        ],
    }


def store_jd(jd_id: str, company: str, role: str, level: str, jd_text: str,
             extracted_data: dict, predicted_questions: dict = None) -> dict:
    """Store JD + extracted skills + predicted questions in database."""
    from .db import get_conn

    conn = get_conn()
    try:
        required_skills = extracted_data.get("required_skills", [])
        preferred_skills = extracted_data.get("preferred_skills", [])
        key_techs = extracted_data.get("key_technologies", {})

        conn.execute("""
            INSERT OR REPLACE INTO jd_descriptions
            (id, company, role, level, raw_jd, required_skills, preferred_skills,
             skill_depth_required, estimated_difficulty, years_experience,
             predicted_questions, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            jd_id, company, role, level, jd_text[:8000],
            json.dumps([s.get("name") if isinstance(s, dict) else s for s in required_skills]),
            json.dumps([s.get("name") if isinstance(s, dict) else s for s in preferred_skills]),
            json.dumps(key_techs),
            extracted_data.get("estimated_difficulty", "unknown"),
            extracted_data.get("years_experience", 0),
            json.dumps(predicted_questions or {}),
            str(datetime.now()),
        ))

        # Per-skill analysis rows
        for skill in required_skills:
            skill_name = skill.get("name") if isinstance(skill, dict) else skill
            importance = skill.get("importance", 5) if isinstance(skill, dict) else 5
            context = skill.get("context", "") if isinstance(skill, dict) else ""
            conn.execute("""
                INSERT OR REPLACE INTO jd_skill_analysis
                (jd_id, skill_name, importance_score, depth_required, typical_questions, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                jd_id, skill_name, float(importance), int(importance),
                json.dumps([context] if context else []),
                str(datetime.now()),
            ))

        conn.commit()
        return {"success": True, "jd_id": jd_id}

    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def get_jd(jd_id: str):
    """Retrieve a stored JD and its analysis."""
    from .db import get_conn

    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM jd_descriptions WHERE id = ?", (jd_id,)
        ).fetchone()
        if not row:
            return None

        jd = dict(row)
        for field in ("required_skills", "preferred_skills", "skill_depth_required"):
            jd[field] = json.loads(jd.get(field) or "[]" if field != "skill_depth_required" else "{}")
        jd["predicted_questions"] = json.loads(jd.get("predicted_questions") or "{}")

        skill_rows = conn.execute(
            "SELECT * FROM jd_skill_analysis WHERE jd_id = ? ORDER BY importance_score DESC",
            (jd_id,)
        ).fetchall()
        jd["skill_analysis"] = [dict(r) for r in skill_rows]
        return jd
    finally:
        conn.close()


def get_jd_skills(jd_id: str) -> dict:
    """Return {skill_name: importance} for a JD."""
    from .db import get_conn

    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT skill_depth_required FROM jd_descriptions WHERE id = ?", (jd_id,)
        ).fetchone()
        return json.loads(row[0] or "{}") if row else {}
    finally:
        conn.close()


def list_jds(company: str = None, limit: int = 20) -> list:
    """List stored JDs."""
    from .db import get_conn

    conn = get_conn()
    try:
        if company:
            rows = conn.execute(
                "SELECT id, company, role, level, estimated_difficulty, years_experience, created_at "
                "FROM jd_descriptions WHERE LOWER(company) LIKE ? ORDER BY created_at DESC LIMIT ?",
                (f"%{company.lower()}%", limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, company, role, level, estimated_difficulty, years_experience, created_at "
                "FROM jd_descriptions ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ─── Phase 2: Skill Gap Analysis ──────────────────────────────────────────────

def analyze_skill_gap(jd_id: str, user_skills: dict) -> dict:
    """
    Compare user's skill levels vs JD requirements.

    user_skills: {"Kafka": 6, "Java": 8, "System Design": 5} (scale 1-10)

    Returns readiness %, per-skill gaps, priority focus, and behavioral guide.
    """
    from .db import get_conn

    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT company, role, level, skill_depth_required, required_skills FROM jd_descriptions WHERE id = ?",
            (jd_id,)
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return {"error": f"JD not found: {jd_id}"}

    company = row["company"]
    role = row["role"]
    jd_required = json.loads(row["skill_depth_required"] or "{}")

    # Case-insensitive user skills lookup
    user_skills_normalized = {k.lower(): v for k, v in user_skills.items()}

    gaps = {}
    for skill, required in jd_required.items():
        current = user_skills_normalized.get(skill.lower(), 0)
        gap = max(0, required - current)
        prep_h = _estimate_prep_hours(skill, gap)

        if gap == 0:
            status = "strong"
        elif gap <= 2:
            status = "minor_gap"
        elif gap <= 4:
            status = "moderate_gap"
        else:
            status = "critical_gap"

        gaps[skill] = {
            "skill": skill,
            "required": required,
            "current": current,
            "gap": gap,
            "status": status,
            "prep_hours": prep_h,
        }

    total = len(gaps) or 1
    ready_count = sum(1 for g in gaps.values() if g["status"] == "strong")
    partial_count = sum(1 for g in gaps.values() if g["status"] == "minor_gap")

    # Weighted readiness: strong = 1.0, minor_gap = 0.7, moderate = 0.4, critical = 0
    weighted = sum(
        1.0 if g["status"] == "strong"
        else 0.7 if g["status"] == "minor_gap"
        else 0.4 if g["status"] == "moderate_gap"
        else 0.1
        for g in gaps.values()
    )
    readiness_pct = round((weighted / total) * 100)

    priority_focus = sorted(gaps.values(), key=lambda x: x["gap"], reverse=True)[:5]
    total_prep_hours = sum(g["prep_hours"] for g in gaps.values())

    # Get company behavioral guide
    behavioral_guide = get_behavioral_guide(company)

    return {
        "jd_id": jd_id,
        "company": company,
        "role": role,
        "overall_readiness": readiness_pct,
        "interview_ready": readiness_pct >= 75,
        "skill_gaps": gaps,
        "priority_focus": priority_focus,
        "total_prep_hours": total_prep_hours,
        "behavioral_guide": behavioral_guide,
        "summary": _generate_gap_summary(company, readiness_pct, priority_focus),
    }


def _generate_gap_summary(company: str, readiness: int, priority_focus: list) -> str:
    """Generate a text summary of the gap analysis."""
    top_gap = priority_focus[0]["skill"] if priority_focus else "N/A"
    if readiness >= 80:
        return f"You're interview-ready for {company}! Focus on sharpening {top_gap} for maximum impact."
    elif readiness >= 60:
        return f"Good foundation for {company}. Bridge the {top_gap} gap first — it's your highest-priority skill."
    elif readiness >= 40:
        return f"You're {100-readiness}% away from {company} readiness. Start with {top_gap} — it's critical for this role."
    else:
        return f"Significant gaps remain for {company}. Focus on {top_gap} immediately. This will take 4–6 weeks of focused prep."


# ─── Phase 3: Prep Roadmap Generation ─────────────────────────────────────────

_WEEK_THEMES = {
    1: "Foundations & Highest Priority Gaps",
    2: "Core Technical Depth",
    3: "System Design Mastery",
    4: "Mock Interviews & Polish",
    5: "Advanced Topics & Company-Specific",
    6: "Full Practice Mode",
}

_SKILL_RESOURCES = {
    "kafka": ["Kafka: The Definitive Guide (free PDF)", "Learn partitions, consumer groups, DLQ", "Build a simple producer/consumer in Java"],
    "system design": ["Alex Xu System Design Vol 1 & 2", "Practice: URL shortener, notification system, rate limiter", "Draw architecture diagrams before looking at solutions"],
    "java": ["Java Concurrency in Practice", "Practice: multithreading, collections, streams", "LeetCode in Java (use Java-specific APIs)"],
    "spring boot": ["Spring Boot docs", "Build a REST API with Spring Security", "Practice: beans, DI, profiles, actuator"],
    "redis": ["Redis in Action book", "Practice: caching patterns, pub/sub, sorted sets", "Implement LRU cache using Redis"],
    "distributed systems": ["Designing Data-Intensive Applications (DDIA)", "Study: CAP theorem, consensus (Raft/Paxos basics), CRDTs", "Practice: distributed transactions, idempotency"],
    "lld": ["Refactoring.Guru design patterns", "Practice: Parking Lot, Chess, BookMyShow, Elevator, Cache, Rate Limiter", "Apply SOLID principles to your designs"],
    "dsa": ["NeetCode 150 in Java", "Focus: Trees, Graphs, DP, Binary Search, Sliding Window", "1 problem/day minimum"],
    "golang": ["Tour of Go (official)", "Practice goroutines, channels, context, select", "Implement a simple HTTP server in Go"],
    "behavioral": ["Prepare 12-15 STAR stories", "Map stories to company-specific frameworks", "Record yourself and review for clarity"],
    "sql": ["SQL practice on LeetCode", "Study: indexes, query optimization, explain plans", "Practice: complex joins, window functions, CTEs"],
    "kubernetes": ["Kubernetes in Action book", "Deploy a simple app with K8s locally", "Study: pods, services, deployments, HPA"],
}

def generate_prep_roadmap(jd_id: str, user_skills: dict, weeks: int = 4) -> dict:
    """
    Generate a week-by-week personalized prep roadmap.

    user_skills: {"Kafka": 6, "Java": 8} — same as gap analysis input
    weeks: 2–8 weeks available for prep
    """
    gap_result = analyze_skill_gap(jd_id, user_skills)
    if "error" in gap_result:
        return gap_result

    company = gap_result["company"]
    role = gap_result["role"]
    gaps = gap_result["skill_gaps"]
    priority_focus = gap_result["priority_focus"]

    # Sort all skills by gap (critical first)
    all_gaps_sorted = sorted(gaps.values(), key=lambda x: x["gap"], reverse=True)

    # Distribute skills across weeks
    skills_per_week = max(1, len(all_gaps_sorted) // weeks)
    weekly_plans = []

    for week_num in range(1, weeks + 1):
        is_last_week = week_num == weeks
        week_skills = all_gaps_sorted[(week_num - 1) * skills_per_week: week_num * skills_per_week]

        if is_last_week:
            # Last week = mock + polish
            weekly_plans.append({
                "week": week_num,
                "theme": "Mock Interviews & Final Polish",
                "focus": "PRACTICE MODE",
                "topics": [
                    {
                        "skill": "Mock Interviews",
                        "goal": "2-3 full mock rounds (DSA + System Design + Behavioral)",
                        "hours": 8,
                        "resources": ["Pramp (free)", "interviewing.io", "Study partner"],
                    },
                    {
                        "skill": "Weak Area Review",
                        "goal": f"Revisit your biggest gaps: {', '.join(g['skill'] for g in priority_focus[:2])}",
                        "hours": 6,
                        "resources": ["Review your notes", "1-2 timed LeetCode problems per day"],
                    },
                ],
                "daily_target": "1 mock interview + 1 LeetCode problem",
                "lc_target": 5,
                "behavioral_prep": True,
            })
        else:
            topics = []
            for g in week_skills:
                skill_lower = g["skill"].lower()
                resources = _SKILL_RESOURCES.get(skill_lower, [
                    f"Study {g['skill']} fundamentals",
                    f"Practice {g['skill']} problems on LeetCode",
                    f"Build a small project using {g['skill']}",
                ])
                topics.append({
                    "skill": g["skill"],
                    "goal": f"Close {g['gap']}-level gap (current: {g['current']}/10 → target: {g['required']}/10)",
                    "hours": g["prep_hours"],
                    "status": g["status"],
                    "resources": resources[:3],
                })

            weekly_plans.append({
                "week": week_num,
                "theme": _WEEK_THEMES.get(week_num, f"Deep Dive Week {week_num}"),
                "focus": week_skills[0]["skill"] if week_skills else "Review",
                "topics": topics,
                "daily_target": "2h focused study + 1 LeetCode problem",
                "lc_target": 7,
                "behavioral_prep": week_num >= max(1, weeks - 1),
            })

    total_hours = sum(
        sum(t["hours"] for t in w["topics"])
        for w in weekly_plans
    )

    return {
        "jd_id": jd_id,
        "company": company,
        "role": role,
        "weeks": weeks,
        "overall_readiness": gap_result["overall_readiness"],
        "total_prep_hours": total_hours,
        "weekly_plans": weekly_plans,
        "top_priorities": [g["skill"] for g in priority_focus[:3]],
        "interview_ready_by": f"Week {weeks}",
        "behavioral_framework": COMPANY_BEHAVIORAL_DATA.get(
            company.lower(), {}
        ).get("framework", "Universal STAR method"),
    }


# ─── Behavioral Guide ─────────────────────────────────────────────────────────

def get_behavioral_guide(company: str) -> dict:
    """Return company-specific behavioral framework."""
    company_lower = company.lower()

    # Try exact or partial match
    for key, data in COMPANY_BEHAVIORAL_DATA.items():
        if key in company_lower or company_lower in key:
            return {
                "company": company,
                "matched_framework": key,
                **data,
            }

    # Default
    return {
        "company": company,
        "matched_framework": "universal",
        "framework": "Universal STAR Method",
        "format": "STAR: Situation, Task, Action, Result + Learning",
        "key_principles": [
            "Ownership — Take responsibility for outcomes",
            "Impact — Quantify your contributions",
            "Growth — Show what you learned from failures",
            "Collaboration — Demonstrate teamwork",
        ],
        "tips": [
            "Prepare 12-15 STAR stories covering multiple scenarios",
            "Every answer should end with measurable results",
            "Show both technical depth AND soft skills",
        ],
        "top_questions": UNIVERSAL_BEHAVIORAL_QUESTIONS,
        "tc_range": "Varies",
        "stack": "Varies",
    }
