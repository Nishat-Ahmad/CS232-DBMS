from flask import Blueprint, render_template, request, redirect, url_for
from main import Meal, Session
from utils.auth_decorators import login_required, admin_required

meal_bp = Blueprint('meal_bp', __name__, url_prefix='/meals')

@meal_bp.route('/view')
@login_required
@admin_required
def view_meals():
    session = Session()
    meals = session.query(Meal).all()
    session.close()
    return render_template('view_meals.html', meals=meals)

@meal_bp.route('/add', methods=['GET', 'POST'])
def add_meal():
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        price = request.form['price']
        inventory = request.form['inventory']

        session = Session()
        new_meal = Meal(name=name, time=time, price=price, inventory=inventory)
        session.add(new_meal)
        session.commit()
        session.close()
        return redirect(url_for('meal_bp.view_meals'))

    return render_template('add_meal.html')

@meal_bp.route('/edit/<int:meal_id>', methods=['GET', 'POST'])
def edit_meal(meal_id):
    session = Session()
    meal = session.query(Meal).get(meal_id)

    if request.method == 'POST':
        meal.name = request.form['name']
        meal.time = request.form['time']
        meal.price = request.form['price']
        meal.inventory = request.form['inventory']
        session.commit()
        session.close()
        return redirect(url_for('meal_bp.view_meals'))

    session.close()
    return render_template('edit_meal.html', meal=meal)

@meal_bp.route('/delete/<int:meal_id>')
def delete_meal(meal_id):
    session = Session()
    meal = session.query(Meal).get(meal_id)
    session.delete(meal)
    session.commit()
    session.close()
    return redirect(url_for('meal_bp.view_meals'))
