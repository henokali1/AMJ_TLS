from django.contrib import admin
from .models import Client, ReportTemplate

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'passport_no', 'age', 'date')
    search_fields = ('client_name', 'passport_no')
    readonly_fields = ('age',)

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'font_size', 'is_active')
