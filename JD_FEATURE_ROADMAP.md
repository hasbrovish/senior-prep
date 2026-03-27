# JD Analysis Feature — Implementation Roadmap

## 🎯 What We're Building

**Goal:** Transform generic prep → JD-driven, targeted interview prep

```
User uploads JD → System extracts skills → Shows gap vs your skills →
Predicts questions → Generates personalized roadmap → Mock interview practice
```

---

## 📊 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ User: Pastes Amazon SDE2 JD                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Backend: Extract Skills (LLM)                               │
│ → "Kafka", "System Design", "Java", "Spring"                │
│ → Required depth: Kafka(9/10), Java(7/10)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Backend: Predict Questions (LLM + Historical Data)          │
│ → "Design Kafka system for 1M events/day"                   │
│ → "Explain distributed transactions"                        │
│ → "Amazon LP behavioral questions"                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Frontend: Show Results                                      │
│ ├─ Skill gap (you vs JD)                                   │
│ ├─ Predicted questions                                      │
│ ├─ 4-week prep roadmap                                     │
│ └─ Link to practice drills for weak areas                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Implementation Phases

### Phase 1: JD Storage & Extraction (1 week)

**What to build:**
1. Database table for JDs
2. JD upload API endpoint
3. Skill extraction logic
4. Store results

**Files to create/modify:**

```
intel/
├── jd_analyzer.py (NEW)         # Extract skills from JD text
│   └─ extract_skills_from_jd()
│   └─ analyze_skill_depth()
│   └─ predict_interview_topics()
│
├── db.py (MODIFY)
│   └─ Add: jd_descriptions, jd_skill_analysis tables
│
└── intelligence.py (MODIFY)
    └─ Add JD-related functions

app/routers/
└── intelligence.py (NEW)
    └─ POST /jd/upload
    └─ GET /jd/{jd_id}/skills
    └─ GET /jd/{jd_id}/analysis
```

**Example: skill extraction logic**

```python
# intel/jd_analyzer.py

async def extract_skills_from_jd(jd_text: str, company: str):
    """Extract required/preferred skills from JD text"""

    prompt = f"""
    Extract technical skills from this JD for {company}:

    {jd_text}

    Return JSON:
    {{
      "required_skills": ["Kafka", "Java", "SQL"],
      "preferred_skills": ["Golang", "Kubernetes"],
      "years_experience": 5,
      "key_technologies": {{"Kafka": 9, "Java": 7, "Spring": 6}}
    }}
    """

    response = await claude.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.content[0].text)
```

**Database schema:**

```sql
CREATE TABLE jd_descriptions (
    id TEXT PRIMARY KEY,
    company TEXT,
    role TEXT,
    level TEXT,
    raw_jd TEXT,
    required_skills TEXT,      -- JSON: ["Kafka", "Java"]
    preferred_skills TEXT,
    skill_depth_required TEXT, -- JSON: {"Kafka": 9, "Java": 7}
    estimated_difficulty TEXT, -- "senior"
    created_at TEXT
);

CREATE TABLE jd_skill_analysis (
    id TEXT PRIMARY KEY,
    jd_id TEXT,
    skill_name TEXT,
    importance_score FLOAT,    -- 1-10
    frequency INT,
    typical_questions TEXT,    -- JSON: ["How to partition?"]
    depth_required INT,
    created_at TEXT
);
```

---

### Phase 2: Skill Gap & Question Prediction (1 week)

**What to build:**
1. Compare user skills vs JD requirements
2. Predict likely interview questions
3. Get historical questions for skills

**Files to modify:**

```
intel/
└── jd_analyzer.py
    └─ def analyze_skill_gap(user_skills, jd_skills)
    └─ def predict_interview_questions(jd_text, company)
    └─ def get_historical_questions(skill_name)

app/routers/
└── intelligence.py
    └─ POST /jd/{jd_id}/gap-analysis
    └─ GET /jd/{jd_id}/predicted-questions
    └─ GET /intel/questions-by-skill/{skill}
```

**Example: Gap analysis**

