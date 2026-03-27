import { Play, Pause, RotateCcw } from 'lucide-react';
import { useTimer } from '../hooks/useTimer';

export default function PomodoroTimer({ minutes = 25, onComplete, label = 'Focus Session' }) {
  const timer = useTimer(minutes);

  const handleComplete = () => {
    timer.pause();
    if (onComplete) onComplete(timer.elapsedMins);
  };

  const circumference = 2 * Math.PI * 52;
  const offset = circumference * (1 - timer.progress);

  return (
    <div className="card" style={{ textAlign: 'center' }}>
      <div className="card-title">{label}</div>
      <div style={{ position: 'relative', width: 130, height: 130, margin: '0 auto 12px' }}>
        <svg width={130} height={130} style={{ transform: 'rotate(-90deg)' }}>
          <circle cx={65} cy={65} r={52} fill="none" stroke="var(--bg4)" strokeWidth={6} />
          <circle
            cx={65} cy={65} r={52} fill="none"
            stroke={timer.remaining === 0 ? 'var(--green)' : 'var(--gold)'}
            strokeWidth={6} strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{ transition: 'stroke-dashoffset 1s linear' }}
          />
        </svg>
        <div style={{
          position: 'absolute', top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
        }}>
          <div style={{ fontSize: 24, fontWeight: 700, fontFamily: 'var(--serif)', color: 'var(--gold)' }}>
            {timer.display}
          </div>
        </div>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 8 }}>
        {!timer.running ? (
          <button className="btn btn-solid" onClick={timer.start} disabled={timer.remaining === 0}>
            <Play size={14} /> Start
          </button>
        ) : (
          <button className="btn btn-gold" onClick={timer.pause}>
            <Pause size={14} /> Pause
          </button>
        )}
        <button className="btn btn-gold" onClick={() => timer.reset(minutes)}>
          <RotateCcw size={14} />
        </button>
        {timer.elapsed > 60 && (
          <button className="btn btn-green" onClick={handleComplete}>
            Done ({timer.elapsedMins}m)
          </button>
        )}
      </div>
    </div>
  );
}
