from flask import (render_template, url_for, redirect,
                   flash, request, Blueprint, abort)
from .forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                    CommentForm, RequestResetForm, ResetPasswordForm , SupportForm)
from .models import User, User_Favorite ,UserComments ,Support_Message , User_Favorite_Category
from flask_login import login_user, current_user, logout_user, login_required
from .. import bcrypt, mail, db
import os
from PIL import Image
import secrets
from ..meals.models import Meal , Ingredient , Category , Area , Meal_ingredient 
from .scripts.logic import sort_ingrs_by_alphabet
from datetime import datetime
from flask_mail import Message


satatic_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

users_bp = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    url_prefix='/user',
    static_folder='static',
    static_url_path=satatic_path
)
  

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html',
                           title='Register', form=form)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nest_page = request.args.get('next')
            return redirect(nest_page) if nest_page else redirect(url_for('index.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',
                           title='Login', form=form)


@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


def save_prof_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(users_bp.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@users_bp.route('/account', methods=['POST'])
@login_required
def account_post():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        data_not_changed = (current_user.username != form.username.data)
        if not data_not_changed and not form.picture.data:
            flash("No changes", 'success')
        else:
            if data_not_changed:
                current_user.username = form.username.data
                current_user.email = form.email.data
            elif form.picture.data:
                picture_file = save_prof_picture(form.picture.data)
                current_user.image_file = picture_file
            db.session.commit()
            flash("Your account has been updated", 'success')
        return redirect(url_for('users.account_get'))

    return redirect(url_for('users.account_get'))


@users_bp.route('/account', methods=['GET'])
@login_required
def account_get():
    form = UpdateAccountForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    image_file = url_for('users.static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html',
                           title='Account', image_file=image_file, form=form)

@users_bp.route('/new_recipe', methods=["GET"])
@login_required
def new_recipe_get():
    context = { 
        'ingr' : Ingredient.query.all(),
        'areas' : Area.query.all(),
        'categ' : Category.query.all(),
    }
    alphabetic_sorted_ingrs = sort_ingrs_by_alphabet(context['ingr'])
    return render_template('new_recipe.html',
                           title='New Post', legend='New Post' , context = context, alp = alphabetic_sorted_ingrs )


@users_bp.route('/new_recipe', methods=["POST"])
@login_required
def new_recipe_post():
    context = { 
        'ingr' : Ingredient.query.all(),
        'areas' : Area.query.all(),
        'categ' : Category.query.all(),
    }

    alphabetic_sorted_ingrs = sort_ingrs_by_alphabet(context['ingr'])
    
    meal_info = {
           'name': request.form.get('title'),
           'inctruction': request.form.get('content'),
           'country':request.form.get('area'),
           'category':request.form.get('category'),
           'ingredients':request.form.getlist('ingredients'),
       }

    #validate data
    if meal_info['name'] and meal_info['inctruction'] and \
        meal_info['country'] and meal_info['category'] and \
        meal_info ['ingredients'] :
        
        meal = Meal(
            id = Meal.query.order_by(Meal.id.desc()).first().id+1, #get last meal id in db
            name = meal_info['name'],
            category_id =  Category.query.filter_by(name=meal_info['category']).first().id,
            area_id =  Area.query.filter_by(name=meal_info['country']).first().id,
            author_id = current_user.id,
            instructions = meal_info['inctruction'],
            tags = None,
            video_link = None,
        )
        db.session.add(meal)
        
        for x in meal_info['ingredients']  :
            print(meal_info['ingredients'])
            meal_ingr = Meal_ingredient( by_user = 1 , meal_id = meal.id ,ingredient_id = Ingredient.query.filter_by(name = x).first().id)
            db.session.add(meal_ingr)
            db.session.commit()    
            
        db.session.commit()  
        return redirect(url_for('meals.meal_info', m_id = meal.id))

    else:
        error = 'Please fill all Fields '
        return render_template('new_recipe.html',
            title='New Post', legend='New Post' , context = context ,
            error = error , alp = alphabetic_sorted_ingrs)
    return render_template('new_recipe.html',
                           title='New Post', legend='New Post' , context = context, alp = alphabet_sort_ingrs)


@users_bp.route('/favourites', methods=['GET'])
@login_required
def favourites():
    return render_template('favourites.html')


@users_bp.route('/user_profile/<int:u_id>', methods=['GET'])
def users_profiles(u_id) :
    user = db.session.query(User).filter(User.id.like(u_id)).first()
    user_favorite_meals = db.session.query(User_Favorite).filter(User_Favorite.user_id.like(u_id)).all()
    user_meals = db.session.query(Meal).filter(Meal.author_id.like(u_id)).all()
    comments = db.session.query(UserComments).filter(UserComments.user_id.like(u_id)).all()
    favorite_categories = db.session.query(User_Favorite_Category).filter(User_Favorite_Category.user_id.like(u_id)).all()  

    return render_template(
        'user_profile.html' , 
        user = user ,
        ufm = user_favorite_meals ,
        ufc = favorite_categories ,
        user_meals = user_meals ,
        comments = comments )


@users_bp.route('/remove_meal/<int:m_id>/<int:u_id>', methods=['GET'])
def remove_meal(m_id,u_id) :
    meal = db.session.query(Meal).filter(Meal.id.like(m_id)).first()
    if meal.author_id == current_user.id :
        db.session.delete(meal)  
        db.session.commit()
        return redirect(url_for('users.users_profiles' , u_id = u_id))
    else :
        return 'You can not delete another user recipe'


@users_bp.route('/<string:username>/comments')
def user_comments(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    comments = UserComments.query \
        .filter_by(author=user) \
        .order_by(UserComments.date_posted.desc()) \
        .paginate(page=page, per_page=2)
    return redirect(url_for('users.comments',
                            user_id=user.id, comments=comments))


@users_bp.route('/<int:user_id>/comments')
def comments(user_id):
    comments = UserComments.query.\
        filter_by(user_id=user_id).\
        order_by(UserComments.date_posted.desc()).all()
    return render_template('comments.html',
                           user_id=user_id, comments=comments)


@users_bp.route("/update/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    comment = UserComments.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = CommentForm()
    if form.is_submitted():
        comment.content = form.content.data
        comment.date_posted = datetime.utcnow()
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('meals.meal_info', m_id=comment.meal_id))
    elif request.method == "GET":
        form.content.data = comment.content

    return render_template('update_comment.html', form=form, legend="Update Comment")


@users_bp.route("/delete/<int:comment_id>", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = UserComments.query.get_or_404(comment_id)
    m_id = comment.meal_id
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('meals.meal_info', m_id=m_id))

 

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@users_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           title='Reset Password', form=form)


@users_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           title='Reset Password', form=form)


@users_bp.route("/support", methods=['GET'])
@login_required
def support_get():
    form = SupportForm()
    return render_template('support_msg.html' ,form = form)

@users_bp.route("/support", methods=['POST'])
@login_required
def support_post():
    form = SupportForm()
    if form.validate_on_submit():
        s = Support_Message(user_id = current_user.id , content = form.content.data)
        db.session.add(s)
        db.session.commit()
        
        flash(' [Success] Your message send to admin ! ' , 'success')

    return redirect(url_for('users.support_get'))




