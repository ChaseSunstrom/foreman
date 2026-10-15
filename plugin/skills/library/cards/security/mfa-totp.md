---
name: mfa-totp
title: MFA with TOTP
area: security
tags: [security, mfa, totp, authentication, recovery-codes]
detect: [dep:pyotp, dep:otplib]
related: [webauthn-passkeys, account-recovery, rate-limiting, sessions, password-hashing]
---
TOTP second factor: encrypted secrets, single-use codes, attempt limits, hashed recovery codes, step-up on change.

## Verify
- `pytest -q -k totp`: replay, lockout and drift tests pass.
- `git grep -nE "totp_secret|otp_secret" -- ':!*test*'`: the secret is only touched through the encrypt and decrypt helpers.
- `git grep -nE "valid_window|window *=" -- ':!*test*'`: the accepted drift window is small and deliberate.

## Test first
A code must work once only.
```python
import pyotp

def test_totp_code_cannot_be_replayed(client, user_with_totp):
    code = pyotp.TOTP(user_with_totp.secret).now()
    assert client.post("/mfa/verify", json={"code": code}).status_code == 200
    client.post("/logout")
    client.post("/login", json=user_with_totp.creds)
    assert client.post("/mfa/verify", json={"code": code}).status_code == 401
```

## Do
- Generate the secret with a CSPRNG (`pyotp.random_base32()`), at least 160 bits. Show it once at enrollment.
- Store the secret encrypted (envelope key), never in plaintext or logs.
- Activate only after the user proves one valid code at enrollment.
- Record the last accepted time step per user and reject any code at or before it.
- Allow a window of one step either side at most. Compare with a constant-time check.
- Rate limit per account, not just per IP. Lock or back off after about 5 failures.
- Issue 8–10 random recovery codes, store them hashed, and mark each used once.
- Require a fresh password or MFA to disable, change or re-enroll the factor.
- Keep the half-authenticated state in a separate session flag that grants nothing else.

## Avoid
- Marking the session fully logged in after the password and checking MFA client-side: gate every route on the server flag.
- Accepting the same code twice inside its window: persist last-used step.
- Unlimited attempts: 6 digits fall quickly. Throttle and alert.
- Plaintext recovery codes in the DB: hash them like passwords.
- SMS as the only or fallback factor: offer TOTP or WebAuthn, and treat SMS as weaker.
- Letting a session-hijacker turn MFA off silently: require re-auth and email notice.

## Review
- [ ] The secret is encrypted at rest and shown only at enrollment.
- [ ] Used steps are rejected and attempts are limited per account.
- [ ] Recovery codes are hashed, single-use and regenerable.
- [ ] MFA disable and enroll need step-up auth and notify the user.
- [ ] No route returns data in the pending-MFA state.
