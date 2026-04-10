from pathlib import Path

from ..git.objects import get_dangling_commits, get_commit_diff
from ..detectors.patterns import scan_text
from .full import ScanResult, CommitResult


def dangling_scan(repo: Path) -> ScanResult:
    result = ScanResult(repo_path=str(repo), commits_scanned=0)

    for commit in get_dangling_commits(repo):
        result.commits_scanned += 1
        diff = get_commit_diff(repo, commit.sha)
        findings = scan_text(diff)

        if findings:
            result.commits_with_findings.append(CommitResult(
                sha=commit.sha,
                message=commit.message,
                author=commit.author,
                date=commit.date,
                is_dangling=True,
                findings=findings,
            ))

    return result
