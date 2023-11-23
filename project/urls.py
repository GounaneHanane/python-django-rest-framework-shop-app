from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from shop.views import CategoryAPIView, ProductAPIView, ArticleAPIView

router = routers.SimpleRouter()
router.register('category', CategoryAPIView, basename='category')
router.register('product', ProductAPIView, basename='product')
router.register('article', ArticleAPIView, basename='article')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/',include(router.urls))
]
