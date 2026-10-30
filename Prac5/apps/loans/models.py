from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.catalog.models import Book
from apps.readers.models import Reader

LOAN_DAYS = 14
FINE_PER_DAY = 5


class Loan(models.Model):
    class LoanType(models.TextChoices):
        HOME = "home", "На дом"
        HALL = "hall", "В читальный зал"
        RESERVE = "reserve", "Бронь"

    class Status(models.TextChoices):
        NEW = "new", "Оформлена"
        ISSUED = "issued", "Книга выдана"
        RETURNED = "returned", "Возвращена"
        CANCELLED = "cancelled", "Отменена"

    reader = models.ForeignKey(
        Reader, on_delete=models.CASCADE,
        related_name="loans", verbose_name="Читатель",
    )
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT,
        related_name="loans", verbose_name="Книга",
    )
    librarian = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="loans", verbose_name="Библиотекарь",
    )
    loan_type = models.CharField("Вид выдачи", max_length=20, choices=LoanType.choices)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW)
    due_date = models.DateField("Вернуть до", null=True, blank=True)
    fine = models.DecimalField("Штраф, руб.", max_digits=8, decimal_places=2, default=0)
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Оформлена", auto_now_add=True)
    issued_at = models.DateTimeField("Выдана", null=True, blank=True)
    returned_at = models.DateTimeField("Возвращена", null=True, blank=True)

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Выдача №{self.pk} — {self.reader.full_name}"

    @property
    def is_overdue(self):
        return (
            self.status == self.Status.ISSUED
            and self.due_date is not None
            and self.due_date < timezone.localdate()
        )

    def clean(self):
        if not self.pk and self.book_id and self.book.status != Book.Status.AVAILABLE:
            raise ValidationError("Эта книга сейчас недоступна для выдачи")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
            self.book.status = Book.Status.RESERVED
            self.book.save()
        super().save(*args, **kwargs)

    def issue(self):
        self.status = self.Status.ISSUED
        self.issued_at = timezone.now()
        if self.loan_type == self.LoanType.HOME:
            self.due_date = timezone.localdate() + timedelta(days=LOAN_DAYS)
        else:
            self.due_date = timezone.localdate()
        self.book.status = Book.Status.ISSUED
        self.book.save()
        self.save()

    def return_book(self):
        today = timezone.localdate()
        if self.due_date and today > self.due_date:
            self.fine = (today - self.due_date).days * FINE_PER_DAY
        self.status = self.Status.RETURNED
        self.returned_at = timezone.now()
        self.book.status = Book.Status.AVAILABLE
        self.book.save()
        self.save()

    def cancel(self):
        self.status = self.Status.CANCELLED
        if self.book.status == Book.Status.RESERVED:
            self.book.status = Book.Status.AVAILABLE
            self.book.save()
        self.save()
