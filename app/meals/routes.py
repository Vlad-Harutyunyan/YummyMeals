import os
from flask import (
    Blueprint,
    url_for,
    redirect,
    render_template, request
)

from flask_login import login_required
from flask_login import current_user

from .models import Meal, Ingredient, Category, Area, Meal_ingredient
from .. import db
from ..users.models import User_Favorite, User_Favorite_Category, User
from ..users.forms import CommentForm
from ..users.models import UserComments, UserActivities

static_path = os.path.abspath(
    os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)), 'static'))

meals_bp = Blueprint(
    'meals',
    __name__,
    template_folder='templates',
    url_prefix='/meal',
    static_folder='static',
    static_url_path=static_path
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
    checker = None

    if current_user.is_authenticated:
        checker = db.session.query(Category). \
            join(User_Favorite_Category). \
            filter_by(user_id=current_user.id).all()

    return render_template(
        'category_list.html',
        categories=categories,
        checker=checker)


@meals_bp.route('/areas')
def areas_list():
    areas = Area.query.all()
    return render_template(
        'areas_list.html',
        areas=areas)


@meals_bp.route('/search/')
def meal_search():
    meal_name = request.args.get('meal_name')
    page = request.args.get('page', 1, type=int)
    meallist = db.session.query(Meal).filter(
        Meal.name.contains(meal_name.lower())) \
        .paginate(page, 6, False)
    if meallist:
        next_url = url_for('meals.test_route', page=meallist.next_num) \
            if meallist.has_next else None
        prev_url = url_for('meals.test_route', page=meallist.prev_num) \
            if meallist.has_prev else None

        return render_template(
            'main_page.html',
            meallist=meallist,
            next_url=next_url,
            prev_url=prev_url, )
    else:
        return redirect('/meal')


@meals_bp.route('/search_by_username/')
def meal_search_by_username():
    u_name = request.args.get('srch_user_username')
    page = request.args.get('page', 1, type=int)
    meallist = None
    if isinstance(u_name, str) and not u_name.isdecimal():
        meallist = db.session.query(Meal) \
            .join(User).filter(User.username.contains(u_name.lower())) \
            .paginate(page, 6, False)
    elif u_name.isdecimal():
        meallist = db.session.query(Meal) \
            .join(User).filter(User.id.like(int(u_name))) \
            .paginate(page, 6, False)
    if meallist:
        next_url = url_for('meals.test_route', page=meallist.next_num) \
            if meallist.has_next else None
        prev_url = url_for('meals.test_route', page=meallist.prev_num) \
            if meallist.has_prev else None
        return render_template(
            'main_page.html',
            meallist=meallist,
            next_url=next_url,
            prev_url=prev_url)
    else:
        return redirect('/meal')


@meals_bp.route('/areas/<int:a_id>/')
def meals_by_countries(a_id: int):
    page = request.args.get('page', 1, type=int)

    meallist = Meal.query.filter_by(area_id=a_id).paginate(page, 6, False)
    next_url = url_for(
        'meals.meals_by_countries',
        a_id=a_id,
        page=meallist.next_num) \
        if meallist.has_next else None
    prev_url = url_for(
        'meals.meals_by_countries',
        a_id=a_id,
        page=meallist.prev_num) \
        if meallist.has_prev else None

    return render_template(
        'main_page.html',
        meallist=meallist,
        next_url=next_url,
        prev_url=prev_url,

    )


@meals_bp.route('/category/<int:c_id>/')
def meals_by_category(c_id):
    page = request.args.get('page', 1, type=int)

    meallist = Meal.query.filter_by(category_id=c_id).paginate(page, 6, False)
    next_url = url_for(
        'meals.meals_by_category',
        c_id=c_id,
        page=meallist.next_num) \
        if meallist.has_next else None
    prev_url = url_for(
        'meals.meals_by_category',
        c_id=c_id,
        page=meallist.prev_num) \
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
    bb = db.session.query(User_Favorite).filter(
        User_Favorite.meal_id.like(meal_id),
        User_Favorite.user_id.like(current_user.id)).first()

    # User Activity
    user_activity = UserActivities.query.filter_by(
        user_id=current_user.id).first()

    if not bb:
        check = False
        user_favorite = User_Favorite(
            user_id=current_user.id,
            meal_id=meal_id
        )

        db.session.add(user_favorite)

        # User Activity +
        user_activity.favorite_meals += 1
    else:
        check = True
        db.session.delete(bb)

        # User Activity -
        user_activity.favorite_meals -= 1

    db.session.commit()
    print(request.referrer)

    if 'meal/meal_info' in request.referrer:
        return redirect(url_for('meals.meal_info', m_id=meal_id, check=check))
    else:
        return redirect(url_for('users.users_profiles', u_id=current_user.id))


@meals_bp.route('/meal_info/<int:m_id>/', methods=['GET'])
def meal_info(m_id):
    meal = Meal.query.filter_by(id=m_id).first()
    ingredients = Meal_ingredient.query.filter_by(meal_id=m_id).all()
    form = CommentForm()
    try:
        check = db.session.query(User_Favorite).filter(
            User_Favorite.meal_id.like(m_id),
            User_Favorite.user_id.like(current_user.id)
        ).first()
    except:
        check = False
    page = request.args.get('page', 1, type=int)
    comments = UserComments.query. \
        filter(UserComments.meal_id == m_id). \
        order_by(UserComments.date_posted.desc()). \
        paginate(per_page=2, page=page)
    fav_count = len(db.session.query(User_Favorite).filter(
        User_Favorite.meal_id.like(m_id)).all())
    return render_template('meal_info.html',
                           meal=meal, ingredients=ingredients, check=check,
                           form=form, comments=comments, page=page,
                           m_id=m_id, fav_count=fav_count)


@meals_bp.route('/meal_info/<int:m_id>/', methods=['POST'])
@login_required
def meal_info_post(m_id):
    form = CommentForm()
    if form.is_submitted():
        comment = UserComments(
            content=form.content.data,
            user_id=current_user.id,
            meal_id=m_id)
        db.session.add(comment)

        # User Activity
        user_activity = UserActivities.query.filter_by(
            user_id=current_user.id).first()
        user_activity.comments += 1

        db.session.commit()
        return redirect(url_for('meals.meal_info',
                                m_id=m_id))


@meals_bp.route('/add-favorite-category/<int:category_id>', methods=['GET'])
@login_required
def add_favorite_category(category_id):
    bb = db.session.query(User_Favorite_Category).filter(
        User_Favorite_Category.category_id.like(category_id),
        User_Favorite_Category.user_id.like(current_user.id)).first()

    # User Activity
    user_activity = UserActivities.query.filter_by(
        user_id=current_user.id).first()

    if not bb:
        user_favorite_category = User_Favorite_Category(
            user_id=current_user.id,
            category_id=category_id
        )

        db.session.add(user_favorite_category)

        # User Activity +
        user_activity.favorite_categories += 1
    else:
        db.session.delete(bb)

        # User Activity -
        user_activity.favorite_categories -= 1

    db.session.commit()

    if 'meal/categories' in request.referrer:
        return redirect(url_for('meals.categories_list'))
    else:
        return redirect(url_for('users.users_profiles', u_id=current_user.id))


@meals_bp.route('/search/<meal_name>/')
@login_required
def meal_search_name(meal_name):
    meal = Meal.query.filter(Meal.name.contains(str(meal_name).lower())). \
        first()
    if meal:
        return redirect(url_for('meals.meal_info', m_id=meal.id))
    else:
        return redirect('/meal')


@meals_bp.route('/ingredient/<int:ing_id>/')
@login_required
def ingr_info(ing_id):
    ingredient = Ingredient.query.filter_by(id=int(ing_id)).first()
    return render_template(
        'ingredient_info.html',
        name=ingredient.name,
        description=ingredient.description)


@meals_bp.route('/search_by_ingredient/')
def meal_search_by_ingredient():
    i_name = request.args.get('srch_ingredient')
    page = request.args.get('page', 1, type=int)
    meallist = None
    if isinstance(i_name, str) and not i_name.isdecimal():
        ing_dict = {}
        for i in list(i_name.split(",")):
            meal_ing = db.session.query(Meal_ingredient).join(Ingredient). \
                filter(Ingredient.name.contains(i.strip())).all()
            mylist = []
            for j in meal_ing:
                mylist.append(j.meal.name)
            ing_dict[i] = mylist
        res = list(set.intersection(*map(set, list(ing_dict.values()))))
        meallist = Meal.query.filter(Meal.name.in_(res)).paginate(page, 15,
                                                                  False)

    next_url = url_for('meals.meal_search_by_ingredient',
                       page=meallist.next_num, srch_ingredient=i_name) \
        if meallist.has_next else None
    prev_url = url_for('meals.meal_search_by_ingredient',
                       page=meallist.prev_num, srch_ingredient=i_name) \
        if meallist.has_prev else None

    return render_template(
        'main_page.html',
        meallist=meallist,
        next_url=next_url,
        prev_url=prev_url
    )
