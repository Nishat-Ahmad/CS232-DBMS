from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from database.models import Session, Attendance, User, Meal, Billing, DeletedAttendance
from utils.auth_decorators import login_required, admin_required
from datetime import datetime
from sqlalchemy.orm import joinedload
from services.billing_service import update_billing_and_notify

attendance_bp = Blueprint('attendance_bp', __name__, url_prefix='/attendance')

# Admin: View all attendance records
@attendance_bp.route('/view')
@login_required
@admin_required
def view_attendance():
    db = Session()
    records = db.query(Attendance).options(joinedload(Attendance.user), joinedload(Attendance.meal)).all()
    db.close()
    return render_template('view_attendance.html', records=records)

# Admin: Add attendance record
@attendance_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_attendance():
    db = Session()
    users = db.query(User).all()
    meals = db.query(Meal).all()
    if request.method == 'POST':
        user_id = request.form['user_id']
        meal_id = request.form['meal_id']
        date = request.form['date']
        status = request.form['status']
        exists = db.query(Attendance).filter_by(user_id=user_id, meal_id=meal_id, date=date).first()
        if exists:
            flash('Attendance already recorded for this user, meal, and date.', 'error')
        else:
            attendance = Attendance(user_id=user_id, meal_id=meal_id, date=date, status=status)
            db.add(attendance)
            db.commit()
            if status == 'present':
                update_billing_and_notify(db, user_id, datetime.strptime(date, '%Y-%m-%d'), meal_id)
            flash('Attendance recorded.', 'success')
        db.close()
        return redirect(url_for('attendance_bp.view_attendance'))
    db.close()
    return render_template('add_attendance.html', users=users, meals=meals, today=datetime.today().strftime('%Y-%m-%d'))

# Admin: Edit attendance record
@attendance_bp.route('/edit/<int:attendance_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_attendance(attendance_id):
    db = Session()
    record = db.query(Attendance).get(attendance_id)
    users = db.query(User).all()
    meals = db.query(Meal).all()
    if not record:
        db.close()
        flash('Attendance record not found.', 'error')
        return redirect(url_for('attendance_bp.view_attendance'))
    if request.method == 'POST':
        record.user_id = request.form['user_id']
        record.meal_id = request.form['meal_id']
        record.date = request.form['date']
        record.status = request.form['status']
        db.commit()
        db.close()
        flash('Attendance updated.', 'success')
        return redirect(url_for('attendance_bp.view_attendance'))
    response = render_template('edit_attendance.html', record=record, users=users, meals=meals)
    db.close()
    return response

# Admin: Delete attendance record
@attendance_bp.route('/delete/<int:attendance_id>')
@login_required
@admin_required
def delete_attendance(attendance_id):
    db = Session()
    record = db.query(Attendance).get(attendance_id)
    if record:
        db.delete(record)
        db.commit()
        flash('Attendance deleted.', 'info')
    else:
        flash('Attendance record not found.', 'error')
    db.close()
    return redirect(url_for('attendance_bp.view_attendance'))

# Admin: View deleted attendance records
@attendance_bp.route('/deleted')
@login_required
@admin_required
def view_deleted_attendance():
    session = Session()
    deleted_attendance = session.query(DeletedAttendance).all()
    session.close()
    return render_template('deleted_attendance.html', records=deleted_attendance)

# Admin: Restore deleted attendance record
@attendance_bp.route('/restore/<int:attendance_id>', methods=['POST'])
@login_required
@admin_required
def restore_attendance(attendance_id):
    session = Session()
    session.execute('''
        INSERT INTO attendance (id, user_id, meal_id, date, status)
        SELECT id, user_id, meal_id, date, status FROM deleted_attendance WHERE id = :attendance_id;
        DELETE FROM deleted_attendance WHERE id = :attendance_id;
    ''', {'attendance_id': attendance_id})
    session.commit()
    session.close()
    flash('Attendance record restored successfully!', 'success')
    return redirect(url_for('attendance_bp.view_deleted_attendance'))

# Student: View own attendance
@attendance_bp.route('/my')
@login_required
def my_attendance():
    db = Session()
    records = db.query(Attendance).options(joinedload(Attendance.meal)).filter_by(user_id=g.user.id).all()
    db.close()
    return render_template('my_attendance.html', records=records)

# Student: Mark own attendance for a meal if bill is paid or under threshold
@attendance_bp.route('/mark', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    db = Session()
    meals = db.query(Meal).all()
    today = datetime.today().date()
    threshold = 10000
    month = today.strftime('%B')
    year = today.year
    bill = db.query(Billing).filter_by(student_id=g.user.id, month=month, year=year).first()
    can_mark = (not bill) or (bill.status == 'paid') or (bill.amount <= threshold)
    if request.method == 'POST' and can_mark:
        meal_id = request.form['meal_id']
        exists = db.query(Attendance).filter_by(user_id=g.user.id, meal_id=meal_id, date=today).first()
        if exists:
            flash('Attendance already marked for this meal today.', 'error')
        else:
            attendance = Attendance(user_id=g.user.id, meal_id=meal_id, date=today, status='present')
            db.add(attendance)
            db.commit()
            update_billing_and_notify(db, g.user.id, today, meal_id)
            flash('Attendance marked!', 'success')
        db.close()
        return redirect(url_for('attendance_bp.my_attendance'))
    db.close()
    return render_template('mark_attendance.html', meals=meals, can_mark=can_mark, bill=bill, threshold=threshold)
