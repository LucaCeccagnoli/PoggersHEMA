from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from articles.api.serializers import *
from articles.api.permissions import *

class ArticleListAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAdminUserOrReadonly]

    def get_queryset(self):
        queryset =  Article.objects.all()

        #ottieni parametri dall'url
        material = self.request.query_params.get("material", None)
        print(material)
        
        if material is not None:
            queryset = queryset.filter(material__exact=material)

        return queryset

    # eseguito in seguito a richiesta GET
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# ottiene dettagli su un singolo articolo
# utenti: solo richieste get
# amministratori: richieste get, put, patch

class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadonly]


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
#         articles = Article.objects.filter(stock__gte=0)

#         # serializza il queryset in tipi di python
#         serializer = ArticleListSerializer(articles, many = True)
#         return Response(serializer.data)

    