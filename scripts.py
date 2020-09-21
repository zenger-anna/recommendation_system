import json
from rec_sys.models import *


def create_recipes():
    with open('data/recipes.json', 'r', encoding='utf-8-sig') as json_dict:
        data = json.load(json_dict)
    for x in data:
        print(type(x['old_id']))
        if not Recipe.objects.filter(title=x['title']).exists():
            r = Recipe.objects.create(
                title=x['title'],
                ingredients=x['ingredients'],
                directions=x['directions'],
                description=x['desc'],
                mean_rating=x['rating'],
                fat=x['fat'],
                calories=x['calories'],
                protein=x['protein'],
                sodium=x['sodium'],
                old_id=x['old_id']
            )
            print(r.id, r.title)
    print('---------')
    print(len(data))


def create_categories():
    with open('data/categories.json', 'r', encoding='utf-8-sig') as json_dict:
        data = json.load(json_dict)
    for x in data:
        if not Category.objects.filter(title=x['category_name']).exists():
            r = Category.objects.create(
                title=x['category_name'],
                old_id=x['old_id']
            )
            print(r.id, r.title)
    print('---------')
    print(len(data))


def create_tags():
    with open('data/tags.json', 'r', encoding='utf-8-sig') as json_dict:
        data = json.load(json_dict)
    for x in data:
        if not Tag.objects.filter(title=x['tag_name']).exists():
            r = Tag.objects.create(
                title=x['tag_name'],
                old_id=x['old_id']
            )
            print(r.id, r.title)
    print('---------')
    print(len(data))


def create_rt():
    with open('data/recipes_with_tags.json', 'r', encoding='utf-8-sig') as json_dict:
        recipes_with_tags = json.load(json_dict)
    for item in recipes_with_tags:
        if Recipe.objects.filter(old_id=item['old_id']).exists():
            recipe = Recipe.objects.get(old_id=item['old_id'])
            tags = Tag.objects.filter(title__in=item['recipe_info'])
            for tag in tags:
                obj, create = RecipesTags.objects.get_or_create(
                    tag=tag,
                    recipe=recipe
                )
                print(obj)


def create_rc():
    with open('data/recipes.json', 'r', encoding='utf-8-sig') as json_dict:
        recipes = json.load(json_dict)
    for item in recipes:
        if Recipe.objects.filter(old_id=item['old_id']).exists():
            recipe = Recipe.objects.get(old_id=item['old_id'])
            categories = Category.objects.filter(title__in=item['categories'])
            for category in categories:
                obj, create = RecipesCategory.objects.get_or_create(
                    category=category,
                    recipe=recipe
                )
                print(obj)


def create_users():
    for count in range(150):
        user = User.objects.create(
            username=User.objects.make_random_password(),
            password=User.objects.make_random_password()
        )
        print(user.id, user.username)


def create_ratings():
    with open('data/new_ratings.json', 'r', encoding='utf-8-sig') as json_dict:
        ratings = json.load(json_dict)
    for rating in ratings:
        if Recipe.objects.filter(old_id=rating['recipe_id']).exists():
            user = User.objects.get(id=rating['user_id'] + 2)
            recipe = Recipe.objects.get(old_id=rating['recipe_id'])
            r = Rating.objects.create(
                user=user,
                recipe=recipe,
                rating=rating['rating']
            )
            print(r.id)


def add_similar():
    with open('data/recipe_simil.json', 'r', encoding='utf-8-sig') as json_dict:
        similar = json.load(json_dict)
    for key in similar:
        print(key)
        recipe = Recipe.objects.get(id=key)
        recipe.similar = similar[key]
        recipe.save()


def add_user_rec_recipes():
    users = User.objects.all()
    for user in users:
        item = UserRecRecipes.objects.create(user_id=user.id)
        print(item)


def old_id_recipe():
    recipes = Recipe.objects.all()
    i = 0
    for recipe in recipes:
        recipe.old_id = i
        recipe.save()
        i += 1
