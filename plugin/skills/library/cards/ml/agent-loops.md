---
name: agent-loops
title: Agent loops
area: ml
tags: [agents, llm, tool-use, loop, budgets, safety]
detect: []
related: [tool-use, claude-agent-sdk, llm-guardrails, llm-evals, llm-cost-latency]
---
A tool-using agent is a bounded loop: call the model, run requested tools, feed results back, stop on end_turn or a budget.

## Verify
- `pytest -q tests/test_agent.py`: the loop runs against a scripted fake model with no network.
- `pytest -q -k budget`: step, token and time caps stop a runaway loop.
- `python -m app.agent --dry-run "task"`: tool calls are printed, not executed, for a manual trace check.

## Test first
Script the model; assert the loop terminates and surfaces tool errors.
```python
from app.agent import run

def test_stops_at_max_steps():
    model = FakeModel(always=tool_use("search", {"q": "x"}))
    out = run(model, tools={"search": lambda q: "r"}, max_steps=3)
    assert out.stop_reason == "max_steps" and model.calls == 3
```

## Do
- Loop: send messages and tool schemas; if `stop_reason == "tool_use"`, run every `tool_use` block and reply with one user message of `tool_result` blocks matching each `tool_use_id`.
- Enforce caps on steps, total tokens, wall time and cost; return a distinct stop reason for each.
- Return tool failures as `tool_result` with `is_error: true` and a short actionable message so the model can recover.
- Validate tool inputs against the schema before executing; allowlist tools per task.
- Truncate or summarise large tool outputs and old turns; keep a running token count.
- Require confirmation for destructive or outward actions; make tools idempotent where possible.
- Log every step (messages, tool calls, latency, usage) for replay.

## Avoid
- `while True` with no cap: a confused agent loops and bills forever. Cap steps and spend.
- Executing only the first tool call when several are returned in parallel: answer all of them.
- Dropping the assistant turn that held the `tool_use` blocks from history: the next call is rejected. Append it verbatim.
- Passing raw tool output (web pages, files) as instructions: treat as untrusted data and delimit it.
- Swallowing exceptions into empty results: the model assumes success. Return the error.
- Evaluating only the final answer: also score the trajectory (tool choice, step count).

## Review
- [ ] Hard limits on steps, tokens, time and cost.
- [ ] Every `tool_use` gets a matching `tool_result`.
- [ ] Tool errors reach the model; inputs are validated.
- [ ] Destructive tools gated and prompt-injection from tool output considered.
- [ ] Trajectories logged and covered by evals.
