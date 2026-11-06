**Verdict: approve with nits.** The gate does what the acceptance criterion says. I did not run the tests. The nits below are scope and test gaps, not defects in the stated behaviour.

## lens: intent
- MEDIUM — plugin/lib/fmhooks.py:3500-3502 — A day is a loose proxy for "the last request". `fm clauses` is only run by the agent (opt-in), and the list stays in meta until `--note` or a new `fm clauses` call. A follow-up request an hour later has a different intent, but a "Done." reply is held with the old request's clauses. — Compare `meta.at` with the turn or prompt start (`_turn_began`, as `reload_due` does) and treat a list older than the latest user prompt as stale. Keep the 1-day cap as a backstop. — 65%
- LOW — plugin/lib/fmhooks.py:3497 — The gate only fires if the agent ran `fm clauses`. The only callers are `planning.md:5` (agent guidance) and `cmd_clauses`, and no hook calls `fm clauses`. The agent that silently drops a clause is the one least likely to have run it. This matches the AC as written ("while fm clauses' open list is non-empty"). It is a limit on the CHANGELOG claim "so a sweeping request isn't called finished". — Reword the CHANGELOG to say "when you've run `fm clauses`", or capture a follow-up that has UserPromptSubmit run it. — 80%
- LOW — plugin/lib/fmhooks.py:3505-3507 — The AC says "the same set never blocks twice", but the key includes `session_id`. A second session in the same project gets blocked once for the same list. The MASTER note documents "once per session and set", so this is consistent with the docs and not with the AC wording. The test's `sess-2` stop runs after the list is empty, so it never exercises this. — Decide which is meant. If once per set, drop the session from the key. — 60%

## lens: adversary: ok
- The clause text is redacted when stored (`fmrecall.py:573`). It is passed through `c.plain` and `c.fit` before reaching the reason, so there are no control characters and the length is bounded. The sha1 is only a dedupe key and has the same use as `_claims_gate`. The agent can silence the gate with `--note`, which is the intended path and is logged.

## lens: edge
- LOW — plugin/lib/fmhooks.py:3501 — `c.age_days(...) or 0` treats a missing or unparseable `at` as fresh, so a corrupt stamp fails open to "block". `cmd_clauses` always writes `at`, so this needs hand-edited meta. — Use `age = c.age_days(...)`, then `if age is None or age > 1: return None`. — 70%
- LOW — plugin/lib/fmhooks.py:3505-3507 — `--note` changes the set hash, so each partial `--note` followed by a done claim in a later turn holds again. Up to N holds are possible. This is probably intended, but it is not tested or documented. — Add a test, or note it in MASTER. — 50%

## lens: operator: ok
- The cost is one meta read per Stop that contains a done claim. A held stop costs one extra model turn per session per list, which is rare. There is no new always-on context. The CHANGELOG entry sits contiguous with its neighbours (no list split) and the MASTER note is in the right section.

## lens: maintainer
- MEDIUM — plugin/tests/test_hooks.py:2084-2099 — Two behaviours would survive mutation: the one-day staleness cutoff and the session scoping of the key. The only `sess-2` stop runs when the list is empty, so any key passes. The 5-item cap, the `closed` pass-through, and the precedence over `_evidence_gate` are also untested. — Add a case that sets `at` two days back and asserts no block. Add a case that stops from `sess-2` with the same open list and asserts the intended result. Add a 6-clause case that asserts only five are named. — 80%
- LOW — plan metadata — `plugin/lib/fmhooks.py` and `plugin/tests/test_hooks.py` are named by no step. Both hunks serve the AC, so this is a plan gap and not scope creep. — Add them to step 1 of T-2138.

## Acceptance criteria
- "Blocked once, naming them": met. `fmhooks.py:3496-3511` and the test at lines 81-83 check it.
- "The same set never blocks twice": met per session (test line 84). It is not shown across sessions (see the LOW above).
- "A `stop_hook_active` stop ends the turn": met. `fmhooks.py:3498` returns None, and test line 79 checks it.
- Verify command (`python3 plugin/tests/run.py test_hooks test_request`): not run here.

## Implicit decisions
- The staleness window is 1 day, not tied to a prompt boundary.
- The hold key is session_id plus sha1 of the JSON list, and the last 50 keys are kept.
- The gate runs after the evidence gate and before the claims gate. It reuses `claims_done` with step=None, so any "fixed", "resolved" or "shipped" counts as a done claim.
- Up to five clauses are named, each cut to 80 characters.
- A `stop_gate` event is logged.
- `closed` is now computed eagerly, even on one-off and reload stops. That is trivial work on briefs already loaded.

## Not checked
I did not run the tests or any hook. I did not check `_read_gate` concurrency beyond the existing lock.

**Noticed:** have a UserPromptSubmit hook run `fm clauses` on multi-part prompts, so the gate doesn't depend on the agent opting in.
