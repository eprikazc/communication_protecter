from celery import shared_task, chain

from slack_connector.models import DLPDetection
from dlp.tasks import analyze


def process_slack_message(event_source):
    text = event_source['event']['text']
    return chain(
        analyze.s(text),
        handle_dlp_result.s(text, event_source),
    )()


@shared_task
def handle_dlp_result(rule_id, text, event_source):
    """Analyzes text according to existing `FilterRule` records.
    Returns ID of the rule that failed first, or None if all rules passed
    """
    if rule_id:
        detection = DLPDetection.objects.create(
            dlp_rule_id=rule_id,
            text=text,
            event_source=event_source,
        )
        return detection.id
