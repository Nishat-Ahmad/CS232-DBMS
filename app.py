from flask import Flask, render_template, request, redirect, url_for
from main import User, WeeklyMenu, MealInstance, Attendance, Billing, Inventory, Session  # Import User model and Session from models.py

# Initialize Flask app
app = Flask(__name__)

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to view all users
@app.route('/view_users')
def view_users():
    session = Session()  # Create a new session
    users = session.query(User).all()  # Query all users
    session.close()  # Close the session
    return render_template('view_users.html', users=users)

# Route to add a user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        
        # Create new user and add to the database
        session = Session()
        new_user = User(email=email, role=role, password=password)
        session.add(new_user)
        session.commit()
        session.close()

        return redirect(url_for('view_users'))

    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
