import os
import random

from flask import (
    Flask,
    g,
    url_for,
    redirect,
    render_template,
    Blueprint
)
from flask_login import current_user
from sqlalchemy import func, desc, and_ , select

from .. import db
from ..meals.models import Meal
from ..users.models import UserComments, User_Favorite, User

static_path = os.path.abspath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static'))

index_bp = Blueprint(
    'index',
    __name__,
    template_folder='templates',
    url_prefix='/',
    static_folder='static',
    static_url_path=static_path
)


@index_bp.route('/')
def index():
    tops = db.session.query(Meal).order_by(func.random()).limit(5).all()
    
    return render_template('index_page.html',tops=tops) 
