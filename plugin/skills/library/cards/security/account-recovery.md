---
name: account-recovery
title: Account recovery
area: security
tags: [security, password-reset, recovery, authentication, tokens, email]
detect: []
related: [mfa-totp, webauthn-passkeys, email-security, rate-limiting, sessions]
---
Password reset and recovery: single-use hashed tokens, short expiry, uniform responses, rate limits, session revocation, and a notice to the owner.

## Verify
- `pytest -q -k "reset or recovery"`: token and enumeration tests pass.
- `git grep -nE "reset_token|password_reset" -- ':!*test*'`: tokens are only stored through the hashing helper.
- `git grep -nE "Host|X-Forwarded-Host|request\.host" -- '*reset*' '*mail*'`: reset links are built from configured base URL, never request headers.

## Test first
Responses must not reveal whether an account exists, and tokens must be one-shot.
```python
def test_reset_request_is_uniform(client, user):
    a = client.post("/reset", json={"email": user.email})
    b = client.post("/reset", json={"email": "nobody@nowhere.example"})
    assert (a.status_code, a.json()) == (b.status_code, b.json())

def test_reset_token_is_single_use_and_revokes_sessions(client, user, issue_token, session_of):
    tok = issue_token(user)
    assert client.post("/reset/confirm", json={"token": tok, "password": "N3w-long-passphrase"}).status_code == 200  # pragma: allowlist secret
    assert client.post("/reset/confirm", json={"token": tok, "password": "Other-long-pass-1"}).status_code == 400  # pragma: allowlist secret
    assert session_of(user).is_valid() is False
```

## Do
- Generate the token with a CSPRNG (at least 128 bits), store only its hash with the user id, expiry (15–60 minutes) and a used flag.
- Return the same message and a similar response time whether or not the account exists. Send the mail asynchronously.
- Rate limit per account and per IP for requests and for confirmation attempts.
- Build the link from a configured base URL. Put the token in the path or fragment, and set `Referrer-Policy: no-referrer` on the page.
- On success: invalidate the token and all other outstanding tokens, revoke all sessions and API refresh tokens, and email the owner.
- Do not log the user in automatically after reset unless MFA still applies.
- Keep MFA in force during recovery. Offer recovery codes or a second passkey, and add a delay plus notices for factor-reset flows.
- Re-check password policy and breach lists on the new password.

## Avoid
- Security questions: answers are guessable or public. Use out-of-band proof.
- Sequential or time-based tokens, or a hash of the email: use random bytes.
- Building the reset URL from the `Host` header: poisoning sends the token to an attacker. Use configuration.
- "No account with that email" messages: they enable enumeration. Use one message.
- Leaving old sessions alive after a reset: the attacker stays logged in. Revoke them.
- Recovery that skips MFA through support or email alone: that makes MFA optional. Require a stronger, delayed process.

## Review
- [ ] Tokens are random, hashed at rest, short-lived and single-use.
- [ ] Request responses are uniform in body, status and timing.
- [ ] Links use configured hosts only.
- [ ] Reset revokes sessions and notifies the owner.
- [ ] MFA cannot be bypassed through recovery.
