---
name: aws-lambda
title: AWS Lambda
area: cloud
tags: [aws, lambda, serverless, functions, events, cold-start]
detect: [dep:aws-lambda-powertools, dep:aws_lambda_powertools, dep:@types/aws-lambda, dep:aws-lambda, dep:@aws-sdk/client-lambda, dep:aws-lambda-go]
related: [aws-sam, aws-cdk, aws-iam, aws-sqs-sns, serverless-framework]
---
AWS Lambda functions: small handlers, init-time clients, idempotent event processing, tuned memory and timeout.

## Verify
- `sam local invoke Fn --event events/e.json`: the handler runs against a sample event (needs SAM and Docker).
- `aws lambda invoke --function-name NAME --payload fileb://e.json out.json && cat out.json`: the deployed function responds.
- `aws logs tail /aws/lambda/NAME --since 10m`: real errors, REPORT lines with duration and max memory.
- `aws lambda get-function-configuration --function-name NAME`: runtime, timeout, memory and env as deployed.

## Test first
Call the handler directly with a recorded event; no AWS needed.
```python
import json
from app.handler import handler

def test_rejects_bad_body():
    event = {"httpMethod": "POST", "body": "not json"}
    res = handler(event, None)
    assert res["statusCode"] == 400
    assert "error" in json.loads(res["body"])
```
Keep sample events in `events/`. Stub clients with `botocore.stub.Stubber` or `moto`.

## Do
- Create SDK clients and read config outside the handler so warm invocations reuse them.
- Keep handlers thin: parse the event, call plain functions, shape the response.
- Make handlers idempotent; every event source delivers at least once.
- Set timeout below the caller's (API Gateway 29 s, SQS visibility timeout at least 6x the function timeout).
- Report partial batch failures (`batchItemFailures`, with `ReportBatchItemFailures` on the mapping) for SQS and streams.
- Tune memory with measurements; CPU scales with it.
- Set a DLQ or on-failure destination for async invokes. Use structured JSON logs.
- Use layers or bundling for dependencies; prefer arm64 when dependencies allow.

## Avoid
- Writing to the filesystem outside `/tmp`: the rest is read-only. Cap use of `/tmp`.
- Recursive trigger loops (function writes to the bucket that triggers it): use prefix filters or separate buckets.
- Returning a bare dict from an API Gateway proxy handler: return `statusCode`, `headers` and a string `body`.
- Unbounded concurrency hammering a database: set reserved concurrency or use RDS Proxy.
- Secrets in plain env vars: read from Secrets Manager or SSM, cached at init.
- `async` handler that never awaits the promise or leaves work running after return: the runtime freezes it.

## Review
- [ ] Clients and config are initialised outside the handler.
- [ ] Handler is idempotent and bounded in time.
- [ ] Role grants only the actions the function calls.
- [ ] Failures route to a DLQ or destination.
- [ ] Logs carry a request id and no secrets.
