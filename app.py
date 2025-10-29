from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from emotion_detector import EmotionDetector
from face_emotion_detector import FaceEmotionDetector
from database import EmotionDatabase
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Initialize detectors
text_detector = EmotionDetector()
face_detector = FaceEmotionDetector()

# Initialize database
db = EmotionDatabase('emotion_data.db')
print("[APP] Database initialized")

# Keep in-memory history for backward compatibility (optional)
emotion_history = []

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for deployment platforms"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Emotion Detection',
        'version': '1.0'
    }), 200

@app.route('/camera-test')
def camera_test():
    """Serve the camera test page"""
    from flask import send_from_directory
    return send_from_directory('static', 'camera-test.html')

@app.route('/data')
def data_viewer():
    """Serve the database viewer page"""
    return render_template('data_viewer.html')

@app.route('/api/detect', methods=['POST'])
def detect_emotion():
    """
    API endpoint to detect emotion from text
    Expects JSON: {"text": "your text here"}
    Returns: {"emotion": "happy", "confidence": 0.95, "all_emotions": {...}}
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided',
                'message': 'Please provide text in the request body'
            }), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                'error': 'Empty text',
                'message': 'Please provide non-empty text'
            }), 400
        
        if len(text) > 5000:
            return jsonify({
                'error': 'Text too long',
                'message': 'Please provide text with less than 5000 characters'
            }), 400
        
        # Detect emotion
        result = text_detector.detect(text)
        
        # Save to database
        db_entry = {
            'text': text,
            'emotion': result['emotion'],
            'confidence': result['confidence'],
            'all_emotions': result['all_emotions'],
            'sentiment_polarity': result['sentiment']['polarity'],
            'sentiment_subjectivity': result['sentiment']['subjectivity'],
            'type': 'text',
            'timestamp': datetime.now().isoformat()
        }
        db.add_emotion(db_entry)
        
        # Also add to in-memory history for quick access
        history_entry = {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'emotion': result['emotion'],
            'confidence': result['confidence'],
            'timestamp': db_entry['timestamp'],
            'type': 'text'
        }
        emotion_history.append(history_entry)
        
        # Keep only last 50 entries in memory
        if len(emotion_history) > 50:
            emotion_history.pop(0)
        
        return jsonify({
            'success': True,
            'emotion': result['emotion'],
            'confidence': result['confidence'],
            'all_emotions': result['all_emotions'],
            'sentiment': result['sentiment'],
            'text_length': len(text),
            'timestamp': history_entry['timestamp']
        })
    
    except Exception as e:
        app.logger.error(f"Error in detect_emotion: {str(e)}")
        return jsonify({
            'error': 'Processing error',
            'message': 'An error occurred while processing your request'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get emotion detection history from database"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = db.get_recent_history(limit)
        
        # Format for frontend
        formatted_history = []
        for entry in history:
            formatted_history.append({
                'text': entry['text'][:100] + '...' if len(entry.get('text', '')) > 100 else entry.get('text', 'Facial expression'),
                'emotion': entry['emotion'],
                'confidence': entry['confidence'],
                'timestamp': entry['timestamp'],
                'type': entry['type']
            })
        
        return jsonify({
            'success': True,
            'history': formatted_history
        })
    except Exception as e:
        app.logger.error(f"Error in get_history: {str(e)}")
        return jsonify({
            'error': 'Error fetching history',
            'message': str(e)
        }), 500

@app.route('/api/detect-face', methods=['POST'])
def detect_face_emotion():
    """
    API endpoint to detect emotion from facial expression
    Expects JSON: {"image": "base64_encoded_image"}
    Returns: {"emotion": "happy", "confidence": 0.95, "all_emotions": {...}}
    """
    try:
        print("[API] Received face detection request")
        data = request.get_json()
        
        if not data or 'image' not in data:
            print("[ERROR] No image data in request")
            return jsonify({
                'error': 'No image provided',
                'message': 'Please provide a base64 encoded image'
            }), 400
        
        image_data = data['image']
        print(f"[API] Image data received, length: {len(image_data)}")
        
        # Detect emotion from face
        print("[API] Calling face detector...")
        result = face_detector.detect_from_base64(image_data)
        print(f"[API] Detection result: {result}")
        
        if not result.get('success', False):
            error_msg = result.get('error', 'Failed to detect emotion')
            print(f"[ERROR] Detection failed: {error_msg}")
            return jsonify({
                'error': 'Detection failed',
                'message': error_msg
            }), 400
        
        # Save to database
        db_entry = {
            'text': f"Facial expression detected ({result.get('faces_detected', 1)} face(s))",
            'emotion': result['emotion'],
            'confidence': result['confidence'],
            'all_emotions': result['all_emotions'],
            'type': 'face',
            'faces_detected': result.get('faces_detected', 1),
            'method': result.get('method', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }
        db.add_emotion(db_entry)
        
        # Also add to in-memory history
        history_entry = {
            'text': db_entry['text'],
            'emotion': result['emotion'],
            'confidence': result['confidence'],
            'timestamp': db_entry['timestamp'],
            'type': 'face'
        }
        emotion_history.append(history_entry)
        
        # Keep only last 50 entries in memory
        if len(emotion_history) > 50:
            emotion_history.pop(0)
        
        return jsonify({
            'success': True,
            'emotion': result['emotion'],
            'confidence': result['confidence'],
            'all_emotions': result['all_emotions'],
            'faces_detected': result.get('faces_detected', 1),
            'method': result.get('method', 'unknown'),
            'timestamp': history_entry['timestamp']
        })
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[EXCEPTION] Error in detect_face_emotion: {str(e)}")
        print(f"[TRACEBACK] {error_trace}")
        app.logger.error(f"Error in detect_face_emotion: {str(e)}")
        app.logger.error(f"Traceback: {error_trace}")
        return jsonify({
            'error': 'Processing error',
            'message': f'An error occurred while processing your image: {str(e)}'
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about detected emotions from database"""
    try:
        stats = db.get_statistics()
        
        return jsonify({
            'success': True,
            'stats': {
                'total': stats['total_detections'],
                'emotions': stats['emotion_counts'],
                'by_type': stats['type_counts'],
                'avg_confidence': stats['avg_confidence'],
                'daily_activity': stats['daily_activity']
            }
        })
    
    except Exception as e:
        app.logger.error(f"Error in get_stats: {str(e)}")
        return jsonify({
            'error': 'Error fetching statistics',
            'message': str(e)
        }), 500

@app.route('/api/database-info', methods=['GET'])
def get_database_info():
    """Get database information"""
    try:
        info = db.get_database_info()
        return jsonify({
            'success': True,
            'database': info
        })
    except Exception as e:
        app.logger.error(f"Error in get_database_info: {str(e)}")
        return jsonify({
            'error': 'Error fetching database info',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found', 'message': 'The requested resource was not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error', 'message': 'An internal error occurred'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable (for deployment) or use 5000 for local
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Run the app
    app.run(debug=debug, host='0.0.0.0', port=port)
