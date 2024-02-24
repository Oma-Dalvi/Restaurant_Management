# restaurants/admin.py
from django.contrib import admin
from .models import *


admin.site.register(MenuType)
admin.site.register(Dish)
admin.site.register(Restaurant)
admin.site.register(RestaurantMenu)
admin.site.register(MenuDish)
