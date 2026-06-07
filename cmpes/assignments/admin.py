from django.contrib import admin

from .models import ContractAssignment


@admin.register(ContractAssignment)
class ContractAssignmentAdmin(admin.ModelAdmin):
    list_display = ("contract", "user", "role_in_contract", "responsibility", "assigned_at")
    list_filter = ("role_in_contract",)
    search_fields = ("contract__title", "user__full_name", "responsibility")
