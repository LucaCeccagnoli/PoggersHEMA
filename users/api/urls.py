from django.urls import path, include
from users.api.views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name = "current-user"), # dati utente loggato
    path("user-list/", UserListAPIView.as_view(), name = "user-list"),  # lista utenti
    path("orders/", OrderListAPIView.as_view(), name = "order-list"),   # lista completa ordini

    path("obtain-token/", obtain_auth_token, name = "obtain-token"),    # ottieni token utente
    path("register-user/", registration_view, name = "register-user"),  # registrazione nuovo utente

    path("get-logged-user/", get_logged_user_view, name = "get-logged-user"),
]