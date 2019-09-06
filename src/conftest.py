import pytest

from dlp.models import FilterRule


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture
def company_email_rule(db):
    return FilterRule.objects.create(
        name='Company email address', pattern='@company.com')
