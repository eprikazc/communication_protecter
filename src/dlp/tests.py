import pytest

from dlp.models import FilterRule
from dlp.tasks import analyze


@pytest.fixture
def company_email_rule(db):
    return FilterRule.objects.create(
        name='Company email address', pattern='@company.com')


def test_analyze_ok(company_email_rule):
    res = analyze('This message is ok')
    assert res is None


def test_analyze_complains(company_email_rule):
    res = analyze(
        'This message is not ok\n'
        'It contains this address: secret@company.com\n'
        'Therefore DLP should report it')
    assert res == company_email_rule.id
