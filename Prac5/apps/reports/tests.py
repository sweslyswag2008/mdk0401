from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.catalog.models import Author, Book
from apps.loans.models import Loan
from apps.readers.models import Reader


class ReportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("lib", password="x")
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        author = Author.objects.create(name="Н. Гоголь")
        self.reader = Reader.objects.create(full_name="Ольга", ticket_number="Ч-1", phone="+7")
        self.books = [Book.objects.create(author=author, title=f"Книга {i}", year=1900,
                                          inventory_number=f"К-{i}") for i in range(3)]

    def loan(self, book):
        return Loan.objects.create(reader=self.reader, book=book, librarian=self.user, loan_type="home")

    def test_kpi_counts(self):
        l1 = self.loan(self.books[0]); l1.issue(); l1.return_book()
        l2 = self.loan(self.books[1]); l2.issue()
        Loan.objects.filter(pk=l2.pk).update(due_date=timezone.localdate() - timedelta(days=2))
        kpi = self.api.get("/api/reports/kpi/").data
        self.assertEqual(kpi["loans_count"], 2)
        self.assertEqual(kpi["returned_count"], 1)
        self.assertEqual(kpi["on_hands"], 1)
        self.assertEqual(kpi["overdue"], 1)
        self.assertEqual(kpi["books_available"], 2)

    def test_kpi_updates_after_return(self):
        loan = self.loan(self.books[0]); loan.issue()
        self.assertEqual(self.api.get("/api/reports/kpi/").data["on_hands"], 1)
        loan.return_book()
        self.assertEqual(self.api.get("/api/reports/kpi/").data["on_hands"], 0)

    def test_top_books_and_stock(self):
        for _ in range(2):
            l = self.loan(self.books[0]); l.issue(); l.return_book()
        self.loan(self.books[1])
        top = self.api.get("/api/reports/top-books/").data
        self.assertEqual(top[0]["title"], "Книга 0")
        self.assertEqual(top[0]["count"], 2)
        stock = {r["status"]: r["count"] for r in self.api.get("/api/reports/stock/").data}
        self.assertEqual(stock["reserved"], 1)

    def test_overdue_list(self):
        loan = self.loan(self.books[0]); loan.issue()
        Loan.objects.filter(pk=loan.pk).update(due_date=timezone.localdate() - timedelta(days=3))
        rows = self.api.get("/api/reports/overdue/").data
        self.assertEqual(rows[0]["days_overdue"], 3)

    def test_reports_need_auth(self):
        self.assertEqual(APIClient().get("/api/reports/kpi/").status_code, 401)
