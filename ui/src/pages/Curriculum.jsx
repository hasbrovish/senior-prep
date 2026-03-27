import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api';
import { useProgress, useSaveProgress, useWeeklyPlan } from '../hooks/useProgress';
import { BookOpen, ExternalLink, CheckCircle2, Filter } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const CATEGORY_COLORS = {
  dsa: 'var(--green)', 'system-design': 'var(--orange)', lld: 'var(--purple)',
  behavioral: 'var(--pink)', java: 'var(--blue)', 'ml-system-design': 'var(--cyan)',
};

export default function Curriculum() {
  const [weekFilter, setWeekFilter] = useState(0);
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [sourceFilter, setSourceFilter] = useState('all');

  const { data: curriculum, isLoading } = useQuery({
    queryKey: ['curriculum'], queryFn: api.getCurriculum, staleTime: 300000,
  });
  const { data: progress } = useProgress();
  const saveProgress = useSaveProgress();
  const { data: weeklyPlan } = useWeeklyPlan();

  const items = curriculum?.items || [];
  const done = new Set(progress?.curriculum_done || []);

  const categories = useMemo(() => [...new Set(items.map(i => i.category))], [items]);
  const sources = useMemo(() => [...new Set(items.map(i => i.source))], [items]);
  const maxWeek = useMemo(() => Math.max(...items.map(i => i.week_start), 1), [items]);

  const filtered = useMemo(() => {
    return items.filter(item => {
      if (weekFilter > 0 && item.week_start !== weekFilter) return false;
      if (categoryFilter !== 'all' && item.category !== categoryFilter) return false;
      if (sourceFilter !== 'all' && item.source !== sourceFilter) return false;
      return true;
    });
  }, [items, weekFilter, categoryFilter, sourceFilter]);

  const toggleDone = (id) => {
    const newDone = done.has(id)
      ? (progress?.curriculum_done || []).filter(d => d !== id)
      : [...(progress?.curriculum_done || []), id];
    saveProgress.mutate({ ...progress, curriculum_done: newDone });
  };

  const categoryProgress = useMemo(() => {
    const map = {};
    for (const item of items) {
      if (!map[item.category]) map[item.category] = { total: 0, done: 0 };
      map[item.category].total++;
      if (done.has(item.id)) map[item.category].done++;
    }
    return Object.entries(map).map(([cat, { total, done: d }]) => ({
      category: cat, total, done: d, pct: Math.round((d / total) * 100),
    }));
  }, [items, done]);

  const overallPct = items.length > 0 ? Math.round((done.size / items.length) * 100) : 0;

  if (isLoading) return <div className="page"><div className="loading">Loading curriculum...</div></div>;

  return (
    <div className="page">
      <div className="page-header">
        <h2>Curriculum</h2>
        <div className="sub">{done.size}/{items.length} completed ({overallPct}%)</div>
      </div>

      {/* Overall Progress */}
      <div className="card mb-24">
        <div className="flex-between mb-8">
          <div className="card-title" style={{ marginBottom: 0 }}>Progress by Category</div>
          <span style={{ fontSize: 14, fontWeight: 700, color: 'var(--gold)' }}>{overallPct}%</span>
        </div>
        <div className="progress-bar mb-16">
          <div className="progress-fill" style={{ width: `${overallPct}%`, background: 'var(--gold)' }} />
        </div>
        {categoryProgress.length > 0 && (
          <div style={{ width: '100%', height: 180 }}>
            <ResponsiveContainer>
              <BarChart data={categoryProgress}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--bg4)" />
                <XAxis dataKey="category" tick={{ fill: 'var(--text3)', fontSize: 10 }} />
                <YAxis tick={{ fill: 'var(--text3)', fontSize: 10 }} />
                <Tooltip contentStyle={{ background: 'var(--bg3)', border: '1px solid var(--bg4)', borderRadius: 6, fontSize: 11 }} />
                <Bar dataKey="done" fill="var(--gold)" name="Done" radius={[4, 4, 0, 0]} />
                <Bar dataKey="total" fill="var(--bg4)" name="Total" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="card mb-16" style={{ padding: '10px 16px' }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
          <Filter size={14} style={{ color: 'var(--text3)' }} />
          <select value={weekFilter} onChange={e => setWeekFilter(Number(e.target.value))} style={{ width: 100 }}>
            <option value={0}>All Weeks</option>
            {Array.from({ length: maxWeek }, (_, i) => (
              <option key={i + 1} value={i + 1}>Week {i + 1}</option>
            ))}
          </select>
          <select value={categoryFilter} onChange={e => setCategoryFilter(e.target.value)} style={{ width: 130 }}>
            <option value="all">All Categories</option>
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <select value={sourceFilter} onChange={e => setSourceFilter(e.target.value)} style={{ width: 160 }}>
            <option value="all">All Sources</option>
            {sources.map(s => <option key={s} value={s}>{s === 'hi' ? 'Hello Interview' : s === 'pp' ? 'Programming Pathshala' : s}</option>)}
          </select>
          <span style={{ fontSize: 10, color: 'var(--text3)' }}>{filtered.length} items</span>
        </div>
      </div>

      {/* Weekly Plan */}
      {weeklyPlan?.plan && (
        <div className="card mb-24" style={{ borderLeft: '3px solid var(--gold)' }}>
          <div className="card-title">AI Weekly Plan</div>
          <div style={{ fontSize: 12, lineHeight: 1.7, whiteSpace: 'pre-wrap', maxHeight: 200, overflowY: 'auto' }}>
            {weeklyPlan.plan}
          </div>
        </div>
      )}

      {/* Item List */}
      <div className="card">
        <div className="card-title">Curriculum Items</div>
        <div style={{ maxHeight: 600, overflowY: 'auto' }}>
          {filtered.map(item => {
            const isDone = done.has(item.id);
            return (
              <div key={item.id} style={{
                display: 'flex', alignItems: 'center', gap: 10,
                padding: '8px 10px', marginBottom: 3, borderRadius: 6,
                background: isDone ? 'var(--bg2)' : 'transparent',
                opacity: isDone ? 0.6 : 1,
              }}>
                <button onClick={() => toggleDone(item.id)} style={{ flexShrink: 0 }}>
                  <CheckCircle2 size={16} style={{ color: isDone ? 'var(--green)' : 'var(--bg4)' }} />
                </button>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 12 }}>{item.title}</div>
                  <div style={{ fontSize: 9, color: 'var(--text3)', marginTop: 2 }}>
                    W{item.week_start} &middot; {item.section} &middot; {item.source_label || item.source}
                  </div>
                </div>
                <span className="tag" style={{
                  background: `${CATEGORY_COLORS[item.category] || 'var(--text3)'}22`,
                  color: CATEGORY_COLORS[item.category] || 'var(--text3)',
                }}>
                  {item.category}
                </span>
                {item.url && (
                  <a href={item.url} target="_blank" rel="noopener noreferrer" style={{ flexShrink: 0 }}>
                    <ExternalLink size={12} style={{ color: 'var(--text3)' }} />
                  </a>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
