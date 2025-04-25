from flask import Blueprint, render_template, request, redirect, url_for
from main import User, Session

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

@user_bp.route('/view')
def view_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return render_template('view_users.html', users=users)

@user_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

        session = Session()
        new_user = User(email=email, role=role, password=password)
        session.add(new_user)
        session.commit()
        session.close()
        return redirect(url_for('user_bp.view_users'))

    return render_template('add_user.html')


