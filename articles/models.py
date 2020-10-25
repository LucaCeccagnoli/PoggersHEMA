from django.db import models

# Create your models here.

# basic shop articles
class Article(models.Model):
    name = models.CharField(max_length = 100)
    material = models.CharField(max_length = 100)
    weight = models.DecimalField(max_digits = 10, decimal_places = 2)   #weight in grams
    price = models.DecimalField(max_digits = 10, decimal_places = 2)    
    stock = models.IntegerField(default = 0)

# instance of a shopping cart article
# ! sostituire agli articles semplici nel modello Order
class OrderItem(models.Model):
    article = models.OneToOneField(Article, on_delete = models.CASCADE)
    amount = models.IntegerField(default = 1)
    
    def __str__(self):
        return self.product.name