"""
Author Model
Represents research authors in the system
"""

from datetime import datetime
from models import db


class Author(db.Model):
    """
    Author model representing research authors
    One author can have many papers
    """
    
    __tablename__ = 'authors'
    
    # Primary key
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Author information
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    university = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship: One author has many papers
    papers = db.relationship('Paper', backref='author', lazy='dynamic',
                            cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of Author"""
        return f'<Author {self.name}>'
    
    def to_dict(self):
        """Convert author to dictionary for JSON serialization"""
        return {
            'author_id': self.author_id,
            'name': self.name,
            'email': self.email,
            'university': self.university,
            'country': self.country,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paper_count': self.papers.count()
        }
    
    @property
    def paper_count(self):
        """Get the number of papers for this author"""
        return self.papers.count()
