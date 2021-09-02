from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from users.models import *
from users.api.serializers import *
from users.api.permissions import *

import requests, json
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.shortcuts import render
from core.forms import LoginForm, CustomUserForm

# mostra dati utente, solo per l'utente proprietario
# get
class CurrentUserAPIView(APIView):
    permission_classes = [  permissions.IsAuthenticatedOrReadOnly,
                            isAccountOwner, 
                        ]

    def get(self, request):     # view caricata da una richiesta get dalla api
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data)    

# per promuovere/cancellare un utente
# get, patch, delete
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDisplaySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# lista di tutti gli utenti
# get
class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerUser]

# registrazione di un nuovo utente
@api_view(['POST',])
def registration_view(request):
    print(request.data)
    context = {}

    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            print( "registered new user: ",user.username)

            context["registration"] = "Registrated successfully as " + user.username
            
        else:
            #salva errori del serializer in un dizionario
            if 'username' in serializer.errors: context['username'] = serializer.errors['username'][0]
            if 'email' in serializer.errors: context['email'] = serializer.errors['email'][0]
            if 'password' in serializer.errors: context['password'] = serializer.errors['password'][0]

    return JsonResponse(context)

# ottiene informazioni sull'utente loggato
@permission_classes([IsAuthenticated])
def  get_logged_user_view(request):
    if request.method == 'GET':
        message = {}
        if request.user.is_authenticated:
            message["user"] = request.user.username
            message['email'] = request.user.email
            message["id"] = request.user.id
            message["admin"] = request.user.is_admin
            message["token"] = str(Token.objects.get(user_id = request.user.id))
        else:
            message["user"] = ""
            message['email'] = ""
            message["id"] = ""
            message["admin"] = False
            message["token"] = ""
            print("utente non autenticato")
        
        return JsonResponse(message)

# cambio delle credenziali da parte di un utente
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def change_credentials(request):
    if request.method == "POST":
        #ottieni l'utente
        response = {}
        user = CustomUser.objects.filter(id__exact = request.user.id).get()
        #cambio username
        if 'username' in request.data:
            # se lo stesso username non è già presente
            if not CustomUser.objects.filter(username__exact = request.data['username']):
                user.username = request.data['username']
                user.save()
                response["username_success"] = "username updated succesfully"
            else:
                response["username_errors"] = "this username already exists"
        #cambio email
        if 'email' in request.data:
            # se la stessa email non è già presente
            if not CustomUser.objects.filter(email__exact = request.data['email']):
                user.email = request.data['email']
                user.save()
                response["email_success"] = "email address updated succesfully"
            else:
                response["email_errors"] = "this email already exists"

        #cambio password
        if 'password_new' in request.data:
            # se la password attuale è corretta, assegna la nuova, altrimenti ritorna errore
            if user.check_password(request.data['password_current']):
                user.set_password(request.data['password_new'])
                user.save()
                response["password_success"] = "password updated succesfully"
            else:
                response['password_errors'] = 'you current password doesn\' t match'

        return JsonResponse(response)
            
'''
@api_view(['POST',])
def login_view(request):
    if request.method == "POST":
        # ottieni dati utente e token
        username = request.data.get('username')
        password = request.data.get('password')
        token = request.data.get('token')
        errors = {}
        
        # controlla se l'utente esiste, se username e password sono corretti, se il token è corretto
        user = authenticate(request, username = username, password = password)
        if user is not None:
            if (user.username != username) or (user.password != password):
                errors['credentials'] = "incorrect username or password"
            else:
                if Token.objects.filter(key__exact = token ).filter(user__exact = username) is None: 
                    errors['token'] = "incorrect authentication token"
                else:
                    login(request, user)
                    return HttpResponseRedirect("/")
        else:
            errors['account'] = "this account does not exist"

        if len(errors) > 0:
            #ritorna gli errori come json
            return JsonResponse(json.dumps(errors))

    return HttpResponseRedirect("/login/")
'''

    

        



    