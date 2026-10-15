---
name: tool-use
title: Claude tool use
area: ml
tags: [claude, llm, tools, function-calling, agents, json-schema]
detect: []
related: [anthropic-sdk, prompt-caching, llm-evals, rag]
---
Claude tool use: define tools with JSON Schema, run the loop on `tool_use` blocks, and return `tool_result` blocks.

## Verify
- `pytest -q`: the tool loop passes against a scripted fake client.
- `python -c "import jsonschema, mypkg.tools as t; [jsonschema.Draft202012Validator.check_schema(x['input_schema']) for x in t.TOOLS]"`: every tool schema is valid JSON Schema.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Script the model: first response asks for a tool, second finishes. Assert the result was fed back with the right id.
```python
from mypkg.agent import run

def test_tool_result_is_returned_with_matching_id(fake_client_factory):
    client = fake_client_factory([
        {"stop_reason": "tool_use", "content": [{"type": "tool_use", "id": "t1", "name": "add", "input": {"a": 1, "b": 2}}]},
        {"stop_reason": "end_turn", "content": [{"type": "text", "text": "3"}]},
    ])
    assert run(client, "1+2?") == "3"
    last = client.requests[1]["messages"][-1]
    assert last["content"][0]["tool_use_id"] == "t1"
```

## Do
- Give each tool `name`, a precise `description` (what it does, when to use it, what it returns) and an `input_schema` with `required` fields.
- Loop while `response.stop_reason == "tool_use"`. Append the assistant message as returned, then one user message holding a `tool_result` block per `tool_use` block.
- Match every `tool_use_id`. Return all results from parallel calls in a single user message.
- Return errors as a `tool_result` with `is_error: true` and a message the model can act on.
- Validate tool input before executing. Treat it as untrusted. Apply authorization checks in the tool, not in the prompt.
- Cap loop iterations and total tokens. Raise when the cap is hit.
- Use `tool_choice` to force a tool for structured extraction.
- Keep tool results small: truncate or summarize large payloads.

## Avoid
- Appending only the text of an assistant turn: dropping `tool_use` blocks makes the next call fail. Append the full `content`.
- Missing or mismatched `tool_use_id` in the result: API error. Echo the id exactly.
- Running shell, SQL or file tools on model-provided strings unchecked: injection. Allow-list, parameterize and sandbox.
- Vague descriptions and overlapping tools: wrong tool picked. Sharpen descriptions and merge duplicates.
- Unbounded loops: runaway cost. Add an iteration cap.
- Throwing exceptions out of the loop when a tool fails: the model cannot recover. Return `is_error`.
- Parsing the model's prose instead of the structured `input`: fragile.

## Review
- [ ] Schemas are valid, with required fields and clear descriptions.
- [ ] Results are returned with matching ids, errors flagged with `is_error`.
- [ ] Inputs are validated and permissions enforced in code.
- [ ] Loop has iteration and token limits.
- [ ] Tests cover multi-tool, error and no-tool paths with a fake client.
