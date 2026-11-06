## Verdict
Changes needed. These are two small, cheap fixes, not a redesign.

## lens: intent / edge / maintainer
- MEDIUM — plugin/lib/fmhooks.py:1197-1198, 3518-3524 — `meta["clauses"]` is project-wide but the hook now writes it for every session, and the gate never checks `session_id`. Session B's 3-clause prompt makes session A's "Done." hold on B's clauses. The once-per-set key (`g["clauses"]`) is also project-wide, so that hold uses up B's own. Reproducer: two `UserPromptSubmit` calls with different `session_id`s, the multi-part one second, then `stop("All done.")` for the first session. Fix: store `"session": sid` in the record and have the gate return None when `meta.get("session") not in (None, pl.get("session_id"))`. Confidence: high.
- MEDIUM — plugin/lib/fmrecall.py:542,554 — a clause with fewer than 2 distinct content tokens can never be covered, because `account` needs 2 or more shared tokens. "Please fix it." tokenises to `["pleas"]` (`fix` is in `_STOP`, `it` is under 3 letters). "Let me know." and "Thanks a lot!" are similar. A prompt such as "Fix the login timeout. Rename the tab to preferences. Thanks a lot!" therefore holds every time, whatever tasks exist. Fix: in `clauses()`, keep only parts where `len(set(_tokens(x))) >= 2`. This fixes `fm clauses` too. Confidence: high. I did not run the existing `fm clauses` tests against it.
- LOW — plugin/lib/fmhooks.py:3527 — the key is computed from the re-accounted list. Capturing a task that covers one of three held clauses shrinks the set and changes the key, so the gate holds again. That is up to N holds per prompt. Fix: hold only if some clause has not been held before, using a per-clause hash.
- LOW — plugin/lib/fmhooks.py:52 — `len(text.split()) < 9` is dead code. Three clauses of 3 or more words each already need 9 or more words. Delete it.
- LOW — plugin/lib/fmhooks.py:1191 — `_asks(text)` sits outside the try block. If it raised, the generic handler would drop the whole prompt, including a pending "yes" approval. Fix: wrap it, or compute `asks` inside the existing try.
- LOW — plugin/tests/test_hooks.py:103-122 — nothing covers the `FOREMAN_WORKER_OF` guard, the slash-command guard, the over-12 cap, or the session scoping. Each guard could be deleted without a test failing.

## Your question: false holds from context sentences
Take "I tried the build. It failed with a stack trace. Please fix it." It becomes 3 clauses and 13 words, so it is recorded. A task whose Raw request holds the prompt covers the first two clauses. But `fm task new` makes `--raw` optional (fmcli.py:5829), so the usual title-only task shares about 1 token with each context sentence. Those clauses stay unaccounted. "Please fix it." is uncoverable in any case.

The same happens with intake blocks (`CONTEXT:`, `MUST:`, `SKIP:` lines) and with a pasted traceback of 12 lines or fewer. Each line becomes a clause.

The hold fires only on a done claim, once per set, and the agent then has to run one `fm clauses --note N` call per clause. At 5 to 10 multi-part prompts a day across parallel sessions, that is 20 or more extra turns a day. The larger cost is that the agent learns to answer "answered in chat" reflexively, which empties the gate of value.

My view: the cost is acceptable only after the two MEDIUM fixes above. The session scope removes cross-session false holds. The 2-token filter removes the clauses that can never be covered, which is the structural false positive. I would not add a verb or imperative heuristic. It would be a hardcoded list, and the memory notes say to learn from data instead. I would revisit after a week of `stop_gate` events (logged at fmhooks.py:3531) show how many holds end in `--note`.

## Acceptance criteria
- Multi-part prompt records its clauses at submit, the Stop gate holds the uncovered one, a task covering a clause drops it, and a 2-clause prompt records nothing: met in the test at test_hooks.py:103-122. I read it and did not run it.

## Implicit decisions
- Clauses are stored redacted but not passed through `c.plain`.
- The 3–12 bounds and the 1-day age limit were reused unchanged.
- A later plain prompt leaves the old list in place for up to a day, so it can still hold.
- Prompts sent by a program are still recorded. `_sent_by_program` gates approvals only.

## Not checked
I did not run the tests. I did not check whether CHANGELOG or MASTER wording matches the code beyond the diff.

Noticed: the recorded list persists for a day across unrelated later turns. Clearing it on a non-multi-part, non-"yes" prompt would narrow that.
