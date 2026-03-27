import { useState } from 'react';
import { useProgress, useSaveProgress } from '../hooks/useProgress';
import { useLogActivity } from '../hooks/useProgress';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import { Target, Plus, Flame, TrendingUp, RefreshCw, User } from 'lucide-react';
import StreakHeatmap from '../components/StreakHeatmap';

const PATTERNS = [
  'Arrays', 'Two Pointers', 'Sliding Window', 'Stack', 'Queue',
  'Linked List', 'Binary Search', 'Heap', 'Trees', 'Graphs',
  'DFS', 'BFS', 'Backtracking', 'Dynamic Programming', 'Greedy',
  'Trie', 'Union Find', 'Intervals', 'Matrix', 'Bit Manipulation',
  'Math', 'Sorting', 'Hashing', 'String', 'Design',
];

export default function LeetCode() {
  const { data: progress, isLoading } = useProgress();
  const saveProgress = useSaveProgress();
  const logActivity = useLogActivity();
  const qc = useQueryClient();
  const [form, setForm] = useState({ name: '', pattern: '', difficulty: 'Medium', time: '', hard: false, notes: '' });
  const [filter, setFilter] = useState('');
  const [usernameInput, setUsernameInput] = useState('');

  const syncMut = useMutation({
    mutationFn: api.syncLeetCode,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['progress'] }),
  });
  const usernameMut = useMutation({
    mutationFn: api.setLcUsername,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['progress'] }),
  });

  if (isLoading) return <div className="page"><div className="loading">Loading...</div></div>;

  const lcDone = progress?.lc_done || [];
  const lcSync = progress?.lc_sync || {};
  const dailyLogs = progress?.daily_logs || {};

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.name.trim()) return;

    const entry = { name: form.name.trim(), date: new Date().toISOString().slice(0, 10) };
    if (form.pattern) entry.pattern = form.pattern;
    if (form.time) entry.time_mins = parseInt(form.time);
    if (form.hard) entry.hard = true;

    const updated = { ...progress, lc_done: [...lcDone, entry] };
    saveProgress.mutate(updated);
    logActivity.mutate({
      activity_type: 'lc', title: form.name.trim(),
      duration_mins: form.time ? parseInt(form.time) : undefined,
      difficulty: form.difficulty, outcome: 'completed',
      notes: form.notes || undefined,
    });
    setForm({ name: '', pattern: '', difficulty: 'Medium', time: '', hard: false, notes: '' });
  };

  const filteredDone = filter
    ? lcDone.filter(p => p.name?.toLowerCase().includes(filter.toLowerCase()) || p.pattern?.toLowerCase().includes(filter.toLowerCase()))
    : lcDone;

  const patternCounts = {};
  for (const p of lcDone) {
    if (p.pattern) patternCounts[p.pattern] = (patternCounts[p.pattern] || 0) + 1;
  }
  const topPatterns = Object.entries(patternCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);

  return (
    <div className="page">
      <div className="page-header">
        <h2>LeetCode Tracker</h2>
        <div className="sub">Log problems, track patterns, build your heatmap</div>
      </div>

      {/* Sync Bar */}
      <div className="card mb-24" style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '12px 16px' }}>
        {lcSync.username ? (
          <>
            <User size={14} style={{ color: 'var(--text3)' }} />
            <span style={{ fontSize: 12, color: 'var(--text2)' }}>{lcSync.username}</span>
            <span style={{ fontSize: 10, color: 'var(--text3)' }}>
              {lcSync.last_sync ? `Last sync: ${lcSync.last_sync}` : 'Never synced'}
            </span>
            <div style={{ flex: 1 }} />
            <button className="btn btn-gold btn-sm" onClick={() => syncMut.mutate()} disabled={syncMut.isPending}>
              <RefreshCw size={12} style={{ animation: syncMut.isPending ? 'spin 1s linear infinite' : 'none' }} />
              {syncMut.isPending ? 'Syncing...' : 'Sync Now'}
            </button>
          </>
        ) : (
          <>
            <User size={14} style={{ color: 'var(--gold)' }} />
            <input
              placeholder="LeetCode username"
              value={usernameInput}
              onChange={e => setUsernameInput(e.target.value)}
              style={{ flex: 1 }}
              onKeyDown={e => e.key === 'Enter' && usernameInput.trim() && usernameMut.mutate(usernameInput.trim())}
            />
            <button className="btn btn-solid btn-sm"
              onClick={() => usernameInput.trim() && usernameMut.mutate(usernameInput.trim())}
              disabled={usernameMut.isPending || !usernameInput.trim()}>
              Connect
            </button>
          </>
        )}
        {syncMut.isError && <span style={{ fontSize: 10, color: 'var(--red)' }}>{syncMut.error?.message}</span>}
        {usernameMut.isError && <span style={{ fontSize: 10, color: 'var(--red)' }}>Failed to set username</span>}
      </div>

      {/* Stats */}
      <div className="grid grid-4 mb-24">
        <div className="card" style={{ textAlign: 'center' }}>
          <div className="card-value" style={{ color: 'var(--gold)' }}>{lcSync.total || lcDone.length}</div>
          <div style={{ fontSize: 9, color: 'var(--text3)' }}>Total</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div className="card-value" style={{ color: 'var(--green)' }}>{lcSync.easy || 0}</div>
          <div style={{ fontSize: 9, color: 'var(--text3)' }}>Easy</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div className="card-value" style={{ color: 'var(--orange)' }}>{lcSync.medium || 0}</div>
          <div style={{ fontSize: 9, color: 'var(--text3)' }}>Medium</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div className="card-value" style={{ color: 'var(--red)' }}>{lcSync.hard || 0}</div>
          <div style={{ fontSize: 9, color: 'var(--text3)' }}>Hard</div>
        </div>
      </div>

      {/* Log Form */}
      <div className="card mb-24">
        <div className="card-title">Log Problem</div>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 80px', gap: 8, marginBottom: 8 }}>
            <input placeholder="Problem name (e.g. Two Sum)" value={form.name}
                   onChange={e => setForm(f => ({ ...f, name: e.target.value }))} />
            <select value={form.pattern} onChange={e => setForm(f => ({ ...f, pattern: e.target.value }))}>
              <option value="">Pattern</option>
              {PATTERNS.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
            <select value={form.difficulty} onChange={e => setForm(f => ({ ...f, difficulty: e.target.value }))}>
              <option>Easy</option><option>Medium</option><option>Hard</option>
            </select>
            <input type="number" placeholder="Min" value={form.time}
                   onChange={e => setForm(f => ({ ...f, time: e.target.value }))} />
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <label style={{ fontSize: 11, display: 'flex', alignItems: 'center', gap: 4, color: 'var(--text3)' }}>
              <input type="checkbox" checked={form.hard}
                     onChange={e => setForm(f => ({ ...f, hard: e.target.checked }))} /> Struggled
            </label>
            <div style={{ flex: 1 }} />
            <button type="submit" className="btn btn-solid" disabled={saveProgress.isPending}>
              <Plus size={14} /> Log
            </button>
          </div>
        </form>
      </div>

      {/* Heatmap + Patterns */}
      <div className="grid grid-2 mb-24">
        <StreakHeatmap dailyLogs={dailyLogs} lcDone={lcDone} />
        <div className="card">
          <div className="card-title">Pattern Distribution</div>
          {topPatterns.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {topPatterns.map(([pattern, count]) => (
                <div key={pattern} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: 11, flex: 1 }}>{pattern}</span>
                  <div className="progress-bar" style={{ width: 100 }}>
                    <div className="progress-fill" style={{
                      width: `${(count / topPatterns[0][1]) * 100}%`, background: 'var(--gold)',
                    }} />
                  </div>
                  <span style={{ fontSize: 11, fontWeight: 600, minWidth: 24, textAlign: 'right' }}>{count}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">Log problems with patterns to see distribution</div>
          )}
        </div>
      </div>

      {/* History */}
      <div className="card">
        <div className="flex-between mb-8">
          <div className="card-title" style={{ marginBottom: 0 }}>History ({filteredDone.length})</div>
          <input placeholder="Filter..." value={filter} onChange={e => setFilter(e.target.value)}
                 style={{ width: 200 }} />
        </div>
        <div style={{ maxHeight: 300, overflowY: 'auto' }}>
          {filteredDone.slice().reverse().slice(0, 50).map((p, i) => (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: 8,
              padding: '6px 0', borderBottom: '1px solid var(--bg4)', fontSize: 12,
            }}>
              <span style={{ color: 'var(--text3)', fontSize: 10, minWidth: 70 }}>{p.date}</span>
              <span style={{ flex: 1 }}>{p.name}</span>
              {p.pattern && <span className="tag tag-purple">{p.pattern}</span>}
              {p.hard && <span className="tag tag-red">hard</span>}
              {p.time_mins && <span style={{ fontSize: 10, color: 'var(--text3)' }}>{p.time_mins}m</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
