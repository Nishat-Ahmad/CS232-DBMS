from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    '''Ensures the user is logged in.'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login required!', 'danger')
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    '''Ensures the user is an admin.'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'admin':
            flash('Admin access required!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    '''Ensures the user is a student.'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'student':
            flash('Only students can complain.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function