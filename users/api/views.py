from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework import generics

from users.models import *
from users.api.serializers import *
from users.api.permissions import *

import requests, json
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.shortcuts import render
from users.forms import LoginForm, CustomUserForm

# mostra dati utente
# solo per l'utente proprietario
class CurrentUserAPIView(APIView):
    permission_classes = [  permissions.IsAuthenticatedOrReadOnly,
                            isAccountOwner, 
                        ]

    def get(self, request):     # view caricata da una richiesta get dalla api
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data)    

# lista di tutti gli utenti
# solo admin
class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['POST',])
def registration_view(request):
    #print(request.data)

    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            print( "registered new user: ",user.username)

            #se la registrazione ha successo, reindirizza alla pagina principale
            return HttpResponseRedirect("/")
        else:
            errors = {}
            #salva errori del serializer in un dizionario
            if 'username' in serializer.errors: errors['username'] = serializer.errors['username'][0]
            if 'email' in serializer.errors: errors['email'] = serializer.errors['email'][0]
            if 'password' in serializer.errors: serializer.errors['password'][0]

            jsonMessages = json.dumps(errors)

            #ritorna un json di risposta con gli errori
            return JsonResponse(errors)

    # comportamento di default: ricarica la pagina
    return HttpResponseRedirect("/registration/")

def  get_logged_user_view(request):
    if request.method == 'GET':
        current_user = request.user
        message = {}
        if current_user is not None:
            message["user"] = current_user.username
        else:
            message["user"] = ""
        
        return JsonResponse(message)

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

    

        



    