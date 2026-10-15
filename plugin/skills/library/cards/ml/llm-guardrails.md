---
name: llm-guardrails
title: LLM guardrails
area: ml
tags: [llm, safety, injection, validation, pii, moderation]
detect: [dep:guardrails-ai, dep:nemoguardrails, dep:llm-guard]
related: [prompt-engineering, agent-loops, mcp-servers, llm-structured-output, llm-evals]
---
Layered controls around LLM calls: constrain inputs, validate outputs, limit tool power and test against injection.

## Verify
- `pytest -q tests/test_guardrails.py`: injection, PII and over-length cases are blocked or sanitised.
- `python -m evals.redteam --suite injection`: attack success rate stays under the agreed threshold.
- `grep -rn "api_key\|secret" app/prompts`: no credentials end up in prompts.

## Test first
```python
from app.guard import check_output

def test_output_with_email_is_redacted():
    out = check_output("Contact bob@example.com for details")
    assert "bob@example.com" not in out.text and out.flags == ["pii"]
```

## Do
- Treat model output and retrieved or tool content as untrusted data; delimit it and never let it change system rules.
- Limit blast radius: least-privilege tools, allowlists, human confirmation for irreversible actions, scoped credentials.
- Validate outputs with schemas and business rules before acting; reject, do not repair silently.
- Cap input length, output tokens, tool calls and spend per user and per request; add rate limits.
- Redact PII and secrets before logging and before sending to third parties.
- Render model text safely: escape HTML, never `eval`, never execute generated SQL or shell without sandboxing and parameterisation.
- Keep a red-team set of injection and jailbreak prompts in the eval suite and run it on every prompt or model change.
- Log blocked events with reasons for review.

## Avoid
- Relying on "ignore malicious instructions" in the system prompt alone: it fails. Enforce in code and permissions.
- Passing model output straight into shell, SQL or URLs: injection. Validate, parameterise, allowlist hosts.
- Giving an agent read access to private data plus a way to send data out: exfiltration. Separate or gate.
- A classifier guardrail with no measured false rates: it blocks users or misses attacks. Evaluate both.
- Logging full prompts with PII: a data leak. Redact first.
- One-time safety testing: models and prompts drift. Automate.

## Review
- [ ] Untrusted content delimited and cannot trigger privileged actions unconfirmed.
- [ ] Outputs validated before use; sinks (HTML, SQL, shell) safe.
- [ ] Limits on tokens, calls and spend.
- [ ] PII and secrets redacted in logs.
- [ ] Red-team suite runs in CI.
