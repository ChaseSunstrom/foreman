---
name: secrets-management
title: Secrets management
area: security
tags: [security, secrets, credentials, env, vault, rotation]
detect: [file:.env, file:.env.example, file:.gitleaks.toml, file:.pre-commit-config.yaml, dep:python-dotenv, dep:dotenv, dep:hvac]
related: [crypto-usage, pii-logging, dependency-audit, trivy, owasp-top-10]
---
Keep secrets out of the repo and logs, load them from the environment or a secret store, scan for leaks, and rotate on exposure.

## Verify
- `gitleaks detect --source . --no-banner`: the working tree and history have no detected secrets.
- `git check-ignore -q .env && echo ignored`: the real env file is ignored by git.
- `trivy fs --scanners secret .`: the filesystem scan finds no secrets.
- `git ls-files | grep -E "\.env$|\.pem$|id_rsa"`: no key or env file is tracked.

## Test first
The failing check is a leak scan or a config test.
```python
import re, pathlib
def test_no_tracked_secrets():
    pat = re.compile(r"(AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
    for p in pathlib.Path("src").rglob("*"):
        if p.is_file():
            assert not pat.search(p.read_text(errors="ignore")), p

def test_missing_secret_fails_fast(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError):
        load_settings()
```

## Do
- Read secrets from environment variables or a store (Vault, cloud secret manager, sealed or encrypted files) at startup, and fail fast when one is missing.
- Commit `.env.example` with placeholder values only, and ignore `.env` in `.gitignore`.
- Run a secret scanner as a pre-commit hook and in CI, covering history on first run.
- Use distinct, least-privilege credentials per environment and per service, with an expiry where the provider supports it.
- Prefer short-lived credentials (workload identity, OIDC from CI) over long-lived keys.
- Rotate immediately when a secret is exposed: revoke first, then clean history. Deleting a commit does not un-leak it.
- Redact secrets in logs, error messages and crash reports.

## Avoid
- A default or fallback secret in code (`os.getenv("KEY", "dev-secret")`): it reaches production. Fail when unset.
- Baking secrets into Docker images with `ENV` or `COPY .env`: they persist in layers. Inject at runtime or use build secrets (`RUN --mount=type=secret`).
- Passing secrets as command-line arguments: they show in `ps` and shell history. Use stdin, files or env.
- Frontend bundles with API secrets (`NEXT_PUBLIC_*`, `VITE_*`): they ship to every browser. Keep them behind a server.
- Sharing one admin key across services and people: no audit trail and a huge blast radius. Issue scoped keys.
- Committing a key then "removing" it in the next commit: it stays in history. Rotate it.

## Review
- [ ] No secret in the diff, history, image layers or logs.
- [ ] A scanner runs on commit and in CI.
- [ ] Missing secrets stop startup with a clear error.
- [ ] Credentials are scoped and rotatable.
- [ ] Any exposure was treated as compromise and rotated.
