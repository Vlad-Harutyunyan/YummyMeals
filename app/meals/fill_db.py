# from scripts.api import meals, ingredient, categories, meal_ingredient, area
import sys
sys.path.append(".")
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey ,create_engine
from sqlalchemy.orm import sessionmaker , relationship
import os
from .scripts.api import thisfolder
from ast import literal_eval
from flask import Flask ,Blueprint ,redirect ,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .models import Area,Meal_ingredient, Ingredient, Meal, Category
from .. import db


def read_from_txt(file_name,list_name):
    with open(file_name, 'r', encoding='raw_unicode_escape') as fd:
        mylist = []
        for line in fd:
            mylist.append(literal_eval(line))
    print(f'---------{list_name}----------')
    return (mylist)

meals=read_from_txt(f"{thisfolder}/final_lists/meals.txt",'meals')
print(meals)
ingredient=read_from_txt(f"{thisfolder}/final_lists/ingredient.txt",'ingredient')
print(ingredient)
meal_ingredient=read_from_txt(f"{thisfolder}/final_lists/meal_ingredient.txt",'meal_ingredient')
print(meal_ingredient)
categories=read_from_txt(f"{thisfolder}/final_lists/categories.txt",'categories')
print(categories)
area=read_from_txt(f"{thisfolder}/final_lists/area.txt",'area')
print(area)




def fill_areas_to_db() :
    db.session.query(Area).delete()
    db.session.commit()
    for i in area:
        a = Area(name=i[1])
        db.session.add(a)
        db.session.commit()


def fill_categories_to_db():
    db.session.query(Category).delete()
    db.session.commit()
    for i in categories:
        a = Category(name=i[1], img_link=i[2],description=i[3])
        db.session.add(a)
        db.session.commit()

def fill_ingredients_to_db():
    db.session.query(Ingredient).delete()
    db.session.commit()
    for i in ingredient:
        a = Ingredient(name=i[1],description=i[2])
        db.session.add(a)
        db.session.commit()


def fill_meals_to_db():
    db.session.query(meal).delete()
    db.session.commit()
    for i in meals:
        a = Meal(name=i[1], category_id=i[2], area_id=i[3], instructions=i[5], img_link=i[6], tags=i[7],
                 video_link=i[8])
        db.session.add(a)
        db.session.commit()

def fill_meal_ingredient_to_db():
    db.session.query(Meal_ingredient).delete()
    db.session.commit()
    for i in meal_ingredient:
        a = Meal_ingredient(meal_id=i[0],ingredient_id=i[1])
        db.session.add(a)
        db.session.commit()






def fill_all():
    fill_areas_to_db()
    fill_meal_ingredient_to_db()
    fill_categories_to_db()
    fill_ingredients_to_db()
    fill_meals_to_db()
    print('All done successfuly!')
#
#
# fill_all()
# delete_Area_data()