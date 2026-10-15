---
name: aws-step-functions
title: AWS Step Functions
area: cloud
tags: [aws, step-functions, state-machine, workflow, asl, orchestration]
detect: [dep:@aws-sdk/client-sfn, file:*.asl.json, file:*.asl.yaml]
related: [aws-lambda, aws-eventbridge, aws-iam, aws-sam, aws-sqs-sns]
---
Step Functions state machines in ASL: retries and catches on every task, least-privilege role, idempotent steps, Standard vs Express chosen on purpose.

## Verify
- `aws stepfunctions validate-state-machine-definition --definition file://sm.asl.json`: ASL parses and states link up.
- `aws stepfunctions start-execution --state-machine-arn ARN --input '{"id":"t1"}'`: a smoke execution starts.
- `aws stepfunctions describe-execution --execution-arn ARN --query status`: it reached SUCCEEDED.
- `aws stepfunctions get-execution-history --execution-arn ARN --reverse-order --max-items 20`: the failing state and its error.

## Test first
Use Step Functions Local or TestState-style checks. Assert the failure path before the happy path.
```python
def test_charge_failure_routes_to_refund(sfn, arn):
    ex = sfn.start_execution(stateMachineArn=arn, input='{"amount":-1}')
    out = wait(sfn, ex["executionArn"])
    assert out["status"] == "FAILED"
    assert "RefundOrder" in visited_states(sfn, ex["executionArn"])
```

## Do
- Add `Retry` with `ErrorEquals`, `IntervalSeconds`, `MaxAttempts`, `BackoffRate` and `Catch` to every Task. Retry transient errors only.
- Set `TimeoutSeconds` on every Task so a hung worker cannot hold an execution open.
- Use Standard for long or auditable flows. Use Express for short high-volume flows with at-least-once semantics, so make steps idempotent.
- Use `Map` with `MaxConcurrency` for fan-out. For very large inputs read items from S3 with a distributed Map.
- Call AWS services with optimized integrations (`arn:aws:states:::dynamodb:putItem`) instead of a Lambda that wraps an SDK call.
- Pass small payloads. Store large data in S3 and pass the key. Trim with `InputPath`, `ResultSelector`, `OutputPath`.
- Give the role only the actions and resources the states call. Turn on logging for Express machines.
- Use `.waitForTaskToken` for human or external callbacks and set a heartbeat.

## Avoid
- A state with no `Catch`: any error fails the execution with no cleanup. Add a Catch that routes to a compensation state.
- Retrying non-idempotent tasks blindly: duplicates side effects. Use idempotency keys.
- Polling loops built from Wait and Choice for work a callback pattern covers: use `.sync` or a task token.
- Payloads near the 256 KB state limit: executions fail at runtime. Offload to S3.
- Execution names reused with Standard: duplicates are rejected within the retention window. Derive a name from a business id or omit it.
- `Resource: "*"` on the execution role: scope to the function and table ARNs.

## Review
- [ ] Every Task has Retry, Catch and a timeout.
- [ ] Steps are idempotent or carry an idempotency key.
- [ ] Standard vs Express choice is stated in the definition comments or README.
- [ ] Role policy lists exact resources.
- [ ] A failure-path test exists for each Catch.
