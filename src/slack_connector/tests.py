import pytest

from slack_connector.models import DLPDetection
from slack_connector.tasks import (
    get_process_slack_message_chain, handle_dlp_result)


@pytest.fixture
def good_message():
    return {
        'event': {
            'channel': 'ABC',
            'ts': '1567763452.001200',
            'text': 'Good message',
        }
    }


@pytest.fixture
def bad_message():
    return {
        'event': {
            'channel': 'ABC',
            'ts': '1567763452.001200',
            'text': 'This is bad message - user@company.com',
        }
    }


def test_handle_dlp_result_ok(company_email_rule, good_message):
    text = good_message['event']['text']
    task = handle_dlp_result.s(None, text, good_message).apply()
    assert task.result is None


def test_handle_dlp_result_detection(company_email_rule, bad_message, mocker):
    mocker.patch('slack_connector.tasks.block_message')
    text = bad_message['event']['text']
    task = handle_dlp_result.s(
        company_email_rule.id, text, bad_message).apply()
    assert_result_is_dlp_detection(task.result)


def test_process_slack_message_chain_ok(company_email_rule, good_message):
    chain = get_process_slack_message_chain(good_message)
    res = chain.apply().get()
    assert res is None


def test_process_slack_message_chain_detection(company_email_rule, bad_message, mocker):
    mocker.patch('slack_connector.tasks.block_message')
    chain = get_process_slack_message_chain(bad_message)
    res = chain.apply().get()
    assert_result_is_dlp_detection(res)


def assert_result_is_dlp_detection(result):
    detections = DLPDetection.objects.all()
    assert len(detections) == 1
    assert result is detections[0].id
