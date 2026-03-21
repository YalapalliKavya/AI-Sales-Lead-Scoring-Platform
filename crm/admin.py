from django.contrib import admin
from .models import Lead, InteractionLog, ContactMessage

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "status", "crm_status", "assigned_to", "created_at")
    search_fields = ("name", "email", "company", "source")
    list_filter = ("status", "crm_status", "source", "assigned_to")

@admin.register(InteractionLog)
class InteractionLogAdmin(admin.ModelAdmin):
    list_display = ("lead", "created_at")
    search_fields = ("lead__name", "note")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")