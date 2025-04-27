from flask import Flask, render_template
from routes.user_routes import user_bp
from routes.meal_routes import meal_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = 'oogs'

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(meal_bp)
app.register_blueprint(auth_bp)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

