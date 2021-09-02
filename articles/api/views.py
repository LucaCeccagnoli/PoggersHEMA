from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from rest_framework import generics, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token

from articles.api.serializers import *
from articles.api.permissions import *
from users.api.permissions import *
from articles.models import *

import random, json

# ottiene lista degli articoli, filtrando per categorie
# get
class ArticleListAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAdminUserOrReadonly]

    # eseguito in seguito a richiesta GET
    def get(self, request, *args, **kwargs):
        #ottieni categorie dall'url
        category = None
        sub_category = None
        if 'category' in kwargs : category = str(kwargs['category'])
        if 'sub_category' in kwargs : sub_category = str(kwargs['sub_category'])

        print("ArticleListAPIView: " ,category, type(category))

        self.queryset = Article.objects.all()
        if category is not None:
            self.queryset = self.queryset.filter(category__exact = category)
        if sub_category is not None:
            self.queryset = self.queryset.filter(sub_category__exact = sub_category)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# dettagli di un singolo articolo
# get, put / patch, delete
class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticated]

# creazione di un nuovo articolo
# post
class ArticleCreateAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticated, IsManagerUser]

# lista di tutti gli oggetti negli ordini, solo per superuser
# get, put/patch, delete
class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemListSerializer
    permission_classes = [permissions.IsAuthenticated]

# aggiunge un oggetto al carrello dell'utente
# post
class AddItemAPIView(APIView):
    def post(self, request):
        # messaggi da riportare al client
        response = {}
        token =  Token.objects.get(key = request.data['token'])
        user = CustomUser.objects.get(id = token.user.id)

        if user.is_authenticated:
            print(request.data)

            #controlla se l'utente ha un carrello
            order_query = Order.objects.filter(owner__exact = user.id).filter(is_ordered__exact = False)
            if not order_query:
                # crea un nuovo carrello
                cart = Order(ref_code = generate_ref_code(), owner = user)
                cart.save()
                print("creato nuovo carrello")
            else:
                cart = order_query.first()
                print("ottenuto carrello esistente")

            # ottieni tutti gli order item del carrello dell'utente che non sono stati spediti
            order_item_query  = OrderItem.objects.filter(order__exact = cart)

            # controlla se l'articolo ordinato è già nel carrello
            duplicate_item_query =  order_item_query.filter(article__exact = Article.objects.get(pk = request.data['pk']))
            if duplicate_item_query:
                # incrementa il count dell'order item
                item = duplicate_item_query.get()   # ottiene l'item trovato dalla query)

                if(item.amount >= 9):
                    response['error'] = "You can't order more copies of this article"
                else:
                    item.amount += 1
                    response['message'] = item.article.name + "in your order: " + str(item.amount)
                    item.save()
            # se l'articolo viene aggiunto per la prima volta
            else:
                try:
                    print("id carrello: ", cart.owner.username)
                    item = OrderItem(article = Article.objects.get(pk = request.data['pk']), order = cart)
                    item.save()

                    response['message'] = item.article.name +' added to cart'
                except IntegrityError:
                    response['message'] = 'This article is already part of your order'

            print("item id: ", item.pk)
            cart.save()

        else:
            response['error'] = 'You are not authenticated'

        return JsonResponse(response)


# ottiene un ordine data la chiave primaria del suo proprietario
# usato per mostrare all'utente gli oggetti nel suo carrello
# get
class OrderDetailApiView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated, isAccountOwner]
    serializer_class = OrderItemListSerializer

    def get(self, request, *args, **kwargs):
        # ottieni carrello dell'utente
        cart = Order.objects.filter(owner__exact = kwargs['pk']).filter(is_ordered__exact = False).get()
        # ottieni oggetti dell'ordine
        self.queryset = OrderItem.objects.filter(order__exact = cart)
        return self.list(request, *args, **kwargs)

# conferma un ordine e genera il relativo shipment
# post
class ConfirmOrderAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, isAccountOwner]
    def post(self, request, *args, **kwargs):
        messages = {}
        # ottieni carrello dell'utente
        order = Order.objects.filter(owner__exact = kwargs['pk']).filter(is_ordered__exact = False).get()
        # crea uno shipment relativo all'ordine
        shipment = Shipment(order = order, shipping_address = request.data['address'])
        # imposta l'ordine come ordinato
        order.is_ordered = True

        order.save()
        shipment.save()
        return JsonResponse(messages)

# ottieni lista shipment totali o per singolo utente
# get
class ShipmentListAPIView(generics.ListAPIView):
    serializer_class = ShipmentsListSerializer
    queryset = Shipment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsManagerUser]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            self.queryset = Shipment.objects.filter(order__owner__exact = kwargs['pk'])
            return self.list(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


# class ArticleDetailAPIView(APIView):
#     def get_object(self, pk):
#         article = get_object_or_404(Article, pk = pk)
#         return article

#     # ottiene dati su un singolo articolo
#     def get(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleDetailSerializer(article)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         if request.user.has_perm('articles.add_Article'):
#             article = self.get_object(pk)
#             serializer = ArticleDetailSerializer(article, data = request.data)
#             if serializer.is_valid():   # i dati vanno sempre validati prima di essere inseriti
#                 serializer.save()
#                 return Response(serializer.data)
#             else:
#                 return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(status = status.HTTP_403_FORBIDDEN)

# class ArticleDetailAPIView(generics.GenericAPIView,
#                             mixins.RetrieveModelMixin,
#                             mixins.UpdateModelMixin,
#                             mixins.DestroyModelMixin):

#     serializer_class = ArticleListSerializer

#     def get_queryset(self):
#         queryset = Article.objects.filter(pk)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         if request.user.has_perm(permissions.IsAdminUser):
#             return self.update(request, *args, **kwargs)
#         else:
#             return Response(status = status.HTTP_400_BAD_REQUEST)

# class ArticleListAPIView(APIView):
#     '''
#     Elenco degli articoli
#     '''
#     def get(self, request):
#         # ritorna solo gli articoli disponibili

#         # serializza il queryset in tipi di python
#         serializer = ArticleListSerializer(articles, many = True)
#         return Response(serializer.data)


def generate_ref_code():
    code = ''
    for i in range(15):
        code += str(random.randint(0,9))

    return code
