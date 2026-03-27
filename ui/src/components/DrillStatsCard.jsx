import { Flame, Target, Coffee } from 'lucide-react';

export default function DrillStatsCard({ stats = {} }) {
  const drillStats = stats.stats || {};
  const total = drillStats.total || 0;
  const java = drillStats.java || 0;
  const streak = drillStats.streak || 0;

  return (
    <div className="card">
      <div className="card-title">Drill Progress</div>
      <div style={{ display: 'flex', gap: 20 }}>
        <StatItem icon={Target} label="Total Done" value={total} color="var(--green)" />
        <StatItem icon={Coffee} label="Java" value={java} color="var(--purple)" />
        <StatItem icon={Flame} label="Streak" value={`${streak}d`} color="var(--orange)" />
      </div>
    </div>
  );
}

function StatItem({ icon: Icon, label, value, color }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <Icon size={16} style={{ color }} />
      <div>
        <div style={{ fontSize: 18, fontWeight: 700, fontFamily: 'var(--serif)', color }}>{value}</div>
        <div style={{ fontSize: 9, color: 'var(--text3)' }}>{label}</div>
      </div>
    </div>
  );
}
