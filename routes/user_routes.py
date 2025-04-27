from flask import Blueprint, render_template, request, redirect, url_for
from database.models import User, Session
from utils.auth_decorators import login_required, admin_required

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

@user_bp.route('/view')
@login_required
@admin_required
def view_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return render_template('view_users.html', users=users)

@user_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        session = Session()
        new_user = User(name=name, email=email, password=password, role=role)
        session.add(new_user)
        session.commit()
        session.close()
        return redirect(url_for('user_bp.view_users'))

    return render_template('add_user.html')

@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        user.role = request.form['role']
        session.commit()
        session.close()
        return redirect(url_for('user_bp.view_users'))

    session.close()
    return render_template('edit_user.html', user=user)

@user_bp.route('/delete/<int:user_id>')
def delete_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    session.close()
    return redirect(url_for('user_bp.view_users'))
