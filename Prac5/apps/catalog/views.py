from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "country"]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author", "status", "genre", "year"]
    search_fields = ["title", "inventory_number", "isbn", "author__name"]
    ordering_fields = ["title", "year", "created_at"]

    @action(detail=True, methods=["patch"], url_path="status")
    def set_status(self, request, pk=None):
        book = self.get_object()
        value = request.data.get("status")
        if value not in Book.Status.values:
            return Response({"status": "Недопустимый статус"}, status=400)
        book.status = value
        book.save()
        return Response(BookSerializer(book).data)
