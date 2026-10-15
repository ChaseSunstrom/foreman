---
name: key-rotation
title: Key and secret rotation
area: security
tags: [security, rotation, keys, secrets, jwks, kms]
detect: []
related: [secrets-management, encryption-at-rest, jwt, api-keys, gitleaks]
---
Every key and secret can be replaced without downtime: versioned ids, overlapping validity, automated schedule, and a tested emergency path.

## Verify
- `pytest -q -k rotation`: dual-key acceptance and retirement tests pass.
- `git grep -nE "kid|key_id|key_version" -- ':!*test*'`: tokens and ciphertexts carry a key identifier.
- `gitleaks detect --source . --no-banner --redact`: no stale keys remain in history that need revoking.

## Test first
Old and new keys both verify during overlap, and the retired key fails.
```python
def test_rotation_overlap_and_retirement(keyring, signer):
    old = signer.sign({"sub": "u1"})
    keyring.rotate()                      # new key becomes primary, old stays verify-only
    assert keyring.verify(old)["sub"] == "u1"
    new = signer.sign({"sub": "u1"})
    assert keyring.header(new)["kid"] != keyring.header(old)["kid"]
    keyring.retire_old()
    with __import__("pytest").raises(Exception):
        keyring.verify(old)
    assert keyring.verify(new)["sub"] == "u1"
```

## Do
- Give every key an id (`kid`). Sign and encrypt with the newest, and accept or decrypt with any still-valid version.
- Load keys from a store at startup and on a refresh interval, so rotation needs no deploy.
- Rotate in phases: add the new key, make it primary, wait for the longest token or cache lifetime, then retire the old one.
- Publish public keys through a JWKS endpoint with caching that respects the overlap.
- For stored data, re-encrypt lazily on read or in a background job, and track progress by key version.
- Support two active credentials per integration (API keys, DB passwords) so clients switch without an outage.
- Automate with the secret manager's schedule. Alert on keys older than policy.
- Write and rehearse an emergency revoke: who triggers it, what breaks, how long it takes.

## Avoid
- Swapping a key in place with a single deploy: every in-flight token fails. Use overlap.
- No `kid`, so verifiers try one key: add ids and a lookup.
- Rotating the key but leaving the old value in env files, CI variables and backups: sweep all copies and revoke.
- Rotation that has never been run: it is untested until exercised. Schedule a drill.
- Treating a leak as a rotation task only: also review access logs for use of the leaked secret.
- Long-lived keys with no owner: assign an owner and an expiry date.

## Review
- [ ] Keys carry ids and the code supports multiple active versions.
- [ ] Rotation is automated and needs no deploy.
- [ ] Retired keys are revoked and removed from every store.
- [ ] Re-encryption progress is measurable.
- [ ] An emergency rotation runbook has been rehearsed.
