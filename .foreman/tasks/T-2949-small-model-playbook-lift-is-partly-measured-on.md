---
id: T-2949
type: FIX
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/smallcards.py, plugin/tests/test_small_cards.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-04T10:08:29Z
updated: 2026-11-06T03:52:59Z
---
# Small-model playbook variants are scored on checks the writer never saw, drafted only by a local model, against an original keyed by its text
## Raw request
> Small-model playbook lift is partly measured on the prompt: smallcards._variant_prompt hands the writer the exact 'has' phrases the eval briefs check, then scores the variant on those same briefs, so a variant passes by containing the phrases; score variants on held-out briefs the writer never saw (or drop the phrase list), print which writer drafted it, refuse a paid fallback for variant(), and key _orig_eval's cache by the playbook text's hash (T-2917 audit)
## Interpretation
Reading 1 (chosen): the variant's lift must measure the card, not phrase copying: the writer's prompt drops the brief check phrases, the result names which writer drafted it, variant() refuses a paid fallback, and the original's cached eval is reused only for the same playbook text. Reading 2: split the briefs into a writer-visible half and a scored half; rejected, it halves an already small brief set (BRIEF_CAP) and the phrases come from the playbook the writer already sees.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the writer's prompt holds none of the briefs' check phrases unless the playbook's own quoted text does, and the variant is scored on the briefs the writer never saw — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] variant() asks only a local writer: with no local answer it raises and sends nothing to a paid model; the result and its line name the writer that drafted the card — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] _orig_eval reuses a booked original only when the playbook text's sha matches; an edited playbook is measured again — verify with `python3 plugin/tests/run.py test_small_cards`
## Non-goals
## Approach (options → choice → why)
1. Do less: drop the phrase list from _variant_prompt, ask with writer=local, add the text's sha to _orig_eval's cache key and the writer to the line; likely outcome: an honest lift with four small changes. 2. Use what exists: keep the list but score on a second brief draft; fails if: the second draft repeats the first's phrases, since both quote the same playbook. 3. Split briefs half and half; fails if: 2 to 3 scored briefs give a lift too noisy to rank. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: no check phrase in the writer prompt beyond the playbook text; no paid fallback; writer named; cache keyed by text sha  <- CURRENT
2. [ ] the four changes in smallcards (prompt, writer=local, writer in result and line, sha key)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T10:08:29Z created
- 2026-11-05T02:40:24Z planned from capture
- 2026-11-05T02:40:25Z set approved=True
- 2026-11-05T02:40:25Z set scope=['plugin/lib/sampo/smallcards.py', 'plugin/tests/test_small_cards.py', 'CHANGELOG.md']
- 2026-11-05T02:40:29Z blocked: planned and approved; waits for a builder slot
- 2026-11-06T03:52:59Z unblocked
## Follow-ups captured
