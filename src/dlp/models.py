from django.db import models


class FilterRule(models.Model):
    name = models.CharField(max_length=80)
    pattern = models.CharField(
        max_length=80, help_text='Regular expression to check against')
    description = models.TextField(
        blank=True,
        help_text='You can put verbose description of the rule here')

    def __str__(self):
        return self.name
