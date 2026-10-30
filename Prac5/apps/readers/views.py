from rest_framework import viewsets, filters
from .models import Reader
from .serializers import ReaderSerializer


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.select_related("librarian").all()
    serializer_class = ReaderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["full_name", "ticket_number", "phone", "email"]
    ordering_fields = ["created_at", "full_name"]
