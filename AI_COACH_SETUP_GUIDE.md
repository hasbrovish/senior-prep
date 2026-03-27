# AI Coach Setup & Troubleshooting Guide

## ❌ Problem: AI Coach Not Working

The AI Coach endpoints require `ANTHROPIC_API_KEY` to be configured. Without it, all Claude-powered features fail silently.

---

## 🔧 Setup Instructions

### Option 1: Local Development

Set the API key in your terminal before running the server:

```bash
export ANTHROPIC_API_KEY="sk-ant-v0_..."
python3 -m uvicorn app.main:app --reload --port 5555
```

Or in `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-v0_...
```

Then load it:
```bash
source .env
```

### Option 2: Railway Deployment

1. Go to your Railway project dashboard
2. Click **Settings** → **Variables**
3. Add environment variable:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** `sk-ant-v0_...` (your actual key)
4. Click **Save**
5. Redeploy:
   ```bash
   git push
   ```

---

## 📋 Features Requiring ANTHROPIC_API_KEY

| Feature | Endpoint | Status |
|---------|----------|--------|
| AI Coach Chat | POST `/api/coach` | ❌ Fails without key |
| Coach Stream | POST `/api/coach/stream` | ❌ Fails without key |
| JD Analysis | POST `/api/intel/jd/upload` | ❌ Fails without key |
| Answer Evaluation | POST `/api/evaluate` | ❌ Fails without key |
| Interview Readiness | POST `/api/coach/readiness` | ❌ Fails without key |
| Mock Interview | POST `/api/coach/mock` | ❌ Fails without key |

---

## 🔍 Error Messages

### When API Key is Missing

**Status Code:** 400
**Response:** `{"detail": "ANTHROPIC_API_KEY not configured"}`

**Frontend shows:** "Error: Could not reach the AI coach. Is the server running?"

### When API Key is Invalid

**Status Code:** 401
**Response:** `{"error": "Authentication failed"}`

### When LLM Call Fails

**Status Code:** 500
**Response:** `{"error": "Error calling Claude: ..."}`

---

## ✅ Verification Checklist

### 1. Check API Key is Set
```bash
# Local
echo $ANTHROPIC_API_KEY

# Railway (view logs)
railway logs --follow
# Look for: "✅ ANTHROPIC_API_KEY found"
```

### 2. Test Coach Endpoint Directly
```bash
curl -X POST http://localhost:5555/api/coach \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

**Expected Success Response (200):**
```json
{
  "text": "Hi! I'm your AI coach..."
}
```

**Expected Error Response (400):**
```json
{
  "detail": "ANTHROPIC_API_KEY not configured"
}
```

### 3. Test Coach Stream Endpoint
```bash
curl -X POST http://localhost:5555/api/coach/stream \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Give me a quick tip"}
    ]
  }'
```

**Expected:** Server-Sent Events (SSE) stream
```
data: Hi
data: !
data: [DONE]
```

---

## 🚀 Getting ANTHROPIC_API_KEY

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in (create account if needed)
3. Go to **API Keys** section
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-`)
6. Add to Railway or local environment

---

## 🐛 Troubleshooting

### Issue: Coach shows "No response received"
**Cause:** API key not set or network error
**Fix:**
- Check API key is configured
- Check server logs for errors
- Verify network connectivity

### Issue: Coach message disappears after sending
**Cause:** Streaming failed, fallback to non-streaming also failed
**Fix:**
- Check browser console (F12) for errors
- Verify ANTHROPIC_API_KEY is set
- Check server is running

### Issue: "Could not reach the AI coach. Is the server running?"
**Cause:** Both streaming and non-streaming endpoints failed
**Fix:**
- Verify server is running: `curl http://localhost:5555/health`
- Check ANTHROPIC_API_KEY
- Check server logs for exceptions

### Issue: Coach responds but very slowly
**Cause:** LLM response latency or knowledge base loading
**Fix:**
- First response loads knowledge base (~5-10 seconds)
- Subsequent responses are faster (~1-3 seconds)
- Check internet connection

---

## 📊 Coach Features After Setup

Once ANTHROPIC_API_KEY is configured, the AI Coach provides:

1. **Real-time Streaming Chat**
   - Messages stream character-by-character
   - RAG: Uses your prep documents + interview experiences
   - Context-aware based on tab selection

2. **Interview Preparation**
   - Review DSA gaps
   - Practice STAR stories
   - System design Q&A
   - Mock interview feedback

3. **JD-Driven Prep**
   - Upload job description
   - Get skill gap analysis
   - Generate personalized roadmap
   - Predict likely questions

4. **Answer Evaluation**
   - Get feedback on your answers
   - Scoring (1-5)
   - Improvement suggestions

---

## 🔐 Security Notes

- Never commit API keys to git
- Use environment variables for secrets
- Railway environment variables are encrypted
- Local `.env` files should be in `.gitignore`

---

## 📞 Support

If Coach still doesn't work after setup:

1. Check `/health` endpoint
2. View server logs for errors
3. Verify all other APIs work (Intelligence, Curriculum, etc.)
4. Check browser console (F12) for client-side errors
5. Try both streaming and non-streaming endpoints

---

**Once API key is configured, reload the portal and AI Coach will be fully functional!** ✨
