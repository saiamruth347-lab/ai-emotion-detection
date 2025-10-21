# 🎭 AI Emotion Detection Web Application

A comprehensive real-time emotion detection web application that uses Machine Learning, Natural Language Processing (NLP), and Computer Vision to analyze emotions from multiple input sources.

## 🌟 Features

### Multi-Modal Detection
- **📝 Text Analysis**: Analyze emotions from written text using NLP
- **😊 Facial Expression Detection**: Real-time emotion detection from webcam using Computer Vision
- **🎤 Speech Analysis**: Coming soon!

### Core Features
- **7 Emotion Categories**: Happy, Sad, Angry, Fear, Surprise, Neutral, Disgust
- **Real-time Processing**: Instant emotion detection with ML algorithms
- **Sentiment Analysis**: Polarity and subjectivity scores for text
- **Face Detection**: Automatic face detection and emotion recognition
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Analysis History**: Track your recent emotion analyses across all modes
- **Statistics Dashboard**: View emotion detection statistics
- **Secure Backend**: Flask-based API with proper error handling

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3 (Modern design with CSS Grid & Flexbox)
- Vanilla JavaScript (ES6+)

### Backend
- Python 3.8+
- Flask (Web framework)
- NLTK (Natural Language Toolkit)
- TextBlob (Sentiment analysis)
- OpenCV (Computer Vision for face detection)
- DeepFace (Facial emotion recognition)
- TensorFlow (Deep learning backend)
- NumPy (Numerical computations)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd "c:\Users\saiam\Ai Emo Detection"
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Download NLTK Data

The application will automatically download required NLTK data on first run, but you can also do it manually:

```python
python -c "import nltk; nltk.download('punkt')"
```

## 🎯 Running the Application

### 1. Start the Flask Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

### 2. Open in Browser

Navigate to: `http://localhost:5000`

## 📖 How to Use

### Text Analysis Mode
1. **Select Mode**: Click on "Text Analysis" tab (default)
2. **Enter Text**: Type or paste your text in the input area
3. **Analyze**: Click the "Analyze Emotion" button or press `Ctrl+Enter`
4. **View Results**: See the detected emotion with confidence score
5. **Explore Details**: Check emotion breakdown and sentiment analysis

### Facial Expression Mode
1. **Select Mode**: Click on "Facial Expression" tab
2. **Start Camera**: Click "Start Camera" and allow camera permissions
3. **Position Face**: Make sure your face is clearly visible in the camera
4. **Capture**: Click "Capture & Analyze" to detect emotion
5. **View Results**: See detected emotion from your facial expression
6. **Stop Camera**: Click "Stop Camera" when done

### General
- **Track History**: View your recent analyses in the history section
- **View Statistics**: Check emotion detection statistics across all modes

## 🎨 Features Explained

### Emotion Detection
The application uses a hybrid approach combining:
- **Keyword Matching**: Extensive emotion keyword dictionaries
- **Sentiment Analysis**: TextBlob for polarity and subjectivity
- **Context Analysis**: Handles negations and intensifiers
- **Confidence Scoring**: Normalized probability scores for each emotion

### Supported Emotions
- 😊 **Happy**: Joy, excitement, pleasure
- 😢 **Sad**: Sorrow, disappointment, grief
- 😠 **Angry**: Rage, frustration, irritation
- 😨 **Fear**: Anxiety, worry, dread
- 😲 **Surprise**: Shock, amazement, astonishment
- 😐 **Neutral**: Calm, indifferent, balanced
- 🤢 **Disgust**: Revulsion, distaste (facial expressions only)

### Facial Expression Detection
The application uses advanced computer vision:
- **Face Detection**: OpenCV Haar Cascade for detecting faces
- **Emotion Recognition**: DeepFace with pre-trained models
- **Real-time Processing**: Webcam capture and instant analysis
- **Multi-face Support**: Can detect emotions from multiple faces

### Sentiment Metrics
- **Polarity**: -1 (negative) to +1 (positive)
- **Subjectivity**: 0 (objective) to 1 (subjective)

