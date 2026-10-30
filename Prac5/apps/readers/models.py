from django.db import models
from django.conf import settings


class Reader(models.Model):
    full_name = models.CharField("ФИО", max_length=100)
    ticket_number = models.CharField("Номер читательского билета", max_length=20, unique=True)
    phone = models.CharField("Телефон", max_length=20, unique=True)
    email = models.EmailField("Email", blank=True)
    group = models.CharField("Группа / класс", max_length=20, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    librarian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="readers",
        verbose_name="Записал библиотекарь",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} (билет {self.ticket_number})"
