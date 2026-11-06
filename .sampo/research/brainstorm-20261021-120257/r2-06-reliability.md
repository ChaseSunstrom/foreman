# Brainstorm — lens: reliability

- **Derive the changed-file set two independent ways and fail closed on disagreement** — FIX — value 5 — effort M — risk low — category: judge integrity
  Why: the harness judges "every changed file" to catch guard violations, Git config/hook edits and undone commits, but the pack shows one derivation. Assumption: it relies on `git status`/diff alone, which misses ignored paths, mode-only changes, symlink swaps and submodules.
  Done when: a fixture where a worker edits an ignored file, chmods a script and swaps a symlink yields identical changed sets from `git status --porcelain=v2 -z` and a content-hash walk, and a deliberately blinded first deriver makes the run refuse to close.

- **Tripwire the out-of-tree files a worker can reach** — SECURITY — value 4 — effort M — risk low — category: containment
  Why: restoring Git config and hooks covers in-repo damage. CLI workers also run with the user's home access (`~/.gitconfig`, shell rc files, `~/.claude` settings, `$FOREMAN_HOME`). Assumption: those are not currently hashed around a run.
  Done when: a fake worker appending to `~/.bashrc` in a scratch HOME causes the run to report and restore it, with the path named in the final status.

- **Land a run by compare-and-swap ref update from the recorded base** — FIX — value 4 — effort M — risk med — category: atomic landing
  Why: "close with a commit" plus "a commit undone" suggests commits are made in place. A kill between step commits leaves a half-landed state. Assumption: runs commit directly on the user's branch.
  Done when: killing at every journal point in a scripted run leaves the branch either at the base sha or at the full verified result (`update-ref old new`), never between the two.

- **Detect silent prompt truncation by comparing reported to expected prompt tokens** — FIX — value 4 — effort S — risk low — category: local models
  Why: the planned "local models' real context" item exists because llama.cpp-style servers truncate the head of an over-long prompt without error, and a slot then fills against a half-read prompt.
  Done when: a stub endpoint reporting `prompt_tokens` below 70% of the harness's estimate makes the slot fail with a "truncated at N tokens" cause instead of being accepted.

- **Roll back a single adopted upstream asset when its probe fails after an update** — FEATURE — value 4 — effort M — risk low — category: upstream sync
  Why: the whole-snapshot last-good idea exists, but the request is to keep up with six repos automatically. One bad skill or plugin should not freeze the other 165. Assumption: adoption is tracked per asset in a lockfile.
  Done when: an update whose `SKILL.md` fails the spec lint or capability-card diff is pinned to its previous sha while the rest of the sync completes, and `fm doctor` lists the pin and the reason.

- **Cache accepted slot answers in the run journal so a resume replays them, not re-asks** — FEATURE — value 4 — effort M — risk low — category: resume determinism
  Why: durable runs and reopen are planned. A resumed run that re-queries a nondeterministic model can plan differently from the half-executed run it continues, and costs more.
  Done when: killing a run after the plan slot and resuming it executes the same plan hash with zero extra model calls for that slot.

- **Put a cross-process rate limiter per endpoint and key in front of every runner** — FIX — value 3 — effort S — risk low — category: concurrency
  Why: the TUI, `--task` runs and bench can run at once against one key. Each backs off alone and they then retry in sync. Assumption: only per-call retries exist.
  Done when: three concurrent runs against a stub that returns 429 with `Retry-After: 2` produce at most one request per window across all three, verified in the stub's log.

- **Replay the final verdict from saved evidence in a clean process before closing** — FEATURE — value 4 — effort M — risk low — category: judge purity
  Why: "every claim backed by a check that runs" depends on the judge being a pure function of diff, events and checks. A verdict that is not reproducible from the saved evidence is a hidden state bug.
  Done when: close re-runs the judge in a fresh interpreter on the stored diff and event log and refuses to close on any mismatch, and a test that injects wall-clock dependence fails it.

- **State what containment is real, from probed primitives** — SECURITY — value 4 — effort M — risk med — category: honest sandboxing
  Why: the environment is a hardened kernel, where unprivileged user namespaces are often disabled. Sandbox ideas (bwrap, Landlock, seccomp) would silently degrade there. Assumption: nothing records which primitive was actually available.
  Done when: each run's receipt reads "contained by landlock", "contained by bwrap" or "not contained: guard only", chosen by a probe at start, and a test with the probe stubbed off shows the weaker label.

- **Wild: Slip a known-answer canary slot into the start of every run to detect a swapped model** — FEATURE — value 3 — effort S — risk low — category: model drift
  Why: assumption: any OpenAI-compatible endpoint can be re-pointed or silently route to a different model. The harness trusts the configured name.
  Done when: a stub that answers the canary wrongly makes the run stop with "endpoint answers unlike its profile" before the plan slot is spent.

- **Wild: Cross-check the judge with a second one in POSIX sh and git plumbing** — SECURITY — value 3 — effort L — risk med — category: diverse redundancy
  Why: one Python judge shares its bugs with the code a worker may have touched. A tiny independent implementation catches a class of common-mode failure.
  Done when: a mutation that blinds the Python judge to a hook edit is still caught by the shell judge, and the run closes red.

- **Wild: Show per-endpoint reliability weather from the user's own call history before choosing a runner** — FEATURE — value 3 — effort S — risk low — category: forecasting
  Why: runner choice is by capability, not by recent health. The home screen could show last-24h stall, 429 and truncation rates per runner.
  Done when: seeded history with 40% stalls on one runner shows that runner marked "shaky" in `fm code runners`, and the default skips it.
