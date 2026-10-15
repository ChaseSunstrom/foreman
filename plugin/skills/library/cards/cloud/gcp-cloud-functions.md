---
name: gcp-cloud-functions
title: GCP Cloud Functions
area: cloud
tags: [gcp, cloud-functions, serverless, eventarc, functions-framework]
detect: [dep:@google-cloud/functions-framework, dep:functions-framework, dep:firebase-functions]
related: [gcp-cloud-run, gcp-pubsub, gcp-iam, gcp-firestore]
---
Cloud Functions (2nd gen, on Cloud Run): a dedicated service account, secrets from Secret Manager, idempotent event handlers, bounded concurrency and timeouts.

## Verify
- `gcloud functions describe F --gen2 --region R --format='value(serviceConfig.serviceAccountEmail,serviceConfig.timeoutSeconds,serviceConfig.maxInstanceCount)'`: identity, timeout and instance cap.
- `gcloud functions logs read F --gen2 --region R --limit 50`: recent logs and errors.
- `gcloud functions get-iam-policy F --gen2 --region R`: who can invoke it (no `allUsers` unless intended).
- `functions-framework --target=handler --port=8080` then `curl -s localhost:8080`: runs locally with the same entry point.

## Test first
Call the handler through the Functions Framework test client and assert the unauthenticated and duplicate-event cases.
```python
def test_duplicate_event_is_a_noop(client, store):
    ev = {"id": "evt-1", "data": {"v": 1}}
    client.post("/", json=ev); client.post("/", json=ev)
    assert store.count("evt-1") == 1
```

## Do
- Deploy 2nd gen and set `--service-account` to a function-specific account with only the roles it needs. The default compute account is broad.
- Mount secrets from Secret Manager (`--set-secrets`) instead of plain env vars.
- Make event handlers idempotent by deduplicating on the event id, since delivery is at least once.
- Set `--timeout`, `--memory`, `--max-instances` and, if cold starts matter, `--min-instances`.
- Initialize clients at module scope to reuse them across invocations, and keep the work per request in the handler.
- Require authentication (`--no-allow-unauthenticated`) and let callers present an identity token. Make public access an explicit choice.
- Return 2xx only after the work is durable. For event functions, an error response triggers retry when retries are enabled, so enable them only for idempotent work.
- Log structured JSON with `severity` so Cloud Logging reads levels.

## Avoid
- Gen 1 for new work: it lacks concurrency and longer timeouts. Use 2nd gen.
- `--allow-unauthenticated` as a shortcut to make it work: the endpoint becomes public. Grant `roles/run.invoker` to the caller identity.
- Secrets baked into `--set-env-vars`: they show in the console. Use Secret Manager.
- Retries on non-idempotent handlers: duplicates charge twice. Dedupe by event id or disable retries.
- Background work after returning: the instance may be throttled once the response is sent. Finish before responding.
- Unbounded scale into a database: set `--max-instances` to protect downstream limits.
- Heavy global initialization that fails: the instance crashes on start. Fail with a clear log and keep init cheap.

## Review
- [ ] Dedicated service account with scoped roles.
- [ ] Auth required, invoker bindings explicit.
- [ ] Secrets from Secret Manager.
- [ ] Idempotency tested for event triggers.
- [ ] Timeout, memory and max instances set deliberately.
