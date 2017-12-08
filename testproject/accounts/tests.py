import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("users:list")

    def test_invalid_password(self):
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "password",
            "confirm_password": "INVALID_PASSWORD"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_registration(self):
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "12312312",
            "confirm_password": "12312312"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_unique_username_validation(self):
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "12312312",
            "confirm_password": "12312312"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "email": "test2@testuser.com",
            "password": "12312312",
            "confirm_password": "12312312"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("users:login")

    def setUp(self):
        self.username = "bigshaq"
        self.email = "biq@shaq.com"
        self.password = "neva_hot"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "snowman"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "I_know"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("auth_token" in json.loads(response.content))


class UserLogoutAPIViewTestCase(APITestCase):
    url = reverse("users:logout")

    def setUp(self):
        self.username = "bigshaq"
        self.email = "biq@shaq.com"
        self.password = "neva_hot"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_logout(self):
        response = self.client.post(self.url)
        self.assertEqual(200, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token).exists())