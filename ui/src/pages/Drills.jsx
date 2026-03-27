import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import { ExternalLink, CheckCircle2, Flame, Target, Coffee } from 'lucide-react';
import { useLogActivity } from '../hooks/useProgress';

const DIFF_COLORS = { Easy: 'var(--green)', Medium: 'var(--orange)', Hard: 'var(--red)' };

export default function Drills() {
  const [selectedCompany, setSelectedCompany] = useState(null);
  const qc = useQueryClient();

  const { data: todayDrill, isLoading } = useQuery({
    queryKey: ['drillToday'], queryFn: api.getDrillToday, staleTime: 60000,
  });
  const { data: stats } = useQuery({
    queryKey: ['drillStats'], queryFn: api.getDrillStats, staleTime: 60000,
  });
  const { data: companies } = useQuery({
    queryKey: ['drillCompanies'], queryFn: api.getDrillCompanies, staleTime: 300000,
  });
  const { data: companyDrill } = useQuery({
    queryKey: ['drillCompany', selectedCompany],
    queryFn: () => api.getDrillCompany(selectedCompany),
    enabled: !!selectedCompany, staleTime: 120000,
  });

  const logActivity = useLogActivity();
  const markDone = useMutation({
    mutationFn: api.markDrillDone,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['drillToday'] });
      qc.invalidateQueries({ queryKey: ['drillStats'] });
    },
  });

  const handleDone = (problem) => {
    markDone.mutate({
      problem_name: problem.name,
      time_mins: 0,
      struggled: false,
      language: 'java',
    });
    logActivity.mutate({
      activity_type: 'drill',
      title: problem.name,
      difficulty: problem.difficulty,
      outcome: 'completed',
    });
  };

  const drillStats = stats?.stats || {};
  const problems = todayDrill?.problems || [];
  // API returns companies as either string[] or { company: count } map
  const rawCompanies = companies?.companies;
  const companyList = Array.isArray(rawCompanies)
    ? rawCompanies
    : rawCompanies && typeof rawCompanies === 'object'
      ? Object.keys(rawCompanies).sort((a, b) => a.localeCompare(b))
      : [];

  return (
    <div className="page">
      <div className="page-header">
        <h2>Drills</h2>
        <div className="sub">Daily curated problems based on your gaps and war plan</div>
      </div>

      {/* Stats */}
      <div className="grid grid-3 mb-24">
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Target size={20} style={{ color: 'var(--green)' }} />
          <div>
            <div className="card-value" style={{ fontSize: 24 }}>{drillStats.total || 0}</div>
            <div style={{ fontSize: 9, color: 'var(--text3)' }}>Total Drills</div>
          </div>
        </div>
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Coffee size={20} style={{ color: 'var(--purple)' }} />
          <div>
            <div className="card-value" style={{ fontSize: 24, color: 'var(--purple)' }}>{drillStats.java || 0}</div>
            <div style={{ fontSize: 9, color: 'var(--text3)' }}>Java Problems</div>
          </div>
        </div>
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Flame size={20} style={{ color: 'var(--orange)' }} />
          <div>
            <div className="card-value" style={{ fontSize: 24, color: 'var(--orange)' }}>{drillStats.streak || 0}</div>
            <div style={{ fontSize: 9, color: 'var(--text3)' }}>Day Streak</div>
          </div>
        </div>
      </div>

      {/* Today's Drill */}
      <div className="card mb-24">
        <div className="card-title">Today's Drill</div>
        {isLoading ? (
          <div className="loading">Loading problems...</div>
        ) : problems.length === 0 ? (
          <div className="empty-state">No drill problems available</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {problems.map((p) => (
              <div key={p.lc_id} style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '12px 14px', background: 'var(--bg2)', borderRadius: 8,
                borderLeft: `3px solid ${DIFF_COLORS[p.difficulty] || 'var(--text3)'}`,
              }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>
                    #{p.lc_id} {p.name}
                  </div>
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                    <span className="tag tag-gold">{p.difficulty}</span>
                    <span className="tag tag-purple">{p.pattern}</span>
                    {(p.companies || []).slice(0, 3).map(c => (
                      <span key={c} className="tag tag-blue">{c}</span>
                    ))}
                  </div>
                  {p.java_tip && (
                    <div style={{ fontSize: 10, color: 'var(--purple)', marginTop: 6 }}>{p.java_tip}</div>
                  )}
                </div>
                <div style={{ display: 'flex', gap: 6 }}>
                  <a href={p.url || `https://leetcode.com/problems/${(p.name || '').toLowerCase().replace(/\s+/g, '-')}`}
                     target="_blank" rel="noopener noreferrer"
                     className="btn btn-gold btn-sm">
                    <ExternalLink size={12} /> Solve
                  </a>
                  <button className="btn btn-green btn-sm" onClick={() => handleDone(p)}>
                    <CheckCircle2 size={12} /> Done
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Company Problem Bank */}
      <div className="card">
        <div className="card-title">Company Problem Bank</div>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
          {companyList.map((c) => (
            <button key={c} className={`btn btn-sm ${selectedCompany === c ? 'btn-solid' : 'btn-gold'}`}
                    onClick={() => setSelectedCompany(selectedCompany === c ? null : c)}>
              {c}
            </button>
          ))}
        </div>
        {selectedCompany && companyDrill && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 4 }}>
              {companyDrill.count} problems for {companyDrill.company}
            </div>
            {(companyDrill.problems || []).slice(0, 20).map(p => (
              <div key={p.lc_id} style={{
                display: 'flex', alignItems: 'center', gap: 10,
                padding: '8px 10px', background: 'var(--bg2)', borderRadius: 6,
              }}>
                <span style={{ color: DIFF_COLORS[p.difficulty], fontSize: 11, minWidth: 50 }}>{p.difficulty}</span>
                <span style={{ flex: 1, fontSize: 12 }}>{p.name}</span>
                <span className="tag tag-purple">{p.pattern}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
