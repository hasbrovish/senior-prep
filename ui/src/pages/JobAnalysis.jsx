import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  BriefcaseBusiness, ChevronRight, Upload, BarChart3, MapPin,
  Brain, Clock, TrendingUp, CheckCircle, AlertCircle, AlertTriangle,
  RefreshCw, ChevronDown, ChevronUp, Star, Target,
} from 'lucide-react';
import { api } from '../api';

// ─── helpers ──────────────────────────────────────────────────────────────────

const STATUS_COLOR = {
  strong: 'var(--green)',
  minor_gap: 'var(--gold)',
  moderate_gap: '#f97316',
  critical_gap: 'var(--red)',
};

const STATUS_LABEL = {
  strong: 'Strong',
  minor_gap: 'Minor gap',
  moderate_gap: 'Moderate gap',
  critical_gap: 'Critical gap',
};

const IMPORTANCE_COLOR = (n) => {
  if (n >= 8) return 'var(--red)';
  if (n >= 6) return 'var(--gold)';
  return 'var(--text3)';
};

function ReadinessBadge({ pct }) {
  const color = pct >= 75 ? 'var(--green)' : pct >= 50 ? 'var(--gold)' : 'var(--red)';
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      padding: '16px 24px', background: 'var(--bg2)', borderRadius: 12,
      border: `2px solid ${color}`,
    }}>
      <div style={{ fontSize: 42, fontWeight: 800, color, lineHeight: 1 }}>{pct}%</div>
      <div style={{ fontSize: 11, color: 'var(--text3)', marginTop: 4 }}>Interview Readiness</div>
      {pct >= 75
        ? <div style={{ fontSize: 10, color: 'var(--green)', marginTop: 4 }}>✓ Interview Ready</div>
        : <div style={{ fontSize: 10, color: 'var(--gold)', marginTop: 4 }}>Keep prepping</div>}
    </div>
  );
}

function SkillBar({ skill, required, current, status }) {
  const color = STATUS_COLOR[status] || 'var(--text3)';
  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
        <span style={{ fontSize: 12, fontWeight: 500 }}>{skill}</span>
        <span style={{ fontSize: 10, color }}>
          {current}/10 vs {required}/10 required
        </span>
      </div>
      <div style={{ height: 6, background: 'var(--bg4)', borderRadius: 3, position: 'relative' }}>
        <div style={{
          height: '100%', borderRadius: 3,
          width: `${(required / 10) * 100}%`,
          background: 'var(--bg4)',
          position: 'absolute', top: 0, left: 0,
        }} />
        <div style={{
          height: '100%', borderRadius: 3,
          width: `${(current / 10) * 100}%`,
          background: color,
          position: 'absolute', top: 0, left: 0,
        }} />
      </div>
    </div>
  );
}

function SkillSlider({ skill, required, value, onChange }) {
  const gap = Math.max(0, required - value);
  const color = gap === 0 ? 'var(--green)' : gap <= 2 ? 'var(--gold)' : gap <= 4 ? '#f97316' : 'var(--red)';
  return (
    <div style={{
      padding: '10px 14px', background: 'var(--bg2)', borderRadius: 8,
      border: `1px solid ${color}33`,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span style={{ fontSize: 12, fontWeight: 600 }}>{skill}</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 10, color: 'var(--text3)' }}>Required: {required}/10</span>
          <span style={{
            fontSize: 10, padding: '1px 6px', borderRadius: 4,
            background: color + '22', color,
          }}>
            {value}/10 {gap > 0 ? `(gap: ${gap})` : '✓'}
          </span>
        </div>
      </div>
      <input
        type="range" min={0} max={10} value={value}
        onChange={(e) => onChange(parseInt(e.target.value, 10))}
        style={{ width: '100%', accentColor: color, cursor: 'pointer' }}
      />
    </div>
  );
}

function ImportanceBadge({ n }) {
  const label = n >= 8 ? 'HIGH' : n >= 6 ? 'MED' : 'LOW';
  const color = IMPORTANCE_COLOR(n);
  return (
    <span style={{
      fontSize: 9, padding: '2px 5px', borderRadius: 3,
      border: `1px solid ${color}`, color, letterSpacing: 0.5,
    }}>{label}</span>
  );
}

