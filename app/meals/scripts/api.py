import requests
import json
import os
import schedule
import time
from datetime import datetime



thisfolder = os.path.dirname(os.path.abspath(__file__))


def to_unquie_id(this_id):
    return int(f'{this_id}{int(datetime.now().timestamp())}')//3


def list_to_json_file(path, res):
    with open(path, 'w') as outfile:
        json.dump(res, outfile, indent=4,
                  ensure_ascii=True)


def filter_json(search_col, keyword, path):
    with open(path) as json_file:
        data = json.load(json_file)
    for x in data:
        if x[search_col].lower() == keyword.lower():
            return x['id']


def parse_categories():
    url = "https://www.themealdb.com/api/json/v1/1/categories.php"
    response1 = requests.request("GET", url)
    categ = json.loads(response1.text)['categories']
    categ_list = []
    for x in categ:
        categ_obj = {
            "id": to_unquie_id(int(x['idCategory'])),
            "name": x['strCategory'],
            "img_link": x['strCategoryThumb'],
            "description": x['strCategoryDescription'],
        }
        categ_list.append(categ_obj)
    list_to_json_file(f'{thisfolder}/categories.json', categ_list)
    print('Done! categories parsed.')
    return(categ)


def parse_ingredients():
    url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
    response1 = requests.request("GET", url)
    ingredients = json.loads(response1.text)['meals']
    ingredients_list = []
    for i in ingredients:
        if i["strType"] is None:
            i['strType'] = ""
        if i['strDescription'] is None:
            i['strDescription'] = ""
    for x in ingredients:
        ingr_obj = {
            "id": to_unquie_id(int(x['idIngredient'])),
            "name": x['strIngredient'],
            "description": x['strDescription'],
        }
        ingredients_list.append(ingr_obj)

    list_to_json_file(f'{thisfolder}/ingredients.json', ingredients_list)
    print('Done! ingredients parsed.')


def parse_areas():
    url = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
    response1 = requests.request("GET", url)
    areas = json.loads(response1.text)['meals']
    areas_list = []
    cnt_id = 1
    for x in areas:
        if x['strArea'] != 'Unknown':
            area_obj = {
                "id": to_unquie_id(cnt_id),
                "name": x['strArea'],
            }
            areas_list.append(area_obj)
            cnt_id += 1
    list_to_json_file(f'{thisfolder}/areas.json', areas_list)
    print('Done! areas parsed.')


def unparsed_meals(categ):
    categ_list = []
    categ = parse_categories()
    for x in categ:
        categ_list.append(x['strCategory'])
    meal_list = []
    for x in categ_list:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={x}"
        response = requests.request("GET", url)
        res = json.loads(response.text)['meals']
        for c in res:
            meal_list.append(c['idMeal'])
    res_list = []
    for x in meal_list:
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={x}"
        response = requests.request("GET", url)
        res = json.loads(response.text)['meals']
        res_list.append(res)

    with open(f'{thisfolder}/unparse_meals.json', 'w') as outfile:
        json.dump(res_list, outfile, indent=4,
                  ensure_ascii=True)

        print("Done! meals(unparsed) done")


def parse_meals():
    res = []
    with open(f"{thisfolder}/unparse_meals.json") as unparse_meals:
        data = json.load(unparse_meals)
    cnt_id = 1
    ingr_meal = []
    for meal in data:
        meal_unique_id = to_unquie_id(int(meal[0]['idMeal']))
        meal_obj = {
            'id': meal_unique_id, 'name': meal[0]['strMeal'],
            'category_id': filter_json('name', meal[0]['strCategory'],
                                       f"{thisfolder}/categories.json"),
            'area_id': filter_json('name', meal[0]['strArea'],
                                   f"{thisfolder}/areas.json"),
            'like_count': 0,
            'instructions': meal[0]['strInstructions'],
            'img_link': meal[0]['strMealThumb'],
            'tags': meal[0]['strTags'],
            'video_link': meal[0]['strYoutube'],
        }

        for x in range(1, 20):
            if (meal[0][f'strIngredient{x}']
            and not meal[0][f'strIngredient{x}'] is None):
                    ingr_id = filter_json('name', meal[0][f'strIngredient{x}'],
                                          f"{thisfolder}/ingredients.json")
                    if ingr_id:
                        obj = {
                               'meal_id': meal_unique_id,
                               'ingredient_id': ingr_id
                                }
                        ingr_meal.append(obj)
        res.append(meal_obj)
        cnt_id += 1
    list_to_json_file(f'{thisfolder}/ingredient_list.json', ingr_meal)
    list_to_json_file(f'{thisfolder}/parsed_meals.json', res)
    print('Done! meals parsed.')


