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

def  get_logged_user_view(request):
    if request.method == 'GET':
        print(request.user)
        message = {}
        if request.user.is_authenticated:
            message["user"] = request.user.username
            message["id"] = request.user.id
            message["token"] = str(Token.objects.get(user_id = request.user.id))
        else:
            message["user"] = ""
            message["id"] = ""
            message["token"] = ""
            print("utente non autenticato")
        
        return JsonResponse(message)

@api_view(['POST',])
def user_test(request):
    if request.method == "POST":
        token =  Token.objects.get(key = request.data["token"])
        user = CustomUser.objects.get(id = token.user.id)
        print(user.id)
        return JsonResponse({ "user" : user})

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

    

        



    