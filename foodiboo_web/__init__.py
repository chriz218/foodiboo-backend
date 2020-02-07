from app import app
from flask import render_template
from foodiboo_web.blueprints.users.views import users_blueprint
from foodiboo_web.blueprints.food_dishes.views import food_dishes_blueprint
from foodiboo_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

# Blueprints
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(food_dishes_blueprint, url_prefix="/food_dishes")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    return render_template('home.html')
