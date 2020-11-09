from django.urls import path, include
from articles.api.views import *

urlpatterns = [
    # get lista articoli, con o senza categorie
    path("article-list/", ArticleListAPIView.as_view()),   
    path("article-list/<str:category>", ArticleListAPIView.as_view()),
    path("article-list/<str:category>/<str:sub_category>", ArticleListAPIView.as_view()),

    # dettagli su un singolo articolo e creazione nuovo articolo
    path("article-detail/<int:pk>", ArticleDetailAPIView.as_view()),    
    path("article-detail/create/", ArticleCreateAPIView.as_view()),     

    # ottiene gli oggetti nel carrello di un utente data la sua chiave primaria
    path("orders/<int:pk>", OrderDetailApiView.as_view(), name = "order-list"),

    # conferma l'ordine nel carrello di un utente e genera il rispettivo shipment
    path("confirm-order/<int:pk>", ConfirmOrderAPIView.as_view(), name = "confirm-order"),

    # lista completa shipment, o quelli di un utente data la sua chiave primaria
    path("shipment-list/", ShipmentListAPIView.as_view() ),
    path("shipment-list/<int:pk>", ShipmentListAPIView.as_view()),

    # aggiungi articolo al carrello
    path("add-to-cart/", AddItemAPIView.as_view(), name = "add-to-cart"),   

    # lista oggetti negli ordini
    path("order-items/<int:pk>", OrderItemDetailAPIView.as_view(), name = "order-item-detail") 
]
