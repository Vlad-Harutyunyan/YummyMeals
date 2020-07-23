from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey ,create_engine
from sqlalchemy.orm import sessionmaker, relationship
import os
import json
from .. import db
from ..users.models import User


class Area(db.Model):

    __tablename__ = 'area'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    img_link =  Column(String)
    description = Column(String)

class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
 

class Meal_ingredient(db.Model):
    __tablename__ = 'meal_ingredient'

    id = Column(Integer, primary_key=True)
    by_user = Column(Integer, default = 0 )
    meal_id = Column(String,ForeignKey('meal.id'))
    ingredient_id = Column(String,ForeignKey('ingredient.id'))
    meal = relationship("Meal")
    ingredient = relationship("Ingredient")

class Meal(db.Model):
    __tablename__ = 'meal'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id =  Column(Integer, ForeignKey('category.id'))
    area_id = Column(Integer, ForeignKey('area.id'))
    author_id = Column(Integer, ForeignKey('user.id'), default = 1)
    instructions = Column(String)
    img_link = Column(String , default = 'default.jpg')
    tags = Column(String)
    video_link = Column(String)
    area = relationship("Area")
    category = relationship("Category")
    user = relationship("User")







path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))



