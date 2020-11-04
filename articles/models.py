from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver, Signal
from django.contrib.auth.models import AbstractUser 
from users.models import CustomUser

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
        return self.name + " - " + self.material + " id: " + str(self.pk)

# carrello spedizione di un utente
class Order(models.Model):
    ref_code = models.CharField(max_length = 15)
    owner = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True, related_name = "owner") 
    is_ordered = models.BooleanField(default = False)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([ art.price for art in self.items.all()])

    def __str__(self):
        return "owner : " + str(self.owner.id) + " code : " + self.ref_code

# instance of a shopping cart article
# ! sostituire agli articles semplici nel modello Order
class OrderItem(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, null = True)
    amount = models.IntegerField(default = 1)
    
    def __str__(self):
        return self.article.name + "( " + str(self.amount) + " )" + "order: " + self.order.ref_code + " pk: " + str(self.pk)


