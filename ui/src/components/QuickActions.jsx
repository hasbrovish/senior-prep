import { useNavigate } from 'react-router-dom';
import { Swords, Timer, Code2, Brain, Target, RefreshCw } from 'lucide-react';

export default function QuickActions({ onSync }) {
  const nav = useNavigate();

  const actions = [
    { icon: Swords, label: 'Start Drill', color: 'var(--green)', onClick: () => nav('/drills') },
    { icon: Timer, label: 'Mock Interview', color: 'var(--orange)', onClick: () => nav('/mock') },
    { icon: Code2, label: 'LLD Practice', color: 'var(--purple)', onClick: () => nav('/lld') },
    { icon: Brain, label: 'Behavioral', color: 'var(--pink)', onClick: () => nav('/behavioral') },
    { icon: Target, label: 'Log LeetCode', color: 'var(--cyan)', onClick: () => nav('/leetcode') },
    { icon: RefreshCw, label: 'Sync LC', color: 'var(--gold)', onClick: onSync },
  ];

  return (
    <div className="card">
      <div className="card-title">Quick Actions</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
        {actions.map((a) => (
          <button
            key={a.label}
            onClick={a.onClick}
            style={{
              display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6,
              padding: '12px 8px', background: 'var(--bg2)', borderRadius: 8,
              border: '1px solid var(--bg4)', cursor: 'pointer', transition: 'all 0.15s',
            }}
            onMouseOver={e => e.currentTarget.style.borderColor = a.color}
            onMouseOut={e => e.currentTarget.style.borderColor = 'var(--bg4)'}
          >
            <a.icon size={18} style={{ color: a.color }} />
            <span style={{ fontSize: 9, color: 'var(--text3)', letterSpacing: 0.5 }}>{a.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
