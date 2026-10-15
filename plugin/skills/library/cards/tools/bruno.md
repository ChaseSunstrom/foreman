---
name: bruno
title: Bruno
area: tools
tags: [api, http, testing, collections, git-friendly]
detect: [file:bruno.json]
related: [curl-httpie, jq, github-cli]
---
Bruno: an API client that stores requests as plain-text .bru files in the repo, so collections are reviewed and versioned like code.

## Verify
- `bru run --env local`: run every request in the collection against the `local` environment, with its tests and assertions (CLI package `@usebruno/cli`).
- `bru run path/to/folder --env local`: run only one folder or request.
- `bru run --env local --output results.json --format json`: machine-readable results for CI.
- `bru run --env local --env-var token=$TOKEN`: pass a secret at run time rather than storing it.
- `git diff --stat -- '*.bru'`: collection changes appear as small text diffs.

## Test first
Write the request with an assertion that fails against the current behavior.
```
meta {
  name: create item rejects blank name
  type: http
  seq: 3
}

post {
  url: {{baseUrl}}/items
  body: json
}

body:json {
  { "name": "" }
}

assert {
  res.status: eq 422
}
```
Run `bru run --env local` and see this request fail before the fix.

## Do
- Keep a collection folder with `bruno.json` at its root, committed with the code it exercises.
- Put per-environment values in `environments/*.bru` and reference them as `{{baseUrl}}`.
- Mark secrets as secret variables in the environment, and supply real values locally or from CI env.
- Use `assert` blocks for status and shape, and `tests` blocks with scripts for deeper checks.
- Order dependent requests with `seq`, and pass data using `bru.setVar` in post-response scripts.
- Run the collection in CI against an ephemeral service, with `bru run` exit code gating the job.

## Avoid
- Committing real tokens in environment files: use secret variables and CI env vars. Rotate any that leaked.
- Relying on request order without `seq`: runs differ between machines. Set explicit sequence numbers.
- Assertions that only check status: a 200 with wrong body passes. Assert key fields too.
- Pointing collections at shared staging with destructive requests: use a local or ephemeral environment.
- Editing .bru files by hand with syntax slips: open and run them in the app or CLI right after.
- Hard-coded IDs from your own database: create the data in an earlier request and capture the id.

## Review
- [ ] `bru run` passes locally and in CI with the intended environment.
- [ ] No secrets in committed environment files.
- [ ] Requests assert body content, not only status codes.
- [ ] Destructive requests cannot hit shared systems.
