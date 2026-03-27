import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api';
import { Brain, ChevronDown, ChevronUp, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function Behavioral() {
  const [expandedLp, setExpandedLp] = useState(null);
  const [starForm, setStarForm] = useState({ situation: '', task: '', action: '', result: '' });

  const { data: lpCheck, isLoading } = useQuery({
    queryKey: ['behavioralCheck'], queryFn: api.getBehavioralCheck, staleTime: 120000,
  });
  const { data: probes } = useQuery({
    queryKey: ['behavioralProbes', expandedLp],
    queryFn: () => api.getBehavioralProbes(expandedLp),
    enabled: !!expandedLp, staleTime: 300000,
  });

  const lpData = Array.isArray(lpCheck) ? lpCheck : (lpCheck?.principles || lpCheck?.results || []);

  return (
    <div className="page">
      <div className="page-header">
        <h2>Behavioral Prep</h2>
        <div className="sub">Leadership principles, STAR stories, and behavioral probes</div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {/* LP Check */}
        <div className="card" style={{ maxHeight: 'calc(100vh - 120px)', overflowY: 'auto' }}>
          <div className="card-title">Leadership Principle Gaps</div>
          {isLoading ? (
            <div className="loading">Loading...</div>
          ) : lpData.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {lpData.map((lp, i) => {
                const key = lp.lp || lp.key || lp.principle || `lp-${i}`;
                const label = lp.label || lp.name || lp.principle || key;
                const status = lp.status || lp.coverage || 'unknown';
                const isWeak = status === 'weak' || status === 'missing' || lp.gap;
                const isExpanded = expandedLp === key;

                return (
                  <div key={key}>
                    <button
                      onClick={() => setExpandedLp(isExpanded ? null : key)}
                      style={{
                        display: 'flex', alignItems: 'center', gap: 10, width: '100%',
                        padding: '10px 12px', background: 'var(--bg2)', borderRadius: 6,
                        borderLeft: `3px solid ${isWeak ? 'var(--red)' : 'var(--green)'}`,
                      }}>
                      {isWeak ? <AlertTriangle size={14} style={{ color: 'var(--red)' }} /> :
                               <CheckCircle2 size={14} style={{ color: 'var(--green)' }} />}
                      <span style={{ flex: 1, textAlign: 'left', fontSize: 12 }}>{label}</span>
                      {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    </button>
                    {isExpanded && probes && (
                      <div style={{ padding: '8px 12px 8px 24px', background: 'var(--bg3)', borderRadius: '0 0 6px 6px' }}>
                        {(probes.questions || []).map((q, qi) => (
                          <div key={qi} style={{ fontSize: 11, color: 'var(--text)', padding: '4px 0', borderBottom: '1px solid var(--bg4)' }}>
                            {q}
                          </div>
                        ))}
                        {(!probes.questions || probes.questions.length === 0) && (
                          <div style={{ fontSize: 11, color: 'var(--text3)' }}>No probe questions available</div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">No LP data available. Run behavioral check from CLI first.</div>
          )}
        </div>

        {/* STAR Builder */}
        <div className="card">
          <div className="card-title">STAR Story Builder</div>
          <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 12 }}>
            Practice structuring behavioral answers using the STAR framework
          </div>
          {['situation', 'task', 'action', 'result'].map(field => (
            <div key={field} style={{ marginBottom: 12 }}>
              <label style={{ fontSize: 10, color: 'var(--gold)', textTransform: 'uppercase', letterSpacing: 1, display: 'block', marginBottom: 4 }}>
                {field}
              </label>
              <textarea
                rows={3}
                placeholder={
                  field === 'situation' ? 'Describe the context and challenge...' :
                  field === 'task' ? 'What was your specific responsibility?' :
                  field === 'action' ? 'What steps did you take? Be specific...' :
                  'What was the measurable outcome?'
                }
                value={starForm[field]}
                onChange={e => setStarForm(prev => ({ ...prev, [field]: e.target.value }))}
              />
            </div>
          ))}
          <button className="btn btn-purple"
            onClick={() => {
              const story = Object.entries(starForm).map(([k, v]) => `**${k.toUpperCase()}:** ${v}`).join('\n\n');
              navigator.clipboard?.writeText(story);
            }}>
            Copy Story
          </button>
        </div>
      </div>
    </div>
  );
}
