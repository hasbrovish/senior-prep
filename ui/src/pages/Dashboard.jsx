import { useProgress, useGaps, useDailyPlan, usePlanStats, useTodayLog, useDrillStats, useMockTrend } from '../hooks/useProgress';
import ReadinessGauge from '../components/ReadinessGauge';
import LCProgressChart from '../components/LCProgressChart';
import GapRadar from '../components/GapRadar';
import StreakHeatmap from '../components/StreakHeatmap';
import MockTrendChart from '../components/MockTrendChart';
import WeeklyComparison from '../components/WeeklyComparison';
import TodayPlan from '../components/TodayPlan';
import QuickActions from '../components/QuickActions';
import ActivityFeed from '../components/ActivityFeed';
import DrillStatsCard from '../components/DrillStatsCard';

export default function Dashboard() {
  const { data: progress, isLoading: pLoading } = useProgress();
  const { data: gaps } = useGaps();
  const { data: dailyPlan } = useDailyPlan();
  const { data: planStats } = usePlanStats();
  const { data: todayLog } = useTodayLog();
  const { data: drillStats } = useDrillStats();
  const { data: mockTrend } = useMockTrend();

  if (pLoading) return <div className="page"><div className="loading">Loading dashboard...</div></div>;

  const lcSync = progress?.lc_sync || {};
  const readiness = gaps?.readiness || 0;
  const gapList = gaps?.gaps || [];

  return (
    <div className="page">
      <div className="page-header">
        <h2>Dashboard</h2>
        <div className="sub">Your interview preparation at a glance</div>
      </div>

      {/* Row 1: Readiness + LC + Gaps */}
      <div className="grid grid-3 mb-24">
        <ReadinessGauge value={readiness} />
        <LCProgressChart lcSync={lcSync} />
        <GapRadar gaps={gapList} />
      </div>

      {/* Row 2: Quick Actions + Today Plan */}
      <div className="grid grid-2 mb-24">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <QuickActions onSync={() => window.location.reload()} />
          <DrillStatsCard stats={drillStats} />
        </div>
        <TodayPlan dailyPlan={dailyPlan} />
      </div>

      {/* Row 3: Heatmap + Activity Feed */}
      <div className="grid grid-2 mb-24">
        <StreakHeatmap dailyLogs={progress?.daily_logs || {}} lcDone={progress?.lc_done || []} />
        <ActivityFeed todayLog={todayLog} />
      </div>

      {/* Row 4: Weekly Comparison + Mock Trend */}
      <div className="grid grid-2 mb-24">
        <WeeklyComparison planStats={planStats} />
        <MockTrendChart trendData={mockTrend} />
      </div>

      {/* Row 5: Gap Details */}
      {gapList.length > 0 && (
        <div className="card">
          <div className="card-title">Gap Details</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {gapList.map((g, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '10px 14px', background: 'var(--bg2)', borderRadius: 6,
                borderLeft: `3px solid ${g.severity === 'CRITICAL' ? 'var(--red)' : g.severity === 'HIGH' ? 'var(--orange)' : 'var(--text4)'}`,
              }}>
                <span className={`tag tag-${g.severity === 'CRITICAL' ? 'red' : g.severity === 'HIGH' ? 'orange' : 'gold'}`}>
                  {g.severity}
                </span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 12, fontWeight: 600 }}>{g.area}</div>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginTop: 2 }}>{g.action}</div>
                </div>
                <div style={{ fontSize: 10, color: 'var(--text3)' }}>
                  {g.current} / {g.target}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
