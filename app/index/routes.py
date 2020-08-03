import os

from flask import (
    Flask,
    g,
    url_for,
    redirect,
    render_template,
    Blueprint
)
from flask_login import current_user

satatic_path = os.path.abspath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static'))

index_bp = Blueprint(
    'index',
    __name__,
    template_folder='templates',
    url_prefix='/',
    static_folder='static',
    static_url_path=satatic_path
)


@index_bp.route('/')
def index():
    return render_template('index.html')
