from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import MenuType, Dish, Restaurant, RestaurantMenu, MenuDish


class RestaurantSerializer(serializers.ModelSerializer):
    menus = StringRelatedField(many=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        restaurant = Restaurant.objects.create(**validated_data)
        if password:
            restaurant.password = make_password(password)
            restaurant.save()
        return restaurant


class MenuTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.menu_name = validated_data.get('menu_name', instance.menu_name)
        instance.save()
        return instance


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class RestaurantMenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.SlugRelatedField(slug_field='restaurant_name', queryset=Restaurant.objects.all())
    menu_type = serializers.SlugRelatedField(slug_field='menu_name', queryset=MenuType.objects.all())

    class Meta:
        model = RestaurantMenu
        fields = '__all__'


class MenuDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDish
        fields = '__all__'


# class RestaurantLoginSerializer(serializers.Serializer):
#     name = serializers.CharField(
#         max_length=100,
#         style={'placeholder': 'restaurant name', 'autofocus': True}
#     )
#     password = serializers.CharField(
#         max_length=100,
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )
#     remember_me = serializers.BooleanField()
#
#     def validate(self, data):
#         """
#         Check if the provided name and password match a restaurant in the database.
#         """
#         name = data.get('name')
#         password = data.get('password')
#
#         if name and password:
#             # Replace this with your logic to authenticate the restaurant
#             try:
#                 restaurant = Restaurant.objects.get(restaurant_name=name)
#                 print(restaurant, '____')
#             except Restaurant.DoesNotExist:
#                 raise serializers.ValidationError("Restaurant with this name does not exist.")
#
#             if restaurant.password == password:
#                 raise serializers.ValidationError("Incorrect password.")
#         return data


class RestaurantLoginSerializer(serializers.Serializer):
    restaurant_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)


class RestaurantOwnMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = '__all__'



class MenuDishCreateSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(write_only=True)

    class Meta:
        model = MenuDish
        fields = [
            'dish_name',
            'description',
            'price',
            'image',
            'is_veg',
            'is_available',
        ]

    def create(self, validated_data):
        dish_name = validated_data.pop('dish_name')
        menu = self.context['menu']

        dish, _ = Dish.objects.get_or_create(name=dish_name)

        menu_dish, created = MenuDish.objects.get_or_create(
            menu=menu,
            dish=dish,
            defaults=validated_data
        )

        if not created:
            # update existing dish if already added
            for key, value in validated_data.items():
                setattr(menu_dish, key, value)
            menu_dish.save()

        return menu_dish
