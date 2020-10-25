from rest_framework import serializers
from users.models import *
from articles.api.serializers import ArticleDetailSerializer

# mostra dettagli di un singolo utente
class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [  "username",
                    "first_name",
                    "last_name",
                    "email",
                    "id",
                ]  

# mostra lista degli utenti
class UserListSerializer( serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [  "username",
                    "first_name",
                    "last_name",
                    "email",
                    "id",
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