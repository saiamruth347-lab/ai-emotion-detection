"""
Database module for AI Emotion Detection
Uses SQLite to store emotion detection history
"""
import sqlite3
from datetime import datetime
import json
import os

class EmotionDatabase:
    """Handles all database operations for emotion detection"""
    
    def __init__(self, db_path='emotion_data.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create emotions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                emotion VARCHAR(50) NOT NULL,
                confidence REAL NOT NULL,
                all_emotions TEXT,
                sentiment_polarity REAL,
                sentiment_subjectivity REAL,
                detection_type VARCHAR(20) NOT NULL,
                faces_detected INTEGER,
                method VARCHAR(50),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_emotion 
            ON emotions(emotion)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON emotions(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_type 
            ON emotions(detection_type)
        ''')
        
        conn.commit()
        conn.close()
        print(f"[DATABASE] Initialized at {self.db_path}")
    
    def add_emotion(self, data):
        """
        Add emotion detection result to database
        Args:
            data: dict with emotion data
        Returns:
            int: ID of inserted record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO emotions (
                text, emotion, confidence, all_emotions,
                sentiment_polarity, sentiment_subjectivity,
                detection_type, faces_detected, method, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('text', ''),
            data['emotion'],
            data['confidence'],
            json.dumps(data.get('all_emotions', {})),
            data.get('sentiment_polarity'),
            data.get('sentiment_subjectivity'),
            data.get('type', 'text'),
            data.get('faces_detected'),
            data.get('method'),
            data.get('timestamp', datetime.now().isoformat())
        ))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"[DATABASE] Added emotion record #{record_id}: {data['emotion']}")
        return record_id
    
    def get_recent_history(self, limit=10):
        """
        Get recent emotion detection history
        Args:
            limit: Number of records to return
        Returns:
            list: Recent emotion records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, text, emotion, confidence, all_emotions,
                   sentiment_polarity, sentiment_subjectivity,
                   detection_type, faces_detected, method, timestamp
            FROM emotions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': row[0],
                'text': row[1],
                'emotion': row[2],
                'confidence': row[3],
                'all_emotions': json.loads(row[4]) if row[4] else {},
                'sentiment_polarity': row[5],
                'sentiment_subjectivity': row[6],
                'type': row[7],
                'faces_detected': row[8],
                'method': row[9],
                'timestamp': row[10]
            })
        
        return history
    
    def get_statistics(self):
        """
        Get emotion statistics
        Returns:
            dict: Statistics about emotions
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total detections
        cursor.execute('SELECT COUNT(*) FROM emotions')
        total = cursor.fetchone()[0]
        
        # Emotion counts
        cursor.execute('''
            SELECT emotion, COUNT(*) as count
            FROM emotions
            GROUP BY emotion
            ORDER BY count DESC
        ''')
        emotion_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Detection type counts
        cursor.execute('''
            SELECT detection_type, COUNT(*) as count
            FROM emotions
            GROUP BY detection_type
        ''')
        type_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Average confidence by emotion
        cursor.execute('''
            SELECT emotion, AVG(confidence) as avg_conf
            FROM emotions
            GROUP BY emotion
        ''')
        avg_confidence = {row[0]: round(row[1], 3) for row in cursor.fetchall()}
        
        # Recent activity (last 7 days)
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM emotions
            WHERE timestamp >= datetime('now', '-7 days')
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
        ''')
        daily_activity = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_detections': total,
            'emotion_counts': emotion_counts,
            'type_counts': type_counts,
            'avg_confidence': avg_confidence,
            'daily_activity': daily_activity
        }
    
    def search_by_emotion(self, emotion, limit=50):
        """
        Search records by emotion
        Args:
            emotion: Emotion to search for
            limit: Max records to return
        Returns:
            list: Matching records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, text, emotion, confidence, timestamp
            FROM emotions
            WHERE emotion = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (emotion, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'text': row[1],
            'emotion': row[2],
            'confidence': row[3],
            'timestamp': row[4]
        } for row in rows]
    
    def delete_old_records(self, days=30):
        """
        Delete records older than specified days
        Args:
            days: Number of days to keep
        Returns:
            int: Number of deleted records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM emotions
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"[DATABASE] Deleted {deleted} old records")
        return deleted
    
    def clear_all(self):
        """Clear all records from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM emotions')
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"[DATABASE] Cleared {deleted} records")
        return deleted
    
    def get_database_info(self):
        """Get database information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM emotions')
        total_records = cursor.fetchone()[0]
        
        # Database file size
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        db_size_mb = round(db_size / (1024 * 1024), 2)
        
        conn.close()
        
        return {
            'database_path': self.db_path,
            'total_records': total_records,
            'size_mb': db_size_mb,
            'size_bytes': db_size
        }


# Test the database
if __name__ == '__main__':
    print("Testing Emotion Database...")
    print("=" * 60)
    
    db = EmotionDatabase('test_emotions.db')
    
    # Test adding emotion
    print("\n1. Adding test emotion...")
    test_data = {
        'text': 'I am so happy today!',
        'emotion': 'happy',
        'confidence': 0.92,
        'all_emotions': {'happy': 0.92, 'sad': 0.05, 'neutral': 0.03},
        'sentiment_polarity': 0.8,
        'sentiment_subjectivity': 0.9,
        'type': 'text',
        'timestamp': datetime.now().isoformat()
    }
    record_id = db.add_emotion(test_data)
    print(f"   Added record #{record_id}")
    
    # Test getting history
    print("\n2. Getting history...")
    history = db.get_recent_history(5)
    print(f"   Found {len(history)} records")
    
    # Test statistics
    print("\n3. Getting statistics...")
    stats = db.get_statistics()
    print(f"   Total detections: {stats['total_detections']}")
    print(f"   Emotions: {stats['emotion_counts']}")
    
    # Test database info
    print("\n4. Database info...")
    info = db.get_database_info()
    print(f"   Path: {info['database_path']}")
    print(f"   Records: {info['total_records']}")
    print(f"   Size: {info['size_mb']} MB")
    
    print("\n" + "=" * 60)
    print("Database test complete!")
