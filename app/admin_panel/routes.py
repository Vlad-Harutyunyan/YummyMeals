from flask_admin.contrib.sqla import ModelView
from .. import admin ,db
from ..users.models import User , UserComments ,User_Favorite , User_Favorite_Category
from ..meals.models import Meal_ingredient , Meal  , Category , Area , Ingredient
from flask_login import current_user
from flask_admin import expose,AdminIndexView
import os
from flask import render_template

template_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))




class AdminIndexPage(AdminIndexView) :
    # @expose('/')
    # def index(self):
    #     arg1 = 'Hello'
    #     return self.render('admin/admin_home.html', arg1=arg1)
    #this part in development 
    
    def is_accessible(self):
        return (current_user.is_authenticated and 
            current_user.is_admin)
    

class IndexView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and 
            current_user.is_admin)

            

            #adding views
admin.add_views(IndexView(User,db.session))     
admin.add_views(IndexView(UserComments,db.session))     
admin.add_views(IndexView(User_Favorite,db.session))     
admin.add_views(IndexView(User_Favorite_Category,db.session))     
admin.add_views(IndexView(Meal,db.session))     
admin.add_views(IndexView(Category,db.session))     
admin.add_views(IndexView(Area,db.session))     
admin.add_views(IndexView(Ingredient,db.session))       
admin.add_views(IndexView(Meal_ingredient,db.session))     




