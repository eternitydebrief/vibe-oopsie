import json
from rich.console import Console
from rich.table import Table

from ..scanners.full import ScanResult

console = Console()


def print_results(result: ScanResult, as_json: bool = False):
    if as_json:
        print_json(result)
    else:
        print_table(result)


def print_json(result: ScanResult):
    data = {
        "repo": result.repo_path,
        "commits_scanned": result.commits_scanned,
        "findings": [
            {
                "sha": c.sha,
                "message": c.message,
                "author": c.author,
                "date": c.date,
                "is_dangling": c.is_dangling,
                "secrets": [
                    {"type": f.pattern_name, "match": f.matched_text, "line": f.line_number, "context": f.context}
                    for f in c.findings
                ],
            }
            for c in result.commits_with_findings
        ],
    }
    print(json.dumps(data, indent=2))


def print_table(result: ScanResult):
    if not result.commits_with_findings:
        console.print(f"[green]no secrets found in {result.commits_scanned} commits[/green]")
        return

    console.print(f"\n[red]found secrets in {len(result.commits_with_findings)} commits[/red]\n")

    for commit in result.commits_with_findings:
        tag = "[yellow][dangling][/yellow] " if commit.is_dangling else ""
        console.print(f"{tag}[cyan]{commit.sha[:8]}[/cyan] - {commit.message[:50]}")
        console.print(f"  by {commit.author} on {commit.date}")

        table = Table(show_header=True, header_style="bold")
        table.add_column("type")
        table.add_column("match")
        table.add_column("line")

        for f in commit.findings:
            table.add_row(f.pattern_name, f.matched_text[:40], str(f.line_number))

        console.print(table)
        console.print()
