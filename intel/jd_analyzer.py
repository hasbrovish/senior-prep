"""
JD Analyzer: Extract skills, requirements, and predict interview topics from job descriptions.
Uses Claude LLM for intelligent skill extraction and analysis.
"""

import json
import os
from datetime import datetime
from anthropic import Anthropic

client = Anthropic()


def extract_skills_from_jd(jd_text: str, company: str, role: str = "SDE") -> dict:
    """
    Extract technical skills from a job description using Claude.

    Returns:
        {
            "required_skills": [
                {"name": "Kafka", "importance": 9, "context": "..."},
                ...
            ],
            "preferred_skills": [...],
            "years_experience": 5,
            "key_technologies": {"Kafka": 9, "Java": 7, "Spring": 6}
        }
    """

    prompt = f"""You are an expert technical recruiter analyzing job descriptions.

Extract and analyze skills from this {company} {role} JD:

{jd_text}

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

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.content[0].text.strip()
        # Remove markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]

        return json.loads(result_text.strip())
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse skill extraction response: {e}")
        return {
            "required_skills": [],
            "preferred_skills": [],
            "key_technologies": {},
            "years_experience": 0,
            "estimated_difficulty": "unknown"
        }
    except Exception as e:
        print(f"❌ Error extracting skills: {e}")
        raise


def predict_interview_questions(jd_text: str, company: str, required_skills: list) -> dict:
    """
    Predict 15-20 interview questions likely to be asked based on the JD.

    Returns:
        {
            "system_design": [
                {"q": "Design...", "importance": 9, "topics": ["kafka", "scalability"]},
                ...
            ],
            "behavioral": [...],
            "technical": [...]
        }
    """

    skills_str = ", ".join([s["name"] if isinstance(s, dict) else s for s in required_skills[:5]])

    prompt = f"""For this {company} JD requiring {skills_str}:

{jd_text}

Predict 15-20 interview questions they WILL ask.

Return ONLY valid JSON:
{{
  "system_design": [
    {{"q": "Design Kafka-based event streaming system for 1M events/day", "importance": 9, "topics": ["kafka", "scalability", "throughput"]}},
    {{"q": "How would you handle 1M RPS?", "importance": 8, "topics": ["scalability", "load-balancing"]}}
  ],
  "behavioral": [
    {{"q": "Tell about handling a production incident", "importance": 8, "topics": ["problem-solving", "communication"]}},
    {{"q": "Conflict with team member?", "importance": 7, "topics": ["teamwork"]}}
  ],
  "technical": [
    {{"q": "Explain distributed transactions", "importance": 8, "topics": ["transactions", "consistency"]}},
    {{"q": "Java collections framework?", "importance": 6, "topics": ["java", "data-structures"]}}
  ],
  "estimated_prep_time_hours": 80
}}"""

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.content[0].text.strip()
        # Remove markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]

        return json.loads(result_text.strip())
    except Exception as e:
        print(f"❌ Error predicting questions: {e}")
        return {
            "system_design": [],
            "behavioral": [],
            "technical": [],
            "estimated_prep_time_hours": 0
        }


def store_jd(jd_id: str, company: str, role: str, level: str, jd_text: str,
             extracted_data: dict) -> dict:
    """Store JD and extracted skills in database."""
    from .db import get_conn
    from datetime import date

    conn = get_conn()

    try:
        # Insert JD description
        required_skills = extracted_data.get("required_skills", [])
        preferred_skills = extracted_data.get("preferred_skills", [])
        key_techs = extracted_data.get("key_technologies", {})

        conn.execute("""
            INSERT OR REPLACE INTO jd_descriptions
            (id, company, role, level, raw_jd, required_skills, preferred_skills,
             skill_depth_required, estimated_difficulty, years_experience, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            jd_id,
            company,
            role,
            level,
            jd_text,
            json.dumps([s.get("name") if isinstance(s, dict) else s for s in required_skills]),
            json.dumps([s.get("name") if isinstance(s, dict) else s for s in preferred_skills]),
            json.dumps(key_techs),
            extracted_data.get("estimated_difficulty", "unknown"),
            extracted_data.get("years_experience", 0),
            str(datetime.now()),
        ))

        # Insert per-skill analysis
        for skill in required_skills:
            skill_name = skill.get("name") if isinstance(skill, dict) else skill
            importance = skill.get("importance", 5) if isinstance(skill, dict) else 5
            context = skill.get("context", "") if isinstance(skill, dict) else ""

            conn.execute("""
                INSERT INTO jd_skill_analysis
                (jd_id, skill_name, importance_score, depth_required, typical_questions, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                jd_id,
                skill_name,
                float(importance),
                int(importance),
                json.dumps([context]) if context else json.dumps([]),
                str(datetime.now()),
            ))

        conn.commit()
        return {"success": True, "jd_id": jd_id}

    except Exception as e:
        conn.rollback()
        print(f"❌ Error storing JD: {e}")
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def get_jd(jd_id: str) -> dict:
    """Retrieve a stored JD and its analysis."""
    from .db import get_conn

    conn = get_conn()

    try:
        row = conn.execute(
            "SELECT * FROM jd_descriptions WHERE id = ?",
            (jd_id,)
        ).fetchone()

        if not row:
            return None

        jd_data = dict(row)

        # Parse JSON fields
        jd_data["required_skills"] = json.loads(jd_data.get("required_skills", "[]"))
        jd_data["preferred_skills"] = json.loads(jd_data.get("preferred_skills", "[]"))
        jd_data["skill_depth_required"] = json.loads(jd_data.get("skill_depth_required", "{}"))

        # Get skill analysis
        skill_rows = conn.execute(
            "SELECT * FROM jd_skill_analysis WHERE jd_id = ? ORDER BY importance_score DESC",
            (jd_id,)
        ).fetchall()

        jd_data["skill_analysis"] = [dict(r) for r in skill_rows]

        return jd_data

    finally:
        conn.close()


def get_jd_skills(jd_id: str) -> dict:
    """Get skill depth required for a JD."""
    from .db import get_conn

    conn = get_conn()

    try:
        row = conn.execute(
            "SELECT skill_depth_required FROM jd_descriptions WHERE id = ?",
            (jd_id,)
        ).fetchone()

        if not row:
            return {}

        return json.loads(row[0] or "{}")

    finally:
        conn.close()


def list_jds(company: str = None, limit: int = 20) -> list:
    """List all stored JDs, optionally filtered by company."""
    from .db import get_conn

    conn = get_conn()

    try:
        if company:
            rows = conn.execute(
                "SELECT * FROM jd_descriptions WHERE LOWER(company) LIKE ? ORDER BY created_at DESC LIMIT ?",
                (f"%{company.lower()}%", limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM jd_descriptions ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()

        return [dict(r) for r in rows]

    finally:
        conn.close()
