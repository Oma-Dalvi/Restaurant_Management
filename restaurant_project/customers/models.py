from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True, db_column='id')
    customer_name = models.CharField(max_length=255)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name


