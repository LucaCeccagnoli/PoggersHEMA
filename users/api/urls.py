from django.urls import path, include
from users.api.views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name = "current-user"), # dati utente loggato
    path("user-list/", UserListAPIView.as_view(), name = "user-list"),  # lista utenti
    path("orders/", OrderListAPIView.as_view(), name = "order-list"),   # lista completa ordini

    path("registration/", RegistrationAPIView.as_view(), name = "registration"),   #pagina registrazione
    path("login/", login_view, name = "login"),          #pagina login

    path("auth/login", obtain_auth_token, name = "obtain-token"),
    path("provajson/", registration_view, name = "prova-json"),
]