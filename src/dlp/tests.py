from dlp.tasks import analyze


def test_analyze_ok(company_email_rule):
    task = analyze.s('This message is ok').apply()
    assert task.result is None


def test_analyze_complains(company_email_rule):
    task = analyze.s(
        'This message is not ok\n'
        'It contains this address: secret@company.com\n'
        'Therefore DLP should report it').apply()
    assert task.result == company_email_rule.id
