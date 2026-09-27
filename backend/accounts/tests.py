from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


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

class LoginTests(APITestCase):
    def setUp(self):
        self.url = reverse("login")

        self.user = User.objects.create_user(
            email="login@example.com",
            password="SecureTestPassword123!",
            first_name="Test",
            last_name="User",
        )

    def test_user_can_login_with_email_and_password(self):
        data = {
            "email": "login@example.com",
            "password": "SecureTestPassword123!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

        self.assertEqual(
            response.data["user"]["email"],
            "login@example.com",
        )

    def test_invalid_password_is_rejected(self):
        data = {
            "email": "login@example.com",
            "password": "WrongPassword123!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_unknown_email_is_rejected(self):
        data = {
            "email": "unknown@example.com",
            "password": "SecureTestPassword123!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_token_returns_new_access_token(self):
        login_response = self.client.post(
            self.url,
            {
                "email": "login@example.com",
                "password": "SecureTestPassword123!",
            },
            format="json",
        )

        refresh_token = login_response.data["refresh"]

        response = self.client.post(
            reverse("token_refresh"),
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_can_logout_and_blacklist_refresh_token(self):
        login_response = self.client.post(
            self.url,
            {
                "email": "login@example.com",
                "password": "SecureTestPassword123!",
            },
            format="json",
        )

        #access_token = login_response.data["access"]
        refresh_token = login_response.data["refresh"]

        #self.client.credentials(
        #    HTTP_AUTHORIZATION=f"Bearer {access_token}"
        #)

        logout_response = self.client.post(
            reverse("logout"),
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(
            logout_response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        #self.client.credentials()

        refresh_response = self.client.post(
            reverse("token_refresh"),
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

class CurrentUserTests(APITestCase):
    def setUp(self):
        self.url = reverse("current_user")

        self.user = User.objects.create_user(
            email="current@example.com",
            password="SecureTestPassword123!",
            first_name="Current",
            last_name="User",
        )

    def test_authenticated_user_can_retrieve_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "current@example.com")
        self.assertEqual(response.data["first_name"], "Current")
        self.assertEqual(response.data["last_name"], "User")
        self.assertNotIn("password", response.data)

    def test_unauthenticated_user_cannot_retrieve_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

class PasswordResetTests(APITestCase):
    def setUp(self):
        self.request_url = reverse("password_reset")
        self.confirm_url = reverse("password_reset_confirm")

        self.user = User.objects.create_user(
            email="reset@example.com",
            password="OldSecurePassword123!",
            first_name="Reset",
            last_name="User",
        )

    def test_password_reset_request_sends_email(self):
        response = self.client.post(
            self.request_url,
            {"email": "reset@example.com"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to,
            ["reset@example.com"],
        )
        self.assertIn(
            "/reset-password/",
            mail.outbox[0].body,
        )

    def test_unknown_email_returns_same_response(self):
        known_response = self.client.post(
            self.request_url,
            {"email": "reset@example.com"},
            format="json",
        )

        unknown_response = self.client.post(
            self.request_url,
            {"email": "unknown@example.com"},
            format="json",
        )

        self.assertEqual(
            known_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            unknown_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            known_response.data,
            unknown_response.data,
        )

    def test_password_can_be_reset_with_valid_token(self):
        uid = urlsafe_base64_encode(
            force_bytes(self.user.pk)
        )
        token = default_token_generator.make_token(
            self.user
        )

        response = self.client.post(
            self.confirm_url,
            {
                "uid": uid,
                "token": token,
                "password": "NewSecurePassword123!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password(
                "NewSecurePassword123!"
            )
        )
        self.assertFalse(
            self.user.check_password(
                "OldSecurePassword123!"
            )
        )

    def test_invalid_reset_token_is_rejected(self):
        uid = urlsafe_base64_encode(
            force_bytes(self.user.pk)
        )

        response = self.client.post(
            self.confirm_url,
            {
                "uid": uid,
                "token": "invalid-token",
                "password": "NewSecurePassword123!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password(
                "OldSecurePassword123!"
            )
        )

    def test_weak_new_password_is_rejected(self):
        uid = urlsafe_base64_encode(
            force_bytes(self.user.pk)
        )
        token = default_token_generator.make_token(
            self.user
        )

        response = self.client.post(
            self.confirm_url,
            {
                "uid": uid,
                "token": token,
                "password": "password",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password(
                "OldSecurePassword123!"
            )
        )