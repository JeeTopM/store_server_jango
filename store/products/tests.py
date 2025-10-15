from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from products.models import Product, ProductCategory


class BaseProductViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']
    template_name = 'products/products.html'
    expected_title = 'Store - Каталог'

    def _common_assertions(self, response, expected_queryset):
        """Общие проверки для всех продуктовых представлений"""
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], self.expected_title)
        self.assertTemplateUsed(response, self.template_name)

        paginate_by = response.context_data['paginator'].per_page
        expected_products = list(expected_queryset[:paginate_by])
        self.assertEqual(list(response.context_data['object_list']), expected_products)


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductListViewTestCase(BaseProductViewTestCase):

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        products = Product.objects.all()

        self._common_assertions(response, products)

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        products = Product.objects.all()

        self._common_assertions(response, products)


class ProductListViewTestCaseAlternative(BaseProductViewTestCase):
    def _get_test_cases(self):
        return [
            (reverse('products:index'), Product.objects.all()),
            (
                reverse('products:category', kwargs={'category_id': ProductCategory.objects.first().id}),
                Product.objects.all()  # или Product.objects.filter(category=category)
            )
        ]

    def test_all_views(self):
        for path, expected_queryset in self._get_test_cases():
            with self.subTest(path=path):
                response = self.client.get(path)
                self._common_assertions(response, expected_queryset)



'''
from http import HTTPStatus
from itertools import product
from unicodedata import category

from django.test import TestCase
from django.urls import reverse

import products
from products.models import Product, ProductCategory


# Create your tests here.
class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        products = Product.objects.all()
        paginate_by = response.context_data['paginator'].per_page
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data['object_list']), list(products[:paginate_by]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)
        paginate_by = response.context_data['paginator'].per_page
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(
            list(response.context_data['object_list']),
            list(Product.objects.all()[:paginate_by])
        )
'''