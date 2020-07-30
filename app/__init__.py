from flask import Flask, Blueprint, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime
from flask_mail import Mail
from flask_admin import Admin


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
admin = Admin(name='Admin_panel', template_mode='bootstrap3')


def create_app():
    """Construct the core app object."""
    global app, mail

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "not_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'yummymealbook@gmail.com'
    app.config['MAIL_PASSWORD'] = '789456123yummy'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    mail = Mail(app)

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    migrate.init_app(app, db)
    


    # handle login_requerd for blueprint
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/user/login')

    @app.template_filter('formatdatetime')
    def format_datetime(value, format="%d %b %Y %I:%M %p"):
        """Format a date time to (Default): d Mon YYYY HH:MM P"""
        if value is None:
            return ""
        return value.strftime(format)

    @app.template_filter('timeagofilter')
    def humanize_ts(time, timestamp=False):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
        time = int((time - datetime(1970, 1, 1)).total_seconds())
        now = datetime.now()
        diff = now - datetime.fromtimestamp(time)
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(int(second_diff)) + " seconds ago"
            if second_diff < 120:
                return "a minute ago"
            if second_diff < 3600:
                return str(int(second_diff / 60)) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str(int(second_diff / 3600)) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + " days ago"
        if day_diff < 31:
            return str(int(day_diff / 7)) + " weeks ago"
        if day_diff < 365:
            return str(int(day_diff / 30)) + " months ago"
        return str(int(day_diff / 365)) + " years ago"


    #admin panel 




    with app.app_context():
        from .users.routes import users_bp
        from .index.routes import index_bp
        from .meals.routes import meals_bp
        from .errors.routes import errors_bp
        from .mail.routes import mail_bp

        #admin panel register
        from .admin_panel import routes
        from .admin_panel.routes import AdminIndexPage
        admin.init_app(app,index_view=AdminIndexPage(
        name='Home',
        url='/admin/',
        ))


        # Register Blueprints
        app.register_blueprint(errors_bp)
        app.register_blueprint(index_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(meals_bp)
        app.register_blueprint(mail_bp)

        db.create_all()
  
        return app