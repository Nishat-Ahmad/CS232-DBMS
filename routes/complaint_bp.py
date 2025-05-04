from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.models import Session, Complaint, Student
from flask import session as flask_session
from utils.auth_decorators import login_required, student_required

complaint_bp = Blueprint('complaint_bp', __name__, url_prefix='/complaint')

@complaint_bp.route('/create', methods=['GET', 'POST'])
@login_required
@student_required
def create_complaint():
    if request.method == 'POST':
        # Get the complaint message from the form
        message = request.form['message']
        student_id = flask_session.get('user_id')  # Get the student ID from the session

        if not message:
            flash("Complaint message cannot be empty", 'danger')
            return redirect(url_for('complaint_bp.create_complaint'))

        # Create the complaint object
        db_session = Session()
        new_complaint = Complaint(student_id=student_id, message=message)

        # Add complaint to the database
        db_session.add(new_complaint)
        db_session.commit()
        db_session.close()

        flash("Your complaint has been submitted successfully!", 'success')
        return redirect(url_for('index'))  # Redirect to the index page or another suitable page

    return render_template('create_complaint.html')  # Render complaint form page

