from django.urls import path, include
from articles.api.views import *

urlpatterns = [
    path("articles/", ArticleListAPIView.as_view()),                    # lista completa articoli
    path("articles/<int:pk>", ArticleDetailAPIView.as_view()),          # singolo articolo
    path("orders/", OrderListAPIView.as_view(), name = "order-list"),   # lista completa ordini

    #carrello di un utente data la sua chiave primaria
    path("orders/<int:pk>", OrderDetailApiView.as_view(), name = "order-list"),   
    path("add-to-cart/", AddItemAPIView.as_view(), name = "add-to-cart"),   # aggiungi articolo al carrello
]