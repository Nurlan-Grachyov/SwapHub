from rest_framework import status
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from ads.models import Ad
from ads.views import AdsViewSet
from change.models import ExchangeOffer
from change.views import ChangeViewSet
from users.models import CustomUser


class ChangeTest(APITestCase):
    def setUp(self):
        """
        Initializes test environment by creating users, advertisements, and exchange offers.
        """
        self.factory = APIRequestFactory()

        # Creating seller
        self.sender = CustomUser.objects.create(
            username="ad_sender", email="ad_sender@mail.ru"
        )
        self.sender.set_password("12345678")
        self.sender.save()

        # Creating buyer
        self.receiver = CustomUser.objects.create(
            username="received", email="received@mail.ru"
        )
        self.receiver.set_password("12345678")
        self.receiver.save()

        # Data for seller's advertisement
        self.ad_sender_data = {
            "title": "Продам телефон",
            "description": "Продам iphone 16",
            "category": "Техника",
            "condition": "used",
            "user": self.sender,
        }

        # Create seller's advertisement
        self.ad_sender = Ad.objects.create(**self.ad_sender_data)

        # Data for buyer's advertisement
        self.ad_receiver_data = {
            "title": "Куплю телефон",
            "description": "Продам iphone 16",
            "category": "Техника",
            "condition": "used",
            "user": self.receiver,
        }

        # Create buyer's advertisement
        self.ad_receiver = Ad.objects.create(**self.ad_receiver_data)

        # Data for exchange offer
        self.change_data = {
            "ad_sender": self.ad_sender.id,
            "ad_receiver": self.ad_receiver.id,
            "sender_user": self.sender.id,
            "receiver_user": self.receiver.id,
            "comment": "Привет",
            "status": "pending",
        }

        # Create exchange offer
        self.change = ExchangeOffer.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            sender_user=self.sender,
            receiver_user=self.receiver,
            comment="Привет",
            status="pending",
        )

        self.update_change_data = {
            "ad_sender": self.ad_sender.id,
            "ad_receiver": self.ad_receiver.id,
            "sender_user": self.sender.id,
            "receiver_user": self.receiver.id,
            "comment": "Привет",
            "status": "pending",
        }

    def test_create_change(self):
        """
        Tests creation of an exchange offer via authenticated user.
        """
        request = self.factory.post("change/", data=self.change_data)
        force_authenticate(request, user=self.receiver)
        response = ChangeViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ExchangeOffer.objects.filter(comment="Привет").exists())

    def test_retrieve_change(self):
        """
        Tests retrieval of an exchange offer using its unique identifier.
        """
        request = self.factory.get(f"change/{self.change.id}/", json=self.change)
        force_authenticate(request, user=self.receiver)
        response = ChangeViewSet.as_view({"get": "retrieve"})(
            request, pk=self.change.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_change_with_root(self):
        """
        Tests updating an exchange offer with authentication.
        """
        request = self.factory.put(
            f"change/{self.change.id}/", data=self.update_change_data
        )
        force_authenticate(request, user=self.receiver)
        response = ChangeViewSet.as_view({"put": "update"})(request, pk=self.change.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ExchangeOffer.objects.filter(comment="Привет").exists())

    def test_update_change_without_root(self):
        """
        Tests unauthorized attempt to update an exchange offer without authentication.
        """
        request = self.factory.put(
            f"change/{self.change.id}/", data=self.update_change_data
        )
        response = ChangeViewSet.as_view({"put": "update"})(request, pk=self.change.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_change(self):
        """
        Tests deleting an exchange offer, which should result in method not allowed error.
        """
        request = self.factory.delete(f"change/{self.change.id}/", json=self.change)
        force_authenticate(request, user=self.receiver)
        response = ChangeViewSet.as_view({"delete": "destroy"})(
            request, pk=self.change.id
        )
        self.change.delete()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
