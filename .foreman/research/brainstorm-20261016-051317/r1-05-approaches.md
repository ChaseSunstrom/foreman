# Brainstorm — lens: approaches

- **Make verbs self-register from drop-in files** — CLEAN — value 4 — effort M — risk low — category: dev experience
  Why: every new command edits one `HELP_TIERS` line in `fmcli.py`, and nearly every second parallel merge of the day conflicted (T-1059, T-1062 twice). This is the structural fix. Each verb ships a small `verbs/<name>.toml` (tier, summary), and help is assembled at run time. The cheaper alternative is a `merge=union` gitattribute on the registry. That is a stopgap, because ordering still collides.
  Done when: two lanes that each add a verb merge with no conflict, and `fm help` lists both in their tiers.

- **Add a sidecar index of brief headers** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: hooks went 135 to 72 ms once they stopped parsing all 1,069 briefs (T-1140). `fm state --json` still took over 120 s under load, and other commands still parse every brief. A stat-keyed index of id, status, type and size, rebuilt only for changed files, gives them the same win. The trade-off is one more cache that can go stale, so it has to fall back to a full parse.
  Done when: `fm state --json` on the 1,069-brief repo takes under 1 s warm, and the output matches the unindexed path byte for byte.

- **Lint a verify command when it is added** — FIX — value 4 — effort S — risk low — category: reliability
  Why: verify commands name test modules that don't exist or `npm test` in a repo without npm, and this is caught only when they run (T-1128/T-1133 made such runs editable, but nothing checks at add time). A preflight resolves the binary, checks that the named file or module exists, and runs a collect-only or `--help` probe where one is cheap. It warns instead of blocking, because some commands need a built tree.
  Done when: adding `python3 -m pytest nosuch.py` or `npm test` in a repo with no package.json prints a specific warning, and a valid command adds silently.

- **Gate builder fan-out on machine load** — FEATURE — value 4 — effort S — risk low — category: lanes
  Why: load reached 30-60 with 4 builders. That made `fm state` slow, and a load-sensitive criterion failed a merge once and then passed. A governor reads loadavg against core count and holds new lanes, or runs merges one at a time, while the machine is over a threshold. The trade-off is lower peak throughput in exchange for fewer false reds.
  Done when: with a simulated load above the threshold, `fm lane` queues the next builder with a stated reason, then starts it once load drops.

- **Wrap builders in an environment contract** — FIX — value 4 — effort M — risk med — category: lanes
  Why: builders hung on bare stdin readers (T-1129), ran bare `fm lease drop` (T-1134), and cd'd into subdirectories so lease paths doubled (`mods/foreman-ui/mods/foreman-ui/...`). These were fixed one at a time. A wrapper fixes the class: stdin is `/dev/null`, the cwd is pinned to the worktree root, and the lease API rejects a path whose leading segments repeat. The alternative is more prompt text, which has already failed three times.
  Done when: a fixture builder that reads stdin and one that cds then leases a relative path both end in a clear error instead of hanging or writing a doubled path.

- **Build a round checklist page with build/skip marks** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: pillar 3 requires showing every idea on a checklist with build/skip marks before skipping any, and the user's wording is "do everything in that brainstorm". A static HTML page lists the ideas grouped by cluster, with toggles that write a decisions file. The loop reads that file, and an unmarked idea defaults to build.
  Done when: `fm ideas --page` writes an HTML file, and a toggled skip shows up in the decisions file and is excluded from the queue.

- **Render the pane from one view-model in terminal and HTML** — FEATURE — value 3 — effort L — risk med — category: UI
  Why: the pane wasn't screenshot-verified this round, and pillar 4 needs before and after shots of every screen. A single JSON view-model with two renderers lets a headless browser capture deterministic screenshots from the HTML one. The risk is that the two drift apart, so the terminal output needs a golden test.
  Done when: `fm ui --html` writes a page for the demo fixture, and a screenshot test of it passes in CI.

- **Explain a guard decision from the CLI** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: twice the main thread wrote a scratch script to replay a command through the real hook with the real cwd (T-1125, T-1141). `fm guard why "<cmd>"` runs the real hook path with the current cwd and prints allow or deny, the rule that matched, and the safe alternative. `fm guard why --last` replays the most recent denial.
  Done when: the verb reproduces the T-1141 heredoc case's allow verdict and names the rule, with no scratch script.

- **Keep a persistent capability map that diffs over time** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: pillar 2 asks for a map of rival products with have, half-have and lack marks, and it gets redone from scratch each run. Store it as a file with one row per capability and a status. Each round re-scouts the rivals (their pages are untrusted text) and reports only new rows and status changes, then queues the gaps.
  Done when: running the scout twice produces an empty second diff, and a manually added rival capability shows up as a new gap task.

- **Mine the workflow's own friction into tasks** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: the end-of-round review found its problems by hand: repeated merge conflicts, re-merge builders, scratch replay scripts. The ledger already holds these signals. A miner counts conflicts per file, re-merge lanes, and scratch scripts in the temp dir, and files a task when one recurs. It would have found the `HELP_TIERS` problem two merges in.
  Done when: replaying this round's ledger yields a task naming `HELP_TIERS` as a conflict hotspot.

- **Escalate uncertain heuristics to a cached cheap model** — FEATURE — value 3 — effort M — risk med — category: accuracy
  Why: the card backtest is a text match, history fix seeding is keyword-based, and the untrusted-text check is keyword heuristics. The heuristic stays the first pass. Only results in an uncertain band go to Haiku, with the verdict cached by content hash and the model output treated as data. That avoids a model call on every check.
  Done when: a labelled set of 30 borderline cases scores higher than the keyword-only result, and a second run makes zero model calls.

- **Wild: Let `fm do "<sentence>"` route plain English to verbs** — FEATURE — value 3 — effort M — risk med — category: usability
  Why: assumption: a user who says "I shouldn't need to ask" wants one entry point and not a 150-verb vocabulary. The router shows the classified task type and the verbs it would run, and does nothing until confirmed. It builds on bare `fm` answering "what now?".
  Done when: `fm do "make the pane calmer"` prints a FEATURE classification and a dry-run list, and changes nothing without `--yes`.

- **Wild: Give skipped ideas a resurrection trigger** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: about 30 deferred "Later from T-…" items sit with no condition for coming back. Several already say "later: needs evidence" (T-0861, T-0863, T-0866). A skipped item carries a testable trigger such as "when the same ask appears 3 times", and it re-enters the queue when the trigger fires.
  Done when: a skipped item with a count trigger reappears in the queue after the third matching ask, and the ledger records the trigger firing.

- **Wild: Pair every idea with a "do less" sibling on the checklist** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: assumption: the checklist should show the smaller alternative next to the full build, so the choice is visible and not a binary skip. A cheap model drafts a one-line cut-down variant, and the page marks the cheaper path as the default for L-effort items.
  Done when: each L-effort row on the checklist page shows a smaller variant, and picking it queues the smaller task.
