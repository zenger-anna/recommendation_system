import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from rec_sys.models import *


def gen_recipes_lists():
    users = User.objects.all()
    recipes = Recipe.objects.all()

    ratings = Rating.objects.all()
    n_users = users.count()
    n_recipes = recipes.count()
    rating_matrix = np.zeros((n_users, n_recipes))
    print('start matrix')
    for rating in ratings:
        rating_matrix[int(rating.user.id - 2), int(rating.recipe.old_id)] = rating.rating
    print('matrix done')
    recipe_cosine_similarity = pd.DataFrame(cosine_similarity(rating_matrix.T))

    for user in users:
        print(' -- USER {} -- '.format(user.id))
        # получаем список избранных рецептов
        f_recipes = Recipe.objects.filter(addedrecipes__user=user).order_by('-addedrecipes__id')[:5]
        if not f_recipes.exists():
            # если нет избранных, попробуем рекомендовать по истории просмотров
            # (аналогично возьмем до 5 последних просмотров)
            f_recipes = Recipe.objects.filter(history__user=user).order_by('-history__view_date')[:5]
            if not f_recipes.exists():
                # для тех, кто в танке, просто будем советовать 50 самых популярных рецептов
                print('User {} has no favourites or history! '
                      'Gen recipes list with the best mean rating.'.format(user.id))
                rec_recipes_list = Recipe.objects.all().order_by('-mean_rating')[:50]
                user.userrecrecipes.recipe_list = '$'.join([str(x) for x in rec_recipes_list.values_list('id', flat=True)])
                user.userrecrecipes.save()
            else:
                content_based_rec = cb_recommend(f_recipes)
                recommendation = ub_recommend(content_based_rec, user, recipe_cosine_similarity, rating_matrix)
                user.userrecrecipes.recipe_list = '$'.join([str(x) for x in recommendation])
                user.userrecrecipes.save()
        else:
            content_based_rec = cb_recommend(f_recipes)
            recommendation = ub_recommend(content_based_rec, user, recipe_cosine_similarity, rating_matrix)
            user.userrecrecipes.recipe_list = '$'.join([str(x) for x in recommendation])
            user.userrecrecipes.save()


def cb_recommend(f_recipes):
    content_based_rec = []
    for recipe in f_recipes:
        recipe.similar = recipe.similar.split('$')
        for recipe_id in recipe.similar:
            content_based_rec.append(Recipe.objects.get(id=recipe_id).old_id)
    print('   - CONTENT-BASED RECOMMENDATION DONE')
    return content_based_rec


def ub_recommend(content_based_rec, current_user, recipe_cosine_similarity, rating_matrix):

    predict = pd.Series(index=content_based_rec)
    recipes_rec_simil = recipe_cosine_similarity[content_based_rec]

    for recipe_id, recipe_simil in recipes_rec_simil.iteritems():
        top_recipe_simil = recipe_simil.sort_values(ascending=False)[:900]
        top_ratings = rating_matrix[current_user.id - 2].T[top_recipe_simil.index.values]

        i = 0
        for index, recipe_sim in top_recipe_simil.items():
            if top_ratings[i] != 0:
                top_ratings[i] = recipe_sim * (top_ratings[i] - Recipe.objects.get(old_id=index).mean_rating)
            else:
                top_ratings[i] = 0
            i += 1

        if top_recipe_simil.sum() != 0:
            predict[recipe_id] = Recipe.objects.get(old_id=recipe_id).mean_rating + top_ratings.sum() / top_recipe_simil.sum()
        else:
            predict[recipe_id] = Recipe.objects.get(old_id=recipe_id).mean_rating + top_ratings.sum() / 900

    recommendation = []
    predict = list(predict.sort_values(ascending=False).index)[:50]
    for index in predict:
        recommendation.append(Recipe.objects.get(old_id=index).id)
    print('   - COLLABORATIVE FILTERING DONE')
    return recommendation
