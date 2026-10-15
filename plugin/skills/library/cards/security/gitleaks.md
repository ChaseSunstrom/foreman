---
name: gitleaks
title: Gitleaks
area: security
tags: [security, secrets, scanning, git, pre-commit, ci]
detect: [file:.gitleaks.toml]
related: [secrets-management, api-keys, key-rotation, supply-chain-pinning]
---
Secret scanning with gitleaks: pre-commit on staged changes, CI over history, tuned allowlist, and rotation when something leaks.

## Verify
- `gitleaks detect --source . --no-banner --redact`: scan the repo history with values masked in the output.
- `gitleaks protect --staged --no-banner --redact`: scan only staged changes before commit.
- `gitleaks detect --source . --no-git --no-banner`: scan the working tree, including untracked files.
- `git config core.hooksPath`: the hook directory in use, to confirm the pre-commit hook is wired.

## Test first
Prove the scanner catches a planted fake key, and the allowlist stays narrow.
```python
import subprocess, pathlib

def test_gitleaks_flags_a_planted_secret(tmp_path):
    f = tmp_path / "cfg.py"
    f.write_text('AWS_KEY = "AKIAIOSFODNN7EXAMPLE"\n')  # pragma: allowlist secret
    r = subprocess.run(["gitleaks", "detect", "--no-git", "--source", str(tmp_path),
                        "--no-banner"], capture_output=True)
    assert r.returncode != 0

def test_allowlist_has_no_broad_paths():
    cfg = pathlib.Path(".gitleaks.toml").read_text()
    assert 'paths = [".*"]' not in cfg and "'''.*'''" not in cfg
```

## Do
- Run `gitleaks protect --staged` as a pre-commit hook and `gitleaks detect` in CI on every push and pull request, with full history.
- Extend the default rules with `[extend] useDefault = true` in `.gitleaks.toml` and add rules for your own key prefixes.
- Allowlist narrowly: a specific fingerprint, one test fixture path, or a rule id plus regex. Add a comment on why.
- Use obviously fake values in tests and docs (`AKIAIOSFODNN7EXAMPLE`) and allowlist those exact strings. <!-- pragma: allowlist secret -->
- Commit a baseline report for a legacy repo and pass it with `--baseline-path` so only new leaks fail.
- On a real hit: revoke and rotate first, then remove from history if needed. Deletion alone does not help.
- Keep real secrets in a secret manager and out of `.env` files in git.

## Avoid
- Allowlisting a whole directory or `.*` to silence noise: fix the rule or allowlist the specific fingerprint.
- `git commit --no-verify` habits: CI is the backstop, so keep the CI scan mandatory.
- Scanning only the latest commit: old commits keep the secret reachable. Scan history.
- Treating removal from the file as remediation: the key is still in history and forks, so rotate it.
- Printing matches unredacted in CI logs: use `--redact`.
- Disabling the scan on a failing test fixture: replace it with a clearly fake value.

## Review
- [ ] Pre-commit and CI both run the scan, with history in CI.
- [ ] `.gitleaks.toml` extends defaults and has only narrow allowlists.
- [ ] Custom rules cover internal token prefixes.
- [ ] A rotation procedure is written for hits.
- [ ] CI logs use redaction.
