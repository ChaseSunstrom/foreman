---
name: azure-functions
title: Azure Functions
area: cloud
tags: [azure, functions, serverless, triggers, bindings, func]
detect: [dep:azure-functions, dep:@azure/functions, dep:Microsoft.Azure.Functions.Worker, dep:Microsoft.NET.Sdk.Functions, file:host.json, file:local.settings.json, file:function.json]
related: [azure-app-service, azure-bicep, aws-lambda]
---
Azure Functions apps: triggers and bindings, `host.json` tuning, managed identity, local run with Core Tools.

## Verify
- `func start`: the host starts locally and lists every function (needs Core Tools and Azurite for storage triggers).
- `az functionapp function list -g RG -n APP -o table`: deployed functions are registered.
- `az functionapp log tail -g RG -n APP`: live logs from the deployed app (or use Application Insights).

## Test first
Test the function body directly, with the trigger input faked.
```python
import azure.functions as func
from function_app import add_item

def test_add_item_bad_json_is_400():
    req = func.HttpRequest("POST", "/api/items", body=b"nope", headers={})
    res = add_item(req)
    assert res.status_code == 400
```
Tests live in `tests/`. Use the same model (v2 decorators in Python, isolated worker in .NET) the app uses.

## Do
- Use the current programming model: Python v2 (`@app.route` in `function_app.py`), Node v4 (`app.http`), .NET isolated worker.
- Keep `local.settings.json` out of git; mirror values into app settings in Azure.
- Use managed identity and identity-based connections (`AzureWebJobsStorage__accountName`) over connection strings.
- Reference secrets with Key Vault references (`@Microsoft.KeyVault(SecretUri=...)`).
- Reuse clients (HTTP, SDK) across invocations through module scope or DI.
- Tune `host.json`: queue `batchSize`, `maxConcurrentRequests`, retry policy, `functionTimeout`.
- Use Durable Functions for long workflows, fan-out and human approval; keep orchestrators deterministic.
- Choose `authLevel` deliberately; prefer Entra auth at the app over function keys.

## Avoid
- `authLevel: anonymous` on a function that mutates data without other auth.
- Non-deterministic code in a Durable orchestrator (`datetime.now`, random, I/O): use the context APIs and activities.
- Python v1 `function.json` model mixed with v2 decorators in one app: pick one.
- Long work on the Consumption plan HTTP trigger: it hits the 230 s HTTP limit. Return 202 and queue it.
- Committing `local.settings.json` with real keys.
- Creating a new `HttpClient` per call in .NET: socket exhaustion. Inject `IHttpClientFactory`.
- Forgetting `FUNCTIONS_WORKER_RUNTIME` in app settings.

## Review
- [ ] One programming model, current trigger decorators.
- [ ] Storage and secrets use managed identity or Key Vault.
- [ ] Auth level and CORS are deliberate.
- [ ] Orchestrators are deterministic.
- [ ] `host.json` limits match the downstream capacity.
