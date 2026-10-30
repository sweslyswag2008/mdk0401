from django import forms
from .models import Reader


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ["full_name", "ticket_number", "phone", "email", "group", "birth_date", "librarian"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "ticket_number": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "group": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "librarian": forms.Select(attrs={"class": "form-select"}),
        }
