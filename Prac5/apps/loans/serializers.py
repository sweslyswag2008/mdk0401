from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    reader_name = serializers.CharField(source="reader.full_name", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)
    librarian_name = serializers.CharField(source="librarian.get_full_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    loan_type_display = serializers.CharField(source="get_loan_type_display", read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id", "reader", "reader_name", "book", "book_title",
            "librarian", "librarian_name", "loan_type", "loan_type_display",
            "status", "status_display", "due_date", "is_overdue", "fine",
            "comment", "created_at", "issued_at", "returned_at",
        ]
        read_only_fields = [
            "librarian", "status", "due_date", "fine",
            "created_at", "issued_at", "returned_at",
        ]

    def validate_book(self, book):
        from apps.catalog.models import Book
        if not self.instance and book.status != Book.Status.AVAILABLE:
            raise serializers.ValidationError("Эта книга сейчас недоступна для выдачи")
        return book