```python
@router.post("/jd/{jd_id}/gap-analysis")
async def analyze_gap(jd_id: str, user_skills: dict):
    """
    Input: {
      "java": 7,        # Your skill level 1-10
      "kafka": 5,
      "system_design": 6
    }
    """
    jd = get_jd(jd_id)
    jd_skills = get_jd_skills(jd_id)

    gaps = {}
    for skill, required_depth in jd_skills.items():
        your_depth = user_skills.get(skill, 0)
        gap = required_depth - your_depth

        gaps[skill] = {
            "skill": skill,
            "required": required_depth,
            "current": your_depth,
            "gap": max(0, gap),
            "status": "Strong ✅" if gap <= 0 else f"Gap: {gap} levels",
            "prep_time": _estimate_prep_hours(skill, gap)
        }

    readiness = sum(1 for g in gaps.values() if g['gap'] <= 0) / len(gaps)

    return {
        "overall_readiness": f"{readiness * 100:.0f}%",
        "interview_ready": readiness >= 0.8,
        "skill_gaps": gaps,
        "priority_focus": sorted(
            gaps.values(),
            key=lambda x: x['gap'],
            reverse=True
        )[:5],
        "estimated_prep_time": f"{sum(g['prep_time'] for g in gaps.values())} hours"
    }
```

**Example: Predict questions**

```python
async def predict_interview_questions(jd_text: str, company: str) -> dict:
    """Predict what they'll ask based on JD"""

    prompt = f"""
    For this {company} JD:

    {jd_text}

    Predict 15 interview questions they will ask.
    Format: {{
      "system_design": [
        {{"q": "Design...", "importance": 9}},
      ],
      "behavioral": [...],
      "technical": [...]
    }}
    """

    response = await claude.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.content[0].text)
```

---

### Phase 3: Roadmap Generation (1 week)

**What to build:**
1. Generate week-by-week prep plan
2. Link to specific drills/problems
3. Prioritize based on gaps

**Files to create:**

```
intel/
└── roadmap_generator.py (NEW)
    └─ def generate_prep_roadmap(jd_id, weeks_available)
    └─ def get_weekly_targets(skills, week_num)

app/routers/
└── intelligence.py
    └─ POST /jd/{jd_id}/roadmap
    └─ GET /jd/{jd_id}/roadmap/week/{week_num}
```

**Example: Generate roadmap**

```python
def generate_prep_roadmap(jd_id: str, weeks: int = 4) -> dict:
    """Create personalized week-by-week prep plan"""

    jd = get_jd(jd_id)
    gaps = analyze_gap(jd_id, get_user_skills())

    roadmap = {
        "company": jd.company,
        "role": jd.role,
        "weeks": weeks,
        "weekly_plans": []
    }

    # Prioritize skills with largest gaps
    priority_skills = sorted(
        gaps.items(),
        key=lambda x: x['gap'],
        reverse=True
    )

    for week_num in range(1, weeks + 1):
        week_plan = {
            "week": week_num,
            "theme": _get_week_theme(week_num, priority_skills),
            "topics": _generate_topics_for_week(
                week_num,
                priority_skills,
                weeks
            ),
            "practice": _get_practice_drills(week_plan['topics']),
            "mock_interview": week_num == weeks,
            "target": _get_week_target(week_num)
        }
        roadmap["weekly_plans"].append(week_plan)

    return roadmap

# Example output:
{
  "week_1": {
    "theme": "Foundations",
    "topics": [
      {"skill": "Kafka", "depth": "Learn partitions, consumer groups", "hours": 8},
      {"skill": "Java", "depth": "Review concurrency basics", "hours": 6}
    ],
    "practice": [
      {"problem": "Implement a queue", "platform": "LeetCode"},
      {"problem": "Design a simple pub/sub", "type": "system_design"}
    ]
  }
}
```

---

### Phase 4: Portal UI (1 week)

**What to build:**
1. JD upload component
2. Gap analysis visualization
3. Roadmap display
4. Question bank viewer

**Files to create:**

```
ui/src/pages/
├── JobAnalysis.jsx (NEW)        # Main JD upload & analysis
│   ├─ JDUploadForm
│   ├─ SkillGapChart
│   ├─ PredictedQuestions
│   └─ PrepRoadmap
│
└── SkillIntelligence.jsx (NEW) # Trending skills + deep dives
    ├─ SkillSearch
    ├─ TrendingSkills
    └─ QuestionBank
```

