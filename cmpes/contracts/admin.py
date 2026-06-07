from django.contrib import admin

from .models import Contract, ContractDocument


class ContractDocumentInline(admin.TabularInline):
    model = ContractDocument
    extra = 0
    readonly_fields = ("uploaded_at",)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "start_date", "end_date", "created_by")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("title", "description")
    inlines = [ContractDocumentInline]


@admin.register(ContractDocument)
class ContractDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "contract", "document_type", "version", "uploaded_by", "uploaded_at")
    list_filter = ("document_type", "uploaded_at")
    search_fields = ("title", "contract__title", "notes")