## 🔒 Security Features

- Input validation and sanitization
- Character limit enforcement (5000 chars)
- CORS protection
- Error handling and logging
- Rate limiting ready (can be added)

## 📁 Project Structure

```
Ai Emo Detection/
├── app.py                      # Flask application & API endpoints
├── emotion_detector.py         # Text emotion detection (NLP)
├── face_emotion_detector.py    # Facial emotion detection (CV)
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── templates/
│   └── index.html             # Frontend HTML
└── static/
    ├── style.css              # Styling
    └── script.js              # Frontend JavaScript
```

## 🔧 API Endpoints

### POST `/api/detect`
Analyze text and detect emotion

**Request:**
```json
{
  "text": "I am so happy today!"
}
```

**Response:**
```json
{
  "success": true,
  "emotion": "happy",
  "confidence": 0.85,
  "all_emotions": {
    "happy": 0.85,
    "sad": 0.05,
    "angry": 0.02,
    "fear": 0.03,
    "surprise": 0.03,
    "neutral": 0.02
  },
  "sentiment": {
    "polarity": 0.8,
    "subjectivity": 0.9
  }
}
```

### POST `/api/detect-face`
Analyze facial expression and detect emotion

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response:**
```json
{
  "success": true,
  "emotion": "happy",
  "confidence": 0.92,
  "all_emotions": {
    "happy": 0.92,
    "neutral": 0.04,
    "surprise": 0.02,
    "sad": 0.01,
    "angry": 0.01
  },
  "faces_detected": 1,
  "method": "deepface"
}
```

### GET `/api/history`
Get recent emotion detection history (both text and face)

### GET `/api/stats`
Get emotion detection statistics across all modes

## 🎓 Machine Learning Approach

### Text Emotion Detection
1. **Text Preprocessing**: Tokenization, lowercasing, cleaning
2. **Feature Extraction**: Keyword matching with emotion dictionaries
3. **Sentiment Analysis**: TextBlob for polarity/subjectivity
4. **Context Handling**: Negation and intensifier detection
5. **Score Normalization**: Probability distribution across emotions

### Facial Emotion Detection
1. **Face Detection**: Haar Cascade classifier to locate faces
2. **Image Preprocessing**: Resize, normalize, convert color spaces
3. **Deep Learning**: DeepFace with pre-trained CNN models
4. **Emotion Classification**: 7-class emotion recognition
5. **Confidence Scoring**: Softmax probabilities for each emotion

## 🚀 Future Enhancements

- [x] Facial expression detection ✅
- [ ] Speech/audio emotion detection
- [ ] Real-time video emotion tracking
- [ ] Deep Learning text models (BERT, RoBERTa)
- [ ] Multi-language support
- [ ] User authentication & profiles
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Export analysis reports (PDF/CSV)
- [ ] API rate limiting
- [ ] Batch processing
- [ ] Mobile app version

## 🐛 Troubleshooting

### Issue: NLTK Data Not Found
**Solution:** Run `python -c "import nltk; nltk.download('punkt')"`

### Issue: Port 5000 Already in Use
**Solution:** Change port in `app.py`: `app.run(port=5001)`

### Issue: Module Not Found
**Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`

### Issue: Camera Not Working
**Solution:** 
- Check browser permissions for camera access
- Use HTTPS or localhost (required for camera API)
- Ensure no other application is using the camera

### Issue: DeepFace Installation Failed
**Solution:** 
- DeepFace requires TensorFlow which may take time to install
- On first run, DeepFace will download pre-trained models (~100MB)
- If installation fails, the app will use basic face detection (lower accuracy)

## 📝 License

This project is created for educational purposes as part of an AI internship program.

## 👨‍💻 Developer

Created as part of the AI Internship Program - Project 1: Emotion Detection using AI

## 🤝 Contributing

This is an internship project, but suggestions and improvements are welcome!

## 📧 Support

For issues or questions, please refer to the project documentation or contact your internship supervisor.

---

**Built with ❤️ using Flask, Python, NLP & Machine Learning**
