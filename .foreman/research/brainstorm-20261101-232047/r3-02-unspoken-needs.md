# Brainstorm — lens: unspoken needs

Earlier questions my lens can answer: with `--round-first` on, Foreman-filed captures are held until the round's next seed is filed, so the user won't see a trigger working until then (assumption: no urgent flag is set). After a week away, the only page that could undo a trigger is one that lists each trigger's fires with their undo lines, and I don't see one in the pack.

- **Compute the cell counts at run time** — FIX — value 3 — effort S — risk low — category: mission intake
  Why: this pack's own history quotes "58", "59" and "61" empty cells for what is presumably the same grid. A hand-typed count undermines "coverage must be real".
  Done when: the Mission request and the report take their empty-cell number from `coverage.md` at run time, and a test shows a changed grid changes the number.

- **Log every cell reclassification** — FEATURE — value 4 — effort S — risk low — category: coverage integrity
  Why: the user's rules forbid templated or padded cells. The cheapest way to hit "no empty cells" is to move cells to n/a or "existing". Assumption: no ledger records cell state changes today.
  Done when: each gap→n/a or gap→existing move writes a row with a reason and a cited file, and the sweep goes red when the n/a share rises more than a set amount in one generation.

- **Append user-only items to a live report file** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: pillar 7 says "what only the user can do goes in the final report". A crash or usage-limit death mid-run loses an in-memory list.
  Done when: killing the run mid-Mission leaves a report file listing every user-only item found so far, and the final report reads from it.

- **Anchor cell citations to symbols, not line numbers** — CLEAN — value 3 — effort S — risk low — category: coverage integrity
  Why: cells must be "grounded in a file". Cites like `fmcli.py:1282` rot on the next edit, and Missions 5–8 run in parallel lanes, so edits are constant. Assumption: current cells use file:line cites.
  Done when: the linter accepts a cite only as file plus symbol or test name and rejects bare line numbers. A rename of the cited symbol turns the cell red.

- **Run the cell probes on a stranger repo** — FEATURE — value 5 — effort M — risk med — category: self-hosting bias
  Why: Foreman mostly tests itself, and the user already wants recall measured per language on child-authored scenarios. A thinking cell that only holds in this repo isn't covered.
  Done when: each filled Exhaustive-thinking cell's probe also runs on a fixture repo in a different language, and cells that pass only on Foreman's own repo are listed.

- **Map each standing steer to the cells that enforce it** — FEATURE — value 4 — effort M — risk low — category: steers
  Why: the rule is that every steer becomes a rule plus an automatic check. A reverse map shows which steers touch the thinking stages with no check, and which cells serve no steer.
  Done when: `fm genesis sweep` prints steers with no cell and cells with no steer. It names at least one real orphan or says "none".

- **Give readings and options short ids that one-word replies bind to** — FEATURE — value 3 — effort S — risk low — category: asking
  Why: the user is told to expect no mid-run questions, and when a stop does happen, answers typed as free text can't be matched to a reading. Binding "r2" or "do less" to the stored reading records which reading the user actually meant.
  Done when: a reply of "r2" selects reading 2, is logged against it, and an unknown id is refused with the list.

- **Derive new stage columns from the missed-ask list** — FEATURE — value 4 — effort M — risk med — category: grid growth
  Why: the pack lists eight asks earlier brainstorms missed, for example T-2525 (the late start point). Standing rule (steer #6) lets Genesis add stages through `fm genesis grow`. Assumption: no step yet asks which cell each missed ask should have lived in.
  Done when: each missed ask is assigned a (row, stage) cell. Any ask that fits no column produces a `grow` proposal carrying the ask as its evidence.

- **Age every gap cell and name its task or its wait reason** — FEATURE — value 3 — effort S — risk low — category: coverage integrity
  Why: "empty cells go to the next Seed" is a handoff with no clock, and 28 "Later from T-07xx" bundles show how deferred work sits.
  Done when: every gap cell shows days open and a task id or a revisit date, and a cell with neither fails the sweep.

- **Let the user cross out a cell in the web UI to mint a steer and check** — FEATURE — value 3 — effort M — risk med — category: web UI — wild
  Why: assumption: the user will want to say "this cell is nonsense" or "this matters most" where they see it. They already have the steer-to-check pipeline (`fm decide --check`); the UI has no entry point to it.
  Done when: a cross-out or star on a cell stores a steer with a check, and the next sweep reflects it.

- **Order the fill by the user's predicted scrutiny** — FEATURE — value 3 — effort S — risk low — category: prioritization — wild
  Why: a tool-less child sees only the steers and "asked" lines and ranks the 58 cells by which the user would challenge first. Those cells are filled first and cold-read hardest. The child's guess is then scored against which cells the user actually opens.
  Done when: the fill order file shows the child's rank, and a later report shows the rank correlation with the cells the user opened.

- **Give each cell a "break me" command** — FEATURE — value 4 — effort M — risk med — category: trust — wild
  Why: assumption: the user wants proof without reading prose. Each cell ships one command that triggers its failure in a scratch copy and shows the catch.
  Done when: for at least 10 cells the command runs in under a minute, shows the red state, and leaves the real tree untouched (checked by a clean `git status`).

- **Show gap-cell progress as a living page, not a file** — FEATURE — value 2 — effort S — risk low — category: web UI
  Why: pillar 3 wants every idea on a checklist page, and the user will want the same for cells. The sweep also cross-checks the page against `coverage.md`.
  Done when: the page lists cells by state with live counts that equal `coverage.md`'s.

Next question: Which cells does Exhaustive thinking share with #3 and #4, and who owns a shared cell when two parallel lanes both fill it?
Next question: When the plan gate can't run at all (hookless harness, crashed hook, no user present), what does the user see afterwards?
