# 🚀 Deployment Guide - AI Emotion Detection

This guide covers multiple deployment options for your Flask application.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ All code committed to Git
- ✅ GitHub repository created (optional but recommended)
- ✅ Updated `requirements.txt` with all dependencies

## 🌐 Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Steps:**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository or upload code
4. Render will auto-detect the `render.yaml` configuration
5. Click "Create Web Service"

**Configuration (if manual setup needed):**
- **Build Command:** `pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt')"`
- **Start Command:** `gunicorn app:app`
- **Environment:** Python 3
- **Port:** 10000 (auto-configured)

**Environment Variables:**
```
PYTHON_VERSION=3.11.0
PORT=10000
```

### Option 2: Railway (Easy Setup)

**Steps:**
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and uses `Procfile`
5. Add environment variables if needed

**Configuration:**
- Railway automatically detects `Procfile` and `requirements.txt`
- No additional configuration needed!

### Option 3: Heroku (Classic Platform)

**Steps:**
1. Install Heroku CLI: `npm install -g heroku`
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

**Configuration:**
- Uses `Procfile` and `runtime.txt` automatically
- Add buildpack if needed: `heroku buildpacks:set heroku/python`

### Option 4: PythonAnywhere (Beginner Friendly)

**Steps:**
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and sign up
2. Upload your code via Files or Git
3. Create a new Web app (Flask)
4. Configure WSGI file to point to `app.py`
5. Install requirements in Bash console: `pip install -r requirements.txt`

## 📦 Required Files (Already Created)

- ✅ `Procfile` - Tells platforms how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `render.yaml` - Render-specific configuration
- ✅ `requirements.txt` - Python dependencies

## ⚙️ Update Requirements

Add `gunicorn` to your requirements.txt for production:

```bash
pip install gunicorn
pip freeze > requirements.txt
```

Or manually add to `requirements.txt`:
```
gunicorn>=21.2.0
```

## 🔐 Environment Variables

For production, set these environment variables:

```
FLASK_ENV=production
SECRET_KEY=your-secure-random-key-here
DEBUG=False
HOST=0.0.0.0
PORT=10000
```

## 🎯 Post-Deployment Checklist

- [ ] Test all endpoints (text detection, face detection)
- [ ] Verify camera permissions work (HTTPS required)
- [ ] Check database initialization
- [ ] Test error handling
- [ ] Monitor logs for issues
- [ ] Set up custom domain (optional)

## 🐛 Common Issues

### Issue: Large Dependencies (TensorFlow, DeepFace)
**Solution:** 
- Some free tiers have memory limits
- Consider using lighter models or upgrading plan
- Render and Railway handle large dependencies well

### Issue: Camera Not Working
**Solution:**
- Ensure deployment uses HTTPS (most platforms do by default)
- Browser requires HTTPS for camera access

### Issue: NLTK Data Not Found
**Solution:**
- Add NLTK download to build command:
  ```
  python -c "import nltk; nltk.download('punkt')"
  ```

### Issue: Port Configuration
**Solution:**
- Use environment variable: `port = int(os.environ.get('PORT', 5000))`
- Update `app.py` if needed

## 📊 Recommended Platform Comparison

| Platform | Free Tier | Ease of Use | Best For |
|----------|-----------|-------------|----------|
| **Render** | ✅ Yes | ⭐⭐⭐⭐ | Production apps |
| **Railway** | ✅ Limited | ⭐⭐⭐⭐⭐ | Quick deploys |
| **Heroku** | ⚠️ Paid | ⭐⭐⭐ | Enterprise |
| **PythonAnywhere** | ✅ Yes | ⭐⭐⭐ | Beginners |

## 🚀 Quick Deploy Commands

### For Render:
```bash
# Push to GitHub, then connect on Render dashboard
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### For Railway:
```bash
# Install Railway CLI (optional)
npm i -g @railway/cli
railway login
railway init
railway up
```

### For Heroku:
```bash
heroku login
heroku create ai-emotion-detection
git push heroku main
heroku open
```

## 📝 Notes

- **Database:** SQLite works for development but consider PostgreSQL for production
- **File Storage:** Uploaded images are temporary; consider cloud storage for persistence
- **Scaling:** Most platforms auto-scale; monitor usage
- **Costs:** Start with free tier, upgrade as needed

## 🎉 Success!

Once deployed, your app will be available at:
- Render: `https://your-app-name.onrender.com`
- Railway: `https://your-app-name.up.railway.app`
- Heroku: `https://your-app-name.herokuapp.com`

---

**Need Help?** Check platform-specific documentation or deployment logs for troubleshooting.
