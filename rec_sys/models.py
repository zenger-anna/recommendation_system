from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# blank - нельзя добавлять новые значения пустыми, null - не может быть пустого значения в БД


class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False, null=False)
    ingredients = models.TextField(max_length=4000, unique=False, blank=False, null=False)
    directions = models.TextField(max_length=10000, unique=False, blank=False, null=False)
    description = models.TextField(max_length=4000, unique=False, blank=True, null=True)
    mean_rating = models.FloatField(default=0.0)
    fat = models.FloatField(unique=False, blank=True, null=True)
    calories = models.FloatField(unique=False, blank=True, null=True)
    protein = models.FloatField(unique=False, blank=True, null=True)
    sodium = models.FloatField(unique=False, blank=True, null=True)
    old_id = models.IntegerField()
    similar = models.TextField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return ' - '.join([str(self.id), str(self.title), str(self.mean_rating), str(self.calories)])


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, blank=False, null=False)
    view_date = models.DateTimeField(blank=False, null=False, auto_now_add=True)

    def __str__(self):
        return ' - '.join([str(self.user), str(self.recipe), str(self.view_date)])


class AddedRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return ' - '.join([str(self.user), str(self.recipe)])


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, blank=False, null=False)
    rating = models.IntegerField()

    def __str__(self):
        return ' - '.join([str(self.user), str(self.recipe), str(self.rating)])


class Tag(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False, null=False)
    old_id = models.IntegerField()

    def __str__(self):
        return str(self.title)


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False, null=False)
    old_id = models.IntegerField()

    def __str__(self):
        return str(self.title)


class RecipesTags(models.Model):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, blank=False, null=False)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return ' - '.join([str(self.tag), str(self.recipe)])


class RecipesCategory(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=False, null=False)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return ' - '.join([str(self.category), str(self.recipe)])


class UserRecRecipes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipe_list = models.TextField(max_length=2000, blank=True, null=True)
