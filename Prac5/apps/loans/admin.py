from django.contrib import admin
from .models import Loan


@admin.action(description="Выдать книгу читателю")
def make_issued(modeladmin, request, queryset):
    for loan in queryset.filter(status=Loan.Status.NEW):
        loan.issue()


@admin.action(description="Принять книгу обратно")
def make_returned(modeladmin, request, queryset):
    for loan in queryset.filter(status=Loan.Status.ISSUED):
        loan.return_book()


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("id", "reader", "book", "loan_type", "status", "due_date", "fine", "created_at")
    list_filter = ("status", "loan_type", "created_at")
    search_fields = ("reader__full_name", "reader__ticket_number", "book__title")
    readonly_fields = ("created_at", "issued_at", "returned_at")
    actions = [make_issued, make_returned]
