import os
import threading as t

from ..meals.models import Meal_ingredient, Meal, Category, Area, Ingredient
from .admin_thread import FlaskThread
from ..mail.routes import mail_send
from ..meals.fill_db import fill_all
from .. import admin, db
from ..users.models import User, UserComments, User_Favorite,\
    User_Favorite_Category, Support_Message

from flask import render_template, Blueprint, abort,\
    redirect, flash, current_app, request
from flask_paginate import Pagination, get_page_parameter
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import expose, AdminIndexView


static_path = os.path.abspath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static'))

adm = Blueprint(
    'adm', __name__, template_folder='templates', url_prefix='/admin')

MAX_QSIZE = 5
BUFF_SIZE = 5


class AdminIndexPage(AdminIndexView):
    @expose('/')
    def index(self):

        page = request.args.get('page', 1, type=int)
        users_msgs = db.session.query(Support_Message)\
            .filter(Support_Message.adm_checked.is_(False))\
            .order_by(Support_Message.date_posted.desc()).\
            paginate(per_page=5, page=page)

        return self.render(
            'admin/index_page.html', users_msgs=users_msgs, page=page)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class IndexView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


@adm.route('/send_mails')
def send_mails():
    if (current_user.is_authenticated and
            current_user.is_admin):

            FlaskThread(target=mail_send).start()
            flash('Your request in progress . . . ', 'info')

            return redirect('/admin')
    return abort(403)


@adm.route('/update_db')
def update_db():
    if (current_user.is_authenticated and
            current_user.is_admin):

            FlaskThread(target=fill_all).start()
            flash('Your request in progress . . . ', 'info')

            return redirect('/admin')
    return abort(403)


# adding views
admin.add_views(IndexView(User, db.session))
admin.add_views(IndexView(UserComments, db.session))
admin.add_views(IndexView(User_Favorite, db.session))
admin.add_views(IndexView(User_Favorite_Category, db.session))
admin.add_views(IndexView(Meal, db.session))
admin.add_views(IndexView(Category, db.session))
admin.add_views(IndexView(Area, db.session))
admin.add_views(IndexView(Ingredient, db.session))
admin.add_views(IndexView(Meal_ingredient, db.session))
admin.add_views(IndexView(Support_Message, db.session))
