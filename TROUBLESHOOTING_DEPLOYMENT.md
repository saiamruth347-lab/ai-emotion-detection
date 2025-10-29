# 🔧 Deployment Troubleshooting Guide

## 🚨 Common Deployment Crashes & Fixes

### ❌ Issue 1: Memory Limit Exceeded (Most Common)

**Symptoms:**
```
Killed
OOMKilled
Memory limit exceeded
Process exited with code 137
```

**Cause:** TensorFlow + DeepFace use ~1.5GB RAM. Free tiers have 512MB-1GB limits.

**Solutions:**

#### Option A: Use Lighter Dependencies
Replace `requirements.txt` with `requirements-light.txt`:
```bash
# Rename files
mv requirements.txt requirements-full.txt
mv requirements-light.txt requirements.txt

# Commit and push
git add .
git commit -m "Use lighter dependencies for deployment"
git push origin main
```

**Changes in light version:**
- `tensorflow` → `tensorflow-cpu` (smaller, no GPU)
- `opencv-python` → `opencv-python-headless` (no GUI, smaller)

#### Option B: Upgrade to Paid Tier
- **Railway:** Pro plan ($20/month) - 8GB RAM
- **Render:** Starter plan ($7/month) - 512MB → 2GB RAM

#### Option C: Use Different Platform
- **Google Cloud Run:** 2GB free tier
- **AWS Lambda:** Not suitable for large ML models
- **DigitalOcean App Platform:** $5/month, 1GB RAM

---

### ❌ Issue 2: Port Binding Error

**Symptoms:**
```
Error: Cannot bind to port
Address already in use
Failed to bind to 0.0.0.0:5000
```

**Cause:** App not using platform's PORT environment variable.

**Fix:** Already fixed in `app.py`, but verify:

```python
# Should be in app.py (line 282)
port = int(os.environ.get('PORT', 5000))
```

**Redeploy:**
```bash
git push origin main
```

---

### ❌ Issue 3: Build Timeout

**Symptoms:**
```
Build exceeded time limit
Timeout after 15 minutes
Build failed: timeout
```

**Cause:** Installing TensorFlow takes too long.

**Solutions:**

#### Option A: Increase Build Timeout
**Railway:** Automatically handles this
**Render:** Free tier: 15 min, Paid: 30 min

#### Option B: Use Docker (Advanced)
Create `Dockerfile` for faster builds with caching.

---

### ❌ Issue 4: Missing NLTK Data

**Symptoms:**
```
LookupError: Resource punkt not found
NLTK data not downloaded
```

**Fix:** Already handled in `render.yaml`, but verify build command:

```yaml
buildCommand: pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

**Manual fix:**
Add to your code (in `emotion_detector.py` or `app.py`):
```python
import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
```

---

### ❌ Issue 5: DeepFace Model Download Fails

**Symptoms:**
```
Failed to download model
Connection timeout
Model not found
```

**Cause:** First-time model download during deployment.

**Fix:** Models download on first API call, not during build.

**Workaround:**
Add to build command:
```bash
python -c "from deepface import DeepFace; DeepFace.build_model('Emotion')"
```

---

### ❌ Issue 6: Gunicorn Workers Crash

**Symptoms:**
```
Worker timeout
Worker failed to boot
Gunicorn workers dying
```

**Fix:** Reduce workers or increase timeout.

Update `Procfile`:
```
web: gunicorn --workers=1 --timeout=120 --bind=0.0.0.0:$PORT app:app
```

---

### ❌ Issue 7: Database Permission Error

**Symptoms:**
```
Permission denied: emotion_data.db
Unable to open database file
```

**Cause:** SQLite file can't be written in read-only filesystem.

**Fix:** Use `/tmp` directory for database:

Update `app.py`:
```python
import os
db_path = os.environ.get('DATABASE_PATH', '/tmp/emotion_data.db')
db = EmotionDatabase(db_path)
```

---

## 🔍 How to Debug

### 1. Check Logs
**Railway:**
```
Dashboard → Your Service → Logs tab
```

**Render:**
```
Dashboard → Your Service → Logs
```

### 2. Test Locally First
```bash
# Test with production settings
export FLASK_ENV=production
export DEBUG=False
python app.py
```

### 3. Check Resource Usage
**Railway:**
```
Dashboard → Metrics → RAM/CPU usage
```

### 4. Verify Environment Variables
Make sure these are set:
```
FLASK_ENV=production
DEBUG=False
PORT=10000
```

---

## 🎯 Recommended Fix for Your App

### Step 1: Use Lighter Dependencies
```bash
# Use the light version
git mv requirements.txt requirements-full.txt
git mv requirements-light.txt requirements.txt
git add .
git commit -m "Use tensorflow-cpu for lower memory usage"
git push origin main
```

### Step 2: Update Procfile for Better Stability
```bash
# Edit Procfile
web: gunicorn --workers=1 --threads=2 --timeout=120 --bind=0.0.0.0:$PORT app:app
```

### Step 3: Add Health Check Endpoint
Add to `app.py`:
```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200
```

---

## 📊 Platform-Specific Solutions

### Railway
- **Memory:** Upgrade to Pro ($20/mo) for 8GB RAM
- **Timeout:** No build timeout on Pro
- **Logs:** Real-time in dashboard

### Render
- **Memory:** Free tier = 512MB (too small for TensorFlow)
- **Solution:** Use Starter plan ($7/mo) = 2GB RAM
- **Alternative:** Use `tensorflow-cpu` and `opencv-python-headless`

---

## ✅ Quick Fix Checklist

- [ ] Check deployment logs for specific error
- [ ] Verify `PORT` environment variable is used
- [ ] Use `requirements-light.txt` (tensorflow-cpu)
- [ ] Reduce Gunicorn workers to 1
- [ ] Set database path to `/tmp/`
- [ ] Add health check endpoint
- [ ] Consider upgrading to paid tier

---

## 🆘 Still Crashing?

**Share these details:**
1. Platform (Railway/Render/Heroku)
2. Error message from logs
3. Memory usage from metrics
4. Build command used

**I'll help you fix it!**
