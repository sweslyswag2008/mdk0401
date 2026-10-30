from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Администратор"
        LIBRARIAN = "librarian", "Библиотекарь"
        HEAD = "head", "Заведующий"

    full_name = models.CharField("ФИО", max_length=255, blank=True)
    role = models.CharField(
        "Роль", max_length=32,
        choices=Role.choices,
        default=Role.LIBRARIAN,
    )

    def __str__(self):
        return self.full_name or self.username
