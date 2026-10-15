---
name: llm-streaming
title: LLM streaming
area: ml
tags: [llm, streaming, sse, async, tool-use, latency]
detect: []
related: [anthropic-sdk, tool-use, llm-cost-latency, fastapi]
---
Stream model output token by token over the messages API and forward it to clients without losing tool calls, usage or errors.

## Verify
- `pytest -q tests/test_stream.py`: event handling, tool-call assembly and mid-stream failure paths pass on a fake event stream.
- `curl -N -s localhost:8000/chat -d '{"q":"hi"}'`: the endpoint emits chunks incrementally, not one buffered body.
- `pytest -q -k disconnect`: a client disconnect cancels the upstream request.

## Test first
Feed a scripted event list and assert the assembled result.
```python
import pytest
from app.stream import collect

@pytest.mark.anyio
async def test_partial_tool_json_is_joined():
    events = [
        {"type": "content_block_start", "index": 0, "content_block": {"type": "tool_use", "id": "t1", "name": "f", "input": {}}},
        {"type": "content_block_delta", "index": 0, "delta": {"type": "input_json_delta", "partial_json": "{\"a\":"}},
        {"type": "content_block_delta", "index": 0, "delta": {"type": "input_json_delta", "partial_json": "1}"}},
        {"type": "content_block_stop", "index": 0},
    ]
    assert (await collect(events)).tool_calls[0].input == {"a": 1}
```

## Do
- Use the SDK stream helper (`client.messages.stream(...)`) and its text and final-message accessors rather than parsing SSE by hand.
- Handle the event sequence: `message_start`, `content_block_start`, `content_block_delta` (`text_delta`, `input_json_delta`), `content_block_stop`, `message_delta` (stop reason, usage), `message_stop`.
- Concatenate `partial_json` per block index and parse only at `content_block_stop`.
- Read final usage from the final message to meter cost.
- Forward to browsers as SSE (`text/event-stream`) with a keepalive comment line and `X-Accel-Buffering: no` behind proxies.
- Cancel upstream when the client disconnects; wrap the stream in a context manager so the connection closes.
- Send errors as an explicit event; an `error` event can arrive after a 200 status.

## Avoid
- `json.loads` on each `input_json_delta`: fragments are invalid JSON. Join, then parse at block stop.
- Buffering the response in a proxy or middleware (gzip, no `no-cache`): the user sees nothing until the end. Disable buffering.
- Assuming one content block: text and tool blocks interleave; key everything by `index`.
- Ignoring `stop_reason`: `max_tokens` and `tool_use` need different handling.
- Retrying a half-streamed answer by appending: restart cleanly or tell the client to discard.
- Streaming without a timeout: set read and total timeouts.

## Review
- [ ] Tool input assembled per index and parsed at block stop.
- [ ] Disconnect and exceptions close the upstream stream.
- [ ] Usage and stop reason are recorded.
- [ ] Proxies and compression do not buffer.
- [ ] Mid-stream error is surfaced to the client.
