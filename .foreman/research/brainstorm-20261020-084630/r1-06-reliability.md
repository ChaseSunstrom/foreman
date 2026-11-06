# Brainstorm — lens: reliability

- **Test the drive against 2.1.304's headless Stop rule** — FIX — value 4 — effort S — risk low — category: compat
  Why: the pack says a plugin can no longer keep a headless run going past Stop or `--max-turns` by spawning subagents. Assumption: Foreman's unattended drive or `fm run` relies on re-prompting at Stop in some path.
  Done when: a fixture runs `claude -p` against the drive. It either finishes the queue another way or exits with a one-line "headless Stop is final; use `fm run`" message, and the test asserts one of the two.

- **Fuzz the compaction point in the e2e roundtrip** — FEATURE — value 5 — effort M — risk low — category: compaction
  Why: plain Claude Code's misses came after compaction, and Foreman's "request text that survives compaction" was fixed case by case (T-1235). Assumption: `roundtrip.py` forces compaction at one fixed point or none.
  Done when: `roundtrip.py --compact-seed N` forces compaction at a random step, including idle compaction. The run asserts that the active task, its criteria and the queued request text are in the first post-compaction context, and a failure prints the seed.

- **Bisect Claude Code versions when the roundtrip goes red** — FEATURE — value 4 — effort M — risk med — category: upstream compat
  Why: Foreman was last adapted to 2.1.301 while 2.1.304 shipped changes (`decider: "person"`, the hook cap, the Stop rule). Nobody found out until the main session read the changelog.
  Done when: `fm doctor --cc-range` installs candidate versions into throwaway prefixes, runs the roundtrip on each, and prints the last-good and first-bad version.

- **Randomize test order and shard in CI, printing the seed** — CLEAN — value 4 — effort M — risk low — category: test reliability
  Why: 226 test files, and the recent commits are all CI fixes (CPU-time bounds, a stubbed bubblewrap, a red macOS job T-1249). Hidden coupling is the likely next failure. Assumption: tests currently run in fixed order.
  Done when: CI runs the suite in a shuffled order with the seed in the annotation, `--seed N` reproduces the order locally, and two seeds both pass.

- **Lint for GNU-only shell and tool flags** — FIX — value 3 — effort S — risk low — category: portability
  Why: the macOS CI job is red (T-1249). Assumption: the cause is a GNU-ism such as `sed -i`, `date -d`, `stat -c` or `readlink -f`.
  Done when: a lint step fails on a fixture containing each GNU-ism, passes on the current tree, and the macOS job goes green.

- **Refuse to publish a benchmark delta inside the noise** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the numbers move between reruns (Haiku +29% became +14%, long session 6/6 vs 3/6 with only 3 runs), and every site claim must be measured.
  Done when: the benchmark build computes run-to-run spread per metric, tags each figure "beyond noise" or "within noise", and the page renders "no measurable difference" for the latter.

- **Stamp every benchmark result with model, CC version and prompt hash** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: the page compares reruns across 1.2.38 to 1.2.40 and Claude Code 2.1.301 to 2.1.304. A comparison is only valid if the inputs held still.
  Done when: each result JSON carries the model id, Claude Code version, Foreman version and suite hash, and the page refuses to chart runs with mismatched stamps without an explicit flag.

- **Ratchet injected bytes per turn in CI** — PERFORMANCE — value 4 — effort M — risk low — category: context cost
  Why: Foreman is about 60% dearer in the long session because hook notes and bookkeeping calls grow the context faster, and the skill list (~3,200 of ~9,600 chars) is re-sent after every compaction.
  Done when: a recorded-session fixture measures hook-injected plus skill-listing bytes per turn, CI fails if the number rises over the committed baseline, and lowering the baseline needs a one-line commit.

- **Check hook fan-out against the 12-concurrent cap** — FIX — value 3 — effort S — risk low — category: hooks
  Why: 2.1.304 runs at most 12 prompt/agent hooks of one event at a time, and Foreman has many hooks plus `bench_hooks.py`. Assumption: some event is near or over the cap once a user's own plugins are added.
  Done when: `fm doctor` counts prompt/agent hooks per event across installed plugins and warns above 8. A test shows the Foreman-only count is under the cap.

- **Fix the site theme flash with an inline head script** — FIX — value 2 — effort S — risk low — category: site
  Why: T-1244: `site.js` and `style.css` apply the stored theme only after load, so dark-mode users see a flash.
  Done when: a headless-browser test with a stored dark theme finds the dark class on `<html>` before first paint (checked via an early `MutationObserver` or the first screenshot).

- **Wild: Run a "compaction storm" soak** — FEATURE — value 3 — effort M — risk low — category: soak
  Why: the marathon survived 7 compactions, but only once and with Haiku. Wild: assumption that more compactions find more bugs.
  Done when: a nightly Haiku run with a dollar cap forces compaction every N tokens for 20 cycles and fails if the task ledger diverges from git or a queued request is lost.

- **Wild: Add a reproducible "reliability weather" file to every release** — FEATURE — value 2 — effort S — risk low — category: release
  Why: five releases in a row (1.2.36 to 1.2.40) each carried CI or site fixes. Wild: assumption that a short per-release record makes patterns visible.
  Done when: `fm release` writes a small JSON with the counts of red CI runs, hook crashes, doctor warnings and flaky retries since the last tag, and the release notes link to it.

- **Wild: Give the guard a replayable "known-24" regression corpus** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the published safety claim is 20 of 24 dangerous commands stopped (4 saved first) and 0 of 25 everyday commands stopped. The guard must never weaken, but the claim lives only in benchmark output.
  Done when: both corpora are committed as fixtures, a unit test fails if any dangerous command stops being stopped or saved, and the same test fails if any everyday command is blocked.
