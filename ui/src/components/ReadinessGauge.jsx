import { RadialBarChart, RadialBar, PolarAngleAxis } from 'recharts';

export default function ReadinessGauge({ value = 0, label = 'Readiness' }) {
  const color = value >= 70 ? '#4ecdc4' : value >= 40 ? '#ffa502' : '#ff4757';
  const data = [{ value, fill: color }];

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div className="card-title">{label}</div>
      <div style={{ position: 'relative', width: 160, height: 160 }}>
        <RadialBarChart
          width={160} height={160}
          cx={80} cy={80}
          innerRadius={55} outerRadius={75}
          startAngle={225} endAngle={-45}
          data={data}
          barSize={12}
        >
          <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
          <RadialBar
            dataKey="value"
            cornerRadius={6}
            background={{ fill: 'var(--bg4)' }}
            angleAxisId={0}
          />
        </RadialBarChart>
        <div style={{
          position: 'absolute', top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
        }}>
          <div style={{ fontSize: 28, fontWeight: 700, fontFamily: 'var(--serif)', color }}>{value}%</div>
          <div style={{ fontSize: 9, color: 'var(--text3)', letterSpacing: 1 }}>SDE-2</div>
        </div>
      </div>
    </div>
  );
}
