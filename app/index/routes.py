import os
import random
from operator import itemgetter
from flask import (
    Flask,
    g,
    url_for,
    redirect,
    render_template,
    Blueprint
)
from flask_login import current_user
from sqlalchemy import func, desc, and_, select
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
    mydict = {}
    for record in User_Favorite.query.all():
        mydict[record.meal_id] = len(User_Favorite.query.
                                     filter_by(meal_id=record.meal_id).all())
    print(mydict)
    res = dict(sorted(mydict.items(), key=itemgetter(1), reverse=True)[:5])
    print(list(res.keys()))
    tops = Meal.query.filter(Meal.id.in_(list(res.keys()))).all()
    tops = sorted(tops, key=lambda o: list(res.keys()).index(o.id))
    return render_template('index_page.html', tops=tops)
