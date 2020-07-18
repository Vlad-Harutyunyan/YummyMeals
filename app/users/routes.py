from flask import render_template, url_for, redirect, flash, request ,Blueprint
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from .models import User, Post
from flask_login import login_user, current_user, logout_user, login_required 
from .. import bcrypt
from .. import db
import os
satatic_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'static' ))

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


@users_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html',
                           title='Account', image_file=image_file, form=form)
