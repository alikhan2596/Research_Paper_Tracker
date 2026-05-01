"""
Research Paper Tracker - Main Application
A full-stack Flask application for managing academic papers, authors, and topics
Connected to Azure SQL Database
"""

from flask import Flask, render_template
from flask_login import LoginManager
from config import config
import os

# Import models and database
from models import db, Author, Paper, PaperTopic, Topic, User

# Import route blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.papers import papers_bp
from routes.authors import authors_bp
from routes.topics import topics_bp
from routes.api import api_bp


def create_app(config_name='default'):
    """
    Application factory function
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize database with engine options
    db.init_app(app)
    
    # Configure engine options if specified
    if hasattr(app.config, 'get') and app.config.get('SQLALCHEMY_ENGINE_OPTIONS'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = app.config['SQLALCHEMY_ENGINE_OPTIONS']
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'error'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login"""
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(papers_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(topics_bp)
    app.register_blueprint(api_bp)
    
    # Create database tables and seed data on first run
    with app.app_context():
        initialize_database()
    
    return app


def initialize_database():
    """
    Initialize database tables and seed with sample data
    Only runs if tables are empty
    """
    try:
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Check if database is empty (seed only if users table is empty)
        if User.query.count() == 0:
            print("Database is empty. Seeding temporarily disabled due to function issues.")
            print("Please manually seed the database or fix the seed_database function.")
            # seed_database()  # Temporarily disabled
            # print("✓ Database seeded successfully")
        else:
            print("Database already contains data. Skipping seed.")
            
    except Exception as e:
        print(f"✗ Error initializing database: {str(e)}")
        # Don't raise - allow app to start even if seeding fails


def seed_database():
    """
    Seed database with realistic sample data
    Creates 10 authors, 15 papers, 8 topics, and 1 admin user
    """
    from datetime import datetime, timedelta
    from werkzeug.security import generate_password_hash
    
    try:
        # Create topics (only if table is empty)
        if Topic.query.count() == 0:
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
            
            topics = []
            for topic_name in topics_data:
                topic = Topic(topic_name=topic_name)
                db.session.add(topic)
                topics.append(topic)
            
            db.session.commit()
            print(f"  - Created {len(topics)} topics")
        else:
            print("  - Topics already exist, skipping")
        
        # Refresh topics to get their IDs
        topics = Topic.query.all()
        
        # Create authors (only if table is empty)
        if Author.query.count() == 0:
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
            
            authors = []
            for author_data in authors_data:
                author = Author(**author_data)
                db.session.add(author)
                authors.append(author)
            
            db.session.commit()
            print(f"  - Created {len(authors)} authors")
        else:
            print("  - Authors already exist, skipping")
        
        # Refresh authors to get their IDs
        authors = Author.query.all()
        
        # Create papers (only if table is empty)
        if Paper.query.count() == 0:
            papers_data = [
                {
                    'title': 'Attention Is All You Need: Transformer Networks for NLP',
                    'abstract': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.',
                    'journal_name': 'NeurIPS',
                    'publication_date': datetime(2017, 12, 4),
                    'citations': 89000,
                    'status': 'Published',
                    'author_index': 0,
                    'topic_indices': [2, 6]
                },
                {
                    'title': 'Deep Residual Learning for Image Recognition',
                    'abstract': 'Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously.',
                    'journal_name': 'CVPR',
                    'publication_date': datetime(2016, 6, 27),
                    'citations': 165000,
                    'status': 'Published',
                    'author_index': 1,
                    'topic_indices': [1, 3, 6]
                },
                {
                    'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
                    'abstract': 'We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers.',
                    'journal_name': 'NAACL',
                    'publication_date': datetime(2019, 6, 2),
                    'citations': 72000,
                    'status': 'Published',
                    'author_index': 0,
                    'topic_indices': [2, 6]
                },
                {
                    'title': 'Generative Adversarial Networks',
                    'abstract': 'We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models.',
                    'journal_name': 'NeurIPS',
                    'publication_date': datetime(2014, 12, 8),
                    'citations': 69000,
                    'status': 'Published',
                    'author_index': 2,
                    'topic_indices': [0, 1, 5]
                },
                {
                    'title': 'YOLO: Real-Time Object Detection',
                    'abstract': 'We present YOLO, a new approach to object detection. Prior work on object detection repurposes classifiers to perform detection.',
                    'journal_name': 'CVPR',
                    'publication_date': datetime(2016, 6, 27),
                    'citations': 45000,
                    'status': 'Published',
                    'author_index': 1,
                    'topic_indices': [3, 5]
                },
                {
                    'title': 'Word2Vec: Efficient Estimation of Word Representations',
                    'abstract': 'We propose two novel model architectures for computing continuous vector representations of words from very large data sets.',
                    'journal_name': 'ICLR',
                    'publication_date': datetime(2013, 4, 17),
                    'citations': 58000,
                    'status': 'Published',
                    'author_index': 4,
                    'topic_indices': [2, 0]
                },
                {
                    'title': 'Long Short-Term Memory Networks',
                    'abstract': 'Recurrent neural networks are powerful sequence learners. Long Short-Term Memory (LSTM) is a recurrent neural network architecture that has been designed to address the vanishing gradient problem.',
                    'journal_name': 'Neural Computation',
                    'publication_date': datetime(1997, 11, 15),
                    'citations': 52000,
                    'status': 'Published',
                    'author_index': 5,
                    'topic_indices': [6, 0]
                },
                {
                    'title': 'Random Forests',
                    'abstract': 'Random forests are a combination of tree predictors such that each tree depends on the values of a random vector sampled independently.',
                    'journal_name': 'Machine Learning',
                    'publication_date': datetime(2001, 1, 1),
                    'citations': 89000,
                    'status': 'Published',
                    'author_index': 6,
                    'topic_indices': [0, 4]
                },
                {
                    'title': 'Support Vector Machines',
                    'abstract': 'The support-vector network is a learning machine for two-group classification problems. The machine conceptually implements a learning method based on statistical learning theory.',
                    'journal_name': 'Machine Learning',
                    'publication_date': datetime(1995, 9, 1),
                    'citations': 78000,
                    'status': 'Published',
                    'author_index': 7,
                    'topic_indices': [0, 5]
                },
                {
                    'title': 'K-Means Clustering Algorithm',
                    'abstract': 'The k-means algorithm is a simple iterative method to partition a given dataset into a user specified number of clusters, k, based on some similarity/dissimilarity metric.',
                    'journal_name': 'IEEE Transactions on Pattern Analysis',
                    'publication_date': datetime(1967, 6, 1),
                    'citations': 65000,
                    'status': 'Published',
                    'author_index': 8,
                    'topic_indices': [4, 7]
                },
                {
                    'title': 'Neural Style Transfer',
                    'abstract': 'We introduce a new algorithm that can transfer the artistic style from one image onto another while preserving the content of the original image.',
                    'journal_name': 'CVPR',
                    'publication_date': datetime(2016, 6, 27),
                    'citations': 32000,
                    'status': 'Published',
                    'author_index': 9,
                    'topic_indices': [1, 3, 5]
                },
                {
                    'title': 'Gradient Boosting Decision Trees',
                    'abstract': 'Gradient boosting is a machine learning technique for regression and classification problems, which produces a prediction model in the form of an ensemble of weak prediction models.',
                    'journal_name': 'ICML',
                    'publication_date': datetime(2001, 7, 1),
                    'citations': 41000,
                    'status': 'Published',
                    'author_index': 6,
                    'topic_indices': [0, 4]
                },
                {
                    'title': 'Graph Neural Networks for Social Network Analysis',
                    'abstract': 'This paper explores the application of graph neural networks to analyze social network structures and predict user behavior patterns.',
                    'journal_name': 'WWW',
                    'publication_date': datetime(2023, 5, 1),
                    'citations': 150,
                    'status': 'Under Review',
                    'author_index': 3,
                    'topic_indices': [0, 7]
                },
                {
                    'title': 'Federated Learning for Privacy-Preserving AI',
                    'abstract': 'We propose a federated learning framework that enables collaborative model training while preserving data privacy across multiple institutions.',
                    'journal_name': 'Nature Machine Intelligence',
                    'publication_date': datetime(2024, 1, 15),
                    'citations': 45,
                    'status': 'Under Review',
                    'author_index': 8,
                    'topic_indices': [0, 5]
                },
                {
                    'title': 'Self-Supervised Learning for Medical Image Analysis',
                    'abstract': 'This research investigates self-supervised learning techniques for medical image classification when labeled data is scarce.',
                    'journal_name': 'Medical Image Analysis',
                    'publication_date': datetime(2024, 3, 20),
                    'citations': 12,
                    'status': 'Draft',
                    'author_index': 4,
                    'topic_indices': [1, 3]
                }
            ]
            
            papers = []
            for paper_data in papers_data:
                author = authors[paper_data['author_index']]
                topic_indices = paper_data.pop('topic_indices')
                paper_data.pop('author_index')  # Remove helper field
                
                paper = Paper(
                    **paper_data,
                    author_id=author.author_id
                )
                
                # Add topics to paper
                for topic_idx in topic_indices:
                    if topic_idx < len(topics):
                        paper.topics.append(topics[topic_idx])
                
                db.session.add(paper)
                papers.append(paper)
            
            db.session.commit()
            print(f"  - Created {len(papers)} papers")
        else:
            print("  - Papers already exist, skipping")
        
        # Create users (only if table is empty)
        if User.query.count() == 0:
            admin_user = User(
                username='admin',
                email='admin@researchtracker.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            
            # Create a regular viewer user
            viewer_user = User(
                username='viewer',
                email='viewer@researchtracker.com',
                password_hash=generate_password_hash('viewer123'),
                role='viewer'
            )
            db.session.add(viewer_user)
            
            db.session.commit()
            print("  - Created 2 users (admin and viewer)")
            print("\n  Login credentials:")
            print("  Admin: username='admin', password='admin123'")
            print("  Viewer: username='viewer', password='viewer123'")
        else:
            print("  - Users already exist, skipping")
    
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error seeding database: {str(e)}")
        raise


# Create application instance
app = create_app(os.getenv('FLASK_CONFIG', 'default'))


if __name__ == '__main__':
    print("=" * 60)
    print("Research Paper Tracker - Starting Application")
    print("=" * 60)
    print(f"Environment: {os.getenv('FLASK_CONFIG', 'default')}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
    print("=" * 60)
    
    # Run development server
    app.run(debug=True, host='0.0.0.0', port=5000)
