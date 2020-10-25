from rest_framework import serializers
from articles.models import *

# dati da mostrare in una lista di articoli
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [  "pk",
                    "name",
                    "material",
                    "weight",
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