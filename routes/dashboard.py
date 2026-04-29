"""
Dashboard Routes
Handles the main dashboard page with statistics and charts
"""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from models.paper import Paper, db
from models.author import Author
from models.topic import Topic
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard_bp.route('/')
@login_required
def dashboard():
    """
    Main dashboard page
    Displays summary statistics and charts
    """
    # Get summary statistics
    total_papers = Paper.query.count()
    total_authors = Author.query.count()
    total_citations = db.session.query(func.sum(Paper.citations)).scalar() or 0
    total_topics = Topic.query.count()
    
    # Get top 5 authors by number of papers
    top_authors = db.session.query(
        Author.name,
        func.count(Paper.paper_id).label('paper_count')
    ).join(Paper, Author.author_id == Paper.author_id)\
     .group_by(Author.author_id, Author.name)\
     .order_by(func.count(Paper.paper_id).desc())\
     .limit(5)\
     .all()
    
    # Get papers published per year (all years)
    yearly_papers = db.session.query(
        extract('year', Paper.publication_date).label('year'),
        func.count(Paper.paper_id).label('count')
    ).group_by(extract('year', Paper.publication_date))\
     .order_by(extract('year', Paper.publication_date))\
     .all()
    
    # Get papers by status
    status_counts = db.session.query(
        Paper.status,
        func.count(Paper.paper_id).label('count')
    ).group_by(Paper.status).all()
    
    # Get recent 5 papers
    recent_papers = Paper.query.order_by(Paper.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_papers=total_papers,
                         total_authors=total_authors,
                         total_citations=total_citations,
                         total_topics=total_topics,
                         top_authors=top_authors,
                         yearly_papers=yearly_papers,
                         status_counts=status_counts,
                         recent_papers=recent_papers,
                         is_admin=current_user.is_admin())


@dashboard_bp.route('/health')
def health():
    """
    Health check endpoint
    Returns JSON status of application and database connectivity
    """
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    }), 200
