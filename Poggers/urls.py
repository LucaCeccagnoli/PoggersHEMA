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

from core.views import IndexTemplateView
from users.forms import CustomUserForm

urlpatterns = [
    # pagina amministrazione
    path('admin/', admin.site.urls),

    #registrazione da browser con form personalizzato
    #se ha successo, porta alla homepage, con url "/"
    path('accounts/register/', 
        RegistrationView.as_view(
            form_class = CustomUserForm,
            success_url="/",
            ), 
        name = "django_registration_register" 
        ),

    # altri url di django_registration (non ancora utilizzati)
    path('accounts/', include("django_registration.backends.one_step.urls")),

    # url default di django_registration, url: "accounts/login"
    path('accounts/', include("django.contrib.auth.urls")),

    # api
    path('api/', include("users.api.urls")), 
    path('api/', include("articles.api.urls")),

    #login da browsable-api
    path('api-auth/', include("rest_framework.urls")), 

    #login tramite rest
    path('api/rest-auth/', include("rest_auth.urls")),   

    #registrazione tramite rest
    path('api/rest-auth/registration/',
        include("rest_auth.registration.urls")),    

    #homepage
    re_path(r"^.*$", IndexTemplateView.as_view(), name = "entry-point"),
]
