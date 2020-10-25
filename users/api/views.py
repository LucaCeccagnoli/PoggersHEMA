from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics

from users.models import *
from users.api.serializers import *
from users.api.permissions import *

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




    