import re
from ..models import Meal, Ingredient, Category, Area, Meal_ingredient
# from ..app.users.models import User_Favorite, User_Favorite_Category, User

def name_correct(name):
    name_split=name.split(" ")
    name1=""
    for i in name_split:
        name1+=i.capitalize()+" "
    res=[name1.strip(),name1.strip().lower(),name1.strip().upper(),name]
    return (list(set(res)))

