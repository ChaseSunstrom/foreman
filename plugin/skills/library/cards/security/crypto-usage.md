---
name: crypto-usage
title: Cryptography usage
area: security
tags: [security, cryptography, aes-gcm, hmac, random, keys]
detect: [dep:cryptography, dep:pycryptodome, dep:pynacl, dep:libsodium-wrappers, dep:tweetnacl, dep:ring, dep:github.com/google/tink/go, dep:bouncycastle]
related: [password-hashing, jwt, tls, secrets-management, webhook-signatures]
---
Crypto usage: use a high-level vetted library, authenticated encryption, CSPRNG randomness, constant-time compares, and managed keys.

## Verify
- `pytest -q tests/security/test_crypto.py`: round-trip, tamper, nonce-uniqueness and wrong-key tests pass.
- `grep -rnE "\b(md5|sha1|DES|RC4|ECB)\b|random\.(random|randint|choice)|Math\.random" src/`: no weak primitives or non-cryptographic randomness in security code.
- `bandit -r src -t B303,B304,B311,B324`: weak hash, cipher and random findings clear.

## Test first
```python
import pytest
def test_ciphertext_tamper_is_detected():
    blob = encrypt(b"secret", aad=b"user:1")
    bad = blob[:-1] + bytes([blob[-1] ^ 1])
    with pytest.raises(Exception):
        decrypt(bad, aad=b"user:1")

def test_same_plaintext_gives_different_ciphertext():
    assert encrypt(b"x", aad=b"") != encrypt(b"x", aad=b"")

def test_wrong_aad_fails():
    with pytest.raises(Exception):
        decrypt(encrypt(b"x", aad=b"a"), aad=b"b")
```

## Do
- Pick a high-level API: libsodium secretbox, `cryptography` `Fernet`, Tink, or `AESGCM` / ChaCha20-Poly1305 for AEAD.
- With AES-GCM use a fresh unique 96-bit nonce per message under a key, store it with the ciphertext, and bind context with associated data.
- Get random bytes from the OS (`secrets`, `os.urandom`, `crypto.randomBytes`, `crypto/rand`) for keys, nonces, tokens and ids.
- Compare MACs and tokens with constant-time functions (`hmac.compare_digest`, `crypto.timingSafeEqual`, `subtle.ConstantTimeCompare`).
- Use HMAC-SHA-256 for integrity with a shared key, and Ed25519 or ECDSA for signatures others verify.
- Derive keys from passwords with argon2id or scrypt, and from other keys with HKDF.
- Separate keys per purpose and rotate them. Keep key ids with the ciphertext so old data stays readable.
- Keep master keys in a KMS or HSM when available.

## Avoid
- ECB mode, unauthenticated CBC or CTR: patterns leak and bits can be flipped. Use an AEAD.
- Reusing a nonce with the same GCM or ChaCha key: it leaks plaintext and forges tags. Use random 96-bit nonces within limits, or a misuse-resistant scheme such as XChaCha20.
- `random` or `Math.random` for tokens: predictable. Use the OS CSPRNG.
- MD5 or SHA-1 for integrity or signatures: collisions. Use SHA-256 or better.
- `==` on MACs or tokens: timing leak. Use constant-time compare.
- Inventing a protocol (hash of key plus message, custom padding): use HMAC and established formats.
- Hardcoded keys or IVs in source: load keys from the secret store.
- Encrypting without authenticating the context (user id, version): ciphertexts get swapped. Bind with AAD.

## Review
- [ ] Only vetted libraries and AEAD modes are used.
- [ ] Randomness comes from the OS CSPRNG.
- [ ] Nonces are unique and keys are not hardcoded.
- [ ] Secret comparisons are constant-time.
- [ ] Keys are per-purpose, versioned and rotatable.
