from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "country"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    genre_display = serializers.CharField(source="get_genre_display", read_only=True)

    class Meta:
        model = Book
        fields = [
            "id", "author", "author_name", "title", "year", "publisher",
            "genre", "genre_display", "pages", "isbn", "inventory_number",
            "shelf", "status", "status_display", "description", "created_at",
        ]
        read_only_fields = ["created_at"]
