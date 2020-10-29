from django import forms
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from users.models import CustomUser

# estensione del form di registrazione standard per adattarlo a utenti customizzati
class CustomUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser

class LoginForm(AuthenticationForm):
    pass