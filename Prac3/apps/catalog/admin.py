from django.contrib import admin

from .models import Category, Edition, Location, Publisher


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "publisher", "category")
    list_filter = ("publisher", "category")
    search_fields = ("name",)
    autocomplete_fields = ("publisher", "category")
