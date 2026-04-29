"""
Authors Routes
Handles authors management and viewing
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import or_
from models.author import Author, db
from models.paper import Paper

authors_bp = Blueprint('authors', __name__, url_prefix='/authors')


@authors_bp.route('/')
@login_required
def authors():
    """
    Authors management page
    Displays card-based grid of authors with search
    """
    # Get search query
    search_query = request.args.get('search', '').strip()
    
    # Build query
    query = Author.query
    
    # Apply search filter
    if search_query:
        query = query.filter(
            or_(
                Author.name.ilike(f'%{search_query}%'),
                Author.university.ilike(f'%{search_query}%')
            )
        )
    
    # Order by name
    authors_list = query.order_by(Author.name).all()
    
    return render_template('authors.html',
                         authors=authors_list,
                         search_query=search_query,
                         is_admin=current_user.is_admin())


@authors_bp.route('/<int:author_id>')
@login_required
def author_detail(author_id):
    """
    Author detail page
    Displays all papers for a specific author
    """
    author = Author.query.get_or_404(author_id)
    papers = Paper.query.filter_by(author_id=author_id)\
                        .order_by(Paper.publication_date.desc()).all()
    
    return render_template('authors.html',
                         author=author,
                         papers=papers,
                         is_admin=current_user.is_admin())


@authors_bp.route('/add', methods=['POST'])
@login_required
def add_author():
    """
    Add a new author (admin only)
    """
    if not current_user.is_admin:
        flash('You do not have permission to add authors.', 'error')
        return redirect(url_for('authors.authors'))
    
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    university = request.form.get('university', '').strip()
    country = request.form.get('country', '').strip()
    
    # Input validation
    if not all([name, email, university, country]):
        flash('All fields are required.', 'error')
        return redirect(url_for('authors.authors'))
    
    # Check if email already exists
    if Author.query.filter_by(email=email).first():
        flash('Email already registered.', 'error')
        return redirect(url_for('authors.authors'))
    
    try:
        new_author = Author(
            name=name,
            email=email,
            university=university,
            country=country
        )
        db.session.add(new_author)
        db.session.commit()
        
        flash('Author added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add author. Please try again.', 'error')
    
    return redirect(url_for('authors.authors'))
