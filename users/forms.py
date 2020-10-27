from django import forms
from django_registration.forms import RegistrationForm
from users.models import CustomUser

# estensione del form di registrazione standard per adattarlo a utenti customizzati
class CustomUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())