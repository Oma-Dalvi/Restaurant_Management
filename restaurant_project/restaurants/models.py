from django.db import models


class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100)
    cuisine = models.ForeignKey(Cuisine, related_name='dishes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')

    def __str__(self):
        return self.name
