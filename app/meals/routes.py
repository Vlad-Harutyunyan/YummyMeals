import os
import re

from flask import (
    Blueprint,
    url_for,
    redirect,
    render_template, request, flash
)

from flask_paginate import Pagination, get_page_parameter
from flask_login import login_required
from flask_mail import Mail, Message
from flask_login import current_user

from .models import Meal, Ingredient, Category, Area, Meal_ingredient
from .. import db
from ..users.models import User_Favorite, User_Favorite_Category, User
from .lib.funct import name_correct
from ..users.forms import CommentForm
from ..users.models import UserComments

stat_path = os.path.abspath(os.path.join(
os.path.dirname(
os.path.abspath(__file__)),
'static'))

meals_bp = Blueprint(
    'meals',
    __name__,
    template_folder='templates',
    url_prefix='/meal',
    static_folder='static',
    static_url_path=stat_path
)

def get_fav_catgories(category_id):
    check = db.session.query(User_Favorite_Category).filter(
        User_Favorite_Category.category_id.like(category_id),
        User_Favorite_Category.user_id.like(current_user.id)).first()
    return check


@meals_bp.route('/')
def test_route():
    page = request.args.get('page', 1, type=int)
    meallist = Meal.query.paginate(page, 6, False)
    next_url = url_for('meals.test_route', page=meallist.next_num) \
        if meallist.has_next else None
    prev_url = url_for('meals.test_route', page=meallist.prev_num) \
        if meallist.has_prev else None

    return render_template(

        'main_page.html',
        meallist=meallist,
        next_url=next_url,
        prev_url=prev_url,

    )


@meals_bp.route('/categories')
def categories_list():
    categories = Category.query.all()
    checker = db.session.query(Category).join(User_Favorite_Category).filter_by(user_id = current_user.id).all() 
    return render_template('category_list.html', categories=categories , checker = checker)
  

@meals_bp.route('/search_by_fullname/<meal_name>/')
def meal_search_by_fullname(meal_name):
    meal_name = name_correct(meal_name)
    meal = Meal.query.filter_by(name=meal_name).first()
    if meal:
        form = CommentForm()
        check = False
        page = request.args.get('page', 1, type=int)
        comments = UserComments.query.filter(UserComments.meal_id == meal.id).paginate(per_page=2, page=page)
        ingredients = Meal_ingredient.query.filter_by(meal_id=meal.id).all()
        return render_template('meal_info.html', meal=meal, ingredients=ingredients,
                           form=form,check = check,comments=comments,page=page)
    else:
        return redirect('/meal')


@meals_bp.route('/search/')
def meal_search():
    meal_name =  request.args.get('meal_name')
    page = request.args.get('page', 1, type=int)
    meallist = db.session.query(Meal).filter(Meal.name.contains(meal_name.lower())).paginate(page, 6, False)
    if meallist:
        next_url = url_for('meals.test_route', page=meallist.next_num) \
            if meallist.has_next else None
        prev_url = url_for('meals.test_route', page=meallist.prev_num) \
            if meallist.has_prev else None

        return render_template(
        'main_page.html',
        meallist=meallist,
        next_url=next_url,
        prev_url=prev_url,
    )
    else:
        return redirect('/meal')

@meals_bp.route('/search_by_username/')
def meal_search_by_username():
    u_name =  request.args.get('srch_user_username')
    page = request.args.get('page', 1, type=int)
    meallist = None 
    if isinstance(u_name,str) and not u_name.isdecimal():
        meallist = db.session.query(Meal).join(User).filter(User.username.contains(u_name.lower())).paginate(page, 6, False)
    elif u_name.isdecimal():
        meallist = db.session.query(Meal).join(User).filter(User.id.like(int(u_name))).paginate(page, 6, False)
    if meallist:    
        next_url = url_for('meals.test_route', page=meallist.next_num) \
            if meallist.has_next else None
        prev_url = url_for('meals.test_route', page=meallist.prev_num) \
            if meallist.has_prev else None
        
        return render_template(
        'main_page.html',
        meallist=meallist,
        next_url=next_url,
        prev_url=prev_url,
    )
    else:
        return redirect('/meal')

