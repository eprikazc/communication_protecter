import pytest

from dlp.models import FilterRule
from slack_connector.models import DLPDetection
from slack_connector.tasks import get_process_slack_message_chain, handle_dlp_result


@pytest.fixture
def company_email_rule(db):
    return FilterRule.objects.create(
        name='Company email address', pattern='@company.com')


def test_handle_dlp_result_ok(company_email_rule):
    task = handle_dlp_result.s(None, 'this message is ok', '{...}').apply()
    assert task.result is None


def test_handle_dlp_resul_detection(company_email_rule):
    task = handle_dlp_result.s(
        company_email_rule.id, 'this message is ok', '{...}').apply()
    assert_result_is_dlp_detection(task.result)


def test_process_slack_message_chain_ok(company_email_rule):
    chain = get_process_slack_message_chain({
        'event': {
            'text': 'This is good message',
        },
    })
    res = chain.apply().get()
    assert res is None


def test_process_slack_message_chain_detection(company_email_rule):
    chain = get_process_slack_message_chain({
        'event': {
            'text': 'This is bad message - user@company.com',
        },
    })
    res = chain.apply().get()
    assert_result_is_dlp_detection(res)


def assert_result_is_dlp_detection(result):
    detections = DLPDetection.objects.all()
    assert len(detections) == 1
    assert result is detections[0].id
