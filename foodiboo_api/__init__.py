from app import app
from flask_cors import CORS

cors = CORS(app, support_credentials=True, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from foodiboo_api.blueprints.users.views import users_api_blueprint
from foodiboo_api.blueprints.food_dishes.views import food_dishes_api_blueprint
from foodiboo_api.blueprints.sessions.views import sessions_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(food_dishes_api_blueprint, url_prefix='/api/v1/food_dishes')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/sessions')
