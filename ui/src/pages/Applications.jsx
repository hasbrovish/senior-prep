import { useState } from 'react';
import { useProgress, useSaveProgress } from '../hooks/useProgress';
import { Plus, ArrowRight } from 'lucide-react';

const STAGES = ['Applied', 'OA', 'Phone Screen', 'Onsite', 'Offer', 'Rejected'];
const STAGE_COLORS = {
  Applied: 'var(--text3)', OA: 'var(--blue)', 'Phone Screen': 'var(--cyan)',
  Onsite: 'var(--orange)', Offer: 'var(--green)', Rejected: 'var(--red)',
};

export default function Applications() {
  const { data: progress, isLoading } = useProgress();
  const saveProgress = useSaveProgress();
  const [form, setForm] = useState({ company: '', role: '', link: '' });
  const [showForm, setShowForm] = useState(false);

  if (isLoading) return <div className="page"><div className="loading">Loading...</div></div>;

  const apps = progress?.applications || [];

  const handleAdd = (e) => {
    e.preventDefault();
    if (!form.company.trim()) return;
    const entry = {
      id: Date.now(), company: form.company.trim(), role: form.role.trim(),
      link: form.link.trim(), stage: 'Applied', date: new Date().toISOString().slice(0, 10),
    };
    saveProgress.mutate({ ...progress, applications: [...apps, entry] });
    setForm({ company: '', role: '', link: '' });
    setShowForm(false);
  };

  const moveStage = (id, newStage) => {
    const updated = apps.map(a => a.id === id ? { ...a, stage: newStage } : a);
    saveProgress.mutate({ ...progress, applications: updated });
  };

  const removeApp = (id) => {
    saveProgress.mutate({ ...progress, applications: apps.filter(a => a.id !== id) });
  };

  const byStage = {};
  for (const stage of STAGES) byStage[stage] = apps.filter(a => (a.stage || 'Applied') === stage);

  return (
    <div className="page">
      <div className="page-header">
        <div className="flex-between">
          <div>
            <h2>Applications</h2>
            <div className="sub">{apps.length} total applications tracked</div>
          </div>
          <button className="btn btn-solid" onClick={() => setShowForm(!showForm)}>
            <Plus size={14} /> Add Application
          </button>
        </div>
      </div>

      {showForm && (
        <div className="card mb-24">
          <form onSubmit={handleAdd}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, marginBottom: 8 }}>
              <input placeholder="Company" value={form.company} onChange={e => setForm(f => ({ ...f, company: e.target.value }))} />
              <input placeholder="Role (e.g. SDE-2)" value={form.role} onChange={e => setForm(f => ({ ...f, role: e.target.value }))} />
              <input placeholder="Job link (optional)" value={form.link} onChange={e => setForm(f => ({ ...f, link: e.target.value }))} />
            </div>
            <button type="submit" className="btn btn-solid" disabled={saveProgress.isPending}>Add</button>
          </form>
        </div>
      )}

      {/* Kanban */}
      <div style={{ display: 'grid', gridTemplateColumns: `repeat(${STAGES.length}, 1fr)`, gap: 12, overflowX: 'auto' }}>
        {STAGES.map(stage => (
          <div key={stage}>
            <div style={{
              fontSize: 10, fontWeight: 600, letterSpacing: 1.5, textTransform: 'uppercase',
              color: STAGE_COLORS[stage], marginBottom: 8, textAlign: 'center',
            }}>
              {stage} ({byStage[stage].length})
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6, minHeight: 100 }}>
              {byStage[stage].map(app => {
                const stageIdx = STAGES.indexOf(stage);
                const nextStage = STAGES[stageIdx + 1];
                return (
                  <div key={app.id} style={{
                    padding: '10px', background: 'var(--bg3)', borderRadius: 6,
                    border: '1px solid var(--bg4)',
                  }}>
                    <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 2 }}>{app.company}</div>
                    {app.role && <div style={{ fontSize: 10, color: 'var(--text3)' }}>{app.role}</div>}
                    <div style={{ fontSize: 9, color: 'var(--text4)', marginTop: 2 }}>{app.date}</div>
                    <div style={{ display: 'flex', gap: 4, marginTop: 8 }}>
                      {nextStage && stage !== 'Rejected' && (
                        <button className="btn btn-gold btn-sm" style={{ fontSize: 9, padding: '2px 6px' }}
                                onClick={() => moveStage(app.id, nextStage)}>
                          <ArrowRight size={10} /> {nextStage}
                        </button>
                      )}
                      {stage !== 'Rejected' && stage !== 'Offer' && (
                        <button className="btn btn-red btn-sm" style={{ fontSize: 9, padding: '2px 6px' }}
                                onClick={() => moveStage(app.id, 'Rejected')}>
                          Reject
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
