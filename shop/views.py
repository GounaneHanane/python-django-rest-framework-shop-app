from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from shop.models import Category, Product, Article
from shop.serializers import ArticleSerializer, CategoryListSerializer, ProductListSerializer, CategoryDetailSerializer, ProductDetailSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    

class CategoryAPIView(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    def get_queryset(self):
        return Category.objects.filter(active=True)
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
class ProductAPIView(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer
    def get_queryset(self):
        query_set = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            query_set = query_set.filter(category_id=category_id)
        return query_set
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
class ArticleAPIView(ModelViewSet): 
    serializer_class = ArticleSerializer
    def get_queryset(self):
        query_set = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            query_set = query_set.filter(product_id=product_id)
        return query_set
    

