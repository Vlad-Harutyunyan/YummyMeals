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
import re


def name_correct(name):
    matches = re.finditer(" ", name)
    list1 = [match.start() for match in matches]
    name1=name[0]
    for i in range (0,len(name)-1):
        if i in list1:
            name1+=name[i]+name[i+1].upper()
        else:
            name1+=name[i+1].lower()
    name1=name1.replace("  "," ")
    return(name1)


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



@meals_bp.route('/search/<meal_name>/')
def meal_search(meal_name):
    meal_name=name_correct(meal_name)
    meal = Meal.query.filter_by(name=meal_name).first()
    if meal :
        ingredients = Meal_ingredient.query.filter_by(meal_id=meal.id).all()
        return render_template('meal_info.html', meal = meal, ingredients = ingredients)
    else :
        return redirect('/meal')



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

@meals_bp.route('/meal_info/<int:m_id>/')
def meal_info(m_id):
    meal = Meal.query.filter_by(id=m_id).first()

    ingredients = Meal_ingredient.query.filter_by(meal_id=m_id).all()
    return render_template('meal_info.html', meal = meal, ingredients = ingredients)

