# Testing Strategy — What's Missing

**Current Problem:** Issues discovered *only through manual testing*. No automated safeguards.

---

## 🏗️ Testing Pyramid (What Should Exist)

```
        ▲
        │      E2E Tests (5%)
        │      - Full user workflows
        │      - API → UI integration
        │    ┌─────────────────┐
        │    │ Integration Tests (15%)
        │    │ - API endpoints return correct data
        │    │ - Database reads/writes
        │    │ - Component + API together
        │    ├──────────────────────┐
        │    │ Unit Tests (80%)
        │    │ - Functions, components, logic
        │    │ - Fast, isolated, no dependencies
        │    └──────────────────────┘
        └─────────────────────────────
```

### Your Current State ❌
```
        ▲
        │      ❌ E2E Tests = 0
        │    ┌─────────────────┐
        │    │ ❌ Integration Tests = 0
        │    │
        │    ├──────────────────────┐
        │    │ ❌ Unit Tests = 0
        │    │
        │    └──────────────────────┘
        └─────────────────────────────
         Manual Testing Only (unreliable, slow)
```

---

## 📋 Issues That Should Have Been Caught Automatically

### Issue 1: Daily Plan Showing Raw Markdown
**Test That Would Catch This:**
```python
# Backend: test that daily plan returns valid markdown
def test_daily_plan_contains_markdown_headers():
    response = get_daily_plan()
    assert "#" in response or "##" in response  # Has markdown

# Frontend: test that TodayPlan component renders markdown
def test_today_plan_renders_headers():
    result = render(<TodayPlan dailyPlan={{ plan: "# Hello\n## World" }} />)
    assert result.getByRole('heading', { level: 1 }).textContent === 'Hello'
    assert not result.textContent.includes('# Hello')  # Not raw text
```

**Missing:** React component test + CSS validation test

---

### Issue 2: LeetCode Data Not Showing in Portal
**Test That Would Catch This:**
```python
# Backend: verify /api/progress returns lc_sync
def test_progress_includes_lc_sync():
    progress = get_progress()
    assert 'lc_sync' in progress
    assert progress['lc_sync']['total'] > 0

# Frontend: verify LeetCode component receives data
def test_leetcode_page_displays_sync_data():
    result = render(<LeetCode />)
    screen.getByText('158')  # Should show total
    screen.getByText('62')   # Should show easy
```

**Missing:** Component test + API integration test

---

### Issue 3: /api/curriculum Failing on Railway
**Test That Would Catch This:**
```python
# Test curriculum generation doesn't timeout
def test_curriculum_endpoint_completes_in_time():
    start = time.time()
    response = get('/api/curriculum')
    duration = time.time() - start

    assert response.status == 200
    assert len(response['items']) > 300
    assert duration < 5  # Should be fast

# Test with Railway-like constraints
def test_curriculum_with_limited_memory():
    # Simulate Railway memory limits
    # Verify endpoint doesn't OOM
```

**Missing:** Performance test + load test

---

## 🛠️ What's Missing in Your Stack

| Layer | What's Missing | Impact | Priority |
|-------|---|---|---|
| **Unit Tests** | No function-level tests | Logic bugs slip through | 🔴 HIGH |
| **Component Tests** | React components untested | UI bugs (like markdown) | 🔴 HIGH |
| **Integration Tests** | API ↔ Database not tested | Data flow breaks | 🔴 HIGH |
| **API Contract Tests** | No validation of response shape | Frontend breaks | 🔴 HIGH |
| **E2E Tests** | No user workflow tests | Full features broken | 🟡 MEDIUM |
| **Performance Tests** | No timeout/load testing | Railway failures | 🟡 MEDIUM |
| **CI/CD Pipeline** | No automated test on push | Bad code merged | 🔴 HIGH |
| **Pre-commit Hooks** | No linting/format checks | Code quality degrades | 🟡 MEDIUM |
| **Error Monitoring** | Limited error logging | Can't diagnose failures | 🟡 MEDIUM |
| **Type Safety** | JavaScript (no TypeScript) | Type mismatches missed | 🟡 MEDIUM |

---

## 🚀 Implementation Plan (Priority Order)

### Phase 1: Foundation (This Week) 🔴 HIGH IMPACT
**Focus:** Catch the bugs you found manually

