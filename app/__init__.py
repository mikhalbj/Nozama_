from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .carts import bp as cart_bp
    app.register_blueprint(cart_bp)
    from .inventories import bp as inventory_bp
    app.register_blueprint(inventory_bp)
    
    from .accounts import bp as account_bp
    app.register_blueprint(account_bp)

    from .product import bp as prod_bp
    app.register_blueprint(prod_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp)

    from .newReview import bp as newReview_bp
    app.register_blueprint(newReview_bp)

    return app
