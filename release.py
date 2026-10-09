#!/usr/bin/env python3
"""Release Foreman in one command (T-0678): python3 release.py VERSION [--canary] [--push URL] [--no-check]

1. --canary: re-run `fm sentinel` in every local project `fm projects` knows, and print what fails there now.
2. Refuse a dirty tree, or a version that isn't newer than plugin.json's.
3. Bump plugin.json and Foreman's two marketplace.json entries; head the Unreleased changelog entries VERSION.
4. Run the gates (`fm check`) unless --no-check; commit "Foreman VERSION".
5. --push URL: merge the branch into that remote's main from a scratch clone (--no-ff), and push.
Updating a machine's install afterwards: git pull there, `claude plugin marketplace update foreman`,
`claude plugin update foreman@foreman`.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FM = [sys.executable, os.path.join(HERE, "plugin", "bin", "fm")]


def git(root, *args, check=True):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"release: git {' '.join(args)} failed: {r.stderr.strip()[:300]}")
    return r.stdout


def version_of(root):
    with open(os.path.join(root, "plugin", ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
        return json.load(f)["version"]


def newer(a, b):
    return tuple(int(x) for x in a.split(".")) > tuple(int(x) for x in b.split("."))


def bump(root, old, new):
    """Every "version": "OLD" in plugin.json and in marketplace.json's Foreman entries (not other plugins')."""
    path = os.path.join(root, "plugin", ".claude-plugin", "plugin.json")
    text = open(path, encoding="utf-8").read()
    open(path, "w", encoding="utf-8").write(text.replace(f'"version": "{old}"', f'"version": "{new}"', 1))
    path = os.path.join(root, ".claude-plugin", "marketplace.json")
    data = json.load(open(path, encoding="utf-8"))
    if data.get("metadata", {}).get("version") == old:
        data["metadata"]["version"] = new
    for p in data.get("plugins", []):
        if p.get("name") == "foreman" and p.get("version") == old:
            p["version"] = new
    open(path, "w", encoding="utf-8").write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    path = os.path.join(root, "CHANGELOG.md")
    text = open(path, encoding="utf-8").read()
    if "## Unreleased\n" not in text:
        sys.exit("release: CHANGELOG.md has no '## Unreleased' heading")
    head = f"## Unreleased\n\n## {new} — {datetime.date.today().isoformat()}\n"
    open(path, "w", encoding="utf-8").write(text.replace("## Unreleased\n", head, 1).replace(head + "\n", head, 1))


def canary():
    """`fm sentinel` in every local project fm knows: what an earlier task proved that fails there now."""
    try:
        listed = json.loads(subprocess.run([*FM, "projects", "--json"], capture_output=True, text=True,
                                           timeout=120).stdout or "{}").get("projects", [])
    except (ValueError, subprocess.TimeoutExpired):
        listed = []
    print(f"canary: fm sentinel in {len(listed)} project(s)")
    for x in listed:
        if not x.get("exists"):
            continue
        r = subprocess.run([*FM, "sentinel"], cwd=x["root"], capture_output=True, text=True, timeout=1800)
        first = (r.stdout.strip().splitlines() or ["(no output)"])[0]
        print(f"  {'✗' if r.returncode else '✓'} {x['project']}: {first}")


def push(root, url, branch, version):
    with tempfile.TemporaryDirectory() as tmp:
        clone = os.path.join(tmp, "rel")
        subprocess.run(["git", "clone", "-q", root, clone], check=True)
        git(clone, "remote", "add", "gh", url)
        git(clone, "fetch", "-q", "gh", "main")
        git(clone, "checkout", "-q", "-b", "rel", "gh/main")
        git(clone, "merge", "-q", "--no-ff", f"origin/{branch}", "-m", f"Foreman {version}")
        git(clone, "push", "-q", "gh", "rel:main")
    print(f"release: pushed Foreman {version} to {url} main")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("version")
    ap.add_argument("--root", default=HERE)
    ap.add_argument("--no-check", action="store_true", help="skip fm check (tests only)")
    ap.add_argument("--canary", action="store_true", help="first, fm sentinel in every local project")
    ap.add_argument("--push", metavar="URL", help="then merge into URL's main from a scratch clone and push")
    a = ap.parse_args()
    if not re.fullmatch(r"\d+\.\d+\.\d+", a.version):
        sys.exit("release: VERSION is MAJOR.MINOR.PATCH, e.g. 1.2.20")
    if a.canary:
        canary()
    if git(a.root, "status", "--porcelain").strip():
        sys.exit("release: the tree has uncommitted changes; commit or finish them first")
    old = version_of(a.root)
    if not newer(a.version, old):
        sys.exit(f"release: {a.version} isn't newer than {old}")
    bump(a.root, old, a.version)
    if not a.no_check:
        r = subprocess.run([*FM, "check"], cwd=a.root)
        if r.returncode:
            git(a.root, "checkout", "--", ".")
            sys.exit("release: fm check failed; the version bump was undone")
    git(a.root, "add", "plugin/.claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "CHANGELOG.md")
    git(a.root, "commit", "-qm", f"Foreman {a.version}")
    print(f"release: Foreman {old} → {a.version} committed")
    if a.push:
        push(a.root, a.push, git(a.root, "branch", "--show-current").strip(), a.version)


if __name__ == "__main__":
    main()
