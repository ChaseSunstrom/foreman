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
   It carries the user's standing intent (`plugin/templates/standing-intent.md`): under gen-0, over every later
   steer, read by every cold read and seed, and #13's exam fails a draft missing a clause.
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
   From gen 2 the seed's 8th Mission is the moonshot (mission-moonshot.md): run `fm genesis frontier N`
   first, give each `### idea` its `Prior art:`, `Better by:` and `Novelty: 1-5` lines, run `fm genesis
   novelty N` (the cold read that marks obvious ideas), then name the `Spiked pick:` and its `Spike: shipped|failed`
   line; a failed spike goes to not-yet.md, and report.md lists each shipped moonshot with `(asked: …)`.
   When ideas, failures or misses keep fitting no category, `fm genesis grow KIND --name N --evidence E
   --measure M` adds one to frame.md (from gen 2; never removed). Give an added capability its coverage.md row
   before that generation's sweep, and list every added category in report.md (its F-N id and name). Today an
   added capability joins the exam spec, scorecard, seed and export; the other kinds are recorded and checked.
   Each seed carries "## The user's standing rules (steers)": every steer still in force (`c.steer_rules`, minus
   one a later steer `--reverses` or `--revisited`). Drift fails a seed missing one and only notes a steer newer than the seed.
3. After a tower edit, `fm genesis check` (exit 1 names every empty cell and not-yet gap).

Kinds:
- blocked: a brief waits on the user or a grant; work the rest of the queue.
- fatal: the tower can't go on as filed; fix what the action names.
- stopped: three reverted generations in a row. Read lineage.md and the critiques, then write the next seed by hand
  or file the report. Only step stops: `fm genesis seed` still runs, so the next seed is a choice, not a default.
- done: report.md is filed.

## See it

`fm genesis status` prints the tower; `fm genesis live on` (a publish grant) keeps the site's genesis page current.
