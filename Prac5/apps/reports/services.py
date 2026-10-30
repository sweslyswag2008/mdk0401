from datetime import timedelta

from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.catalog.models import Book
from apps.loans.models import Loan
from apps.readers.models import Reader


class ReportService:
    @staticmethod
    def kpi(days: int = 30) -> dict:
        since = timezone.now() - timedelta(days=days)
        period = Loan.objects.filter(created_at__gte=since).exclude(status=Loan.Status.CANCELLED)
        fines = Loan.objects.filter(
            status=Loan.Status.RETURNED, returned_at__gte=since,
        ).aggregate(total=Sum("fine"))["total"] or 0
        return {
            "loans_count": period.count(),
            "returned_count": period.filter(status=Loan.Status.RETURNED).count(),
            "on_hands": Loan.objects.filter(status=Loan.Status.ISSUED).count(),
            "overdue": Loan.objects.filter(
                status=Loan.Status.ISSUED, due_date__lt=timezone.localdate(),
            ).count(),
            "fines_total": float(fines),
            "books_available": Book.objects.filter(status=Book.Status.AVAILABLE).count(),
            "readers_total": Reader.objects.count(),
            "period_days": days,
        }

    @staticmethod
    def loans_by_day(days: int = 30) -> list:
        since = timezone.now() - timedelta(days=days)
        rows = (
            Loan.objects.filter(created_at__gte=since)
            .exclude(status=Loan.Status.CANCELLED)
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(total=Count("id"))
            .order_by("day")
        )
        return [{"date": str(r["day"]), "total": r["total"]} for r in rows]

    @staticmethod
    def top_books(limit: int = 5) -> list:
        rows = (
            Loan.objects.exclude(status=Loan.Status.CANCELLED)
            .values("book__author__name", "book__title")
            .annotate(count=Count("id"))
            .order_by("-count", "book__title")[:limit]
        )
        return [
            {"author": r["book__author__name"], "title": r["book__title"], "count": r["count"]}
            for r in rows
        ]

    @staticmethod
    def librarian_load(days: int = 30) -> list:
        since = timezone.now() - timedelta(days=days)
        rows = (
            Loan.objects.filter(created_at__gte=since)
            .exclude(status=Loan.Status.CANCELLED)
            .values("librarian__username")
            .annotate(count=Count("id"), fines=Sum("fine"))
        )
        return [
            {"librarian": r["librarian__username"], "loans": r["count"], "fines": float(r["fines"] or 0)}
            for r in rows
        ]

    @staticmethod
    def stock_status() -> list:
        return [
            {"status": r["status"], "count": r["count"]}
            for r in Book.objects.values("status").annotate(count=Count("id"))
        ]

    @staticmethod
    def overdue_list() -> list:
        rows = Loan.objects.filter(
            status=Loan.Status.ISSUED, due_date__lt=timezone.localdate(),
        ).select_related("reader", "book").order_by("due_date")
        today = timezone.localdate()
        return [
            {
                "reader": l.reader.full_name,
                "ticket": l.reader.ticket_number,
                "book": l.book.title,
                "due_date": str(l.due_date),
                "days_overdue": (today - l.due_date).days,
            }
            for l in rows
        ]
