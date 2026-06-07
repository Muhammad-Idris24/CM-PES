from django.contrib import admin

from .models import Evaluation, EvaluationDetail


class EvaluationDetailInline(admin.TabularInline):
    model = EvaluationDetail
    extra = 0


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("contract", "evaluator", "total_score", "created_at")
    list_filter = ("created_at", "contract")
    search_fields = ("contract__title", "feedback", "evaluator__full_name")
    inlines = [EvaluationDetailInline]
