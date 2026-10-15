---
name: upstash
title: Upstash Redis and QStash
area: cloud
tags: [upstash, redis, qstash, ratelimit, serverless, rest]
detect: [dep:@upstash/redis, dep:@upstash/ratelimit, dep:@upstash/qstash, dep:upstash-redis, dep:qstash]
related: [vercel, cloudflare-workers, netlify]
---
Upstash serverless Redis over REST plus QStash messaging: environment-based clients, bounded commands, rate limits with a real identifier, signature-checked webhooks.

## Verify
- `curl -s -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN" "$UPSTASH_REDIS_REST_URL/ping"`: the REST endpoint and token work.
- `curl -s -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN" "$UPSTASH_REDIS_REST_URL/dbsize"`: size sanity check after tests.
- `grep -rnE "(UPSTASH_REDIS_REST_TOKEN|QSTASH_TOKEN) *[=:] *['\"A-Za-z0-9]" . --exclude-dir=node_modules --exclude-dir=.git`: tokens appear only in env references and docs, never as literals.
- `curl -s -H "Authorization: Bearer $QSTASH_TOKEN" https://qstash.upstash.io/v2/dlq`: the QStash dead letter queue is empty or understood.

## Test first
Test the limiter and the webhook verifier against a test database and signed requests.
```ts
test("limiter blocks the 6th request per user in a window", async () => {
  const results = [];
  for (let i = 0; i < 6; i++) results.push(await limiter.limit("user:42"));
  expect(results.map(r => r.success)).toEqual([true, true, true, true, true, false]);
});
```

## Do
- Create clients with `Redis.fromEnv()` once at module scope, reading `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` from the environment.
- Use a separate database or key prefix per environment, and give tests their own database that you flush.
- Set a TTL on every cache or ephemeral key (`ex` or `EXPIRE`), and namespace keys (`app:env:entity:id`).
- Use `@upstash/ratelimit` with a stable identifier (user id, API key, or the trusted client IP) and a suitable algorithm (sliding window for smoothness, token bucket for bursts).
- Pipeline or `multi` related commands to cut round trips, since each REST call costs latency.
- Verify QStash webhooks with the `Receiver` and both signing keys (current and next) on the raw body before acting.
- Make QStash handlers idempotent and return non-2xx only when a retry is wanted. Configure retries and a failure callback or DLQ handling.
- Keep values small, and avoid commands that scan large key spaces (`KEYS`).

## Avoid
- Tokens in client-side bundles: the REST token is full access. Use server code, or a read-only token when you must expose reads.
- Rate limiting on a spoofable header: attackers rotate it. Use an authenticated id or the platform's trusted IP.
- `KEYS *` or unbounded `SCAN` loops in request paths: slow and costly. Index with sets or hashes.
- Keys without TTL: the database fills and bills grow. Always expire cache keys.
- Trusting QStash callbacks without signature verification: anyone can post to the URL. Verify with the `Receiver`.
- Verifying the signature after parsing JSON: the body bytes change. Verify the raw text first.
- Treating Redis as the system of record when persistence settings were not reviewed: confirm durability needs.

## Review
- [ ] Clients come from env, one per process, tokens never in code or bundles.
- [ ] Every ephemeral key has a TTL and a namespace.
- [ ] Rate limit identifiers are trustworthy and tested.
- [ ] QStash webhooks verify signatures on the raw body and are idempotent.
- [ ] Environments use separate databases or prefixes.
