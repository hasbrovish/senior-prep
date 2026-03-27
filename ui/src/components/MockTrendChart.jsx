import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function MockTrendChart({ trendData = {} }) {
  const weeks = trendData.weeks || {};
  const data = Object.entries(weeks)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([week, avg]) => ({
      week: week.slice(5),
      score: typeof avg === 'number' ? Number(avg.toFixed(1)) : 0,
    }));

  const trend = trendData.trend || 'no_data';
  const trendColor = trend === 'improving' ? 'var(--green)' : trend === 'declining' ? 'var(--red)' : 'var(--text3)';

  return (
    <div className="card">
      <div className="flex-between mb-8">
        <div className="card-title" style={{ marginBottom: 0 }}>Mock Score Trend</div>
        {trend !== 'no_data' && (
          <span className="tag" style={{ background: `${trendColor}22`, color: trendColor }}>
            {trend}
          </span>
        )}
      </div>
      {data.length > 0 ? (
        <div style={{ width: '100%', height: 180 }}>
          <ResponsiveContainer>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--bg4)" />
              <XAxis dataKey="week" tick={{ fill: 'var(--text3)', fontSize: 10 }} />
              <YAxis domain={[0, 5]} tick={{ fill: 'var(--text3)', fontSize: 10 }} />
              <Tooltip
                contentStyle={{ background: 'var(--bg3)', border: '1px solid var(--bg4)', borderRadius: 6, fontSize: 11 }}
              />
              <Line
                type="monotone" dataKey="score" stroke="var(--gold)"
                strokeWidth={2} dot={{ fill: 'var(--gold)', r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="empty-state">No mock scores yet</div>
      )}
    </div>
  );
}
