from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product
class ShopAPITestCase:
    class TestCategory(APITestCase):
        url = reverse_lazy('category-list')
        def format_datetime(self, value):
            return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        def test_list(self):
            category = Category.objects.create(name='Fruits', active=True)
            Category.objects.create(name='Légumes', active=False)

            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)

            excepted = [
                {
                    'id': category.pk,
                    'name': category.name,
                    'date_created': self.format_datetime(category.date_created),
                    'date_updated': self.format_datetime(category.date_updated),
                }
            ]
            self.assertEqual(excepted, response.json())

        def test_create(self):
            self.assertFalse(Category.objects.exists())
            response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
            self.assertEqual(response.status_code, 405)
            self.assertFalse(Category.objects.exists())
        def test_detail(self):
            url_detail = reverse('category-detail',kwargs={'pk': self.category.pk})
            response = self.client.get(url_detail)
            self.assertEqual(response.status_code, 200)
            excepted = {
                'id': self.category.pk,
                'name': self.category.name,
                'date_created': self.format_datetime(self.category.date_created),
                'date_updated': self.format_datetime(self.category.date_updated),
                'products': self.get_product_detail_data(self.category.products.filter(active=True)),
            }
            self.assertEqual(excepted, response.json())
    class TestProduct(APITestCase):
        url = reverse_lazy('product-list')
        def test_list(self):
            product = Product.objects.create(name='Ananas', active=True)
            Product.objects.create(name='Banane', active=False)

            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
            excepted = [
                {
                    'id': product.pk,
                    'name': product.name,
                    'date_created': self.format_datetime(product.date_created),
                    'date_updated': self.format_datetime(product.date_updated),
                    'category': product.category_id
                }
            ]
            self.assertEqual(excepted, response.json())
        def test_create(self):
            self.assertFalse(Product.objects.exists())
            response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
            self.assertEqual(response.status_code, 405)
            self.assertFalse(Product.objects.exists())
