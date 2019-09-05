import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from slack_connector.tasks import process_slack_message


@csrf_exempt
def slack_event_handler(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'status': 'Not a valid JSON'})
    try:
        event_type = payload['event']['type']
    except (TypeError, KeyError):
        return JsonResponse({'status': 'Cannot get event type'})
    if event_type == 'message':
        process_slack_message(payload)
    return JsonResponse({})
