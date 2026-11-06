# Brainstorm — lens: bold bets

- **Verify the repo's own integrity at doctor time** — FIX — value 5 — effort S — risk low — category: reliability
  Why: A crash left four zero-byte loose git objects that broke `git diff`; `fm doctor` passed. Foreman's evidence depends on git, so silent corruption undermines every diff-based claim.
  Done when: With a zero-byte file planted in `.git/objects`, `fm doctor` fails and names the file. It offers a quarantine command that restores `git diff`.

- **Make the guard explain and learn from its false positives** — FIX — value 5 — effort M — risk med — category: guard precision
  Why: Friction shows `git stash list`, read-only python on state files, and a heredoc that merely edits source text were all blocked. Each block costs a turn and trains the user to grant approvals reflexively.
  Done when: A fixture corpus of the three known false positives passes. Each remaining block prints the exact rule and a one-line safe alternative. A new suite test fails if any read-only verb in the corpus is blocked.

- **Add a first-class "waiting on background work" drive state** — FIX — value 4 — effort M — risk med — category: drive loop
  Why: 18 drive turns ended only to wait on a reviewer subagent. The drive treats waiting as stopping, which burns a turn and a resume each time.
  Done when: Starting a reviewer in the background, then running the drive, shows a `waiting` state in `fm next` and the UI. The drive does not end the turn, and `fm friction` shows zero wait-only turn endings in a replayed session.

- **Quarantine flaky gates with a load-aware retry and a flake ledger** — FIX — value 4 — effort S — risk low — category: gates
  Why: One test class failed once under heavy machine load and passed on rerun. Without a record, a rerun-to-green is indistinguishable from a real fix.
  Done when: A gate failure that passes on an automatic single rerun is recorded as `flaky` with the test name and load average. It never counts as clean evidence, and `fm friction` lists repeat offenders.

- **Turn reviewer findings into permanent parser fuzz cases** — FEATURE — value 4 — effort M — risk low — category: review to tests
  Why: Every review batch found 3–7 real issues, mostly edge cases in new parsers and privacy of exported text. They are fixed once and never generalized.
  Done when: Each accepted reviewer finding of type edge or privacy is appended as a case to a checked-in corpus. A suite test runs all parsers and exporters over the corpus, and a deliberately reintroduced bug turns it red.

- **Scan every export for secrets and paths before it is written** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: Reviews flagged privacy of exported text. The exports (`fm export agents`, `fm pr`, proof pack, MCP server) all publish ledger text to other tools.
  Done when: A seeded API key, an absolute home path and the user's email in a lesson are redacted or refused in every export. A single shared function does this, and a test enumerates all exporters so a new one cannot skip it.

- **Wild: Let Foreman bet against itself with a settle-by date** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: Many ideas have no evidence of value after shipping. Assumption: a prediction like "this cuts wait-only turns by 80%" is rarely checked afterward.
  Done when: `fm bet "<claim>" --metric <cmd> --by DATE` records a baseline. `fm next` reports the settled result after the date, and the idea is marked won or lost in `fm friction`.

- **Wild: Give the user a "why did you do that" replay for any turn** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: The user steers by corrections and vetoes. Assumption: they want to see which rule, hint or lesson drove a given action so they can fix the cause rather than repeat the correction.
  Done when: `fm why` on a recent action prints the brief step, the hooks that fired, the recalled lessons and the hint shown. It turns "never X" into a veto in one yes/no.

- **Wild: Run a chaos monkey over Foreman's own state** — SECURITY — value 3 — effort M — risk low — category: resilience
  Why: A machine crash corrupted git objects and Foreman never noticed. Assumption: state files, the ledger and the queue have similar untested failure modes: truncation, partial writes, a missing lock.
  Done when: `fm chaos` runs in a temp copy and truncates a ledger line, empties a state file and kills a write halfway. Each case either recovers with a clear message or is filed as a self item, and none loses a finished task's evidence.

- **Wild: Merge the overlapping inbox items into one proof-and-judge pipeline** — CLEAN — value 3 — effort S — risk low — category: roadmap
  Why: The open inbox lists research cross-checks, quorum, debate-pair review, shadow plan review, a bench judge, skill duels, the counterfactual ledger and the regression court. Most are the same mechanism: run a second opinion, score it and keep the cost capped.
  Done when: The inbox shows the overlapping items merged into one item with sub-criteria. The ones that depend on a second model are cut or deferred until a single shared judge exists, and the item count drops by at least four.
