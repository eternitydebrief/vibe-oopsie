from vibe_oopsie.detectors.patterns import scan_text


def test_finds_aws_key():
    text = "aws_key = AKIAIOSFODNN7EXAMPLE"
    findings = scan_text(text)
    assert len(findings) == 1
    assert findings[0].pattern_name == "aws_access_key"


def test_finds_github_token():
    text = "token: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    findings = scan_text(text)
    assert len(findings) == 1
    assert findings[0].pattern_name == "github_token"


def test_no_false_positives_on_clean():
    text = "just some normal code\nno secrets here\n"
    findings = scan_text(text)
    assert len(findings) == 0
