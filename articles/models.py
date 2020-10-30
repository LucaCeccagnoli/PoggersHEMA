from django.db import models

# Create your models here.

# basic shop articles
class Article(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100, null = True)
    material = models.CharField(max_length = 100, default = "synthetic")
    category = models.CharField(max_length = 100, default = "none")
    sub_category = models.CharField(max_length = 100, default = "none")
    price = models.DecimalField(max_digits = 10, decimal_places = 2)    
    stock = models.IntegerField(default = 5)

    def __str__(self):
        return self.name + " - " + self.material

# instance of a shopping cart article
# ! sostituire agli articles semplici nel modello Order
class OrderItem(models.Model):
    article = models.OneToOneField(Article, on_delete = models.CASCADE)
    amount = models.IntegerField(default = 1)
    
    def __str__(self):
        return self.article.name
