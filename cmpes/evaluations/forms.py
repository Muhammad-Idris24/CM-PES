from django import forms

from .models import Evaluation, EvaluationDetail


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ("contract", "feedback")


class EvaluationDetailForm(forms.ModelForm):
    class Meta:
        model = EvaluationDetail
        fields = ("kpi", "score")
