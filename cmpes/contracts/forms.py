from django import forms

from .models import Contract, ContractDocument


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ("title", "description", "start_date", "end_date", "status", "document")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ContractDocumentForm(forms.ModelForm):
    class Meta:
        model = ContractDocument
        fields = ("title", "document_type", "version", "file", "notes")
