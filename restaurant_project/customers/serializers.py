from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import *
from restaurants.models import  Restaurant


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        restaurant = Customer.objects.create(**validated_data)
        if password:
            restaurant.password = make_password(password)
            restaurant.save()
        return restaurant


class CustomerLoginSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['restaurant_id', 'restaurant_name']