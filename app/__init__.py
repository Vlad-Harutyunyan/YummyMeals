from gevent import monkey
monkey.patch_all()

import os
from datetime import datetime

from flask import Flask, Blueprint, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from flask_admin import Admin
from flask_socketio import SocketIO

from app.config import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()
admin = Admin(name='Admin_panel', template_mode='bootstrap3')
socketio = SocketIO(async_mode='gevent', always_connect=True)


def create_app(debug=False, port=5010):
    """Construct the  core app object."""

    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = debug
    app.port = port
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

# Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    migrate.init_app(app, db)
    socketio.init_app(app)

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
        
    @app.template_filter('correctLink')
    def correctLink(url):
        url = 'https://www.youtube.com/watch?v=UIcuiU1kV8I'
        p = url.split('watch')[1].split('v=')[1]
        res = f"https://www.youtube.com/embed/{p}"
        return res
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


# admin panel

    with app.app_context():

        from .users.routes import users_bp
        from .index.routes import index_bp
        from .meals.routes import meals_bp
        from .errors.routes import errors_bp
        from .mail.routes import mail_bp


# admin panel register
        from .admin_panel.routes import AdminIndexPage, adm
        admin.init_app(app, index_view=AdminIndexPage(
            name='Main',
            url='/admin/',
            ))


# Register Blueprints
        app.register_blueprint(errors_bp)
        app.register_blueprint(index_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(meals_bp)
        app.register_blueprint(mail_bp)
        app.register_blueprint(adm)

        db.create_all()
        return app
