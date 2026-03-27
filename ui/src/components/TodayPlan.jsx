import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';
import { api } from '../api';

export default function TodayPlan({ dailyPlan = {} }) {
  const [expanded, setExpanded] = useState(false);
  const qc = useQueryClient();
  const refresh = useMutation({
    mutationFn: api.refreshDailyPlan,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['dailyPlan'] }),
  });

  const plan = dailyPlan.plan || '';
  const cached = dailyPlan.cached;
  const lines = plan.split('\n').filter(Boolean);
  const preview = lines.slice(0, 6).join('\n');
  const hasMore = lines.length > 6;

  return (
    <div className="card">
      <div className="flex-between mb-8">
        <div className="card-title" style={{ marginBottom: 0 }}>AI Daily Plan</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {cached && <span style={{ fontSize: 9, color: 'var(--text4)' }}>cached</span>}
          <button
            className="btn btn-gold btn-sm"
            onClick={() => refresh.mutate()}
            disabled={refresh.isPending}
          >
            <RefreshCw size={12} className={refresh.isPending ? 'loading' : ''} />
            Refresh
          </button>
        </div>
      </div>
      {plan ? (
        <div style={{ fontSize: 12, lineHeight: 1.7, color: 'var(--text)', whiteSpace: 'pre-wrap' }}>
          {expanded ? plan : preview}
          {hasMore && (
            <button
              onClick={() => setExpanded(!expanded)}
              style={{ display: 'flex', alignItems: 'center', gap: 4, marginTop: 8, fontSize: 10, color: 'var(--gold)' }}
            >
              {expanded ? <><ChevronUp size={14} /> Show less</> : <><ChevronDown size={14} /> Show more</>}
            </button>
          )}
        </div>
      ) : (
        <div className="empty-state">No plan generated yet. Click refresh to create one.</div>
      )}
    </div>
  );
}
