from rest_framework import status
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from ads.models import Ad
from ads.views import AdsViewSet
from users.models import CustomUser


class AdsTest(APITestCase):
    def setUp(self):
        """
        Set up initial data and users for testing.
        """
        self.factory = APIRequestFactory()

        # Owner of the ad
        self.ad_owner = CustomUser.objects.create(
            username="ad_owner", email="ad_owner@mail.ru"
        )
        self.ad_owner.set_password("12345678")
        self.ad_owner.save()

        # Normal user who doesn't own any ads
        self.normal_user = CustomUser.objects.create(
            username="normal_user", email="normal_user@mail.ru"
        )
        self.normal_user.set_password("12345678")
        self.normal_user.save()

        # Initial ad data
        self.ad_data = {
            "title": "Продам телефон",
            "description": "Продам iphone 16",
            "category": "Техника",
            "condition": "used",
        }

        # Creation of two ads owned by the owner
        self.ad = Ad.objects.create(
            title="Продам телефон",
            description="Продам iphone 16",
            category="Техника",
            condition="used",
            user=self.ad_owner,
        )

        Ad.objects.create(
            title="Куплю телефон",
            description="Продам iphone 16",
            category="Техника",
            condition="used",
            user=self.ad_owner,
        )
        self.ad_to_delete = Ad.objects.get(
            title="Куплю телефон",
            description="Продам iphone 16",
            category="Техника",
            condition="used",
            user=self.ad_owner,
        )

        # Updated ad data
        self.update_ad_data = {
            "id": 4,
            "title": "Продам телефон",
            "description": "Продам iphone 16",
            "image_url": "",
            "category": "Техника",
            "condition": "new",
            "user": self.ad_owner.id,
        }

    def test_create_ad(self):
        """
        Test creating a new ad through an authorized user.
        """
        request = self.factory.post("ads/", data=self.ad_data)
        force_authenticate(request, user=self.ad_owner)
        response = AdsViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Ad.objects.filter(title="Продам телефон").exists())

    def test_retrieve_ad(self):
        """
        Test retrieving an ad by its ID.
        """
        request = self.factory.get(f"ads/{self.ad.id}/", json=self.ad)
        force_authenticate(request, user=self.ad_owner)
        response = AdsViewSet.as_view({"get": "retrieve"})(request, pk=self.ad.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ad_with_root(self):
        """
        Test updating an ad when logged in as the owner.
        """
        request = self.factory.put(f"ads/{self.ad.id}/", data=self.update_ad_data)
        force_authenticate(request, user=self.ad_owner)
        response = AdsViewSet.as_view({"put": "update"})(request, pk=self.ad.id)
        expected_response = {
            k: v
            for k, v in self.update_ad_data.items()
            if k not in ["id", "created_at"]
        }
        if "data" in response.data:
            actual_response = {
                k: v
                for k, v in response.data["data"].items()
                if k not in ["id", "created_at"]
            }
        else:
            actual_response = {
                k: v for k, v in response.data.items() if k not in ["id", "created_at"]
            }
        self.assertDictEqual(expected_response, actual_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Ad.objects.filter(title="Продам телефон").exists())

    def test_update_ad_without_root(self):
        """
        Test updating an ad by another user (should be forbidden).
        """
        request = self.factory.put(f"ads/{self.ad.id}/", data=self.update_ad_data)
        force_authenticate(request, user=self.normal_user)
        response = AdsViewSet.as_view({"put": "update"})(request, pk=self.ad.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ad(self):
        """
        Test successful deletion of an ad by its owner.
        """
        request = self.factory.delete(
            f"ads/{self.ad_to_delete.id}/", json=self.ad_to_delete
        )
        force_authenticate(request, user=self.ad_owner)
        response = AdsViewSet.as_view({"delete": "destroy"})(
            request, pk=self.ad_to_delete.id
        )
        self.ad_to_delete.delete()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ad.objects.filter(title="Куплю телефон").exists())
