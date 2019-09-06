import pytest

from dlp.models import FilterRule
from slack_connector.models import DLPDetection
from slack_connector.tasks import process_slack_message, handle_dlp_result


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
    detections = DLPDetection.objects.all()
    assert len(detections) == 1
    assert task.result is detections[0].id
