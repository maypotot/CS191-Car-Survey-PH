from django.db import models

class Vehicle(models.Model):
    model = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    transmission = models.CharField(max_length=10)
    year = models.IntegerField()
    odometer = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.maker} {self.model}"

class Value(models.Model):
    value_price = models.IntegerField()
    highest_value = models.IntegerField()
    lowest_value = models.IntegerField()