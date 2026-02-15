from django.urls import path
from .views import *

urlpatterns = [
    path('customer_register', CustomerRegistrationAPi.as_view(), name='customer-register'),
    path('customer_login', CustomerLoginAPi.as_view(), name='customer-login'),


    path('restaurant_list', RestaurantListApi.as_view(), name='restaurant-list'),

    path('restaurant/<int:restaurant_id>/menu/',SearchRestaurantMenuAPI.as_view(), name='customer-restaurant-menu')
]
