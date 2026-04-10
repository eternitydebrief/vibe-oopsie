import subprocess
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Commit:
    sha: str
    message: str
    author: str
    date: str
    is_dangling: bool = False


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
    )
    return result.stdout.decode("utf-8", errors="replace").strip()


def get_all_commits(repo: Path) -> list[Commit]:
    output = run_git(repo, "log", "--all", "--format=%H|%s|%an|%ai")
    commits = []
    for line in output.splitlines():
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) >= 4:
            commits.append(Commit(sha=parts[0], message=parts[1], author=parts[2], date=parts[3]))
    return commits


def get_dangling_commits(repo: Path) -> list[Commit]:
    output = run_git(repo, "fsck", "--unreachable", "--no-reflogs")
    dangling = []
    for line in output.splitlines():
        if "unreachable commit" in line:
            sha = line.split()[-1]
            info = run_git(repo, "log", "-1", "--format=%s|%an|%ai", sha)
            parts = info.split("|", 2)
            if len(parts) >= 3:
                dangling.append(
                    Commit(sha=sha, message=parts[0], author=parts[1], date=parts[2], is_dangling=True)
                )
    return dangling


def get_commit_diff(repo: Path, sha: str) -> str:
    return run_git(repo, "show", "--format=", sha)