function QuestionCard({ q, importance, topics }) {
  return (
    <div style={{
      padding: '10px 14px', background: 'var(--bg2)', borderRadius: 8,
      border: '1px solid var(--bg4)', marginBottom: 8,
    }}>
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 8 }}>
        <ImportanceBadge n={importance} />
        <span style={{ fontSize: 13, flex: 1 }}>{q}</span>
      </div>
      {topics?.length > 0 && (
        <div style={{ marginTop: 6, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
          {topics.map((t) => (
            <span key={t} style={{
              fontSize: 9, padding: '1px 5px', borderRadius: 4,
              background: 'var(--bg3)', color: 'var(--text3)',
            }}>{t}</span>
          ))}
        </div>
      )}
    </div>
  );
}

function WeekCard({ week }) {
  const [open, setOpen] = useState(week.week <= 2);
  return (
    <div style={{
      border: '1px solid var(--bg4)', borderRadius: 10,
      marginBottom: 10, overflow: 'hidden',
    }}>
      <button
        onClick={() => setOpen((o) => !o)}
        style={{
          width: '100%', display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', padding: '12px 16px',
          background: 'var(--bg2)', border: 'none', cursor: 'pointer',
        }}
      >
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <div style={{
            width: 28, height: 28, borderRadius: '50%',
            background: 'var(--bg3)', display: 'flex', alignItems: 'center',
            justifyContent: 'center', fontSize: 11, fontWeight: 700,
            color: 'var(--gold)',
          }}>W{week.week}</div>
          <div style={{ textAlign: 'left' }}>
            <div style={{ fontSize: 13, fontWeight: 600 }}>{week.theme}</div>
            <div style={{ fontSize: 10, color: 'var(--text3)' }}>
              Focus: {week.focus} · {week.daily_target}
            </div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {week.behavioral_prep && (
            <span style={{ fontSize: 9, color: 'var(--gold)', border: '1px solid var(--gold)', padding: '2px 5px', borderRadius: 3 }}>
              BEHAVIORAL
            </span>
          )}
          {open ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </div>
      </button>
      {open && (
        <div style={{ padding: '12px 16px', background: 'var(--bg1)' }}>
          {week.topics.map((topic, i) => (
            <div key={i} style={{
              marginBottom: 10, padding: '10px 12px',
              background: 'var(--bg2)', borderRadius: 8,
              border: '1px solid var(--bg3)',
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: 13, fontWeight: 600 }}>{topic.skill}</span>
                <span style={{ fontSize: 10, color: 'var(--text3)' }}>~{topic.hours}h</span>
              </div>
              <div style={{ fontSize: 11, color: 'var(--text2)', marginBottom: 6 }}>{topic.goal}</div>
              {topic.resources?.map((r, j) => (
                <div key={j} style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 2 }}>
                  → {r}
                </div>
              ))}
            </div>
          ))}
          <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
            <span style={{ fontSize: 10, color: 'var(--text3)' }}>
              LC target: {week.lc_target} problems
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Main component ────────────────────────────────────────────────────────────

export default function JobAnalysis() {
  const qc = useQueryClient();
  const [tab, setTab] = useState('analyze');
  const [form, setForm] = useState({ company: '', role: '', level: 'senior', jdText: '' });
  const [currentJd, setCurrentJd] = useState(null);
  const [userSkills, setUserSkills] = useState({});
  const [gapResult, setGapResult] = useState(null);
  const [roadmapResult, setRoadmapResult] = useState(null);
  const [roadmapWeeks, setRoadmapWeeks] = useState(4);
  const [qTab, setQTab] = useState('system_design');
  const [behavioralCompany, setBehavioralCompany] = useState('');

  const { data: jdList, isLoading: listLoading } = useQuery({
    queryKey: ['jdList'],
    queryFn: api.listJds,
    staleTime: 30000,
  });

  const { data: behavioralData } = useQuery({
    queryKey: ['behavioral', behavioralCompany],
    queryFn: () => api.getBehavioralGuide(behavioralCompany),
    enabled: !!behavioralCompany && tab === 'behavioral',
    staleTime: 300000,
  });

  const uploadMut = useMutation({
    mutationFn: api.uploadJd,
    onSuccess: (data) => {
      const skills = {};
      Object.keys(data.key_technologies || {}).forEach((s) => { skills[s] = 5; });
      setCurrentJd(data);
      setUserSkills(skills);
      setGapResult(null);
      setRoadmapResult(null);
      setBehavioralCompany(data.company);
      setTab('gap');
      qc.invalidateQueries({ queryKey: ['jdList'] });
    },
  });

  const loadJdMut = useMutation({
    mutationFn: api.getJdAnalysis,
    onSuccess: (data) => {
      const skills = {};
      const depth = typeof data.skill_depth_required === 'object' && !Array.isArray(data.skill_depth_required)
        ? data.skill_depth_required : {};
      Object.keys(depth).forEach((s) => { skills[s] = 5; });
      // Normalize shape to match upload response
      setCurrentJd({
        jd_id: data.id,
        company: data.company,
        role: data.role,
        level: data.level,
        extracted_skills: data.skill_analysis?.map((r) => ({ name: r.skill_name, importance: r.importance_score })) || [],
        preferred_skills: data.preferred_skills || [],
        key_technologies: depth,
        estimated_difficulty: data.estimated_difficulty,
        predicted_questions: data.predicted_questions || {},
      });
      setUserSkills(skills);
      setGapResult(null);
      setRoadmapResult(null);
      setBehavioralCompany(data.company);
      setTab('gap');
    },
  });

  const gapMut = useMutation({
    mutationFn: () => api.analyzeJdGap(currentJd.jd_id, userSkills),
    onSuccess: (data) => {
      setGapResult(data);
    },
  });

  const roadmapMut = useMutation({
    mutationFn: () => api.generateJdRoadmap(currentJd.jd_id, userSkills, roadmapWeeks),
    onSuccess: (data) => {
      setRoadmapResult(data);
      setTab('roadmap');
    },
  });

  const skillDepth = currentJd?.key_technologies || {};
  const questions = currentJd?.predicted_questions || {};
  const qCategories = Object.keys(questions).filter((k) => Array.isArray(questions[k]) && questions[k].length > 0);

  // ── Render ──────────────────────────────────────────────────────────────────

  const TABS = [
    { key: 'analyze', label: 'Analyze JD', icon: Upload },
    { key: 'gap', label: 'Skill Gap', icon: BarChart3, disabled: !currentJd },
    { key: 'questions', label: 'Questions', icon: Brain, disabled: !currentJd },
    { key: 'roadmap', label: 'Roadmap', icon: MapPin, disabled: !currentJd },
    { key: 'behavioral', label: 'Behavioral', icon: Target },
  ];

  return (
    <div className="page">
      <div className="page-header">
        <h2>Job Analysis</h2>
        <div className="sub">
          Upload JD → AI extracts skills → Analyze your gaps → Generate personalized roadmap
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 24, flexWrap: 'wrap' }}>
        {TABS.map(({ key, label, icon: Icon, disabled }) => (
          <button
            key={key}
            onClick={() => !disabled && setTab(key)}
            disabled={disabled}
            style={{
              display: 'flex', alignItems: 'center', gap: 6, padding: '6px 14px',
              borderRadius: 6, border: 'none', cursor: disabled ? 'not-allowed' : 'pointer',
              background: tab === key ? 'var(--gold)' : 'var(--bg3)',
              color: tab === key ? 'var(--bg1)' : disabled ? 'var(--text3)' : 'var(--text2)',
              fontWeight: tab === key ? 600 : 400, fontSize: 12,
              opacity: disabled ? 0.5 : 1,
            }}
          >
            <Icon size={12} />
            {label}
          </button>
        ))}
        {currentJd && (
          <div style={{
            marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 8,
            padding: '4px 10px', background: 'var(--bg2)', borderRadius: 6,
            border: '1px solid var(--bg4)',
          }}>
            <BriefcaseBusiness size={11} style={{ color: 'var(--gold)' }} />
            <span style={{ fontSize: 11 }}>{currentJd.company}</span>
            <span style={{ fontSize: 10, color: 'var(--text3)' }}>{currentJd.role}</span>
          </div>
        )}
      </div>

      {/* ── Analyze Tab ─────────────────────────────────────────────────────── */}
      {tab === 'analyze' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: 20 }}>
          {/* Upload form */}
          <div className="card">
            <div className="card-title">Analyze a Job Description</div>
            <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 16 }}>
              Paste any JD → AI extracts required skills, predicts interview questions, and estimates prep time
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 8 }}>
              <input
                placeholder="Company *  e.g. Amazon, Razorpay"
                value={form.company}
                onChange={(e) => setForm((f) => ({ ...f, company: e.target.value }))}
              />
              <input
                placeholder="Role *  e.g. Backend SDE-2"
                value={form.role}
                onChange={(e) => setForm((f) => ({ ...f, role: e.target.value }))}
              />
            </div>
            <select
              value={form.level}
              onChange={(e) => setForm((f) => ({ ...f, level: e.target.value }))}
              style={{ marginBottom: 8 }}
            >
              <option value="junior">Junior (0-2 YOE)</option>
              <option value="mid">Mid / SDE-2 (2-5 YOE)</option>
              <option value="senior">Senior / SDE-3 (5-8 YOE)</option>
              <option value="staff">Staff (8+ YOE)</option>
            </select>

            <textarea
              rows={14}
              placeholder="Paste the full job description here…"
              value={form.jdText}
              onChange={(e) => setForm((f) => ({ ...f, jdText: e.target.value }))}
              style={{ marginBottom: 12, fontFamily: 'inherit', fontSize: 12 }}
            />

            <button
              className="btn btn-solid"
              onClick={() => uploadMut.mutate({ jd_text: form.jdText, company: form.company, role: form.role, level: form.level })}
              disabled={uploadMut.isPending || !form.company.trim() || !form.role.trim() || !form.jdText.trim()}
            >
              {uploadMut.isPending ? (
                <><RefreshCw size={13} style={{ animation: 'spin 1s linear infinite' }} /> Analyzing with AI...</>
              ) : (
                <><Upload size={13} /> Analyze JD</>
              )}
            </button>

            {uploadMut.isError && (
              <div style={{ marginTop: 8, fontSize: 11, color: 'var(--red)' }}>
                {uploadMut.error?.message}
              </div>
            )}
            {uploadMut.isSuccess && (
              <div style={{ marginTop: 8, fontSize: 11, color: 'var(--green)' }}>
                ✓ Analysis complete — {currentJd?.extracted_skills?.length || 0} skills extracted
              </div>
            )}
          </div>

          {/* Recent JDs */}
          <div className="card" style={{ overflowY: 'auto', maxHeight: 500 }}>
            <div className="card-title">Recent JDs</div>
            {listLoading && (
              <div style={{ fontSize: 11, color: 'var(--text3)' }}>Loading…</div>
            )}
            {(jdList?.jds || []).length === 0 && !listLoading && (
              <div style={{ fontSize: 11, color: 'var(--text3)' }}>
                No JDs analyzed yet. Upload your first one!
              </div>
            )}
            {(jdList?.jds || []).map((jd) => (
              <div
                key={jd.id}
                onClick={() => loadJdMut.mutate(jd.id)}
                style={{
                  padding: '10px 12px', borderRadius: 8, cursor: 'pointer',
                  border: '1px solid var(--bg4)', marginBottom: 8,
                  background: currentJd?.jd_id === jd.id ? 'var(--bg3)' : 'var(--bg2)',
                  transition: 'all 0.15s',
                }}
                onMouseOver={(e) => e.currentTarget.style.borderColor = 'var(--gold)'}
                onMouseOut={(e) => e.currentTarget.style.borderColor = 'var(--bg4)'}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>{jd.company}</div>
                  <ChevronRight size={12} style={{ color: 'var(--text3)' }} />
                </div>
                <div style={{ fontSize: 11, color: 'var(--text2)' }}>{jd.role}</div>
                <div style={{ fontSize: 10, color: 'var(--text3)', marginTop: 2 }}>
                  {jd.estimated_difficulty} · {jd.years_experience}+ YOE
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Gap Analysis Tab ─────────────────────────────────────────────────── */}
      {tab === 'gap' && currentJd && (
        <div>
          <div style={{
            display: 'flex', alignItems: 'center', gap: 12,
            padding: '12px 16px', background: 'var(--bg2)', borderRadius: 10,
            border: '1px solid var(--bg4)', marginBottom: 20,
          }}>
            <BriefcaseBusiness size={16} style={{ color: 'var(--gold)' }} />
            <div>
              <div style={{ fontWeight: 600 }}>{currentJd.company} — {currentJd.role}</div>
              <div style={{ fontSize: 11, color: 'var(--text3)' }}>
                {currentJd.estimated_difficulty} · Set your current level for each skill (0–10)
              </div>
            </div>
            {gapResult && (
              <div style={{ marginLeft: 'auto' }}>
                <ReadinessBadge pct={gapResult.overall_readiness} />
              </div>
            )}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 16 }}>
            {Object.entries(skillDepth).map(([skill, required]) => (
              <SkillSlider
                key={skill}
                skill={skill}
                required={required}
                value={userSkills[skill] ?? 5}
                onChange={(v) => setUserSkills((s) => ({ ...s, [skill]: v }))}
              />
            ))}
          </div>

          <div style={{ display: 'flex', gap: 10, marginBottom: 20 }}>
            <button
              className="btn btn-solid"
              onClick={() => gapMut.mutate()}
              disabled={gapMut.isPending || Object.keys(skillDepth).length === 0}
            >
              {gapMut.isPending ? <><RefreshCw size={13} style={{ animation: 'spin 1s linear infinite' }} /> Analyzing…</> : <><BarChart3 size={13} /> Analyze Gap</>}
            </button>
            {gapResult && (
              <button
                className="btn btn-gold btn-sm"
                onClick={() => roadmapMut.mutate()}
                disabled={roadmapMut.isPending}
              >
                {roadmapMut.isPending ? 'Generating…' : <><MapPin size={13} /> Generate {roadmapWeeks}-Week Roadmap</>}
              </button>
            )}
            {gapResult && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ fontSize: 11, color: 'var(--text3)' }}>Weeks:</span>
                <select
                  value={roadmapWeeks}
                  onChange={(e) => setRoadmapWeeks(Number(e.target.value))}
                  style={{ padding: '4px 8px', fontSize: 12, minWidth: 60 }}
                >
                  {[2, 3, 4, 5, 6, 8].map((w) => <option key={w} value={w}>{w}</option>)}
                </select>
              </div>
            )}
          </div>

          {/* Gap Results */}
          {gapResult && (
            <div>
              {/* Summary */}
              <div style={{
                padding: '12px 16px', background: 'var(--bg2)', borderRadius: 10,
                border: '1px solid var(--bg4)', marginBottom: 16,
              }}>
                <div style={{ fontSize: 13, color: 'var(--text2)' }}>{gapResult.summary}</div>
                <div style={{ fontSize: 11, color: 'var(--text3)', marginTop: 4 }}>
                  Est. total prep: {gapResult.total_prep_hours}h
                </div>
              </div>

              {/* Skill breakdown */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                {Object.values(gapResult.skill_gaps || {}).map((g) => (
                  <div
                    key={g.skill}
                    style={{
                      padding: '10px 14px', background: 'var(--bg2)', borderRadius: 8,
                      border: `1px solid ${STATUS_COLOR[g.status]}33`,
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                      <span style={{ fontSize: 12, fontWeight: 600 }}>{g.skill}</span>
                      <span style={{
                        fontSize: 9, padding: '2px 5px', borderRadius: 3,
                        color: STATUS_COLOR[g.status],
                        border: `1px solid ${STATUS_COLOR[g.status]}`,
                      }}>
                        {STATUS_LABEL[g.status]}
                      </span>
                    </div>
                    <SkillBar
                      skill={g.skill} required={g.required}
                      current={g.current} status={g.status}
                    />
                    <div style={{ fontSize: 10, color: 'var(--text3)' }}>
                      {g.prep_hours}h to close gap
                    </div>
                  </div>
                ))}
              </div>

              {/* Priority focus */}
              {gapResult.priority_focus?.length > 0 && (
                <div className="card" style={{ marginTop: 16 }}>
                  <div className="card-title">Priority Focus (Top Gaps)</div>
                  {gapResult.priority_focus.map((g, i) => (
                    <div key={g.skill} style={{
                      display: 'flex', alignItems: 'center', gap: 10,
                      padding: '8px 0', borderBottom: i < gapResult.priority_focus.length - 1 ? '1px solid var(--bg4)' : 'none',
                    }}>
                      <div style={{
                        width: 22, height: 22, borderRadius: '50%',
                        background: 'var(--bg3)', display: 'flex', alignItems: 'center',
                        justifyContent: 'center', fontSize: 10, fontWeight: 700, color: 'var(--gold)',
                      }}>{i + 1}</div>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontSize: 12, fontWeight: 600 }}>{g.skill}</div>
                        <div style={{ fontSize: 10, color: 'var(--text3)' }}>
                          {g.current}/10 → {g.required}/10 required · {g.prep_hours}h
                        </div>
                      </div>
                      <span style={{
                        fontSize: 10, color: STATUS_COLOR[g.status],
                        border: `1px solid ${STATUS_COLOR[g.status]}`,
                        padding: '1px 5px', borderRadius: 3,
                      }}>
                        gap: {g.gap}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* ── Questions Tab ────────────────────────────────────────────────────── */}
      {tab === 'questions' && currentJd && (
        <div>
          <div style={{
            padding: '10px 14px', background: 'var(--bg2)', borderRadius: 8,
            border: '1px solid var(--bg4)', marginBottom: 16, fontSize: 11, color: 'var(--text3)',
          }}>
            Predicted interview questions for <b style={{ color: 'var(--text1)' }}>{currentJd.company} — {currentJd.role}</b>.
            Based on JD text + company patterns.
          </div>

          {qCategories.length === 0 && (
            <div style={{ fontSize: 12, color: 'var(--text3)', textAlign: 'center', padding: 40 }}>
              No predicted questions available. Re-analyze the JD with an active Anthropic API key for AI predictions.
            </div>
          )}

          {qCategories.length > 0 && (
            <>
              <div style={{ display: 'flex', gap: 4, marginBottom: 16, flexWrap: 'wrap' }}>
                {qCategories.map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setQTab(cat)}
                    style={{
                      padding: '5px 12px', borderRadius: 6, border: 'none',
                      cursor: 'pointer', fontSize: 11,
                      background: qTab === cat ? 'var(--bg4)' : 'var(--bg2)',
                      color: qTab === cat ? 'var(--text1)' : 'var(--text3)',
                      textTransform: 'capitalize',
                    }}
                  >
                    {cat.replace(/_/g, ' ')} ({questions[cat]?.length || 0})
                  </button>
                ))}
              </div>
              <div>
                {(questions[qTab] || []).map((item, i) => (
                  <QuestionCard
                    key={i}
                    q={item.q || item}
                    importance={item.importance || 6}
                    topics={item.topics}
                  />
                ))}
              </div>
            </>
          )}

          {/* Also show extracted skills summary */}
          <div className="card" style={{ marginTop: 20 }}>
            <div className="card-title">Required Skills</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {(currentJd.extracted_skills || []).map((s) => {
                const name = typeof s === 'string' ? s : s.name;
                const imp = typeof s === 'object' ? s.importance : 7;
                return (
                  <div key={name} style={{
                    padding: '4px 10px', borderRadius: 6,
                    background: 'var(--bg2)', border: '1px solid var(--bg4)',
                    display: 'flex', alignItems: 'center', gap: 6,
                  }}>
                    <span style={{ fontSize: 12 }}>{name}</span>
                    <ImportanceBadge n={imp} />
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ── Roadmap Tab ──────────────────────────────────────────────────────── */}
      {tab === 'roadmap' && currentJd && (
        <div>
          {!roadmapResult ? (
            <div className="card" style={{ textAlign: 'center', padding: 40 }}>
              <MapPin size={32} style={{ color: 'var(--gold)', marginBottom: 12 }} />
              <div style={{ fontSize: 14, marginBottom: 8 }}>No roadmap yet</div>
              <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 16 }}>
                Go to Gap Analysis, set your skill levels, then click "Generate Roadmap"
              </div>
              <button
                className="btn btn-gold"
                onClick={() => setTab('gap')}
              >
                Go to Gap Analysis
              </button>
            </div>
          ) : (
            <div>
              {/* Roadmap header */}
              <div style={{
                padding: '14px 18px', background: 'var(--bg2)', borderRadius: 10,
                border: '1px solid var(--bg4)', marginBottom: 20,
                display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16,
              }}>
                <div>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 2 }}>TARGET</div>
                  <div style={{ fontSize: 13, fontWeight: 700 }}>{roadmapResult.company}</div>
                  <div style={{ fontSize: 11, color: 'var(--text2)' }}>{roadmapResult.role}</div>
                </div>
                <div>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 2 }}>DURATION</div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: 'var(--gold)', lineHeight: 1 }}>
                    {roadmapResult.weeks}w
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 2 }}>TOTAL HOURS</div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: 'var(--gold)', lineHeight: 1 }}>
                    {roadmapResult.total_prep_hours}h
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 2 }}>CURRENT READINESS</div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: 'var(--green)', lineHeight: 1 }}>
                    {roadmapResult.overall_readiness}%
                  </div>
                </div>
              </div>

              {/* Top priorities */}
              {roadmapResult.top_priorities?.length > 0 && (
                <div style={{
                  padding: '10px 14px', background: 'var(--bg2)', borderRadius: 8,
                  border: '1px solid var(--bg4)', marginBottom: 16, fontSize: 12,
                }}>
                  <span style={{ color: 'var(--text3)' }}>Top priorities: </span>
                  {roadmapResult.top_priorities.map((p, i) => (
                    <span key={p}>
                      <span style={{ color: 'var(--gold)', fontWeight: 600 }}>{p}</span>
                      {i < roadmapResult.top_priorities.length - 1 && <span style={{ color: 'var(--text3)' }}> → </span>}
                    </span>
                  ))}
                </div>
              )}

              {/* Weekly plans */}
              {(roadmapResult.weekly_plans || []).map((week) => (
                <WeekCard key={week.week} week={week} />
              ))}

              {/* Regenerate */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 16 }}>
                <span style={{ fontSize: 11, color: 'var(--text3)' }}>Regenerate with:</span>
                <select
                  value={roadmapWeeks}
                  onChange={(e) => setRoadmapWeeks(Number(e.target.value))}
                  style={{ padding: '4px 8px', fontSize: 12 }}
                >
                  {[2, 3, 4, 5, 6, 8].map((w) => <option key={w} value={w}>{w} weeks</option>)}
                </select>
                <button
                  className="btn btn-gold btn-sm"
                  onClick={() => roadmapMut.mutate()}
                  disabled={roadmapMut.isPending}
                >
                  <RefreshCw size={11} /> Regenerate
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── Behavioral Tab ───────────────────────────────────────────────────── */}
      {tab === 'behavioral' && (
        <div>
          {/* Company selector */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
            {['Amazon', 'Google', 'Flipkart', 'Razorpay', 'PhonePe', 'Swiggy', 'CRED', 'Stripe', 'Microsoft', 'Bloomberg', 'DoorDash'].map((c) => (
              <button
                key={c}
                onClick={() => setBehavioralCompany(c)}
                style={{
                  padding: '5px 12px', borderRadius: 6, border: 'none',
                  cursor: 'pointer', fontSize: 11,
                  background: behavioralCompany === c ? 'var(--gold)' : 'var(--bg3)',
                  color: behavioralCompany === c ? 'var(--bg1)' : 'var(--text2)',
                  fontWeight: behavioralCompany === c ? 600 : 400,
                }}
              >
                {c}
              </button>
            ))}
          </div>

          {!behavioralCompany && (
            <div className="card" style={{ textAlign: 'center', padding: 40 }}>
              <Brain size={32} style={{ color: 'var(--gold)', marginBottom: 12 }} />
              <div style={{ fontSize: 13 }}>Select a company above to see its behavioral framework</div>
            </div>
          )}

          {behavioralCompany && !behavioralData && (
            <div style={{ fontSize: 12, color: 'var(--text3)', padding: 20 }}>Loading framework…</div>
          )}

          {behavioralData && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              {/* Framework */}
              <div>
                <div className="card" style={{ marginBottom: 16 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                    <div>
                      <div className="card-title" style={{ marginBottom: 2 }}>{behavioralData.company}</div>
                      <div style={{ fontSize: 12, color: 'var(--gold)' }}>{behavioralData.framework}</div>
                    </div>
                    {behavioralData.tc_range && (
                      <div style={{
                        fontSize: 10, padding: '4px 8px', background: 'var(--bg3)',
                        borderRadius: 6, color: 'var(--text2)', textAlign: 'right',
                      }}>
                        <div>TC Range</div>
                        <div style={{ color: 'var(--green)', fontWeight: 600 }}>{behavioralData.tc_range}</div>
                      </div>
                    )}
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 12 }}>
                    {behavioralData.format}
                  </div>
                  {behavioralData.stack && (
                    <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 12 }}>
                      <b>Stack:</b> {behavioralData.stack}
                    </div>
                  )}

                  <div className="card-title" style={{ fontSize: 11, marginBottom: 6 }}>Key Principles</div>
                  {(behavioralData.key_principles || []).map((p, i) => (
                    <div key={i} style={{
                      padding: '6px 10px', borderRadius: 6, background: 'var(--bg1)',
                      marginBottom: 6, fontSize: 11, lineHeight: 1.5,
                      borderLeft: '3px solid var(--gold)',
                    }}>
                      {p}
                    </div>
                  ))}
                </div>

                {/* Tips */}
                {(behavioralData.tips || []).length > 0 && (
                  <div className="card">
                    <div className="card-title">Interview Tips</div>
                    {behavioralData.tips.map((tip, i) => (
                      <div key={i} style={{
                        display: 'flex', gap: 8, marginBottom: 8, fontSize: 11,
                      }}>
                        <CheckCircle size={12} style={{ color: 'var(--green)', flexShrink: 0, marginTop: 1 }} />
                        <span style={{ color: 'var(--text2)', lineHeight: 1.5 }}>{tip}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Top Questions */}
              <div className="card">
                <div className="card-title">
                  Must-Prepare Questions
                  <span style={{ fontSize: 10, color: 'var(--text3)', marginLeft: 8 }}>
                    ({(behavioralData.top_questions || []).length} questions)
                  </span>
                </div>
                <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 12 }}>
                  Prepare STAR stories for each of these — they come up in almost every round.
                </div>
                {(behavioralData.top_questions || []).map((q, i) => (
                  <div key={i} style={{
                    padding: '8px 12px', background: 'var(--bg1)', borderRadius: 6,
                    marginBottom: 6, display: 'flex', gap: 8, alignItems: 'flex-start',
                  }}>
                    <span style={{
                      minWidth: 18, height: 18, borderRadius: '50%',
                      background: 'var(--bg3)', display: 'flex', alignItems: 'center',
                      justifyContent: 'center', fontSize: 9, color: 'var(--gold)',
                      fontWeight: 700, flexShrink: 0, marginTop: 1,
                    }}>{i + 1}</span>
                    <span style={{ fontSize: 12, lineHeight: 1.5 }}>{q}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
