# Brainstorm — lens: what the user would notice and love

- **Replay a user's "no" as a pre-action veto** — FEATURE — value 4 — effort M — risk low — category: preferences
  Why: the user repeatedly refused things (rm of the dev-mods copy denied, "never hand commands") and steers "learn". Existing ideas cover mining corrections, but none list the exact refused *actions* and consult them in the guard before proposing the same `fm ask` again. Mechanism: `fm ask` outcomes stored as (category, normalized command, task) in the state dir; a repeat ask within N days auto-skips with "you declined this on DATE" instead of re-prompting.
  Done when: after a denied `fm ask` for command X, a second identical ask in a new session returns declined without a Claude Code prompt, covered by a test.

- **Add a feature census that diffs Foreman against what people ask harnesses for** — FEATURE — value 4 — effort M — risk low — category: landscape
  Why: user said "research other great plugins/things people want harnesses to do". Landscape was researched once by hand. Mechanism: `fm landscape` runs `fm research ask` over a fixed list of sources (plugin marketplaces, harness changelogs), stores a normalized feature table in the state dir, and on re-run reports only new rows not covered by a Foreman command (matched via `fm recall`). Quote-checked claims reuse existing verification.
  Done when: running twice reports zero new rows the second time and a seeded fake changelog row appears as a candidate capture.

- **Bench ablation of the integration hints themselves** — FEATURE — value 4 — effort M — risk med — category: bench
  Why: `fm next` now names third-party skills, and the user's steer is "learn — demote hints that never help". Mechanism: `fm bench run` with the skill routing on vs off per case, recording pass and cost, writing a per-skill lift to the capability index which ranks hints. Measurable by the existing A/B compare.
  Done when: `fm bench gate` output includes a per-skill lift column and a skill with negative lift drops out of `fm next` hints.

- **Replay the user's own steers as the bench judge's preference rubric** — FEATURE — value 5 — effort M — risk med — category: bench
  Why: pass/fail on tests ignores what this user cares about (quiet output, no commands handed over, fewer turns). Mechanism: a rubric file compiled from standing-preference memory plus verbatim corrections; the replay transcript is scored mechanically on checkable items (turn count, final message length, any "run this command" phrasing via regex, token cost) and added to `fm bench show`.
  Done when: a seeded replay whose final message says "run `pytest`" scores a preference violation in the bench output.

- **Make `fm next` retire itself when ignored hints are provably free** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: the "Next:" hint text is injected every turn and users are usage-sensitive. Mechanism: hash the hint per task; if the same hint was already injected and the transcript shows the action taken or the state unchanged, inject a 1-line pointer instead of the full text, using the existing change-suppression and re-arming on compaction.
  Done when: two consecutive turns with unchanged state inject a shorter second note, verified by a hook-output length test.

- **Wild: Foreman as an apprentice that watches the user's manual Claude Code habits across projects** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: assumption: the user has several projects with similar repeated manual work; `fm repeats` only covers one session history. Mechanism: scan all project transcripts for repeated prompts and phrases ("keep recursively improving"), propose a cross-project standing order or draft playbook behind a yes/no. Wild.
  Done when: running over two project transcript sets surfaces a repeated phrase present in both as one proposal.

- **Wild: Self-play red team where a child writes the user's next complaint** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: the user keeps pushing "recursive improvement" with complaints discovered late. Mechanism: a `claude -p` child with only the verbatim steers and the last diff predicts three likely objections; each becomes a queued falsifiable check (grep or bench case) before the task is called done; objections that later match a real user complaint raise the child's weight. Wild.
  Done when: `fm ideas` or `fm task done` shows predicted objections, and one is turned into a bench case.

- **Wild: Skill transplant — absorb a foreign plugin's best procedure as a measured playbook** — FEATURE — value 4 — effort L — risk med — category: compat
  Why: user wants "add them to foreman". Mechanism: `fm adopt PLUGIN:SKILL` reads the foreign SKILL.md, trims to a playbook file with cost note, runs it against 3 bench cases versus the original skill enabled, and keeps it only if it matches pass rate at lower always-on cost. Wild.
  Done when: an adopted playbook appears in the STAGE_REFERENCE with a recorded bench comparison.

- **Wild: Standing "second Foreman" that reviews Foreman's own session transcript at wake-up** — FEATURE — value 3 — effort M — risk low — category: reflection
  Why: drive stalls (21 waits for background work) were found only via friction digests. Mechanism: at SessionStart, a Haiku `claude -p` reads the previous session's events.jsonl summary only and writes at most two lines to the friction digest ("long idle at X"), costing one cheap call per session.
  Done when: a session with a seeded long wait yields a friction line at next start.

- **Group queued research questions into one batched `fm research ask`** — PERFORMANCE — value 3 — effort S — risk low — category: research
  Why: `fm research ask` plans sub-questions per call and re-fetches pages; several asks in one queue repeat fetches and planner calls. Mechanism: accept multiple questions, share the planner call and a per-run URL fetch cache.
  Done when: two questions citing the same URL trigger one fetch, asserted in a test.

- **Surface each bench case's cheapest-passing configuration in the dashboard band** — FEATURE — value 2 — effort S — risk low — category: ui
  Why: `fm bench models` saves routing data but the user sees none of it. Mechanism: the foreman-ui dashboard reads the saved routing file and shows one line "Sonnet passes S, Haiku fails M" only when it changed since last view.
  Done when: changing the saved routing file changes the dashboard line once, with a render test.
