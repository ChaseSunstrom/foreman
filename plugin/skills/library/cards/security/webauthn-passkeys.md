---
name: webauthn-passkeys
title: WebAuthn and passkeys
area: security
tags: [security, webauthn, passkeys, authentication, fido2]
detect: [dep:@simplewebauthn/server, dep:webauthn, dep:github.com/go-webauthn/webauthn]
related: [mfa-totp, account-recovery, sessions, cors]
---
Passkey login: server-issued single-use challenge, pinned RP ID and origin, sign counter checks, safe recovery.

## Verify
- `pytest -q -k webauthn`: the challenge and origin tests pass.
- `git grep -nE "rp_?id|expected_?origin|expectedOrigin" -- ':!*test*'`: RP ID and origin come from config, never from the request.
- `curl -sI https://localhost:8443/ -k | grep -i strict-transport`: HSTS is on, since WebAuthn needs a secure context.

## Test first
A challenge is bound to one ceremony and used once.
```python
def test_assertion_with_reused_challenge_is_rejected(client, passkey):
    ch = client.post("/webauthn/login/options").json()["challenge"]
    body = passkey.sign(challenge=ch, origin="https://app.example")
    assert client.post("/webauthn/login/verify", json=body).status_code == 200
    assert client.post("/webauthn/login/verify", json=body).status_code == 400

def test_assertion_from_other_origin_is_rejected(client, passkey):
    ch = client.post("/webauthn/login/options").json()["challenge"]
    body = passkey.sign(challenge=ch, origin="https://evil.example")
    assert client.post("/webauthn/login/verify", json=body).status_code == 400
```

## Do
- Use a maintained library for verification. Do not parse CBOR or COSE yourself.
- Generate at least 16 random bytes per challenge. Store it server-side with a short TTL, bound to the session, and delete on use.
- Pin `rpId` and the expected origin list in config.
- Verify the signature, challenge, origin, RP ID hash, and the user-present flag. Require user verification for passwordless login.
- Store credential id, public key, sign count and transports. Reject a nonzero counter that fails to increase.
- Let users register more than one passkey, and list and remove them behind step-up auth.
- Plan recovery up front: a second passkey, recovery codes, or verified-identity reset.

## Avoid
- Taking `origin` or `rpId` from request headers: an attacker picks them. Read from config.
- Reusing or predictable challenges: replay works. Random, single-use, expiring.
- Skipping attestation verification choices: use `none` unless you truly need hardware policy, and do not half-verify.
- Storing a private-key-like secret per user: only the public key lives on the server.
- Treating a passkey as the whole account when email reset bypasses it: harden recovery to match.
- Resident-key or user-handle mixups: key lookups on credential id and verify the user handle matches.

## Review
- [ ] Challenge is random, single-use, expiring and session-bound.
- [ ] RP ID and origins are fixed in config and tested with a wrong origin.
- [ ] Counter and user-verification flags are checked.
- [ ] Multiple credentials and a recovery path exist.
- [ ] Credential add and remove require recent authentication.
