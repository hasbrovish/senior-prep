import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import { Download, Upload, RefreshCw, Search, TrendingUp, Users, Database, Zap } from 'lucide-react';

const TARGET_COMPANIES = ['Google', 'Amazon', 'Meta', 'Flipkart', 'Razorpay', 'PhonePe', 'Stripe', 'CRED', 'Swiggy', 'Microsoft'];
const SOURCE_LABELS = {
  leetcode_discuss: 'LC Discuss',
  reddit_cscareerquestions: 'Reddit /cscq',
  reddit_developersIndia: 'Reddit /devIndia',
  reddit_expdevs: 'Reddit /expdevs',
  reddit_leetcode: 'Reddit /lc',
  reddit_leetcodedesi: 'Reddit /lcdesi',
  reddit_ExperiencedDevs: 'Reddit /expd',
  hackernews: 'HackerNews',
  blind: 'Blind',
};

export default function Intelligence() {
  const [tab, setTab] = useState('overview');
  const [companyFilter, setCompanyFilter] = useState('');
  const [importForm, setImportForm] = useState({
    company: '', title: '', body: '', source: 'blind', role: 'SDE-2', result: 'unknown',
  });
  const qc = useQueryClient();

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['intelStats'], queryFn: api.getIntelStats, staleTime: 60000,
  });
  const { data: trending, isLoading: trendLoading } = useQuery({
    queryKey: ['intelTrending'], queryFn: api.getTrending, staleTime: 60000,
  });
  const { data: experiences, isLoading: expLoading } = useQuery({
    queryKey: ['intelExperiences', companyFilter],
    queryFn: () => api.getExperiences({ company: companyFilter || undefined, limit: 30 }),
    staleTime: 30000,
  });

  const scrape = useMutation({
    mutationFn: api.triggerScrape,
    onSuccess: () => setTimeout(() => qc.invalidateQueries({ queryKey: ['intelStats'] }), 3000),
  });
  const importExp = useMutation({
    mutationFn: api.importExperience,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['intelStats'] });
      qc.invalidateQueries({ queryKey: ['intelExperiences'] });
    },
  });

  const handleImport = () => {
    if (!importForm.company.trim() || !importForm.body.trim()) return;
    importExp.mutate({
      ...importForm,
      title: importForm.title || `${importForm.company} Interview Experience`,
    });
    setImportForm({ company: '', title: '', body: '', source: 'blind', role: 'SDE-2', result: 'unknown' });
  };

  return (
    <div className="page">
      <div className="page-header">
        <div className="flex-between">
          <div>
            <h2>Intelligence</h2>
            <div className="sub">Interview experiences from Google, Amazon, Flipkart + trending topics</div>
          </div>
          <button
            className="btn btn-gold btn-sm"
            onClick={() => scrape.mutate()}
            disabled={scrape.isPending}
          >
            <RefreshCw size={12} className={scrape.isPending ? 'spin' : ''} />
            {scrape.isPending ? 'Scraping...' : 'Refresh Data'}
          </button>
        </div>
        {scrape.isSuccess && (
          <div style={{ marginTop: 6, fontSize: 11, color: 'var(--green)' }}>
            ✅ Scrape triggered — new data will appear in ~30s
          </div>
        )}
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20 }}>
        {[['overview', 'Overview'], ['trending', 'Trending'], ['experiences', 'Experiences'], ['company', 'By Company'], ['import', 'Add Manually']].map(([key, label]) => (
          <button key={key} onClick={() => setTab(key)}
            className={`btn btn-sm ${tab === key ? 'btn-solid' : 'btn-gold'}`}>
            {label}
          </button>
        ))}
      </div>

      {/* ── OVERVIEW ─────────────────────────────────────────────────────────── */}
      {tab === 'overview' && (
        <div>
          {/* Stats Row */}
          <div className="grid grid-4 mb-16">
            <div className="card" style={{ textAlign: 'center' }}>
              <div className="card-value">{statsLoading ? '…' : stats?.total_experiences ?? 0}</div>
              <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase' }}>Total Experiences</div>
            </div>
            <div className="card" style={{ textAlign: 'center' }}>
              <div className="card-value">{statsLoading ? '…' : stats?.companies ?? 0}</div>
              <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase' }}>Companies</div>
            </div>
            <div className="card" style={{ textAlign: 'center' }}>
              <div className="card-value">{trendLoading ? '…' : trending?.total_rounds ?? 0}</div>
              <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase' }}>Interview Rounds</div>
            </div>
            <div className="card" style={{ textAlign: 'center' }}>
              <div className="card-value">{trendLoading ? '…' : (trending?.top_topics?.length ?? 0)}</div>
              <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase' }}>Trending Topics</div>
            </div>
          </div>

          {/* Sources */}
          <div className="card mb-16">
            <div className="card-title">Data Sources</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {(stats?.sources || []).map((s) => (
                <div key={s.source} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: 11, color: 'var(--text2)', minWidth: 140 }}>
                    {SOURCE_LABELS[s.source] || s.source}
                  </span>
                  <div style={{ flex: 1, background: 'var(--bg4)', borderRadius: 4, height: 6, overflow: 'hidden' }}>
                    <div style={{
                      height: '100%', borderRadius: 4, background: 'var(--gold)',
                      width: `${Math.min(100, (s.cnt / (stats?.total_experiences || 1)) * 100)}%`,
                    }} />
                  </div>
                  <span style={{ fontSize: 11, color: 'var(--text3)', minWidth: 30, textAlign: 'right' }}>{s.cnt}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Round Distribution */}
          {trending?.round_types && (
            <div className="card mb-16">
              <div className="card-title">Round Type Distribution</div>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                {Object.entries(trending.round_types).map(([type, count]) => (
                  <div key={type} className="card" style={{ padding: '10px 16px', textAlign: 'center', minWidth: 100 }}>
                    <div style={{ fontSize: 18, fontWeight: 700, color: 'var(--gold)' }}>{count}</div>
                    <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'capitalize' }}>
                      {type.replace(/_/g, ' ')}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recent Experiences Preview */}
          <div className="card">
            <div className="flex-between mb-12">
              <div className="card-title" style={{ marginBottom: 0 }}>Recent Experiences</div>
              <button className="btn btn-gold btn-sm" onClick={() => setTab('experiences')}>View All</button>
            </div>
            {(stats?.recent || []).map((e, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                padding: '6px 0', borderBottom: '1px solid var(--bg4)', fontSize: 11,
              }}>
                <span style={{ fontWeight: 600 }}>{e.company || 'Unknown'}</span>
                <span style={{ color: 'var(--text3)' }}>{e.role}</span>
                <span className={`tag ${e.overall_result === 'offer' ? 'tag-green' : e.overall_result === 'reject' ? 'tag-red' : 'tag-gold'}`}>
                  {e.overall_result || 'unknown'}
                </span>
                <span style={{ color: 'var(--text4)', fontSize: 10 }}>{e.date_scraped?.slice(0, 10)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── TRENDING ──────────────────────────────────────────────────────────── */}
      {tab === 'trending' && (
        <div>
          <div className="grid grid-2 mb-16">
            {/* Top Topics */}
            <div className="card">
              <div className="card-title">Hot Topics (Last 30 Days)</div>
              {trendLoading ? (
                <div className="empty-state">Loading...</div>
              ) : (trending?.top_topics || []).slice(0, 12).map(([topic, count], i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '5px 0', borderBottom: '1px solid var(--bg4)' }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--gold)', minWidth: 24 }}>#{i + 1}</span>
                  <span style={{ flex: 1, fontSize: 12, textTransform: 'capitalize' }}>{topic}</span>
                  <span style={{ fontSize: 11, color: 'var(--text3)' }}>{count}×</span>
                </div>
              ))}
            </div>

            {/* Hot By Company */}
            <div className="card">
              <div className="card-title">Hot by Company</div>
              {Object.entries(trending?.hot_by_company || {})
                .filter(([c]) => TARGET_COMPANIES.map(t => t.toLowerCase()).includes(c.toLowerCase()) || c !== 'unknown')
                .slice(0, 6)
                .map(([company, topics]) => (
                  <div key={company} style={{ marginBottom: 10 }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--gold)', marginBottom: 4, textTransform: 'capitalize' }}>
                      {company}
                    </div>
                    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                      {Object.entries(topics).slice(0, 4).map(([topic, count]) => (
                        <span key={topic} className="tag tag-blue" style={{ fontSize: 9 }}>
                          {topic} ({count})
                        </span>
                      ))}
                    </div>
                  </div>
                ))
              }
            </div>
          </div>

          {/* Difficulty Distribution */}
          {trending?.difficulty_dist && (
            <div className="card mb-16">
              <div className="card-title">Difficulty Distribution</div>
              <div style={{ display: 'flex', gap: 12 }}>
                {Object.entries(trending.difficulty_dist).map(([d, c]) => (
                  <div key={d} style={{ textAlign: 'center', padding: '8px 16px', background: 'var(--bg2)', borderRadius: 8 }}>
                    <div style={{
                      fontSize: 16, fontWeight: 700,
                      color: d === 'hard' ? 'var(--red)' : d === 'medium' ? 'var(--orange)' : d === 'easy' ? 'var(--green)' : 'var(--text3)',
                    }}>{c}</div>
                    <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'capitalize' }}>{d}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── EXPERIENCES ───────────────────────────────────────────────────────── */}
      {tab === 'experiences' && (
        <div>
          <div className="card mb-16">
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <Search size={14} style={{ color: 'var(--text3)' }} />
              <input
                placeholder="Filter by company (e.g. Google, Amazon)"
                value={companyFilter}
                onChange={e => setCompanyFilter(e.target.value)}
                style={{ flex: 1 }}
              />
              {companyFilter && (
                <button className="btn btn-sm btn-gold" onClick={() => setCompanyFilter('')}>Clear</button>
              )}
            </div>
          </div>

          {/* Target company quick filters */}
          <div style={{ display: 'flex', gap: 6, marginBottom: 16, flexWrap: 'wrap' }}>
            {TARGET_COMPANIES.map(c => (
              <button key={c} onClick={() => setCompanyFilter(companyFilter === c ? '' : c)}
                style={{
                  padding: '4px 10px', borderRadius: 4, fontSize: 10, cursor: 'pointer',
                  background: companyFilter === c ? 'var(--gold)' : 'var(--bg3)',
                  color: companyFilter === c ? '#000' : 'var(--text2)',
                  border: '1px solid var(--bg4)',
                }}>
                {c}
              </button>
            ))}
          </div>

          {expLoading ? (
            <div className="card"><div className="empty-state">Loading experiences...</div></div>
          ) : (experiences?.experiences || []).length === 0 ? (
            <div className="card">
              <div className="empty-state">
                {companyFilter ? `No experiences for "${companyFilter}". Try a different company.` : 'No experiences. Run a scrape or import manually.'}
              </div>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {(experiences?.experiences || []).map((exp, i) => (
                <div key={i} className="card" style={{ padding: '12px 16px' }}>
                  <div className="flex-between mb-6">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{ fontWeight: 700, fontSize: 13 }}>{exp.company}</span>
                      {exp.role && <span className="tag tag-blue">{exp.role}</span>}
                      <span className="tag" style={{ fontSize: 9, color: 'var(--text4)' }}>{SOURCE_LABELS[exp.source] || exp.source}</span>
                    </div>
                    <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                      {exp.overall_result && exp.overall_result !== 'unknown' && (
                        <span className={`tag ${exp.overall_result === 'offer' ? 'tag-green' : 'tag-red'}`}>
                          {exp.overall_result}
                        </span>
                      )}
                      <span style={{ fontSize: 9, color: 'var(--text4)' }}>{exp.date_scraped?.slice(0, 10)}</span>
                    </div>
                  </div>
                  {exp.title && (
                    <div style={{ fontSize: 11, color: 'var(--text2)', marginBottom: 4 }}>{exp.title}</div>
                  )}
                  {exp.body_summary && exp.body_summary !== 'None' && (
                    <div style={{ fontSize: 11, color: 'var(--text3)', lineHeight: 1.5 }}>
                      {exp.body_summary}
                    </div>
                  )}
                  {exp.tips && (
                    <div style={{ marginTop: 6, fontSize: 11, color: 'var(--green)' }}>
                      💡 {exp.tips}
                    </div>
                  )}
                  {exp.tc_offered && (
                    <div style={{ marginTop: 4, fontSize: 10, color: 'var(--gold)' }}>
                      💰 TC: {exp.tc_offered}
                    </div>
                  )}
                  {exp.url && (
                    <a href={exp.url} target="_blank" rel="noopener noreferrer"
                      style={{ fontSize: 10, color: 'var(--cyan)', marginTop: 4, display: 'inline-block' }}>
                      View original →
                    </a>
                  )}
                </div>
              ))}
            </div>
          )}
          <div style={{ fontSize: 10, color: 'var(--text4)', marginTop: 8, textAlign: 'center' }}>
            Showing {experiences?.count || 0} experiences. Use enrichment (API key required) to extract questions from raw posts.
          </div>
        </div>
      )}

      {/* ── BY COMPANY ────────────────────────────────────────────────────────── */}
      {tab === 'company' && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 10 }}>
            {TARGET_COMPANIES.map(company => {
              const compData = trending?.hot_by_company?.[company.toLowerCase()] || {};
              return (
                <div key={company} className="card"
                  style={{ cursor: 'pointer', border: '1px solid var(--bg4)' }}
                  onClick={() => { setTab('experiences'); setCompanyFilter(company); }}
                >
                  <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 8 }}>{company}</div>
                  {Object.keys(compData).length > 0 ? (
                    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                      {Object.entries(compData).slice(0, 3).map(([topic, count]) => (
                        <span key={topic} className="tag tag-blue" style={{ fontSize: 9 }}>
                          {topic} ({count})
                        </span>
                      ))}
                    </div>
                  ) : (
                    <div style={{ fontSize: 10, color: 'var(--text4)' }}>No data yet — import manually</div>
                  )}
                </div>
              );
            })}
          </div>
          <div style={{ marginTop: 12, fontSize: 10, color: 'var(--text4)', textAlign: 'center' }}>
            Click a company to see its experiences. Data from LeetCode Discuss, Reddit, Blind.
          </div>
        </div>
      )}

      {/* ── IMPORT ────────────────────────────────────────────────────────────── */}
      {tab === 'import' && (
        <div className="card">
          <div className="card-title">Add Interview Experience Manually</div>
          <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 12, lineHeight: 1.6 }}>
            Copy from <strong>Blind</strong>, <strong>Enginebogie</strong>, <strong>Reddit</strong> — paste interview experience text here to add to your intelligence database.
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, marginBottom: 8 }}>
            <input placeholder="Company *" value={importForm.company}
              onChange={e => setImportForm(f => ({ ...f, company: e.target.value }))} />
            <input placeholder="Role (e.g. SDE-2)" value={importForm.role}
              onChange={e => setImportForm(f => ({ ...f, role: e.target.value }))} />
            <select value={importForm.source} onChange={e => setImportForm(f => ({ ...f, source: e.target.value }))}>
              <option value="blind">Blind</option>
              <option value="leetcode_discuss">LeetCode Discuss</option>
              <option value="reddit">Reddit</option>
              <option value="enginebogie">Enginebogie</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 8, marginBottom: 8 }}>
            <input placeholder="Post title (optional)" value={importForm.title}
              onChange={e => setImportForm(f => ({ ...f, title: e.target.value }))} />
            <select value={importForm.result} onChange={e => setImportForm(f => ({ ...f, result: e.target.value }))}>
              <option value="unknown">Result: Unknown</option>
              <option value="offer">Got Offer</option>
              <option value="reject">Rejected</option>
            </select>
          </div>
          <textarea rows={10} placeholder="Paste the full interview experience text here... *"
            value={importForm.body} onChange={e => setImportForm(f => ({ ...f, body: e.target.value }))}
            style={{ marginBottom: 12 }} />
          <button className="btn btn-solid" onClick={handleImport}
            disabled={importExp.isPending || !importForm.company.trim() || !importForm.body.trim()}>
            <Upload size={14} /> Save to Intelligence DB
          </button>
          {importExp.isSuccess && (
            <div style={{ marginTop: 8, fontSize: 11, color: 'var(--green)' }}>
              ✅ Saved! It will be enriched with AI once ANTHROPIC_API_KEY is configured.
            </div>
          )}
          {importExp.isError && (
            <div style={{ marginTop: 8, fontSize: 11, color: 'var(--red)' }}>
              ❌ Failed: {importExp.error?.message}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
