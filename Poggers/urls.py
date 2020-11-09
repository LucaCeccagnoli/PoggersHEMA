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
from django.urls import path, include, re_path  
from django_registration.backends.one_step.views import RegistrationView 

from core.forms import CustomUserForm  # form di registrazione customizzato
from core.views import *

from rest_auth import urls

# la registrazione tramite api avviene con rest-auth, mentre quella degli utenti con django-registration

urlpatterns = [

    # pagine accessibili agli utenti
    path('', IndexTemplateView.as_view(), name = "entry-point"),# homepage 
    path("registration/", RegistrationView.as_view()),          # registrazione
    path("login/", LoginView.as_view()),                        # login
    path("shopping-cart/", ShoppingCartView.as_view()),         # carrello dell'utente
    path("account/", AccountView.as_view(), name = "account"),  # cambio username e email

    # pagine accessibili agli amministratori
    path('manager/user-list/', ManagerUserListView.as_view()),                      # lista degli utenti
    path('manager/article-list/', ManagerArticleListView.as_view()),                # lista degli articoli
    path('manager/article-detail/', ManagerArticleDetailView.as_view()),            # aggiunta di un articolo
    path('manager/article-detail/<int:pk>', ManagerArticleDetailView.as_view()),    # modifica di un articolo
    path("manager/shipments/", ShipmentsListView.as_view()),                        # lista degli shipment
    path("manager/shipments/<int:pk>/", ShipmentsListView.as_view()),               # shipment di un utente

    # include gli endpoint della API
    path('api/', include("users.api.urls")),
    path('api/', include("articles.api.urls")),

    # endpoint forniti da rest-auth
    # /login, /logout
    path('api/rest-auth/', include("rest_auth.urls")),

    # pagina amministrazione, accessibile solo al superuser
    path('admin/', admin.site.urls),

    # login da browsable-api, per superuser
    path('api-auth/', include("rest_framework.urls")),
]
