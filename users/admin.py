from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import *

# Register your models here.
# Modello utente usato dagli amministratori
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # i campi che verranno mostrati nella pagina cambio lista dell'admin
    list_display = ["id", "email", "username", "is_staff"]

admin.site.register(CustomUser, CustomUserAdmin)