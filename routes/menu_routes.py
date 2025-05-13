from flask import Blueprint, render_template, redirect, url_for, request, flash, g
from database.models import Menu, MenuDay, Meal, Session, DeletedMenu
from datetime import datetime
from utils.auth_decorators import login_required, admin_required
from sqlalchemy.exc import IntegrityError
import logging
logging.basicConfig(filename='db_errors.log', level=logging.ERROR)

menu_bp = Blueprint('menu_bp', __name__)

# View all menus
@menu_bp.route('/menus')
@login_required
def view_menus():
    session = Session()
    menus = session.query(Menu).all()
    session.close()
    return render_template('view_menus.html', menus=menus)

# Create a new menu
from datetime import datetime

@menu_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required 
def add_menu():
    if request.method == 'POST':
        name = request.form['name']
        start_date_str = request.form['start_date']
        is_template = 'is_template' in request.form

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else datetime.today()

        new_menu = Menu(name=name, start_date=start_date, is_template=is_template)

        session = Session() 
        try:
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                breakfast_id = request.form[f'{day}_breakfast']
                lunch_id = request.form[f'{day}_lunch']
                dinner_id = request.form[f'{day}_dinner']

                menu_day = MenuDay(
                    menu=new_menu,
                    day_of_week=day,
                    breakfast_id=breakfast_id,
                    lunch_id=lunch_id,
                    dinner_id=dinner_id
                )
                session.add(menu_day) 
            session.add(new_menu)  
            session.commit()  
            flash('Menu added successfully!', 'success')
            return redirect(url_for('menu_bp.view_menus'))  
        except IntegrityError as e:
            session.rollback()
            logging.error(f"IntegrityError in add_menu: {str(e)}")
            flash('A menu with this information already exists or a database constraint was violated.', 'danger')
            return redirect(request.url)
        finally:
            session.close()
    # GET request: Fetch all meals to display in the form
    session = Session()
    meals = session.query(Meal).all()  
    session.close()

    return render_template('add_menu.html', meals=meals, datetime=datetime)


@menu_bp.route('/menus/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_menu(id):
    session = Session()
    menu = session.get(Menu, id)
    if not menu:
        session.close()
        flash('Menu not found.', 'error')
        return redirect(url_for('menu_bp.view_menus'))

    menu_days = session.query(MenuDay).filter_by(menu_id=id).all()

    if request.method == 'POST':
        menu.name = request.form['name']
        menu.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        menu.is_template = 'is_template' in request.form

        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            menu_day = next((md for md in menu_days if md.day_of_week == day), None)
            if menu_day:
                breakfast_id = request.form[f'{day}_breakfast']
                lunch_id = request.form[f'{day}_lunch']
                dinner_id = request.form[f'{day}_dinner']

              
                breakfast = session.get(Meal, breakfast_id)
                lunch = session.get(Meal, lunch_id)
                dinner = session.get(Meal, dinner_id)

                if not breakfast or not lunch or not dinner:
                    session.close()
                    flash(f'Invalid meal selection for {day.capitalize()}.', 'error')
                    return redirect(url_for('menu_bp.edit_menu', id=id))

                
                menu_day.breakfast_id = breakfast_id
                menu_day.lunch_id = lunch_id
                menu_day.dinner_id = dinner_id

        session.commit()
        session.close()
        flash('Menu updated successfully!', 'success')
        return redirect(url_for('menu_bp.view_menus'))

    meals = session.query(Meal).all()
    session.close()

    return render_template('edit_menu.html', menu=menu, meals=meals, menu_days=menu_days, datetime=datetime)

@menu_bp.route('/menus/delete/<int:id>', methods=['POST'])
@admin_required
def delete_menu(id):
    session = Session()
    menu = session.get(Menu, id)

    if not menu:
        session.close()
        flash('Menu not found.', 'error')
        return redirect(url_for('menu_bp.view_menus'))

    try:
        session.query(MenuDay).filter_by(menu_id=id).delete()

        session.delete(menu)

        session.commit()
        session.close()

        flash('Menu deleted successfully!', 'success')
    except Exception as e:
        session.rollback() 
        session.close()
        flash(f'Error deleting menu: {str(e)}', 'error')

    return redirect(url_for('menu_bp.view_menus'))

# Student: View current menu
@menu_bp.route('/my')
@login_required
def my_menu():
    db = Session()
    from sqlalchemy.orm import joinedload
    menu = db.query(Menu).options(joinedload(Menu.days).joinedload(MenuDay.breakfast), joinedload(Menu.days).joinedload(MenuDay.lunch), joinedload(Menu.days).joinedload(MenuDay.dinner)).order_by(Menu.start_date.desc()).first()
    db.close()
    return render_template('my_menu.html', menu=menu)

@menu_bp.route('/deleted')
@login_required
@admin_required
def view_deleted_menus():
    session = Session()
    deleted_menus = session.query(DeletedMenu).all()
    session.close()
    return render_template('deleted_menus.html', menus=deleted_menus)

@menu_bp.route('/restore/<int:menu_id>', methods=['POST'])
@login_required
@admin_required
def restore_menu(menu_id):
    session = Session()
    session.execute('''
        INSERT INTO menus (id, name, start_date, is_template)
        SELECT id, name, start_date, is_template FROM deleted_menus WHERE id = :menu_id;
        DELETE FROM deleted_menus WHERE id = :menu_id;
    ''', {'menu_id': menu_id})
    session.commit()
    session.close()
    flash('Menu restored successfully!', 'success')
    return redirect(url_for('menu_bp.view_deleted_menus'))
