---
name: server-sent-events
title: Server-Sent Events
area: design
tags: [sse, eventsource, streaming, http, realtime, reconnect]
detect: [dep:sse-starlette, dep:eventsource, dep:eventsource-parser, dep:better-sse, dep:@microsoft/fetch-event-source]
related: [websockets, event-driven, retries-backoff, caching]
---
One-way HTTP event streams with event IDs, resumable reconnects, heartbeats and proxy-safe headers.

## Verify
- `curl -N -H 'Accept: text/event-stream' localhost:8080/events`: frames arrive incrementally, not at the end.
- `curl -si -N -H 'Last-Event-ID: 41' localhost:8080/events`: the server resumes after ID 41, and the response has `Content-Type: text/event-stream`.
- `curl -sI localhost:8080/events`: headers include `Cache-Control: no-cache` and no compression buffering.

## Test first
Consume the stream, drop it, reconnect with `Last-Event-ID` and assert no gap and no duplicate.
```python
def test_resumes_after_last_event_id(client, bus):
    bus.publish_many(["a", "b", "c"])  # ids 1,2,3
    with client.stream("GET", "/events", headers={"Last-Event-ID": "1"}) as r:
        lines = [l for l in r.iter_lines() if l.startswith("data:")][:2]
    assert lines == ["data: b", "data: c"]
```

## Do
- Emit `id:`, `event:` and `data:` fields, each frame ending with a blank line. Split multi-line payloads into several `data:` lines.
- Keep an ordered, replayable event log so `Last-Event-ID` can resume. Say how long it is retained.
- Send a comment heartbeat (`: ping`) every 15-30 s so proxies keep the connection open.
- Set `retry: <ms>` to steer client reconnect timing.
- Send `Cache-Control: no-cache` and `X-Accel-Buffering: no` for nginx. Disable response compression and buffering on the route.
- Authenticate with cookies or an `Authorization` header (via a fetch-based client). The native `EventSource` can't set headers.
- Stop work on client disconnect: watch the request's close or abort signal.

## Avoid
- Native `EventSource` with a bearer token in the query string: it lands in logs. Use cookies, or a fetch-based client with headers.
- No heartbeat: idle proxies and load balancers cut the stream silently. Send periodic comments.
- Gzip or a buffering proxy on the stream: the client sees nothing until the buffer flushes. Disable them for this route.
- Event IDs that are not monotonic or not stable across instances: resume skips or repeats events. Use a sequence from the log.
- Using SSE for client-to-server messages: send normal POSTs.
- Over HTTP/1.1, many tabs open one connection each (about 6 per origin limit): serve over HTTP/2.
- Leaking subscribers when the client leaves: release listeners on disconnect.

## Review
- [ ] Frames are well-formed and carry monotonic IDs.
- [ ] Resume with `Last-Event-ID` is tested and the retention window is documented.
- [ ] Heartbeat, no-cache and no-buffering are set, and compression is off for the route.
- [ ] Auth does not put long-lived secrets in URLs.
- [ ] Subscribers are cleaned up on disconnect.
