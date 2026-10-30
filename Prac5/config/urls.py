from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.catalog.urls")),
    path("api/readers/", include("apps.readers.urls")),
    path("api/loans/", include("apps.loans.urls")),
    path("api/reports/", include("apps.reports.urls")),
    path("api/drf-login/", include("rest_framework.urls")),
]

admin.site.site_header = "Библиотека — система учёта книг"
admin.site.site_title = "Библиотека"
admin.site.index_title = "Управление фондом, читателями и выдачами"
