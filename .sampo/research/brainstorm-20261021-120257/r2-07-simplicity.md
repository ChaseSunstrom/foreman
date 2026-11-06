# Brainstorm — lens: simplicity

Most of the simplicity ground is already covered in the pile (one verb, delete-only passes, ratchets, `upstreams.toml`). These ideas stay out of that and mostly say how to meet the "integrate six repos, work with anything, full management" mandate by reusing what 1.2.48 already has.

- **Point `fm plugins` and `fm scout` at all six repos** — FEATURE — value 4 — effort S — risk low — category: integration
  Why: `fm plugins find/install` and `fm scout` (which already watches Claude Code releases) exist. The mandate asks for six sources, "automatically", and a new verb per source would add six surfaces. One watch list and one catalog source list cover all of them.
  Done when: a test adds a fixture entry for `anthropics/skills` to the watch list and `fm scout` reports a changed sha, with no new top-level verb in `fm --help`.

- **Replace the 29 round-1 briefs with three executable story scripts** — CLEAN — value 4 — effort S — risk low — category: planning
  Why: the pack lists 29 planned-but-unbuilt briefs. The user's real asks reduce to three stories: first run (setup, preflight), daily run (home, run, undo), unattended run (queue, resume). Each story is a shell transcript against a fake runner that fails until the story works, and the briefs become checklist items under it.
  Done when: `tests/stories/{first,daily,unattended}.sh` exist, run in CI, and each of the 29 briefs is closed or folded into one of them.

- **Make the run branch the only run state** — CLEAN — value 4 — effort M — risk med — category: runs
  Why: the planned list has a process registry, durable runs, reopen, undo, PR from a run and a journal, which are six pieces of run state. Instead, each step is a commit on `fm/run-<id>`, and the brief plus a pid lease complete the picture. Resume reads the branch, undo is a branch delete, and PR is a push.
  Done when: killing `fm code` mid-run and rerunning `fm code --task ID` continues from the last commit, with no run-state file other than the lease.

- **Emit one run report that every other output reads** — CLEAN — value 4 — effort M — risk med — category: outputs
  Why: the list proposes receipts, postcards, digests, PR bodies, outcome reports, shift reports and replays. One `report.md` per run (request, plan, checks with commands, diff stat, cost, next step) lets the TUI end screen, the PR text and the digest be views of it.
  Done when: the TUI's final screen, `--json` and the PR body for one fixture run are all produced from the same `report.md`, and a test fails if they disagree.

- **Run `fm code bench` as an ordinary project** — CLEAN — value 3 — effort M — risk med — category: bench
  Why: `fmcode.py` and `fmcodebench.py` are separate paths. Seeded cases become tasks in a fixture project, graded by their own verify commands through the normal run path. That way, any run-path fix (stall, lean sessions) automatically improves what the bench measures.
  Done when: the bench runs through `fm code --task` and `fmcodebench.py` shrinks by at least a third.

- **Use one runner address string everywhere** — FEATURE — value 3 — effort S — risk low — category: runners
  Why: runners are currently CLIs, endpoints, models.json entries and code.toml entries. One syntax (`claude`, `codex`, `openai:MODEL@URL`, `cmd:./my-script`) works in the flag, config, task field, TUI picker and bench report.
  Done when: all five surfaces accept the same string, and a test round-trips each of the four forms.

- **Use grep as the index for the pinned upstream trees** — PERFORMANCE — value 3 — effort S — risk low — category: integration
  Why: the user wants six repos "integrated". The cookbook's `registry.yaml` and the skill frontmatter already index their own content. Pinned shallow trees plus a thin `fm sources find` over `grep -r` and frontmatter avoid building and maintaining a database.
  Done when: `fm sources find "prompt caching"` returns cookbook paths from a pinned tree, with no index file written.

- **Ship `code.toml` as a commented template** — FEATURE — value 3 — effort S — risk low — category: config
  Why: users asked for "one config line picks the default". `fm code init` writes every option commented out with its default and a one-line reason. Editing is uncommenting, and there is no wizard to build or maintain.
  Done when: the generated file parses as empty config, and a test checks every documented option appears exactly once.

- **Adopt at most three upstream capabilities per release** — FEATURE — value 4 — effort S — risk low — category: scope — wild
  Why: assumption: "integrate all of these, fully featured" otherwise yields hundreds of low-value adoptions. A quota ranked by the user's friction counts forces the evidence-led choice, and the rest wait in the register.
  Done when: the release script refuses to close a release with more than three new adoptions, and the register shows ranked waiting items.

- **Emit `replay.sh` from every run** — FEATURE — value 3 — effort M — risk med — category: runs — wild
  Why: assumption: a plain script of patches and check commands, runnable on a clean checkout, makes the cassettes, undo, demo and reproduce-on-another-machine ideas the same artifact. Anyone can read it without Foreman.
  Done when: running `replay.sh` in a fresh clone reproduces the run's diff and its checks go green.

- **Reveal settings only after a run needs them** — FEATURE — value 3 — effort M — risk med — category: config — wild
  Why: assumption: most settings are never touched. A setting appears in `code.toml` and the TUI only once a run hit its case (stall → `FM_STALL`, rate limit → pause policy), with the receipt that triggered it.
  Done when: a fresh install lists no more than five settings, and a forced-stall fixture run adds the stall setting with its reason.

- **Build the home screen as a plain directory listing with colour** — CLEAN — value 3 — effort M — risk med — category: ui — wild
  Why: the home needs "counts, what's active" per project. If each project's state is a directory of briefs and a lease, the home is a sorted listing with no registry, and `ls` shows the same thing.
  Done when: deleting any home cache changes nothing on screen, and the home's data comes from a single function used by `--plain`.
