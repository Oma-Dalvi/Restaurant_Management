from django.urls import path
from .views import *

urlpatterns = [
    path('restaurants_home', RestaurantHome.as_view(), name='restaurants-home'),

    path('restaurants_register', RestaurantRegister.as_view(), name='restaurants-register'),
    # path('restaurants_register/<int:pk>',RestaurantRegister.as_view(), name='restaurants-register'),

    path('restaurants_login', RestaurantLogin.as_view(), name='restaurants-login'),
    # path('restaurants_login/<int:pk>', RestaurantLogin.as_view(), name='restaurants-login'),


    path('restaurants_list', RestaurantListView.as_view(), name='restaurant-list'),
]
