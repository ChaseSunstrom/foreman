---
name: gcp-cloud-run
title: GCP Cloud Run
area: cloud
tags: [gcp, cloud-run, containers, serverless, revisions, deploy]
detect: [dep:@google-cloud/run, dep:google-cloud-run, file:service.yaml, file:cloudbuild.yaml, file:cloudbuild.yml]
related: [gcp-iam, gcp-pubsub, cloud-cost]
---
Cloud Run services and jobs: stateless containers that listen on `$PORT`, revisions, per-service identity, tuned concurrency.

## Verify
- `gcloud run services describe S --region R --format='value(status.url,status.latestReadyRevisionName)'`: the service is deployed and ready.
- `gcloud run services logs read S --region R --limit 50`: startup and request errors.
- `curl -fsS "$(gcloud run services describe S --region R --format='value(status.url)')/healthz"`: the live endpoint answers (add an identity token if private).
- `docker run --rm -e PORT=8080 -p 8080:8080 IMAGE`: the container starts and serves locally.

## Test first
Smoke-test the container contract: port and health.
```python
import os, urllib.request

def test_service_answers_on_port():
    base = os.environ["SERVICE_URL"]
    with urllib.request.urlopen(base + "/healthz", timeout=5) as r:
        assert r.status == 200
```
Run it against a local container first, then the deployed URL. Unit tests stay framework-level.

## Do
- Listen on `0.0.0.0:$PORT` (default 8080); do not hard-code the port.
- Give each service its own service account (`--service-account`), not the default compute one.
- Keep it stateless; store state in Cloud SQL, Firestore or Cloud Storage.
- Set `--concurrency`, `--min-instances` (for cold starts), `--max-instances` (to cap cost and protect databases), `--cpu` and `--memory` deliberately.
- Mount secrets from Secret Manager (`--set-secrets`), not `--set-env-vars`.
- Deploy private by default (no `allUsers` invoker); callers need `roles/run.invoker`.
- Do work only while serving a request unless CPU is always allocated.
- Handle SIGTERM; you have about 10 seconds to shut down.
- Use revisions and traffic splitting (`--no-traffic` then `update-traffic`) for staged rollouts.

## Avoid
- `--allow-unauthenticated` as a shortcut: use an invoker binding or IAP.
- Background threads after the response is sent with request-only CPU: they are throttled. Use Cloud Tasks or Jobs.
- Writing to local disk for persistence: the filesystem is in-memory and per instance.
- Unlimited scaling into a small database: set max instances and pool sizes.
- Deploying `:latest` and expecting a new revision: deploy a distinct tag or digest.
- Secrets baked into the image or env vars in the deploy command history.

## Review
- [ ] Dedicated service account, least-privilege roles.
- [ ] Not public unless intended and documented.
- [ ] Port, health and SIGTERM handled.
- [ ] Min and max instances and concurrency set.
- [ ] Secrets come from Secret Manager.
