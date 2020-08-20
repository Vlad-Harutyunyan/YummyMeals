import sys
from ast import literal_eval
from .models import Area, Meal_ingredient, Ingredient, Meal, Category
from .. import db
from .scripts.api import thisfolder

sys.path.append(".")


def smart_db_update(db_table, record, check=True):
    if check:
        q = db.session.query(db_table).filter(db_table.name == record.name)
        if not db.session.query(q.exists()).scalar():
            db.session.add(record)
            db.session.commit()
    else:
        q = db.session.query(db_table).filter(db_table.id == record.id)
        if not db.session.query(q.exists()).scalar():
            db.session.add(record)
            db.session.commit()


def read_from_txt(file_name, list_name):
    with open(file_name, 'r', encoding='raw_unicode_escape') as fd:
        mylist = []
        for line in fd:
            mylist.append(literal_eval(line))
    return (mylist)


def fill_areas_to_db():
    area = read_from_txt(f"{thisfolder}/final_lists/area.txt", 'area')
    for i in area:
        a = Area(id=i[0], name=i[1])
        smart_db_update(Area, a)


def fill_categories_to_db():
    categories = read_from_txt(f"{thisfolder}/final_lists/categories.txt",
                               'categories')
    for i in categories:
        a = Category(id=i[0], name=i[1], img_link=i[2], description=i[3])
        smart_db_update(Category, a)


def fill_ingredients_to_db():
    ingredient = read_from_txt(f"{thisfolder}/final_lists/ingredient.txt",
                               'ingredient')
    for i in ingredient:
        a = Ingredient(id=i[0], name=i[1], description=i[2])
        smart_db_update(Ingredient, a)


def fill_meals_to_db():
    meals = read_from_txt(f"{thisfolder}/final_lists/meals.txt", 'meals')
    for i in meals:
        a = Meal(id=i[0], name=i[1], category_id=i[2], area_id=i[3],
                 instructions=i[5], img_link=i[6], tags=i[7], video_link=i[8])
        smart_db_update(Meal, a)


def fill_meal_ingredient_to_db():
    meal_ingredient = read_from_txt(
        f"{thisfolder}/final_lists/meal_ingredient.txt",
        'meal_ingredient')
    for i in meal_ingredient:
        a = Meal_ingredient(meal_id=i[0], ingredient_id=i[1])
        smart_db_update(Meal_ingredient, a, check=False)


def fill_all():
    fill_areas_to_db()
    fill_meal_ingredient_to_db()
    fill_categories_to_db()
    fill_ingredients_to_db()
    fill_meals_to_db()
    print('All done successfully!')
