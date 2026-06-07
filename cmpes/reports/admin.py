from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("contract", "report_type", "generated_by", "created_at")
    list_filter = ("report_type", "created_at")
    search_fields = ("contract__title", "content")