**Example: Job Analysis page**

```jsx
// ui/src/pages/JobAnalysis.jsx

export default function JobAnalysis() {
  const [jd, setJd] = useState('');
  const [company, setCompany] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    const result = await api.post('/jd/upload', {
      jd_text: jd,
      company: company,
      role: document.getElementById('role').value
    });
    setAnalysis(result);
    setLoading(false);
  };

  return (
    <div className="page">
      <h2>Job Description Analysis</h2>

      {!analysis ? (
        <div className="card">
          <textarea
            placeholder="Paste job description here..."
            value={jd}
            onChange={(e) => setJd(e.target.value)}
            style={{ height: '300px', width: '100%' }}
          />
          <input placeholder="Company" value={company} onChange={(e) => setCompany(e.target.value)} />
          <input id="role" placeholder="Role (e.g., SDE2)" />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze JD'}
          </button>
        </div>
      ) : (
        <>
          {/* Results */}
          <SkillGapAnalysis skills={analysis.skill_gaps} />
          <PredictedQuestions questions={analysis.predicted_questions} />
          <PrepRoadmap roadmap={analysis.roadmap} />

          <button onClick={() => setAnalysis(null)}>Analyze Another JD</button>
        </>
      )}
    </div>
  );
}
```

---

## ⏰ Timeline

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | JD Storage & Extraction | Upload JD → Extract skills ✅ |
| 2 | Gap Analysis & Questions | Show gaps + predict questions ✅ |
| 3 | Roadmap Generation | 4-week prep plan ✅ |
| 4 | Portal UI | Beautiful dashboard ✅ |
| 5 | Integration Testing | Link with mock practice |
| 6 | Trending Intelligence | Update skills as new JDs arrive |
| 7 | Historical Questions | Build question bank |
| 8 | Polish & Deploy | Production-ready |

---

## 🎯 Quick Wins (Do First)

### Week 1 Priority: Make JD Upload Work

```python
# Simplest version
@router.post("/jd/upload")
async def upload_jd(company: str, jd_text: str):
    # 1. Ask Claude to extract skills
    # 2. Store in DB
    # 3. Return extracted skills + importance scores

    skills = await claude_extract(jd_text)
    # {"Kafka": 9, "Java": 7, "System Design": 8}

    save_to_db(company, jd_text, skills)

    return {"extracted_skills": skills}
```

Then display it:

```jsx
<div>
  <h3>Skills in this JD:</h3>
  {skills.map(s => (
    <div key={s.name}>
      {s.name}: {s.importance}/10
    </div>
  ))}
</div>
```

✅ **That's enough to be useful!** Once this works, add gap analysis next week.

---

## 💡 Sample JD Responses

### Input
```
Amazon SDE2 JD:
"We're looking for an engineer with 5+ years...
Experience with Kafka, Java, distributed systems...
Design and scale systems handling 1M requests/day..."
```

### Output
```json
{
  "extracted_skills": {
    "required": [
      {"name": "Kafka", "importance": 9, "context": "1M events/day streaming"},
      {"name": "System Design", "importance": 9, "context": "Scale to 1M RPS"},
      {"name": "Java", "importance": 8, "context": "Core backend language"},
      {"name": "Distributed Systems", "importance": 8}
    ],
    "preferred": [
      {"name": "Golang", "importance": 6},
      {"name": "Kubernetes", "importance": 5}
    ]
  },
  "predicted_questions": {
    "system_design": [
      "Design a Kafka-based event streaming system",
      "How would you scale to 1M RPS?"
    ],
    "behavioral": [
      "Tell me about handling production incident"
    ]
  },
  "estimated_prep_time": "3-4 weeks to be interview-ready"
}
```

---

## 🚀 Get Started Now

1. **This week:** Build `/jd/upload` endpoint
2. **Test:** Paste real Amazon JD, see skills extracted
3. **Next week:** Add gap analysis
4. **Week 3:** Add question prediction
5. **Week 4:** Launch in portal

**Expected impact:** Increase interview success rate from 40% → 70%+

