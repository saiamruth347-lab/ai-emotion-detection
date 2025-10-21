"""
Test script to verify DeepFace is working correctly
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Testing DeepFace Installation")
print("=" * 60)

# Test 1: Import DeepFace
print("\n1. Testing DeepFace import...")
try:
    from deepface import DeepFace
    print("   [OK] DeepFace imported successfully")
except ImportError as e:
    print(f"   [ERROR] Failed to import DeepFace: {e}")
    print("   [TIP] Install with: pip install deepface")
    exit(1)

# Test 2: Check TensorFlow
print("\n2. Testing TensorFlow...")
try:
    import tensorflow as tf
    print(f"   [OK] TensorFlow version: {tf.__version__}")
except ImportError as e:
    print(f"   [ERROR] TensorFlow not found: {e}")

# Test 3: Check OpenCV
print("\n3. Testing OpenCV...")
try:
    import cv2
    print(f"   [OK] OpenCV version: {cv2.__version__}")
except ImportError as e:
    print(f"   [ERROR] OpenCV not found: {e}")

# Test 4: Test emotion detection on a sample
print("\n4. Testing emotion detection...")
try:
    import numpy as np
    
    # Create a simple test image (black image)
    test_image = np.zeros((224, 224, 3), dtype=np.uint8)
    
    print("   [INFO] Analyzing test image...")
    result = DeepFace.analyze(
        test_image,
        actions=['emotion'],
        enforce_detection=False,
        silent=True
    )
    
    if isinstance(result, list):
        result = result[0]
    
    print(f"   [OK] Emotion detection working!")
    print(f"   [RESULT] Detected emotions: {result['emotion']}")
    print(f"   [RESULT] Dominant: {result['dominant_emotion']}")
    
except Exception as e:
    print(f"   [ERROR] Error during detection: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