@meals_bp.route('/category/<int:c_id>/')
def meals_by_category(c_id):
    page = request.args.get('page', 1, type=int)

    meallist = Meal.query.filter_by(category_id=c_id).paginate(page, 6, False)
    next_url = url_for('meals.meals_by_category', c_id=c_id, page=meallist.next_num) \
        if meallist.has_next else None
    prev_url = url_for('meals.meals_by_category', c_id=c_id, page=meallist.prev_num) \
        if meallist.has_prev else None


    return render_template(

        'main_page.html',
        meallist=meallist,
        next_url=next_url,
        prev_url=prev_url,

    )


@meals_bp.route('/add-favorite/<int:meal_id>', methods=['GET'])
@login_required
def add_favorite(meal_id):
    check = False

    bb = db.session.query(User_Favorite).filter(
        User_Favorite.meal_id.like(meal_id),
        User_Favorite.user_id.like(current_user.id)).first()

    if not bb:
        check = False
        user_favorite = User_Favorite(
            user_id=current_user.id,
            meal_id=meal_id
        )

        db.session.add(user_favorite)
        db.session.commit()
    else:
        check = True
        db.session.delete(bb)
        db.session.commit()
    print(request.referrer)

    if 'meal/meal_info' in request.referrer :
        return redirect(url_for('meals.meal_info', m_id=meal_id))
    else :
        return redirect(url_for('users.users_profiles', u_id=current_user.id))


@meals_bp.route('/meal_info/<int:m_id>/', methods=['GET'])
def meal_info(m_id):
    meal = Meal.query.filter_by(id=m_id).first()
    ingredients = Meal_ingredient.query.filter_by(meal_id=m_id).all()
    form = CommentForm()
    try :
        check = db.session.query(User_Favorite).filter(
            User_Favorite.meal_id.like(m_id),
            User_Favorite.user_id.like(current_user.id)
        ).first()
    except :
        check = False
    page = request.args.get('page', 1, type=int)
    comments = UserComments.query.\
        filter(UserComments.meal_id == m_id).\
        order_by(UserComments.date_posted.desc()).\
        paginate(per_page=2, page=page)
    fav_count = len(db.session.query(User_Favorite).filter(User_Favorite.meal_id.like(m_id)).all())
    return render_template('meal_info.html',
                           meal=meal, ingredients=ingredients, check=check,
                           form=form, comments=comments, page=page, m_id=m_id ,fav_count = fav_count)


@meals_bp.route('/meal_info/<int:m_id>/', methods=['POST'])
@login_required
def meal_info_post(m_id):
    form = CommentForm()
    if form.is_submitted():
        comment = UserComments(content=form.content.data, user_id=current_user.id, meal_id=m_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('meals.meal_info',
                                m_id=m_id))


@meals_bp.route('/add-favorite-category/<int:category_id>', methods=['GET'])
@login_required
def add_favorite_category(category_id):
    # Check = False

    bb = db.session.query(User_Favorite_Category).filter(
        User_Favorite_Category.category_id.like(category_id),
        User_Favorite_Category.user_id.like(current_user.id)).first()

    if not bb:
        check = False
        user_favorite_category = User_Favorite_Category(
            user_id=current_user.id,
            category_id=category_id
        )

        db.session.add(user_favorite_category)
        db.session.commit()
    else:
        check = True
        db.session.delete(bb)
        db.session.commit()

    if 'meal/categories' in request.referrer :
        return redirect(url_for('meals.categories_list'))
    else : 
        return redirect(url_for('users.users_profiles', u_id=current_user.id))
   


@meals_bp.route('/search/<meal_name>/')
def meal_search_name(meal_name):
    if not meal_name in name_correct(meal_name):
        return redirect('/meal')
    else:
        for name1 in name_correct(meal_name):
            meal = Meal.query.filter_by(name=name1).first()
            if meal:
                form = CommentForm()
                check = False
                page = request.args.get('page', 1, type=int)
                comments = UserComments.query.filter(UserComments.meal_id == meal.id).paginate(per_page=2, page=page)
                ingredients = Meal_ingredient.query.filter_by(meal_id=meal.id).all()
                return redirect(url_for('meals.meal_info',m_id=meal.id))


@meals_bp.route('/ingredient/<int:ing_id>/')
@login_required
def ingr_info(ing_id):
    ingredient = Ingredient.query.filter_by(id=int(ing_id)).first()
    return render_template('ingredient_info.html', name=ingredient.name, description=ingredient.description )
            
            
