from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField("ФИО автора", max_length=100, unique=True)
    country = models.CharField("Страна", max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "В фонде"
        RESERVED = "reserved", "Забронирована"
        ISSUED = "issued", "Выдана"
        WRITTEN_OFF = "written_off", "Списана"

    class Genre(models.TextChoices):
        FICTION = "fiction", "Художественная"
        SCIENCE = "science", "Научная"
        TEXTBOOK = "textbook", "Учебная"
        CHILDREN = "children", "Детская"
        REFERENCE = "reference", "Справочная"

    author = models.ForeignKey(
        Author, on_delete=models.PROTECT,
        related_name="books", verbose_name="Автор",
    )
    title = models.CharField("Название", max_length=200)
    year = models.PositiveIntegerField("Год издания")
    publisher = models.CharField("Издательство", max_length=100, blank=True)
    genre = models.CharField("Раздел", max_length=20, choices=Genre.choices, blank=True)
    pages = models.PositiveIntegerField("Страниц", null=True, blank=True)
    isbn = models.CharField("ISBN", max_length=20, blank=True)
    inventory_number = models.CharField("Инвентарный номер", max_length=20, unique=True)
    shelf = models.CharField("Стеллаж / полка", max_length=20, blank=True)
    status = models.CharField(
        "Статус", max_length=20,
        choices=Status.choices, default=Status.AVAILABLE,
    )
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.author.name} ({self.year})"

    def get_absolute_url(self):
        return reverse("catalog:book_detail", args=[self.pk])

    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE
