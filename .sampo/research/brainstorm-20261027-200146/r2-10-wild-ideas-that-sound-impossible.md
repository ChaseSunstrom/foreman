# Brainstorm — lens: wild: ideas that sound impossible

- **Bind each proof to the diff it tested, and refuse to close on a changed diff** — SECURITY — value 4 — effort S — risk low — category: proof integrity
  Why: `fm task prove` shows that commands ran, but nothing ties that proof to the exact diff it checked. assumption: an edit made after the proof still closes the task.
  Done when: editing a file after `fm task prove` makes `fm task close` refuse and name the changed file.

- **Compile the guard's rules into one state machine instead of scanning them per command** — PERFORMANCE — value 4 — effort M — risk med — category: hook latency
  Why: the hook bench put `PreToolUse:Bash:script` p95 near its 300 ms budget (about 310 ms once, 272 ms on a quiet run), so the cost grows with each added rule. assumption: most rules are literal prefixes that a DFA matches in one pass.
  Done when: `bench_hooks --runs 20` reports the same allow/deny verdicts on the fixture corpus and a p95 under 100 ms.

- **Answer "where is X defined" from a local symbol index with zero model tokens** — FEATURE — value 4 — effort S — risk low — category: local-first lookup
  Why: `fm map` already builds a layout and entry list, and the user keeps asking for cheap, fast answers. assumption: most navigation questions name a symbol and need no reasoning.
  Done when: `fm where <symbol>` prints the file and line for a known symbol in under 50 ms and makes no network or model call.

- **Ablate each rules-file line against the duel and delete the ones that change no outcome** — CLEAN — value 3 — effort M — risk med — category: rules budget
  Why: the rules file is over the doctor's 6,400-character budget (6,416), and lines were kept by habit. assumption: a line that no duel task depends on is dead weight.
  Done when: the rules file is under 6,400 characters and the duel pass count does not drop by more than one task.

- **Hide the model's identity from the duel judge, so the verdict is blind** — FEATURE — value 3 — effort M — risk low — category: honest benchmark
  Why: the duel compares Foreman against bare Claude Code (T-1231), and a judge who knows the sides may favour its own. assumption: the judge can score diffs and receipts without knowing which side wrote them.
  Done when: a duel run's judge output contains only anonymised labels A and B, and a re-run with the labels swapped gives the same winner.

- **Dry-run a queued task against a throwaway copy and list the files it would touch** — FEATURE — value 4 — effort M — risk low — category: preflight
  Why: the user wants work to go unattended, and a surprise write to an unexpected file is the cost they'd least want to find later. assumption: a copy plus the task's planned commands shows the likely write set before any real edit.
  Done when: `fm queue dry-run <task>` prints a file list, leaves the real tree's git status unchanged, and matches the files the real run then edits on a test task.

- **Learn from reverts: score each past fix by whether git later reverted it** — FEATURE — value 3 — effort M — risk low — category: lesson confidence
  Why: lessons carry a confidence value (T-0217) that nothing currently raises or lowers from outcomes, and reverts are a clear signal in git history. assumption: a revert within two weeks means the fix was wrong.
  Done when: a fixture repo with one reverted fix and one kept fix gives the reverted task's lesson a lower confidence after `fm lessons refresh`.

- **Diff two commits' gate verdicts as a machine-readable table** — FEATURE — value 3 — effort S — risk low — category: gate regressions
  Why: when a merge breaks a gate, the user has to rerun checks by hand to see which verdict flipped. assumption: the gate outputs are already structured enough to compare.
  Done when: `fm check --diff <a> <b>` prints one row per gate with before and after verdicts and exits non-zero when any gate flips from pass to fail.

- **Wild: run a model's read-only shell commands inside a WebAssembly sandbox so the guard hook never has to see them** — PERFORMANCE — value 4 — effort L — risk high — category: sandboxed reads
  Why: wild. Every shell call pays for a hook round-trip, and most of them only read files. assumption: `grep`, `cat` and `ls` can be replaced by WASM builds that cannot reach the network or write.
  Done when: a fixture session of 200 read-only commands runs with zero hook invocations, and an attempted write from the sandbox fails with no file change.

- **Wild: a second Foreman that stays silent and speaks only when a gate's meaning changes** — FEATURE — value 3 — effort M — risk med — category: silent sentinel
  Why: wild. The user has complained about being asked too often (they want no permission prompts), so a watcher that interrupts only on a real change could replace routine status messages. assumption: a gate's meaning changes when its inputs or its pass criteria change, not on each rerun.
  Done when: over a 20-run fixture where only three runs change a gate's meaning, the sentinel reports exactly those three.

- **Wild: when a test fails, let it propose the smallest edit that would turn it green, and wait for the user to accept or reject it** — FEATURE — value 3 — effort M — risk med — category: test negotiation
  Why: wild. Failing tests are the main source of stalled runs, and a minimal proposed edit gives the user one decision instead of an open-ended fix. assumption: a minimal patch is often enough to name the bug.
  Done when: on a fixture with one planted off-by-one bug, the proposal names that line and the test passes once the proposal is accepted.
