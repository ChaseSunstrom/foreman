# Brainstorm — lens: approaches

- **Cut context packs at boundaries and keep each section once** — FIX — value 4 — effort S — risk low — category: ideas pipeline
  Why: this pack prints "The user's own words" twice, the README stops at "fails in", and the map stops at "plugin…". That is the mid-word-cut problem the user already fixed for titles (T-1985), and it costs every brainstormer tokens.
  Done when: a test builds a pack and asserts each section header appears once and no section ends mid-word or mid-path.

- **Steer the loop by a five-number scorecard** — FEATURE — value 5 — effort M — risk med — category: loop
  Why: assumption: "improve in all ways" has no end, and the loop stops only on a dry-round count. Pick five measurable targets (first-time-pass rate, dead-end refusals per week, hook p95, full-suite wall time, ask-to-close time). Each round attacks the worst one.
  Done when: the loop brief names the metric it is targeting, and `fm loop status` prints all five with their trend.

- **Brainstorm per module, not per repo** — FEATURE — value 4 — effort M — risk low — category: brainstorming
  Why: the 300+ ideas so far are mostly generic, while the user's real asks are module-specific (`run.py`, `fmdocs.py`, `fmambient.py`, `fmloop.py`). A pack built from one module's source, its last ten fixes and its open tasks lets a lens go deep.
  Done when: `fm ideas --module plugin/lib/fmdocs.py` builds a pack with only that module's source and history, and the ideas cite functions in it.

- **Index ideas by theme and reject near-duplicates** — FEATURE — value 4 — effort M — risk low — category: ideas pipeline
  Why: "Suggest the near-miss on every no-match error" appears three times, and close-out receipts three times, in the list above. Store ideas as clusters with counts, show the pack theme names and counts, and refuse a new title that is too close to an existing cluster.
  Done when: filing a title with token overlap ≥0.7 to an existing idea attaches to that cluster, and the pack's ideas section is under 40 lines.

- **Show a file's last three fixes when a task first touches it** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: the same modules are fixed again and again: `run.py` in T-1994, T-1996 and the latest ask, `fmdocs.py` twice, and the ambient run twice. Surfacing the past fixes at first edit turns "sweep for sibling gaps" into something that happens automatically.
  Done when: the first Edit of a file in a task prints the three most recent task ids and titles that touched it, and the test checks a file with no history prints nothing.

- **Audit every Foreman feature against native Claude Code** — CLEAN — value 4 — effort M — risk low — category: slimming
  Why: native hooks, prompt/agent hooks (T-0797), subagents and `/code-review ultra` keep absorbing what plugins used to do. T-0794 (Slim Foreman) is open but has no evidence base.
  Done when: a checked-in table maps each skill, hook and command to a native equivalent with a keep, retire or thin verdict, and each retire verdict becomes a task.

- **Run the Foreman rules with Haiku as a rule linter** — FEATURE — value 4 — effort M — risk low — category: docs and rules — wild
  Why: assumption: a rule that a small model can't follow from the text alone is unclear. Run a scripted task under `claude-haiku-5-5` with only the rules text and log where it stalls, then rewrite those lines.
  Done when: a script outputs the rule lines that the small model violated or asked about, with a count per rule.

- **Shrink every failing input to a minimal repro** — FEATURE — value 3 — effort M — risk low — category: testing — wild
  Why: bugs like the `@path`-only line (T-1989) and the ambiguous `-k` pattern came from long real inputs. Delta-debugging a failing intake text or hook payload to the smallest trigger gives a sharp regression test.
  Done when: `fm repro min <file>` outputs a smaller input that still fails the same check, and a test proves the output is at most half the original on a seeded case.

- **Add a prediction line to each shipped fix and score it later** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: assumption: nothing records whether a fix helped. A `PREDICT:` line (for example "dead-end refusals from run.py fall to 0") gets checked a week later against the event log.
  Done when: `fm report` lists each prediction as hit, miss or unknown, and a test closes a task with a prediction and finds it in the report.

- **Batch shipping into trains with one suite run** — FEATURE — value 3 — effort M — risk med — category: shipping
  Why: the user typed "Ship Tn to main" six times in a row (T-1982, T-1987, T-1992, T-1996, T-2001), and each ship runs its own full test run.
  Done when: `fm ship --train` lands all green closed tasks in order with a single suite run and prints one receipt per task.

- **Rebuild the task ledger from git trailers** — CLEAN — value 3 — effort L — risk high — category: state — wild
  Why: commit subjects already carry T-ids and the sub-ids they fold in (for example "T-2001: T-1998, T-1999, T-2000"). Deriving closed-task state from git, not stored files, removes a class of drift and crash bugs. Open work would still need a store.
  Done when: deleting the closed-task cache and running `fm doctor --rebuild` reproduces the same closed list from git alone.

- **Chain proof receipts by hash** — SECURITY — value 3 — effort M — risk low — category: trust
  Why: "proves its work with commands it actually ran" is only as strong as the state files. A hash chain over each proof record makes editing a past proof detectable, which is cheaper than re-running everything in CI.
  Done when: `fm doctor` fails if any proof record was edited after the fact, and a test edits one and sees the failure.

- **Keep a persistent hook daemon behind thin shims** — PERFORMANCE — value 3 — effort L — risk med — category: hooks
  Why: `bench_hooks.py` exists and T-0832 (shell prefilter) is parked for lack of data. A long-lived process answers hook calls over a socket, so Python startup is paid once per session.
  Done when: `bench_hooks.py --runs 20` shows p95 for the daemon path under half the cold-start p95, and the hook falls back cleanly when the daemon is dead.

- **Run the full suite in CI and wait on its status** — PERFORMANCE — value 2 — effort M — risk med — category: gates
  Why: assumption: the repeated overlapping-suite fixes (T-1967, T-1984) exist because local gates compete for one machine. A CI workflow already exists (the badge in the README). The cost is latency and a remote requirement, which conflicts with local-first users.
  Done when: with the setting on, `fm ship` pushes a branch, waits for the workflow result, and refuses to land if it is red.
