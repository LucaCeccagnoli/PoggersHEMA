from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import generics

from users.models import *
from users.api.serializers import *
from users.api.permissions import *

#import per il form di login
import requests
from django.http import HttpResponseRedirect
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

# lista di tutti gli ordini effettuati da tutti gli utenti
# solo admin
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderListSerializer


class RegistrationAPIView(APIView):
    def get(self, request):
        form = CustomUserForm()
        context = {
            "form": form
        }
        return render(request, "registration.html", context)

    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            data = {
                "username" : form.cleaned_data["username"],
                "email" : form.cleaned_data["email"],
                "password" : form.cleaned_data["password1"],
                "password2" : form.cleaned_data["password2"]
            }

            serializer = RegistrationSerializer(data = data)
            if serializer.is_valid():
                pass
                user = serializer.save()
                print( "registered new user: ",user.username)
            else:
                print("serializer error: ", serializer.errors)
            
        else:
            print("invalid registration form: \n", form.errors)

        return HttpResponseRedirect("/api/registration/")

# da usare quando sarà possibile inviare json dal client
@api_view(['POST',])
def registration_view(request):
    print(request.data)
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            print( "registered new user: ",user.username)
        else:
            print("serializer error: ", serializer.errors)
    
    return HttpResponseRedirect("/api/registration/")

@ensure_csrf_cookie
def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "login.html", context)

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                "username" : form.cleaned_data["username"],
                "password" : form.cleaned_data["password"]
            }

            response = requests.post("http://127.0.0.1:8000//api/auth/login/", data = data)
            print("status code: ", response.status_code)
            print(response)
            #print("response: ", response.json())
            
        else:
            print("invalid registration form: \n", form.errors)
            return HttpResponseRedirect("/api/login/")

    return HttpResponseRedirect("/")


from rest_framework.authtoken.views import ObtainAuthToken

def seepw(self):
    username = "user1"
    u = CustomUser.objects.get(username__exact = username)
    print(u.password)
    return HttpResponseRedirect("/")


    

        



    