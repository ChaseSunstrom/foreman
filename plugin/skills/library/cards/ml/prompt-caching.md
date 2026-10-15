---
name: prompt-caching
title: Claude prompt caching
area: ml
tags: [claude, llm, caching, cost, latency, cache-control]
detect: []
related: [anthropic-sdk, tool-use, rag, llm-evals]
---
Prompt caching on the Claude API: mark stable prefixes with `cache_control` and verify hits through usage fields.

## Verify
- `pytest -q`: a request-shape test confirms the stable prefix is first and carries `cache_control`.
- `python -c "import json,sys; print(json.dumps(json.load(open('usage.json')), indent=1))"`: inspect a logged `usage` object for `cache_creation_input_tokens` and `cache_read_input_tokens`.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Assert the request layout, then assert on usage from a real or recorded response: call twice, the second read count is above zero.
```python
from mypkg.prompt import build_request

def test_stable_prefix_is_cached_and_first():
    r = build_request(user_text="q1", docs="BIG DOC")
    sys_block = r["system"][-1]
    assert sys_block["cache_control"] == {"type": "ephemeral"}
    assert "q1" not in str(r["system"])      # volatile text stays out of the prefix
    r2 = build_request(user_text="q2", docs="BIG DOC")
    assert r["system"] == r2["system"]       # byte-identical prefix
```

## Do
- Add `"cache_control": {"type": "ephemeral"}` to the last block of the stable prefix. Use a list of blocks for `system` so you can attach it.
- Order content: tools, then system, then long documents or examples, then the volatile user turn.
- Keep the prefix byte-identical between calls: stable tool order, no timestamps, ids or random text in it.
- Respect the minimum cacheable prefix length for the model. Shorter prefixes are silently not cached.
- Use up to four breakpoints, for example one after tools, one after system, one at the end of conversation history in multi-turn chats.
- Log `usage.cache_creation_input_tokens` and `usage.cache_read_input_tokens` on every call and alert when reads stay zero.
- Send follow-ups within the cache lifetime. Consider the longer cache TTL option only when gaps exceed the default.

## Avoid
- Putting the cache marker before volatile text: any change before the breakpoint invalidates the cache. Move volatile content after it.
- Interpolating the current time or a request id into the system prompt: a miss every call. Pass it in the user turn.
- Reordering or regenerating tool definitions between requests: invalidates the prefix. Sort them once.
- Assuming it works without checking usage: below-minimum prefixes are never cached. Measure.
- Changing `model` or thinking settings mid-conversation and expecting hits: they reset the cache.
- Caching a prefix used once: the write costs more than a normal read. Cache only reused prefixes.
- Marking every block: wasted breakpoints. Mark the stable boundaries.

## Review
- [ ] The cached prefix is identical across requests, with volatile data after it.
- [ ] Breakpoints sit at the end of tools, system and history as intended.
- [ ] Usage fields are logged and a hit is observed in a second call.
- [ ] Prefix meets the minimum token length.
- [ ] No cache marker on one-off prompts.
