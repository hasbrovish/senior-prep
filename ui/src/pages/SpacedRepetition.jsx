import { useState, useMemo } from 'react';
import { useProgress, useSaveProgress } from '../hooks/useProgress';
import { Plus, Clock, CheckCircle2 } from 'lucide-react';

export default function SpacedRepetition() {
  const { data: progress, isLoading } = useProgress();
  const saveProgress = useSaveProgress();
  const [newTopic, setNewTopic] = useState('');
  const [newCategory, setNewCategory] = useState('dsa');

  if (isLoading) return <div className="page"><div className="loading">Loading...</div></div>;

  const sr = progress?.spaced_repetition || [];
  const today = new Date().toISOString().slice(0, 10);

  const { due, upcoming, mastered } = useMemo(() => {
    const d = [], u = [], m = [];
    for (const item of sr) {
      if (item.confidence >= 5 && item.reviews >= 3) m.push(item);
      else if (!item.next_review || item.next_review <= today) d.push(item);
      else u.push(item);
    }
    d.sort((a, b) => (a.confidence || 0) - (b.confidence || 0));
    u.sort((a, b) => (a.next_review || '').localeCompare(b.next_review || ''));
    return { due: d, upcoming: u, mastered: m };
  }, [sr, today]);

  const handleAdd = (e) => {
    e.preventDefault();
    if (!newTopic.trim()) return;
    const item = {
      id: Date.now(), topic: newTopic.trim(), category: newCategory,
      confidence: 0, reviews: 0, next_review: today, added: today,
    };
    saveProgress.mutate({ ...progress, spaced_repetition: [...sr, item] });
    setNewTopic('');
  };

  const handleReview = (id, confidence) => {
    const intervals = [0, 1, 3, 7, 14, 30];
    const nextDate = new Date();
    nextDate.setDate(nextDate.getDate() + (intervals[confidence] || 7));

    const updated = sr.map(item =>
      item.id === id ? {
        ...item, confidence, reviews: (item.reviews || 0) + 1,
        next_review: nextDate.toISOString().slice(0, 10),
        last_reviewed: today,
      } : item
    );
    saveProgress.mutate({ ...progress, spaced_repetition: updated });
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2>Spaced Repetition</h2>
        <div className="sub">{due.length} due today &middot; {sr.length} total topics &middot; {mastered.length} mastered</div>
      </div>

      {/* Add Topic */}
      <div className="card mb-24">
        <div className="card-title">Add Topic</div>
        <form onSubmit={handleAdd} style={{ display: 'flex', gap: 8 }}>
          <input placeholder="Topic name" value={newTopic} onChange={e => setNewTopic(e.target.value)} style={{ flex: 1 }} />
          <select value={newCategory} onChange={e => setNewCategory(e.target.value)} style={{ width: 120 }}>
            <option value="dsa">DSA</option>
            <option value="system_design">System Design</option>
            <option value="lld">LLD</option>
            <option value="java">Java</option>
            <option value="behavioral">Behavioral</option>
            <option value="other">Other</option>
          </select>
          <button type="submit" className="btn btn-solid"><Plus size={14} /> Add</button>
        </form>
      </div>

      {/* Due for Review */}
      <div className="card mb-24">
        <div className="card-title">Due for Review ({due.length})</div>
        {due.length === 0 ? (
          <div className="empty-state">Nothing due! Add topics or wait for scheduled reviews.</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {due.map(item => (
              <div key={item.id} style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '10px 14px', background: 'var(--bg2)', borderRadius: 8,
              }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>{item.topic}</div>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginTop: 2 }}>
                    {item.category} &middot; {item.reviews || 0} reviews
                  </div>
                </div>
                <div style={{ display: 'flex', gap: 4 }}>
                  {[1, 2, 3, 4, 5].map(c => (
                    <button key={c} onClick={() => handleReview(item.id, c)}
                      title={['Again', 'Hard', 'OK', 'Good', 'Easy'][c - 1]}
                      style={{
                        padding: '4px 8px', borderRadius: 4, fontSize: 11, fontWeight: 600,
                        background: c <= 2 ? 'rgba(255,71,87,0.1)' : c <= 3 ? 'rgba(255,165,2,0.1)' : 'rgba(78,205,196,0.1)',
                        color: c <= 2 ? 'var(--red)' : c <= 3 ? 'var(--orange)' : 'var(--green)',
                        border: '1px solid transparent',
                      }}>
                      {c}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Upcoming + Mastered */}
      <div className="grid grid-2">
        <div className="card">
          <div className="card-title">Upcoming ({upcoming.length})</div>
          <div style={{ maxHeight: 200, overflowY: 'auto' }}>
            {upcoming.slice(0, 20).map(item => (
              <div key={item.id} style={{
                display: 'flex', alignItems: 'center', gap: 8,
                padding: '6px 0', borderBottom: '1px solid var(--bg4)', fontSize: 11,
              }}>
                <Clock size={12} style={{ color: 'var(--text4)' }} />
                <span style={{ flex: 1 }}>{item.topic}</span>
                <span style={{ color: 'var(--text3)', fontSize: 10 }}>{item.next_review}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="card">
          <div className="card-title">Mastered ({mastered.length})</div>
          <div style={{ maxHeight: 200, overflowY: 'auto' }}>
            {mastered.map(item => (
              <div key={item.id} style={{
                display: 'flex', alignItems: 'center', gap: 8,
                padding: '6px 0', borderBottom: '1px solid var(--bg4)', fontSize: 11,
              }}>
                <CheckCircle2 size={12} style={{ color: 'var(--green)' }} />
                <span style={{ flex: 1 }}>{item.topic}</span>
                <span className="tag tag-green">{item.reviews} reviews</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
