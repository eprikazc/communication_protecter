def get_message_text(event_source):
    if event_source['event'].get('subtype') == 'message_changed':
        text = event_source['event']['message']['text']
    else:
        text = event_source['event']['text']
    return text


def get_message_ts(event_source):
    if event_source['event'].get('subtype') == 'message_changed':
        res = event_source['event']['message']['ts']
    else:
        res = event_source['event']['ts']
    return res
