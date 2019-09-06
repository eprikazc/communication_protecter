from celery import shared_task, chain
from django.conf import settings
import requests

from slack_connector.models import DLPDetection
from slack_connector.message_parser import get_message_text, get_message_ts
from dlp.tasks import analyze


def get_process_slack_message_chain(event_source):
    text = get_message_text(event_source)
    return chain(
        analyze.s(text),
        handle_dlp_result.s(text, event_source),
    )


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
        block_message(event_source['event']['channel'], get_message_ts(event_source))
        return detection.id


def block_message(channel, message_timestamp):
    response = requests.post(
        'https://slack.com/api/chat.update',
        headers={
            'Authorization': 'Bearer %s' % settings.SLACK_OAUTH_ACCESS_TOKEN,
        },
        json={
            'channel': channel,
            'text': 'This message has been blocked',
            'ts': message_timestamp,
        }
    )
    assert response.status_code == 200
