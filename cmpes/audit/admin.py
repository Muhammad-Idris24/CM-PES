from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "action", "entity_type", "entity_id", "summary")
    list_filter = ("action", "entity_type", "created_at")
    search_fields = ("summary", "entity_type", "entity_id", "actor__email", "actor__full_name")
    readonly_fields = ("actor", "action", "entity_type", "entity_id", "summary", "metadata", "ip_address", "created_at")