#### 1.1 Unit Tests — Backend (Python)
```bash
# Install testing framework
pip install pytest pytest-asyncio pytest-cov

# Test structure
tests/
├── unit/
│   ├── test_progress_api.py          # /api/progress returns lc_sync
│   ├── test_curriculum_api.py        # /api/curriculum is fast
│   ├── test_coach_api.py             # Coach endpoints work
│   └── test_knowledge_base.py        # KB search, indexing
└── integration/
    ├── test_progress_with_db.py      # progress.json I/O
    └── test_curriculum_generation.py # Full curriculum processing
```

**Example Test:**
```python
# tests/unit/test_progress_api.py
import pytest
from app.routers.progress import get_progress

@pytest.mark.asyncio
async def test_get_progress_includes_lc_sync():
    """Verify /api/progress returns lc_sync data"""
    progress = await get_progress()

    assert isinstance(progress, dict)
    assert 'lc_sync' in progress
    assert progress['lc_sync']['total'] == 158
    assert progress['lc_sync']['easy'] > 0
    assert 'java_problems' in progress['lc_sync']

@pytest.mark.asyncio
async def test_curriculum_completes_in_time():
    """Verify /api/curriculum doesn't timeout"""
    import time
    start = time.time()
    curriculum = await master_curriculum()
    duration = time.time() - start

    assert duration < 3  # Should complete quickly
    assert len(curriculum['items']) > 300
```

**Run:** `pytest tests/ -v --cov=app --cov=intel`

---

#### 1.2 React Component Tests (Frontend)
```bash
# Install testing library
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Test structure
ui/src/__tests__/
├── components/
│   ├── TodayPlan.test.jsx    # Markdown rendering
│   └── LCProgressChart.test.jsx
├── pages/
│   ├── LeetCode.test.jsx     # Data display
│   └── Dashboard.test.jsx
└── hooks/
    └── useProgress.test.js
```

**Example Test:**
```javascript
// ui/src/__tests__/components/TodayPlan.test.jsx
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import TodayPlan from '../../components/TodayPlan';

describe('TodayPlan', () => {
  it('renders markdown headings correctly', () => {
    const dailyPlan = {
      plan: '# Morning Session\n## DSA Practice\n- Two Pointers\n- Binary Search',
    };

    render(
      <QueryClientProvider client={new QueryClient()}>
        <TodayPlan dailyPlan={dailyPlan} />
      </QueryClientProvider>
    );

    // Should render as heading, not raw text
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Morning Session');
    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('DSA Practice');

    // Should NOT show raw markdown
    expect(screen.queryByText('# Morning Session')).not.toBeInTheDocument();
  });

  it('displays LC data when available', () => {
    const dailyPlan = { plan: '# Plan' };
    render(
      <QueryClientProvider client={new QueryClient()}>
        <TodayPlan dailyPlan={dailyPlan} />
      </QueryClientProvider>
    );
    expect(screen.getByText('AI Daily Plan')).toBeInTheDocument();
  });
});
```

**Run:** `npm run test`

---

### Phase 2: Integration & CI/CD (Next Week) 🟡 MEDIUM IMPACT

#### 2.1 API Integration Tests
```python
# tests/integration/test_api_endpoints.py
@pytest.mark.asyncio
async def test_progress_api_returns_complete_data():
    """Full flow: write to progress.json → read via API"""
    # Write test data
    test_data = {
        'lc_sync': {'total': 158, 'easy': 62},
        'applications': []
    }
    save_progress(test_data)

    # Read via API
    response = await get_progress()

    # Verify complete data roundtrip
    assert response == test_data
```

#### 2.2 CI/CD Pipeline (GitHub Actions)
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-asyncio

      - name: Run backend tests
        run: pytest tests/unit -v --cov=app --cov=intel

      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '22'

      - name: Install UI dependencies
        run: cd ui && npm ci

      - name: Run frontend tests
        run: cd ui && npm run test

      - name: Build UI
        run: cd ui && npm run build

      - name: Block merge if tests fail
        run: |
          if [ $? -ne 0 ]; then
            echo "Tests failed - blocking merge"
            exit 1
          fi
