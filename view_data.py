"""
View all data stored in the emotion detection database
"""
from database import EmotionDatabase
import json
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("AI EMOTION DETECTION - DATABASE VIEWER")
print("=" * 70)

# Initialize database
db = EmotionDatabase()

# Get database info
print("\n[DATABASE INFORMATION]")
print("-" * 70)
info = db.get_database_info()
print(f"Database Path: {info['database_path']}")
print(f"Total Records: {info['total_records']}")
print(f"Database Size: {info['size_mb']} MB ({info['size_bytes']} bytes)")

# Get statistics
print("\n[STATISTICS]")
print("-" * 70)
stats = db.get_statistics()
print(f"Total Detections: {stats['total_detections']}")

print("\n[Emotion Breakdown]")
for emotion, count in sorted(stats['emotion_counts'].items(), key=lambda x: x[1], reverse=True):
    percentage = (count / stats['total_detections'] * 100) if stats['total_detections'] > 0 else 0
    print(f"  {emotion:15s}: {count:3d} ({percentage:5.1f}%)")

print("\n[Detection Types]")
for dtype, count in stats['type_counts'].items():
    print(f"  {dtype:10s}: {count}")

if stats['avg_confidence']:
    print("\n[Average Confidence by Emotion]")
    for emotion, conf in sorted(stats['avg_confidence'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {emotion:15s}: {conf:.1%}")

if stats['daily_activity']:
    print("\n[Daily Activity - Last 7 Days]")
    for date, count in sorted(stats['daily_activity'].items(), reverse=True):
        print(f"  {date}: {count} detections")

# Get recent history
print("\n[RECENT HISTORY - Last 20]")
print("-" * 70)
history = db.get_recent_history(20)

if not history:
    print("No records found in database.")
else:
    for i, entry in enumerate(history, 1):
        text_preview = entry.get('text', 'N/A')
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        
        print(f"\n{i}. ID: {entry['id']}")
        print(f"   Type: {entry['type']}")
        print(f"   Emotion: {entry['emotion']} ({entry['confidence']:.1%} confidence)")
        print(f"   Text: {text_preview}")
        print(f"   Time: {entry['timestamp']}")
        
        if entry.get('faces_detected'):
            print(f"   Faces: {entry['faces_detected']}")
        if entry.get('method'):
            print(f"   Method: {entry['method']}")

print("\n" + "=" * 70)
print(f"Showing {len(history)} of {stats['total_detections']} total records")
print("=" * 70)
