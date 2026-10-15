---
name: terraform
title: Terraform
area: infra
tags: [terraform, iac, hcl, state, modules, plan]
detect: [ext:.tf, file:*.tfvars, file:.terraform.lock.hcl, file:terraform.tf]
related: [opentofu, pulumi, ansible, vault, kubernetes]
---
Terraform: declarative HCL with remote locked state, version-pinned providers and modules, and reviewed plans.

## Verify
- `terraform fmt -check -recursive`: formatting.
- `terraform init -backend=false && terraform validate`: syntax, types and references, without touching state.
- `terraform plan -out=tfplan -input=false`: the exact change set, saved for apply.
- `terraform show -json tfplan`: machine-readable plan for policy checks (no deletes of stateful resources).
- `terraform test`: runs `*.tftest.hcl` files, when present.

## Test first
Native tests live in `tests/*.tftest.hcl` and can run against a plan with no apply.
```hcl
run "bucket_is_private" {
  command = plan
  assert {
    condition     = aws_s3_bucket_public_access_block.this.block_public_acls == true
    error_message = "public ACLs must be blocked"
  }
}
```
Red first: it fails until the resource and its setting exist.

## Do
- Configure a remote backend with locking and encryption, and never commit `*.tfstate`.
- Pin `required_version` and each `required_providers` entry with a `~>` constraint, and commit `.terraform.lock.hcl`.
- Pin module sources by version or git ref.
- Give variables a `type`, `description` and `validation`. Mark secrets `sensitive = true`.
- Use `for_each` over a map keyed by stable ids, not `count`, so removing an item doesn't shift the rest.
- Use `moved` blocks to rename or restructure instead of destroy and recreate, and `import` blocks to adopt resources.
- Use `lifecycle { prevent_destroy = true }` on stateful resources, and `create_before_destroy` where replacement must not drop traffic.
- Apply only a saved plan: `terraform apply tfplan`.

## Avoid
- `terraform apply -auto-approve` without a reviewed plan: unreviewed destroys. Apply the saved plan file.
- `count` over a list of objects: reordering destroys and recreates. Use `for_each` keyed by name.
- Secrets in `.tfvars` or defaults: they land in state and git. Use a secret manager data source and `sensitive`.
- Local state or a shared state without locking: corrupted concurrent applies. Use a locking backend.
- Provider with no version constraint: a major upgrade breaks the plan. Pin it.
- `terraform state rm` or hand-editing state to fix drift: use `import`, `moved` or `removed` blocks.
- `provisioner "local-exec"` for configuration: not tracked in state. Use a resource or configuration tool.
- `depends_on` on modules for ordering that references already imply: it widens the plan. Reference an output.

## Review
- [ ] Plan shows only intended creates, updates and deletes, and nothing replaces stateful resources.
- [ ] Providers, modules and Terraform are pinned, and the lock file is committed.
- [ ] Sensitive values are marked and absent from outputs and logs.
- [ ] Resource addresses stay stable, using `moved` for refactors.
