from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import generics, mixins, permissions
from users.models import CustomUser
from users.forms import *
from users.api.permissions import *

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

class ChangeCredentialsView(View):
    def get(self, request):
        current_user = request.user
        username_form = ChangeUsernameForm()
        email_form = ChangeEmailForm()
        password_form =  ChangePasswordForm()
        context = {
            "username_form" : username_form,
            "email_form": email_form,
            "password_form": password_form
        }
        if current_user.is_authenticated:
            return render(request, "account.html", context)
        else:
            return HttpResponseRedirect("/login/")

class ManagerUserListView(View):
    def get(self, request):
        return render (request, "user-list.html")

class ShipmentsListView(View):
    def get(self, request, *args, **kwargs):
        context={}
        if 'pk' in kwargs:
            context['pk'] = kwargs['pk']
        return render(request, "shipments.html", context)

class ManagerArticleListView(View):
    permission_classes = [permissions.IsAuthenticated, IsManagerUser]
    def get(self, request):
        return render(request, "article-list.html")

class ManagerArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        context = {
            "form" :  form
        }
        if 'pk' in kwargs:
            context['pk'] = kwargs['pk']

        print(context)
        return render (request, "article-detail.html", context)
