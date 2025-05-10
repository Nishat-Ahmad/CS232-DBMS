from flask import Flask, render_template, g
from flask import session
from database import models

from routes.user_routes import user_bp
from routes.meal_routes import meal_bp
from routes.auth_routes import auth_bp
from routes.complaint_routes import complaint_bp
from routes.menu_routes import menu_bp
from routes.notification_routes import notification_bp
from routes.attendance_routes import attendance_bp
from routes.billing_routes import billing_bp

app = Flask(__name__)
app.secret_key = 'oogs'

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(meal_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(complaint_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(billing_bp)

# Load user from session before each request
@app.before_request
def load_user():
    if 'user_id' in session:
        user_id = session['user_id']
        db_session = models.Session()  # Use the Session from models
        user = db_session.query(models.User).get(user_id)  # Use User from models
        g.user = user  # Store user in g for easy access across views
        db_session.close()
    else:
        g.user = None  # No user logged in

# Routes
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
