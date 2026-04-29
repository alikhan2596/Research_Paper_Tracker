"""
User Model
Represents application users for authentication
"""

from datetime import datetime
from flask_login import UserMixin
from models import db


class User(UserMixin, db.Model):
    """
    User model for authentication and authorization
    Users have roles: 'admin' or 'viewer'
    """
    
    __tablename__ = 'users'
    
    # Primary key
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User information
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role: 'admin' or 'viewer'
    role = db.Column(db.String(20), nullable=False, default='viewer')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Flask-Login requires an 'id' attribute
    @property
    def id(self):
        """Return user_id as id for Flask-Login compatibility"""
        return self.user_id
    
    def __repr__(self):
        """String representation of User"""
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'
    
    def is_viewer(self):
        """Check if user has viewer role"""
        return self.role == 'viewer'
