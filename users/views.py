from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from users.models import CustomUser
from users.forms import *

# Create your views here.
class RegistrationView(View):
    def get(self, request):
        form = CustomUserForm()
        context = {
            "form": form
        }
        return render(request, "registration.html", context)

    def post(self, request):
        return HttpResponseRedirect("/registration")

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, "login.html", context)
    
    def post(self, request):
        return HttpResponseRedirect("/login/")

# se l'utente è loggato mostra il suo carrello
class ShoppingCartView(View):
    def get(self, request):
        current_user = request.user
        form = PaymentForm()
        context = {
            "form" : form
        }
        if current_user.is_authenticated:
            return render(request, "shopping_cart.html", context)
        else:
            return HttpResponseRedirect("/login/")
