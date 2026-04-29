"""
Routes package initialization
Imports all route modules for registration with Flask app
"""

from .auth import auth_bp
from .dashboard import dashboard_bp
from .papers import papers_bp
from .authors import authors_bp
from .topics import topics_bp
from .api import api_bp

__all__ = ['auth_bp', 'dashboard_bp', 'papers_bp', 'authors_bp', 'topics_bp', 'api_bp']
