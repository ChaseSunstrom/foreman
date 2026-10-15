---
name: azure-bicep
title: Azure Bicep
area: cloud
tags: [azure, bicep, iac, arm, deployment, what-if]
detect: [ext:.bicep, file:bicepconfig.json, file:*.bicepparam]
related: [azure-app-service, azure-functions, cloud-cost]
---
Azure Bicep templates: typed parameters, modules, what-if before deploy, role assignments and identities declared in code.

## Verify
- `az bicep build --file main.bicep --stdout >/dev/null`: compiles with no errors.
- `az bicep lint --file main.bicep`: linter rules (unused parameters, hard-coded locations, secure params).
- `az deployment group what-if -g RG --template-file main.bicep --parameters main.bicepparam`: the exact changes it would make.
- `az deployment group validate -g RG --template-file main.bicep --parameters main.bicepparam`: the service accepts it.

## Test first
Fail on lint and on the what-if output.
```python
import subprocess

def test_what_if_has_no_deletes():
    out = subprocess.run(
        ["az", "deployment", "group", "what-if", "-g", "rg-test",
         "--template-file", "main.bicep", "--no-pretty-print"],
        capture_output=True, text=True, check=True).stdout
    assert '"changeType": "Delete"' not in out
```
For policy, run `bicep lint` in CI and fail on warnings.

## Do
- Add `@description`, `@allowed`, `@minLength` and `@secure()` decorators to parameters.
- Use `.bicepparam` files per environment with `using './main.bicep'`.
- Split into modules (`module x 'modules/x.bicep' = { ... }`) with typed inputs and outputs.
- Use symbolic references (`storage.id`, `storage.properties.primaryEndpoints`) so dependencies are implicit; avoid `dependsOn` unless needed.
- Use `existing` to reference resources you do not own.
- Use `uniqueString(resourceGroup().id)` for globally unique names.
- Assign roles with `Microsoft.Authorization/roleAssignments` and managed identities, not keys.
- Pin API versions deliberately, and use the Bicep linter's version check.
- Use `--mode Incremental` (default) unless you intend to delete unlisted resources.

## Avoid
- Secrets as plain parameters or outputs: use `@secure()`, Key Vault references and `getSecret()` in module params.
- `--mode Complete` on a shared resource group: it deletes everything not in the template.
- Hard-coded `location` strings: take `param location string = resourceGroup().location`.
- Role assignment `name` that is not a deterministic `guid(...)`: redeploys fail with conflicts.
- Skipping what-if: renames create-then-delete.
- Outputs containing secrets or connection strings.
- Mixing portal edits with Bicep: the next deploy overwrites them.

## Review
- [ ] Lint clean; what-if reviewed with no unexpected delete.
- [ ] Secrets use `@secure()` and Key Vault.
- [ ] Role assignments use `guid()` names and minimal built-in roles.
- [ ] Names and locations are parameterised.
- [ ] Modules have typed inputs and outputs.
