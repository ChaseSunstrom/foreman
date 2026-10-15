---
name: webhooks
title: Webhooks
area: domains
tags: [webhooks, hmac, idempotency, retries, signatures, events]
detect: [dep:svix, dep:standardwebhooks, dep:hookdeck, dep:@octokit/webhooks, dep:smee-client]
related: [stripe, chat-bots, cron-jobs, email-sending]
---
Sending and receiving webhooks: verified signatures over raw bodies, fast acknowledgment, idempotent processing and retries.

## Verify
- `curl -s -X POST localhost:3000/hooks -d '{"id":"evt_1"}' -w "%{http_code}\n"`: an unsigned request is rejected (expect 401 or 400).
- `curl -s -X POST localhost:3000/hooks -H "X-Signature: sha256=$SIG" -d @payload.json`: a correctly signed replay is accepted, and sending it twice causes one effect.
- `openssl dgst -sha256 -hmac "$SECRET" payload.json`: computes the expected HMAC to compare.
- A tunnel (ngrok, cloudflared, smee) to receive real provider deliveries in development.

## Test first
Test signature, replay and duplicate handling.
```js
import crypto from 'node:crypto';
import request from 'supertest';
import { app, db } from './app';

const sign = (body, secret, ts) =>
  crypto.createHmac('sha256', secret).update(`${ts}.${body}`).digest('hex');

test('duplicate delivery is processed once, bad signature rejected', async () => {
  const body = JSON.stringify({ id: 'evt_1', type: 'order.paid' });
  const ts = Math.floor(Date.now() / 1000);
  const h = { 'x-timestamp': ts, 'x-signature': sign(body, 's3cret', ts) };
  await request(app).post('/hooks').set(h).send(body).expect(200);
  await request(app).post('/hooks').set(h).send(body).expect(200);
  expect(await db.countEffects('evt_1')).toBe(1);
  await request(app).post('/hooks').set({ ...h, 'x-signature': 'bad' }).send(body).expect(401);
});
```

## Do
- Receiving: compute the HMAC (SHA-256) over the raw body bytes with the shared secret, compare with a constant-time function (`crypto.timingSafeEqual`, `hmac.compare_digest`).
- Include and check a timestamp; reject older than about 5 minutes to stop replays.
- Persist the event with its id (unique constraint), return 2xx immediately, and process in a background worker.
- Treat events as notifications: fetch the current resource when order matters, since delivery can be duplicated or out of order.
- Sending: sign each request, include event id, type and timestamp, retry with exponential backoff and jitter for several days, then disable and notify the endpoint owner.
- Support secret rotation by accepting two signatures during the overlap.
- Give receivers a delivery log, manual redelivery and a test event.
- Sending: fetch only public destinations; resolve DNS and block private, loopback and metadata IP ranges, and cap response time and size.
- Use a standard (Standard Webhooks, Svix) instead of a custom scheme where possible.

## Avoid
- Verifying a re-serialized JSON body: the HMAC differs. Capture the raw body before parsing.
- Comparing signatures with `==`: timing leak. Use constant-time compare.
- Doing heavy work before responding: provider times out and retries, causing duplicates. Ack, then queue.
- Treating "200 OK" as processed when your queue insert failed: lost events. Return 5xx on persistence failure.
- Relying on delivery order or once-only delivery: neither is guaranteed. Dedupe and re-fetch.
- Sending webhooks to user-supplied URLs without SSRF protection: internal network access. Validate destinations.
- Putting secrets in the callback URL query string: leaks in logs. Use signatures.
- Unlimited retries without disabling: hammering dead endpoints. Back off and auto-disable.

## Review
- [ ] Signature and timestamp verified against the raw body in constant time.
- [ ] Event ids are deduped; handlers are idempotent.
- [ ] Response is fast; work runs asynchronously with failure handling.
- [ ] Retry, disable, rotation and redelivery paths exist and are tested.
- [ ] Outbound destinations are SSRF-protected.
