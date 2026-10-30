from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.catalog.models import Author, Book
from apps.readers.models import Reader
from .models import Loan, FINE_PER_DAY


class LoanFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("lib", password="x")
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        author = Author.objects.create(name="А. Пушкин")
        self.book = Book.objects.create(author=author, title="Капитанская дочка",
                                        year=1836, inventory_number="К-10")
        self.reader = Reader.objects.create(full_name="Пётр Иванов",
                                            ticket_number="Ч-1", phone="+7900")

    def new_loan(self, **kw):
        r = self.api.post("/api/loans/", {"reader": self.reader.id, "book": self.book.id,
                                          "loan_type": "home", **kw}, format="json")
        return r

    def test_create_reserves_book(self):
        r = self.new_loan()
        self.assertEqual(r.status_code, 201)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.RESERVED)
        self.assertEqual(r.data["librarian"], self.user.id)

    def test_cannot_loan_unavailable_book(self):
        self.new_loan()
        self.assertEqual(self.new_loan().status_code, 400)

    def test_issue_sets_due_date_and_status(self):
        loan_id = self.new_loan().data["id"]
        r = self.api.post(f"/api/loans/{loan_id}/issue/")
        self.assertEqual(r.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.ISSUED)
        self.assertEqual(r.data["due_date"], str(timezone.localdate() + timedelta(days=14)))

    def test_return_without_overdue_has_no_fine(self):
        loan_id = self.new_loan().data["id"]
        self.api.post(f"/api/loans/{loan_id}/issue/")
        r = self.api.post(f"/api/loans/{loan_id}/return/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(r.data["fine"]), 0)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.AVAILABLE)

    def test_return_overdue_counts_fine(self):
        loan_id = self.new_loan().data["id"]
        self.api.post(f"/api/loans/{loan_id}/issue/")
        Loan.objects.filter(pk=loan_id).update(due_date=timezone.localdate() - timedelta(days=4))
        r = self.api.post(f"/api/loans/{loan_id}/return/")
        self.assertEqual(float(r.data["fine"]), 4 * FINE_PER_DAY)

    def test_cancel_returns_book_to_fund(self):
        loan_id = self.new_loan().data["id"]
        self.api.post(f"/api/loans/{loan_id}/cancel/")
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.AVAILABLE)

    def test_wrong_state_transition(self):
        loan_id = self.new_loan().data["id"]
        self.assertEqual(self.api.post(f"/api/loans/{loan_id}/return/").status_code, 400)
