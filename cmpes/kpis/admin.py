from django.contrib import admin

from .models import KPI


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ("name", "contract", "weight")
    list_filter = ("contract",)
    search_fields = ("name", "description", "contract__title")
