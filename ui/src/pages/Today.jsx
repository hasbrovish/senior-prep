import { useState } from 'react';
import { useProgress, useGaps, useDailyPlan, useTodayLog, useLogActivity } from '../hooks/useProgress';
import { Swords, Timer, Code2, Brain, Target, GraduationCap, BookOpen } from 'lucide-react';
import PomodoroTimer from '../components/PomodoroTimer';
import ActivityFeed from '../components/ActivityFeed';
import TodayPlan from '../components/TodayPlan';

const SESSION_TYPES = [
  { key: 'lc', label: 'LeetCode', icon: Target, color: 'var(--green)', mins: 45 },
  { key: 'drill', label: 'Drill Session', icon: Swords, color: 'var(--cyan)', mins: 30 },
  { key: 'mock', label: 'Mock Interview', icon: Timer, color: 'var(--orange)', mins: 60 },
  { key: 'lld', label: 'LLD Practice', icon: Code2, color: 'var(--purple)', mins: 45 },
  { key: 'behavioral', label: 'Behavioral Prep', icon: Brain, color: 'var(--pink)', mins: 30 },
  { key: 'jqa', label: 'Java Theory', icon: GraduationCap, color: 'var(--blue)', mins: 25 },
  { key: 'system_design', label: 'System Design', icon: BookOpen, color: 'var(--gold)', mins: 45 },
  { key: 'curriculum', label: 'Curriculum', icon: BookOpen, color: 'var(--text2)', mins: 30 },
];

export default function Today() {
  const [activeSession, setActiveSession] = useState(null);
  const [sessionTitle, setSessionTitle] = useState('');
  const { data: progress } = useProgress();
  const { data: gaps } = useGaps();
  const { data: dailyPlan } = useDailyPlan();
  const { data: todayLog } = useTodayLog();
  const logActivity = useLogActivity();

  const lcSync = progress?.lc_sync || {};
  const readiness = gaps?.readiness || 0;

  const handleStartSession = (type) => {
    setActiveSession(type);
    setSessionTitle('');
  };

  const handleCompleteSession = (elapsedMins) => {
    if (!activeSession) return;
    logActivity.mutate({
      activity_type: activeSession.key,
      title: sessionTitle || `${activeSession.label} session`,
      duration_mins: elapsedMins,
      outcome: 'completed',
    });
    setActiveSession(null);
    setSessionTitle('');
  };

  const topGap = (gaps?.gaps || []).find(g => g.severity === 'CRITICAL' || g.severity === 'HIGH');

  return (
    <div className="page">
      <div className="page-header">
        <h2>Today</h2>
        <div className="sub">
          Day {Math.ceil((Date.now() - new Date('2026-03-19').getTime()) / 86400000)} of prep
          &middot; {readiness}% ready
          &middot; {lcSync.streak || 0} day streak
          {lcSync.today_submissions > 0 && ` · ${lcSync.today_submissions} LC today`}
        </div>
      </div>

      {/* Smart Suggestion */}
      {topGap && !activeSession && (
        <div className="card mb-16" style={{ borderLeft: '3px solid var(--orange)' }}>
          <div style={{ fontSize: 10, color: 'var(--orange)', fontWeight: 600, marginBottom: 4, letterSpacing: 1 }}>
            SUGGESTED FOCUS
          </div>
          <div style={{ fontSize: 13 }}>{topGap.area}: {topGap.action}</div>
        </div>
      )}

      {/* Active Session */}
      {activeSession ? (
        <div className="mb-24">
          <div className="grid grid-2">
            <div>
              <PomodoroTimer
                minutes={activeSession.mins}
                onComplete={handleCompleteSession}
                label={activeSession.label}
              />
            </div>
            <div className="card">
              <div className="card-title">Session Notes</div>
              <input
                placeholder="What are you working on?"
                value={sessionTitle}
                onChange={e => setSessionTitle(e.target.value)}
                style={{ marginBottom: 12 }}
              />
              <div style={{ fontSize: 11, color: 'var(--text3)', lineHeight: 1.6 }}>
                Timer is running. Focus on your {activeSession.label.toLowerCase()} session.
                Click "Done" when finished to auto-log your activity.
              </div>
              <button
                className="btn btn-red mt-16"
                onClick={() => setActiveSession(null)}
              >
                Cancel Session
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* Session Launcher */
        <div className="card mb-24">
          <div className="card-title">Start a Session</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 8 }}>
            {SESSION_TYPES.map((s) => (
              <button
                key={s.key}
                onClick={() => handleStartSession(s)}
                style={{
                  display: 'flex', alignItems: 'center', gap: 8,
                  padding: '12px', background: 'var(--bg2)', borderRadius: 8,
                  border: '1px solid var(--bg4)', cursor: 'pointer', transition: 'all 0.15s',
                }}
                onMouseOver={e => e.currentTarget.style.borderColor = s.color}
                onMouseOut={e => e.currentTarget.style.borderColor = 'var(--bg4)'}
              >
                <s.icon size={16} style={{ color: s.color }} />
                <div style={{ textAlign: 'left' }}>
                  <div style={{ fontSize: 11, color: 'var(--text)' }}>{s.label}</div>
                  <div style={{ fontSize: 9, color: 'var(--text3)' }}>{s.mins} min</div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Plan + Feed */}
      <div className="grid grid-2">
        <TodayPlan dailyPlan={dailyPlan} />
        <ActivityFeed todayLog={todayLog} />
      </div>
    </div>
  );
}
