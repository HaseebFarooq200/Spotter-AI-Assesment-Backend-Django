import os
from rest_framework import status
from rest_framework.test import APITestCase

from system_admin.models.user_model import CustomUser
from system_admin.modules.user.serializers import CustomUserSerialzer


class TestSetUp(APITestCase):
    def setUp(self):
        self.tokens = None
        self.headers = {"Authorization": ""}
        self.admin_user = {
            "Email": "admin@studentapply.com",
            "FirstName": "haider",
            "LastName": "majeed",
            "DateOfBirth": "1995-07-27",
            "password": "123456789",
        }

        if not CustomUser.objects.filter(Email=self.admin_user["Email"]).exists():
            self.custom_login(create_user=1)
        return super().setUp()

    def custom_login(self, email=None, password=None, create_user=0):
        if create_user:
            user_serializer = CustomUserSerialzer(data=self.admin_user)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        url = "/api/login/"
        login_request_data = {
            "Email": self.admin_user["Email"] if not email else email,
            "Password": self.admin_user["password"] if not password else password,
        }
        response = self.client.post(url, data=login_request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.headers[
            "Authorization"
        ] = f"Bearer {response.data['Result']['AccessToken']}"
        self.tokens = response.data["Result"]
