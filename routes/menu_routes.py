from flask import Blueprint, render_template, request, redirect, url_for
from main import WeeklyMenu, Session

menu_bp = Blueprint('menu_bp', __name__, url_prefix='/menus')

@menu_bp.route('/view')
def view_menus():
    session = Session()
    menus = session.query(WeeklyMenu).all()
    session.close()
    return render_template('view_menus.html', menus=menus)

@menu_bp.route('/add', methods=['GET', 'POST'])
def add_menu():
    if request.method == 'POST':
        weekday = request.form['weekday']
        meal_type = request.form['meal_type']
        items = request.form['items']

        session = Session()
        new_menu = WeeklyMenu(weekday=weekday, meal_type=meal_type, items=items)
        session.add(new_menu)
        session.commit()
        session.close()
        return redirect(url_for('menu_bp.view_menus'))

    return render_template('add_menu.html')
