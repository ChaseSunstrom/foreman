---
name: pulumi
title: Pulumi
area: infra
tags: [pulumi, iac, stacks, typescript, python, state]
detect: [file:Pulumi.yaml, file:Pulumi.*.yaml, dep:@pulumi/pulumi, dep:pulumi]
related: [terraform, opentofu, kubernetes, vault]
---
Pulumi: infrastructure as real code with stacks, typed Outputs, encrypted config and previewed updates.

## Verify
- `pulumi preview --stack dev --diff`: the planned changes without applying.
- `pulumi preview --expect-no-changes`: the stack has no drift after a refactor.
- `pulumi config`: config keys for the selected stack, secrets shown masked.
- `pulumi stack output --json`: exported outputs match what consumers expect.
- `npm test` or `pytest -q`: unit tests with mocks, no cloud calls.

## Test first
Unit-test the program with `pulumi.runtime.set_mocks`, so no provider is contacted.
```python
import pulumi

class Mocks(pulumi.runtime.Mocks):
    def new_resource(self, args):
        return [args.name + "_id", args.inputs]
    def call(self, args):
        return {}

pulumi.runtime.set_mocks(Mocks())

@pulumi.runtime.test
def test_bucket_not_public():
    import infra
    def check(acl): assert acl != "public-read"
    return infra.bucket.acl.apply(check)
```

## Do
- Create one stack per environment (`dev`, `prod`) with `Pulumi.<stack>.yaml` for config, and keep project code shared.
- Store secrets with `pulumi config set --secret key`, and pick a secrets provider (passphrase or KMS) for the backend.
- Treat resource values as `Output[T]`: transform with `.apply`, `pulumi.Output.all`, or `pulumi.interpolate`.
- Give resources explicit logical names that stay stable, and use `aliases` when renaming or re-parenting.
- Use `ComponentResource` for reusable groups, and set `parent=self` on children.
- Use `protect=True` on stateful resources and `import` an existing resource instead of recreating.
- Pin provider package versions in `package.json` or `requirements.txt` and commit the lockfile.
- Use a remote backend (Pulumi Cloud or object storage), never local files, for shared stacks.

## Avoid
- Using an `Output` as a plain string (`f"{bucket.id}"`, `if output:`): it is not resolved at that time. Use `.apply` or `interpolate`.
- Creating resources inside `.apply`: they do not show in preview. Create resources at top level.
- Renaming a resource without `aliases`: it deletes and recreates. Add the old URN alias.
- `pulumi up --yes` on an unreviewed preview: a destructive diff goes through. Preview first and review.
- Plaintext secrets in config (`pulumi config set key value`): they sit in stack YAML. Use `--secret`.
- Random names via `Math.random` or `uuid` in code: every run changes. Use `pulumi_random` resources.
- `pulumi refresh` followed by `up` blindly: it can import unwanted drift. Review the refresh diff.

## Review
- [ ] Preview shows no unintended replace or delete, and renames use `aliases`.
- [ ] Secrets are marked and Outputs are not logged in clear text.
- [ ] Stateful resources are protected and stacks use a shared backend.
- [ ] Unit tests run with mocks and no credentials.
