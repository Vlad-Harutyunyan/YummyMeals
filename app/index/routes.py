import os
from operator import itemgetter
from flask import (
    redirect,
    render_template,
    Blueprint,
    session
)
from flask_login import current_user
from ..meals.models import Meal
from ..users.models import User_Favorite

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
    res = dict(sorted(mydict.items(), key=itemgetter(1), reverse=True)[:5])
    tops = Meal.query.filter(Meal.id.in_(list(res.keys()))).all()
    tops = sorted(tops, key=lambda o: list(res.keys()).index(o.id))

    # chat
    name = 'Guest'
    if current_user.is_authenticated:
        name = current_user.username
    room = 'main_room'

    session['name'] = name
    session['room'] = room
    name = session.get('name', '')
    room = session.get('room', '')

    return render_template(
        'index_page.html',
        tops=tops,
        name=name,
        room=room)


@index_bp.route('/presentation')
def presentation():
    return redirect(
        'https://view.genial.ly/5f2f99770c24590d87b624b9/presentation-yummy-meals')
