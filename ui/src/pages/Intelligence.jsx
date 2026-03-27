import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '../api';
import { Search, TrendingUp, Building2, Download, FileText, Upload } from 'lucide-react';

export default function Intelligence() {
  const [tab, setTab] = useState('overview');
  const [companySearch, setCompanySearch] = useState('');
  const [importForm, setImportForm] = useState({ company: '', title: '', body: '', source: 'blind', role: 'SDE-2', result: 'unknown' });

  const { data: stats } = useQuery({
    queryKey: ['intelStats'], queryFn: api.getIntelStats, staleTime: 120000,
  });
  const { data: trending } = useQuery({
    queryKey: ['intelTrending'], queryFn: api.getTrending, staleTime: 120000,
  });
  const { data: experiences } = useQuery({
    queryKey: ['intelExperiences'],
    queryFn: () => api.getExperiences({ limit: 20 }),
    staleTime: 60000,
  });
  const { data: companyData } = useQuery({
    queryKey: ['companyIntel', companySearch],
    queryFn: () => api.getCompanyIntel(companySearch),
    enabled: !!companySearch && tab === 'company', staleTime: 120000,
  });

  const scrape = useMutation({ mutationFn: api.triggerScrape });
  const importExp = useMutation({ mutationFn: api.importExperience });

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
        <h2>Intelligence</h2>
        <div className="sub">Interview experiences, trending topics, and company intelligence</div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 24 }}>
        {[['overview', 'Overview'], ['trending', 'Trending'], ['experiences', 'Experiences'], ['company', 'Company Intel'], ['import', 'Import']].map(([key, label]) => (
          <button key={key} onClick={() => setTab(key)} className={`btn ${tab === key ? 'btn-solid' : 'btn-gold'}`}>
            {label}
          </button>
        ))}
      </div>

      {tab === 'overview' && (
        <div>
          {/* Stats Grid */}
          <div className="grid grid-4 mb-24">
            {Object.entries(stats || {}).filter(([k]) => typeof (stats || {})[k] === 'number').slice(0, 4).map(([key, val]) => (
              <div key={key} className="card" style={{ textAlign: 'center' }}>
                <div className="card-value">{val}</div>
                <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}</div>
              </div>
            ))}
          </div>
          <div className="card">
            <div className="flex-between mb-8">
              <div className="card-title" style={{ marginBottom: 0 }}>Scrape Status</div>
              <button className="btn btn-gold btn-sm" onClick={() => scrape.mutate()} disabled={scrape.isPending}>
                <Download size={12} /> {scrape.isPending ? 'Scraping...' : 'Run Scrape'}
              </button>
            </div>
            {scrape.isSuccess && <div style={{ fontSize: 11, color: 'var(--green)' }}>Scrape triggered successfully</div>}
          </div>
        </div>
      )}

      {tab === 'trending' && (
        <div className="card">
          <div className="card-title">Trending Topics (Last 30 Days)</div>
          {trending?.top_topics ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {trending.top_topics.map((topic, i) => (
                <div key={i} style={{
                  display: 'flex', alignItems: 'center', gap: 12,
                  padding: '8px 12px', background: 'var(--bg2)', borderRadius: 6,
                }}>
                  <span style={{ fontSize: 14, fontWeight: 700, color: 'var(--gold)', minWidth: 24 }}>#{i + 1}</span>
                  <span style={{ flex: 1, fontSize: 12 }}>{typeof topic === 'string' ? topic : topic[0]}</span>
                  {typeof topic !== 'string' && <span style={{ fontSize: 11, color: 'var(--text3)' }}>{topic[1]} mentions</span>}
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">No trending data available. Run a scrape first.</div>
          )}
          {trending?.sample_questions && Object.keys(trending.sample_questions).length > 0 && (
            <div style={{ marginTop: 16 }}>
              <div className="card-title">Sample Questions by Round</div>
              {Object.entries(trending.sample_questions).map(([round, questions]) => (
                <div key={round} style={{ marginBottom: 12 }}>
                  <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--gold)', marginBottom: 4 }}>{round}</div>
                  {questions.map((q, i) => (
                    <div key={i} style={{ fontSize: 11, padding: '4px 0', borderBottom: '1px solid var(--bg4)', color: 'var(--text)' }}>
                      {q}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {tab === 'experiences' && (
        <div className="card">
          <div className="card-title">Recent Experiences</div>
          {(experiences?.experiences || []).map((exp, i) => (
            <div key={i} style={{
              padding: '12px 14px', marginBottom: 8, background: 'var(--bg2)', borderRadius: 8,
              borderLeft: '3px solid var(--blue)',
            }}>
              <div className="flex-between mb-8">
                <div>
                  <span style={{ fontWeight: 600, fontSize: 13 }}>{exp.company}</span>
                  {exp.role && <span style={{ fontSize: 11, color: 'var(--text3)', marginLeft: 8 }}>{exp.role}</span>}
                </div>
                {exp.result && <span className={`tag ${exp.result === 'offer' ? 'tag-green' : exp.result === 'reject' ? 'tag-red' : 'tag-gold'}`}>
                  {exp.result}
                </span>}
              </div>
              {exp.rounds && exp.rounds.length > 0 && (
                <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                  {exp.rounds.map((r, ri) => (
                    <span key={ri} className="tag tag-purple">{r.type || r.round_type}</span>
                  ))}
                </div>
              )}
            </div>
          ))}
          {(!experiences?.experiences || experiences.experiences.length === 0) && (
            <div className="empty-state">No experiences in the database. Run a scrape or import manually.</div>
          )}
        </div>
      )}

      {tab === 'company' && (
        <div>
          <div className="card mb-16">
            <div className="card-title">Company Search</div>
            <div style={{ display: 'flex', gap: 8 }}>
              <input placeholder="Company name (e.g. google, amazon)" value={companySearch}
                     onChange={e => setCompanySearch(e.target.value)} style={{ flex: 1 }} />
            </div>
          </div>
          {companyData && (
            <div className="card">
              <div className="card-title">{companyData.company}</div>
              <div className="grid grid-3 mb-16">
                <div><span style={{ fontSize: 10, color: 'var(--text3)' }}>Experiences</span><div style={{ fontSize: 18, fontWeight: 700 }}>{companyData.experiences_in_db}</div></div>
                {companyData.static_info?.level && <div><span style={{ fontSize: 10, color: 'var(--text3)' }}>Target Level</span><div style={{ fontSize: 14, fontWeight: 600 }}>{companyData.static_info.level}</div></div>}
                {companyData.static_info?.tc_range && <div><span style={{ fontSize: 10, color: 'var(--text3)' }}>TC Range</span><div style={{ fontSize: 14, fontWeight: 600 }}>{companyData.static_info.tc_range}</div></div>}
              </div>
              {companyData.round_distribution && Object.keys(companyData.round_distribution).length > 0 && (
                <div style={{ marginBottom: 16 }}>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 6 }}>Round Distribution</div>
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                    {Object.entries(companyData.round_distribution).map(([round, count]) => (
                      <span key={round} className="tag tag-blue">{round}: {count}</span>
                    ))}
                  </div>
                </div>
              )}
              {companyData.recent_questions && companyData.recent_questions.length > 0 && (
                <div>
                  <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 6 }}>Recent Questions</div>
                  {companyData.recent_questions.map((q, i) => (
                    <div key={i} style={{ fontSize: 11, padding: '4px 0', borderBottom: '1px solid var(--bg4)' }}>
                      <span className="tag tag-purple" style={{ marginRight: 6 }}>{q.type}</span>{q.question}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {tab === 'import' && (
        <div className="card">
          <div className="card-title">Manual Import</div>
          <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 12 }}>
            Paste interview experience text from LeetCode Discuss, Blind, Reddit, etc.
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
            <input placeholder="Title (optional)" value={importForm.title}
                   onChange={e => setImportForm(f => ({ ...f, title: e.target.value }))} />
            <select value={importForm.result} onChange={e => setImportForm(f => ({ ...f, result: e.target.value }))}>
              <option value="unknown">Result: Unknown</option>
              <option value="offer">Offer</option>
              <option value="reject">Rejected</option>
            </select>
          </div>
          <textarea rows={10} placeholder="Paste the full interview experience text here... *"
                    value={importForm.body} onChange={e => setImportForm(f => ({ ...f, body: e.target.value }))}
                    style={{ marginBottom: 12 }} />
          <button className="btn btn-solid" onClick={handleImport}
                  disabled={importExp.isPending || !importForm.company.trim() || !importForm.body.trim()}>
            <Upload size={14} /> Import
          </button>
          {importExp.isSuccess && <div style={{ marginTop: 8, fontSize: 11, color: 'var(--green)' }}>Imported successfully</div>}
          {importExp.isError && <div style={{ marginTop: 8, fontSize: 11, color: 'var(--red)' }}>Import failed: {importExp.error?.message}</div>}
        </div>
      )}
    </div>
  );
}
