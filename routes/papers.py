"""
Papers Routes
Handles papers management, CRUD operations, and filtering
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from models.paper import Paper, db
from models.author import Author
from models.topic import Topic
from datetime import datetime
import csv
from io import StringIO

papers_bp = Blueprint('papers', __name__, url_prefix='/papers')


@papers_bp.route('/')
@login_required
def papers():
    """
    Papers management page
    Displays paginated table of papers with search and filters
    """
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get search query
    search_query = request.args.get('search', '').strip()
    
    # Get filters
    status_filter = request.args.get('status', '')
    topic_filter = request.args.get('topic', '')
    
    # Build base query
    query = Paper.query.join(Author)
    
    # Apply search filter
    if search_query:
        query = query.filter(
            or_(
                Paper.title.ilike(f'%{search_query}%'),
                Author.name.ilike(f'%{search_query}%')
            )
        )
    
    # Apply status filter
    if status_filter:
        query = query.filter(Paper.status == status_filter)
    
    # Apply topic filter
    if topic_filter:
        query = query.join(Paper.topics).filter(Topic.topic_name == topic_filter)
    
    # Order by publication date (newest first)
    query = query.order_by(Paper.publication_date.desc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    papers_list = pagination.items
    
    # Get all unique statuses for filter dropdown
    statuses = db.session.query(Paper.status).distinct().all()
    statuses = [s[0] for s in statuses]
    
    # Get all topics for filter dropdown
    topics = Topic.query.order_by(Topic.topic_name).all()
    
    return render_template('papers.html',
                         papers=papers_list,
                         pagination=pagination,
                         search_query=search_query,
                         status_filter=status_filter,
                         topic_filter=topic_filter,
                         statuses=statuses,
                         topics=topics,
                         is_admin=current_user.is_admin())


@papers_bp.route('/<int:paper_id>')
@login_required
def paper_detail(paper_id):
    """
    Paper detail page
    Displays full information about a specific paper
    """
    paper = Paper.query.get_or_404(paper_id)
    return render_template('paper_detail.html', paper=paper, is_admin=current_user.is_admin())


@papers_bp.route('/add', methods=['POST'])
@login_required
def add_paper():
    """
    Add a new paper (admin only)
    """
    if not current_user.is_admin:
        flash('You do not have permission to add papers.', 'error')
        return redirect(url_for('papers.papers'))
    
    title = request.form.get('title', '').strip()
    abstract = request.form.get('abstract', '').strip()
    journal_name = request.form.get('journal_name', '').strip()
    publication_date = request.form.get('publication_date', '')
    citations = request.form.get('citations', 0, type=int)
    status = request.form.get('status', 'Draft')
    author_id = request.form.get('author_id', type=int)
    topic_ids = request.form.getlist('topic_ids')
    
    # Input validation
    if not all([title, journal_name, publication_date, author_id]):
        flash('Title, journal, publication date, and author are required.', 'error')
        return redirect(url_for('papers.papers'))
    
    try:
        publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid publication date format.', 'error')
        return redirect(url_for('papers.papers'))
    
    # Validate author exists
    author = Author.query.get(author_id)
    if not author:
        flash('Invalid author selected.', 'error')
        return redirect(url_for('papers.papers'))
    
    try:
        new_paper = Paper(
            title=title,
            abstract=abstract,
            journal_name=journal_name,
            publication_date=publication_date,
            citations=citations,
            status=status,
            author_id=author_id
        )
        
        # Add topics
        for topic_id in topic_ids:
            topic = Topic.query.get(topic_id)
            if topic:
                new_paper.topics.append(topic)
        
        db.session.add(new_paper)
        db.session.commit()
        
        flash('Paper added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add paper. Please try again.', 'error')
    
    return redirect(url_for('papers.papers'))


@papers_bp.route('/edit/<int:paper_id>', methods=['POST'])
@login_required
def edit_paper(paper_id):
    """
    Edit an existing paper (admin only)
    """
    if not current_user.is_admin:
        flash('You do not have permission to edit papers.', 'error')
        return redirect(url_for('papers.papers'))
    
    paper = Paper.query.get_or_404(paper_id)
    
    title = request.form.get('title', '').strip()
    abstract = request.form.get('abstract', '').strip()
    journal_name = request.form.get('journal_name', '').strip()
    publication_date = request.form.get('publication_date', '')
    citations = request.form.get('citations', 0, type=int)
    status = request.form.get('status', 'Draft')
    author_id = request.form.get('author_id', type=int)
    topic_ids = request.form.getlist('topic_ids')
    
    # Input validation
    if not all([title, journal_name, publication_date, author_id]):
        flash('Title, journal, publication date, and author are required.', 'error')
        return redirect(url_for('papers.paper_detail', paper_id=paper_id))
    
    try:
        publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid publication date format.', 'error')
        return redirect(url_for('papers.paper_detail', paper_id=paper_id))
    
    # Validate author exists
    author = Author.query.get(author_id)
    if not author:
        flash('Invalid author selected.', 'error')
        return redirect(url_for('papers.paper_detail', paper_id=paper_id))
    
    try:
        paper.title = title
        paper.abstract = abstract
        paper.journal_name = journal_name
        paper.publication_date = publication_date
        paper.citations = citations
        paper.status = status
        paper.author_id = author_id
        
        # Update topics (clear and re-add)
        paper.topics = []
        for topic_id in topic_ids:
            topic = Topic.query.get(topic_id)
            if topic:
                paper.topics.append(topic)
        
        db.session.commit()
        
        flash('Paper updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to update paper. Please try again.', 'error')
    
    return redirect(url_for('papers.paper_detail', paper_id=paper_id))


@papers_bp.route('/delete/<int:paper_id>', methods=['POST'])
@login_required
def delete_paper(paper_id):
    """
    Delete a paper (admin only)
    """
    if not current_user.is_admin:
        flash('You do not have permission to delete papers.', 'error')
        return redirect(url_for('papers.papers'))
    
    paper = Paper.query.get_or_404(paper_id)
    
    try:
        db.session.delete(paper)
        db.session.commit()
        flash('Paper deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete paper. Please try again.', 'error')
    
    return redirect(url_for('papers.papers'))


@papers_bp.route('/export/csv')
@login_required
def export_csv():
    """
    Export all papers to CSV file
    """
    papers = Paper.query.join(Author).all()
    
    # Create CSV string
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Title', 'Author', 'Journal', 'Publication Date', 'Citations', 'Status', 'Topics'])
    
    # Write data
    for paper in papers:
        topics = ', '.join([t.topic_name for t in paper.topics])
        writer.writerow([
            paper.title,
            paper.author.name if paper.author else 'N/A',
            paper.journal_name,
            paper.publication_date.strftime('%Y-%m-%d') if paper.publication_date else 'N/A',
            paper.citations,
            paper.status,
            topics
        ])
    
    # Create response
    output.seek(0)
    response = jsonify({'csv': output.getvalue()})
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=papers.csv'
    
    return response


@papers_bp.route('/api/authors')
@login_required
def get_authors():
    """
    API endpoint to get all authors (for dropdown)
    """
    authors = Author.query.order_by(Author.name).all()
    return jsonify([{'id': a.author_id, 'name': a.name} for a in authors])


@papers_bp.route('/api/topics')
@login_required
def get_topics():
    """
    API endpoint to get all topics (for dropdown)
    """
    topics = Topic.query.order_by(Topic.topic_name).all()
    return jsonify([{'id': t.topic_id, 'name': t.topic_name} for t in topics])
