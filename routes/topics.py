"""
Topics Routes
Handles topics viewing and filtering
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.topic import Topic
from models.paper import Paper
from models import db

topics_bp = Blueprint('topics', __name__, url_prefix='/topics')


@topics_bp.route('/')
@login_required
def topics():
    """
    Topics page
    Displays all topics as tags/badges
    """
    topics_list = Topic.query.order_by(Topic.topic_name).all()
    return render_template('topics.html', topics=topics_list, is_admin=current_user.is_admin())


@topics_bp.route('/<int:topic_id>')
@login_required
def topic_detail(topic_id):
    """
    Topic detail page
    Displays all papers for a specific topic
    """
    topic = Topic.query.get_or_404(topic_id)
    papers = topic.papers.order_by(Paper.publication_date.desc()).all()
    
    return render_template('topics.html', topic=topic, papers=papers, is_admin=current_user.is_admin())


@topics_bp.route('/add', methods=['POST'])
@login_required
def add_topic():
    """
    Add a new topic (admin only)
    """
    if not current_user.is_admin():
        flash('Only admins can add topics', 'error')
        return redirect(url_for('topics.topics'))
    
    topic_name = request.form.get('topic_name', '').strip()
    
    if not topic_name:
        flash('Topic name is required', 'error')
        return redirect(url_for('topics.topics'))
    
    # Check if topic already exists
    existing = Topic.query.filter_by(topic_name=topic_name).first()
    if existing:
        flash('Topic already exists', 'error')
        return redirect(url_for('topics.topics'))
    
    try:
        topic = Topic(topic_name=topic_name)
        db.session.add(topic)
        db.session.commit()
        flash(f'Topic "{topic_name}" added successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding topic: {str(e)}', 'error')
    
    return redirect(url_for('topics.topics'))


@topics_bp.route('/<int:topic_id>/delete', methods=['POST'])
@login_required
def delete_topic(topic_id):
    """
    Delete a topic (admin only)
    """
    if not current_user.is_admin():
        flash('Only admins can delete topics', 'error')
        return redirect(url_for('topics.topics'))
    
    topic = Topic.query.get_or_404(topic_id)
    
    try:
        db.session.delete(topic)
        db.session.commit()
        flash(f'Topic "{topic.topic_name}" deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting topic: {str(e)}', 'error')
    
    return redirect(url_for('topics.topics'))
