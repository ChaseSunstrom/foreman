---
id: T-1733
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T03:56:51Z
updated: 2026-10-23T04:31:52Z
base: a0619ce68d9742c9a29456752d6ee9b3e06c35d6
base_tree: a0aee01449c49f8bbb8fc4f536384ee04fe89255
plan0_at: 2026-10-23T04:01:37Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py, CHANGELOG.md]
verified: strong
---
# Fmcore.redact_obj and redact are key-blind: log_event stores {"password": "x"} unredacted
## Raw request
> fmcore.redact_obj and redact are key-blind: log_event stores {"password": "x"} unredacted because the keyword patterns need = or : right after the word
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a credential-named JSON key's value is redacted in text ("password": "x", escaped JSON too) and in objects (redact_obj on {"password": "x"}); token counts and other non-secret keys are kept — verify with `python3 plugin/tests/run.py test_core.Redaction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests for JSON text and objects
2. [x] quote-tolerant keyword pattern; key-aware redact_obj
## Resume here
<!-- auto -->
- 2026-10-23T04:22:25Z step 2/2: quote-tolerant keyword pattern; key-aware redact_obj
- git: foreman/build; 2 uncommitted: plugin/lib/fmcore.py, plugin/tests/test_core.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.Redaction` → red as expected (exit 1) · Ran 5 tests in 0.3s (1 classes, 16 at a time; slowest: Redaction 0s) / FAILED (1 classes) [ran] [tree 715411bc32fb] (2026-10-23T04:01:47Z)
- (step 2) `python3 plugin/tests/run.py test_core test_mcp test_debug test_instruments test_repeats test_code test_ledger_chain test_hooks` → exit 0 · Ran 682 tests in 171.5s (113 classes, 16 at a time; slowest: Worker 169s, Stop 147s, NoTaskGate 125s) / OK [ran] [tree 86f56cc2d954] (2026-10-23T04:30:44Z)
- (ac 1) `python3 plugin/tests/run.py test_core.Redaction` → exit 0 · Ran 5 tests in 0.2s (1 classes, 16 at a time; slowest: Redaction 0s) / OK [ran] [tree a7b1a7ad89f5] (2026-10-23T04:30:55Z)
- (ac 1) `python3 plugin/tests/run.py test_core.Redaction` → exit 0 · Ran 5 tests in 0.2s (1 classes, 16 at a time; slowest: Redaction 0s) / OK [ran] [tree a7b1a7ad89f5] (2026-10-23T04:30:56Z)
- (audit adversary) `self: the keyword pattern now allows a closing quote (or an escaped one) between the key and = or :, so JSON text, escaped JSON and Python reprs match; redact_obj blanks a scalar under a key that ends in a credential word (apiKey, AUTH_TOKEN, password) and keeps None, booleans and keys that only contain the word (tokens, token_count, secret_kinds); 682 tests across the suites that redact pass` → a secret logged as {"password": "x"} or written as JSON text no longer survives into the ledger, events, briefs or exports [tree a7b1a7ad89f5] (2026-10-23T04:30:56Z)
- (audit edge) `self: the keyword pattern now allows a closing quote (or an escaped one) between the key and = or :, so JSON text, escaped JSON and Python reprs match; redact_obj blanks a scalar under a key that ends in a credential word (apiKey, AUTH_TOKEN, password) and keeps None, booleans and keys that only contain the word (tokens, token_count, secret_kinds); 682 tests across the suites that redact pass` → a key like mytoken is redacted (likely a secret); numeric values under a secret key are redacted, booleans and None kept; values under 4 characters in text still pass (as before) [tree a7b1a7ad89f5] (2026-10-23T04:30:56Z)
- (audit self) `self: the keyword pattern now allows a closing quote (or an escaped one) between the key and = or :, so JSON text, escaped JSON and Python reprs match; redact_obj blanks a scalar under a key that ends in a credential word (apiKey, AUTH_TOKEN, password) and keeps None, booleans and keys that only contain the word (tokens, token_count, secret_kinds); 682 tests across the suites that redact pass` → no findings [tree a7b1a7ad89f5] (2026-10-23T04:30:56Z)
- (ac 1) `python3 plugin/tests/run.py test_core.Redaction` → exit 0 · Ran 5 tests in 0.3s (1 classes, 16 at a time; slowest: Redaction 0s) / OK [ran] [tree 49e3981f44dc] (2026-10-23T04:31:30Z)
- (audit adversary) `self: the keyword pattern now allows a closing quote (or an escaped one) between the key and = or :, so JSON text, escaped JSON and Python reprs match; redact_obj blanks a scalar under a key that ends in a credential word (apiKey, AUTH_TOKEN, password) and keeps None, booleans and keys that only contain the word (tokens, token_count, secret_kinds); 682 tests across the suites that redact pass` → a secret logged as {"password": "x"} or written as JSON text no longer survives into the ledger, events, briefs or exports [tree 49e3981f44dc] (2026-10-23T04:31:30Z)
- (audit edge) `self: the keyword pattern now allows a closing quote (or an escaped one) between the key and = or :, so JSON text, escaped JSON and Python reprs match; redact_obj blanks a scalar under a key that ends in a credential word (apiKey, AUTH_TOKEN, password) and keeps None, booleans and keys that only contain the word (tokens, token_count, secret_kinds); 682 tests across the suites that redact pass` → a key like mytoken is redacted (likely a secret); numeric values under a secret key are redacted, booleans and None kept; values under 4 characters in text still pass (as before) [tree 49e3981f44dc] (2026-10-23T04:31:30Z)
- (audit self) `self: the keyword pattern now allows a closing quote (or an escaped one) between the key and = or :, so JSON text, escaped JSON and Python reprs match; redact_obj blanks a scalar under a key that ends in a credential word (apiKey, AUTH_TOKEN, password) and keeps None, booleans and keys that only contain the word (tokens, token_count, secret_kinds); 682 tests across the suites that redact pass` → no findings [tree 49e3981f44dc] (2026-10-23T04:31:30Z)
## Log
- 2026-10-23T03:56:51Z created
- 2026-10-23T04:01:36Z set scope=['plugin/lib/fmcore.py', 'plugin/tests/test_core.py', 'CHANGELOG.md']
- 2026-10-23T04:01:37Z focused
- 2026-10-23T04:14:15Z paused: focus moved to T-1739
- 2026-10-23T04:15:13Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-23T04:15:13Z focused
- 2026-10-23T04:22:26Z paused: focus moved to T-1743
- 2026-10-23T04:25:30Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-23T04:25:30Z focused
- 2026-10-23T04:31:50Z done
- 2026-10-23T04:31:52Z committed 58a59257 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1606-review: Verdict: changes needed.** The core works, but the note's "logs keep it redacted" claim is false on one path, and the report-and-file flow puts t…
- T-1302 [SECURITY S, done, 2 steps] fm code app exports scrub secrets
- T-1606 [SECURITY M, done, 5 steps] Guard trust: pasted secrets, approval fatigue, fm doctor --wrong (from T-1553) — lesson: A claim like 'kept redacted' must be tested b…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_core.py
## Why not caught
the redaction tests used KEY=value shapes only; nothing logged a dict with a secret-named key
## Lessons
- Redaction must read structure (key names), not only text shapes
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- CHANGELOG.md
