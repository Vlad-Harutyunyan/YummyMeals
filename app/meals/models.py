from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from .. import db


class Area(db.Model):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"Area '{self.name}','{self.id}' "


class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    img_link = Column(String)
    description = Column(String)

    def __repr__(self):
        return f"Category '{self.name}','{self.description}' "


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return f"Ingredient '{self.name} , {self.description}'  "


class Meal_ingredient(db.Model):
    __tablename__ = 'meal_ingredient'

    id = Column(Integer, primary_key=True)
    by_user = Column(Integer, default=0)
    meal_id = Column(String, ForeignKey('meal.id'))
    ingredient_id = Column(String, ForeignKey('ingredient.id'))
    meal = relationship("Meal")
    ingredient = relationship("Ingredient")

    def __repr__(self):
        return f"Meal ingr '{self.meal.name}', '{self.ingredient.name}' "


class Meal(db.Model):
    __tablename__ = 'meal'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    area_id = Column(Integer, ForeignKey('area.id'))
    author_id = Column(Integer, ForeignKey('user.id'), default=1)
    instructions = Column(String)
    img_link = Column(String, default='default.jpg')
    tags = Column(String)
    video_link = Column(String)
    date_posted = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    area = relationship("Area")
    category = relationship("Category")
    user = relationship("User")

    def __repr__(self):
        return f"Meal '{self.id}', '{self.name}', '{self.user.username}'," \
               f"'{self.date_posted}'"


path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", ".."))
