import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import { useLogActivity } from '../hooks/useProgress';
import PomodoroTimer from '../components/PomodoroTimer';
import MockTrendChart from '../components/MockTrendChart';
import { Play, Save } from 'lucide-react';

const ROUND_TYPES = [
  { key: 'dsa', label: 'DSA', mins: 45 },
  { key: 'system_design', label: 'System Design', mins: 45 },
  { key: 'lld', label: 'LLD / Machine Coding', mins: 60 },
  { key: 'behavioral', label: 'Behavioral', mins: 30 },
  { key: 'machine_coding', label: 'Machine Coding', mins: 60 },
];

const COMPANIES = ['google', 'amazon', 'microsoft', 'uber', 'flipkart', 'walmart', 'phonepe', 'razorpay', 'atlassian'];

export default function MockInterview() {
  const [company, setCompany] = useState('google');
  const [roundType, setRoundType] = useState('dsa');
  const [phase, setPhase] = useState('setup');
  const [score, setScore] = useState(3);
  const [notes, setNotes] = useState('');
  const [questions, setQuestions] = useState('');

  const qc = useQueryClient();
  const logActivity = useLogActivity();

  const { data: mockTrend } = useQuery({
    queryKey: ['mockTrend'], queryFn: api.getMockTrend, staleTime: 60000,
  });
  const { data: readiness } = useQuery({
    queryKey: ['mockReadiness', company],
    queryFn: () => api.getMockReadiness(company),
    staleTime: 120000,
  });

  const saveMock = useMutation({
    mutationFn: api.saveMockScore,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['mockTrend'] });
      qc.invalidateQueries({ queryKey: ['mockReadiness'] });
      setPhase('done');
    },
  });

  const selectedRound = ROUND_TYPES.find(r => r.key === roundType);

  const handleStart = () => setPhase('active');

  const handleTimerComplete = (elapsedMins) => {
    setPhase('scoring');
  };

  const handleSave = () => {
    saveMock.mutate({
      company, round_type: roundType, score,
      questions: questions.split('\n').filter(Boolean),
      time_mins: selectedRound.mins,
      notes,
    });
    logActivity.mutate({
      activity_type: 'mock', title: `Mock ${selectedRound.label} - ${company}`,
      duration_mins: selectedRound.mins, outcome: score >= 3.5 ? 'completed' : 'struggled',
      confidence: score, difficulty: roundType,
    });
  };

  const readinessData = readiness?.rounds || {};

  return (
    <div className="page">
      <div className="page-header">
        <h2>Mock Interview</h2>
        <div className="sub">Simulate real interview rounds with timing and scoring</div>
      </div>

      {phase === 'setup' && (
        <>
          <div className="card mb-24">
            <div className="card-title">Configure Round</div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
              <div>
                <label style={{ fontSize: 10, color: 'var(--text3)', display: 'block', marginBottom: 4 }}>Company</label>
                <select value={company} onChange={e => setCompany(e.target.value)}>
                  {COMPANIES.map(c => <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
                </select>
              </div>
              <div>
                <label style={{ fontSize: 10, color: 'var(--text3)', display: 'block', marginBottom: 4 }}>Round Type</label>
                <select value={roundType} onChange={e => setRoundType(e.target.value)}>
                  {ROUND_TYPES.map(r => <option key={r.key} value={r.key}>{r.label} ({r.mins}m)</option>)}
                </select>
              </div>
            </div>
            <button className="btn btn-solid" onClick={handleStart}>
              <Play size={14} /> Start Mock ({selectedRound.mins} min)
            </button>
          </div>

          {/* Company Readiness */}
          {Object.keys(readinessData).length > 0 && (
            <div className="card mb-24">
              <div className="card-title">{company} Readiness</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {Object.entries(readinessData).map(([round, pct]) => (
                  <div key={round} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <span style={{ fontSize: 11, minWidth: 120 }}>{round.replace(/_/g, ' ')}</span>
                    <div className="progress-bar" style={{ flex: 1 }}>
                      <div className="progress-fill" style={{
                        width: `${pct}%`,
                        background: pct >= 70 ? 'var(--green)' : pct >= 40 ? 'var(--orange)' : 'var(--red)',
                      }} />
                    </div>
                    <span style={{ fontSize: 11, fontWeight: 600, minWidth: 35, textAlign: 'right' }}>{pct}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <MockTrendChart trendData={mockTrend} />
        </>
      )}

      {phase === 'active' && (
        <div className="grid grid-2">
          <PomodoroTimer minutes={selectedRound.mins} onComplete={handleTimerComplete} label={`${selectedRound.label} — ${company}`} />
          <div className="card">
            <div className="card-title">Questions / Notes</div>
            <textarea
              rows={8} placeholder="Write down the questions asked, your approach, key points..."
              value={questions} onChange={e => setQuestions(e.target.value)}
            />
          </div>
        </div>
      )}

      {phase === 'scoring' && (
        <div className="card">
          <div className="card-title">Score Your Performance</div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 10, color: 'var(--text3)', display: 'block', marginBottom: 8 }}>
              Score (1-5): {score}
            </label>
            <div style={{ display: 'flex', gap: 8 }}>
              {[1, 2, 3, 4, 5].map(s => (
                <button key={s} className={`btn ${score === s ? 'btn-solid' : 'btn-gold'}`}
                        onClick={() => setScore(s)} style={{ minWidth: 40 }}>
                  {s}
                </button>
              ))}
            </div>
            <div style={{ fontSize: 10, color: 'var(--text3)', marginTop: 4 }}>
              1 = Failed completely &middot; 3 = Decent with hints &middot; 5 = Nailed it
            </div>
          </div>
          <textarea rows={4} placeholder="Reflections, what went wrong, what to improve..."
                    value={notes} onChange={e => setNotes(e.target.value)}
                    style={{ marginBottom: 12 }} />
          <button className="btn btn-solid" onClick={handleSave} disabled={saveMock.isPending}>
            <Save size={14} /> Save Score
          </button>
        </div>
      )}

      {phase === 'done' && (
        <div className="card" style={{ textAlign: 'center', padding: 40 }}>
          <div style={{ fontSize: 32, marginBottom: 8 }}>Score: {score}/5</div>
          <div style={{ color: score >= 3.5 ? 'var(--green)' : 'var(--orange)', fontSize: 14, marginBottom: 16 }}>
            {score >= 4 ? 'Strong performance!' : score >= 3 ? 'Decent — keep practicing' : 'Needs work — review weak areas'}
          </div>
          <button className="btn btn-gold" onClick={() => { setPhase('setup'); setScore(3); setNotes(''); setQuestions(''); }}>
            Start Another
          </button>
        </div>
      )}
    </div>
  );
}
