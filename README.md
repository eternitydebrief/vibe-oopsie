# vibe-oopsie

LLMs push secrets to Git. I won't point fingers at who is to blame, but this tool detects secrets in Git.

finds secrets in commits people thought were deleted - dangling commits, force-pushed history, the works.

## install

```
pip install -e .
```

## usage

```
vibe-oopsie scan /path/to/repo
vibe-oopsie dangling /path/to/repo
vibe-oopsie scan /path/to/repo --json
```

## tbd

- more patterns (slack, stripe, gitlab, ssh keys, etc)
- entropy detection
- stash scanning
- reflog scanning
- sarif output
- progress bar
- allowlist/ignore file