import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import { useLogActivity } from '../hooks/useProgress';
import { CheckCircle2, BookOpen, ChevronRight } from 'lucide-react';

export default function JavaQA() {
  const [selectedTopic, setSelectedTopic] = useState(null);
  const qc = useQueryClient();
  const logActivity = useLogActivity();

  const { data: today } = useQuery({
    queryKey: ['jqa'], queryFn: api.getJqa, staleTime: 60000,
  });
  const { data: allTopics } = useQuery({
    queryKey: ['jqaList'], queryFn: api.getJqaList, staleTime: 120000,
  });
  const { data: topicDetail } = useQuery({
    queryKey: ['jqaTopic', selectedTopic],
    queryFn: () => api.getJqaTopic(selectedTopic),
    enabled: !!selectedTopic, staleTime: 120000,
  });

  const markDone = useMutation({
    mutationFn: (id) => api.markJqaDone(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['jqa'] });
      qc.invalidateQueries({ queryKey: ['jqaList'] });
    },
  });

  const handleMarkDone = (id) => {
    markDone.mutate(id);
    logActivity.mutate({
      activity_type: 'jqa', title: `Java topic: ${id}`,
      outcome: 'completed',
    });
  };

  const topics = allTopics?.topics || [];
  const studied = allTopics?.studied_count || 0;
  const total = allTopics?.total || 0;
  const todayTopic = today?.today;
  const progress = total > 0 ? Math.round((studied / total) * 100) : 0;

  return (
    <div className="page">
      <div className="page-header">
        <h2>Java Q&A</h2>
        <div className="sub">
          {studied}/{total} topics studied ({progress}%)
        </div>
      </div>

      {/* Progress Bar */}
      <div className="card mb-24">
        <div className="flex-between mb-8">
          <div className="card-title" style={{ marginBottom: 0 }}>Overall Progress</div>
          <span style={{ fontSize: 14, fontWeight: 700, color: 'var(--gold)' }}>{progress}%</span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%`, background: 'var(--gold)' }} />
        </div>
      </div>

      {/* Today's Topic */}
      {todayTopic && (
        <div className="card mb-24" style={{ borderLeft: '3px solid var(--gold)' }}>
          <div className="card-title">Today's Topic</div>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 8 }}>{todayTopic.label || todayTopic.topic_id}</div>
          <div style={{ display: 'flex', gap: 8 }}>
            <button className="btn btn-gold" onClick={() => setSelectedTopic(todayTopic.topic_id || todayTopic.id)}>
              <BookOpen size={14} /> Study
            </button>
            <button className="btn btn-green" onClick={() => handleMarkDone(todayTopic.topic_id || todayTopic.id)}>
              <CheckCircle2 size={14} /> Mark Done
            </button>
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 16 }}>
        {/* Topic List */}
        <div className="card" style={{ maxHeight: 'calc(100vh - 300px)', overflowY: 'auto' }}>
          <div className="card-title">All Topics</div>
          {topics.map(t => {
            const id = t.topic_id || t.id;
            const label = t.label || t.name || id;
            return (
              <button key={id}
                onClick={() => setSelectedTopic(id)}
                style={{
                  display: 'flex', alignItems: 'center', gap: 8, width: '100%',
                  padding: '8px 10px', marginBottom: 3, borderRadius: 6,
                  background: selectedTopic === id ? 'var(--bg4)' : 'transparent',
                  opacity: t.studied ? 0.5 : 1,
                }}>
                {t.studied && <CheckCircle2 size={12} style={{ color: 'var(--green)' }} />}
                <span style={{ flex: 1, textAlign: 'left', fontSize: 11 }}>{label}</span>
                <ChevronRight size={12} style={{ color: 'var(--text4)' }} />
              </button>
            );
          })}
        </div>

        {/* Topic Detail */}
        <div className="card">
          {topicDetail ? (
            <>
              <div className="flex-between mb-16">
                <div className="card-title" style={{ marginBottom: 0 }}>{topicDetail.label || selectedTopic}</div>
                <button className="btn btn-green btn-sm" onClick={() => handleMarkDone(selectedTopic)}>
                  <CheckCircle2 size={12} /> Done
                </button>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {(topicDetail.questions || []).map((q, i) => (
                  <div key={i} style={{
                    padding: '10px 14px', background: 'var(--bg2)', borderRadius: 6,
                    fontSize: 12, lineHeight: 1.7,
                  }}>
                    <div style={{ fontWeight: 600, marginBottom: 4 }}>Q{i + 1}: {q.question || q.q || q}</div>
                    {(q.answer || q.a || q.hints) && (
                      <div style={{ color: 'var(--text3)', marginTop: 6, whiteSpace: 'pre-wrap' }}>
                        {q.answer || q.a || (Array.isArray(q.hints) ? q.hints.join('\n') : q.hints)}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="empty-state">Select a topic to see questions</div>
          )}
        </div>
      </div>
    </div>
  );
}
