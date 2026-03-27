# Running Tests — Quick Start

This guide shows how to run the tests that catch the bugs you found manually.

---

## ✅ What's Being Tested

| Test | Catches Issue | How to Run |
|------|---|---|
| Progress API | LC data not in progress.json | `pytest tests/unit/test_progress_api.py` |
| Curriculum API | Endpoint timeouts on Railway | `pytest tests/unit/test_curriculum_api.py` |
| TodayPlan Component | Markdown showing as raw text | `npm run test TodayPlan.test.jsx` |
| LeetCode Page | LC stats not visible in portal | `npm run test LeetCode.test.jsx` |

---

## 🚀 Backend Tests (Python)

### Install testing tools
```bash
pip install pytest pytest-asyncio pytest-cov pytest-timeout
```

### Run all backend tests
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/unit/test_progress_api.py -v
```

### Run with coverage report
```bash
pytest tests/ --cov=app --cov=intel --cov-report=html
open htmlcov/index.html
```

### Example Output
```
tests/unit/test_progress_api.py::test_lc_sync_is_included_in_progress PASSED
tests/unit/test_progress_api.py::test_lc_sync_languages_breakdown PASSED
tests/unit/test_curriculum_api.py::test_curriculum_response_structure PASSED
tests/unit/test_curriculum_api.py::test_curriculum_endpoint_performance PASSED

✅ 4 passed in 0.12s
```

---

## 🎨 Frontend Tests (React)

### Install testing library
```bash
cd ui
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
```

### Add to ui/package.json scripts
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

### Run all frontend tests
```bash
cd ui
npm run test
```

### Run specific test file
```bash
npm run test TodayPlan.test.jsx
```

### Run with UI dashboard
```bash
npm run test:ui
# Opens interactive test dashboard
```

### Example Output
```
✓ TodayPlan.test.jsx (3 tests)
  ✓ should render without crashing
  ✓ should display markdown headings as actual headings
  ✓ should render markdown bullets as list items

✓ LeetCode.test.jsx (5 tests)
  ✓ should display synced LC stats
  ✓ should show total label
  ✓ should have form to log new problems
  ✓ should filter problems correctly
  ✓ should display pattern distribution

✅ 8 passed
```

---

## 🔄 Run Both Together

```bash
# Backend tests
pytest tests/unit -v

# Frontend tests
cd ui && npm run test

# Or use a combined script (optional)
./run-all-tests.sh
```

---

## 📊 Understanding Coverage

Coverage shows what % of code is tested:

```
Name                      Stmts   Miss  Cover
───────────────────────────────────────────
app/routers/progress.py      32     2    94%
intel/knowledge_base.py     210    45    79%
───────────────────────────────────────────
Total                       500    60    88%
```

**Goal: 80%+ coverage by end of month**

---

## ❌ What Happens When Tests Fail

### Backend test failure
```python
AssertionError: lc_sync missing required field: total
test_progress_api.py::test_lc_sync_is_included_in_progress FAILED
```

**Action:** Check that progress.json includes `lc_sync` with `total` field

### Frontend test failure
```
● TodayPlan › should display markdown headings

  AssertionError: Unable to find an element with the role "heading", level: 1
```

**Action:** Check that TodayPlan component imports and uses ReactMarkdown correctly

---

## 🛠️ Debugging Tests

### Run single test in debug mode
```bash
pytest tests/unit/test_progress_api.py::test_lc_sync_is_included_in_progress -vvs
```

### Stop on first failure
```bash
pytest tests/ -x  # Exit on first failure
```

### Show print statements
```bash
pytest tests/ -s  # Show stdout
```

---

## 📝 Writing New Tests

### Backend test template
```python
def test_your_feature_works():
    """Describe what should happen"""
    # Setup
    data = {"key": "value"}

    # Action
    result = function_to_test(data)

    # Assert
    assert result == expected_value, "Describe what went wrong"
```

### Frontend test template
```javascript
it('should do something', () => {
  // Setup
  const { getByText } = render(<YourComponent prop="value" />);

  // Action + Assert
  expect(getByText('Expected Text')).toBeInTheDocument();
});
```

---

## 🎯 Next Steps

1. ✅ Run tests to verify they pass
   ```bash
   pytest tests/unit -v
   cd ui && npm run test
   ```

2. ✅ Check coverage
   ```bash
   pytest tests/unit --cov=app --cov-report=term-missing
   ```

3. ✅ Add 2-3 more tests for critical features (drill, coach, mock)

4. ✅ Set up CI/CD to run tests automatically on every push

---

## 📞 Common Issues

### "ModuleNotFoundError: No module named 'pytest'"
```bash
pip install pytest pytest-asyncio
```

### "Cannot find module react-markdown in TodayPlan"
```bash
cd ui && npm install react-markdown
```

### "TypeError: client is not defined"
In frontend tests, wrap component in `QueryClientProvider`:
```javascript
<QueryClientProvider client={new QueryClient()}>
  <YourComponent />
</QueryClientProvider>
```

---

**Questions?**
- Check individual test files for comments explaining what's being tested
- Read `TESTING_STRATEGY.md` for deeper understanding
- See example test outputs above

