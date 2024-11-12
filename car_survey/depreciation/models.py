from django.db import models


class UserInput(models.Model):
    model = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    odometer = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.maker} {self.model}"
