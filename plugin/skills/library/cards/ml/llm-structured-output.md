---
name: llm-structured-output
title: LLM structured output
area: ml
tags: [llm, json, schema, tool-use, pydantic, extraction]
detect: [dep:anthropic, dep:instructor]
related: [tool-use, anthropic-sdk, llm-evals, llm-guardrails, prompt-engineering]
---
Get schema-valid JSON from an LLM by forcing a tool call with a JSON Schema, then validating and retrying on failure.

## Verify
- `pytest -q tests/test_extract.py`: schema validation, retry and refusal paths pass against recorded responses.
- `python -c "from app.schemas import Out; import json; json.dumps(Out.model_json_schema())"`: the schema serialises and is what the model is sent.
- `pytest -q -m live --maxfail=1`: a small live suite (opt-in marker) that hits the real API on a fixed example set.

## Test first
Replay saved responses; assert bad output is rejected, not coerced.
```python
import pytest
from pydantic import ValidationError
from app.extract import parse_tool_input, Invoice

def test_missing_total_is_rejected():
    raw = {"vendor": "ACME", "lines": []}
    with pytest.raises(ValidationError):
        parse_tool_input(raw, Invoice)
```

## Do
- Define one tool whose `input_schema` is the target schema, and set `tool_choice` to `{"type": "tool", "name": "..."}` so the reply is always that tool's `input`.
- Generate the schema from Pydantic (`model_json_schema()`) so code and prompt share one source of truth.
- Put field semantics in schema `description` strings; use `enum` for closed sets and `null` unions for unknown values instead of letting the model invent.
- Validate every response with the model class. On `ValidationError`, retry once with the error text appended as a user turn, then fail loudly.
- Check `stop_reason`: `max_tokens` means truncated JSON; raise `max_tokens` or shrink the schema.
- Cache the static prefix (schema, instructions) with `cache_control` when many documents share it.
- Keep temperature low for extraction and log the raw response next to the parsed result.

## Avoid
- Asking for "JSON only" in prose then `json.loads` the text: fences, prose and trailing commas break it. Use a forced tool call.
- Deep recursive or huge schemas: accuracy drops and truncation rises. Split into stages.
- Silently coercing bad output (defaults, `try/except: pass`): hides model drift. Reject and count failures.
- Required fields for data the source may lack: the model fabricates values. Make them optional or nullable.
- Unbounded retry loops: cap attempts and tokens; each retry costs full input.
- Testing only on happy-path documents: add empty, adversarial and over-long inputs.

## Review
- [ ] Schema comes from one typed model and descriptions state meaning and units.
- [ ] Every response is validated; failures retry at most N times and are logged.
- [ ] `stop_reason` is checked before parsing.
- [ ] Optional data is nullable, not required.
- [ ] Eval examples cover missing, ambiguous and malicious input.
