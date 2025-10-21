import re
import nltk
from textblob import TextBlob
import numpy as np
from collections import Counter

class EmotionDetector:
    """
    Emotion Detection using NLP and Machine Learning algorithms
    Detects emotions: happy, sad, angry, fear, surprise, neutral
    """
    
    def __init__(self):
        """Initialize the emotion detector with keyword patterns"""
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        # Emotion keywords dictionary (expanded for better accuracy)
        self.emotion_keywords = {
            'happy': [
                'happy', 'joy', 'joyful', 'great', 'awesome', 'wonderful',
                'fantastic', 'excellent', 'amazing', 'love', 'loved', 'loving', 'delighted',
                'pleased', 'cheerful', 'glad', 'blessed', 'grateful',
                'fortunate', 'lucky', 'celebrate', 'celebration', 'yay', 'hooray', 'brilliant',
                'perfect', 'beautiful', 'lovely', 'enjoy', 'enjoyed', 'enjoying', 'fun'
            ],
            'excited': [
                'excited', 'thrilled', 'ecstatic', 'pumped', 'hyped', 'energized',
                'enthusiastic', 'eager', 'stoked', 'fired up', 'exhilarated', 'elated'
            ],
            'content': [
                'content', 'satisfied', 'peaceful', 'serene', 'comfortable', 'relaxed',
                'pleased', 'fulfilled', 'gratified'
            ],
            'calm': [
                'calm', 'peaceful', 'tranquil', 'serene', 'composed', 'collected',
                'relaxed', 'mellow', 'zen', 'chill', 'easygoing'
            ],
            'sad': [
                'sad', 'unhappy', 'depressed', 'down', 'miserable', 'upset', 'disappointed',
                'heartbroken', 'lonely', 'alone', 'cry', 'crying', 'tears', 'sorrow',
                'grief', 'regret', 'sorry', 'hurt', 'pain', 'painful', 'miss', 'missing',
                'lost', 'hopeless', 'despair', 'gloomy', 'melancholy', 'blue', 'dejected',
                'disheartened', 'unfortunate', 'tragic', 'tragedy', 'mourn', 'mourning'
            ],
            'tired': [
                'tired', 'exhausted', 'weary', 'fatigued', 'drained', 'worn out',
                'sleepy', 'drowsy', 'lethargic', 'sluggish', 'burned out'
            ],
            'bored': [
                'bored', 'uninterested', 'indifferent', 'apathetic', 'dull', 'monotonous',
                'tedious', 'uninspired', 'listless'
            ],
            'angry': [
                'angry', 'mad', 'furious', 'rage', 'hate', 'hatred', 'annoyed', 'irritated',
                'outraged', 'livid', 'enraged', 'pissed', 'upset',
                'resentful', 'bitter', 'hostile', 'aggressive', 'violent', 'fight',
                'fighting', 'argue', 'arguing', 'argument', 'damn', 'hell', 'stupid', 'idiot',
                'terrible', 'awful', 'worst', 'horrible', 'sucks', 'ridiculous'
            ],
            'frustrated': [
                'frustrated', 'annoyed', 'irritated', 'exasperated', 'aggravated',
                'bothered', 'vexed', 'irked', 'fed up'
            ],
            'disgust': [
                'disgusted', 'disgust', 'revolted', 'repulsed', 'nauseated', 'sick',
                'gross', 'yuck', 'ew', 'nasty', 'vile', 'repugnant'
            ],
            'fear': [
                'fear', 'afraid', 'scared', 'frightened', 'terrified',
                'worried', 'worry', 'nervous', 'panic', 'panicked', 'dread', 'horror',
                'horrified', 'alarmed', 'concerned', 'uneasy', 'tense',
                'overwhelmed', 'insecure', 'threatened', 'danger', 'dangerous', 'risk',
                'risky', 'uncertain', 'doubt', 'doubtful', 'suspicious', 'paranoid'
            ],
            'anxious': [
                'anxious', 'anxiety', 'stressed', 'stress', 'nervous', 'tense',
                'apprehensive', 'uneasy', 'restless', 'on edge', 'jittery'
            ],
            'worried': [
                'worried', 'concern', 'concerned', 'troubled', 'distressed',
                'bothered', 'perturbed', 'fretful'
            ],
            'surprise': [
                'surprise', 'surprised', 'shocking', 'shocked', 'amazed', 'astonished',
                'astounded', 'stunned', 'unexpected', 'wow', 'omg', 'unbelievable',
                'incredible', 'extraordinary', 'remarkable', 'startled', 'speechless',
                'bewildered', 'sudden', 'suddenly', 'whoa'
            ],
            'confused': [
                'confused', 'puzzled', 'perplexed', 'baffled', 'bewildered',
                'mystified', 'disoriented', 'uncertain', 'unclear', 'lost'
            ],
            'neutral': [
                'okay', 'ok', 'fine', 'alright', 'normal', 'regular', 'usual', 'ordinary',
                'average', 'moderate', 'so-so', 'whatever', 'meh', 'nothing', 'neither'
            ]
        }
        
        # Emotion intensifiers
        self.intensifiers = [
            'very', 'extremely', 'really', 'so', 'too', 'quite', 'absolutely',
            'completely', 'totally', 'utterly', 'incredibly', 'exceptionally'
        ]
        
        # Negation words
        self.negations = [
            'not', 'no', 'never', 'neither', 'nobody', 'nothing', 'nowhere',
            'hardly', 'barely', 'scarcely', "n't", 'cannot', 'cant'
        ]
    
    def preprocess_text(self, text):
        """Clean and preprocess the input text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\!\?]', '', text)
        
        # Tokenize
        words = nltk.word_tokenize(text)
        
        return text, words
    
    def calculate_sentiment(self, text):
        """Calculate sentiment polarity and subjectivity using TextBlob"""
        blob = TextBlob(text)
        sentiment = blob.sentiment
        
        return {
            'polarity': round(sentiment.polarity, 3),  # -1 to 1
            'subjectivity': round(sentiment.subjectivity, 3)  # 0 to 1
        }
    
    def detect_emotion_keywords(self, words):
        """Detect emotions based on keyword matching"""
        emotion_scores = {emotion: 0 for emotion in self.emotion_keywords.keys()}
        
        # Check for negations and intensifiers
        for i, word in enumerate(words):
            # Check if word is in any emotion category
            for emotion, keywords in self.emotion_keywords.items():
                if word in keywords:
                    score = 1.0
                    
                    # Check for intensifiers before the word
                    if i > 0 and words[i-1] in self.intensifiers:
                        score *= 1.5
                    
                    # Check for negations before the word
                    if i > 0 and words[i-1] in self.negations:
                        score *= -0.5  # Reverse the emotion
                    
                    emotion_scores[emotion] += score
        
        return emotion_scores
    
    def detect(self, text):
        """
        Main method to detect emotion from text
        Returns: dict with emotion, confidence, and all emotion scores
        """
        if not text or not text.strip():
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'all_emotions': {},
                'sentiment': {'polarity': 0.0, 'subjectivity': 0.0}
            }
        
        # Preprocess
        processed_text, words = self.preprocess_text(text)
        
        # Get sentiment
        sentiment = self.calculate_sentiment(processed_text)
        
        # Detect emotions using keywords
        emotion_scores = self.detect_emotion_keywords(words)
        
        # Adjust scores based on sentiment polarity
        if sentiment['polarity'] > 0.3:
            emotion_scores['happy'] += sentiment['polarity'] * 2
        elif sentiment['polarity'] < -0.3:
            emotion_scores['sad'] += abs(sentiment['polarity']) * 1.5
            emotion_scores['angry'] += abs(sentiment['polarity']) * 1.0
        
        # If no emotions detected, use sentiment to determine emotion
        if sum(emotion_scores.values()) == 0:
            if sentiment['polarity'] > 0.1:
                emotion_scores['happy'] = sentiment['polarity']
            elif sentiment['polarity'] < -0.1:
                emotion_scores['sad'] = abs(sentiment['polarity'])
            else:
                emotion_scores['neutral'] = 1.0
        
        # Normalize scores
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            normalized_scores = {
                emotion: round(score / total_score, 3)
                for emotion, score in emotion_scores.items()
            }
        else:
            normalized_scores = {emotion: 0.0 for emotion in emotion_scores.keys()}
            normalized_scores['neutral'] = 1.0
        
        # Get dominant emotion
        dominant_emotion = max(normalized_scores, key=normalized_scores.get)
        confidence = normalized_scores[dominant_emotion]
        
        return {
            'emotion': dominant_emotion,
            'confidence': round(confidence, 3),
            'all_emotions': normalized_scores,
            'sentiment': sentiment
        }

# Test the detector
if __name__ == '__main__':
    detector = EmotionDetector()
    
    test_texts = [
        "I am so happy and excited about this!",
        "This is terrible and makes me really angry.",
        "I'm feeling sad and lonely today.",
        "That was a shocking surprise!",
        "I'm worried and afraid about the future.",
        "Everything is just okay, nothing special."
    ]
    
    print("Testing Emotion Detector:\n")
    for text in test_texts:
        result = detector.detect(text)
        print(f"Text: {text}")
        print(f"Emotion: {result['emotion']} (Confidence: {result['confidence']})")
        print(f"All emotions: {result['all_emotions']}")
        print(f"Sentiment: {result['sentiment']}\n")
