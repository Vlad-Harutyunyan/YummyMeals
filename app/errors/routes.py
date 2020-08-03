import os

from flask import (
    Blueprint,
    url_for,
    redirect,
    render_template
)

satatic_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static'))

errors_bp = Blueprint(
    'errors',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/',
    static_url_path=satatic_path
)


@errors_bp.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404
