---
name: sentry
title: Sentry
area: infra
tags: [sentry, errors, monitoring, releases, sourcemaps, tracing]
detect: [dep:@sentry/node, dep:@sentry/browser, dep:@sentry/react, dep:@sentry/nextjs, dep:sentry-sdk, dep:sentry-go*, dep:sentry, file:sentry.properties, file:.sentryclirc]
related: [opentelemetry, grafana, prometheus]
---
Sentry: error and performance monitoring through an SDK with releases, source maps, scrubbing and sampling.

## Verify
- `sentry-cli info`: auth token and organization resolve.
- `sentry-cli releases list`: the CLI reaches the project and the release exists.
- `sentry-cli sourcemaps upload --release "$REL" ./dist`: source maps upload for the release (check the CLI version's subcommand with `--help`).
- `grep -rn 'Sentry.init\|sentry_sdk.init' src`: init exists exactly once and early.
- `SENTRY_DSN= <run tests>`: tests run with the SDK disabled by an empty DSN.

## Test first
Capture events with a test transport or `before_send` and assert on them, so no event leaves the process.
```python
import sentry_sdk

events = []
sentry_sdk.init(dsn="http://k@localhost/1", before_send=lambda e, h: events.append(e))

def test_failure_is_reported_without_pii():
    try: process({"email": "a@b.c"})
    except ValueError: sentry_sdk.capture_exception()
    assert events and "a@b.c" not in str(events[0])
```
Red first: fails until the exception is captured and the scrubber removes the email.

## Do
- Initialize the SDK once, before other code, with `dsn` from the environment, `environment`, and `release` (git SHA).
- Create the release in CI, upload source maps or debug symbols, then deploy, so events symbolicate.
- Set `tracesSampleRate` or `traces_sampler` deliberately below 1.0 in production.
- Scrub with `beforeSend` / `before_send`, and keep `send_default_pii` false unless needed.
- Add context with `setUser` with an opaque id, tags for low-cardinality facets, and `set_context` for details.
- Use `fingerprint` to group dynamic messages, and `ignoreErrors` or `before_send` filters for noise.
- Flush before exit in short-lived processes (`Sentry.flush`/`sentry_sdk.flush`, or `close`).
- Use `Sentry.captureException(err)` for handled errors, and keep the original error object so stack traces survive.

## Avoid
- A DSN committed in a public client bundle as a secret: the DSN is public by design, but auth tokens and `.sentryclirc` are not. Keep tokens in CI secrets.
- `tracesSampleRate: 1.0` in production: cost and overhead. Lower it.
- Capturing `new Error(String(err))` or logging strings: loses the stack. Capture the original exception.
- Minified frontends without uploaded source maps or a matching `release`: unreadable stacks. Upload per release and match the value in `init`.
- Sending emails, tokens and bodies in breadcrumbs and extras: personal data stored. Scrub in `beforeBreadcrumb` and `beforeSend`.
- High-cardinality tags (ids, timestamps): they are indexed. Put them in context.
- Initializing in each request handler: duplicate handlers and events. Init once.
- Serverless functions exiting without flush: events dropped. Flush before returning.

## Review
- [ ] Release, environment and source maps align with what is deployed.
- [ ] PII scrubbing and sampling rates are configured, with tokens kept in secrets.
- [ ] Handled and unhandled errors keep stack traces and grouping is sensible.
- [ ] Tests assert capture without sending to the network.
