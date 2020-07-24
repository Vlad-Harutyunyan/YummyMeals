from flask import (
    Blueprint,
    url_for,
    redirect,
    render_template ,request
)

import os
satatic_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'static' ))
from .models import Meal ,Ingredient , Category , Area , Meal_ingredient
from .. import db
from flask_paginate import Pagination, get_page_parameter


from ..users.forms import CommentForm
from ..users.models import UserComments
from flask_login import current_user


meals_bp = Blueprint(
    'meals',
    __name__,
    template_folder='templates',
    url_prefix='/meal',
    static_folder='static',
    static_url_path=satatic_path
)


@meals_bp.route('/fill_db')
def fill_db():
    from .fill_db import fill_all
    fill_all()
    return 'done'
    

@meals_bp.route('/')
def test_route():

    page = request.args.get('page', 1, type=int)
    meallist = Meal.query.paginate( page, 6 , False) 
    next_url = url_for('meals.test_route', page=meallist.next_num) \
        if meallist.has_next else None
    prev_url = url_for('meals.test_route', page=meallist.prev_num) \
        if meallist.has_prev else None

    return render_template(

        'main_page.html', 
        meallist = meallist ,
        next_url = next_url, 
        prev_url = prev_url,

    )


@meals_bp.route('/categories')
def categories_list():
    categories = Category.query.all()
    return render_template('category_list.html', categories = categories)


@meals_bp.route('/category/<int:c_id>/')
def meals_by_category(c_id):
    page = request.args.get('page', 1, type=int)

    meallist = Meal.query.filter_by(category_id=c_id).paginate( page, 6 , False) 
    next_url = url_for('meals.meals_by_category', c_id = c_id , page=meallist.next_num) \
        if meallist.has_next else None
    prev_url = url_for('meals.meals_by_category',  c_id = c_id , page=meallist.prev_num) \
        if meallist.has_prev else None

    return render_template(

        'main_page.html', 
        meallist = meallist ,
        next_url = next_url, 
        prev_url = prev_url,
        
    )


@meals_bp.route('/meal_info/<int:m_id>/', methods=['GET'])
def meal_info(m_id):
    meal = Meal.query.filter_by(id=m_id).first()
    ingredients = Meal_ingredient.query.filter_by(meal_id=m_id).all()
    form = CommentForm()
    return render_template('meal_info.html', meal=meal, ingredients=ingredients, form=form)


@meals_bp.route('/meal_info/<int:m_id>/', methods=['POST'])
def meal_info_post(m_id):
    form = CommentForm()
    if form.is_submitted():
        comment = UserComments(content=form.content.data, user_id=current_user.id, meal_id=m_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('meals.meal_info', m_id=m_id))




