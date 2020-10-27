from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver

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


# alla creazione di un nuovo utente, genera un token
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)
