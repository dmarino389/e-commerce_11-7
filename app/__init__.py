from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Application Factory
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions with app instance
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
