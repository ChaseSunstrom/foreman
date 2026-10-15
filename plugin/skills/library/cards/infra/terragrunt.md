---
name: terragrunt
title: Terragrunt
area: infra
tags: [terragrunt, terraform, opentofu, dry, environments, hcl]
detect: [file:terragrunt.hcl, file:root.hcl, file:terragrunt.stack.hcl]
related: [terraform, terraform-state, terraform-modules, opentofu]
---
Terragrunt: DRY backend and provider config, per-environment units, explicit dependencies and run-all orchestration.

## Verify
- `terragrunt hcl format --check`: formatting of HCL files (older releases use `terragrunt hclfmt --terragrunt-check`).
- `terragrunt validate`: unit validates after init.
- `terragrunt plan`: plan for one unit from its directory.
- `terragrunt run-all plan`: plan across all units in dependency order (newer releases also offer `terragrunt run --all plan`).

## Test first
Assert the plan outcome for a new unit before applying.
```bash
cd live/dev/vpc
terragrunt plan -detailed-exitcode
# expect 2 (changes) the first time and 0 after apply
terragrunt apply -auto-approve && terragrunt plan -detailed-exitcode
```
In CI, a clean `run-all plan -detailed-exitcode` on main is the drift check.

## Do
- Keep a root file (`root.hcl` or the parent `terragrunt.hcl`) holding `remote_state` and `generate "provider"`; units include it with `include "root" { path = find_in_parent_folders("root.hcl") }`.
- Use `remote_state` with `generate` for `backend.tf` and a per-unit `key` built from `path_relative_to_include()`.
- Point units at modules with `terraform { source = "...//modules/vpc?ref=v1.2.0" }`, pinned to a tag.
- Declare `dependency "vpc" { config_path = "../vpc" }` and read `dependency.vpc.outputs`; set `mock_outputs` for plan before the dependency applies.
- Share values through `locals` and `read_terragrunt_config`, with env-level files like `env.hcl`.
- Run `run-all` with a parallelism cap and review plans before `apply`.
- Commit `.terraform.lock.hcl` per unit or generate it consistently.

## Avoid
- Unpinned module `source` refs: a surprise change applies to every environment. Pin a tag.
- `mock_outputs` allowed for `apply`: real infra gets fake ids. Use `mock_outputs_allowed_terraform_commands = ["validate", "plan"]`.
- Cyclic dependencies between units: they fail run-all. Split shared pieces into a lower unit.
- One giant unit per environment: slow plans and big blast radius. Split by lifecycle.
- `run-all apply -auto-approve` as the normal path: unreviewed changes across stacks. Plan, review, then apply.
- Committing the `.terragrunt-cache` directory: ignore it.

## Review
- [ ] Backend and provider generation live in one root file.
- [ ] Module sources are pinned.
- [ ] Dependencies are explicit; mocks are limited to plan and validate.
- [ ] Units are split by blast radius.
- [ ] CI runs plan on every unit and ignores cache dirs.
