"""
Models package initialization
Imports all models for easy access
Creates a shared SQLAlchemy instance
"""

from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy instance - must be initialized once
db = SQLAlchemy()

from .author import Author
from .paper import Paper, PaperTopic
from .topic import Topic
from .user import User

__all__ = ['db', 'Author', 'Paper', 'PaperTopic', 'Topic', 'User']
