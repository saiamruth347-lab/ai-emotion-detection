# 🚀 Quick Start Guide

## Installation (2 minutes)

### Option 1: Basic Installation (Text Analysis Only)
```bash
# Install core dependencies
pip install flask flask-cors textblob nltk numpy python-dotenv

# Run the app
python app.py
```

### Option 2: Full Installation (Text + Facial Expression)
```bash
# Install all dependencies (may take 5-10 minutes)
pip install flask flask-cors textblob nltk numpy python-dotenv opencv-python pillow deepface tensorflow

# Run the app
python app.py
```

## First Run

1. Open browser: http://localhost:5000
2. Choose your detection mode:
   - **Text Analysis**: Type text and click "Analyze Emotion"
   - **Facial Expression**: Click tab, start camera, and capture

## Quick Test

### Test Text Analysis
```
Text: "I am so happy and excited about this!"
Expected: Happy emotion with high confidence
```

### Test Facial Expression
1. Click "Facial Expression" tab
2. Click "Start Camera"
3. Smile at the camera
4. Click "Capture & Analyze"
5. Expected: Happy emotion detected

## Common Issues

**Camera not working?**
- Allow camera permissions in browser
- Make sure you're on localhost or HTTPS

**DeepFace not installed?**
- App will still work with basic face detection
- Install with: `pip install deepface tensorflow`

**Port 5000 in use?**
- Change port in app.py: `app.run(port=5001)`

## Features Overview

✅ **Text Analysis**: NLP-based emotion detection from text
✅ **Facial Expression**: Computer vision emotion detection from webcam
✅ **7 Emotions**: Happy, Sad, Angry, Fear, Surprise, Neutral, Disgust
✅ **Real-time**: Instant analysis and results
✅ **History**: Track all your analyses
✅ **Statistics**: View emotion distribution

## Next Steps

- Read full documentation: [README.md](README.md)
- Explore the code: Check `app.py`, `emotion_detector.py`, `face_emotion_detector.py`
- Customize: Modify emotion keywords, add new features
- Deploy: Use gunicorn for production deployment

---

**Need help?** Check the full README.md or troubleshooting section!
