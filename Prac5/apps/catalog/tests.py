from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from .models import Author, Book


class CatalogTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.api.force_authenticate(User.objects.create_user("lib", password="x"))
        self.author = Author.objects.create(name="Лев Толстой", country="Россия")

    def make_book(self, inv, **kw):
        data = dict(author=self.author, title="Война и мир", year=1869, inventory_number=inv)
        data.update(kw)
        return Book.objects.create(**data)

    def test_default_status_available(self):
        self.assertTrue(self.make_book("К-1").is_available)

    def test_create_and_list_via_api(self):
        r = self.api.post("/api/books/", {
            "author": self.author.id, "title": "Анна Каренина",
            "year": 1877, "inventory_number": "К-2", "genre": "fiction",
        }, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.api.get("/api/books/").data["count"], 1)

    def test_inventory_number_unique(self):
        self.make_book("К-1")
        r = self.api.post("/api/books/", {
            "author": self.author.id, "title": "Другая", "year": 2000, "inventory_number": "К-1",
        }, format="json")
        self.assertEqual(r.status_code, 400)

    def test_filter_and_search(self):
        self.make_book("К-1")
        self.make_book("К-2", title="Воскресение", status="issued")
        self.assertEqual(self.api.get("/api/books/?status=issued").data["count"], 1)
        self.assertEqual(self.api.get("/api/books/?search=Воскр").data["count"], 1)

    def test_set_status(self):
        b = self.make_book("К-1")
        r = self.api.patch(f"/api/books/{b.id}/status/", {"status": "written_off"}, format="json")
        self.assertEqual(r.status_code, 200)
        b.refresh_from_db()
        self.assertEqual(b.status, Book.Status.WRITTEN_OFF)
        bad = self.api.patch(f"/api/books/{b.id}/status/", {"status": "xxx"}, format="json")
        self.assertEqual(bad.status_code, 400)
