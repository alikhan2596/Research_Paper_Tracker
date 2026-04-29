"""
Script to add sample authors to the database
Run this after adding topics and before adding papers
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models.author import Author

def add_sample_authors():
    """Add sample authors to the database"""
    
    with app.app_context():
        authors_data = [
            {
                'name': 'Dr. Sarah Chen',
                'email': 'sarah.chen@mit.edu',
                'university': 'Massachusetts Institute of Technology',
                'country': 'USA'
            },
            {
                'name': 'Prof. James Wilson',
                'email': 'j.wilson@stanford.edu',
                'university': 'Stanford University',
                'country': 'USA'
            },
            {
                'name': 'Dr. Maria Garcia',
                'email': 'm.garcia@ox.ac.uk',
                'university': 'University of Oxford',
                'country': 'UK'
            },
            {
                'name': 'Prof. Ahmed Hassan',
                'email': 'ahassan@kaust.edu.sa',
                'university': 'King Abdullah University of Science and Technology',
                'country': 'Saudi Arabia'
            },
            {
                'name': 'Dr. Yuki Tanaka',
                'email': 'tanaka@tokyo.ac.jp',
                'university': 'University of Tokyo',
                'country': 'Japan'
            },
            {
                'name': 'Prof. Emily Brown',
                'email': 'e.brown@cam.ac.uk',
                'university': 'University of Cambridge',
                'country': 'UK'
            },
            {
                'name': 'Dr. Michael Lee',
                'email': 'mlee@ethz.ch',
                'university': 'ETH Zurich',
                'country': 'Switzerland'
            },
            {
                'name': 'Prof. Anna Mueller',
                'email': 'mueller@tum.de',
                'university': 'Technical University of Munich',
                'country': 'Germany'
            },
            {
                'name': 'Dr. Raj Patel',
                'email': 'rpatel@iitb.ac.in',
                'university': 'Indian Institute of Technology Bombay',
                'country': 'India'
            },
            {
                'name': 'Prof. Liu Wei',
                'email': 'liuwei@tsinghua.edu.cn',
                'university': 'Tsinghua University',
                'country': 'China'
            }
        ]
        
        added_count = 0
        for author_data in authors_data:
            # Check if author already exists
            existing = Author.query.filter_by(email=author_data['email']).first()
            if existing:
                print(f"  - Author '{author_data['name']}' already exists, skipping")
                continue
            
            author = Author(**author_data)
            db.session.add(author)
            added_count += 1
            print(f"  - Added: {author_data['name']}")
        
        try:
            db.session.commit()
            print(f"\n✓ Successfully added {added_count} authors to the database")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error adding authors: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Sample Authors to Database")
    print("=" * 60)
    add_sample_authors()
