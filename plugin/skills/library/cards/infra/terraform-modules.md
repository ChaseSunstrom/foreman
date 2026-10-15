---
name: terraform-modules
title: Terraform modules
area: infra
tags: [terraform, opentofu, modules, hcl, versioning, registry]
detect: [file:versions.tf, file:variables.tf, file:outputs.tf]
related: [terraform, terraform-state, terraform-testing, terragrunt, opentofu]
---
Reusable Terraform modules: narrow inputs, typed and validated variables, pinned providers and versions, minimal outputs.

## Verify
- `terraform fmt -check -recursive`: formatting.
- `terraform init -backend=false && terraform validate`: syntax and type checks without touching state.
- `tflint --recursive`: provider-aware lint, if tflint is configured.
- `terraform-docs markdown table .`: inputs and outputs documentation generated from code, if terraform-docs is used.

## Test first
Write a `terraform test` run for the contract before the resources.
```hcl
# tests/basic.tftest.hcl
run "rejects_bad_cidr" {
  command = plan
  variables { cidr = "not-a-cidr" }
  expect_failures = [var.cidr]
}
```
Run with `terraform test`. Add a second `run` with `command = plan` asserting an output or resource attribute.

## Do
- Layout: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`, `examples/`, `tests/`.
- Type every variable (`object({...})` with `optional()` defaults), add `description`, and use `validation` blocks with clear `error_message`.
- Declare `required_version` and `required_providers` with a source and a version constraint; do not configure providers (no `provider` blocks) inside a reusable module.
- Mark secrets `sensitive = true` in variables and outputs.
- Use `for_each` over a map with stable keys rather than `count` for collections.
- Expose only the outputs callers need (ids, arns); keep internal resources private.
- Pin consumers to a module version (`version = "~> 2.1"` for registry, `?ref=v2.1.0` for git) and release with tags.
- Use `moved` blocks when renaming resources so state is not destroyed.

## Avoid
- `count` with a list of names: removing one element shifts and recreates the rest. Use `for_each` keyed by name.
- `provider` configuration inside a module: it breaks `for_each` and removal of the module. Pass providers via `providers = {}`.
- Unpinned `source` refs like a bare branch name: a surprise upgrade. Pin a tag or version.
- Wrapper modules that only re-expose a single resource: more surface than value. Call the resource directly.
- Output of whole resource objects: leaks sensitive attributes and couples callers to internals. Output specific fields.
- Renames without `moved`: Terraform plans destroy and create. Add `moved { from = ... to = ... }`.

## Review
- [ ] Variables are typed, described and validated.
- [ ] Providers and Terraform versions are constrained.
- [ ] `terraform test` or an example plans cleanly.
- [ ] Renames carry `moved` blocks.
- [ ] No secrets in defaults or outputs.
