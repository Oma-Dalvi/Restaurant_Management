from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Cuisine, Dish, Restaurant


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class CuisineSerializer(serializers.ModelSerializer):
    selected = serializers.BooleanField(default=False, write_only=True)
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Cuisine
        fields = ['id', 'name', 'selected']
        # fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    cuisines = serializers.PrimaryKeyRelatedField(queryset=Cuisine.objects.all(), many=True)
    # cuisines = serializers.ListField(child=serializers.CharField(), write_only=True)


    class Meta:
        model = Restaurant
        fields = ['name', 'password', 'cuisines']

    def create(self, validated_data):
        cuisines_data = validated_data.pop('cuisines', [])
        password = validated_data.pop('password', None)
        restaurant = Restaurant.objects.create(**validated_data)
        if password:
            restaurant.password = make_password(password)
            restaurant.save()
        for cuisine_name in cuisines_data:
            cuisine, _ = Cuisine.objects.get_or_create(name=cuisine_name)
            restaurant.cuisines.add(cuisine)
        return restaurant


class RestaurantLoginSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        style={'placeholder': 'name', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    remember_me = serializers.BooleanField()

    def validate(self, data):
        """
        Check if the provided name and password match a restaurant in the database.
        """
        name = data.get('name')
        password = data.get('password')

        if name and password:
            # Replace this with your logic to authenticate the restaurant
            try:
                restaurant = Restaurant.objects.get(name=name)
                print(restaurant,'____')
            except Restaurant.DoesNotExist:
                raise serializers.ValidationError("Restaurant with this name does not exist.")

            if not restaurant.check_password(password):
                raise serializers.ValidationError("Incorrect password.")

        return data