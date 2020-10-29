"""Poggers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path  #re_path permette di scrivere url con espressioni regolari
from django_registration.backends.one_step.views import RegistrationView # registrazione a step singolo

from users.forms import CustomUserForm  # form di registrazione customizzato
from users.views import *

from core.views import IndexTemplateView
from users.forms import CustomUserForm

from rest_auth import urls

# la registrazione tramite api avviene con rest-auth, mentre quella degli utenti con django-registration

urlpatterns = [
    # pagina amministrazione
    path('admin/', admin.site.urls),

    # url login e registrazione
    path("registration/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),

    # api
    path('api/', include("users.api.urls")), 
    path('api/', include("articles.api.urls")),

    # rest auth fornisce url per automatizzare l'autenticazione
    # api/rest-auth/login/ autentica l'utente con token e ne effettua il login
    path('api/rest-auth/', include("rest_auth.urls")), 

    #login da browsable-api
    path('api-auth/', include("rest_framework.urls")), 

    #homepage
    re_path(r"^.*$", IndexTemplateView.as_view(), name = "entry-point"),
]
