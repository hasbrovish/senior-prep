import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

const COLORS = { Easy: '#4ecdc4', Medium: '#ffa502', Hard: '#ff4757' };

export default function LCProgressChart({ lcSync = {} }) {
  const easy = lcSync.easy || 0;
  const medium = lcSync.medium || 0;
  const hard = lcSync.hard || 0;
  const total = lcSync.total || 0;
  const java = lcSync.java_problems || 0;

  const data = [
    { name: 'Easy', value: easy },
    { name: 'Medium', value: medium },
    { name: 'Hard', value: hard },
  ].filter(d => d.value > 0);

  return (
    <div className="card">
      <div className="card-title">LeetCode Progress</div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
        <div style={{ width: 120, height: 120 }}>
          {data.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data} dataKey="value" nameKey="name"
                  cx="50%" cy="50%" innerRadius={30} outerRadius={50}
                  strokeWidth={0}
                >
                  {data.map((d) => (
                    <Cell key={d.name} fill={COLORS[d.name]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ background: 'var(--bg3)', border: '1px solid var(--bg4)', borderRadius: 6, fontSize: 11 }}
                  itemStyle={{ color: 'var(--text)' }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state" style={{ padding: 10 }}>No data</div>
          )}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 28, fontWeight: 700, fontFamily: 'var(--serif)', color: 'var(--gold)' }}>{total}</div>
          <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 8 }}>Total Solved</div>
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <Stat label="Easy" value={easy} color={COLORS.Easy} />
            <Stat label="Med" value={medium} color={COLORS.Medium} />
            <Stat label="Hard" value={hard} color={COLORS.Hard} />
            <Stat label="Java" value={java} color="var(--purple)" />
          </div>
          {lcSync.streak > 0 && (
            <div style={{ marginTop: 8, fontSize: 11, color: 'var(--orange)' }}>
              {lcSync.streak} day streak
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value, color }) {
  return (
    <div>
      <div style={{ fontSize: 16, fontWeight: 700, color }}>{value}</div>
      <div style={{ fontSize: 9, color: 'var(--text3)' }}>{label}</div>
    </div>
  );
}
