import { Clock, CheckCircle2, XCircle, Minus } from 'lucide-react';

const TYPE_COLORS = {
  lc: 'var(--green)', mock: 'var(--orange)', curriculum: 'var(--blue)',
  lld: 'var(--purple)', jqa: 'var(--cyan)', system_design: 'var(--pink)',
  behavioral: 'var(--gold)', drill: 'var(--green)', notes: 'var(--text2)',
};

export default function ActivityFeed({ todayLog = {} }) {
  const logs = todayLog.logs || [];
  const count = todayLog.count || 0;
  const mins = todayLog.total_minutes || 0;

  return (
    <div className="card">
      <div className="flex-between mb-8">
        <div className="card-title" style={{ marginBottom: 0 }}>Today's Activity</div>
        <div style={{ fontSize: 10, color: 'var(--text3)' }}>
          {count} items &middot; {mins} min
        </div>
      </div>
      {logs.length === 0 ? (
        <div className="empty-state">No activities logged today</div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, maxHeight: 240, overflowY: 'auto' }}>
          {logs.slice(0, 10).map((log, i) => (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: 10,
              padding: '8px 10px', background: 'var(--bg2)', borderRadius: 6,
            }}>
              <div style={{
                width: 4, height: 28, borderRadius: 2,
                background: TYPE_COLORS[log.activity_type] || 'var(--text3)',
              }} />
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12, color: 'var(--text)' }}>{log.title}</div>
                <div style={{ fontSize: 9, color: 'var(--text3)', marginTop: 2 }}>
                  {log.activity_type} {log.duration_mins ? `· ${log.duration_mins}m` : ''}
                </div>
              </div>
              <OutcomeIcon outcome={log.outcome} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function OutcomeIcon({ outcome }) {
  if (outcome === 'solved' || outcome === 'completed') return <CheckCircle2 size={14} style={{ color: 'var(--green)' }} />;
  if (outcome === 'struggled' || outcome === 'failed') return <XCircle size={14} style={{ color: 'var(--red)' }} />;
  return <Minus size={14} style={{ color: 'var(--text4)' }} />;
}
