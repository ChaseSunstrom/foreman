---
name: sops
title: SOPS
area: infra
tags: [sops, secrets, age, encryption, gitops, kms]
detect: [file:.sops.yaml, file:*.sops.yaml, file:*.sops.json, file:*.enc.yaml]
related: [sealed-secrets, external-secrets, vault, flux, terraform-state]
---
SOPS: encrypt values inside YAML, JSON, ENV and INI files with age or a cloud KMS, so secrets live safely in git.

## Verify
- `sops --decrypt secrets.enc.yaml >/dev/null`: you hold a key that can decrypt it.
- `grep -c 'ENC\[' secrets.enc.yaml`: values are encrypted (nonzero) and the file has a `sops:` metadata block.
- `sops filestatus secrets.enc.yaml`: reports whether the file is encrypted (when available in your version).
- `git grep -nE 'AGE-SECRET-KEY'`: no age private key was committed (expect no output).

## Test first
Make plain secrets fail CI before encrypting.
```bash
for f in $(git ls-files 'secrets/*.yaml'); do
  grep -q '^sops:' "$f" || { echo "plaintext secret: $f"; exit 1; }
done
```
Then `sops --encrypt --in-place secrets/app.yaml` and the check passes.

## Do
- Define rules in `.sops.yaml` under `creation_rules` with `path_regex` and `age` recipients (or `kms`, `pgp`); every new file is encrypted to those recipients automatically.
- Prefer age keys: `age-keygen -o key.txt`; share only the public `age1...` recipient in `.sops.yaml`.
- Keep the private key out of the repo: set `SOPS_AGE_KEY_FILE` or use cloud KMS with IAM.
- Use `encrypted_regex` (for example `^(data|stringData)$`) so Kubernetes manifests keep readable metadata.
- List several recipients (team members plus CI) and run `sops updatekeys FILE` after changing them.
- Edit with `sops FILE` (decrypts into your editor and re-encrypts on save).
- Rotate data keys with `sops --rotate --in-place FILE` after membership changes or leaks.
- Pair with Flux (`decryption.provider: sops`) or helm-secrets for deploys.

## Avoid
- Committing the age private key or a decrypted copy: full compromise. Ignore `key.txt` and `*.dec.*` files.
- Encrypting without a `.sops.yaml`, then pasting recipients ad hoc: inconsistent access. Use creation rules.
- Removing a person from `.sops.yaml` and assuming access is revoked: old ciphertext remains decryptable by them. Run `updatekeys`, rotate the data key and rotate the secrets themselves.
- Editing encrypted files by hand: breaks the MAC check. Use `sops FILE`.
- Merge conflicts resolved by taking one side blindly: re-decrypt both sides, merge, re-encrypt.
- Whole-file encryption of manifests: unreadable diffs. Encrypt values only via `encrypted_regex`.

## Review
- [ ] `.sops.yaml` rules cover every secrets path.
- [ ] Private keys are out of the repo and CI uses scoped keys.
- [ ] Recipients list matches current team membership.
- [ ] CI blocks plaintext secrets.
- [ ] Rotation procedure is documented.
