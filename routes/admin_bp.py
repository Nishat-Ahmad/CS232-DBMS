from flask import Blueprint, render_template, flash, redirect, url_for
from database.models import Session, Complaint
from utils.auth_decorators import login_required, admin_required
from sqlalchemy.orm import joinedload

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# Route to view unresolved complaints
@admin_bp.route('/complaints')
@login_required
@admin_required
def view_complaints():
    db_session = Session()
    complaints = db_session.query(Complaint) \
        .options(joinedload(Complaint.student)) \
        .filter(Complaint.status != 'resolved') \
        .all()
    db_session.close()
    return render_template('admin_complaints.html', complaints=complaints)

# Route to view resolved complaints
@admin_bp.route('/complaints/resolved')
@login_required
@admin_required
def view_resolved_complaints():
    db_session = Session()
    complaints = db_session.query(Complaint) \
        .options(joinedload(Complaint.student)) \
        .filter(Complaint.status == 'resolved') \
        .all()
    db_session.close()
    return render_template('admin_resolved_complaints.html', complaints=complaints)

# Route to resolve a complaint
@admin_bp.route('/complaints/resolve/<int:id>', methods=['POST'])
@login_required
@admin_required
def resolve_complaint(id):
    db_session = Session()
    complaint = db_session.get(Complaint, id)  # Fetch complaint by ID
    if complaint:
        complaint.status = 'resolved'
        db_session.commit()  # Commit changes to the database
        flash("Complaint marked as resolved", 'success')

    db_session.close()
    return redirect(url_for('admin_bp.view_complaints'))
