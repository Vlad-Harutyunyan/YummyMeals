import re
from ..models import Meal, Ingredient, Category, Area, Meal_ingredient
# from ..app.users.models import User_Favorite, User_Favorite_Category, User


def name_correct(name):
    matches = re.finditer(" ", name)
    list1 = [match.start() for match in matches]
    name1 = name[0]
    for i in range(0, len(name) - 1):
        if i in list1:
            name1 += name[i] + name[i + 1].upper()
        else:
            name1 += name[i + 1].lower()
    name1 = name1.replace("  ", " ")
    return (name1)

