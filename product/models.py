from django.db import models
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    modelno = models.CharField(max_length=100)
    length = models.FloatField(null=True, blank=True)
    breadth = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='images')
    thumbnail = models.ImageField(upload_to='images', blank=True, null=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name