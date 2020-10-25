from django.urls import path
from users.api.views import *

urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name = "current-user"), # dati utente loggato
    path("user-list/", UserListAPIView.as_view(), name = "user-list"),  # lista utenti
    path("orders/", OrderListAPIView.as_view(), name = "order-list"),   # lista completa ordini
]