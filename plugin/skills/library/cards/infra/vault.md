---
name: vault
title: HashiCorp Vault
area: infra
tags: [vault, secrets, policies, auth, kv, pki]
detect: [file:*.hcl, file:vault.hcl, file:vault-config.hcl, file:policies/*.hcl, dep:hvac, dep:node-vault, dep:github.com/hashicorp/vault/api]
related: [terraform, kubernetes, cert-manager, ansible, argo-cd]
---
Vault: central secrets with auth methods, least-privilege policies, KV v2, dynamic credentials and audit devices.

## Verify
- `vault status`: initialized, unsealed, and the HA mode.
- `vault policy fmt policies/app.hcl`: formats the policy file and fails on syntax errors.
- `vault token capabilities secret/data/app/config`: what the current token can do on a path.
- `vault policy write app policies/app.hcl && vault token create -policy=app -ttl=5m`: a short-lived token to test with.
- `vault audit list`: at least one audit device is enabled.

## Test first
Test a policy by minting a token and asserting allow and deny, against a dev server (`vault server -dev`).
```sh
vault policy write app policies/app.hcl
T=$(vault token create -policy=app -ttl=5m -field=token)
VAULT_TOKEN=$T vault kv get secret/app/config                 # red until the policy grants read
! VAULT_TOKEN=$T vault kv get secret/other/config 2>/dev/null  # must be denied
```

## Do
- Write policies with explicit paths and minimal capabilities. KV v2 paths need `secret/data/...` for reads and `secret/metadata/...` for lists.
- Authenticate workloads with machine identities (Kubernetes, AppRole, JWT/OIDC, cloud IAM) and short token TTLs.
- Prefer dynamic secrets (database, cloud) with leases over static ones.
- Use KV v2 (`vault kv put secret/app key=val`) for versioned static secrets.
- Enable at least one audit device (`vault audit enable file file_path=...`).
- Renew or re-login before token expiry, and revoke leases on shutdown.
- Use auto-unseal with a KMS or transit seal, and use Raft integrated storage with periodic snapshots.
- Use the `transit` engine for encryption as a service, so apps never hold keys.

## Avoid
- `-dev` mode or the root token in real use: dev is in-memory and unsealed. Revoke the root token after setup and use scoped tokens.
- Reading `secret/app` via the CLI path but writing policy for `secret/app`: KV v2 needs the `data/` prefix in policies. Fix the path.
- Long-lived static tokens in environment variables and CI: they leak. Use workload auth and short TTLs.
- Wildcard policies like `path "*" { capabilities = ["read","list","create","update","delete"] }` : effectively root. List specific paths.
- Printing secrets in logs (`vault kv get` in CI with echo): masked only if registered. Pass directly to the consumer.
- Skipping audit devices: if every audit device blocks, Vault stops serving, so run two, and without any you lose forensics.
- Storing the unseal keys or root token together in one place: one compromise opens everything. Use auto-unseal or Shamir split among custodians.
- `vault kv put` with a secret value as a CLI argument: lands in shell history. Use `@file` or stdin (`-`).

## Review
- [ ] Policies are path-specific, tested for allow and deny, and use the right KV v2 paths.
- [ ] Workloads authenticate with machine identity and short TTLs.
- [ ] Audit is enabled, auto-unseal is in place, and the root token is revoked.
- [ ] No secrets in shell history, logs or repo.
