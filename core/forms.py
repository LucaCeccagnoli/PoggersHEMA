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
    current_password = forms.CharField(widget = forms.PasswordInput(), label = "old password")
    new_password = forms.CharField(widget = forms.PasswordInput(), label = "new password")
    confirm_password = forms.CharField(widget = forms.PasswordInput(), label = "confirm new password")

class ArticleForm(forms.Form):
    name = forms.CharField(max_length = 20, label = "name", required = True)
    material = forms.CharField(max_length = 20, label = "material", required = True)
    description = forms.CharField(widget = forms.Textarea, max_length = 255)
    category = forms.CharField(max_length = 20, label = "category")
    sub_category = forms.CharField(max_length = 20, label = "sub category")
    price = forms.DecimalField(max_digits = 5, decimal_places = 2, required = True)
    image = forms.URLField(max_length = 255, label = "image (URL)")