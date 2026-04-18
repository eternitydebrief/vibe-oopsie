import re
from dataclasses import dataclass


PATTERNS = {
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "github_token": re.compile(r"ghp_[A-Za-z0-9]{36}"),
    "generic_secret": re.compile(r"(?i)(password|secret|api_key|apikey)\s*[=:]\s*['\"][^'\"]{8,}['\"]"),
}


@dataclass
class Finding:
    pattern_name: str
    matched_text: str
    line_number: int
    context: str


def scan_text(text: str) -> list[Finding]:
    findings = []
    lines = text.splitlines()

    for i, line in enumerate(lines, 1):
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(line):
                findings.append(Finding(
                    pattern_name=name,
                    matched_text=match.group(),
                    line_number=i,
                    context=line.strip()[:100],
                ))

    return findings
