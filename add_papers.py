"""
Script to add sample papers to the database
Run this after the app is running and database is connected
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models.paper import Paper
from models.author import Author
from models.topic import Topic

def add_sample_papers():
    """Add 8-10 sample papers to the database"""
    
    with app.app_context():
        # Check if we have authors and topics
        authors = Author.query.all()
        topics = Topic.query.all()
        
        if not authors:
            print("No authors found. Please add authors first.")
            return
        
        if not topics:
            print("No topics found. Please add topics first.")
            return
        
        print(f"Found {len(authors)} authors and {len(topics)} topics")
        
        # Sample papers data
        papers_data = [
            {
                'title': 'Attention Is All You Need: Transformer Networks for NLP',
                'abstract': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.',
                'journal_name': 'NeurIPS',
                'publication_date': datetime(2017, 12, 4),
                'citations': 89000,
                'status': 'Published',
                'author': authors[0] if len(authors) > 0 else None,
                'topics': [topics[2], topics[6]] if len(topics) > 6 else [topics[0]]
            },
            {
                'title': 'Deep Residual Learning for Image Recognition',
                'abstract': 'Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously.',
                'journal_name': 'CVPR',
                'publication_date': datetime(2016, 6, 27),
                'citations': 165000,
                'status': 'Published',
                'author': authors[1] if len(authors) > 1 else authors[0],
                'topics': [topics[1], topics[3], topics[6]] if len(topics) > 6 else [topics[0]]
            },
            {
                'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
                'abstract': 'We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers.',
                'journal_name': 'NAACL',
                'publication_date': datetime(2019, 6, 2),
                'citations': 72000,
                'status': 'Published',
                'author': authors[0] if len(authors) > 0 else None,
                'topics': [topics[2], topics[6]] if len(topics) > 6 else [topics[0]]
            },
            {
                'title': 'Generative Adversarial Networks',
                'abstract': 'We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models.',
                'journal_name': 'NeurIPS',
                'publication_date': datetime(2014, 12, 8),
                'citations': 69000,
                'status': 'Published',
                'author': authors[2] if len(authors) > 2 else authors[0],
                'topics': [topics[0], topics[1], topics[5]] if len(topics) > 5 else [topics[0]]
            },
            {
                'title': 'YOLO: Real-Time Object Detection',
                'abstract': 'We present YOLO, a new approach to object detection. Prior work on object detection repurposes classifiers to perform detection.',
                'journal_name': 'CVPR',
                'publication_date': datetime(2016, 6, 27),
                'citations': 45000,
                'status': 'Published',
                'author': authors[1] if len(authors) > 1 else authors[0],
                'topics': [topics[3], topics[5]] if len(topics) > 5 else [topics[0]]
            },
            {
                'title': 'Word2Vec: Efficient Estimation of Word Representations',
                'abstract': 'We propose two novel model architectures for computing continuous vector representations of words from very large data sets.',
                'journal_name': 'ICLR',
                'publication_date': datetime(2013, 4, 17),
                'citations': 58000,
                'status': 'Published',
                'author': authors[4] if len(authors) > 4 else authors[0],
                'topics': [topics[2], topics[0]] if len(topics) > 2 else [topics[0]]
            },
            {
                'title': 'Long Short-Term Memory Networks',
                'abstract': 'Recurrent neural networks are powerful sequence learners. Long Short-Term Memory (LSTM) is a recurrent neural network architecture that has been designed to address the vanishing gradient problem.',
                'journal_name': 'Neural Computation',
                'publication_date': datetime(1997, 11, 15),
                'citations': 52000,
                'status': 'Published',
                'author': authors[5] if len(authors) > 5 else authors[0],
                'topics': [topics[6], topics[0]] if len(topics) > 6 else [topics[0]]
            },
            {
                'title': 'Random Forests',
                'abstract': 'Random forests are a combination of tree predictors such that each tree depends on the values of a random vector sampled independently.',
                'journal_name': 'Machine Learning',
                'publication_date': datetime(2001, 1, 1),
                'citations': 89000,
                'status': 'Published',
                'author': authors[6] if len(authors) > 6 else authors[0],
                'topics': [topics[0], topics[4]] if len(topics) > 4 else [topics[0]]
            },
            {
                'title': 'Support Vector Machines',
                'abstract': 'The support-vector network is a learning machine for two-group classification problems. The machine conceptually implements a learning method based on statistical learning theory.',
                'journal_name': 'Machine Learning',
                'publication_date': datetime(1995, 9, 1),
                'citations': 78000,
                'status': 'Published',
                'author': authors[7] if len(authors) > 7 else authors[0],
                'topics': [topics[0], topics[5]] if len(topics) > 5 else [topics[0]]
            },
            {
                'title': 'K-Means Clustering Algorithm',
                'abstract': 'The k-means algorithm is a simple iterative method to partition a given dataset into a user specified number of clusters, k, based on some similarity/dissimilarity metric.',
                'journal_name': 'IEEE Transactions on Pattern Analysis',
                'publication_date': datetime(1967, 6, 1),
                'citations': 65000,
                'status': 'Published',
                'author': authors[8] if len(authors) > 8 else authors[0],
                'topics': [topics[4], topics[7]] if len(topics) > 7 else [topics[0]]
            }
        ]
        
        # Add papers
        added_count = 0
        for paper_data in papers_data:
            # Check if paper already exists
            existing = Paper.query.filter_by(title=paper_data['title']).first()
            if existing:
                print(f"  - Paper '{paper_data['title']}' already exists, skipping")
                continue
            
            author = paper_data.pop('author')
            paper_topics = paper_data.pop('topics')
            
            paper = Paper(**paper_data, author_id=author.author_id if author else None)
            
            # Add topics
            for topic in paper_topics:
                paper.topics.append(topic)
            
            db.session.add(paper)
            added_count += 1
            print(f"  - Added: {paper_data['title']}")
        
        try:
            db.session.commit()
            print(f"\n✓ Successfully added {added_count} papers to the database")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error adding papers: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Sample Papers to Database")
    print("=" * 60)
    add_sample_papers()
