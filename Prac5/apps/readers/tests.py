from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from .models import Reader


class ReaderTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.api.force_authenticate(User.objects.create_user("lib", password="x"))

    def payload(self, **kw):
        d = {"full_name": "Мария Смирнова", "ticket_number": "Ч-001", "phone": "+79990000001"}
        d.update(kw)
        return d

    def test_create_reader(self):
        r = self.api.post("/api/readers/", self.payload(), format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Reader.objects.count(), 1)

    def test_phone_must_be_unique(self):
        self.api.post("/api/readers/", self.payload(), format="json")
        r = self.api.post("/api/readers/", self.payload(ticket_number="Ч-002"), format="json")
        self.assertEqual(r.status_code, 400)

    def test_edit_keeps_own_phone(self):
        rid = self.api.post("/api/readers/", self.payload(), format="json").data["id"]
        r = self.api.patch(f"/api/readers/{rid}/", {"group": "ИСП-271"}, format="json")
        self.assertEqual(r.status_code, 200)

    def test_search_by_ticket(self):
        self.api.post("/api/readers/", self.payload(), format="json")
        self.assertEqual(self.api.get("/api/readers/?search=Ч-001").data["count"], 1)
