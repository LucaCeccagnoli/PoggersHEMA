from django import forms
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from users.models import CustomUser

# estensione del form di registrazione standard per adattarlo a utenti customizzati
class CustomUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser

class LoginForm(AuthenticationForm):
    pass

class PaymentForm(forms.Form):
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')
    address = forms.CharField(max_length = 100, required = True)

class ChangeUsernameForm(forms.Form):
    username = forms.CharField(label = 'new username')

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label = 'new email')

class ChangePasswordForm(forms.Form):
    password_current = forms.CharField(widget = forms.PasswordInput())
    password_new = forms.CharField(widget = forms.PasswordInput())
    password_info = forms.CharField(widget = forms.PasswordInput())