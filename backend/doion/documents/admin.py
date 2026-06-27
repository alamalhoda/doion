from django.contrib import admin
from doion.documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("owner", "document_type", "file_size", "created_at")
    list_filter = ("document_type", "created_at")
    search_fields = ("owner__username",)
    readonly_fields = ("created_at", "updated_at")
