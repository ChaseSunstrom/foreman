# Brainstorm — lens: user value

- **Trace each part of the request to its evidence** — FEATURE — value 5 — effort M — risk low
  Why: assumption: multi-part requests like the user's own often lose a clause, and the gates check steps and criteria, not the user's words.
  Done when: capture splits a 3-clause request into atomic asks, `fm task done` refuses while any ask has no linked criterion or evidence, and the outcome report lists each ask beside its evidence.

- **Turn pasted errors into a repro at intake** — FEATURE — value 4 — effort M — risk med
  Why: FIX tasks need red→green proof, and the user never runs commands, so they paste tracebacks or logs. Nothing in the pack parses a pasted trace.
  Done when: a pasted Python or Node traceback yields a FIX brief with scope globs from its frames and a draft failing verify command, and a fixture test covers three trace formats.

- **Check the final message's claims against evidence** — FIX — value 4 — effort M — risk med
  Why: the Stop hook gates evidence but not what the summary asserts, so "all tests pass" can be stated without a matching record for the current tree.
  Done when: a Stop-hook test shows a final message saying "tests pass" is flagged with one factual note when the latest evidence is stale or missing, and is not flagged when it matches.

- **Suggest a codemod when the same edit repeats** — PERFORMANCE — value 4 — effort M — risk low
  Why: the thrash ring buffer already sees edits. Five or more near-identical edits by hand cost many turns and tokens, and cheap-model delegation still spends tokens.
  Done when: after a 5th similar edit a single note proposes a scripted rewrite with a dry-run diff, and a replayed trace shows the note fires once and not on unrelated edits.

- **Check that verify commands can run here at plan time** — FIX — value 3 — effort S — risk low
  Why: the lint covers PATH, "can't fail" and pipes, but not missing env vars, services or ports, so a task can reach done and only then find it can't be verified.
  Done when: `fm focus` on a brief whose verify command needs an unset env var or a closed port prints a one-line blocker and offers one yes/no, and a test covers both cases.

- **Let the user's wording set ceremony for one task** — FEATURE — value 3 — effort S — risk low
  Why: the `profile` setting is global. The user speaks in natural language ("quick", "just", "be careful"), and a per-request signal would save turns without changing settings.
  Done when: "quick fix" on an S task selects the lean gate set, "be careful" raises one tier of audits, and both are logged in the brief and show in `fm gates`.

- **Queue an offline dependency and vulnerability sweep** — SECURITY — value 3 — effort M — risk low
  Why: assumption: `fm run` and idle-time work can call local tools such as `pip-audit`, `npm audit` and lockfile age, and nothing now finds stale or vulnerable dependencies without a request.
  Done when: `fm doctor --deps` writes at most one queued SECURITY brief per project per week for findings, skips cleanly when the tools are absent, and hooks make no network calls.
