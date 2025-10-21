"""
Simple test to verify face emotion detector works
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Testing Face Emotion Detector...")
print("=" * 60)

from face_emotion_detector import FaceEmotionDetector
import numpy as np
import cv2

# Create detector
print("\n1. Creating detector...")
detector = FaceEmotionDetector()
print(f"   DeepFace available: {detector.deepface_available}")

# Create a simple test image (black with a white rectangle for "face")
print("\n2. Creating test image...")
test_image = np.zeros((480, 640, 3), dtype=np.uint8)
# Draw a simple face-like rectangle
cv2.rectangle(test_image, (200, 150), (440, 330), (255, 255, 255), -1)

print(f"   Image shape: {test_image.shape}")
print(f"   Image dtype: {test_image.dtype}")

# Test detection
print("\n3. Testing detection...")
try:
    result = detector.detect_from_array(test_image)
    print(f"   Success: {result.get('success', False)}")
    
    if result.get('success'):
        print(f"   Emotion: {result.get('emotion')}")
        print(f"   Confidence: {result.get('confidence')}")
        print(f"   Method: {result.get('method')}")
        print(f"   Faces detected: {result.get('faces_detected')}")
    else:
        print(f"   Error: {result.get('error')}")
        
except Exception as e:
    print(f"   EXCEPTION: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test complete!")
