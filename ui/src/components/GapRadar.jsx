import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts';

const SEVERITY_SCORE = { CRITICAL: 1, HIGH: 2, MODERATE: 3, LOW: 4, NONE: 5 };

export default function GapRadar({ gaps = [] }) {
  const areaMap = {};
  for (const g of gaps) {
    const area = g.area || 'Other';
    const score = SEVERITY_SCORE[g.severity] || 3;
    areaMap[area] = score;
  }

  const areas = ['DSA (Java)', 'Hard Problems', 'System Design', 'LLD', 'Behavioral', 'Applications'];
  const data = areas.map(area => {
    const key = Object.keys(areaMap).find(k => area.toLowerCase().includes(k.toLowerCase()) || k.toLowerCase().includes(area.toLowerCase().split(' ')[0]));
    return {
      area: area.length > 12 ? area.slice(0, 12) + '..' : area,
      fullArea: area,
      score: key ? areaMap[key] : 3,
    };
  });

  if (gaps.length === 0) {
    return (
      <div className="card">
        <div className="card-title">Gap Analysis</div>
        <div className="empty-state">No gap data yet</div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-title">Gap Analysis</div>
      <div style={{ width: '100%', height: 220 }}>
        <ResponsiveContainer>
          <RadarChart data={data} cx="50%" cy="50%" outerRadius="70%">
            <PolarGrid stroke="var(--bg4)" />
            <PolarAngleAxis
              dataKey="area"
              tick={{ fill: 'var(--text3)', fontSize: 9 }}
            />
            <Radar
              dataKey="score"
              stroke="var(--gold)"
              fill="var(--gold)"
              fillOpacity={0.15}
              strokeWidth={2}
            />
            <Tooltip
              contentStyle={{ background: 'var(--bg3)', border: '1px solid var(--bg4)', borderRadius: 6, fontSize: 11 }}
              formatter={(val) => {
                const labels = { 1: 'Critical', 2: 'High gap', 3: 'Moderate', 4: 'Low gap', 5: 'Strong' };
                return [labels[val] || val, 'Status'];
              }}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
