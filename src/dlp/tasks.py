import logging
import re

from celery import shared_task

from dlp.models import FilterRule


@shared_task
def analyze(text):
    """Analyzes text according to existing `FilterRule` records.
    Returns ID of the rule that failed first, or None if all rules passed
    """
    for rule in FilterRule.objects.all():
        if re.search(rule.pattern, text):
            logging.warning('Message is bad: "%s"' % text)
            return rule.id
