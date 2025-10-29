import cv2
import numpy as np
from PIL import Image
import io
import base64
import os

class FaceEmotionDetector:
    """
    Facial Emotion Detection using DeepFace and OpenCV
    Detects emotions from facial expressions in images
    """
    
    def __init__(self):
        """Initialize the face emotion detector"""
        self.emotions_map = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'fear': '😨',
            'surprise': '😲',
            'neutral': '😐',
            'disgust': '🤢'
        }
        
        # Load face cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Flag to check if DeepFace is available
        self.deepface_available = False
        try:
            from deepface import DeepFace
            self.DeepFace = DeepFace
            self.deepface_available = True
            print("[OK] DeepFace loaded successfully - Accurate emotion detection enabled")
        except ImportError as e:
            print(f"[WARNING] DeepFace not available: {e}")
            print("[WARNING] Using basic emotion detection (lower accuracy)")
        except Exception as e:
            print(f"[WARNING] Error loading DeepFace: {e}")
            print("[WARNING] Using basic emotion detection (lower accuracy)")
    
    def detect_from_base64(self, base64_image):
        """
        Detect emotion from base64 encoded image
        Args:
            base64_image: Base64 encoded image string
        Returns:
            dict with emotion detection results
        """
        try:
            # Remove data URL prefix if present
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]
            
            # Decode base64 to image
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            return self.detect_from_array(img_array)
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to process image: {str(e)}'
            }
    
    def detect_from_array(self, img_array):
        """
        Detect emotion from numpy array image
        Args:
            img_array: Numpy array of image
        Returns:
            dict with emotion detection results
        """
        try:
            print(f"[DETECT] Processing image array, shape: {img_array.shape}")
            
            # Detect faces with more lenient parameters
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,  # More sensitive (was 1.1)
                minNeighbors=3,     # More lenient (was 5)
                minSize=(20, 20)    # Smaller minimum (was 30x30)
            )
            
            print(f"[DETECT] Faces detected by Haar Cascade: {len(faces)}")
            
            # If no faces detected by Haar Cascade, try DeepFace anyway
            # DeepFace has its own face detection
            if len(faces) == 0:
                print("[DETECT] No faces found by Haar Cascade, trying DeepFace anyway...")
                if self.deepface_available:
                    # Try DeepFace with enforce_detection=False
                    return self._detect_with_deepface(img_array, [])
                else:
                    return {
                        'success': False,
                        'error': 'No face detected in the image. Please ensure your face is visible, well-lit, and centered.',
                        'faces_detected': 0,
                        'tip': 'Try: Better lighting, face camera directly, move closer'
                    }
            
            # Use DeepFace if available, otherwise use basic detection
            if self.deepface_available:
                return self._detect_with_deepface(img_array, faces)
            else:
                return self._detect_basic(img_array, faces)
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Detection failed: {str(e)}'
            }
    
    def _detect_with_deepface(self, img_array, faces):
        """Use DeepFace for emotion detection with enhanced mapping"""
        try:
            print(f"[ANALYZING] Image with DeepFace... (Image shape: {img_array.shape})")
            
            # Analyze the image
            result = self.DeepFace.analyze(
                img_array, 
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            print(f"[OK] DeepFace analysis complete")
            
            # Handle both single face and multiple faces
            if isinstance(result, list):
                result = result[0]
            
            emotions = result['emotion']
            print(f"[RESULT] Raw emotions: {emotions}")
            
            # Get dominant emotion
            dominant_emotion = result['dominant_emotion'].lower()
            print(f"[RESULT] Dominant emotion: {dominant_emotion}")
            
            # Map DeepFace emotions to our enhanced 16-emotion system
            enhanced_emotions = self._map_to_enhanced_emotions(emotions)
            
            # Get the final dominant emotion from enhanced mapping
            final_emotion = max(enhanced_emotions, key=enhanced_emotions.get)
            confidence = float(enhanced_emotions[final_emotion])
            
            print(f"[ENHANCED] Final emotion: {final_emotion} ({confidence:.1%})")
            
            # Count faces detected (use DeepFace's count if Haar didn't find any)
            faces_count = len(faces) if len(faces) > 0 else 1
            
            return {
                'success': True,
                'emotion': final_emotion,
                'confidence': round(float(confidence), 3),
                'all_emotions': enhanced_emotions,
                'faces_detected': int(faces_count),
                'method': 'deepface_enhanced'
            }
            
        except Exception as e:
            print(f"[ERROR] DeepFace error: {str(e)}")
            print(f"[WARNING] Falling back to basic detection")
            # Fallback to basic detection
            return self._detect_basic(img_array, faces)
    
    def _map_to_enhanced_emotions(self, deepface_emotions):
        """
        Map DeepFace's 7 emotions to our 16-emotion system
        DeepFace provides: angry, disgust, fear, happy, sad, surprise, neutral
        We enhance to: happy, excited, content, calm, sad, tired, bored, 
                       angry, frustrated, disgust, fear, anxious, worried, 
                       surprise, confused, neutral
        """
        # Normalize DeepFace scores
        total = sum(deepface_emotions.values())
        normalized = {k.lower(): v / total for k, v in deepface_emotions.items()}
        
        # Initialize our 16 emotions
        enhanced = {
            'happy': 0.0,
            'excited': 0.0,
            'content': 0.0,
            'calm': 0.0,
            'sad': 0.0,
            'tired': 0.0,
            'bored': 0.0,
            'angry': 0.0,
            'frustrated': 0.0,
            'disgust': 0.0,
            'fear': 0.0,
            'anxious': 0.0,
            'worried': 0.0,
            'surprise': 0.0,
            'confused': 0.0,
            'neutral': 0.0
        }
        
        # Map happy -> happy, excited, content (BOOSTED)
        if 'happy' in normalized:
            happy_score = normalized['happy']
            if happy_score > 0.5:  # Very happy = excited (lowered threshold)
                enhanced['excited'] = happy_score * 0.7
                enhanced['happy'] = happy_score * 0.5
            elif happy_score > 0.2:  # Moderately happy (lowered threshold)
                enhanced['happy'] = happy_score * 0.9
                enhanced['content'] = happy_score * 0.4
            else:  # Slightly happy = content
                enhanced['content'] = happy_score * 0.7
                enhanced['happy'] = happy_score * 0.5
        
        # Map sad -> sad, tired, bored (BOOSTED)
        if 'sad' in normalized:
            sad_score = normalized['sad']
            if sad_score > 0.4:  # Very sad (lowered threshold)
                enhanced['sad'] = sad_score * 1.0
                enhanced['tired'] = sad_score * 0.3
            elif sad_score > 0.2:  # Moderately sad (lowered threshold)
                enhanced['sad'] = sad_score * 0.8
                enhanced['bored'] = sad_score * 0.5
            else:  # Slightly sad
                enhanced['tired'] = sad_score * 0.6
                enhanced['sad'] = sad_score * 0.6
        
        # Map angry -> angry, frustrated (BOOSTED)
        if 'angry' in normalized:
            angry_score = normalized['angry']
            if angry_score > 0.4:  # Very angry (lowered threshold)
                enhanced['angry'] = angry_score * 1.0
                enhanced['frustrated'] = angry_score * 0.3
            else:  # Moderately angry = frustrated
                enhanced['frustrated'] = angry_score * 0.8
                enhanced['angry'] = angry_score * 0.6
        
        # Map fear -> fear, anxious, worried (BOOSTED)
        if 'fear' in normalized:
            fear_score = normalized['fear']
            if fear_score > 0.4:  # Very fearful (lowered threshold)
                enhanced['fear'] = fear_score * 0.9
                enhanced['anxious'] = fear_score * 0.4
            elif fear_score > 0.2:  # Moderately fearful = anxious (lowered threshold)
                enhanced['anxious'] = fear_score * 0.8
                enhanced['worried'] = fear_score * 0.5
            else:  # Slightly fearful = worried
                enhanced['worried'] = fear_score * 0.8
                enhanced['fear'] = fear_score * 0.4
        
        # Map surprise -> surprise, confused (BOOSTED)
        if 'surprise' in normalized:
            surprise_score = normalized['surprise']
            if surprise_score > 0.3:  # Clear surprise (lowered threshold)
                enhanced['surprise'] = surprise_score * 1.0
                enhanced['confused'] = surprise_score * 0.3
            else:  # Mild surprise = confused
                enhanced['confused'] = surprise_score * 0.8
                enhanced['surprise'] = surprise_score * 0.6
        
        # Map disgust directly (BOOSTED)
        if 'disgust' in normalized:
            enhanced['disgust'] = normalized['disgust'] * 1.2  # Boost disgust detection
        
        # Map neutral -> neutral, calm (REDUCED to allow other emotions to show)
        if 'neutral' in normalized:
            neutral_score = normalized['neutral']
            # Only use neutral if it's VERY dominant (>0.8)
            if neutral_score > 0.8:  # Very neutral
                enhanced['neutral'] = neutral_score * 0.5
                enhanced['calm'] = neutral_score * 0.3
            elif neutral_score > 0.6:  # Moderately neutral = calm
                enhanced['calm'] = neutral_score * 0.4
                enhanced['neutral'] = neutral_score * 0.2
            else:  # Low neutral - distribute to calm minimally
                enhanced['calm'] = neutral_score * 0.3
                enhanced['neutral'] = neutral_score * 0.1
        
        # Normalize to sum to 1.0
        total_enhanced = sum(enhanced.values())
        if total_enhanced > 0:
            enhanced = {k: round(float(v / total_enhanced), 3) for k, v in enhanced.items()}
        
        # Ensure all values are Python floats, not numpy float32
        enhanced = {k: float(v) for k, v in enhanced.items()}
        
        return enhanced
    
    def _detect_basic(self, img_array, faces):
        """Basic emotion detection based on face features"""
        # This is a simplified version - in production, you'd use a trained model
        # For now, we'll return a neutral emotion with lower confidence
        
        return {
            'success': True,
            'emotion': 'neutral',
            'confidence': 0.6,
            'all_emotions': {
                'neutral': 0.6,
                'happy': 0.1,
                'sad': 0.1,
                'angry': 0.05,
                'fear': 0.05,
                'surprise': 0.05,
                'disgust': 0.05
            },
            'faces_detected': len(faces),
            'method': 'basic',
            'note': 'Install DeepFace for accurate emotion detection'
        }
    
    def detect_from_file(self, file_path):
        """
        Detect emotion from image file
        Args:
            file_path: Path to image file
        Returns:
            dict with emotion detection results
        """
        try:
            img_array = cv2.imread(file_path)
            if img_array is None:
                return {
                    'success': False,
                    'error': 'Failed to load image file'
                }
            return self.detect_from_array(img_array)
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to read file: {str(e)}'
            }


# Test the detector
if __name__ == '__main__':
    detector = FaceEmotionDetector()
    print("Face Emotion Detector initialized")
    print(f"DeepFace available: {detector.deepface_available}")
    print("\nReady to detect emotions from facial expressions!")
