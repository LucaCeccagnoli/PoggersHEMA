from rest_framework import serializers, mixins
from users.models import *
from articles.api.serializers import ArticleDetailSerializer

# mostra dettagli di un singolo utente
class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [  "username",
                    "email",
                    "id",
                ]  

# mostra lista degli utenti
class UserListSerializer( serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [  "username",
                    "email",
                    "id",
                ] 

# registrazione utente
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style= {'input_type' : 'password'}, write_only = True)

    class Meta:
        model = CustomUser
        fields = [  "username",
                    "email",
                    "password",
                    "password2",
                ] 

        extra_kwargs = {
            'password': {'write_only': True}    #nasconde la password
        }

    def save(self):        #ridefinire se bisogna controllare che le password corrispondano
        # ottiene dati registrazione 
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        # controllo password
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        # se le password sono uguali, aggiunge il nuovo utente al database
        user = CustomUser(
            username = username,
            email = email,
            password = password
        )
        user.set_password(password)
        user.save()
        return user

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
