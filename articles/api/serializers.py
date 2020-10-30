from rest_framework import serializers
from articles.models import *

# dati da mostrare in una lista di articoli
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [  "pk",
                    "name",
                    "description",
                    "material",
                    "price",
                    "stock",
                ]  

# dati aggiuntivi mostrati sul dettaglio di un articolo
class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [  "pk",
                    "name",
                    "material",
                    "weight",
                    "price",
                    "stock",
                ]  

# mostra lista degli ordini
class OrderListSerializer(serializers.ModelSerializer):
    items = ArticleDetailSerializer(many=True, read_only = True)

    class Meta:
        model = Order
        fields = "__all__"
        # fields = [ sada , asda]
        # exclude = [ items ]

# mostra dettagli di un singolo ordine
class OrderDetailSerializer(serializers.ModelSerializer):
    items = ArticleDetailSerializer(many=True, read_only = True)

    class Meta:
        model = Order
        fields = "__all__"
