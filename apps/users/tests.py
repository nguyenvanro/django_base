from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserCRUDTestBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpass123!"
        cls.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password=cls.password,
        )
        cls.other = User.objects.create_user(
            username="other",
            email="other@example.com",
            password=cls.password,
        )
        cls.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password=cls.password,
            is_staff=True,
        )

    def _auth_as(self, user):
        self.client.force_authenticate(user=user)

    def _assert_envelope(self, body, expected_status, message_substr=None):
        for key in ("status_code", "message", "data", "errors"):
            self.assertIn(key, body)
        self.assertEqual(body["status_code"], expected_status)
        if message_substr is not None:
            self.assertIn(message_substr, body["message"])


class UserRegisterTests(UserCRUDTestBase):
    def test_register_success(self):
        url = reverse("users:user-list")
        resp = self.client.post(
            url,
            {
                "username": "newbie",
                "email": "newbie@example.com",
                "password": "StrongP@ss123",
                "first_name": "New",
                "last_name": "Bie",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self._assert_envelope(resp.data, 201, "User registered")
        self.assertEqual(resp.data["data"]["username"], "newbie")
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_register_weak_password(self):
        url = reverse("users:user-list")
        resp = self.client.post(
            url,
            {"username": "weak", "email": "weak@example.com", "password": "123"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self._assert_envelope(resp.data, 400, "Validation")
        self.assertIn("password", resp.data["errors"])

    def test_register_duplicate_username(self):
        url = reverse("users:user-list")
        resp = self.client.post(
            url,
            {
                "username": self.user.username,
                "email": "dup@example.com",
                "password": "StrongP@ss123",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", resp.data["errors"])


class UserListTests(UserCRUDTestBase):
    def test_list_requires_admin(self):
        self._auth_as(self.user)
        url = reverse("users:user-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self._assert_envelope(resp.data, 403)

    def test_list_unauthenticated(self):
        url = reverse("users:user-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_admin_ok(self):
        self._auth_as(self.admin)
        url = reverse("users:user-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "Users fetched")
        page = resp.data["data"]
        for key in ("count", "next", "previous", "results"):
            self.assertIn(key, page)
        usernames = {row["username"] for row in page["results"]}
        self.assertIn(self.user.username, usernames)
        self.assertIn(self.admin.username, usernames)


class UserRetrieveTests(UserCRUDTestBase):
    def test_retrieve_own(self):
        self._auth_as(self.user)
        url = reverse("users:user-detail", args=[self.user.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "User fetched")
        self.assertEqual(resp.data["data"]["id"], self.user.id)

    def test_retrieve_other_forbidden(self):
        self._auth_as(self.user)
        url = reverse("users:user-detail", args=[self.other.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_admin_can_view_any(self):
        self._auth_as(self.admin)
        url = reverse("users:user-detail", args=[self.user.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)



class UserUpdateTests(UserCRUDTestBase):
    def test_patch_own_profile(self):
        self._auth_as(self.user)
        url = reverse("users:user-detail", args=[self.user.id])
        resp = self.client.patch(url, {"first_name": "Updated"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "User updated")
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_patch_other_forbidden(self):
        self._auth_as(self.user)
        url = reverse("users:user-detail", args=[self.other.id])
        resp = self.client.patch(url, {"first_name": "Hack"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteTests(UserCRUDTestBase):
    def test_delete_requires_admin(self):
        self._auth_as(self.user)
        url = reverse("users:user-detail", args=[self.other.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=self.other.id).exists())

    def test_delete_admin_ok(self):
        self._auth_as(self.admin)
        url = reverse("users:user-detail", args=[self.other.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "User deleted")
        self.assertFalse(User.objects.filter(pk=self.other.id).exists())


class ChangePasswordTests(UserCRUDTestBase):
    def _url(self, user):
        return reverse("users:user-change-password", args=[user.id])

    def test_change_own_password_success(self):
        self._auth_as(self.user)
        resp = self.client.post(
            self._url(self.user),
            {"old_password": self.password, "new_password": "BrandNewP@ss1"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_envelope(resp.data, 200, "Password changed")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("BrandNewP@ss1"))

    def test_change_password_wrong_old(self):
        self._auth_as(self.user)
        resp = self.client.post(
            self._url(self.user),
            {"old_password": "wrong-old", "new_password": "BrandNewP@ss1"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self._assert_envelope(resp.data, 400, "Old password is incorrect")
        self.assertIn("old_password", resp.data["errors"])

    def test_change_password_weak_new(self):
        self._auth_as(self.user)
        resp = self.client.post(
            self._url(self.user),
            {"old_password": self.password, "new_password": "123"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self._assert_envelope(resp.data, 400, "Validation")
        self.assertIn("new_password", resp.data["errors"])

    def test_change_password_other_forbidden(self):
        self._auth_as(self.user)
        resp = self.client.post(
            self._url(self.other),
            {"old_password": self.password, "new_password": "BrandNewP@ss1"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
