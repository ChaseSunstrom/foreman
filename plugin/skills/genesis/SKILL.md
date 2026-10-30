---
name: genesis
description: Use whenever the user wants Genesis: a self-seeding run of generations toward one goal they wrote, from gen-0 to a final report, driven by fm genesis step.
disable-model-invocation: true
---

# Foreman: Genesis

A tower of generations toward one goal the user wrote (gen-0). Tower files change only through `fm genesis put`,
every choice goes through `fm decide`, and anything that leaves the machine needs its grant.
A user steer mid-run becomes a standing rule plus its check in the same task:
`fm decide "<rule>" --cites "user steer <date>" --check "python3 plugin/tests/run.py test_…"` (or
`fm genesis check`, `fm exam scorecard`); the sweep stays red while a steer rule has no check or its check fails.

## Start (no gen-0 yet)

1. The user's own words are gen-0. Given only a line, or nothing: `fm genesis draft "<line>"` prints a whole gen-0.
   Show it; their MUST/NEVER lines stay verbatim, and anything it marks unconfirmed is kept or cut by them.
2. `fm genesis init --file -` saves it read-only and sealed by its hash (refused if it holds a secret); drift fails
   if gen-0 ever changes, and the sweep turns red on a grant kind no earlier generation used.
3. `fm genesis spec` maps its §2 capabilities to an exam, a third held out for grading only.
4. `fm genesis exam` grades Genesis itself (#13) on the held-out third: drafts from a line, nothing and "super
   improve this" on generated projects; `--arm plain` is the baseline. `fm exam run --agent genesis` runs a whole
   generation in a throwaway repo.

## Drive

Repeat until the kind is done or stopped (on blocked, work the rest of the queue and come back):

1. `fm genesis step --json` names the one next action: {stage, gen, action, command, kind}.
2. Do it. Stages in order: spec (when spec.md is missing), seed (≤ 8 Missions), mission (`fm mission`,
   `fm ideas`), intake, build (each brief closed with `fm task finish`), critique, select (`fm genesis select N`), drift (`fm genesis drift N`), sweep
   (`fm genesis sweep N`), then the next seed (`fm genesis seed N+1`) or the report.
3. After a tower edit, `fm genesis check` (exit 1 names every empty cell and not-yet gap).

Kinds:
- blocked: a brief waits on the user or a grant; work the rest of the queue.
- fatal: the tower can't go on as filed; fix what the action names.
- stopped: three reverted generations in a row. Read lineage.md and the critiques, then write the next seed by hand
  or file the report. Only step stops: `fm genesis seed` still runs, so the next seed is a choice, not a default.
- done: report.md is filed.

## See it

`fm genesis status` prints the tower; `fm genesis live on` (a publish grant) keeps the site's genesis page current.
