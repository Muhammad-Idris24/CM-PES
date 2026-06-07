from django import forms

from .models import ContractAssignment


class ContractAssignmentForm(forms.ModelForm):
    class Meta:
        model = ContractAssignment
        fields = ("contract", "user", "role_in_contract", "responsibility")
