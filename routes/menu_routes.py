from flask import Blueprint, render_template, redirect, url_for, request, flash
from database.models import Menu, MenuDay, Meal, Session
from datetime import datetime
from utils.auth_decorators import login_required, admin_required

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
@admin_required  # Assuming only admins can add menus
def add_menu():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        start_date_str = request.form['start_date']
        is_template = 'is_template' in request.form

        # Convert start_date string to datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else datetime.today()

        # Create new Menu
        new_menu = Menu(name=name, start_date=start_date, is_template=is_template)

        # Add MenuDays for each day of the week (Monday to Sunday)
        session = Session()  # Start a new session
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            breakfast_id = request.form[f'{day}_breakfast']
            lunch_id = request.form[f'{day}_lunch']
            dinner_id = request.form[f'{day}_dinner']

            # Create a MenuDay for the current day of the week
            menu_day = MenuDay(
                menu=new_menu,
                day_of_week=day,
                breakfast_id=breakfast_id,
                lunch_id=lunch_id,
                dinner_id=dinner_id
            )
            session.add(menu_day)  # Add MenuDay to the session
        
        session.add(new_menu)  # Add Menu to the session
        session.commit()  # Commit all changes
        session.close()  # Close the session
        
        flash('Menu added successfully!', 'success')
        return redirect(url_for('menu_bp.view_menus'))  # Redirect to menu view page

    # GET request: Fetch all meals to display in the form
    session = Session()
    meals = session.query(Meal).all()  # Query all meals available
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

                # Validate meal IDs exist
                breakfast = session.get(Meal, breakfast_id)
                lunch = session.get(Meal, lunch_id)
                dinner = session.get(Meal, dinner_id)

                if not breakfast or not lunch or not dinner:
                    session.close()
                    flash(f'Invalid meal selection for {day.capitalize()}.', 'error')
                    return redirect(url_for('menu_bp.edit_menu', id=id))

                # Update MenuDay with new values
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
        # Delete the associated MenuDays first to avoid foreign key constraint errors
        session.query(MenuDay).filter_by(menu_id=id).delete()

        # Now delete the Menu itself
        session.delete(menu)

        session.commit()
        session.close()

        flash('Menu deleted successfully!', 'success')
    except Exception as e:
        session.rollback()  # Rollback in case of any error
        session.close()
        flash(f'Error deleting menu: {str(e)}', 'error')

    return redirect(url_for('menu_bp.view_menus'))
