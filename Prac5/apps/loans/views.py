from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Loan
from .serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.select_related("reader", "book", "librarian").all()
    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "loan_type", "librarian", "reader"]
    search_fields = ["reader__full_name", "reader__ticket_number", "book__title"]
    ordering_fields = ["created_at", "due_date"]

    def perform_create(self, serializer):
        serializer.save(librarian=self.request.user)

    def _do(self, request, pk, method, allowed):
        loan = self.get_object()
        if loan.status not in allowed:
            return Response({"detail": "Действие недоступно в статусе «%s»" % loan.get_status_display()}, status=400)
        getattr(loan, method)()
        return Response(self.get_serializer(loan).data)

    @action(detail=True, methods=["post"])
    def issue(self, request, pk=None):
        return self._do(request, pk, "issue", [Loan.Status.NEW])

    @action(detail=True, methods=["post"], url_path="return")
    def return_(self, request, pk=None):
        return self._do(request, pk, "return_book", [Loan.Status.ISSUED])

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        return self._do(request, pk, "cancel", [Loan.Status.NEW])
