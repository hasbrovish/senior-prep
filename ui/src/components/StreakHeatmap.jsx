import { useMemo } from 'react';

export default function StreakHeatmap({ dailyLogs = {}, lcDone = [] }) {
  const cells = useMemo(() => {
    const today = new Date();
    const grid = [];
    for (let i = 119; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const key = d.toISOString().slice(0, 10);
      const logCount = (dailyLogs[key] || []).length;
      const lcCount = lcDone.filter(p => p.date === key).length;
      const intensity = Math.min(logCount + lcCount, 5);
      grid.push({ date: key, intensity, day: d.getDay(), weekOffset: Math.floor(i / 7) });
    }
    return grid;
  }, [dailyLogs, lcDone]);

  const getColor = (intensity) => {
    if (intensity === 0) return 'var(--bg4)';
    const alpha = [0.2, 0.35, 0.5, 0.7, 0.9][Math.min(intensity - 1, 4)];
    return `rgba(232, 200, 122, ${alpha})`;
  };

  const weeks = Math.ceil(cells.length / 7);

  return (
    <div className="card">
      <div className="card-title">Activity Heatmap</div>
      <div style={{ overflowX: 'auto', padding: '4px 0' }}>
        <svg width={weeks * 14 + 20} height={7 * 14 + 8} style={{ display: 'block' }}>
          {cells.map((cell, i) => {
            const col = Math.floor(i / 7);
            const row = i % 7;
            return (
              <rect
                key={cell.date}
                x={col * 14 + 2}
                y={row * 14 + 2}
                width={11}
                height={11}
                rx={2}
                fill={getColor(cell.intensity)}
              >
                <title>{`${cell.date}: ${cell.intensity} activities`}</title>
              </rect>
            );
          })}
        </svg>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginTop: 8, fontSize: 9, color: 'var(--text3)' }}>
        <span>Less</span>
        {[0, 1, 2, 3, 4].map(i => (
          <div key={i} style={{ width: 10, height: 10, borderRadius: 2, background: getColor(i) }} />
        ))}
        <span>More</span>
      </div>
    </div>
  );
}
