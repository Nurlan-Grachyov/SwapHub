from http.client import responses

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from ads.models import Product
from ads.views import AdsViewSet
from users.models import CustomUser


class ProductsTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.product_owner = CustomUser.objects.create(
            username="owner", email="owner@mail.ru"
        )
        self.product_owner.set_password("12345678")
        self.product_owner.save()

        self.normal_user = CustomUser.objects.create(
            username="normal_user", email="normal_user@mail.ru"
        )
        self.normal_user.set_password("12345678")
        self.normal_user.save()

        self.product_data = {
            "title": "Продам телефон",
            "description": "Продам iphone 16",
            "category": "Техника",
            "condition": "used"
        }

        self.product = Product.objects.create(title="Продам телефон", description="Продам iphone 16",
                                              category="Техника", condition="used", user=self.product_owner,
                                              )

        Product.objects.create(title="Куплю телефон", description="Продам iphone 16",
                                              category="Техника", condition="used", user=self.product_owner)
        self.product_to_delete = Product.objects.get(title="Куплю телефон", description="Продам iphone 16",
                                              category="Техника", condition="used", user=self.product_owner)

        self.update_product_data = {
            'id': 4,
            'title': 'Продам телефон',
            'description': 'Продам iphone 16',
            'image_url': "",
            'category': 'Техника',
            'condition': 'new',
            'user': self.product_owner.id
        }

    def test_create_product(self):
        request = self.factory.post("ads/", data=self.product_data)

        force_authenticate(request, user=self.product_owner)
        response = AdsViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Product.objects.filter(title="Продам телефон").exists())

    def test_retrieve_habit(self):
        request = self.factory.get(f"ads/{self.product.id}/", json=self.product)
        force_authenticate(request, user=self.product_owner)
        response = AdsViewSet.as_view({"get": "retrieve"})(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_with_root(self):
        request = self.factory.put(
            f"ads/{self.product.id}/", data=self.update_product_data
        )
        force_authenticate(request, user=self.product_owner)
        response = AdsViewSet.as_view({"put": "update"})(request, pk=self.product.id)
        expected_response = {k: v for k, v in self.update_product_data.items() if k not in ['id', 'created_at']}
        if 'data' in response.data:
            actual_response = {k: v for k, v in response.data['data'].items() if k not in ['id', 'created_at']}
        else:
            actual_response = {k: v for k, v in response.data.items() if k not in ['id', 'created_at']}
        self.assertDictEqual(expected_response, actual_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Product.objects.filter(title="Продам телефон").exists())

    def test_update_product_without_root(self):
        request = self.factory.put(
            f"ads/{self.product.id}/", data=self.update_product_data
        )
        force_authenticate(request, user=self.normal_user)
        response = AdsViewSet.as_view({"put": "update"})(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product(self):
        request = self.factory.delete(f"ads/{self.product_to_delete.id}/", json=self.product_to_delete)
        force_authenticate(request, user=self.product_owner)
        response = AdsViewSet.as_view({"delete": "destroy"})(
            request, pk=self.product_to_delete.id
        )
        self.product_to_delete.delete()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(title="Куплю телефон").exists())
