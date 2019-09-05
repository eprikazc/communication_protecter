from django.contrib import admin
from slack_connector.models import DLPDetection


@admin.register(DLPDetection)
class DLPDetectionAdmin(admin.ModelAdmin):
    list_display = ('text', 'dlp_rule', 'created_at')
    ordering = ['-created_at']
