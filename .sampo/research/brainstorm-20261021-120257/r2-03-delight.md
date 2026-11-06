# Brainstorm — lens: delight

- **Paste anything into the request box** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: assumption: the pack lists URL, issue, stack trace, screenshot and diff intake as separate ideas, but nothing makes one box recognise them all. The user said "I should be able to do anything with it", which implies one place to drop things.
  Done when: pasting a GitHub skill URL, an issue URL, a stack trace and an image path each shows a one-line "I'll do X" chip, and Enter runs it.

- **Credit the upstream on every run that used it** — FEATURE — value 3 — effort S — risk low — category: attribution
  Why: assumption: adopting the six repos makes provenance visible, and credit is the friendliest way to show it. Licence classes already exist (skills are source-available, the tutorial is ideas-only).
  Done when: a run that loads an adopted skill ends with "with help from anthropics/skills · pdf (licence: …)", and that line links to the pinned sha.

- **Show an intermission screen on a rate limit** — FEATURE — value 4 — effort M — risk low — category: resilience, delight
  Why: the pack shows stall detection with causes and "pause on a usage limit and resume at reset" as separate ideas. Nothing designs the wait itself. Combine them: a countdown, the queued steps that will resume, and a one-key "meanwhile, run a read-only step on a local runner".
  Done when: a simulated 429 shows a countdown screen, and pressing the key runs a read-only step on a second runner.

- **Tab-complete the request from repo signals** — FEATURE — value 4 — effort M — risk low — category: input
  Why: the pack has ghost placeholders and "suggest the first task", but those only fire on an empty box. Failing test names, TODOs and open task ids exist locally already (`fm map`, the queue).
  Done when: typing "fix the fl" and pressing Tab completes to a real flaky-test name from the repo, offline.

- **Show an ETA by analogy** — FEATURE — value 3 — effort S — risk low — category: progress
  Why: assumption: the pack's ETA ideas are numeric ("about 4 min"). Naming a past run is easier to trust: "about as long as T-1213 (6 min, same runner)". The ledger already holds the history.
  Done when: a run on a runner with at least 3 past similar runs shows "about as long as T-NNNN (N min)", and the number matches that run's recorded time.

- **Preview marketplace entries as real replays** — FEATURE — value 4 — effort L — risk med — category: discovery
  Why: the pack's plugin-recommendation ideas show a README or capability card. A 10-second replay recorded in a trial lane against a fixture repo shows what the plugin does. The guard still applies, since the trial runs unguarded nothing.
  Done when: a shelf entry for a plugin with a slash command plays a recorded run of it on a fixture. The recording is produced inside the guarded trial lane, and the shelf is built from those recordings.

- **Run the docs inside the TUI** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: the pack covers "run every command in the docs in CI", but a reader still has to copy the commands out. A Run key on each fenced example, executed in a scratch fixture, makes the docs explorable. Docs are on the thin list.
  Done when: in `fm code docs`, pressing r on a README example runs it in a temp fixture and shows its real output beside it.

- **Hatch a draft skill from a repeated habit (wild)** — FEATURE — value 4 — effort L — risk med — category: skills
  Why: wild. The pack has "draft a skill from a habit" and "show a live spec meter" as separate ideas, plus pets that grow from proven work. Combine them: the detected habit appears on the home screen as an egg, its SKILL.md draft fills in, the spec meter rises as each run validates it, and it hatches after N proven uses.
  Done when: a request repeated three times creates an egg. After two further successful runs the egg hatches into a spec-valid SKILL.md that passes the `skills` repo naming and description rules.

- **Swap cookbook patterns mid-run, like cartridges (wild)** — FEATURE — value 3 — effort L — risk high — category: orchestration
  Why: wild. The pack has `--pattern` flags and diagrams of patterns. It doesn't let you change shape at a station boundary, for example evaluator-optimizer to orchestrator-workers when a step keeps failing. The live diagram redraws as the shape changes.
  Done when: pressing a key at a station boundary re-plans the remaining steps under another pattern, the diagram redraws, and the run journal records the swap.

- **Run a weekly "guest runner" low-risk task (wild)** — FEATURE — value 3 — effort M — risk low — category: runners
  Why: wild. The pack has auditions and a runner career card. Without a standing, cheap, low-risk experiment on an unfamiliar runner, nobody tries a new CLI until something breaks. Each result becomes a verdict card and a data point for routing.
  Done when: with the setting on, once a week a read-only or trivially revertible queued task is offered to an unused detected runner. The result card shows pass/fail, cost and time, and the routing table is updated.

- **Mirror the user's typing register** — FEATURE — value 2 — effort S — risk low — category: tone
  Why: assumption: terse requesters ("fix it", "etc.") dominate the user's own words. The pack tunes report length by what gets acted on, but nothing adapts to how the user writes. Applies only to prose, never to checks or verdicts.
  Done when: after 10 requests of under 8 words, closing messages drop to one line and a `--verbose` key expands them. Verdict and proof lines stay unchanged.
