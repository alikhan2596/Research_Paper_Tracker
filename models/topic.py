"""
Topic Model
Represents research topics/categories in the system
"""

from models import db


class Topic(db.Model):
    """
    Topic model representing research topics/categories
    One topic can be associated with many papers (many-to-many)
    """
    
    __tablename__ = 'topics'
    
    # Primary key
    topic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Topic information
    topic_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    def __repr__(self):
        """String representation of Topic"""
        return f'<Topic {self.topic_name}>'
    
    def to_dict(self):
        """Convert topic to dictionary for JSON serialization"""
        return {
            'topic_id': self.topic_id,
            'topic_name': self.topic_name,
            'paper_count': self.papers.count()
        }
    
    @property
    def paper_count(self):
        """Get the number of papers for this topic"""
        return self.papers.count()