def write_to_txt(file_name, my_list):
    os.remove(file_name)
    with open(file_name, 'a', encoding="utf-8") as outfile:
        for sublist in my_list:
            outfile.write('{}\n'.format(sublist))


def parse_all():
    parse_categories()
    unparsed_meals(parse_categories)
    parse_ingredients()
    parse_areas()
    parse_meals()


def prep_query(file_name, fields):
    with open(f'{thisfolder}/{file_name}', encoding="utf8") as jf:
        list1 = json.load(jf)
    list_new = []
    for i in range(len(list1)):
        list_new.append([])
    for j in range(0, len(list1)):
        for k, v in list1[j].items():
            if k in fields:
                list_new[j].append(v)
    return list_new


def prep_lists():
    meals = prep_query("parsed_meals.json", ("id", "name", "category_id",
                                             "area_id", "like_count",
                                             "instructions", "img_link",
                                             "tags", "video_link"))
    write_to_txt(f"{thisfolder}/final_lists/meals.txt", meals)

    ingredient = prep_query("ingredients.json", ("id", "name", "description"))
    write_to_txt(f"{thisfolder}/final_lists/ingredient.txt", ingredient)

    meal_ingredient = prep_query("ingredient_list.json", ("meal_id",
                                 "ingredient_id"))
    write_to_txt(f"{thisfolder}/final_lists/meal_ingredient.txt",
                  meal_ingredient)

    categories = prep_query("categories.json",
                            ("id", "name", "img_link", "description"))
    write_to_txt(f"{thisfolder}/final_lists/categories.txt", categories)

    area = prep_query("areas.json", ("id", "name"))
    write_to_txt(f"{thisfolder}/final_lists/area.txt", area)

#   unparsed_meals=prep_query("unparse_meals.json",
#     ("idMeal", "strMeal", "strArea", "strInstructions", "strMealThumb",
#      "strTags", "strYoutube", "strIngredient1", "strIngredient2",
#      "strIngredient3", "strIngredient4", "strIngredient5",
#      "strIngredient6", "strIngredient7", "strIngredient8",
#      "strIngredient9", "strIngredient10", "strIngredient11",
#      "strIngredient12", "strIngredient13", "strIngredient14",
#      "strIngredient15", "strIngredient16", "strIngredient17",
#      "strIngredient18", "strIngredient19", "strIngredient20",
#      "strMeasure1", "strMeasure2", "strMeasure3",
#      "strMeasure4", "strMeasure5", "strMeasure6", 	"strMeasure7",
#      "strMeasure8", "strMeasure9", "strMeasure10", "strMeasure11",
#      "strMeasure12", "strMeasure13", "strMeasure14", "strMeasure15",
#      "strMeasure16", "strMeasure17", "strMeasure18", "strMeasure19",
#      "strMeasure20", "dateModified"))
#    print("unparsed_meals", meals)
#    write_to_txt(f"{thisfolder}/final_lists/unparsed_meals.txt",unparsed_meals)


def main():
    parse_all()
    prep_lists()
    now=datetime.now()
    current_time=now.strftime("%H:%M:%S")
    print("last updated at  ", current_time)



if __name__ == "__main__":
    main()
    schedule.every(24).hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
