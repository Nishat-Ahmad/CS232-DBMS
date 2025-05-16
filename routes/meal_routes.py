from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.models import Meal, DeletedMeal, Session
from utils.auth_decorators import login_required, admin_required
from sqlalchemy import text

meal_bp = Blueprint('meal_bp', __name__, url_prefix='/meals')

@meal_bp.route('/view')
@login_required
@admin_required
def view_meals():
    '''View all meals'''
    session = Session()
    meals = session.query(Meal).all()
    session.close()
    return render_template('view_meals.html', meals=meals)

@meal_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_meal():
    '''Add a meal'''
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        price = request.form['price']
        inventory = request.form['inventory']

        if not name or not time or not price or not inventory:
            flash("Please fill in all fields.", 'error')
            return redirect(url_for('meal_bp.add_meal'))

        if time not in ['breakfast', 'lunch', 'dinner']:
            flash("Invalid meal time.", 'error')
            return redirect(url_for('meal_bp.add_meal'))

        session = Session()
        new_meal = Meal(name=name, time=time, price=price, inventory=inventory)
        session.add(new_meal)
        session.commit()
        session.close()
        flash('Meal added successfully!', 'success')
        return redirect(url_for('meal_bp.view_meals'))

    return render_template('add_meal.html')

@meal_bp.route('/edit/<int:meal_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_meal(meal_id):
    '''Edit meal'''
    session = Session()
    meal = session.query(Meal).get(meal_id)

    if not meal:
        flash("Meal not found.", 'error')
        return redirect(url_for('meal_bp.view_meals'))

    if request.method == 'POST':
        meal.name = request.form['name']
        meal.time = request.form['time']
        meal.price = request.form['price']
        meal.inventory = request.form['inventory']

        session.commit()
        session.close()
        flash('Meal updated successfully!', 'success')
        return redirect(url_for('meal_bp.view_meals'))

    session.close()
    return render_template('edit_meal.html', meal=meal)

@meal_bp.route('/delete/<int:meal_id>')
@login_required
@admin_required
def delete_meal(meal_id):
    '''Delete meal'''
    session = Session()
    meal = session.query(Meal).get(meal_id)
    if meal:
        session.delete(meal)
        session.commit()
        flash('Meal deleted successfully.', 'success')
    else:
        flash('Meal not found.', 'error')
    session.close()
    return redirect(url_for('meal_bp.view_meals'))

@meal_bp.route('/deleted')
@login_required
@admin_required
def view_deleted_meals():
    '''View deleted meals'''
    session = Session()
    deleted_meals = session.query(DeletedMeal).all()
    session.close()
    return render_template('deleted_meals.html', meals=deleted_meals)

@meal_bp.route('/restore/<int:meal_id>', methods=['POST'])
@login_required
@admin_required
def restore_meal(meal_id):
    '''Restore meal'''
    session = Session()
    session.execute(text('''
        INSERT INTO meals (id, name, time, price, inventory)
        SELECT id, name, time, price, inventory FROM deleted_meals WHERE id = :meal_id;
        DELETE FROM deleted_meals WHERE id = :meal_id;
    '''), {'meal_id': meal_id})
    session.commit()
    session.close()
    flash('Meal restored successfully!', 'success')
    return redirect(url_for('meal_bp.view_deleted_meals'))
