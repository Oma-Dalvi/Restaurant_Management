# restaurants/admin.py
from django.contrib import admin
from .models import Cuisine, Dish, Restaurant

admin.site.register(Cuisine)
admin.site.register(Dish)
admin.site.register(Restaurant)
