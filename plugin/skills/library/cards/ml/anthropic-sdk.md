---
name: anthropic-sdk
title: Anthropic SDK (Claude API)
area: ml
tags: [python, typescript, claude, llm, messages-api, streaming]
detect: [dep:anthropic, dep:@anthropic-ai/sdk]
related: [tool-use, prompt-caching, llm-evals, rag]
---
Claude API apps with the anthropic SDK: the Messages API, system prompts, streaming, token limits, retries and error handling.

## Verify
- `python -c "import anthropic; print(anthropic.__version__)"`: the SDK is installed (use `npm ls @anthropic-ai/sdk` for TypeScript).
- `pytest -q`: tests pass with the client mocked, with no network and no key.
- `grep -rnE "sk-ant-[A-Za-z0-9_-]{10,}" . --include=*.py --include=*.ts --include=*.env*`: no key is committed (should print nothing).
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Inject the client so tests never call the API. Assert the request you build and how you handle the response.
```python
from types import SimpleNamespace as NS
from mypkg.summarize import summarize

def test_summarize_sets_limits_and_returns_text():
    calls = []
    class Fake:
        class messages:
            @staticmethod
            def create(**kw):
                calls.append(kw)
                return NS(content=[NS(type="text", text="ok")], stop_reason="end_turn")
    assert summarize(Fake, "long text") == "ok"
    assert calls[0]["max_tokens"] > 0 and calls[0]["system"]
```

## Do
- Create one `anthropic.Anthropic()` (or `AsyncAnthropic`) client at startup. It reads `ANTHROPIC_API_KEY` from the environment.
- Call `client.messages.create(model=..., max_tokens=..., system=..., messages=[...])`. `max_tokens` is required. Read the model id from config, not literals scattered in code.
- Put instructions in the top-level `system` parameter. Messages hold only `user` and `assistant` turns, and they alternate.
- Read output from `response.content` blocks: filter `type == "text"` rather than assuming `content[0]`. Check `stop_reason` for `max_tokens` truncation and `tool_use`.
- Stream long outputs with `client.messages.stream(...)` and iterate `text_stream`.
- Rely on the SDK's built-in retries (`max_retries`) and set a `timeout`. Catch `anthropic.RateLimitError`, `APIStatusError` and `APIConnectionError`.
- Log `response.usage` (input, output, cache tokens) for cost tracking.

## Avoid
- The legacy text-completions endpoint and the `Human:` and `Assistant:` prompt format: use the Messages API.
- Putting the system prompt as a `system` role message in `messages`: it is rejected. Use the `system` parameter.
- Assuming `response.content[0].text` always exists: tool-use responses start with other blocks. Filter by type.
- Omitting `max_tokens` or setting it tiny and ignoring `stop_reason == "max_tokens"`: silent truncation. Check and continue or raise.
- Hard-coding a model id throughout the code: breaks on retirement. Centralize it in config.
- Parsing JSON out of free text with regexes: brittle. Use tool use with an input schema for structured output.
- Calling the blocking client inside an async server: stalls the loop. Use `AsyncAnthropic`.
- Committing keys or logging full prompts that contain user data.

## Review
- [ ] One shared client, key from the environment, timeout and retries set.
- [ ] `max_tokens` is set and truncation is handled.
- [ ] Output handling filters content blocks by type.
- [ ] Model id lives in one config value.
- [ ] Tests mock the client and cover an error path.
