from django.contrib.auth.hashers import make_password
from django.db import models
import os

def dish_image_upload_path(instance, filename):
    restaurant = instance.menu.restaurant
    restaurant_name = restaurant.restaurant_name.replace(" ", "_")

    return os.path.join(
        "restaurants",
        restaurant_name,
        "dishes",
        filename
    )




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

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


    # def save(self, *args, **kwargs):
    #     # Hash the password before saving
    #     self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.restaurant_name


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_type = models.ForeignKey(MenuType, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        unique_together = ('restaurant', 'menu_type')

    def __str__(self):
        return f"{self.restaurant.restaurant_name} - {self.menu_type.menu_name}"
        # return f"{self.restaurant.restaurant_name} - {self.menu_type.menu_name} - {self.dishes.name}"


class MenuDish(models.Model):
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image = models.ImageField(
        upload_to=dish_image_upload_path,
        null=True,
        blank=True
    )

    is_available = models.BooleanField(default=True)
    is_veg = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        unique_together = ('menu', 'dish')

    def __str__(self):
        return f"{self.menu} - {self.dish.name}"



