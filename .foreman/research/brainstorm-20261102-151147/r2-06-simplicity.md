# Brainstorm — lens: simplicity

- **Make `fm go` run the last printed Next command** — FEATURE — value 4 — effort S — risk low — category: ux
  Why: the user already asked for "one next command on every nonzero fm exit" (c20), and that is only half the loop. They still have to retype or copy it. A bare `go` would also make the printed commands the one path through the tool.
  Done when: after a refusal that prints `Next: fm X`, running `fm go` executes exactly `fm X`. With no recorded Next it exits 2 and says so.

- **Use one consent flag for every code-running verb** — CLEAN — value 4 — effort S — risk low — category: cli surface
  Why: T-2636 added `fm prove --steer`, which "needs --yes-run like the other code-running modes", so each prove mode now carries its own consent wording. Foreman's consent steers (grants, publish, push) already show consent splitting into many forms.
  Done when: a test enumerates every verb that runs repo code. Each accepts `--yes-run` and refuses without it with the same one-line message, and no other consent flag exists on them.

- **Replace the `fm run` stop flags with one `--until` expression** — FEATURE — value 4 — effort M — risk med — category: drive
  Why: T-2669 added `--stall-usd`. The steers add `--pace off`, `--round-first`, the budget cap and the risk budget, so each new stop reason gets a new flag. A single `--until "usd_since_close>5 or tasks>=10"` could hold all of them, and the receipt would name the clause that fired.
  Done when: `fm run --until "usd_since_close>0.01"` stops and the receipt quotes that clause. `--stall-usd N` still works as an alias for the matching expression.

- **Hard-code flags whose value never varied in 60 days** — CLEAN — value 3 — effort S — risk low — category: subtraction
  Why: `fm usage --prune` (fmcost.py:1480) already counts unused verbs, and the user dropped "unused verbs under fm tidy" because that remainder was small. Flag values are the unmeasured part. A flag that always takes the same value is a decision, not an option.
  Done when: `fm usage --flags` lists each flag whose recorded values have a single entry over 60 days, with its call count, and files one CLEAN capture per flag.

- **Store the coverage grid sparsely** — CLEAN — value 3 — effort M — risk low — category: genesis
  Why: the steers define coverage.md as 13 capabilities plus every harness area, by surfaces, by stages, and every cell must hold a grounded idea or a recorded n/a. Most cells are n/a or reused phrasing. The "templated cell" ban is a symptom of that. Storing only real cells and deriving the empties would remove it.
  Done when: `fm genesis check` reads a file containing only grounded cells and prints the empty-cell list computed from the frame. A fixture with a duplicated phrase across rows still fails.

- **Delete deciders that abstain almost always** — CLEAN — value 3 — effort S — risk low — category: measurement
  Why: the user dropped the c16 "report abstain rate" row because `check_predictions` already reports muted kinds. The one real gap noted was that `decide()` doesn't book a None answer. A decider that abstains over 95% of the time costs lines and decides nothing, so the better fix is to remove it.
  Done when: `fm doctor` names any decider with at least 20 calls and an abstain rate above 95%, and files a CLEAN capture to remove it.

- **Cap each Mission brief at one screen and one Done-when command** — CLEAN — value 3 — effort S — risk low — category: genesis
  Why: Mission 6's request is "exhaustive thinking", and the pack shows briefs deferred as "Later from T-0760 (29 ideas…)" and "(525-idea brainstorm)". Bulk is how the backlog got to 30+ deferred items.
  Done when: `fm genesis check` fails a Mission file over 25 lines or with more than one `Done when:` line, and passes one that meets both limits.

- **Add `fm tail`, one chronological stream across all ledgers (read-only)** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: assumption: the user checks several readers (`fm burden`, `outcomes`, `digest`, `usage`) to answer "what happened?". A merged read view gives one place to look without the risk of rewriting the ledgers, which "Merge Foreman's ledgers into one record" would take on.
  Done when: `fm tail -n 20` prints the last 20 events from at least three ledger classes in time order, each tagged with its source. It writes nothing, and a torn tail line is skipped with a warning.

- **Reduce all gate and doctor checks to one registry** — CLEAN — value 4 — effort L — risk med — category: gates
  Why: the map names three gates (`fm doctor`, `roundtrip.py`, `bench_hooks.py`). A steer check is stored by `fm decide --check`, run by `genesis sweep` and named by `doctor`. One check is therefore wired in several places.
  Done when: a single `checks` table lists each check once. `doctor`, `sweep` and `ship` iterate it, and a test fails if any check exists outside it.

- **Run a receipts-only week (wild)** — FEATURE — value 3 — effort M — risk med — category: noise
  Why: the standing intent is to hold back what the user doesn't need. `fm burden --by-source` (T-2667) now counts injected characters per source. A mode that suppresses every injected note except the closing receipt, with `fm more` to reveal them, would show which sources get requested.
  Done when: with `FM_QUIET=1`, SessionStart injects nothing. `fm more` prints the withheld notes, and the ledger counts reveals per source.

- **Cap each Mission's file reach (wild)** — CLEAN — value 3 — effort M — risk med — category: locality
  Why: assumption: large Missions are what create the broad "touches everything" diffs, such as `register.tsx` needing a split (T-0166). A declared path budget per Mission, checked at merge, would force smaller, separable changes.
  Done when: a Mission declares `reach: plugin/lib/fmguard*, plugin/tests/…`. The merge check fails a diff that touches a path outside it and reports the offending file.

- **Quarantine unreferenced skills behind a stub index (wild)** — PERFORMANCE — value 3 — effort M — risk med — category: footprint
  Why: `plugin/skills` holds 1,388 of 2,134 files, and the map notes that cards load by name (`fm lib show NAME`). If the install ships only a one-line index and fetches a skill on first call, most files never exist on a user's disk.
  Done when: a fresh install writes fewer than 200 files under skills. `fm lib show python` still resolves, and a skill that was never fetched is absent from disk.

- **Convert failed-spike notes into one "not yet" page (FIX-light)** — CLEAN — value 2 — effort S — risk low — category: genesis
  Why: the standing rule sends failed spikes to not-yet.md with the blocker. Blocked tasks (T-0335/36/37, T-0352, T-0418) wait on one user action each. Printing them as a single table keyed by that action shows what unblocks the most.
  Done when: `fm next --blocked` prints one row per unblocking action with the count of tasks it frees, sorted descending.

Next question: which of the 40+ standing steers could the user delete without noticing, and how would a measurement tell?
Next question: what is the smallest set of verbs a new user needs in week one, according to the usage ledger rather than the docs?
