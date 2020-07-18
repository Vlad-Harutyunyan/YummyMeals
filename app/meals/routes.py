from flask import (
    Blueprint,
    url_for,
    redirect,
    render_template
)

import os
satatic_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'static' ))
from .models import Meal ,Ingredient , Category , Area , Meal_ingredient
from .. import db


meals_bp = Blueprint(
    'meals',
    __name__,
    template_folder='templates',
    url_prefix='/meal',
    static_folder='static',
    static_url_path=satatic_path
)


# @meals_bp.route('/fill_db')
# def fill_db():
#     from .models import fill_all
#     fill_all()
#     return 'done'
    

@meals_bp.route('/')
def test_route():
    meallist = Meal.query.all()
    return render_template('main_page.html', meallist = meallist)


@meals_bp.route('/meal_info/<int:m_id>/')
def meal_info(m_id):
    meal = Meal.query.filter_by(id=m_id).first()
    ingredients = Meal_ingredient.query.filter_by(meal_id=m_id).all()
    return render_template('meal_info.html', meal = meal,ingredients = ingredients)
