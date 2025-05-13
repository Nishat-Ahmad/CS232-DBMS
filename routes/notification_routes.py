from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session as flask_session
from database.models import Session, Notification, NotificationRead
from utils.auth_decorators import login_required, admin_required, student_required
from sqlalchemy.orm import joinedload

notification_bp = Blueprint('notification_bp', __name__, url_prefix='/notifications')

# Admin: Create new notification
@notification_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_notification():
    if request.method == 'POST':
        message = request.form['message']
        target_role = request.form['target_role']
        admin_id = flask_session.get('user_id')

        if not message:
            flash("Message cannot be empty", 'danger')
            return redirect(url_for('notification_bp.create_notification'))

        db_session = Session()
        notification = Notification(
            message=message,
            target_role=target_role,
            admin_id=admin_id
        )
        db_session.add(notification)
        db_session.commit()
        db_session.close()

        flash("Notification created successfully", 'success')

        return redirect(url_for('notification_bp.view_all_notifications')) 

    return render_template('create_notification.html')

# Admin: View all notifications
@notification_bp.route('/all')
@login_required
@admin_required
def view_all_notifications():  
    db_session = Session()
    notifications = db_session.query(Notification).options(joinedload(Notification.admin)).all()
    db_session.close()
    return render_template('all_notifications.html', notifications=notifications)


# Student: View notifications for student
@notification_bp.route('/student')
@login_required
@student_required
def view_student_notifications():
    student_id = flask_session.get('user_id')
    db_session = Session()

    notifications = db_session.query(Notification) \
        .filter(Notification.target_role.in_(['student', 'all'])) \
        .all()

    read_ids = {read.notification_id for read in db_session.query(NotificationRead).filter_by(student_id=student_id)}

    db_session.close()
    return render_template('student_notifications.html', notifications=notifications, read_ids=read_ids)

# Student: Mark notification as read
@notification_bp.route('/mark_read/<int:notification_id>', methods=['POST'])
@login_required
@student_required
def mark_as_read(notification_id):
    student_id = flask_session.get('user_id')
    db_session = Session()

    existing = db_session.query(NotificationRead).filter_by(student_id=student_id, notification_id=notification_id).first()
    if not existing:
        read_entry = NotificationRead(student_id=student_id, notification_id=notification_id)
        db_session.add(read_entry)
        db_session.commit()

    db_session.close()
    return redirect(url_for('notification_bp.view_student_notifications'))
