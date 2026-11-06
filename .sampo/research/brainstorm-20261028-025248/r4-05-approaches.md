# Brainstorm — lens: approaches

- **Serialize merges through GitHub's merge queue instead of cancelling runs** — FIX — value 4 — effort S — risk low — category: CI ordering
  Why: main's newest tests run was cancelled by a 35-min macOS job limit (T-1809), so a red sha said nothing, and runs cancel each other. Assumption: the repo can enable merge queue. The queue tests each PR against the tree it would merge into, so the required check runs on the real merged state.
  Done when: two PRs merged in the same minute both get a full gate run on their combined tree, and no run on main is cancelled by another.

- **Trace each gate's real inputs and cache on them** — PERFORMANCE — value 4 — effort M — risk med — category: gate caching
  Why: the affected-check picks files from heuristics and co-change, and the full gate re-runs everything (124 s CPU for a full read). Assumption: `strace -f -e trace=openat` or fanotify works on the CI and dev hosts. Each gate's recorded read set becomes its cache key, so a gate reruns only when a file it actually read changed.
  Done when: a gate that reads only `plugin/lib/x.py` is skipped after an edit to `README.md`, and a gate that does read a changed file always reruns.

- **Hermetic gates under a content-addressed action cache** — PERFORMANCE — value 4 — effort L — risk med — category: build hermeticity
  Why: gates depend on ambient state (the Ubuntu 26 `sleep`, snap chromium, `FOREMAN_CHROME`), which is why CI and local disagree. Assumption: Nix or Bazel is acceptable as an optional dependency. Each gate becomes an action keyed by its inputs and toolchain, so an identical action is a cache hit on any machine.
  Done when: the same gate run on two machines with different `PATH` produces the same action hash and one of them reports a cache hit.

- **Count pack tokens with the count-tokens endpoint, not a character guess** — FEATURE — value 3 — effort S — risk low — category: cost accuracy
  Why: the 140k context target and the 6,400-char rules budget use character estimates, and the rules file is already 16 chars over budget (T-1520). Assumption: the account can call the token-count endpoint, which is free and exact for input.
  Done when: `fm cost` before send matches the endpoint's count within 1% on three real packs.

- **Run the failing CI job locally with `act` before pushing** — FEATURE — value 3 — effort S — risk low — category: CI feedback
  Why: the Ubuntu 26 uutils `sleep` and the Python 3.12 crashes (T-1799, T-1807) were only found after a push. Assumption: `act` runs the same images closely enough to catch these. `fm ci local <job>` replays one job in a container.
  Done when: `fm ci local linux` reproduces the last known CI failure before any push.

- **Let Renovate file dependency lanes with the proof attached** — FEATURE — value 3 — effort S — risk low — category: dependency upkeep
  Why: the Node 24 action pins (T-1804) were bumped by hand. Assumption: Renovate's grouping and cooldown cover what the Foreman dependency lane would do. Each bump PR carries a gate receipt and merges only on green.
  Done when: a Renovate action bump opens a PR whose body includes the gate result, and it merges with no manual edit.

- **Vendor Foreman into each repo as a pinned git subtree** — FEATURE — value 3 — effort M — risk med — category: version skew
  Why: plugin and CLI skew is a standing risk (the "parity" and "refuse a mismatched release" ideas), and a repo's Foreman version is invisible to its history today. Trade-off: upgrades become a visible commit, and the repo carries the tool's files. Assumption: teams accept that cost.
  Done when: a commit that changes the subtree version is the only way the CLI and plugin change in that repo, and `fm doctor` fails when they disagree.

- **Give `/compact` a Foreman-written focus string** — PERFORMANCE — value 2 — effort S — risk low — category: context hygiene
  Why: compaction currently drops whatever the host chooses, and context per reply is measured at 200k. Assumption: the host's `/compact` accepts focus instructions. Foreman writes a focus line (open task, next step, pinned decisions) before compacting.
  Done when: after `/compact`, the next reply still names the open task and its next step in a test transcript.

- **Wild: bisect the pack to find the section that causes repeat ideas** — FEATURE — value 2 — effort M — risk low — category: brainstorm hygiene
  Why: wild. The ideas-so-far list repeats across rounds, and the pack is large. When a round repeats an idea, split the pack in halves, rerun the lens on each, and keep halving until the repeat trigger is isolated to one section, which then gets dropped.
  Done when: a planted repeat-trigger section is identified in at most log2(N) rounds and removed from the next pack.

- **Wild: file each lens as a branch and merge the slate with git** — FEATURE — value 2 — effort M — risk low — category: brainstorm storage
  Why: wild. Each lens writes its ideas as commits on its own branch, so `git log` shows each idea's birth, `git blame` shows which lens produced it, and duplicates are dropped by a merge rather than a prompt. Assumption: the ledger can live in a git repo.
  Done when: `git log --all -- ideas/` lists every lens's ideas and a deliberately duplicated idea is removed by the merge step.

- **Wild: an exquisite-corpse round where each lens sees only the last idea before it** — FEATURE — value 2 — effort S — risk med — category: brainstorm diversity
  Why: wild. Each child gets one idea from the previous lens instead of the full pack, which cuts input tokens sharply and forces each lens to build on a neighbour. Trade-off: fewer independent ideas, so the risk is a narrower slate.
  Done when: a round at this setting uses at most a third of the full-pack round's input tokens and still files at least 10 parseable ideas.
