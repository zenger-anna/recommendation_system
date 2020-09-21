from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.core.paginator import Paginator
from .models import *
from .forms import *


def search_recipes(request):

    search_input = ''
    if 'search_by_name' in request.GET:
        search_input = request.GET['search_input']
        recipes = Recipe.objects.filter(title__icontains=search_input).order_by('-mean_rating').values(
            'id', 'title', 'mean_rating')
        base_url = '/search/?search_input=' + search_input + '&search_by_name=&'
    else:
        if 'log_out_nav_but' in request.GET:
            logout(request)
        recipes = Recipe.objects.all().order_by('-mean_rating').values('id', 'title', 'mean_rating')
        base_url = '/search/?'
    paginator = Paginator(recipes, 20)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'search.html', {'page': page, 'base_url': base_url, 'search_input': search_input})


def view_recipe(request, recipe_id):

    added = False
    recipe = Recipe.objects.get(id=recipe_id)
    rated = Rating.objects.filter(user=request.user.id, recipe=recipe_id).exists()
    if rated:
        recipe_rating = Rating.objects.get(user=request.user.id, recipe=recipe_id).rating
    else:
        recipe_rating = 0
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'add_recipe' in request.POST:
                added = True
                AddedRecipes.objects.create(user=request.user, recipe=recipe)
            elif 'del_recipe' in request.POST:
                added = False
                added_recipes = AddedRecipes.objects.filter(user=request.user.id, recipe=recipe_id)
                for item in added_recipes:
                    item.delete()
            elif 'rating_1' or 'rating_2' or 'rating_3' or 'rating_4' or 'rating_5' in request.POST:
                if rated:
                    user_rating = Rating.objects.get(user=request.user.id, recipe=recipe_id)
                else:
                    user_rating = Rating.objects.create(user=request.user, recipe=recipe, rating=0)
                    rated = True
                if 'rating_1' in request.POST:
                    user_rating.rating = 1
                elif 'rating_2' in request.POST:
                    user_rating.rating = 2
                elif 'rating_3' in request.POST:
                    user_rating.rating = 3
                elif 'rating_4' in request.POST:
                    user_rating.rating = 4
                elif 'rating_5' in request.POST:
                    user_rating.rating = 5
                user_rating.save()
                recipe_rating = user_rating.rating
        if AddedRecipes.objects.filter(user=request.user.id, recipe=recipe_id).exists():
            added = True
        if History.objects.filter(user=request.user, recipe=recipe).exists():
            h = History.objects.filter(user=request.user, recipe=recipe)
            for item in h:
                item.delete()
        else:
            history = History.objects.filter(user=request.user.id).order_by('view_date')
            if len(history) == 20:
                history[0].delete()
        History.objects.create(user=request.user, recipe=recipe)
    recipe = recipe.__dict__
    recipe['ingredients'] = recipe['ingredients'].split('00000000')
    recipe['directions'] = recipe['directions'].split('00000000')
    if recipe['description'] is None:
        recipe['description'] = 'This recipe has no description yet...'
    recipe['similar'] = recipe['similar'].split('$')
    similar_recipes = []
    for recipe_id in recipe['similar']:
        similar_recipes.append(Recipe.objects.get(id=recipe_id))
    return render(request, 'recipe_page.html', {'recipe': recipe,
                                                'added': added,
                                                'similar_recipes': similar_recipes,
                                                'rated': rated,
                                                'recipe_rating': recipe_rating})


def view_about(request):
    return render(request, 'about.html')


def view_account(request):
    f_recipes = Recipe.objects.filter(addedrecipes__user=request.user).order_by('-addedrecipes__id')
    h_recipes = Recipe.objects.filter(history__user=request.user).order_by('-history__view_date')
    return render(request, 'account.html', {'favourite_recipes': f_recipes, 'history_recipes': h_recipes})


def view_day_recipes(request):
    recipes_list = request.user.userrecrecipes.recipe_list.split('$')
    recipes = []
    for recipe_id in recipes_list:
        recipes.append(Recipe.objects.get(id=recipe_id))
    return render(request, 'day_recipes.html', {'recipes': recipes})


def log_in(request):

    if 'log_in_but' in request.GET:
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect('/search/')
            return response
        else:
            return render(request, 'login.html', {'login_error': True})
    return render(request, 'login.html', {'login_error': False})


class SignIn(View):

    def get(self, request):
        form_user = UserForm()
        return render(request, 'signin.html', context={'form_user': form_user, 'signin_error': False})

    def post(self, request):
        post_user = request.POST.copy()
        bound_form_user = UserForm(post_user)
        if bound_form_user.is_valid():
            new_user = bound_form_user.save()
            u = User.objects.get(username=new_user.username)
            u.set_password(new_user.password)
            u.save()
            rec_recipes_list = Recipe.objects.all().order_by('-mean_rating')[:50]
            UserRecRecipes.objects.create(
                user_id=u.id,
                recipe_list='$'.join([str(x) for x in rec_recipes_list.values_list('id', flat=True)])
            )
            login(request, u)
            response = redirect('/search/')
            return response
        return render(request, 'signin.html', context={'form_user': bound_form_user, 'signin_error': True})
