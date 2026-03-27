import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import { useProgress, useSaveProgress } from '../hooks/useProgress';
import { Download, Upload, Trash2, RefreshCw, Database, Wifi } from 'lucide-react';

export default function SettingsPage() {
  const { data: progress } = useProgress();
  const saveProgress = useSaveProgress();
  const qc = useQueryClient();

  const { data: health } = useQuery({
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

  const handleReset = () => {
    if (!window.confirm('This will reset all portal data. Progress data will NOT be affected. Continue?')) return;
    api.savePortalData({
      resources: [], notes: [], goals: [], career: {},
      coach_history: [], sessions: {},
    });
    qc.invalidateQueries();
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2>Settings</h2>
        <div className="sub">System status, data management, and configuration</div>
      </div>

      {/* System Status */}
      <div className="card mb-24">
        <div className="card-title">System Status</div>
        <div className="grid grid-3">
          <StatusItem icon={Wifi} label="Server" value={health ? 'Online' : 'Offline'}
                      color={health ? 'var(--green)' : 'var(--red)'} detail={health?.env || ''} />
          <StatusItem icon={Database} label="KB Chunks"
                      value={kbStats?.total_chunks || kbStats?.chunks || '—'}
                      color="var(--blue)" detail={kbStats?.categories ? `${Object.keys(kbStats.categories).length} categories` : ''} />
          <StatusItem icon={RefreshCw} label="Last Sync"
                      value={progress?.lc_sync?.last_sync ? new Date(progress.lc_sync.last_sync).toLocaleDateString() : 'Never'}
                      color="var(--gold)" detail={progress?.lc_sync?.username || ''} />
        </div>
      </div>

      {/* Knowledge Base */}
      <div className="card mb-24">
        <div className="flex-between mb-8">
          <div className="card-title" style={{ marginBottom: 0 }}>Knowledge Base</div>
          <button className="btn btn-gold btn-sm" onClick={() => reindexKb.mutate()} disabled={reindexKb.isPending}>
            <RefreshCw size={12} className={reindexKb.isPending ? 'loading' : ''} /> Reindex
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
