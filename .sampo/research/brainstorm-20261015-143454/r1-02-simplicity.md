# Brainstorm — lens: simplicity

Round 1, simplicity lens. The pile is already dense here, so these are mostly narrow, second-order cuts grounded in the pack. I assumed repo layout details from the file map and did not verify them.

- **Make one Foreman install the only install** — CLEAN — value 4 — effort S — risk low — category: install
  Why: T-0923 only warns when marketplace and `install.sh` copies differ. A warning treats the symptom, so the fix is to make the skew impossible. The installer would link `~/.claude/foreman` to the marketplace checkout, or the reverse, so there is one tree to update. Assumption: both paths can be pointed at one directory.
  Done when: after installing by both routes in a scratch HOME, `readlink -f` of both entry points gives one directory and `fm doctor` has no version-skew check left to run.

- **Derive every version string from one tag** — CLEAN — value 3 — effort S — risk low — category: release
  Why: T-0431 "Release 1.2.16" is still deferred while 1.2.28 has already shipped, so version-bound queue items rot. Stamp the plugin manifest, CHANGELOG header, installer and desktop from a single source at release time. A release task whose version is below the current tag closes itself as superseded.
  Done when: bumping one source updates every version string, and a test fails if any file disagrees. The stale T-0431 closes as superseded.

- **Stop committing demo recordings and build them as release assets** — CLEAN — value 3 — effort S — risk low — category: repo weight
  Why: the demo recordings (`demo/live.*`, `demo/record_live.py`) went stale when the pane was redesigned, which forced a "re-record" task. Binary captures in git also go out of date with every UI change. Generating them in release CI means the README always links the current one. Assumption: the recordings are checked in.
  Done when: `git ls-files demo` lists scripts only, and the release workflow publishes a fresh recording that the README links.

- **Generate test fixture repos from compact specs** — CLEAN — value 2 — effort M — risk med — category: test weight
  Why: the repo has 350 files and 155 are tests, including whole fixture trees such as `fixtures/instruments/repo/app.py`. A builder that creates each fixture from a few lines at test time shrinks the tree and keeps fixtures from drifting from the code they exercise. Assumption: most fixtures are small and deterministic.
  Done when: the fixtures directory shrinks by at least half in file count and the full suite still passes.

- **Write only non-default settings to the settings file** — CLEAN — value 3 — effort M — risk low — category: config
  Why: the installer touches many settings, and users can't tell which ones they chose. A file holding only deviations from defaults is short enough to read. It also means a later default change reaches everyone who never overrode it.
  Done when: a fresh install writes an empty or near-empty settings file, and `fm config` output matches the previous effective values.

- **Move the root clutter under `docs/` and keep the root to README, install and license** — CLEAN — value 2 — effort S — risk low — category: repo layout
  Why: the root holds 11 files, including MASTER.md, BUILD_PROMPT.md and INSTALL.md, so a newcomer opening the repo sees a pile. Assumption: the installer and marketplace metadata don't need these at the root, apart from INSTALL.md, which agents may fetch by raw URL.
  Done when: the root listing has at most 5 entries, and a link checker finds no dead path in README or docs.

- **Give installer and `fm` prompts one non-interactive contract** — FEATURE — value 3 — effort S — risk low — category: scripting
  Why: the installer now asks before enabling bypassPermissions, `fm tidy --apply` confirms, and INSTALL.md is meant for agents to follow. Each prompt behaves its own way when stdin is closed. A single `--yes` and `FM_YES` convention, with a "no tty means safe default, never hang" rule, removes that class of problem.
  Done when: every prompt site runs with `</dev/null` in a test, takes the documented safe default without hanging, and `--yes` takes the affirmative.

- **Mark unverified adapters unsupported and hide them from help and doctor** — CLEAN — value 4 — effort S — risk low — category: scope
  Why: T-0335, T-0336 and T-0337 (Codex, Gemini CLI, opencode) have been blocked on live verification. Unverifiable code is a liability and implies support that doesn't exist. Anything not live-verified within N releases is labelled unsupported and dropped from `fm --help`, `fm doctor` and the README.
  Done when: each adapter carries a "last verified" date in the manifest, and one that has passed the cutoff shows nowhere in help or doctor output.

- **Add a surface-delta trailer to every commit** — FEATURE — value 3 — effort M — risk low — category: scope ratchet — wild
  Why: a hook writes `Surface: +1 verb -2 settings +0 skills` into each commit, computed from the registries. `fm doctor` sums the trailers per release, so "did this round grow Foreman?" becomes one line, not an argument. Assumption: verb, setting and skill registries can be diffed mechanically.
  Done when: a commit that adds a verb carries the trailer, and `fm doctor` prints the net surface for the last tag range.

- **Enforce a two-minute rule: every verb must appear in the scripted tour or be labelled labs** — CLEAN — value 4 — effort M — risk med — category: surface — wild
  Why: with 108 verbs, one useful keep-test is whether the verb earns a seat in the 60-second `fm demo` or the tour. Verbs that can't be shown there go under a `labs` label, hidden from default help but still working. Nothing is deleted, so the risk stays low, and the long tail stops competing for attention.
  Done when: CI fails if a non-labs verb is absent from the tour script, and `fm --help` lists only tour verbs.

- **Cap the generated product page at one printed page** — CLEAN — value 3 — effort M — risk low — category: docs — wild
  Why: an `fm print` command renders "what Foreman is and does" from the verb, setting and skill registries as a single page, and CI fails if it overflows. A product that can't be summarised on one page is telling you something. This also stops MASTER.md's hand-written feature list from drifting.
  Done when: `fm print` output fits 60 lines of 80 columns, and adding a verb without a one-line description fails the check.
