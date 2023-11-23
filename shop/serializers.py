from rest_framework import serializers
 
from shop.models import Category, Product, Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'name', 'date_created', 'price', 'product']
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created']
class ProductDetailSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']
    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        response = ArticleSerializer(queryset, many=True)
        return response.data

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'products']
    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data