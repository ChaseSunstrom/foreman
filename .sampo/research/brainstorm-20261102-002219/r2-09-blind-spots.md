# Brainstorm — lens: blind spots

- **Run a contamination canary through every learner** — SECURITY — value 5 — effort M — risk low — category: user model
  Why: T-2554 needed a manual fix because mistaken captures and Mission briefs leaked into `fmforesight`. Nothing asked whether the same leak exists in the other learners (recall, outcomes, bets, friction, lessons).
  Done when: a test plants one marked Foreman-authored line in each ledger and fails if any learner's output carries the marker. The test passes after the T-2554 filter and goes red when a filter is removed.

- **Make the test suite unable to write the real state dir** — FIX — value 5 — effort S — risk low — category: test hygiene
  Why: two "first brief" and "second brief" captures were sample lines fed to `fm intake` while debugging T-2547's test, and both had to be dropped by hand. Missing question: "what do our own tests write into the user's real ledgers?"
  Done when: `fm doctor` or CI hashes the real state dir before and after the suite and fails on any change. A planted test that calls `fm capture` without a sandbox HOME is caught.

- **Fix the breakage-ahead detector and give each detector a precision ledger** — FIX — value 4 — effort M — risk low — category: self-filed noise
  Why: three "Breakage ahead" items were dropped as false alarms. Each flagged a test-only change with no paired source, but the commit's real change lived in another module (`fmcli.py` and `fmgenesis.py`), and one was a premise-only test edit.
  Done when: replaying those three commits yields no flag. A ledger shows each self-filing detector's dropped share, and a detector over 50% dropped after 5 items is muted with a recorded reason.

- **Replay every question against the pack from before the miss** — FEATURE — value 5 — effort M — risk med — category: brainstorm quality
  Why: the pack lists eight missed asks and says what question would have caught each, but nothing tests those questions. Assumption: packs are stored at brainstorm time, so they can be replayed.
  Done when: for each missed ask, a tool-less child runs the catching question against the stored earlier pack. A scorecard shows how many of the eight it recovers, and the question is kept only if it recovers its own ask without recovering a dropped one.

- **Build an add-one arm matrix next to ablate-one** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: T-2534 (guard-only arm) and T-2536 (`--ablate`) each came after the fact. Interactions are invisible when every feature is only ever removed from the full set.
  Done when: `fm exam run --agent plain+<feature>` runs for each toggleable feature. The scorecard prints per-feature solo gain beside the ablate loss, and flags a feature whose two numbers disagree in sign.

- **Count injected context in tokens, not characters** — PERFORMANCE — value 3 — effort M — risk low — category: lean ratchet
  Why: T-2533 and T-2535 track chars. Chars per token differ between JSON, code and prose, so a note can stay flat in chars and grow in cost. Assumption: a local tokenizer approximation or the host's count is available.
  Done when: the ratchet records tokens alongside chars. A test shows a 1 KB JSON note and a 1 KB prose note get different token counts, and the ratchet trips on tokens.

- **Resolve every external reference Foreman has written, on every harness** — FEATURE — value 4 — effort M — risk low — category: install liveness
  Why: T-2542 covered systemd units only. Foreman also writes into hook entries, the status line command, MCP registrations and PATH links for four non-Claude harnesses. Assumption: a moved plugin dir leaves these dangling silently.
  Done when: `fm doctor` lists each external reference with resolves/executes/dangling. A planted moved-plugin-dir scenario turns the matching rows red.

- **Flag truncated steers in the store and in packs** — FIX — value 3 — effort S — risk low — category: steers
  Why: many steers in this pack end in "…" mid-rule (the standing intent, the #2 gen-2 growth rule, the tower-filing cold-read rule). Assumption: only the display is cut, but a pack reader cannot tell, and a cold read fed that text enforces half a rule.
  Done when: `fm doctor` fails if any stored steer ends in an ellipsis shorter than its source message. Packs link a full-text path for any steer they shorten.

- **Show a "deleted by a user word" note beside each cell n/a** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: the user's asks (dropped, re-scoped, steered) repeatedly correct Foreman's reading, such as T-2341's re-scope after reading `fmdoors`. A cell resolved without the user's own correction history repeats the miss. Assumption: re-scopes are recorded as steered rows.
  Done when: each filled cell lists the steered or dropped ledger rows touching its module, or says "none". The sweep fails a cell whose module has a steer the cell contradicts.

- **Wild: a regret half-life per module** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. The eight missed asks all landed on modules built in recent Missions (lean ratchet, exam, timers, foresight). For each module, measure days from landing to the user's first FIX or FEATURE ask touching it.
  Done when: `fm outcomes --regret` prints the median days for each module and ranks the next Mission's re-read list by shortest half-life.

- **Wild: a stub user who only knows the steers writes the next ask, and the project grades itself on surprise** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: wild. The eight missed asks were arguably predictable from the standing rules (lean ratchet, free arms, grounding). A tool-less child given the steers alone writes the three most likely next asks.
  Done when: the child's three asks are compared to the user's real next three. A match counts as predicted, and every miss is added to the missed-asks list with the question that would have caught it.

- **Wild: weekly "what Foreman still can't see about itself" probe** — FEATURE — value 3 — effort M — risk med — category: self-observability
  Why: wild. Every missed ask was Foreman failing to observe itself (per-call notes, timers, its own noise, its own duplicates). A child that sees only `fm doctor` output lists what an operator would want that it doesn't show.
  Done when: each week files at most 3 tasks, each carrying the grounding line the Mission rule requires. The next week's run skips any item already built or dropped.

- **Run a producer/consumer pair check on every generated artifact** — CLEAN — value 4 — effort M — risk low — category: wiring
  Why: the question "what produces this and what reads it?" would have found T-2547's grounding gap and T-2546's already-built gap earlier. The pack asks which anticipation outputs no session path reads.
  Done when: a registry lists each artifact (prefetch files, drafts, sealed predictions, coverage cells) with its writer and its reader's session path. The sweep fails any entry with no reader.

Next question: Which of these missed asks would a different harness's user have made, and is the missed-ask list itself skewed to Claude Code?
Next question: Which of Foreman's self-filed task classes has the user never dropped, and is that because they are good or because the user stopped looking?
