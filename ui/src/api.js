const BASE = '';

async function request(method, path, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`${res.status}: ${text}`);
  }
  return res.json();
}

export const api = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),

  getProgress: () => request('GET', '/api/progress'),
  saveProgress: (data) => request('POST', '/api/progress', data),
  getPortalData: () => request('GET', '/api/portal-data'),
  savePortalData: (data) => request('POST', '/api/portal-data', data),
  getGaps: (level = 'sde2') => request('GET', `/api/gaps?level=${level}`),

  getDailyPlan: () => request('GET', '/api/plan/daily'),
  refreshDailyPlan: () => request('POST', '/api/plan/daily/refresh'),
  getWeeklyPlan: () => request('GET', '/api/plan/weekly'),
  refreshWeeklyPlan: () => request('POST', '/api/plan/weekly/refresh'),
  getPlanStats: () => request('GET', '/api/plan/stats'),

  getTodayLog: () => request('GET', '/api/log/today'),
  getRecentLogs: () => request('GET', '/api/log/recent'),
  logActivity: (data) => request('POST', '/api/log', data),

  getDrillToday: () => request('GET', '/api/drill/today'),
  markDrillDone: (data) => request('POST', '/api/drill/done', data),
  getDrillStats: () => request('GET', '/api/drill/stats'),
  getDrillCompanies: () => request('GET', '/api/drill/companies'),
  getDrillCompany: (c) => request('GET', `/api/drill/company/${c}`),

  getJqa: () => request('GET', '/api/jqa'),
  getJqaList: () => request('GET', '/api/jqa/list'),
  getJqaTopic: (id) => request('GET', `/api/jqa/topic/${id}?hints=true`),
  markJqaDone: (id) => request('POST', `/api/jqa/done/${id}`),

  getMockTrend: () => request('GET', '/api/mock/trend'),
  saveMockScore: (data) => request('POST', '/api/mock/score', data),
  getMockReadiness: (c) => request('GET', `/api/mock/readiness/${c}`),

  getLldProblems: () => request('GET', '/api/lld/problems'),
  getLldProblem: (key) => request('GET', `/api/lld/problem/${key}`),
  saveLldScore: (data) => request('POST', '/api/lld/score', data),
  getLldScores: () => request('GET', '/api/lld/scores'),
  evaluateLld: (data) => request('POST', '/api/lld/evaluate', data),

  getBehavioralCheck: () => request('GET', '/api/behavioral/check'),
  getBehavioralProbes: (lp) => request('GET', `/api/behavioral/probes/${lp}`),

  getTc: (company) => request('GET', `/api/tc/${company}`),
  getBrief: () => request('GET', '/api/brief'),

  coach: (data) => request('POST', '/api/coach', data),
  jdAnalyze: (data) => request('POST', '/api/jd-analyze', data),
  evaluate: (data) => request('POST', '/api/evaluate', data),
  getKbStats: () => request('GET', '/api/coach/kb/stats'),
  getCoachQuestions: () => request('GET', '/api/coach/questions'),

  getCurriculum: () => request('GET', '/api/curriculum'),
  getWarplan: (week) => request('GET', week ? `/api/warplan?week=${week}` : '/api/warplan'),

  syncLeetCode: () => request('POST', '/api/progress/lc/sync'),
  setLcUsername: (username) => request('POST', '/api/progress/lc/username', { username }),

  // JD Analysis (Phases 1–3)
  uploadJd: (data) => request('POST', '/api/intel/jd/upload', data),
  getJdAnalysis: (jdId) => request('GET', `/api/intel/jd/${jdId}`),
  listJds: (company) => request('GET', company ? `/api/intel/jd?company=${encodeURIComponent(company)}` : '/api/intel/jd'),
  analyzeJdGap: (jdId, userSkills) => request('POST', `/api/intel/jd/${jdId}/gap-analysis`, { user_skills: userSkills }),
  generateJdRoadmap: (jdId, userSkills, weeks) => request('POST', `/api/intel/jd/${jdId}/roadmap`, { user_skills: userSkills, weeks }),
  getBehavioralGuide: (company) => request('GET', `/api/intel/jd/behavioral/${encodeURIComponent(company)}`),

  getIntelStats: () => request('GET', '/api/intel/stats'),
  getExperiences: (params) => {
    const qs = new URLSearchParams(params).toString();
    return request('GET', `/api/intel/experiences?${qs}`);
  },
  getTrending: () => request('GET', '/api/intel/trending'),
  getCompanyIntel: (c) => request('GET', `/api/intel/company/${c}`),
  triggerScrape: () => request('POST', '/api/intel/scrape'),
  importExperience: (data) => request('POST', '/api/intel/import', data),

  getCareerLadder: () => request('GET', '/api/career/ladder'),
  getSkillMap: () => request('GET', '/api/career/skill-map'),
  getWeeklyCareerPlan: () => request('GET', '/api/career/weekly-plan'),

  streamCoach(data, onChunk) {
    return fetch(`${BASE}/api/coach/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(async (res) => {
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const chunk = line.slice(6);
            if (chunk === '[DONE]') return;
            onChunk(chunk);
          }
        }
      }
    });
  },
};
