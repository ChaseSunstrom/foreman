---
name: aws-sam
title: AWS SAM
area: cloud
tags: [aws, sam, serverless, lambda, cloudformation, local]
detect: [file:samconfig.toml, file:template.yaml, file:template.yml, file:samconfig.yaml]
related: [aws-lambda, aws-cloudformation, aws-cdk, localstack, aws-iam]
---
AWS SAM apps: a `Transform: AWS::Serverless-2016-10-31` template, local invoke, guided deploy through `samconfig.toml`.

## Verify
- `sam validate --lint`: the template is valid and passes cfn-lint rules.
- `sam build`: functions build, dependencies resolve.
- `sam local invoke FnName --event events/e.json`: the handler works locally (needs Docker).
- `sam deploy --no-confirm-changeset --no-fail-on-empty-changeset`: non-interactive deploy using `samconfig.toml`.

## Test first
Unit-test the handler directly; use the event JSON `sam local generate-event` produces.
```python
import json
from hello_world.app import lambda_handler

def test_missing_id_is_400():
    event = {"pathParameters": None}
    res = lambda_handler(event, None)
    assert res["statusCode"] == 400
```
Handlers sit in a directory per function with its own `requirements.txt` or `package.json`; tests in `tests/unit`. Add one integration test against the deployed stack, found with `sam list endpoints --output json`.

## Do
- Put shared settings in `Globals` (Runtime, Timeout, MemorySize, Environment).
- Use SAM policy templates (`S3ReadPolicy`, `DynamoDBCrudPolicy`, `SQSPollerPolicy`) instead of inline wildcards.
- Define events inline (`Type: Api`, `HttpApi`, `SQS`, `Schedule`) so SAM creates the permissions.
- Keep per-environment values in `samconfig.toml` sections (`[default.deploy.parameters]`, `[prod.deploy.parameters]`) and `Parameters`.
- Use `sam sync --watch` for dev stacks only.
- Use `Metadata: BuildMethod` (`esbuild`, `makefile`) for compiled or bundled functions.
- Output ARNs and URLs in `Outputs` and `Export` only when another stack needs them.

## Avoid
- `sam deploy --guided` in CI: it prompts. Commit `samconfig.toml` and pass flags.
- Running `sam local` without Docker running: it fails with a connection error.
- Deploying from the source directory instead of `.aws-sam/build`: `sam deploy` uses the build output, so rebuild after every code change.
- `CodeUri: .` pointing at the repo root: it bundles everything. Point at the function directory.
- Hand-written `AWS::Lambda::Permission` and role for events SAM already wires.
- `sam sync` against production: it skips changeset review.
- Editing `.aws-sam/` files: they are regenerated.

## Review
- [ ] `sam validate --lint` clean.
- [ ] Policies use templates or specific ARNs.
- [ ] Timeout and memory set, with a DLQ for async functions.
- [ ] `samconfig.toml` has no secrets and no guided-only settings.
- [ ] Event source mapping uses partial batch failure when batching.
