from django.urls import path, include
from articles.api.views import *

urlpatterns = [
    # lista completa articoli
    path("article-list/", ArticleListAPIView.as_view()), 
    # articoli filtrati per categorie
    path("article-list/<str:category>", ArticleListAPIView.as_view()), 
    path("article-list/<str:category>/<str:sub_category>", ArticleListAPIView.as_view()),
    path("article-detail/<int:pk>", ArticleDetailAPIView.as_view()),          # singolo articolo
    path("orders/", OrderListAPIView.as_view(), name = "order-list"),   # lista completa ordini
                                                                        # con chiave primaria per ottenerne un singolo

    # ottiene gli oggetti nel carrello di un utente data la sua chiave primaria
    path("orders/<int:pk>", OrderDetailApiView.as_view(), name = "order-list"),  
    # conferma l'ordine nel carrello di un utente e genera il rispettivo shipment
    path("confirm-order/<int:pk>", ConfirmOrderAPIView.as_view(), name = "confirm-order"),
    path("add-to-cart/", AddItemAPIView.as_view(), name = "add-to-cart"),   # aggiungi articolo al carrello

    path("order-items/<int:pk>", OrderItemDetailAPIView.as_view(), name = "order-item-detail") # lista oggetti negli ordini
]