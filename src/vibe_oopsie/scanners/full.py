from pathlib import Path
from dataclasses import dataclass, field

from ..git.objects import get_all_commits, get_commit_diff, get_dangling_commits
from ..detectors.patterns import scan_text, Finding


@dataclass
class CommitResult:
    sha: str
    message: str
    author: str
    date: str
    is_dangling: bool
    findings: list[Finding] = field(default_factory=list)


@dataclass
class ScanResult:
    repo_path: str
    commits_scanned: int
    commits_with_findings: list[CommitResult] = field(default_factory=list)


def full_scan(repo: Path) -> ScanResult:
    result = ScanResult(repo_path=str(repo), commits_scanned=0)

    all_commits = get_all_commits(repo)
    dangling = get_dangling_commits(repo)
    all_commits.extend(dangling)

    for commit in all_commits:
        result.commits_scanned += 1
        diff = get_commit_diff(repo, commit.sha)
        findings = scan_text(diff)

        if findings:
            result.commits_with_findings.append(CommitResult(
                sha=commit.sha,
                message=commit.message,
                author=commit.author,
                date=commit.date,
                is_dangling=commit.is_dangling,
                findings=findings,
            ))

    return result
