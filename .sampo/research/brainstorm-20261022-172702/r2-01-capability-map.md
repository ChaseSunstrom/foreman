# Brainstorm — lens: capability map

- **Replay the transcript against the skill listing** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: the pack's "why" list is inference ("as far as we can see"); no measurement of which turns should have loaded a skill. `fm usage` only counts uses.
  Done when: `fm skills replay <session>` prints, per past turn, the skills whose description matches the turn's task and whether the Skill tool was called, and the output on the last 30 days of Foreman sessions reproduces the 2-of-13 usage figure.

- **Add a skill-coverage matrix to the capability map** — FEATURE — value 4 — effort S — risk low — category: capability map
  Why: assumption: skills cover only 13 of the moments Foreman has (plan, edit, prove, close, review, design, bench, lane, fsck, settings, guard, intake). No list of moments vs. skills exists in the pack.
  Done when: `fm skills map` lists each `fm` command family and hook moment with the skill or playbook that covers it, and flags the uncovered ones; the output is a test fixture.

- **Ship a "before you edit" / "before you close" skill pair with bundled scripts** — FEATURE — value 5 — effort M — risk low — category: skills
  Why: hooks inject "Next: fm …" so skills lose; the two moments that matter most (plan-before-edit, prove-before-close) have no task-shaped skill, and a skill can bundle a script that prints the checklist plus live task state.
  Done when: both skills exist, their descriptions start "Use whenever you are about to …", and a bench case shows each is invoked at its moment.

- **Add a design skill family (3D scene, motion, looks, tokens, critique)** — FEATURE — value 5 — effort M — risk low — category: design
  Why: the user asked repeatedly for 3D, motion and non-generic UI; ui/scene-3d (7 reads) and ui/motion (4 reads) are the playbooks actually read, yet no design skill is listed. `fm scene`, `fm design lint/roll/tokens`, `fm critique` exist as commands with no skill wrapper.
  Done when: `foreman:design-*` skills exist, each pointing at its fm command and playbook, and a UI task in the bench loads one.

- **Make the hook "Next:" line carry a one-line skill excerpt** — FEATURE — value 4 — effort S — risk low — category: hooks
  Why: Claude skips skills because the hook already hands it the command. Embedding the skill's key rule inside the hook text makes the skill's content arrive without needing the Skill tool. Stays under the 10 KB preview limit.
  Done when: hook output for a planning turn includes the matching skill's top rule, size measured ≤ a set budget in `bench_hooks.py`.

- **Add a description-budget optimizer** — FEATURE — value 3 — effort S — risk low — category: skills
  Why: 1,957 of 2,000 chars used, T-1508 kept the cap; allocation is by hand. Descriptions should be spent where firing value is highest.
  Done when: `fm skills budget` ranks skills by (task-frequency × fire-rate) per character, suggests trims, and `fm doctor` fails if the total exceeds the cap.

- **Add per-skill kill criteria to doctor** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: 11 of 13 skills had zero uses in 30 days; nothing forces a decision about them.
  Done when: `fm doctor` warns for any skill with zero uses after N sessions post-rewrite, naming merge or delete, and the warning clears when handled.

- **Run skills on the cheap model in the bench** — PERFORMANCE — value 3 — effort M — risk med — category: evals
  Why: Haiku-class models trigger skills less reliably than larger ones; a description that works on Opus may be invisible on Haiku, and Foreman runs builder lanes on the cheapest model that can.
  Done when: the trigger eval reports fire-rate per model tier and the rewritten descriptions reach a set rate on Haiku.

- **Offer a skill-pack export for other repos (`fm skills export`)** — FEATURE — value 2 — effort M — risk med — category: distribution
  Why: assumption: the discipline skills (prove, close, review) are useful without the rest of Foreman; the anthropics/skills pattern shows standalone folders spread.
  Done when: export writes self-contained skill folders with no fm dependency, and a clean-repo test loads them.

- **Make the model pick skills by asking `fm which <task text>`** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: a deterministic router covering all 82 playbooks plus 13 skills sidesteps the listing cap, and since Claude already runs fm commands from hooks, it is the path of least resistance. (Differs from the earlier "foreman:index" idea: it is a command, not a listing entry.)
  Done when: `fm which "add a spinner animation"` returns ui/motion with its path, and the hook "Next:" line suggests it on UI tasks.

- **Wild: Skill karaoke — replay a skill's steps as a live checklist in the pane** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A loaded skill's steps tick off in the foreman-ui pane as the matching fm commands run, so people see the skill working and notice when it's skipped.
  Done when: loading a skill shows its steps in the pane and each ticks when its command appears in the transcript.

- **Wild: Skill sparring — a nightly agent attacks each description with adversarial prompts** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: wild. A sub-agent writes prompts that should and shouldn't fire each skill, finds confusable pairs, and proposes description edits, checked by the trigger eval before anything lands.
  Done when: a nightly run writes a report of confusable skill pairs and one accepted edit with eval before/after numbers.

- **Wild: Skill receipts in the close-out — "this task would have used foreman:X"** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. Each closed task lists the skills used and the ones that matched but were skipped, which turns the dead-skill problem into a visible nudge the user sees every run.
  Done when: the final task report contains a "skills used / skipped" line, backed by the replay data.
