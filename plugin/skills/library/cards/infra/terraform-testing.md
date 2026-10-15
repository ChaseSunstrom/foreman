---
name: terraform-testing
title: Terraform testing
area: infra
tags: [terraform, opentofu, testing, tftest, policy, checkov, terratest]
detect: [file:*.tftest.hcl, file:.tflint.hcl, file:.checkov.yaml]
related: [terraform, terraform-modules, terraform-state, opentofu]
---
Testing Terraform: native `terraform test` plan and apply runs, static policy scans, and clean plans as the CI gate.

## Verify
- `terraform fmt -check -recursive`: formatting.
- `terraform validate`: static validity (after `terraform init -backend=false`).
- `terraform test`: runs every `*.tftest.hcl` file in the module and its `tests/` directory.
- `tflint --recursive`: provider-specific lint rules, when `.tflint.hcl` is present.
- `checkov -d .`: security policy scan, when Checkov is used.

## Test first
Plan-mode tests are fast and need no credentials with mocked providers.
```hcl
mock_provider "aws" {}

run "bucket_is_private" {
  command = plan
  variables { name = "logs" }
  assert {
    condition     = aws_s3_bucket_public_access_block.this.block_public_acls == true
    error_message = "public access must be blocked"
  }
}
```
Run `terraform test` and watch it fail before adding the resource.

## Do
- Prefer `command = plan` tests with `mock_provider` or `override_resource` for speed; use `command = apply` only in sandbox accounts.
- Use `expect_failures` to prove variable validations and preconditions reject bad input.
- Assert on outputs and resource attributes with `assert` blocks and clear `error_message`.
- Chain `run` blocks to feed one run's outputs into the next with `run.NAME.output`.
- Keep an `examples/` directory that plans cleanly and serve it as the integration fixture.
- Add `precondition` and `postcondition` lifecycle checks so misuse fails at plan time.
- Run static scans (tflint, Checkov or tfsec-family tools) in CI beside `terraform test`.
- For real-infra tests use short-lived isolated accounts and always destroy; `terraform test` destroys at the end of a file.

## Avoid
- Apply-mode tests against shared or production accounts: they create and destroy real resources. Use sandboxes and mocks.
- Asserting on whole-resource equality: brittle across provider versions. Assert on the attributes that matter.
- Skipping `terraform init` in CI for module tests: provider downloads are needed unless mocked. Run init first.
- Tests that need long-lived secrets in the repo: use environment credentials and OIDC.
- Ignoring plan warnings and deprecations: they become errors on upgrade. Treat them as failures in CI.
- Mocked tests as the only check: add at least one example plan against the real provider schema.

## Review
- [ ] Each variable validation has an `expect_failures` run.
- [ ] Core resource attributes are asserted.
- [ ] CI runs fmt, validate, test and one static scan.
- [ ] Apply-mode tests are isolated and destroy their resources.
- [ ] Mocks are paired with a real-provider plan.
