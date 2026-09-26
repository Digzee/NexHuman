from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class RegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse("register")

    def test_user_can_register(self):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "SecureTestPassword123!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get(email="test@example.com")

        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.check_password("SecureTestPassword123!"))
        self.assertNotIn("password", response.data)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            email="test@example.com",
            password="SecureTestPassword123!",
        )

        data = {
            "first_name": "Another",
            "last_name": "User",
            "email": "test@example.com",
            "password": "AnotherSecurePassword123!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_weak_password_is_rejected(self):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "weak@example.com",
            "password": "password",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_is_not_returned(self):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "private@example.com",
            "password": "SecureTestPassword123!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)

    def test_first_and_last_name_are_required(self):
        data = {
            "email": "noname@example.com",
            "password": "SecureTestPassword123!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertEqual(User.objects.count(), 0)