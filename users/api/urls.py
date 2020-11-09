from django.urls import path, include
from users.api.views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name = "current-user"), # dati utente loggato
    path("user-list/", UserListAPIView.as_view(), name = "user-list"),  # lista utenti
    path("user-detail/<int:pk>/", UserDetailAPIView.as_view() , name = "make-manager"), #modifica singoli utenti

    path("obtain-token/", obtain_auth_token, name = "obtain-token"),    # ottieni token utente
    path("register-user/", registration_view, name = "register-user"),  # registrazione nuovo utente

    path("change-credentials/", change_credentials, name = "change-credentials"),   #cambio credenziali
    path("get-logged-user/", get_logged_user_view, name = "get-logged-user"),       # ottieni l'utente loggato
]