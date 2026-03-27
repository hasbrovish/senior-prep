import { useState } from 'react';
import { useProgress, useSaveProgress } from '../hooks/useProgress';
import { Bug, Plus, Search } from 'lucide-react';

export default function BugJournal() {
  const { data: progress, isLoading } = useProgress();
  const saveProgress = useSaveProgress();
  const [form, setForm] = useState({ description: '', category: 'logic', context: '' });
  const [filter, setFilter] = useState('');

  if (isLoading) return <div className="page"><div className="loading">Loading...</div></div>;

  const bugs = progress?.bug_journal || [];

  const handleAdd = (e) => {
    e.preventDefault();
    if (!form.description.trim()) return;
    const entry = {
      id: Date.now(), date: new Date().toISOString().slice(0, 10),
      description: form.description.trim(), category: form.category,
      context: form.context.trim(),
    };
    saveProgress.mutate({ ...progress, bug_journal: [...bugs, entry] });
    setForm({ description: '', category: 'logic', context: '' });
  };

  const filtered = filter
    ? bugs.filter(b => b.description.toLowerCase().includes(filter.toLowerCase()) || (b.context || '').toLowerCase().includes(filter.toLowerCase()))
    : bugs;

  const categoryCounts = {};
  for (const b of bugs) categoryCounts[b.category || 'other'] = (categoryCounts[b.category || 'other'] || 0) + 1;

  return (
    <div className="page">
      <div className="page-header">
        <h2>Bug Journal</h2>
        <div className="sub">Track mistakes and common pitfalls to avoid repeating them</div>
      </div>

      {/* Add Bug */}
      <div className="card mb-24">
        <div className="card-title">Log a Bug / Mistake</div>
        <form onSubmit={handleAdd}>
          <textarea rows={3} placeholder="What went wrong? What mistake did you make?"
                    value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                    style={{ marginBottom: 8 }} />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr auto', gap: 8 }}>
            <select value={form.category} onChange={e => setForm(f => ({ ...f, category: e.target.value }))}>
              <option value="logic">Logic Error</option>
              <option value="edge_case">Edge Case</option>
              <option value="syntax">Syntax</option>
              <option value="time_complexity">Time Complexity</option>
              <option value="approach">Wrong Approach</option>
              <option value="communication">Communication</option>
              <option value="other">Other</option>
            </select>
            <input placeholder="Context (problem name, topic, etc.)" value={form.context}
                   onChange={e => setForm(f => ({ ...f, context: e.target.value }))} />
            <button type="submit" className="btn btn-solid"><Plus size={14} /> Log</button>
          </div>
        </form>
      </div>

      {/* Category Stats */}
      {Object.keys(categoryCounts).length > 0 && (
        <div className="card mb-24">
          <div className="card-title">Mistake Categories</div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {Object.entries(categoryCounts).sort((a, b) => b[1] - a[1]).map(([cat, count]) => (
              <div key={cat} style={{
                padding: '8px 14px', background: 'var(--bg2)', borderRadius: 6,
                border: '1px solid var(--bg4)',
              }}>
                <div style={{ fontSize: 16, fontWeight: 700, color: 'var(--red)' }}>{count}</div>
                <div style={{ fontSize: 9, color: 'var(--text3)' }}>{cat.replace(/_/g, ' ')}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Bug List */}
      <div className="card">
        <div className="flex-between mb-8">
          <div className="card-title" style={{ marginBottom: 0 }}>Journal ({filtered.length})</div>
          <input placeholder="Search..." value={filter} onChange={e => setFilter(e.target.value)} style={{ width: 200 }} />
        </div>
        <div style={{ maxHeight: 400, overflowY: 'auto' }}>
          {filtered.slice().reverse().map(bug => (
            <div key={bug.id || bug.date} style={{
              padding: '10px 12px', marginBottom: 6, background: 'var(--bg2)', borderRadius: 6,
              borderLeft: '3px solid var(--red)',
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span className="tag tag-red">{(bug.category || 'other').replace(/_/g, ' ')}</span>
                <span style={{ fontSize: 10, color: 'var(--text4)' }}>{bug.date}</span>
              </div>
              <div style={{ fontSize: 12, lineHeight: 1.6 }}>{bug.description}</div>
              {bug.context && <div style={{ fontSize: 10, color: 'var(--text3)', marginTop: 4 }}>Context: {bug.context}</div>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
