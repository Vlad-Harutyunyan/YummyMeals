from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey ,create_engine
from sqlalchemy.orm import sessionmaker , relationship
from .. import db
import os
import json


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
    instructions = Column(String)
    img_link = Column(String)
    tags = Column(String)
    video_link = Column(String)
    area = relationship("Area")
    category = relationship("Category")

path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))

def prep_query(file_name,fields):
    with open (file_name,encoding="utf8") as jf :
        list1  = json.load(jf)
    list_new=[]
    for i in range (len(list1)):
        list_new.append([])
    for j in range (0,len(list1)):
        for k,v in list1[j].items():
            if k in fields:
                list_new[j].append(v)
    return list_new

meals=prep_query(f'{path}/scripts/parsed_meals.json', ("id","name","category_id", "area_id", "like_count", "instructions","img_link", "tags", "video_link"))
# print("meals", meals)
ingredient=prep_query(f'{path}/scripts/ingredients.json',("id","name","description"))
# print("ingredient", ingredient)
meal_ingredient=prep_query(f'{path}/scripts/ingredient_list.json',("meal_id", "igredient_id"))
# print("meal_ingredient", meal_ingredient)
area = prep_query(f'{path}/scripts/areas.json',("id", "name"))
# print("area",area)
categories=prep_query(f'{path}/scripts/categories.json',("id", "name", "img_link", "description"))
# print("categories", categories)

def fill_areas_to_db() :
    for i in area:
        a = Area(name=i[1])
        db.session.add(a)
        db.session.commit()


def fill_categories_to_db():
    for i in categories:
        a = Category(name=i[1], img_link=i[2],description=i[3])
        db.session.add(a)
        db.session.commit()

def fill_ingredients_to_db():
    for i in ingredient:
        a = Ingredient(name=i[1],description=i[2])
        db.session.add(a)
        db.session.commit()


def fill_meals_to_db():
    for i in meals:
        a = Meal(name=i[1], category_id=i[2], area_id=i[3], instructions=i[5], img_link=i[6], tags=i[7],
                 video_link=i[8])
        db.session.add(a)
        db.session.commit()

def fill_meal_ingredient_to_db():
    print(meal_ingredient)
    for i in meal_ingredient:
        a = Meal_ingredient(meal_id=i[0],ingredient_id=i[1])
        db.session.add(a)
        db.session.commit()


def fill_all():
    fill_areas_to_db()
    fill_categories_to_db()
    fill_ingredients_to_db()
    fill_meals_to_db()
    fill_meal_ingredient_to_db()
    print('All done successfuly!')


# session.add(m)

# session.commit()
# def find_category_by_id(category_id):
#     categories = session.query(Category).all()
#     for category in categories :
#         if category.id == category_id :
#             return category

# def find_area_by_id(area_id):
#     areas = session.query(Area).all()
#     for area in areas :
#         if area.id == area_id :
#             return area

# def find_meal_by_category(category_id):
#     meals = session.query(Meal).all()
#     results = []
#     for meal in meals :
#         if meal.category_id == category_id :
#             # print(meal.category_id.name)
#             results.append(meal)
#     return results

# def test():
#     meals = session.query(Meal).all()
#     for meal in meals :
#         print(meal.category.name)

# test()
# print(find_category_by_id(1))
# print(find_area_by_id(1))
# print(find_meal_by_category(1))
#