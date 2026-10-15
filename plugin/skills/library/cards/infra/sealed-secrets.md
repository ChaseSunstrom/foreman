---
name: sealed-secrets
title: Sealed Secrets
area: infra
tags: [kubernetes, secrets, sealed-secrets, kubeseal, gitops, encryption]
detect: [file:sealedsecret*.yaml, file:*-sealed.yaml]
related: [external-secrets, sops, kubernetes-rbac, flux, argo-cd]
---
Sealed Secrets: encrypt Secrets with kubeseal so only the in-cluster controller can decrypt them, making them safe to commit.

## Verify
- `kubectl get sealedsecret -A`: resources exist and the controller synced them.
- `kubectl describe sealedsecret NAME -n NS`: events show `Unsealed` or the decrypt error.
- `kubectl get secret NAME -n NS`: the plain Secret was produced.
- `kubeseal --validate < sealed.yaml`: the controller can decrypt this file.

## Test first
Check that no plain Secret is committed, then seal.
```bash
! git ls-files '*.yaml' | xargs grep -lE '^kind: Secret$'   # plain Secrets fail the check
kubeseal --format yaml < secret.yaml > sealed.yaml
kubeseal --validate < sealed.yaml
```
Run the first line in CI so a plain Secret fails the build.

## Do
- Seal against the right namespace and name: the default `strict` scope binds ciphertext to both.
- Fetch the public cert with `kubeseal --fetch-cert` and pin it for offline sealing.
- Back up the controller's sealing keys (Secrets labeled `sealedsecrets.bitnami.com/sealed-secrets-key`) somewhere safe; losing them makes every sealed file undecryptable.
- Delete the plain Secret file after sealing and keep it out of git history.
- Expect key rotation: the controller renews keys periodically and keeps old ones to decrypt.
- Use `spec.template` to set labels, annotations and type of the resulting Secret.
- Re-seal and rotate the underlying credential after any suspected leak, since old ciphertext stays decryptable.

## Avoid
- `--scope cluster-wide` by default: a sealed value can be moved to any namespace. Use strict scope.
- Piping a plain Secret through `kubectl create secret ... --dry-run=client -o yaml` into a committed file: commit only the sealed output.
- Rebuilding the cluster without restoring the controller key: all SealedSecrets fail to decrypt. Restore keys first.
- Treating sealing as rotation: it hides the value, it does not change it.
- Putting a Secret `data` field value in `stringData` logs or shell history: use stdin.
- Editing the ciphertext by hand: re-run kubeseal.

## Review
- [ ] No plain `kind: Secret` with real data is tracked.
- [ ] Scope is strict unless a reason is written down.
- [ ] Controller key backup exists and has been restore-tested.
- [ ] Resulting Secret type and labels are correct.
- [ ] A sealed file validates against the live controller.
