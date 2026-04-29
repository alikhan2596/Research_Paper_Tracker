"""
Script to add sample topics to the database
Run this before adding papers
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models.topic import Topic

def add_sample_topics():
    """Add sample topics to the database"""
    
    with app.app_context():
        topics_data = [
            'Machine Learning',
            'Deep Learning',
            'Natural Language Processing',
            'Computer Vision',
            'Data Mining',
            'Artificial Intelligence',
            'Neural Networks',
            'Big Data Analytics'
        ]
        
        added_count = 0
        for topic_name in topics_data:
            # Check if topic already exists
            existing = Topic.query.filter_by(topic_name=topic_name).first()
            if existing:
                print(f"  - Topic '{topic_name}' already exists, skipping")
                continue
            
            topic = Topic(topic_name=topic_name)
            db.session.add(topic)
            added_count += 1
            print(f"  - Added: {topic_name}")
        
        try:
            db.session.commit()
            print(f"\n✓ Successfully added {added_count} topics to the database")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error adding topics: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Sample Topics to Database")
    print("=" * 60)
    add_sample_topics()