```

**Effect:** Every PR must pass tests before merging.

---

### Phase 3: Advanced Testing (Following Week) 🟢 NICE-TO-HAVE

#### 3.1 E2E Tests (Cypress/Playwright)
```javascript
// e2e/integration/lc-sync.cy.js
describe('LeetCode Sync', () => {
  it('displays synced LC data on dashboard', () => {
    cy.visit('http://localhost:5555');

    // Navigate to LeetCode page
    cy.contains('LeetCode').click();

    // Should show synced data
    cy.contains('158').should('exist');      // total
    cy.contains('62').should('exist');       // easy

    // Should NOT show raw data
    cy.contains('"total": 158').should('not.exist');
  });
});
```

#### 3.2 Performance Tests
```python
# tests/performance/test_endpoints.py
@pytest.mark.asyncio
async def test_endpoints_response_time():
    """Verify endpoints don't timeout on Railway"""
    endpoints = [
        ('/api/curriculum', 3),      # 3 second limit
        ('/api/progress', 0.5),      # 500ms limit
        ('/api/coach/stream', 5),    # 5 second limit (streaming)
    ]

    for endpoint, limit in endpoints:
        start = time.time()
        response = await client.get(endpoint)
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < limit, f"{endpoint} took {duration}s, limit is {limit}s"
```

---

## 📊 Test Coverage Goals

```
Current: 0% coverage
├─ Unit tests: 0%
├─ Integration tests: 0%
└─ E2E tests: 0%

Target (Month 1):
├─ Unit tests: 60% coverage
├─ Integration tests: 30% coverage (critical paths)
└─ E2E tests: 3-5 workflows

Target (Month 2):
├─ Unit tests: 80% coverage
├─ Integration tests: 50% coverage
└─ E2E tests: 10+ workflows
```

**How to measure:**
```bash
# Backend coverage
pytest tests/ --cov=app --cov=intel --cov-report=html
# Opens coverage/index.html

# Frontend coverage
npm run test -- --coverage
```

---

## 🔧 How to Implement This Week

### Step 1: Add Testing Dependencies (15 min)
```bash
# Backend
pip install pytest pytest-asyncio pytest-cov

# Frontend
npm install --save-dev @testing-library/react vitest

# Add to package.json scripts:
"test": "vitest",
"test:coverage": "vitest --coverage"
```

### Step 2: Write 3 Critical Tests (45 min)
```bash
# Backend: test progress API returns lc_sync
# Frontend: test TodayPlan renders markdown
# Frontend: test LeetCode component displays data
```

**Total: 1 hour of work → catches 90% of manual testing issues automatically**

### Step 3: Set Up CI/CD (30 min)
```bash
# Create .github/workflows/test.yml
# Tests run on every push automatically
# Blocks bad merges to main
```

---

## ✅ Why This Matters

| Before (Current) | After (With Tests) |
|---|---|
| 🔴 Find bugs manually | 🟢 Tests find bugs automatically |
| 🔴 Issues slip to production | 🟢 Catch on PR before merge |
| 🔴 Same bugs come back | 🟢 Regression tests prevent repeats |
| 🔴 Refactoring is scary | 🟢 Tests give confidence |
| 🔴 Can't parallelize work | 🟢 Tests document expected behavior |
| 🔴 New features break old ones | 🟢 Tests ensure nothing breaks |

---

## 📝 Summary: What's Missing

**Testing Layers Not Implemented:**
1. ❌ Unit tests (functions, components)
2. ❌ Integration tests (API + Database)
3. ❌ Component tests (React rendering)
4. ❌ E2E tests (user workflows)
5. ❌ Performance tests (response times)
6. ❌ CI/CD pipeline (auto tests on push)
7. ❌ Pre-commit hooks (code quality)
8. ❌ Type safety (TypeScript)
9. ❌ Error logging/monitoring

**Soft Engineering Gaps:**
1. ❌ Code review process
2. ❌ Staging environment for QA
3. ❌ Manual test checklist
4. ❌ Bug tracking system
5. ❌ Release notes/changelog

---

## 🎯 Immediate Action Items

**This Week:**
- [ ] Set up pytest for backend
- [ ] Write 3 unit tests (progress API, curriculum API, TodayPlan component)
- [ ] Set up vitest for frontend
- [ ] Create GitHub Actions workflow

**Next Week:**
- [ ] Reach 60% test coverage
- [ ] Add integration tests
- [ ] Set up pre-commit hooks

**Week 3:**
- [ ] Add E2E tests
- [ ] Add performance benchmarks
- [ ] Document test strategy in team wiki

---

**Questions to ask before each feature:**
1. "What test would prevent regression of this bug?"
2. "How would QA catch this without manual testing?"
3. "What would break if someone changed this code?"
4. "Is this testable? If not, refactor for testability."

