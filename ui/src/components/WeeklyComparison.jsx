import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function WeeklyComparison({ planStats = {} }) {
  const todayCount = planStats.today_count || 0;
  const weekCount = planStats.week_count || 0;
  const byType = planStats.by_type_7d || {};
  const avgConf = planStats.avg_confidence_7d || 0;

  const typeData = Object.entries(byType).map(([type, count]) => ({
    type: type.length > 8 ? type.slice(0, 8) : type,
    count,
  })).sort((a, b) => b.count - a.count).slice(0, 8);

  return (
    <div className="card">
      <div className="card-title">7-Day Activity Breakdown</div>
      <div style={{ display: 'flex', gap: 16, marginBottom: 12 }}>
        <MiniStat label="Today" value={todayCount} />
        <MiniStat label="This Week" value={weekCount} />
        <MiniStat label="Avg Confidence" value={avgConf ? avgConf.toFixed(1) : '-'} />
      </div>
      {typeData.length > 0 ? (
        <div style={{ width: '100%', height: 160 }}>
          <ResponsiveContainer>
            <BarChart data={typeData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="var(--bg4)" horizontal={false} />
              <XAxis type="number" tick={{ fill: 'var(--text3)', fontSize: 10 }} />
              <YAxis type="category" dataKey="type" tick={{ fill: 'var(--text3)', fontSize: 10 }} width={70} />
              <Tooltip
                contentStyle={{ background: 'var(--bg3)', border: '1px solid var(--bg4)', borderRadius: 6, fontSize: 11 }}
              />
              <Bar dataKey="count" fill="var(--gold)" radius={[0, 4, 4, 0]} barSize={14} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="empty-state">No activity data this week</div>
      )}
    </div>
  );
}

function MiniStat({ label, value }) {
  return (
    <div>
      <div style={{ fontSize: 20, fontWeight: 700, fontFamily: 'var(--serif)', color: 'var(--gold)' }}>{value}</div>
      <div style={{ fontSize: 9, color: 'var(--text3)' }}>{label}</div>
    </div>
  );
}
