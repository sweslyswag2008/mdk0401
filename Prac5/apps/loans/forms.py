from django import forms
from .models import Loan


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["reader", "book", "loan_type", "comment"]
        widgets = {
            "reader": forms.Select(attrs={"class": "form-select"}),
            "book": forms.Select(attrs={"class": "form-select"}),
            "loan_type": forms.Select(attrs={"class": "form-select"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from apps.catalog.models import Book
        self.fields["book"].queryset = Book.objects.filter(status=Book.Status.AVAILABLE)
