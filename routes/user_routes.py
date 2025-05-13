from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.models import Session, User, Admin, Student, DeletedUser
from utils.auth_decorators import login_required, admin_required
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import logging

logging.basicConfig(filename='db_errors.log', level=logging.ERROR)

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

@user_bp.route('/view')
@login_required
@admin_required
def view_users():
    db = Session()
    students = db.query(Student).all()
    admins = db.query(Admin).all()
    db.close()
    return render_template('view_users.html', students=students, admins=admins)

@user_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    role = 'student' 

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  
        roll_number = request.form.get('roll_number')  
        admin_level = request.form.get('admin_level')  

        session = Session()
       
        if role == 'student':
            new_user = Student(name=name, email=email, password=(password), role=role, roll_number=roll_number)
        else:  # Admin
            new_user = Admin(name=name, email=email, password=(password), role=role, admin_level=admin_level)

        session.add(new_user)
        session.commit()
        session.close()

        flash(f'User {name} added successfully!', 'success')
        return redirect(url_for('user_bp.view_users'))

    return render_template('add_user.html', role=role) 


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    db = Session()
    user = db.query(User).get(user_id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        user.roll_number = request.form['roll_number']
        db.commit()
        db.close()
        flash('User updated.', 'success')
        return redirect(url_for('user_bp.view_users'))

    response = render_template('edit_user.html', user=user)
    db.close()
    return response

    

@user_bp.route('/delete/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    db = Session()
    user = db.query(User).get(user_id)
    db.delete(user)
    db.commit()
    db.close()
    flash('User deleted.', 'info')
    return redirect(url_for('user_bp.view_users'))

@user_bp.route('/deleted')
@login_required
@admin_required
def view_deleted_users():
    session = Session()
    deleted_users = session.query(DeletedUser).all()
    session.close()
    return render_template('deleted_users.html', users=deleted_users)

@user_bp.route('/restore/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def restore_user(user_id):
    session = Session()
    try:
        session.execute(text('''
            INSERT INTO users (id, name, email, password, role, type)
            SELECT id, name, email, password, role, type FROM deleted_users WHERE id = :user_id;
        '''), {'user_id': user_id})
        session.execute(text('''
            DELETE FROM deleted_users WHERE id = :user_id;
        '''), {'user_id': user_id})
        session.commit()
        flash('User restored successfully!', 'success')
    except IntegrityError as e:
        session.rollback()
        logging.error(f"IntegrityError in restore_user: {str(e)}")
        flash('User could not be restored: user with this ID or email already exists.', 'danger')
    except Exception as e:
        session.rollback()
        logging.error(f"Error in restore_user: {str(e)}")
        flash('An error occurred while restoring the user.', 'danger')
    finally:
        session.close()
    return redirect(url_for('user_bp.view_deleted_users'))
