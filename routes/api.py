"""
API Routes
REST API endpoints for JSON data access
"""

from flask import Blueprint, jsonify
from models.paper import Paper, db
from models.author import Author
from models.topic import Topic
from sqlalchemy import func

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/papers', methods=['GET'])
def get_papers():
    """
    GET /api/papers
    Returns all papers as JSON
    """
    papers = Paper.query.join(Author).all()
    return jsonify({
        'status': 'success',
        'count': len(papers),
        'data': [paper.to_dict() for paper in papers]
    }), 200


@api_bp.route('/papers/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    """
    GET /api/papers/<id>
    Returns a single paper as JSON
    """
    paper = Paper.query.get_or_404(paper_id)
    return jsonify({
        'status': 'success',
        'data': paper.to_dict()
    }), 200


@api_bp.route('/authors', methods=['GET'])
def get_authors():
    """
    GET /api/authors
    Returns all authors as JSON
    """
    authors = Author.query.all()
    return jsonify({
        'status': 'success',
        'count': len(authors),
        'data': [author.to_dict() for author in authors]
    }), 200


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    GET /api/stats
    Returns dashboard statistics as JSON
    """
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
    
    # Get papers by status
    status_counts = db.session.query(
        Paper.status,
        func.count(Paper.paper_id).label('count')
    ).group_by(Paper.status).all()
    
    return jsonify({
        'status': 'success',
        'data': {
            'total_papers': total_papers,
            'total_authors': total_authors,
            'total_citations': total_citations,
            'total_topics': total_topics,
            'top_authors': [{'name': a[0], 'paper_count': a[1]} for a in top_authors],
            'status_distribution': [{'status': s[0], 'count': s[1]} for s in status_counts]
        }
    }), 200
