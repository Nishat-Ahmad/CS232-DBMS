from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.models import Session, User, Admin, Student, DeletedUser
from utils.auth_decorators import login_required, admin_required
from sqlalchemy import text

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

@user_bp.route('/view')
@login_required
@admin_required
def view_users():
    '''Admin: Shows admin data of all the users.'''
    db = Session()
    students = db.query(Student).all()
    admins = db.query(Admin).all()
    db.close()
    return render_template('view_users.html', students=students, admins=admins)

@user_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    '''Admin: Allows admin to add a user.'''
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
    '''Admin: Allows admin to update user data.'''
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
    '''Deletes a user data from the table.'''
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
    '''Fetches data from the deleted table of users.'''
    session = Session()
    deleted_users = session.query(DeletedUser).all()
    session.close()
    return render_template('deleted_users.html', users=deleted_users)

@user_bp.route('/restore/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def restore_user(user_id):
    '''Restores user from deleted table.'''
    session = Session()
    # Check if user with same id already exists in users table
    existing_user = session.query(User).filter_by(id=user_id).first()
    if existing_user:
        session.close()
        flash('A user with this ID already exists. Cannot restore.', 'danger')
        return redirect(url_for('user_bp.view_deleted_users'))

    # Fetch deleted user row
    deleted_user = session.query(DeletedUser).filter_by(id=user_id).first()
    if not deleted_user:
        session.close()
        flash('Deleted user not found.', 'danger')
        return redirect(url_for('user_bp.view_deleted_users'))

    # Restore to users table
    session.execute(text('''
        INSERT INTO users (id, name, email, password, role, type)
        SELECT id, name, email, password, role, type FROM deleted_users WHERE id = :user_id;
    '''), {'user_id': user_id})

    # Restore to subtable
    if deleted_user.role == 'student':
        session.execute(text('''
            INSERT INTO students (id, roll_number)
            SELECT id, :roll_number FROM deleted_users WHERE id = :user_id;
        '''), {'user_id': user_id, 'roll_number': 'restored-roll'})
    elif deleted_user.role == 'admin':
        session.execute(text('''
            INSERT INTO admins (id, admin_level)
            SELECT id, :admin_level FROM deleted_users WHERE id = :user_id;
        '''), {'user_id': user_id, 'admin_level': 'restored-admin'})

    # Remove from deleted_users
    session.execute(text('DELETE FROM deleted_users WHERE id = :user_id;'), {'user_id': user_id})

    session.commit()
    session.close()
    flash('User restored successfully!', 'success')
    return redirect(url_for('user_bp.view_deleted_users'))
