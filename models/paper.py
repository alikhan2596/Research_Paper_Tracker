"""
Paper Model
Represents research papers in the system
"""

from datetime import datetime
from models import db


class Paper(db.Model):
    """
    Paper model representing research papers
    One paper belongs to one author and can have many topics
    """
    
    __tablename__ = 'papers'
    
    # Primary key
    paper_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Paper information
    title = db.Column(db.String(255), nullable=False, index=True)
    abstract = db.Column(db.Text, nullable=True)
    journal_name = db.Column(db.String(150), nullable=False)
    publication_date = db.Column(db.Date, nullable=False, index=True)
    citations = db.Column(db.Integer, default=0, nullable=False)
    
    # Status: Published, Under Review, Draft
    status = db.Column(db.String(20), nullable=False, default='Draft', index=True)
    
    # Foreign key to Author
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), 
                         nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship: One paper can have many topics (many-to-many)
    topics = db.relationship('Topic', secondary='paper_topics',
                           backref=db.backref('papers', lazy='dynamic'),
                           lazy='dynamic')
    
    def __repr__(self):
        """String representation of Paper"""
        return f'<Paper {self.title}>'
    
    def to_dict(self):
        """Convert paper to dictionary for JSON serialization"""
        return {
            'paper_id': self.paper_id,
            'title': self.title,
            'abstract': self.abstract,
            'journal_name': self.journal_name,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'citations': self.citations,
            'status': self.status,
            'author_id': self.author_id,
            'author_name': self.author.name if self.author else None,
            'topics': [topic.topic_name for topic in self.topics],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @property
    def topic_count(self):
        """Get the number of topics for this paper"""
        return self.topics.count()


class PaperTopic(db.Model):
    """
    Association table for many-to-many relationship between Papers and Topics
    """
    
    __tablename__ = 'paper_topics'
    
    # Foreign keys
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.paper_id'), 
                        primary_key=True, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'), 
                        primary_key=True, nullable=False)
    
    def __repr__(self):
        """String representation of PaperTopic"""
        return f'<PaperTopic paper_id={self.paper_id} topic_id={self.topic_id}>'
