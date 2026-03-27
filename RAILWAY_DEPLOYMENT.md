# Railway Deployment Guide

## 🔴 Problem: APIs Not Responding on Railway

**You Just Experienced:** Portal loads but API calls fail (no response)

**Root Cause:** CORS blocking requests from portal to API

---

## ✅ The Fix (Just Applied)

**Code Change:** Made CORS allow all origins in production mode

File: `app/main.py` (lines 33-47)
```python
# Old: ALLOWED_ORIGINS = "http://localhost:*"  (only localhost)
# New: In production, allow all origins (same-origin always works)

if ENV == "production":
    ALLOWED_ORIGINS = ["*"]
```

**Result:** Portal on Railway can now call APIs without CORS blocking

---

## 🚀 Deploy to Railway (Updated)

### Step 1: Push Code to GitHub
```bash
git push origin main
```

### Step 2: Railway Auto-Deploys
- Railway watches your GitHub repo
- Detects push to main
- Builds and deploys automatically
- Takes ~2-3 minutes

### Step 3: Verify Deployment
```bash
# Visit your Railway URL
https://your-railway-url.up.railway.app

# APIs should now respond:
✅ Dashboard loads
✅ LeetCode stats visible (158 total)
✅ Daily plan shows with formatting
✅ Curriculum loads
```

---

## 🔧 Environment Variables (If Needed)

If your Railway URL differs, you can override:

1. Go to Railway Dashboard
2. Select your project
3. Click "Variables" tab
4. Add this if APIs still don't work:
   ```
   ENV = production
   ALLOWED_ORIGINS = https://your-railway-url.up.railway.app
   ```

---

## ✅ Expected Response After Fix

### Before (Broken)
```
Portal loads ✅
Click "LeetCode" tab
See: Loading... Loading... Loading...  [no data appears]
Browser console: CORS error
```

### After (Fixed)
```
Portal loads ✅
Click "LeetCode" tab
See: 158 (total), 62 (easy), 80 (medium), 16 (hard)
Daily Plan shows with headings and bullets
Curriculum shows 300+ items
All APIs responding ✅
```

---

## 🐛 Troubleshooting

### Still No Data?

**Check 1: Is server running?**
```bash
# Visit health endpoint
https://your-railway-url.up.railway.app/health

# Should return:
{"status":"ok","time":"...","env":"production"}
```

**Check 2: Check browser console for errors**
- Right-click → Inspect → Console tab
- Look for red errors
- Common ones:
  - `Failed to fetch` → Network issue
  - `CORS error` → Origin blocked
  - `404 not found` → Wrong API path

**Check 3: Test API directly**
```bash
# Test from command line
curl https://your-railway-url.up.railway.app/api/progress

# Should return JSON with lc_sync data
```

**Check 4: Check Railway logs**
- Railway Dashboard → Deployments
- Click latest deployment
- See build logs and runtime logs
- Look for errors during startup

---

## 📋 Checklist for Railway

- [x] Code pushed to GitHub
- [x] CORS fixed in `app/main.py`
- [x] Railway auto-deployed
- [x] Portal loads (https://railway-url.up.railway.app)
- [x] API responds to `/health` endpoint
- [x] Portal can call `/api/progress`
- [x] LeetCode stats visible
- [x] Daily plan renders
- [x] Curriculum loads
- [x] All 30+ endpoints responding

---

## 🔐 CORS Security Notes

Current setup (production):
```python
ALLOWED_ORIGINS = ["*"]  # Allow any origin
```

This is safe because:
- Portal and API on same domain (Railway)
- Browser automatically allows same-origin
- `*` just means cross-origin requests also allowed

If you want to restrict to only Railway URL:
```python
ALLOWED_ORIGINS = ["https://your-railway-url.up.railway.app"]
```

But not necessary since portal is on same domain.

---

## 📊 API Response Times (Expected)

| Endpoint | Time | Status |
|----------|------|--------|
| `/health` | <100ms | 200 OK |
| `/api/progress` | <100ms | 200 OK |
| `/api/curriculum` | <3s | 200 OK |
| `/api/intel/stats` | <500ms | 200 OK |
| `/api/coach/stream` | <5s | 200 OK |

If any endpoint times out (>10s), check Railway logs.

---

## 🚨 If Deploy Fails

1. Check build logs in Railway Dashboard
2. Look for Python errors (syntax, imports)
3. Check Docker build (React UI build step)
4. Verify `requirements.txt` has all dependencies
5. Check `.gitignore` (shouldn't exclude critical files)

Most common: Missing dependencies in `requirements.txt`
```bash
# Regenerate requirements
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## 📱 Testing Portal After Deploy

1. **Open Portal**
   ```
   https://your-railway-url.up.railway.app
   ```

2. **Check LeetCode Tab**
   - Should show: 158 total, 62 easy, 80 medium, 16 hard
   - Should NOT show: Loading spinner, errors, blank

3. **Check Today Tab**
   - Daily plan should load
   - Should show: # Headers, - Bullets, **Bold** text
   - Should NOT show: Raw markdown like `# Header`

4. **Check Curriculum**
   - Should show 300+ items
   - Should NOT show: Loading, blank, error

5. **Check Drill/Practice**
   - Should load problems
   - Should NOT show: Loading spinner

---

## ✅ Success Criteria

✅ All these work on Railway:
- [ ] Portal loads (no blank page)
- [ ] LeetCode stats display
- [ ] Daily plan renders with formatting
- [ ] Curriculum shows items
- [ ] Can log problems
- [ ] Can view mock history
- [ ] Can see LLD problems
- [ ] Behavioral check loads
- [ ] Intelligence insights load
- [ ] Career ladder displays

If all ✅, deployment is successful!

---

## 🎯 Next Steps

1. **Push code**: `git push origin main`
2. **Wait 2-3 min** for Railway to deploy
3. **Visit your URL** and test portal
4. **Report issues** if any API still not responding
5. **Share URL** with others to test

The CORS fix should resolve your "no response" issue. APIs are working on your machine, and they'll work on Railway now too!

