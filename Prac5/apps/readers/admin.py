from django.contrib import admin
from .models import Reader


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ("full_name", "ticket_number", "phone", "group", "librarian", "created_at")
    search_fields = ("full_name", "ticket_number", "phone")
    list_filter = ("librarian", "group", "created_at")
