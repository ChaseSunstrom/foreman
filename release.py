#!/usr/bin/env python3
"""Release Foreman in one command (T-0678): python3 release.py VERSION [--canary] [--push URL] [--no-check] [--root DIR]

A thin wrapper over `fm release` (T-1188), which owns the steps (clean tree, gates, version bumps, changelog, commit,
release-check, canary, push, round close), their checkpoints and --resume. Flags that map: --no-check, --push URL
(= fm release --push --remote URL, behind the active task's publish grant), --root (the directory fm runs in).
--canary is accepted for old habits: the canary is always a step now. Run `fm release --help` for the rest.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FM = [sys.executable, os.path.join(HERE, "plugin", "bin", "fm")]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("version")
    ap.add_argument("--root", default=HERE)
    ap.add_argument("--no-check", action="store_true", help="skip the gates (a release with skipped gates can't push)")
    ap.add_argument("--canary", action="store_true", help="accepted; the canary is always a step")
    ap.add_argument("--push", metavar="URL", help="merge into URL's main from a temporary worktree and push")
    a = ap.parse_args()
    argv = [*FM, "release", a.version] + (["--no-check"] if a.no_check else []) + (
        ["--push", "--remote", a.push] if a.push else [])
    sys.exit(subprocess.run(argv, cwd=a.root).returncode)


if __name__ == "__main__":
    main()
