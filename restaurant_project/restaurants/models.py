from django.contrib.auth.hashers import make_password
from django.db import models


class MenuType(models.Model):
    menu_type_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.menu_name


class Dish(models.Model):
    dish_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True, db_column='id')
    restaurant_name = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    menus = models.ManyToManyField(MenuType, through='RestaurantMenu')

    # def save(self, *args, **kwargs):
    #     # Hash the password before saving
    #     self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.restaurant_name


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_type = models.ForeignKey(MenuType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('restaurant', 'menu_type')

    def __str__(self):
        return f"{self.restaurant.restaurant_name} - {self.menu_type.menu_name}"
        # return f"{self.restaurant.restaurant_name} - {self.menu_type.menu_name} - {self.dishes.name}"


class MenuDish(models.Model):
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('menu', 'dish')

    def __str__(self):
        return f"{self.menu} - {self.dish.name}"
