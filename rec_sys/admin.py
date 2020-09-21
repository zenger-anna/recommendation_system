from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Tag)