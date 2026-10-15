---
name: chat-bots
title: Chat Bots
area: domains
tags: [bots, slack, discord, telegram, webhooks, slash-commands]
detect: [dep:@slack/bolt, dep:slack_bolt, dep:discord.js, dep:discord.py, dep:python-telegram-bot, dep:telegraf, dep:grammy, dep:botbuilder, dep:@slack/web-api, dep:slack-sdk]
related: [webhooks, auth-providers, cron-jobs, search]
---
Bots for Slack, Discord, Telegram and similar: verified inbound requests, fast acknowledgments, least-privilege scopes and idempotent handlers.

## Verify
- `curl -s -X POST localhost:3000/slack/events -d '{}' -w "%{http_code}\n"`: unsigned requests are rejected (expect 401 or 403).
- `grep -rnE "xox[bpa]-|[0-9]{8,}:[A-Za-z0-9_-]{30,}" . --exclude-dir=node_modules`: no bot tokens committed.
- `npx tsc --noEmit` or `pytest -q`: handlers compile and pass with a fake client.
- A tunnel (ngrok or cloudflared) to a dev workspace: the real round trip for slash commands and interactivity.

## Test first
Test handlers as functions with a fake platform client; test signature checks directly.
```python
import hmac, hashlib, time

def sign(secret: str, body: bytes, ts: str) -> str:
    base = f"v0:{ts}:{body.decode()}".encode()
    return "v0=" + hmac.new(secret.encode(), base, hashlib.sha256).hexdigest()

def test_rejects_stale_or_bad_signature(client):
    body, ts = b"command=/deploy", str(int(time.time()) - 3600)
    r = client.post("/slack/commands", data=body, headers={
        "X-Slack-Request-Timestamp": ts, "X-Slack-Signature": sign("secret", body, ts)})
    assert r.status_code == 401   # replayed
```

## Do
- Verify each inbound request: Slack signing secret plus timestamp window, Discord Ed25519 signature, Telegram `X-Telegram-Bot-Api-Secret-Token`.
- Acknowledge within the platform deadline (Slack 3 seconds, Discord interactions 3 seconds), then do the work in a job and post the result with the response URL or follow-up API.
- Make handlers idempotent: dedupe on event id, because platforms retry.
- Request the narrowest scopes and intents; add more only when a feature needs them.
- Keep tokens in a secret store; support rotation; per-workspace tokens through OAuth install flow, stored encrypted.
- Respect rate limits: honor `Retry-After` on 429 and queue outbound messages.
- Prefer slash commands, buttons and modals over parsing free-form text.
- Cap message length and chunk long output; escape user text (`<`, `>`, `&` in Slack mrkdwn).
- Log team, channel and event ids, never message bodies containing private data.

## Avoid
- Skipping signature verification "for now": anyone can trigger actions. Verify always.
- Doing slow work before replying: timeouts show errors to users and cause retries. Ack first.
- Requesting admin or all-message scopes by default: large blast radius and review friction. Use least privilege.
- Assuming a single workspace: tokens get mixed. Key state by team id.
- Mentioning `@channel` or `@everyone` from user-controlled text: spam and abuse. Strip or disallow.
- Polling APIs when events or Socket Mode exist: rate-limit trouble. Use events.
- Treating message text as trusted commands (including from an LLM): prompt injection and privilege escalation. Check the user's permission for every action.
- Storing conversation history indefinitely: privacy duty. Set retention.

## Review
- [ ] All inbound routes verify signatures and reject replays.
- [ ] Handlers ack fast, process async, and dedupe retries.
- [ ] Scopes are minimal; secrets are stored and rotatable.
- [ ] Outbound sends respect rate limits and escape user content.
- [ ] Destructive actions check the invoking user's authorization.
