from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("kpi/", views.KPIApiView.as_view(), name="kpi"),
    path("loans/", views.LoansByDayApiView.as_view(), name="loans"),
    path("top-books/", views.TopBooksApiView.as_view(), name="top_books"),
    path("librarian-load/", views.LibrarianLoadApiView.as_view(), name="librarian_load"),
    path("stock/", views.StockApiView.as_view(), name="stock"),
    path("overdue/", views.OverdueApiView.as_view(), name="overdue"),
]
