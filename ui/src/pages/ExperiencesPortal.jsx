import { useState, useMemo, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import {
  Layers, Search, Building2, BookOpen, Star, PlusCircle,
  ChevronDown, ChevronRight, Trash2, TrendingUp, Zap,
  MessageSquare, RefreshCw, Target, Filter
} from 'lucide-react';

// ─── Constants ───────────────────────────────────────────────────────────────

const TARGET_COMPANIES = [
  // FAANG / Big Tech
  'Google', 'Amazon', 'Meta', 'Microsoft', 'Apple',
  // Top Indian product (levels.fyi high paying)
  'Flipkart', 'Razorpay', 'PhonePe', 'CRED', 'Swiggy',
  'Zomato', 'Meesho', 'Dream11', 'Groww', 'Zerodha', 'Juspay',
  // Global high-paying
  'Stripe', 'Atlassian', 'Adobe', 'Uber', 'Goldman Sachs',
  'Databricks', 'Confluent', 'LinkedIn', 'Walmart',
];

const ROUND_TYPES = ['dsa', 'system_design', 'lld', 'behavioral', 'hr', 'machine_coding'];

const ROUND_TYPE_LABELS = {
  dsa: 'DSA', system_design: 'System Design', lld: 'LLD',
  behavioral: 'Behavioral', hr: 'HR', machine_coding: 'Machine Coding',
};

const ROUND_TYPE_COLORS = {
  dsa: 'tag-blue',
  system_design: 'tag-purple',
  lld: 'tag-orange',
  behavioral: 'tag-gold',
  hr: 'tag-green',
  machine_coding: 'tag-red',
};

const DIFFICULTY_COLORS = {
  easy: 'tag-green', medium: 'tag-orange', hard: 'tag-red',
};

const SOURCE_LABELS = {
  leetcode_discuss: 'LC Discuss',
  reddit_cscareerquestions: 'Reddit',
  reddit_developersIndia: 'Reddit/devIndia',
  reddit_expdevs: 'Reddit/expdevs',
  reddit_leetcode: 'Reddit/LC',
  reddit_leetcodedesi: 'Reddit/lcdesi',
  reddit_ExperiencedDevs: 'Reddit/expd',
  reddit_IndiaTechies: 'Reddit/IndiaTechies',
  hackernews: 'HackerNews',
  blind: 'Blind',
  enginebogie: 'Enginebogie',
};

// ─── Shared helpers ───────────────────────────────────────────────────────────

function RoundTypeTag({ type }) {
  const cls = ROUND_TYPE_COLORS[type] || 'tag-gold';
  const label = ROUND_TYPE_LABELS[type] || type?.replace(/_/g, ' ') || '—';
  return <span className={`tag ${cls}`}>{label}</span>;
}

function DifficultyTag({ diff }) {
  if (!diff) return null;
  const cls = DIFFICULTY_COLORS[diff] || 'tag-gold';
  return <span className={`tag ${cls}`}>{diff}</span>;
}

function ResultTag({ result }) {
  if (!result || result === 'unknown') return null;
  const cls = result === 'offer' ? 'tag-green' : result === 'reject' ? 'tag-red' : 'tag-gold';
  return <span className={`tag ${cls}`}>{result}</span>;
}

// ─── Add to Practice Button ───────────────────────────────────────────────────

function AddToPracticeBtn({ roundId }) {
  const [added, setAdded] = useState(false);
  const mutation = useMutation({
    mutationFn: () => api.addToPractice(roundId),
    onSuccess: () => {
      setAdded(true);
      setTimeout(() => setAdded(false), 2500);
    },
  });

  if (!roundId) return null;

  return (
    <button
      className={`btn btn-sm ${added ? 'btn-green' : 'btn-gold'}`}
      onClick={(e) => { e.stopPropagation(); mutation.mutate(); }}
      disabled={mutation.isPending || added}
      style={{ whiteSpace: 'nowrap' }}
    >
      {added ? '✓ Added!' : mutation.isPending ? '...' : '+ Practice'}
    </button>
  );
}

// ─── Question Card ─────────────────────────────────────────────────────────────

function QuestionCard({ q, showCompany = true }) {
  return (
    <div className="card" style={{ padding: '12px 16px', borderLeft: `3px solid var(--bg5)` }}>
      <div style={{ marginBottom: 8 }}>
        <p style={{ fontSize: 12, fontWeight: 600, color: 'var(--text)', lineHeight: 1.5, marginBottom: 6 }}>
          {q.question}
        </p>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center' }}>
          <RoundTypeTag type={q.round_type} />
          <DifficultyTag diff={q.difficulty} />
          {showCompany && q.company && (
            <span className="tag tag-gold">{q.company}</span>
          )}
          {q.frequency > 1 && (
            <span className="tag" style={{ background: 'rgba(232,200,122,0.06)', color: 'var(--text3)', fontSize: 9 }}>
              asked {q.frequency}×
            </span>
          )}
        </div>
      </div>
      <div className="flex-between" style={{ marginTop: 8 }}>
        <span style={{ fontSize: 10, color: 'var(--text4)' }}>
          {q.date_scraped?.slice(0, 10) || ''} · {SOURCE_LABELS[q.source] || q.source || ''}
        </span>
        <AddToPracticeBtn roundId={q.id} />
      </div>
    </div>
  );
}

// ─── TAB: Dashboard ──────────────────────────────────────────────────────────

function DashboardTab({ setTab, setCompanyFilter }) {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['portalStats'],
    queryFn: api.getPortalStats,
    staleTime: 60000,
  });

  const hotQuestions = stats?.hot_questions || [];
  const heatmap = stats?.company_heatmap || [];
  const recent = stats?.recent_experiences || [];

  return (
    <div>
      {/* Stats Bar */}
      <div className="grid grid-4 mb-16">
        {[
          { label: 'Experiences', value: stats?.total_experiences ?? '—', color: 'var(--gold)' },
          { label: 'Questions', value: stats?.total_questions ?? '—', color: 'var(--cyan)' },
          { label: 'Companies', value: stats?.companies_covered ?? '—', color: 'var(--purple)' },
          { label: 'Tips Shared', value: stats?.tips_shared ?? '—', color: 'var(--green)' },
        ].map(({ label, value, color }) => (
          <div key={label} className="card" style={{ textAlign: 'center', padding: '14px 16px' }}>
            <div style={{ fontSize: 28, fontWeight: 700, fontFamily: 'var(--serif)', color }}>
              {isLoading ? '…' : value}
            </div>
            <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: 2 }}>
              {label}
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-2 mb-16" style={{ gap: 16 }}>
        {/* Hot Questions */}
        <div className="card">
          <div className="flex-between mb-12">
            <div className="card-title" style={{ marginBottom: 0 }}>
              <Zap size={12} style={{ marginRight: 6, verticalAlign: 'middle', color: 'var(--orange)' }} />
              Hot Questions
            </div>
            <button className="btn btn-gold btn-sm" onClick={() => setTab('questions')}>
              View All
            </button>
          </div>
          {isLoading ? (
            <div className="empty-state" style={{ padding: '20px 0' }}>Loading...</div>
          ) : hotQuestions.length === 0 ? (
            <div className="empty-state" style={{ padding: '20px 0' }}>
              No questions yet. Run the scraper or import experiences manually.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {hotQuestions.map((q, i) => (
                <div key={i} style={{
                  padding: '8px 12px',
                  background: 'var(--bg2)',
                  borderRadius: 6,
                  borderLeft: `3px solid ${
                    ROUND_TYPE_COLORS[q.round_type] === 'tag-blue' ? 'var(--blue)'
                    : ROUND_TYPE_COLORS[q.round_type] === 'tag-purple' ? 'var(--purple)'
                    : ROUND_TYPE_COLORS[q.round_type] === 'tag-orange' ? 'var(--orange)'
                    : 'var(--gold)'
                  }`,
                }}>
                  <div style={{ fontSize: 11, color: 'var(--text)', lineHeight: 1.4, marginBottom: 5, fontWeight: 500 }}>
                    {q.question?.length > 120 ? q.question.slice(0, 120) + '…' : q.question}
                  </div>
                  <div style={{ display: 'flex', gap: 5, alignItems: 'center' }}>
                    <RoundTypeTag type={q.round_type} />
                    <DifficultyTag diff={q.difficulty} />
                    {q.company && <span className="tag tag-gold" style={{ fontSize: 8 }}>{q.company}</span>}
                    {q.frequency > 1 && (
                      <span style={{ fontSize: 9, color: 'var(--text4)' }}>{q.frequency}×</span>
                    )}
                    <div style={{ marginLeft: 'auto' }}>
                      <AddToPracticeBtn roundId={q.id} />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Experiences */}
        <div className="card">
          <div className="flex-between mb-12">
            <div className="card-title" style={{ marginBottom: 0 }}>
              <TrendingUp size={12} style={{ marginRight: 6, verticalAlign: 'middle', color: 'var(--cyan)' }} />
              Recent Experiences
            </div>
            <button className="btn btn-gold btn-sm" onClick={() => setTab('experiences')}>
              View All
            </button>
          </div>
          {isLoading ? (
            <div className="empty-state" style={{ padding: '20px 0' }}>Loading...</div>
          ) : recent.length === 0 ? (
            <div className="empty-state" style={{ padding: '20px 0' }}>No experiences yet.</div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
              {recent.map((e, i) => (
                <div key={i} style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  padding: '8px 0', borderBottom: i < recent.length - 1 ? '1px solid var(--bg4)' : 'none',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ fontWeight: 600, fontSize: 12 }}>{e.company || '—'}</span>
                    <span style={{ fontSize: 10, color: 'var(--text3)' }}>{e.role}</span>
                  </div>
                  <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                    <ResultTag result={e.overall_result} />
                    <span style={{ fontSize: 9, color: 'var(--text4)' }}>{e.date_scraped?.slice(0, 10)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Company Heatmap */}
      <div className="card">
        <div className="flex-between mb-12">
          <div className="card-title" style={{ marginBottom: 0 }}>
            <Building2 size={12} style={{ marginRight: 6, verticalAlign: 'middle', color: 'var(--gold)' }} />
            Company Heatmap
          </div>
        </div>
        {isLoading ? (
          <div className="empty-state" style={{ padding: '20px 0' }}>Loading...</div>
        ) : heatmap.length === 0 ? (
          <div className="empty-state" style={{ padding: '20px 0' }}>No data yet.</div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))',
            gap: 8,
          }}>
            {heatmap.map((item) => {
              const heat = Math.min(1, (item.exp_count || 0) / 10);
              return (
                <div
                  key={item.company}
                  onClick={() => { setTab('experiences'); setCompanyFilter(item.company); }}
                  style={{
                    padding: '10px 12px',
                    background: `rgba(232,200,122,${0.03 + heat * 0.12})`,
                    border: `1px solid rgba(232,200,122,${0.1 + heat * 0.25})`,
                    borderRadius: 6,
                    cursor: 'pointer',
                    transition: 'all 0.15s',
                  }}
                >
                  <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--text)', marginBottom: 3 }}>
                    {item.company}
                  </div>
                  <div style={{ fontSize: 10, color: 'var(--gold)' }}>
                    {item.exp_count} exp{item.exp_count !== 1 ? 's' : ''}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── TAB: Questions Bank ──────────────────────────────────────────────────────

function QuestionsTab() {
  const [roundTypeFilter, setRoundTypeFilter] = useState('all');
  const [companyFilter, setCompanyFilter] = useState('');
  const [search, setSearch] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['questionsBank', roundTypeFilter],
    queryFn: () => api.getQuestionsBank({
      round_type: roundTypeFilter !== 'all' ? roundTypeFilter : undefined,
      limit: 200,
    }),
    staleTime: 60000,
  });

  const allQuestions = data?.questions || [];

  const filtered = useMemo(() => {
    let qs = allQuestions;
    if (companyFilter) {
      qs = qs.filter(q => q.company?.toLowerCase().includes(companyFilter.toLowerCase()));
    }
    if (search.trim()) {
      const s = search.trim().toLowerCase();
      qs = qs.filter(q => q.question?.toLowerCase().includes(s));
    }
    return qs;
  }, [allQuestions, companyFilter, search]);

  return (
    <div>
      {/* Round Type Sub-tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 14, flexWrap: 'wrap' }}>
        {[['all', 'All'], ...ROUND_TYPES.map(rt => [rt, ROUND_TYPE_LABELS[rt]])].map(([key, label]) => (
          <button
            key={key}
            className={`btn btn-sm ${roundTypeFilter === key ? 'btn-solid' : 'btn-gold'}`}
            onClick={() => setRoundTypeFilter(key)}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Search + company chips */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 12, alignItems: 'center' }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <Search size={12} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--text3)' }} />
          <input
            placeholder="Search questions..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ paddingLeft: 28 }}
          />
        </div>
        {search && (
          <button className="btn btn-sm btn-gold" onClick={() => setSearch('')}>Clear</button>
        )}
      </div>

      {/* Company quick-filter chips */}
      <div style={{ display: 'flex', gap: 5, marginBottom: 16, flexWrap: 'wrap' }}>
        {TARGET_COMPANIES.map(c => (
          <button
            key={c}
            onClick={() => setCompanyFilter(companyFilter === c ? '' : c)}
            style={{
              padding: '3px 10px', borderRadius: 4, fontSize: 10, cursor: 'pointer',
              background: companyFilter === c ? 'var(--gold)' : 'var(--bg3)',
              color: companyFilter === c ? '#000' : 'var(--text2)',
              border: '1px solid var(--bg4)', fontFamily: 'var(--font)',
              fontWeight: companyFilter === c ? 700 : 400,
            }}
          >
            {c}
          </button>
        ))}
        {companyFilter && (
          <button
            className="btn btn-sm btn-red"
            onClick={() => setCompanyFilter('')}
          >
            Clear
          </button>
        )}
      </div>

      <div style={{ fontSize: 10, color: 'var(--text3)', marginBottom: 12 }}>
        Showing {filtered.length} of {allQuestions.length} questions
      </div>

      {isLoading ? (
        <div className="card"><div className="empty-state">Loading questions...</div></div>
      ) : filtered.length === 0 ? (
        <div className="card">
          <div className="empty-state">
            {allQuestions.length === 0
              ? 'No questions extracted yet. Run the scraper or import experiences manually, then trigger enrichment.'
              : 'No questions match your filters.'}
          </div>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {filtered.map((q, i) => <QuestionCard key={q.id || i} q={q} />)}
        </div>
      )}
    </div>
  );
}

// ─── Rich text renderer ───────────────────────────────────────────────────────

function RichBody({ text, maxLines = 6 }) {
  const [expanded, setExpanded] = useState(false);
  if (!text) return null;

  // Parse markdown-like formatting from raw scraped text
  const lines = text.split('\n').filter(l => l.trim());
  const visible = expanded ? lines : lines.slice(0, maxLines);

  const renderLine = (line, i) => {
    // Bold headers: **text** or # text
    if (/^#{1,3}\s/.test(line)) {
      const content = line.replace(/^#{1,3}\s/, '');
      return <div key={i} style={{ fontWeight: 700, color: 'var(--text)', fontSize: 12, marginTop: 6, marginBottom: 2 }}>{content}</div>;
    }
    if (/^\*\*(.+)\*\*:?$/.test(line)) {
      const content = line.replace(/^\*\*(.+)\*\*:?$/, '$1');
      return <div key={i} style={{ fontWeight: 700, color: 'var(--gold)', fontSize: 11, marginTop: 5 }}>{content}</div>;
    }
    // Round labels: "Round 1", "Round 2:"
    if (/^(round\s*\d+|r\d+[\s:—]|technical round|system design round|behavioral round|hr round|machine coding)/i.test(line.trim())) {
      return (
        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 6 }}>
          <span style={{ fontSize: 9, fontWeight: 700, padding: '2px 6px', background: 'var(--bg3)', border: '1px solid var(--bg4)', borderRadius: 3, color: 'var(--cyan)', letterSpacing: 0.5 }}>
            {line.trim().replace(/:$/, '')}
          </span>
        </div>
      );
    }
    // Numbered or bulleted questions
    if (/^[\d]+\.\s/.test(line.trim()) || /^[-•*]\s/.test(line.trim())) {
      const content = line.trim().replace(/^[\d]+\.\s/, '').replace(/^[-•*]\s/, '');
      // Detect if it looks like a question
      const isQuestion = /\?$/.test(content) || /^(design|implement|solve|find|given|write|explain|describe|what|how|why)/i.test(content);
      return (
        <div key={i} style={{ display: 'flex', gap: 6, marginTop: 3, paddingLeft: 8 }}>
          <span style={{ color: 'var(--text4)', fontSize: 10, flexShrink: 0, marginTop: 1 }}>→</span>
          <span style={{ fontSize: 11, color: isQuestion ? 'var(--text)' : 'var(--text2)', lineHeight: 1.5, fontWeight: isQuestion ? 500 : 400 }}>{content}</span>
        </div>
      );
    }
    // TC/offer lines
    if (/\b(ctc|tc|lpa|offer|compensation|salary)\b/i.test(line)) {
      return <div key={i} style={{ fontSize: 11, color: 'var(--green)', marginTop: 2 }}>💰 {line.trim()}</div>;
    }
    // Tips lines
    if (/^(tip|note|advice|suggestion|key takeaway|important)[:–]/i.test(line.trim())) {
      return <div key={i} style={{ fontSize: 11, color: 'var(--orange)', marginTop: 3, fontStyle: 'italic' }}>💡 {line.trim()}</div>;
    }
    // Normal line
    return <div key={i} style={{ fontSize: 11, color: 'var(--text2)', lineHeight: 1.5, marginTop: 1 }}>{line.trim()}</div>;
  };

  return (
    <div>
      {visible.map(renderLine)}
      {lines.length > maxLines && (
        <button
          onClick={e => { e.stopPropagation(); setExpanded(v => !v); }}
          style={{ fontSize: 10, color: 'var(--cyan)', background: 'none', border: 'none', padding: '4px 0', cursor: 'pointer', marginTop: 4 }}
        >
          {expanded ? '▲ Show less' : `▼ Show ${lines.length - maxLines} more lines`}
        </button>
      )}
    </div>
  );
}

// ─── TAB: Experiences ─────────────────────────────────────────────────────────

const DATE_FILTERS = [
  { label: '7d', days: 7 },
  { label: '30d', days: 30 },
  { label: '60d', days: 60 },
  { label: '90d', days: 90 },
  { label: '6m', days: 180 },
  { label: 'All', days: null },
];
const PAGE_SIZE = 15;

function ExperiencesTab({ companyFilter: initialCompany = '' }) {
  const [companyInput, setCompanyInput] = useState(initialCompany);
  const [resultFilter, setResultFilter] = useState('');
  const [daysFilter, setDaysFilter] = useState(null); // null = all time
  const [page, setPage] = useState(0);
  const qc = useQueryClient();

  // Reset page when filters change
  const resetPage = () => setPage(0);

  const { data: expData, isLoading } = useQuery({
    queryKey: ['portalExperiences', companyInput, daysFilter, page],
    queryFn: () => api.getExperiences({
      company: companyInput || undefined,
      days: daysFilter || undefined,
      limit: PAGE_SIZE,
      offset: page * PAGE_SIZE,
    }),
    staleTime: 30000,
    keepPreviousData: true,
  });

  const experiences = useMemo(() => {
    let exps = expData?.experiences || [];
    if (resultFilter) exps = exps.filter(e => e.overall_result === resultFilter);
    return exps;
  }, [expData, resultFilter]);

  const total = expData?.total || 0;
  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div>
      {/* Filter bar */}
      <div className="card mb-12" style={{ padding: '12px 16px' }}>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <Search size={13} style={{ color: 'var(--text3)', flexShrink: 0 }} />
          <input
            placeholder="Filter by company..."
            value={companyInput}
            onChange={e => { setCompanyInput(e.target.value); resetPage(); }}
            style={{ flex: '1 1 160px', minWidth: 120 }}
          />
          <select
            value={resultFilter}
            onChange={e => { setResultFilter(e.target.value); resetPage(); }}
            style={{ flex: '0 0 130px' }}
          >
            <option value="">All Results</option>
            <option value="offer">✅ Offer</option>
            <option value="reject">❌ Reject</option>
            <option value="ghosted">👻 Ghosted</option>
          </select>
          {/* Date range pills */}
          <div style={{ display: 'flex', gap: 3 }}>
            {DATE_FILTERS.map(({ label, days }) => (
              <button
                key={label}
                onClick={() => { setDaysFilter(days); resetPage(); }}
                style={{
                  padding: '3px 8px', fontSize: 10, borderRadius: 4, cursor: 'pointer',
                  background: daysFilter === days ? 'var(--gold)' : 'var(--bg3)',
                  color: daysFilter === days ? '#000' : 'var(--text3)',
                  border: `1px solid ${daysFilter === days ? 'var(--gold)' : 'var(--bg4)'}`,
                  fontFamily: 'var(--font)', fontWeight: daysFilter === days ? 700 : 400,
                }}
              >
                {label}
              </button>
            ))}
          </div>
          {(companyInput || resultFilter) && (
            <button className="btn btn-sm btn-gold" onClick={() => { setCompanyInput(''); setResultFilter(''); resetPage(); }}>
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Company quick-filter chips */}
      <div style={{ display: 'flex', gap: 5, marginBottom: 12, flexWrap: 'wrap' }}>
        {TARGET_COMPANIES.map(c => (
          <button
            key={c}
            onClick={() => { setCompanyInput(companyInput === c ? '' : c); resetPage(); }}
            style={{
              padding: '3px 10px', borderRadius: 4, fontSize: 10, cursor: 'pointer',
              background: companyInput === c ? 'var(--gold)' : 'var(--bg3)',
              color: companyInput === c ? '#000' : 'var(--text2)',
              border: '1px solid var(--bg4)', fontFamily: 'var(--font)',
              fontWeight: companyInput === c ? 700 : 400,
            }}
          >
            {c}
          </button>
        ))}
      </div>

      {/* Count + pagination summary */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
        <span style={{ fontSize: 10, color: 'var(--text3)' }}>
          {isLoading ? 'Loading…' : `${total} experience${total !== 1 ? 's' : ''} · page ${page + 1} of ${Math.max(1, totalPages)}`}
        </span>
        {total > 0 && (
          <button
            className="btn btn-sm btn-gold"
            onClick={() => { api.fixCompanies(); qc.invalidateQueries({ queryKey: ['portalExperiences'] }); }}
            title="Re-extract company names from Unknown entries"
          >
            Fix Unknown Companies
          </button>
        )}
      </div>

      {isLoading ? (
        <div className="card"><div className="empty-state">Loading experiences...</div></div>
      ) : experiences.length === 0 ? (
        <div className="card">
          <div className="empty-state">
            {companyInput ? `No experiences found for "${companyInput}".` : 'No experiences found. Click Scrape Now to fetch data.'}
          </div>
        </div>
      ) : (
        <>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {experiences.map((exp, i) => <RichExperienceCard key={exp.id || i} exp={exp} />)}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: 6, marginTop: 20, alignItems: 'center' }}>
              <button
                className="btn btn-sm btn-gold"
                disabled={page === 0}
                onClick={() => setPage(p => Math.max(0, p - 1))}
              >
                ← Prev
              </button>
              {Array.from({ length: Math.min(7, totalPages) }, (_, i) => {
                const pageNum = page < 4 ? i : page - 3 + i;
                if (pageNum >= totalPages) return null;
                return (
                  <button
                    key={pageNum}
                    onClick={() => setPage(pageNum)}
                    style={{
                      padding: '4px 10px', fontSize: 11, borderRadius: 4, cursor: 'pointer',
                      background: page === pageNum ? 'var(--gold)' : 'var(--bg3)',
                      color: page === pageNum ? '#000' : 'var(--text2)',
                      border: `1px solid ${page === pageNum ? 'var(--gold)' : 'var(--bg4)'}`,
                      fontFamily: 'var(--font)', fontWeight: page === pageNum ? 700 : 400,
                    }}
                  >
                    {pageNum + 1}
                  </button>
                );
              })}
              <button
                className="btn btn-sm btn-gold"
                disabled={page >= totalPages - 1}
                onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

// ─── Rich Experience Card ─────────────────────────────────────────────────────

function RichExperienceCard({ exp }) {
  const [expanded, setExpanded] = useState(false);
  const { data: roundsData, isLoading: roundsLoading } = useQuery({
    queryKey: ['rounds', exp.id],
    queryFn: () => api.getExperienceRounds(exp.id),
    enabled: expanded,
    staleTime: 300000,
  });
  const rounds = roundsData?.rounds || [];

  const sourceLabel = SOURCE_LABELS[exp.source] || exp.source || '';
  const resultColor = exp.overall_result === 'offer' ? 'var(--green)' : exp.overall_result === 'reject' ? 'var(--red)' : 'var(--text4)';

  return (
    <div className="card" style={{ padding: '14px 16px', borderLeft: `3px solid ${exp.overall_result === 'offer' ? 'var(--green)' : exp.overall_result === 'reject' ? 'var(--red)' : 'var(--bg4)'}` }}>
      {/* Header row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 6, cursor: 'pointer' }} onClick={() => setExpanded(v => !v)}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
          {expanded ? <ChevronDown size={13} style={{ color: 'var(--text4)', flexShrink: 0 }} /> : <ChevronRight size={13} style={{ color: 'var(--text4)', flexShrink: 0 }} />}
          <span style={{ fontWeight: 700, fontSize: 14, color: 'var(--gold)' }}>{exp.company || 'Unknown'}</span>
          {exp.role && <span className="tag tag-blue" style={{ fontSize: 9 }}>{exp.role}</span>}
          {exp.overall_result && exp.overall_result !== 'unknown' && (
            <span style={{ fontSize: 10, fontWeight: 700, color: resultColor }}>
              {exp.overall_result === 'offer' ? '✅ Offer' : exp.overall_result === 'reject' ? '❌ Reject' : exp.overall_result}
            </span>
          )}
          <span className="tag" style={{ fontSize: 8, color: 'var(--text4)', background: 'var(--bg2)' }}>{sourceLabel}</span>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexShrink: 0 }}>
          {exp.tc_offered && <span style={{ fontSize: 10, color: 'var(--green)' }}>💰 {exp.tc_offered}</span>}
          <span style={{ fontSize: 9, color: 'var(--text4)' }}>{exp.date_scraped?.slice(0, 10)}</span>
        </div>
      </div>

      {/* Title */}
      {exp.title && (
        <div style={{ fontSize: 12, color: 'var(--text2)', marginBottom: 6, paddingLeft: 21, fontWeight: 500 }}>
          {exp.title}
        </div>
      )}

      {/* Expanded content */}
      {expanded && (
        <div style={{ paddingLeft: 21, marginTop: 8 }}>
          {/* Summary if available */}
          {exp.body_summary && exp.body_summary !== 'None' && (
            <div style={{ fontSize: 11, color: 'var(--cyan)', background: 'var(--bg2)', padding: '8px 12px', borderRadius: 6, marginBottom: 10, borderLeft: '2px solid var(--cyan)' }}>
              {exp.body_summary}
            </div>
          )}

          {/* Tips */}
          {exp.tips && (
            <div style={{ fontSize: 11, color: 'var(--orange)', marginBottom: 10, fontStyle: 'italic' }}>
              💡 {exp.tips}
            </div>
          )}

          {/* Rounds from DB */}
          {roundsLoading && <div style={{ fontSize: 11, color: 'var(--text3)' }}>Loading rounds…</div>}
          {rounds.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>Interview Rounds</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {rounds.map((r, ri) => (
                  <div key={ri} style={{ background: 'var(--bg2)', borderRadius: 6, padding: '10px 12px', border: '1px solid var(--bg4)' }}>
                    <div style={{ display: 'flex', gap: 6, alignItems: 'center', marginBottom: 4, flexWrap: 'wrap' }}>
                      {r.round_num && <span style={{ fontSize: 10, color: 'var(--text4)' }}>R{r.round_num}</span>}
                      <RoundTypeTag type={r.round_type} />
                      <DifficultyTag diff={r.difficulty} />
                      {r.outcome && r.outcome !== 'unknown' && (
                        <span style={{ fontSize: 9, color: r.outcome === 'pass' ? 'var(--green)' : 'var(--red)' }}>
                          {r.outcome === 'pass' ? '✓ Pass' : '✗ Fail'}
                        </span>
                      )}
                    </div>
                    {r.question && (
                      <div style={{ fontSize: 11, color: 'var(--text)', lineHeight: 1.5 }}>
                        {r.question.length > 300
                          ? <RichBody text={r.question} maxLines={5} />
                          : r.question}
                      </div>
                    )}
                    {r.key_insights && (
                      <div style={{ fontSize: 10, color: 'var(--cyan)', marginTop: 4, fontStyle: 'italic' }}>
                        💡 {r.key_insights}
                      </div>
                    )}
                    {r.id && <AddToPracticeBtn roundId={r.id} />}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Source link */}
          {exp.url && (
            <a href={exp.url} target="_blank" rel="noopener noreferrer"
              style={{ fontSize: 10, color: 'var(--cyan)', display: 'inline-block', marginTop: 4 }}>
              View original post →
            </a>
          )}
        </div>
      )}
    </div>
  );
}

// ─── TAB: By Company ─────────────────────────────────────────────────────────

function ByCompanyTab({ setTab, setExpCompanyFilter }) {
  const [selectedCompany, setSelectedCompany] = useState(null);

  const { data: profile, isLoading: profileLoading } = useQuery({
    queryKey: ['companyPortal', selectedCompany],
    queryFn: () => api.getCompanyPortal(selectedCompany),
    enabled: !!selectedCompany,
    staleTime: 120000,
  });

  return (
    <div>
      {!selectedCompany ? (
        <>
          <div style={{ fontSize: 11, color: 'var(--text3)', marginBottom: 14 }}>
            Click a company to see full profile — experiences, questions, round breakdown.
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 10 }}>
            {TARGET_COMPANIES.map(company => (
              <div
                key={company}
                className="card"
                style={{ cursor: 'pointer', transition: 'border-color 0.15s' }}
                onClick={() => setSelectedCompany(company)}
              >
                <div style={{ fontWeight: 700, fontSize: 14, color: 'var(--gold)', marginBottom: 8 }}>
                  {company}
                </div>
                <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginBottom: 8 }}>
                  {['DSA', 'SD', 'Behavioral'].map(t => (
                    <span key={t} className="tag tag-blue" style={{ fontSize: 8 }}>{t}</span>
                  ))}
                </div>
                <button
                  className="btn btn-gold btn-sm"
                  style={{ width: '100%', justifyContent: 'center' }}
                  onClick={(e) => { e.stopPropagation(); setSelectedCompany(company); }}
                >
                  View Profile
                </button>
              </div>
            ))}
          </div>
        </>
      ) : (
        <div>
          <div className="flex-between mb-16">
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <button className="btn btn-gold btn-sm" onClick={() => setSelectedCompany(null)}>
                ← Back
              </button>
              <h3 style={{ fontSize: 18, color: 'var(--gold)', fontFamily: 'var(--serif)' }}>
                {selectedCompany}
              </h3>
            </div>
            <button
              className="btn btn-gold btn-sm"
              onClick={() => { setExpCompanyFilter(selectedCompany); setTab('experiences'); }}
            >
              View All Experiences
            </button>
          </div>

          {profileLoading ? (
            <div className="card"><div className="empty-state">Loading profile...</div></div>
          ) : profile ? (
            <div>
              {/* Summary stats */}
              <div className="grid grid-4 mb-16">
                <div className="card" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--gold)', fontFamily: 'var(--serif)' }}>
                    {profile.experience_count}
                  </div>
                  <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase' }}>Experiences</div>
                </div>
                <div className="card" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--cyan)', fontFamily: 'var(--serif)' }}>
                    {profile.top_questions?.length ?? 0}
                  </div>
                  <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase' }}>Questions</div>
                </div>
                <div className="card" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--purple)', fontFamily: 'var(--serif)' }}>
                    {Object.keys(profile.round_type_counts || {}).length}
                  </div>
                  <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase' }}>Round Types</div>
                </div>
                <div className="card" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--green)', fontFamily: 'var(--serif)' }}>
                    {profile.intel?.dsa_difficulty || '—'}
                  </div>
                  <div style={{ fontSize: 9, color: 'var(--text3)', textTransform: 'uppercase' }}>DSA Difficulty</div>
                </div>
              </div>

              <div className="grid grid-2 mb-16">
                {/* Round Type Breakdown */}
                <div className="card">
                  <div className="card-title">Round Type Breakdown</div>
                  {Object.keys(profile.round_type_counts || {}).length === 0 ? (
                    <div style={{ fontSize: 11, color: 'var(--text3)' }}>No round data extracted yet.</div>
                  ) : (
                    Object.entries(profile.round_type_counts).sort((a, b) => b[1] - a[1]).map(([rt, count]) => {
                      const total = Object.values(profile.round_type_counts).reduce((a, b) => a + b, 0);
                      return (
                        <div key={rt} style={{ marginBottom: 8 }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 3 }}>
                            <RoundTypeTag type={rt} />
                            <span style={{ fontSize: 11, color: 'var(--text3)' }}>{count}</span>
                          </div>
                          <div style={{ height: 4, background: 'var(--bg4)', borderRadius: 2, overflow: 'hidden' }}>
                            <div style={{
                              height: '100%', borderRadius: 2, background: 'var(--gold)',
                              width: `${Math.round((count / total) * 100)}%`,
                            }} />
                          </div>
                        </div>
                      );
                    })
                  )}
                </div>

                {/* Intel */}
                <div className="card">
                  <div className="card-title">Company Intel</div>
                  {!profile.intel || Object.keys(profile.intel).length === 0 ? (
                    <div style={{ fontSize: 11, color: 'var(--text3)' }}>
                      No company intel yet. Run enrichment after importing experiences.
                    </div>
                  ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                      {profile.intel.tc_range && (
                        <div>
                          <div style={{ fontSize: 9, color: 'var(--text3)', marginBottom: 2 }}>TC RANGE</div>
                          <div style={{ fontSize: 12, color: 'var(--gold)' }}>{profile.intel.tc_range}</div>
                        </div>
                      )}
                      {profile.intel.process && (
                        <div>
                          <div style={{ fontSize: 9, color: 'var(--text3)', marginBottom: 2 }}>PROCESS</div>
                          <div style={{ fontSize: 11, color: 'var(--text2)', lineHeight: 1.5 }}>
                            {typeof profile.intel.process === 'string'
                              ? profile.intel.process
                              : JSON.stringify(profile.intel.process)}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* Top Questions */}
              {(profile.top_questions || []).length > 0 && (
                <div className="card mb-16">
                  <div className="card-title">
                    Real Questions Asked ({selectedCompany})
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {profile.top_questions.map((q, i) => (
                      <div key={i} style={{
                        padding: '8px 12px', background: 'var(--bg2)', borderRadius: 6,
                        borderLeft: '3px solid var(--bg5)',
                      }}>
                        <div style={{ fontSize: 12, color: 'var(--text)', lineHeight: 1.5, marginBottom: 5, fontWeight: 500 }}>
                          {q.question}
                        </div>
                        <div style={{ display: 'flex', gap: 5 }}>
                          <RoundTypeTag type={q.round_type} />
                          <DifficultyTag diff={q.difficulty} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Recent Experiences */}
              {(profile.experiences || []).length > 0 && (
                <div>
                  <div className="card-title" style={{ marginBottom: 8 }}>
                    Recent Experiences
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    {profile.experiences.slice(0, 5).map((exp, i) => (
                      <ExperienceCard key={exp.id || i} exp={exp} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="card">
              <div className="empty-state">No data found for {selectedCompany}.</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ─── TAB: My Tips ─────────────────────────────────────────────────────────────

function MyTipsTab() {
  const qc = useQueryClient();
  const [filterCompany, setFilterCompany] = useState('');
  const [filterRoundType, setFilterRoundType] = useState('');
  const [form, setForm] = useState({ company: '', round_type: '', tip: '' });
  const [formError, setFormError] = useState('');

  const { data: tipsData, isLoading } = useQuery({
    queryKey: ['portalTips', filterCompany, filterRoundType],
    queryFn: () => api.getTips(filterCompany || undefined, filterRoundType || undefined),
    staleTime: 30000,
  });

  const tips = tipsData?.tips || [];

  const saveTip = useMutation({
    mutationFn: (data) => api.saveTip(data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['portalTips'] });
      qc.invalidateQueries({ queryKey: ['portalStats'] });
      setForm({ company: '', round_type: '', tip: '' });
      setFormError('');
    },
    onError: (err) => setFormError(err.message),
  });

  const deleteTip = useMutation({
    mutationFn: (id) => api.deleteTip(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['portalTips'] }),
  });

  const handleSubmit = () => {
    if (!form.tip.trim()) { setFormError('Tip text is required.'); return; }
    setFormError('');
    saveTip.mutate({ company: form.company, round_type: form.round_type, tip: form.tip });
  };

  return (
    <div>
      {/* Add Tip Form */}
      <div className="card mb-16">
        <div className="card-title">Add a Tip</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 8 }}>
          <div>
            <div style={{ fontSize: 9, color: 'var(--text3)', marginBottom: 4 }}>COMPANY</div>
            <input
              list="tip-company-list"
              placeholder="e.g. Amazon (optional)"
              value={form.company}
              onChange={e => setForm(f => ({ ...f, company: e.target.value }))}
            />
            <datalist id="tip-company-list">
              {TARGET_COMPANIES.map(c => <option key={c} value={c} />)}
            </datalist>
          </div>
          <div>
            <div style={{ fontSize: 9, color: 'var(--text3)', marginBottom: 4 }}>ROUND TYPE</div>
            <select value={form.round_type} onChange={e => setForm(f => ({ ...f, round_type: e.target.value }))}>
              <option value="">General</option>
              {ROUND_TYPES.map(rt => (
                <option key={rt} value={rt}>{ROUND_TYPE_LABELS[rt]}</option>
              ))}
            </select>
          </div>
        </div>
        <div style={{ marginBottom: 8 }}>
          <div style={{ fontSize: 9, color: 'var(--text3)', marginBottom: 4 }}>TIP *</div>
          <textarea
            rows={3}
            placeholder="Share a concrete tip, strategy, or insight..."
            value={form.tip}
            onChange={e => setForm(f => ({ ...f, tip: e.target.value }))}
          />
        </div>
        {formError && (
          <div style={{ fontSize: 11, color: 'var(--red)', marginBottom: 8 }}>{formError}</div>
        )}
        <button
          className="btn btn-solid"
          onClick={handleSubmit}
          disabled={saveTip.isPending || !form.tip.trim()}
        >
          {saveTip.isPending ? 'Saving...' : 'Save Tip'}
        </button>
        {saveTip.isSuccess && (
          <span style={{ marginLeft: 12, fontSize: 11, color: 'var(--green)' }}>Tip saved!</span>
        )}
      </div>

      {/* Filter */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 14, alignItems: 'center' }}>
        <input
          list="filter-company-list"
          placeholder="Filter by company..."
          value={filterCompany}
          onChange={e => setFilterCompany(e.target.value)}
          style={{ flex: '1 1 160px', minWidth: 100 }}
        />
        <datalist id="filter-company-list">
          {TARGET_COMPANIES.map(c => <option key={c} value={c} />)}
        </datalist>
        <select
          value={filterRoundType}
          onChange={e => setFilterRoundType(e.target.value)}
          style={{ flex: '0 0 140px' }}
        >
          <option value="">All Round Types</option>
          {ROUND_TYPES.map(rt => (
            <option key={rt} value={rt}>{ROUND_TYPE_LABELS[rt]}</option>
          ))}
        </select>
        {(filterCompany || filterRoundType) && (
          <button className="btn btn-sm btn-gold" onClick={() => { setFilterCompany(''); setFilterRoundType(''); }}>
            Reset
          </button>
        )}
      </div>

      {isLoading ? (
        <div className="card"><div className="empty-state">Loading tips...</div></div>
      ) : tips.length === 0 ? (
        <div className="card">
          <div className="empty-state">
            No tips yet. Add your first one above — strategy tips, things that worked, things to avoid.
          </div>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {tips.map((tip) => (
            <div key={tip.id} className="card" style={{ padding: '12px 16px' }}>
              <div className="flex-between" style={{ marginBottom: 8 }}>
                <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                  {tip.company && <span className="tag tag-gold">{tip.company}</span>}
                  {tip.round_type && <RoundTypeTag type={tip.round_type} />}
                  {!tip.company && !tip.round_type && (
                    <span className="tag" style={{ background: 'var(--bg4)', color: 'var(--text3)' }}>General</span>
                  )}
                </div>
                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                  <span style={{ fontSize: 9, color: 'var(--text4)' }}>{tip.created_at?.slice(0, 10)}</span>
                  <button
                    className="btn btn-sm btn-red"
                    onClick={() => deleteTip.mutate(tip.id)}
                    disabled={deleteTip.isPending}
                    title="Delete tip"
                  >
                    <Trash2 size={11} />
                  </button>
                </div>
              </div>
              <p style={{ fontSize: 12, color: 'var(--text)', lineHeight: 1.6 }}>
                {tip.tip}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

const TABS = [
  { key: 'dashboard', label: 'Dashboard', icon: Layers },
  { key: 'questions', label: 'Questions Bank', icon: BookOpen },
  { key: 'experiences', label: 'Experiences', icon: Search },
  { key: 'company', label: 'By Company', icon: Building2 },
  { key: 'tips', label: 'My Tips', icon: Star },
];

export default function ExperiencesPortal() {
  const [tab, setTab] = useState('dashboard');
  const [expCompanyFilter, setExpCompanyFilter] = useState('');
  const qc = useQueryClient();

  const [scrapeRunning, setScrapeRunning] = useState(false);

  const { data: scrapeStatusData } = useQuery({
    queryKey: ['scrapeStatus'],
    queryFn: api.getScrapeStatus,
    refetchInterval: scrapeRunning ? 3000 : false,
    staleTime: 0,
  });

  useEffect(() => {
    if (scrapeStatusData) {
      if (!scrapeStatusData.running && scrapeRunning) {
        setScrapeRunning(false);
        qc.invalidateQueries({ queryKey: ['portalStats'] });
        qc.invalidateQueries({ queryKey: ['portalQuestions'] });
        qc.invalidateQueries({ queryKey: ['portalExperiences'] });
      }
    }
  }, [scrapeStatusData, scrapeRunning, qc]);

  const scrape = useMutation({
    mutationFn: api.triggerScrape,
    onSuccess: () => setScrapeRunning(true),
  });

  const handleSetTabWithFilter = (newTab) => {
    setTab(newTab);
  };

  return (
    <div className="page">
      <div className="page-header">
        <div className="flex-between">
          <div>
            <h2>Experiences Portal</h2>
            <div className="sub">
              Real interview questions, company profiles, and aggregated insights from the community
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            {scrapeStatusData?.last_run && !scrapeRunning && (
              <span style={{ fontSize: 9, color: 'var(--text4)' }}>
                Last: {scrapeStatusData.last_run.slice(0, 16).replace('T', ' ')}
              </span>
            )}
            <button
              className="btn btn-gold btn-sm"
              onClick={() => scrape.mutate()}
              disabled={scrape.isPending || scrapeRunning}
            >
              <RefreshCw size={12} className={(scrape.isPending || scrapeRunning) ? 'spin' : ''} />
              {scrapeRunning ? 'Scraping…' : scrape.isPending ? 'Starting…' : 'Scrape Now'}
            </button>
          </div>
        </div>
        {scrapeRunning && (
          <div style={{ marginTop: 6, fontSize: 11, color: 'var(--cyan)' }}>
            ⏳ Scraping LeetCode Discuss + Reddit + HackerNews — takes ~45s, page auto-refreshes when done
          </div>
        )}
        {scrape.isSuccess && !scrapeRunning && scrapeStatusData?.last_result && (
          <div style={{ marginTop: 6, fontSize: 11, color: 'var(--green)' }}>
            ✅ Done — {Object.entries(scrapeStatusData.last_result)
              .filter(([k]) => k !== 'question_extraction')
              .map(([k, v]) => `${k}: +${v?.inserted ?? 0}`)
              .join(', ')} new experiences
          </div>
        )}
        {scrape.isError && (
          <div style={{ marginTop: 6, fontSize: 11, color: 'var(--red)' }}>
            ❌ Scrape failed: {scrape.error?.message}
          </div>
        )}
      </div>

      {/* Tab Bar */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20, borderBottom: '1px solid var(--bg4)', paddingBottom: 12 }}>
        {TABS.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => setTab(key)}
            style={{
              display: 'flex', alignItems: 'center', gap: 6,
              padding: '6px 14px', fontSize: 11, fontWeight: 600,
              borderRadius: 'var(--radius)', cursor: 'pointer',
              fontFamily: 'var(--font)', letterSpacing: 0.3,
              background: tab === key ? 'var(--gold)' : 'var(--bg3)',
              color: tab === key ? 'var(--bg)' : 'var(--text2)',
              border: `1px solid ${tab === key ? 'var(--gold)' : 'var(--bg4)'}`,
              transition: 'all 0.15s',
            }}
          >
            <Icon size={12} />
            {label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {tab === 'dashboard' && (
        <DashboardTab
          setTab={handleSetTabWithFilter}
          setCompanyFilter={(c) => { setExpCompanyFilter(c); setTab('experiences'); }}
        />
      )}
      {tab === 'questions' && <QuestionsTab />}
      {tab === 'experiences' && (
        <ExperiencesTab companyFilter={expCompanyFilter} />
      )}
      {tab === 'company' && (
        <ByCompanyTab
          setTab={setTab}
          setExpCompanyFilter={setExpCompanyFilter}
        />
      )}
      {tab === 'tips' && <MyTipsTab />}
    </div>
  );
}
