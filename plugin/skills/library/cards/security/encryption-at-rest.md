---
name: encryption-at-rest
title: Encryption at rest
area: security
tags: [security, encryption, aead, kms, envelope, data-protection]
detect: []
related: [crypto-usage, key-rotation, secrets-management, pii-logging, tls]
---
Encrypt sensitive data with an AEAD under keys held in a KMS: envelope encryption, unique nonces, context binding, and tested key separation.

## Verify
- `pytest -q -k encrypt`: round-trip, tamper and wrong-context tests pass.
- `git grep -nE "AES.*(ECB|CBC)|MODE_ECB|createCipher\(|DES|RC4" -- ':!*test*'`: no weak modes or ciphers.
- `git grep -nE "(key|KEY) *= *b?['\"][A-Za-z0-9+/=]{16,}" -- ':!*test*'`: no hard-coded data keys.
- `lsblk -o NAME,FSTYPE | grep -i crypt`: disk-level encryption is active on the host, where relevant.

## Test first
Tampering and context swaps must fail.
```python
import pytest

def test_ciphertext_is_authenticated_and_context_bound(vault):
    ct = vault.encrypt(b"123-45-6789", context={"user": "u1", "field": "ssn"})
    assert b"123-45" not in ct
    assert vault.decrypt(ct, context={"user": "u1", "field": "ssn"}) == b"123-45-6789"
    with pytest.raises(Exception):
        vault.decrypt(ct, context={"user": "u2", "field": "ssn"})
    with pytest.raises(Exception):
        vault.decrypt(ct[:-1] + bytes([ct[-1] ^ 1]), context={"user": "u1", "field": "ssn"})
```

## Do
- Use an AEAD: AES-256-GCM or ChaCha20-Poly1305 (or XChaCha20), through a vetted library such as libsodium, `cryptography` or the cloud SDK.
- Use envelope encryption: a per-record or per-tenant data key encrypted by a KMS key. Store the wrapped key with the ciphertext and a key id.
- Generate every nonce from a CSPRNG, or use a deterministic counter scheme that never repeats under a key. Never reuse one.
- Bind ciphertext to its record with associated data (tenant, row id, field).
- Encrypt specific sensitive fields and backups, and also enable storage-level encryption for disks, buckets and snapshots.
- Keep keys in a KMS or HSM with IAM limits. Application code gets decrypt rights only for its own keys.
- Version ciphertext with a key id so rotation can re-encrypt lazily.
- For searchable fields, use a separate keyed blind index (HMAC) rather than deterministic encryption.

## Avoid
- Rolling your own scheme, or using ECB, or CBC with no MAC: use an AEAD from a high-level library.
- A key in source, in env files in git, or beside the data: fetch from a KMS at runtime.
- Static IV or nonce reuse under GCM: it breaks both secrecy and authenticity.
- Using a password as a key directly: derive with a KDF (Argon2id or scrypt) and a salt.
- Encrypting without associated data, so ciphertexts can be swapped between rows: bind context.
- Treating disk encryption as protection from application bugs or a stolen DB credential: encrypt fields as well.

## Review
- [ ] AEAD only, with unique nonces and bound context.
- [ ] Keys are managed in KMS, never stored with data or in code.
- [ ] Each ciphertext records a key version.
- [ ] Backups and replicas are encrypted too.
- [ ] Decrypt access is limited and audited.
