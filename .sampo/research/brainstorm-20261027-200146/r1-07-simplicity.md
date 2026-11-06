# Brainstorm — lens: simplicity

- **Replace the 15-minute gate wait with one rule** — FIX — value 4 — effort S — risk low — category: gate lock
  Why: Affected checks take the machine-wide gate lock, so builders queue behind each other, and a full check waits 15 minutes before running beside a hung one. Assumption: affected checks don't need the lock at all.
  Done when: two affected checks run concurrently in a test and both finish in about the time of one.

- **Give the Rules file a write-time budget** — FIX — value 4 — effort S — risk low — category: rules budget
  Why: The Rules file has been over the doctor's 6,400-char budget since T-1520 (6,416 chars), and it was only caught by a later manual request.
  Done when: `fm rules set` refuses a 6,401-char file with a message naming the limit, and a test covers the refusal.

- **Cut the overlapping settings to one default each** — CLEAN — value 3 — effort S — risk low — category: settings
  Why: Recent work added compact-at-200k, Sonnet builders, the watchdog, three scopes, and repo pins. Assumption: most users never change these, and the overlap makes them hard to reason about.
  Done when: `fm settings list` shows at most 8 user-facing keys, and a test pins that count.

- **Use one time parser for every deadline** — FIX — value 3 — effort S — risk low — category: time parsing
  Why: `fm task defer --until` expired two hours before the weekly reset because "reset" and local time were handled separately.
  Done when: a table test runs "reset", "HH:MM" and ISO through one parser and gets the same instant each time.

- **Fold the open umbrella items into one backlog file** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: About 20 deferred "Later from T-0760/T-0818/T-0843" items each hold 7 to 29 unevaluated ideas, and T-0794 already proposes slimming Foreman.
  Done when: `fm task list --open` shows no umbrella item with unevaluated sub-ideas, and the open count drops.

- **Retire adapters with no live check** — CLEAN — value 3 — effort M — risk med — category: adapters
  Why: The Codex, Gemini and opencode items (T-0335, T-0336, T-0337) are blocked, and none of those adapters has ever been live-verified.
  Done when: the adapter list holds only adapters with a passing live check in the last release.

- **Make the hook bench compare against a same-run baseline** — FIX — value 3 — effort S — risk low — category: benchmarks
  Why: PreToolUse:Bash:script p95 was 310 ms on a loaded box and 272 ms on a quiet one, so the absolute 300 ms budget is flaky.
  Done when: the bench passes at load 0.6 and at load 1.5 when the ratio to baseline is within its limit.

- **Replace ceremony profiles with one cheap-to-thorough dial** — FEATURE — value 4 — effort M — risk med — category: ceremony
  Why: T-1266 proposes a ceremony profile per task kind, and the user keeps asking for less token burn. Assumption: one dial that sets compact threshold, model and check depth together is easier to reason about than several settings.
  Done when: `fm ceremony set cheap` changes all three settings together, and `fm cost` shows lower context per reply on the bench task.

- **Wild: a bare `fm` runs the one next step** — FEATURE — value 5 — effort M — risk med — category: entry point
  Why: The user wants to just go, without being asked, and fm has many subcommands (doctor, check, task, code, dojo, quiet) to remember. Assumption: most sessions only need the next reversible action.
  Done when: `fm` with one open task and no args runs that task's next step and prints one line saying what it did.

- **Wild: one card the model reads once instead of a rules file** — CLEAN — value 4 — effort M — risk med — category: rules format
  Why: Rules guidance keeps growing past its budget, while the model reads the same few behaviours on every turn. Assumption: a 10-line card covers the rules that change outcomes.
  Done when: the card fits the budget, and the bench shows no drop in pass rate against the full rules file.

- **Wild: archive the skills nobody routes to** — CLEAN — value 4 — effort M — risk med — category: skill catalog
  Why: The project has 1,229 skill files, and the user wants tens of thousands, not all loaded and actually used. Assumption: a skill with zero routed hits over 30 days is dead weight.
  Done when: a zero-hit skill moves to an archive directory, and `fm playbooks route` still returns the same top five on the bench fixture.

- **Wild: ship Foreman as one script with no plugin tree** — FEATURE — value 3 — effort L — risk high — category: distribution
  Why: The install surface is 1,832 files and 107 lib modules, and every extra file is more for the user to install and debug. Assumption: most of the value comes from the loop and the gates, not the catalog.
  Done when: the single file runs `fm doctor` on a clean machine with only python3 installed and passes.
