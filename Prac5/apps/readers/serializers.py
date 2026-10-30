from rest_framework import serializers
from .models import Reader


class ReaderSerializer(serializers.ModelSerializer):
    librarian_name = serializers.CharField(
        source="librarian.get_full_name", read_only=True,
    )

    class Meta:
        model = Reader
        fields = [
            "id", "full_name", "ticket_number", "phone", "email", "group",
            "birth_date", "librarian", "librarian_name", "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate_phone(self, value):
        qs = Reader.objects.filter(phone=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Читатель с таким телефоном уже есть")
        return value
