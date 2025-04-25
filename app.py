from flask import Flask, render_template, request, redirect, url_for
from routes.user_routes import user_bp
from routes.menu_routes import menu_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(menu_bp)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
