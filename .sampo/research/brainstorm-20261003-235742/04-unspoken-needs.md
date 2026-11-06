# Brainstorm — lens: unspoken needs

- **Turn "user said X" into a bench case at capture** — FEATURE — value 5 — effort M — risk low — category: bench
  Why: the user keeps re-steering ("recursively improve", "measurable"); fm bench only builds cases from finished commits, so unfinished or rejected work never becomes a test. Assumption: a rejected or corrected task can be replayed with the user's correction as the pass criterion.
  Done when: `fm bench build --from-correction` creates a case from a recorded correction, and `fm bench run` reports pass/fail for it on a baseline and a candidate.

- **Gate every self-improvement merge on a bench delta with a variance floor** — FEATURE — value 5 — effort M — risk med — category: self-improve
  Why: /foreman:improve uses fm bench, but evals are "single runs, noisy" and the latest probe went dry. Without paired repeats, "improved" can be noise.
  Done when: `fm bench compare` runs each case N≥3 times per side, prints the confidence band, and `/foreman:improve` refuses to promote a candidate whose gain is inside it.

- **Mine what other harnesses ship, as a diffable feature census** — FEATURE — value 4 — effort M — risk low — category: landscape
  Why: the user asked to "research other great plugins and add them"; the landscape pass was one-off (claudekit, Kiro, Spec Kit…). Assumption: a `fm landscape` file listing features by project with a status of have/lack/rejected can be refreshed via `fm research ask`.
  Done when: `fm landscape diff` lists features seen in the latest research that are absent from the census, each with a source quote.

- **Add a skill-adoption trial: run a foreign skill on 3 bench cases before routing it** — FEATURE — value 4 — effort M — risk med — category: plugins
  Why: `fm next` routes to installed skills by name and keyword, and "skills used before rank first," but nothing proves a skill helps. Bench makes this measurable.
  Done when: `fm plugins trial NAME` runs bench cases with and without the skill and writes pass rate and cost; routing hints appear only for skills with non-negative lift.

- **Wild: Build a "regression court" that replays the user's past corrections on every Foreman release** — FEATURE — value 4 — effort M — risk low — category: bench
  Why: corrections ("run.py takes -k", "no fm research list verb") recur as the same class of error. Assumption: corrections can be stored as prompt plus checkable outcome.
  Done when: a release gate runs the stored correction cases headless and fails if a previously corrected behavior reappears.

- **Wild: Let Foreman fork itself into two candidate strategies for an L task and keep whichever passes verify cheaper** — FEATURE — value 4 — effort L — risk high — category: execution
  Why: `fmlanes` worktrees and bench's headless replay already exist, but lanes are only used for disjoint work. Racing alternatives is a new use.
  Done when: `fm race TASK --strategies 2` runs two lanes, reports pass/cost/turns for each, and merges only the winner behind one yes.

- **Add a "what would make this task unnecessary" pre-check using recall plus map** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: "Short-circuit requests that are already done" appears among the earlier ideas, but only as a done check. This one goes further: an impact scan shows whether a built-in or installed skill already covers the request.
  Done when: for a request matching an installed skill's capability, intake prints the skill's name before planning.

- **Compile a per-project "playbook lift" table from bench runs** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: playbooks are unmeasured; bench gives a cheap controlled comparison (playbook reference on versus off) rather than waiting on passive logs.
  Done when: `fm bench ablate playbook:perf` reports pass/cost deltas, and STAGE_REFERENCE drops entries with no lift.

- **Wild: Run a "stranger test": a fresh Claude with only the README tries to use Foreman on a toy repo and logs where it stalls** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: Foreman has 45 subcommands and heavy ceremony; its friction digest covers only the user's own sessions. Assumption: a headless child can complete a scripted toy task.
  Done when: `fm bench stranger` produces a transcript with a stall list and the count of guard blocks or confusion points.

- **Auto-generate a `fm bench` case from every unresolved friction cluster** — FEATURE — value 4 — effort M — risk med — category: self-improve
  Why: friction items auto-close only by hand, and the loop's scoreboard question is open. A failing case per friction cluster turns "friction stopped" into a testable claim.
  Done when: each `fm friction` cluster links a bench case that fails before the fix and passes after, and the digest shows the case id.

- **Wild: Let a night-shift lane tackle the top research-debt question and leave a cited note by morning** — FEATURE — value 3 — effort M — risk med — category: research
  Why: the user wants relentless improvement and leftover quota is wasted; `fm research ask` exists and verifies quotes. Assumption: the usage threshold from economy mode can gate it.
  Done when: with usage below a set threshold, an idle drive runs one `fm research ask` on a queued question and the note appears in recall with ✓/✗ marks.
