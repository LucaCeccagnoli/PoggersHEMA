from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver

# modello default di user customizzabile, contiene firstname, lastname, email e is_staff
from django.contrib.auth.models import AbstractUser 

# Create your models here.

#modello personalizzato di utente (scalabile in futuro)
#   !aggiungere shopping cart
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default = False)


# alla creazione di un nuovo utente, genera un token
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)
