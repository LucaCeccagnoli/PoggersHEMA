from django.db import models

# modello default di user customizzabile, contiene firstname, lastname, email e is_staff
from django.contrib.auth.models import AbstractUser 

from articles.models import Article, OrderItem

class ShoppingCart(models.Model):
    pass

#modello personalizzato di utente (scalabile in futuro)
#   !aggiungere shopping cart
class CustomUser(AbstractUser):
    pass

# Create your models here.
class Order(models.Model):
    ref_code = models.CharField(max_length = 15)
    owner = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True, related_name = "owner") 
    is_ordered = models.BooleanField(default = False)

    # campo molti a molti per gli ordini
    items = models.ManyToManyField(Article)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([ art.price for art in self.items.all()])



