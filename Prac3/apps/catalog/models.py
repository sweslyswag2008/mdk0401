from django.db import models


class Location(models.Model):
    name = models.CharField("Место хранения", max_length=255)

    class Meta:
        verbose_name = "Место хранения"
        verbose_name_plural = "Места хранения"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("Раздел", max_length=255)

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField("Издательство", max_length=255, unique=True)

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

    def __str__(self):
        return self.name


class Edition(models.Model):
    publisher = models.ForeignKey(
        Publisher, on_delete=models.PROTECT,
        verbose_name="Издательство",
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        verbose_name="Раздел",
    )
    name = models.CharField("Издание", max_length=255)

    class Meta:
        verbose_name = "Издание"
        verbose_name_plural = "Издания"

    def __str__(self):
        return f"{self.publisher.name} — {self.name}"
