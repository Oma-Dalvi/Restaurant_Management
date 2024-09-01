from django.urls import path
from .views import *

urlpatterns = [
    path('restaurants_home', RestaurantHome.as_view(), name='restaurants-home'),

    path('restaurants_register', RestaurantRegister.as_view(), name='restaurants-register'),
    # path('restaurants_register/<int:pk>',RestaurantRegister.as_view(), name='restaurants-register'),

    path('restaurants_login', RestaurantLogin.as_view(), name='restaurants-login'),
    # path('restaurants_login/<int:pk>', RestaurantLogin.as_view(), name='restaurants-login'),

    path('restaurants_menu/<int:pk>', RestaurantOwnMenuAPI.as_view(), name='restaurants-menu'),

    path('restaurants_add_menu/<int:pk>', AddRestaurantMenuAPI.as_view(), name='add-restaurant-menu'),

    path('delete-menu/<int:menu_id>/', RestaurantMenuDeleteAPIView.as_view(), name='delete-restaurant-menu'),

    path('restaurants_menu/<int:menu_id>/dishes', RestaurantMenuDishesAPI.as_view(), name='restaurants-menu-dishes'),

    path('restaurants_menu/<int:menu_id>/add_dish', AddDishToMenuAPI.as_view(), name='add-dish-to-menu'),

    path('delete-dish/<int:menu_id>/', RestaurantDishDeleteAPI.as_view(), name='delete-dish'),


    path('logout/', RestaurantLogout.as_view(), name='restaurant-logout'),
]
