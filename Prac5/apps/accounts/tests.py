from django.test import TestCase
from rest_framework.test import APIClient

from .models import User


class AuthTests(TestCase):
    def setUp(self):
        self.api = APIClient()

    def test_register_returns_tokens(self):
        r = self.api.post("/api/auth/register/", {
            "username": "anna", "password": "secret123", "password2": "secret123",
            "first_name": "Анна", "last_name": "Орлова", "position": "librarian",
        }, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertIn("access", r.data)
        self.assertTrue(User.objects.get(username="anna").check_password("secret123"))

    def test_register_password_mismatch(self):
        r = self.api.post("/api/auth/register/", {
            "username": "bob", "password": "secret123", "password2": "other123",
        }, format="json")
        self.assertEqual(r.status_code, 400)

    def test_login_and_me(self):
        User.objects.create_user("ivan", password="secret123")
        r = self.api.post("/api/auth/login/", {"username": "ivan", "password": "secret123"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.api.credentials(HTTP_AUTHORIZATION="Bearer " + r.data["access"])
        me = self.api.get("/api/auth/me/")
        self.assertEqual(me.data["username"], "ivan")

    def test_wrong_password(self):
        User.objects.create_user("ivan", password="secret123")
        r = self.api.post("/api/auth/login/", {"username": "ivan", "password": "bad"}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_api_requires_token(self):
        self.assertEqual(self.api.get("/api/books/").status_code, 401)
