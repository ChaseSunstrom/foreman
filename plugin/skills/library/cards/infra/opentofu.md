---
name: opentofu
title: OpenTofu
area: infra
tags: [opentofu, tofu, iac, hcl, state, encryption]
detect: [file:*.tofu, file:.opentofu-version, file:.terraform.lock.hcl, file:*.tofu.json]
related: [terraform, pulumi, ansible, vault]
---
OpenTofu: the open-source Terraform fork using the `tofu` CLI, HCL, shared providers and native state encryption.

## Verify
- `tofu fmt -check -recursive`: formatting.
- `tofu init -backend=false && tofu validate`: syntax and references without state access.
- `tofu plan -out=tfplan -input=false`: the saved change set.
- `tofu show -json tfplan`: machine-readable plan for policy checks.
- `tofu test`: runs `*.tftest.hcl` (and `*.tofutest.hcl`) tests.

## Test first
Plan-mode tests need no credentials for the assertions that only read config.
```hcl
run "tags_required" {
  command = plan
  variables { environment = "prod" }
  assert {
    condition     = local.tags["env"] == "prod"
    error_message = "env tag must follow the environment variable"
  }
}
```
Red first: fails until `local.tags` is defined from the variable.

## Do
- Use `tofu`, not `terraform`, in scripts and CI, and pin the tool with `required_version` or `.opentofu-version`.
- Pin providers with `required_providers` and commit `.terraform.lock.hcl` (OpenTofu reads the same lock file name).
- Configure state encryption in the `terraform { encryption { ... } }` block with a key provider (`pbkdf2`, or a KMS), and a `method "aes_gcm"`.
- Reach for `.tofu` files when a file must be OpenTofu-only, which lets Terraform-compatible `.tf` files coexist.
- Use `for_each`, `moved`, `import` and `removed` blocks the same way as Terraform to refactor safely.
- Use provider-defined `for_each` on providers and `enabled` in `lifecycle` only after checking the version in use supports it.
- Apply a saved plan, and run `plan` in CI on pull requests.

## Avoid
- Assuming every Terraform feature or provider-registry path is identical: check provider sources (`registry.opentofu.org`) and release notes before upgrading.
- Mixing `terraform` and `tofu` against the same state: the state format and lock can diverge. Choose one per root module.
- Encryption keys or passphrases in `.tf` literals: they commit to git. Pass via variables, env, or a KMS key provider.
- Enabling encryption with no `fallback` during migration: existing unencrypted state becomes unreadable. Add a fallback method, then remove it.
- `-auto-approve` on unreviewed plans: apply the saved plan.
- `count` indexing over lists: reordering churns resources. Use `for_each` over a map.
- Committing `.terraform/` or `*.tfstate`: add them to `.gitignore`.

## Review
- [ ] `tofu validate` and `tofu test` pass and the plan is reviewed.
- [ ] State is remote, locked and encrypted, with keys held outside the repo.
- [ ] CI and docs call `tofu` consistently with a pinned version.
- [ ] Provider and module versions are pinned, and the lock file is committed.
