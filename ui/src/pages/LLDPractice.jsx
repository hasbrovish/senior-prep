import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import { useLogActivity } from '../hooks/useProgress';
import { Code2, Save, Star, Sparkles } from 'lucide-react';

export default function LLDPractice() {
  const [selectedKey, setSelectedKey] = useState(null);
  const [score, setScore] = useState(3);
  const [writeup, setWriteup] = useState('');
  const [evaluation, setEvaluation] = useState('');
  const qc = useQueryClient();
  const logActivity = useLogActivity();

  const { data: problems } = useQuery({
    queryKey: ['lldProblems'], queryFn: api.getLldProblems, staleTime: 300000,
  });
  const { data: scores } = useQuery({
    queryKey: ['lldScores'], queryFn: api.getLldScores, staleTime: 60000,
  });
  const { data: problem } = useQuery({
    queryKey: ['lldProblem', selectedKey],
    queryFn: () => api.getLldProblem(selectedKey),
    enabled: !!selectedKey, staleTime: 300000,
  });

  const saveScore = useMutation({
    mutationFn: api.saveLldScore,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['lldScores'] }),
  });

  const evaluateLld = useMutation({
    mutationFn: api.evaluateLld,
    onSuccess: (data) => setEvaluation(data?.evaluation || 'No evaluation returned'),
  });

  const handleSave = () => {
    saveScore.mutate({ problem_key: selectedKey, score, notes: writeup });
    logActivity.mutate({
      activity_type: 'lld', title: `LLD: ${selectedKey}`,
      outcome: score >= 4 ? 'completed' : 'struggled', confidence: score,
    });
  };

  const handleEvaluate = () => {
    evaluateLld.mutate({ problem_key: selectedKey, writeup });
  };

  const problemList = problems?.problems || [];
  const scoreList = scores?.scores || [];

  return (
    <div className="page">
      <div className="page-header">
        <h2>LLD Practice</h2>
        <div className="sub">Low-level design and machine coding problems</div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: 16 }}>
        {/* Problem List */}
        <div className="card" style={{ maxHeight: 'calc(100vh - 120px)', overflowY: 'auto' }}>
          <div className="card-title">Problems ({problemList.length})</div>
          {problemList.map(p => {
            const scored = scoreList.find(s => s.problem_key === (p.key || p.slug));
            return (
              <button key={p.key || p.slug}
                onClick={() => { setSelectedKey(p.key || p.slug); setWriteup(''); setEvaluation(''); }}
                style={{
                  display: 'block', width: '100%', textAlign: 'left',
                  padding: '10px 12px', marginBottom: 4, borderRadius: 6,
                  background: selectedKey === (p.key || p.slug) ? 'var(--bg4)' : 'var(--bg2)',
                  border: selectedKey === (p.key || p.slug) ? '1px solid var(--gold-border)' : '1px solid transparent',
                }}>
                <div style={{ fontSize: 12, color: 'var(--text)' }}>{p.title || p.name || p.key}</div>
                {scored && (
                  <div style={{ fontSize: 10, color: 'var(--green)', marginTop: 2 }}>
                    Score: {scored.score}/5
                  </div>
                )}
              </button>
            );
          })}
          {problemList.length === 0 && <div className="empty-state">No LLD problems available</div>}
        </div>

        {/* Problem Detail */}
        <div>
          {problem ? (
            <div className="card">
              <div className="card-title">{problem.title || problem.name || selectedKey}</div>
              {problem.description && (
                <div style={{ fontSize: 12, lineHeight: 1.7, marginBottom: 16, whiteSpace: 'pre-wrap' }}>
                  {problem.description}
                </div>
              )}
              {problem.requirements && (
                <div style={{ marginBottom: 16 }}>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 4 }}>Requirements</div>
                  <div style={{ fontSize: 12, lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>{
                    Array.isArray(problem.requirements) ? problem.requirements.join('\n') : problem.requirements
                  }</div>
                </div>
              )}

              <div style={{ marginBottom: 16 }}>
                <label style={{ fontSize: 10, color: 'var(--text3)', display: 'block', marginBottom: 4 }}>Your Design</label>
                <textarea rows={8} value={writeup} onChange={e => setWriteup(e.target.value)}
                          placeholder="Write your class diagram, API design, data models..." />
              </div>

              <div style={{ display: 'flex', gap: 8, marginBottom: 16, alignItems: 'center' }}>
                <span style={{ fontSize: 10, color: 'var(--text3)' }}>Score:</span>
                {[1, 2, 3, 4, 5].map(s => (
                  <button key={s} onClick={() => setScore(s)}
                    style={{ padding: '4px 8px', borderRadius: 4, fontSize: 12,
                      background: score === s ? 'var(--gold)' : 'var(--bg4)',
                      color: score === s ? 'var(--bg)' : 'var(--text)' }}>
                    {s}
                  </button>
                ))}
              </div>

              <div style={{ display: 'flex', gap: 8 }}>
                <button className="btn btn-solid" onClick={handleSave} disabled={saveScore.isPending}>
                  <Save size={14} /> Save Score
                </button>
                {writeup.trim() && (
                  <button className="btn btn-purple" onClick={handleEvaluate} disabled={evaluateLld.isPending}>
                    <Sparkles size={14} /> AI Evaluate
                  </button>
                )}
              </div>

              {evaluation && (
                <div style={{ marginTop: 16, padding: 14, background: 'var(--bg2)', borderRadius: 8,
                             fontSize: 12, lineHeight: 1.7, whiteSpace: 'pre-wrap', borderLeft: '3px solid var(--purple)' }}>
                  {evaluation}
                </div>
              )}
            </div>
          ) : (
            <div className="card empty-state">
              <Code2 size={24} style={{ color: 'var(--text4)', marginBottom: 8 }} />
              <div>Select a problem to start practicing</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
