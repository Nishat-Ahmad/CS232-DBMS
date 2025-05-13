from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session as flask_session
from utils.auth_decorators import login_required, student_required, admin_required
from database.models import Session, Complaint
from sqlalchemy.orm import joinedload

complaint_bp = Blueprint('complaint_bp', __name__, url_prefix='/complaint')

@complaint_bp.route('/create', methods=['GET', 'POST'])
@login_required
@student_required
def create_complaint():
    if request.method == 'POST':
        message = request.form['message']
        student_id = flask_session.get('user_id')

        if not message:
            flash("Complaint message cannot be empty", 'danger')
            return redirect(url_for('complaint_bp.create_complaint'))

        db_session = Session()
        new_complaint = Complaint(student_id=student_id, message=message)

        db_session.add(new_complaint)
        db_session.commit()
        db_session.close()

        flash("Your complaint has been submitted successfully!", 'success')
        return redirect(url_for('index'))  

    return render_template('create_complaint.html')  

@complaint_bp.route('/complaints')
@login_required
@admin_required
def view_complaints():
    db_session = Session()
    complaints = db_session.query(Complaint) \
        .options(joinedload(Complaint.student)) \
        .filter(Complaint.status != 'resolved') \
        .all()
    db_session.close()
    return render_template('resolve_complaints.html', complaints=complaints)

@complaint_bp.route('/complaints/resolved')
@login_required
@admin_required
def view_resolved_complaints():
    db_session = Session()
    complaints = db_session.query(Complaint) \
        .options(joinedload(Complaint.student)) \
        .filter(Complaint.status == 'resolved') \
        .all()
    db_session.close()
    return render_template('resolved_complaints.html', complaints=complaints)

@complaint_bp.route('/complaints/resolve/<int:id>', methods=['POST'])
@login_required
@admin_required
def resolve_complaint(id):
    db_session = Session()
    complaint = db_session.get(Complaint, id) 
    if complaint:
        complaint.status = 'resolved'
        db_session.commit() 
        flash("Complaint marked as resolved", 'success')

    db_session.close()
    return redirect(url_for('complaint_bp.view_complaints'))
