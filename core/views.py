from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import generics, mixins, permissions
from users.models import CustomUser
from core.forms import *
from users.api.permissions import *

# homepage
class IndexTemplateView(TemplateView):

    def get_template_names(self):
        template_name = "index.html"
        return template_name

# pagina registrazione utente
class RegistrationView(View):
    def get(self, request):
        form = CustomUserForm()
        context = {
            "form": form
        }
        return render(request, "registration.html", context)

    def post(self, request):
        return HttpResponseRedirect("/registration")

# pagina di login
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, "login.html", context)

    def post(self, request):
        return HttpResponseRedirect("/login/")

# pagina del carrello utente
# solo per utenti loggati
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

# pagina dell'account utente
# solo per utenti loggati
class AccountView(View):
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

# lista degli utenti
# solo per amministratori
class ManagerUserListView(View):
    def get(self, request):
        if (
                CustomUser.objects.filter(is_admin__exact = True).filter(id__exact = request.user.id) 
                and request.user.is_authenticated
            ):
            return render (request, "user-list.html")
        else:
            return HttpResponseRedirect("/login/")

# lista degli shipment
# solo per amministratori
class ShipmentsListView(View):
    def get(self, request, *args, **kwargs):
        # solo per amministratori, altrimenti redirigi a login
        if (
                CustomUser.objects.filter(is_admin__exact = True).filter(id__exact = request.user.id) 
                and request.user.is_authenticated
            ):
            context={}
            if 'pk' in kwargs:
                context['pk'] = kwargs['pk']
            return render(request, "shipments.html", context)
        else:
            return HttpResponseRedirect("/login/")

# editor degli articoli
# solo per amministratori
class ManagerArticleListView(View):
    def get(self, request):
        # solo per amministratori, altrimenti redirigi a login
        if (
                CustomUser.objects.filter(is_admin__exact = True).filter(id__exact = request.user.id) 
                and request.user.is_authenticated
            ):
            return render(request, "article-list.html")
        else:
             return HttpResponseRedirect("/login/")

# pagina per aggiungere o modificare un articolo
# solo per amministratori
class ManagerArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        # solo per amministratori, altrimenti redirigi a login
        if (
                CustomUser.objects.filter(is_admin__exact = True).filter(id__exact = request.user.id) 
                and request.user.is_authenticated
            ):
            form = ArticleForm()
            context = {
                "form" :  form
            }
            if 'pk' in kwargs:
                context['pk'] = kwargs['pk']

            print(context)
            return render (request, "article-detail.html", context)
        else:
            return HttpResponseRedirect("/login/")





