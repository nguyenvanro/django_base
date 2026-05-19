from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTestBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpass123!"
        cls.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password=cls.password,
        )

    def _login(self):
        url = reverse("authentication:login")
        resp = self.client.post(
            url,
            {"username": self.user.username, "password": self.password},
            format="json",
        )
        return resp.data["data"]

    def _assert_envelope(self, body, expected_status, message_substr=None):
        for key in ("status_code", "message", "data", "errors"):
            self.assertIn(key, body)
        self.assertEqual(body["status_code"], expected_status)
        if message_substr is not None:
            self.assertIn(message_substr, body["message"])


class LoginViewTests(AuthTestBase):
    def test_login_success(self):
        url = reverse("authentication:login")
        resp = self.client.post(
            url,
            {"username": self.user.username, "password": self.password},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "Login successful")
        self.assertIn("access", resp.data["data"])
        self.assertIn("refresh", resp.data["data"])
        self.assertIsNone(resp.data["errors"])

    def test_login_invalid_credentials(self):
        url = reverse("authentication:login")
        resp = self.client.post(
            url, {"username": "tester", "password": "wrong"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self._assert_envelope(resp.data, 401)
        self.assertIsNone(resp.data["data"])

    def test_login_missing_fields(self):
        url = reverse("authentication:login")
        resp = self.client.post(url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self._assert_envelope(resp.data, 400, "Validation")
        self.assertIn("username", resp.data["errors"])
        self.assertIn("password", resp.data["errors"])


class RefreshViewTests(AuthTestBase):
    def test_refresh_success(self):
        tokens = self._login()
        url = reverse("authentication:refresh")
        resp = self.client.post(url, {"refresh": tokens["refresh"]}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "Token refreshed")
        self.assertIn("access", resp.data["data"])

    def test_refresh_invalid_token(self):
        url = reverse("authentication:refresh")
        resp = self.client.post(url, {"refresh": "invalid.token.here"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self._assert_envelope(resp.data, 401)


class LogoutViewTests(AuthTestBase):
    def test_logout_blacklists_refresh_token(self):
        tokens = self._login()
        logout_url = reverse("authentication:logout")
        resp = self.client.post(logout_url, {"refresh": tokens["refresh"]}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "Logged out")

        # Reusing the blacklisted refresh must now fail
        refresh_url = reverse("authentication:refresh")
        resp2 = self.client.post(refresh_url, {"refresh": tokens["refresh"]}, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_401_UNAUTHORIZED)


class VerifyViewTests(AuthTestBase):
    def test_verify_valid_token(self):
        tokens = self._login()
        url = reverse("authentication:verify")
        resp = self.client.post(url, {"token": tokens["access"]}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "valid")

    def test_verify_invalid_token(self):
        url = reverse("authentication:verify")
        resp = self.client.post(url, {"token": "invalid.token"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self._assert_envelope(resp.data, 401)


class MeViewTests(AuthTestBase):
    def test_me_authenticated(self):
        tokens = self._login()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        url = reverse("authentication:me")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "Profile")
        self.assertEqual(resp.data["data"]["id"], self.user.id)
        self.assertEqual(resp.data["data"]["username"], self.user.username)
        self.assertEqual(resp.data["data"]["email"], self.user.email)

    def test_me_unauthenticated(self):
        url = reverse("authentication:me")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self._assert_envelope(resp.data, 401)
