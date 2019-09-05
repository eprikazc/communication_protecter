from django.db import models


class DLPDetection(models.Model):
    dlp_rule = models.ForeignKey(
        'dlp.FilterRule',
        models.SET_NULL,
        null=True,
        help_text='DLP rule that caught the message')
    text = models.TextField(help_text='Text of the message')
    event_source = models.TextField(help_text='JSON string with slack event')
    created_at = models.DateTimeField(auto_now_add=True)
