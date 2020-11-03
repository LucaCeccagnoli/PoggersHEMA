from django.urls import path, include
from articles.api.views import *

urlpatterns = [
    # lista completa articoli
    path("articles/", ArticleListAPIView.as_view()), 
    # articoli filtrati per categorie
    path("articles/<str:category>", ArticleListAPIView.as_view()), 
    path("articles/<str:category>/<str:sub_category>", ArticleListAPIView.as_view()),
    path("articles/<int:pk>", ArticleDetailAPIView.as_view()),          # singolo articolo
    path("orders/", OrderListAPIView.as_view(), name = "order-list"),   # lista completa ordini

    #carrello di un utente data la sua chiave primaria
    path("orders/<int:pk>", OrderDetailApiView.as_view(), name = "order-list"),   
    path("add-to-cart/", AddItemAPIView.as_view(), name = "add-to-cart"),   # aggiungi articolo al carrello
]