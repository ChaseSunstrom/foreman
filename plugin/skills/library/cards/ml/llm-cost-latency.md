---
name: llm-cost-latency
title: LLM cost and latency
area: ml
tags: [llm, cost, latency, caching, batching, tokens]
detect: []
related: [prompt-caching, llm-streaming, agent-loops, anthropic-sdk, llm-evals]
---
Control LLM spend and speed with measured token use, prompt caching, right-sized models, streaming and budgets.

## Verify
- `pytest -q tests/test_budget.py`: per-request and per-user caps trigger and are logged.
- `python -m evals.cost --suite smoke`: tokens, cost and p50/p95 latency per example are reported against the baseline.
- `python -c "from app.llm import usage_report; usage_report()"`: usage by feature, including cache read and write tokens.

## Test first
```python
from app.llm import Budget, BudgetExceeded
import pytest

def test_budget_blocks_before_call():
    b = Budget(max_input_tokens=1000)
    with pytest.raises(BudgetExceeded):
        b.check(estimate_tokens("x" * 100_000))
```

## Do
- Log input, output, cache-read and cache-write tokens and latency for every call, tagged by feature.
- Put the long static prefix (instructions, tools, documents) first and mark it with `cache_control`; keep it byte-identical between calls.
- Route by difficulty: a small model for classification and extraction, a larger one for hard reasoning; confirm on evals.
- Set `max_tokens` deliberately and ask for concise output formats.
- Stream for interactive use to cut perceived latency; run independent calls concurrently with a concurrency limit.
- Use the batch API for offline bulk work that can wait.
- Trim history: summarise or drop old turns and truncate large tool results.
- Set budgets, timeouts and retries with backoff and jitter; cap retries.

## Avoid
- Changing the system prompt or tool order per request: the cache never hits. Make the prefix stable.
- Unbounded agent loops or retries: runaway spend. Cap steps, tokens and attempts.
- Sending whole documents each turn: cache them or retrieve passages.
- Optimising by guess: measure tokens and p95 first.
- Swapping to a cheaper model with no eval: silent quality loss. Compare on the eval set.
- Unlimited parallel fan-out: rate limits and bills spike. Bound concurrency.

## Review
- [ ] Usage and latency logged per feature.
- [ ] Cache hit rate checked and prefix stable.
- [ ] Model choice backed by an eval.
- [ ] Hard caps on tokens, steps, retries and concurrency.
- [ ] Bulk work uses batch processing.
