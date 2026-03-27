import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import { useProgress, useSaveProgress } from '../hooks/useProgress';
import { Download, Upload, Trash2, RefreshCw, Database, Wifi, User, Check } from 'lucide-react';

export default function SettingsPage() {
  const { data: progress } = useProgress();
  const saveProgress = useSaveProgress();
  const qc = useQueryClient();
  const [usernameInput, setUsernameInput] = useState('');
  const [resetMsg, setResetMsg] = useState('');

  const { data: health, isLoading: healthLoading, isError: healthError } = useQuery({
    queryKey: ['health'],
    queryFn: () => api.get('/health'),
    staleTime: 30000,
  });
  const { data: kbStats } = useQuery({
    queryKey: ['kbStats'],
    queryFn: api.getKbStats,
    staleTime: 60000,
  });

  const reindexKb = useMutation({
    mutationFn: () => api.post('/api/coach/kb/reindex'),
  });

  const usernameMut = useMutation({
    mutationFn: api.setLcUsername,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['progress'] });
      setUsernameInput('');
    },
  });

  const syncMut = useMutation({
    mutationFn: api.syncLeetCode,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['progress'] }),
  });

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(progress, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `prepforge-export-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImport = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      saveProgress.mutate(data);
    } catch {
      alert('Invalid JSON file');
    }
  };

  const handleReset = async () => {
    if (!window.confirm('This will reset all portal data. Progress data will NOT be affected. Continue?')) return;
    try {
      await api.savePortalData({
        resources: [], notes: [], goals: [], career: {},
        coach_history: [], sessions: {},
      });
      qc.invalidateQueries();
      setResetMsg('Portal data reset successfully');
    } catch {
      setResetMsg('Reset failed');
    }
  };

  const lcSync = progress?.lc_sync || {};
  const lcUsername = lcSync.username || '';

  return (
    <div className="page">
      <div className="page-header">
        <h2>Settings</h2>
        <div className="sub">System status, data management, and configuration</div>
      </div>

      {/* LeetCode Account */}
      <div className="card mb-24">
        <div className="card-title">LeetCode Account</div>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 12 }}>
          <User size={16} style={{ color: lcUsername ? 'var(--green)' : 'var(--text3)' }} />
          {lcUsername ? (
            <>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 14, fontWeight: 600 }}>{lcUsername}</div>
                <div style={{ fontSize: 10, color: 'var(--text3)' }}>
                  {lcSync.total || 0} problems | Last sync: {lcSync.last_sync || 'Never'}
                </div>
              </div>
              <button className="btn btn-gold btn-sm" onClick={() => syncMut.mutate()} disabled={syncMut.isPending}>
                <RefreshCw size={12} style={{ animation: syncMut.isPending ? 'spin 1s linear infinite' : 'none' }} />
                {syncMut.isPending ? 'Syncing...' : 'Sync Now'}
              </button>
            </>
          ) : (
            <div style={{ fontSize: 12, color: 'var(--text3)' }}>No LeetCode account connected</div>
          )}
        </div>

        <div style={{ display: 'flex', gap: 8 }}>
          <input
            placeholder={lcUsername ? 'Change username...' : 'Enter LeetCode username'}
            value={usernameInput}
            onChange={e => setUsernameInput(e.target.value)}
            style={{ flex: 1 }}
            onKeyDown={e => e.key === 'Enter' && usernameInput.trim() && usernameMut.mutate(usernameInput.trim())}
          />
          <button className="btn btn-solid btn-sm"
            onClick={() => usernameInput.trim() && usernameMut.mutate(usernameInput.trim())}
            disabled={usernameMut.isPending || !usernameInput.trim()}>
            {lcUsername ? 'Update' : 'Connect'}
          </button>
        </div>

        {usernameMut.isSuccess && (
          <div style={{ marginTop: 8, fontSize: 11, color: 'var(--green)', display: 'flex', alignItems: 'center', gap: 4 }}>
            <Check size={12} /> Username updated successfully
          </div>
        )}
        {usernameMut.isError && (
          <div style={{ marginTop: 8, fontSize: 11, color: 'var(--red)' }}>
            Failed: {usernameMut.error?.message}
          </div>
        )}
        {syncMut.isSuccess && (
          <div style={{ marginTop: 8, fontSize: 11, color: 'var(--green)', display: 'flex', alignItems: 'center', gap: 4 }}>
            <Check size={12} /> Synced — {progress?.lc_sync?.total || 0} problems
          </div>
        )}
        {syncMut.isError && (
          <div style={{ marginTop: 8, fontSize: 11, color: 'var(--red)' }}>
            Sync failed: {syncMut.error?.message}
          </div>
        )}
      </div>

      {/* System Status */}
      <div className="card mb-24">
        <div className="card-title">System Status</div>
        <div className="grid grid-3">
          <StatusItem icon={Wifi} label="Server"
                      value={healthLoading ? 'Checking...' : healthError ? 'Offline' : 'Online'}
                      color={healthLoading ? 'var(--text3)' : healthError ? 'var(--red)' : 'var(--green)'}
                      detail={health?.env || ''} />
          <StatusItem icon={Database} label="KB Chunks"
                      value={kbStats?.total_chunks || kbStats?.chunks || '—'}
                      color="var(--blue)" detail={kbStats?.categories ? `${Object.keys(kbStats.categories).length} categories` : ''} />
          <StatusItem icon={RefreshCw} label="Last Sync"
                      value={lcSync.last_sync ? new Date(lcSync.last_sync).toLocaleDateString() : 'Never'}
                      color="var(--gold)" detail={lcUsername || 'Not connected'} />
        </div>
      </div>

      {/* Knowledge Base */}
      <div className="card mb-24">
        <div className="flex-between mb-8">
          <div className="card-title" style={{ marginBottom: 0 }}>Knowledge Base</div>
          <button className="btn btn-gold btn-sm" onClick={() => reindexKb.mutate()} disabled={reindexKb.isPending}>
            <RefreshCw size={12} /> Reindex
          </button>
        </div>
        {kbStats && (
          <div style={{ fontSize: 12, lineHeight: 1.8 }}>
            {Object.entries(kbStats).filter(([k]) => k !== 'categories').map(([key, val]) => (
              <div key={key} style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--bg4)', padding: '4px 0' }}>
                <span style={{ color: 'var(--text3)' }}>{key.replace(/_/g, ' ')}</span>
                <span>{typeof val === 'object' ? JSON.stringify(val) : String(val)}</span>
              </div>
            ))}
          </div>
        )}
        {reindexKb.isSuccess && <div style={{ marginTop: 8, fontSize: 11, color: 'var(--green)' }}>Reindex triggered</div>}
      </div>

      {/* Data Management */}
      <div className="card mb-24">
        <div className="card-title">Data Management</div>
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          <button className="btn btn-gold" onClick={handleExport}>
            <Download size={14} /> Export Progress
          </button>
          <label className="btn btn-gold" style={{ cursor: 'pointer' }}>
            <Upload size={14} /> Import Progress
            <input type="file" accept=".json" onChange={handleImport} style={{ display: 'none' }} />
          </label>
          <button className="btn btn-red" onClick={handleReset}>
            <Trash2 size={14} /> Reset Portal Data
          </button>
        </div>
        {resetMsg && <div style={{ marginTop: 8, fontSize: 11, color: resetMsg.includes('success') ? 'var(--green)' : 'var(--red)' }}>{resetMsg}</div>}
      </div>

      {/* Quick Reference */}
      <div className="card">
        <div className="card-title">Quick Reference</div>
        <div style={{ fontSize: 12, lineHeight: 1.8, color: 'var(--text3)' }}>
          <div><strong style={{ color: 'var(--text)' }}>Dev server:</strong> cd ui && npm run dev</div>
          <div><strong style={{ color: 'var(--text)' }}>API server:</strong> uvicorn app.main:app --reload --port 5555</div>
          <div><strong style={{ color: 'var(--text)' }}>Build for production:</strong> cd ui && npm run build</div>
          <div><strong style={{ color: 'var(--text)' }}>CLI still works:</strong> python prep.py [command]</div>
        </div>
      </div>
    </div>
  );
}

function StatusItem({ icon: Icon, label, value, color, detail }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
      <Icon size={18} style={{ color }} />
      <div>
        <div style={{ fontSize: 14, fontWeight: 600, color }}>{value}</div>
        <div style={{ fontSize: 9, color: 'var(--text3)' }}>{label}{detail ? ` · ${detail}` : ''}</div>
      </div>
    </div>
  );
}
