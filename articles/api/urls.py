from django.urls import path, include
from articles.api.views import *

urlpatterns = [
    path("articles/", ArticleListAPIView.as_view()),
    path("articles/<int:pk>", ArticleDetailAPIView.as_view()),
    path("orders/", OrderListAPIView.as_view(), name = "order-list"),   # lista completa ordini
]