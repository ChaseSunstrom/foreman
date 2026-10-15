---
name: terraform-state
title: Terraform state
area: infra
tags: [terraform, opentofu, state, backend, locking, import, drift]
detect: [file:backend.tf, file:terraform.tfstate, file:.terraform.lock.hcl]
related: [terraform, terraform-modules, terragrunt, opentofu, sops]
---
Terraform state: remote encrypted backend with locking, safe refactors with moved and import blocks, and drift detection.

## Verify
- `terraform init -backend=false && terraform validate`: config is valid.
- `terraform plan -detailed-exitcode`: exit 0 means no changes, 2 means drift or pending changes, 1 means error.
- `terraform state list`: resources tracked in state.
- `terraform plan -refresh-only`: shows drift from real infrastructure without proposing config changes.

## Test first
Make drift detection a failing check before changing anything.
```bash
terraform plan -detailed-exitcode -input=false -lock-timeout=60s
code=$?
test $code -eq 0 || { echo "plan not clean: $code"; exit 1; }
```
For a refactor, assert the plan has zero `destroy` actions: `terraform plan -out=p && terraform show -json p | jq -e '[.resource_changes[].change.actions[]] | all(. != "delete")'`.

## Do
- Use a remote backend with locking (S3 with `use_lockfile` or a DynamoDB table, GCS, azurerm); enable versioning and encryption on the bucket.
- Split state by blast radius and lifecycle (network, data, apps), not one giant state.
- Refactor with `moved` blocks and adopt resources with `import` blocks, then review them in the plan.
- Always plan to a file and apply that file: `terraform plan -out=tfplan` then `terraform apply tfplan`.
- Commit `.terraform.lock.hcl`; never commit `terraform.tfstate` or `.terraform/`.
- Restrict access to the state backend; state holds secrets in plain JSON.
- Use `-lock-timeout` in CI and never `-lock=false` outside break-glass.
- Share cross-state values through outputs and `terraform_remote_state` or a data source on the real resource.

## Avoid
- Local state in a team repo: lost or divergent state. Use a remote backend.
- `terraform state rm` or `state mv` as a first resort: hand edits desync. Prefer `moved` and `removed` blocks.
- `-lock=false` to get past a stuck lock: concurrent writes corrupt state. Confirm no run is active, then `terraform force-unlock ID`.
- Backend config with inline credentials: they land in `.terraform/` and plan files. Use environment or workload identity.
- Applying an unreviewed plan output generated earlier against different state: it is rejected as stale, so re-plan.
- Interpolation in the `backend` block: not supported. Use `-backend-config` files or partial config.

## Review
- [ ] Backend is remote, locked, encrypted and versioned.
- [ ] Refactors show no destroy actions in the plan.
- [ ] State files and local caches are ignored by git.
- [ ] CI plans clean (exit 0) on main.
- [ ] State access is limited and audited.
