from django.urls import path
from .views import *

app_name = 'rec_sys'
urlpatterns = [
    path('', search_recipes, name='search_first'),
    path('search/', search_recipes, name='search'),
    path('about/', view_about, name='about'),
    path('recipe/<int:recipe_id>/', view_recipe, name='view_recipe'),
    path('log_in/', log_in, name='log_in'),
    path('sign_in/', SignIn.as_view(), name='sign_in'),
    path('account/', view_account, name='account'),
    path('day_recipes/', view_day_recipes, name='day_recipes'),
]
