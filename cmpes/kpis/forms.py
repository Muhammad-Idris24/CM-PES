from django import forms

from .models import KPI


class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ("contract", "name", "description", "weight")
        help_texts = {"weight": "Use a decimal weight such as 0.25. Contract KPI weights should total 1.00."}
