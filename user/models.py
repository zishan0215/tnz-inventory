from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name + " " + self.last_name
