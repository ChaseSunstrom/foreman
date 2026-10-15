---
name: password-hashing
title: Password hashing
area: security
tags: [security, passwords, argon2, bcrypt, auth, hashing]
detect: [dep:argon2-cffi, dep:bcrypt, dep:passlib, dep:argon2, dep:bcryptjs, dep:golang.org/x/crypto, dep:argon2id]
related: [crypto-usage, sessions, rate-limiting, secrets-management, pii-logging]
---
Store passwords with a slow, salted, memory-hard hash (argon2id, else scrypt or bcrypt), verify in constant time, and rehash on login.

## Verify
- `pytest -q tests/security/test_passwords.py`: hash format, verify, rehash and no-plaintext tests pass.
- `grep -rniE "md5|sha1|sha256\(.*password" src/`: no fast general-purpose hash applied to passwords.
- `grep -rniE "password" src/ | grep -iE "log|print"`: no password reaches a log line.

## Test first
```python
from argon2 import PasswordHasher
ph = PasswordHasher()

def test_hash_is_salted_and_not_plaintext():
    a, b = hash_password("hunter2hunter2"), hash_password("hunter2hunter2")
    assert a != b and "hunter2" not in a and a.startswith("$argon2id$")

def test_wrong_password_fails_and_old_hash_is_upgraded(db, user_with_old_hash):
    assert not verify_password(user_with_old_hash, "wrong")
    assert verify_password(user_with_old_hash, "right-password")
    assert db.get(user_with_old_hash.id).hash.startswith("$argon2id$")
```

## Do
- Use `argon2-cffi` `PasswordHasher` (argon2id), Node `argon2`, or `golang.org/x/crypto/argon2` `IDKey`. Use bcrypt only when argon2 is unavailable.
- Let the library generate the salt and store its full encoded string, so parameters travel with the hash.
- Tune cost so one hash takes roughly 100-500 ms on production hardware, and raise it over time.
- On successful login, check `check_needs_rehash` (argon2-cffi) and store the upgraded hash.
- Enforce a minimum length (at least 8, prefer 12 or more) and a generous maximum (64 or more). Allow all characters. Check against a breached-password list.
- Apply rate limiting and lockout backoff to login and reset endpoints.
- Make reset tokens random, single-use, short-lived, and stored hashed.

## Avoid
- MD5, SHA-1 or plain SHA-256 for passwords: GPUs crack them fast. Use argon2id, scrypt or bcrypt.
- A global static salt or "pepper" as the only salt: use per-password random salts. A pepper is extra, held outside the database.
- bcrypt on inputs over 72 bytes: it silently truncates. Pre-hash with care or use argon2.
- Comparing hashes with `==`: use the library verify function, which is constant time.
- Distinct errors for unknown user and wrong password: it enumerates accounts. Return one message, and hash a dummy value on unknown users to equalize timing.
- Emailing passwords or logging request bodies that contain them: scrub the field.

## Review
- [ ] Hash is argon2id, scrypt or bcrypt with per-password salt.
- [ ] Cost is tuned, and rehash on login is in place.
- [ ] Login errors and timing do not reveal which accounts exist.
- [ ] Reset tokens are random, expiring, single-use.
- [ ] Passwords never appear in logs, errors or analytics.
