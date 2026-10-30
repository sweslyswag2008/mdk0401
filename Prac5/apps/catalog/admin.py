from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "created_at")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year", "inventory_number", "shelf", "status")
    list_filter = ("author", "status", "genre", "year")
    search_fields = ("title", "inventory_number", "isbn")
    list_editable = ("status",)
