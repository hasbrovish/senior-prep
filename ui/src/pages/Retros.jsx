import { useState } from 'react';
import { useProgress, useSaveProgress } from '../hooks/useProgress';
import { FileText, Plus, AlertTriangle, CheckCircle2, ArrowUpRight } from 'lucide-react';

export default function Retros() {
  const { data: progress, isLoading } = useProgress();
  const saveProgress = useSaveProgress();
  const [tab, setTab] = useState('retros');
  const [retroForm, setRetroForm] = useState({ went_well: '', improve: '', actions: '' });
  const [failureForm, setFailureForm] = useState({ round: '', description: '', learning: '' });

  if (isLoading) return <div className="page"><div className="loading">Loading...</div></div>;

  const retros = progress?.retros || [];
  const failures = progress?.failures || [];

  const handleAddRetro = (e) => {
    e.preventDefault();
    if (!retroForm.went_well.trim() && !retroForm.improve.trim()) return;
    const week = Math.ceil((Date.now() - new Date('2026-03-19').getTime()) / (7 * 86400000));
    const entry = {
      id: Date.now(), date: new Date().toISOString().slice(0, 10), week,
      ...retroForm,
    };
    saveProgress.mutate({ ...progress, retros: [...retros, entry] });
    setRetroForm({ went_well: '', improve: '', actions: '' });
  };

  const handleAddFailure = (e) => {
    e.preventDefault();
    if (!failureForm.description.trim()) return;
    const week = Math.ceil((Date.now() - new Date('2026-03-19').getTime()) / (7 * 86400000));
    const entry = {
      id: Date.now(), date: new Date().toISOString().slice(0, 10), week,
      ...failureForm,
    };
    saveProgress.mutate({ ...progress, failures: [...failures, entry] });
    setFailureForm({ round: '', description: '', learning: '' });
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2>Retros & Failures</h2>
        <div className="sub">Weekly retrospectives and failure analysis</div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 24 }}>
        {[['retros', 'Weekly Retros'], ['failures', 'Failure Log']].map(([key, label]) => (
          <button key={key} onClick={() => setTab(key)}
                  className={`btn ${tab === key ? 'btn-solid' : 'btn-gold'}`}>
            {label} ({key === 'retros' ? retros.length : failures.length})
          </button>
        ))}
      </div>

      {tab === 'retros' && (
        <>
          {/* Retro Form */}
          <div className="card mb-24">
            <div className="card-title">New Weekly Retro</div>
            <form onSubmit={handleAddRetro}>
              <div style={{ marginBottom: 8 }}>
                <label style={{ fontSize: 10, color: 'var(--green)', display: 'block', marginBottom: 4 }}>What went well?</label>
                <textarea rows={2} value={retroForm.went_well}
                          onChange={e => setRetroForm(f => ({ ...f, went_well: e.target.value }))} />
              </div>
              <div style={{ marginBottom: 8 }}>
                <label style={{ fontSize: 10, color: 'var(--orange)', display: 'block', marginBottom: 4 }}>What to improve?</label>
                <textarea rows={2} value={retroForm.improve}
                          onChange={e => setRetroForm(f => ({ ...f, improve: e.target.value }))} />
              </div>
              <div style={{ marginBottom: 8 }}>
                <label style={{ fontSize: 10, color: 'var(--blue)', display: 'block', marginBottom: 4 }}>Action items</label>
                <textarea rows={2} value={retroForm.actions}
                          onChange={e => setRetroForm(f => ({ ...f, actions: e.target.value }))} />
              </div>
              <button type="submit" className="btn btn-solid"><Plus size={14} /> Save Retro</button>
            </form>
          </div>

          {/* Retro History */}
          {retros.slice().reverse().map(r => (
            <div key={r.id || r.date} className="card mb-16">
              <div className="flex-between mb-8">
                <span style={{ fontSize: 12, fontWeight: 600 }}>Week {r.week}</span>
                <span style={{ fontSize: 10, color: 'var(--text3)' }}>{r.date}</span>
              </div>
              {r.went_well && <Section icon={CheckCircle2} color="var(--green)" label="Went well" text={r.went_well} />}
              {r.improve && <Section icon={ArrowUpRight} color="var(--orange)" label="Improve" text={r.improve} />}
              {r.actions && <Section icon={FileText} color="var(--blue)" label="Actions" text={r.actions} />}
            </div>
          ))}
        </>
      )}

      {tab === 'failures' && (
        <>
          {/* Failure Form */}
          <div className="card mb-24">
            <div className="card-title">Log Failure</div>
            <form onSubmit={handleAddFailure}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 8, marginBottom: 8 }}>
                <input placeholder="Round type (DSA, SD, etc.)" value={failureForm.round}
                       onChange={e => setFailureForm(f => ({ ...f, round: e.target.value }))} />
                <input placeholder="What happened?" value={failureForm.description}
                       onChange={e => setFailureForm(f => ({ ...f, description: e.target.value }))} />
              </div>
              <textarea rows={2} placeholder="What did you learn? How to avoid next time?"
                        value={failureForm.learning}
                        onChange={e => setFailureForm(f => ({ ...f, learning: e.target.value }))}
                        style={{ marginBottom: 8 }} />
              <button type="submit" className="btn btn-solid"><Plus size={14} /> Log</button>
            </form>
          </div>

          {/* Failure History */}
          {failures.slice().reverse().map(f => (
            <div key={f.id || f.date} style={{
              padding: '12px 14px', marginBottom: 8, background: 'var(--bg3)', borderRadius: 8,
              borderLeft: '3px solid var(--red)',
            }}>
              <div className="flex-between mb-8">
                <div>
                  {f.round && <span className="tag tag-red">{f.round}</span>}
                  <span style={{ fontSize: 10, color: 'var(--text3)', marginLeft: 8 }}>Week {f.week}</span>
                </div>
                <span style={{ fontSize: 10, color: 'var(--text4)' }}>{f.date}</span>
              </div>
              <div style={{ fontSize: 12, lineHeight: 1.6 }}>{f.description}</div>
              {f.learning && <div style={{ fontSize: 11, color: 'var(--green)', marginTop: 6 }}>Learning: {f.learning}</div>}
            </div>
          ))}
        </>
      )}
    </div>
  );
}

function Section({ icon: Icon, color, label, text }) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
        <Icon size={12} style={{ color }} />
        <span style={{ fontSize: 10, color, fontWeight: 600 }}>{label}</span>
      </div>
      <div style={{ fontSize: 12, lineHeight: 1.6, color: 'var(--text)', whiteSpace: 'pre-wrap', paddingLeft: 18 }}>{text}</div>
    </div>
  );
}
