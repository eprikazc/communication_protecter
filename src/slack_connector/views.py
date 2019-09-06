import hashlib
import hmac
import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from slack_connector.tasks import get_process_slack_message_chain


@csrf_exempt
def slack_event_handler(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'POST method is expected'})
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'status': 'Not a valid JSON'})
    if not _verify_request_signature(request):
        return JsonResponse({'status': 'Cannot verify signature'})
    if 'challenge' in payload:
        return JsonResponse({'challenge': payload['challenge']})
    try:
        event_type = payload['event']['type']
    except (TypeError, KeyError):
        return JsonResponse({'status': 'Cannot get event type'})
    if event_type == 'message':
        get_process_slack_message_chain(payload)()
    return JsonResponse({})


def _verify_request_signature(request):
    """
    Verify request signature as described in
    https://api.slack.com/docs/verifying-requests-from-slack
    """
    signature = request.headers['X-Slack-Signature']
    timestamp = request.headers['X-Slack-Request-Timestamp']
    body = request.body.decode('utf-8')
    base_string = 'v0:%s:%s' % (timestamp, body)
    secret = settings.SLACK_SIGNING_SECRET
    calculated = hmac.new(
        secret.encode(),
        base_string.encode(),
        hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, 'v0=' + calculated)
