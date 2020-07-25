from flask import Flask ,Blueprint ,redirect ,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():
    """Construct the core app object."""
   
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "not_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'


    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    migrate.init_app(app, db)

    #handle login_requerd for blueprint
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/user/login')
    
    @app.template_filter('formatdatetime')
    def format_datetime(value, format="%d %b %Y %I:%M %p"):
        """Format a date time to (Default): d Mon YYYY HH:MM P"""
        if value is None:
            return ""
        return value.strftime(format)

        
    with app.app_context():
        from .users.routes import users_bp
        from .index.routes import index_bp
        from .meals.routes import meals_bp
        from .errors.routes import errors_bp

        # Register Blueprints
        app.register_blueprint(errors_bp)
        app.register_blueprint(index_bp) 
        app.register_blueprint(users_bp)
        app.register_blueprint(meals_bp)

        db.create_all()

        return app