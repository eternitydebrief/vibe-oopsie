import click
from pathlib import Path

from .scanners.full import full_scan
from .scanners.dangling import dangling_scan
from .output.console import print_results


@click.group()
@click.version_option()
def main():
    """git archaeology - find secrets people thought were gone"""
    pass


@main.command()
@click.argument("repo", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="output as json")
def scan(repo: Path, as_json: bool):
    """full scan - history, dangling commits, stashes"""
    results = full_scan(repo)
    print_results(results, as_json=as_json)


@main.command()
@click.argument("repo", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="output as json")
def dangling(repo: Path, as_json: bool):
    """find orphaned commits from force pushes and deleted branches"""
    results = dangling_scan(repo)
    print_results(results, as_json=as_json)


if __name__ == "__main__":
    main()
