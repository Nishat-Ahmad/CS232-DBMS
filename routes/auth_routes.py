from flask import Blueprint, render_template, request, redirect, url_for, session as flask_session, flash
from database.models import Session, User

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    '''handles user login'''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()

        if user:
            print("Password match:", (user.password, password))
            print("User ID:", user.id, "Role:", user.role)

        if user and (user.password, password):
            flask_session['user_id'] = user.id
            flask_session['user_role'] = user.role
            db_session.close()
            return redirect(url_for('index'))

        db_session.close()
        flash("Invalid email or password", 'danger')
        return redirect(url_for('auth_bp.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    '''handles user logout'''
    flask_session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))
