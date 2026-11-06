# Brainstorm — lens: approaches

- **Enforce the core gates in plain git hooks** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: the Codex, Gemini and opencode adapters are unverified (T-0335, T-0336, T-0337) and `fm code` is blocked (T-1207). Git is the one surface every agent shares, so a pre-commit/pre-push hook that checks for a task, proof and scope would cover them all. The trade-off is that it fires at commit time, later than the Claude hook.
  Done when: in a fixture repo, a commit made outside Claude Code with no focused task or proof is refused with a next-step line, and `fm doctor` reports the hooks installed.

- **Cap the share of Foreman-on-Foreman work** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: all ten recent commits (T-1964 to T-2001) fix Foreman's own gates, ambient runs, intake and titles. Doing less internal work is a valid way to improve it. The cap should come from `fm status` data, with no new gate.
  Done when: `fm status` prints the fraction of the last 20 closed tasks that touched protected core, and the loop brief requires a user-facing task once that fraction is above a configured limit.

- **Show a permission diff on every plugin upgrade** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: assumption: the pack shows no upgrade review, and T-0791 only parks injection and supply-chain ideas. Upgrades add hooks, allowed tools, commands and network use, so a mobile-style "what's new in permissions" prompt fits here.
  Done when: upgrading a fixture from version A to B lists the added hooks, commands, tools and hosts, and an added hook needs explicit accept.

- **Tier proof verification by model cost** — PERFORMANCE — value 3 — effort M — risk med — category: cost
  Why: assumption: verification today costs the same on every task. A `claude-haiku-5-5` pass that reads each proof claim against the command output, escalating to a bigger model only on doubt, would cut cost. The trade-off is a cheap model missing subtle forgery.
  Done when: a fixture task with a fabricated proof is flagged by the cheap tier, and each close logs which tier judged it.

- **Compile the guard hook to a static binary** — PERFORMANCE — value 3 — effort L — risk med — category: hooks
  Why: `bench_hooks.py` is a standing gate, so hook latency clearly matters. A daemon (already proposed) adds lifecycle problems. A compiled binary only removes interpreter start-up, and the Python hook stays as fallback.
  Done when: `bench_hooks.py --runs 20` shows the binary's median at least 3x lower than Python's, and removing the binary falls back to Python with the same verdicts.

- **Sync task state across machines through a git ref** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: assumption: the web UI and desktop app are used from more than one machine. A `refs/foreman/state` ref moves the queue and proofs with the repo, and a ref avoids a server and keeps data local.
  Done when: after `fm sync` on machine B, the queue and open task from machine A appear, and a concurrent edit is reported as a conflict, not overwritten.

- **Run one lens per round on a different model family** — FEATURE — value 3 — effort M — risk low — category: brainstorm
  Why: assumption: this idea list is large and repetitive (many near-duplicates), the sign of one model's monoculture. A second vendor through an adapter would add different failure modes, and per-lens keep-rate (T-0829) would show whether it pays.
  Done when: a round records which model produced each idea, and `fm ideas` shows keep-rate per model.

- **Add a "reasons to uninstall" lens** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user's steers and drops are mostly about friction and idle time (never-idle design, mid-word titles, suite overlap). A pre-mortem lens makes that the stated goal, where the current lenses only add features.
  Done when: a round includes a lens whose output is ranked friction points, each tied to a steer or drop in the pack.

- **Generate the command reference and error catalog from code** — CLEAN — value 2 — effort S — risk low — category: developer experience
  Why: assumption: help text, docs and the site drift (the docs-impact blocker exists for this reason). Generating from the source removes a class of docs tasks.
  Done when: the site's command page matches `fm help` output exactly, and a test fails when they differ.

- **Wild: N-version the task lifecycle** — FEATURE — value 3 — effort L — risk low — category: correctness
  Why: wild. A second model writes an independent task-close implementation from the written spec, and both are fuzzed with the same inputs. Disagreements are either bugs or undocumented rules, which is the class behind the steered `_theirs` scope gap.
  Done when: a differential run reports at least one disagreement list, and each entry becomes a test or a doc line.

- **Wild: Pit each release against its three predecessors** — PERFORMANCE — value 3 — effort M — risk low — category: duel
  Why: wild. The duel (T-1231) compares Foreman to plain Claude, but regressions between Foreman versions are the real risk. Old releases as opponents on the user's replayed asks give a monotonic progress check.
  Done when: a release candidate is held when it loses to its predecessor on the replay corpus, with the losing tasks listed.

- **Wild: Publish an opt-in read-only idea board** — FEATURE — value 2 — effort M — risk med — category: community
  Why: wild. The demo and site already exist. Visitors upvoting the "Later from…" backlog would supply demand evidence the pack lacks (T-0862 to T-0869 wait on "evidence of use"). Off by default, since it publishes data outward.
  Done when: with the setting off nothing is sent, and with it on the board shows only titles the user marked public.

- **Track competitor releases and turn gaps into captures** — FEATURE — value 3 — effort M — risk low — category: research
  Why: assumption: the capability map is built from memory. A setting-gated `fm radar` would diff public changelogs of comparable agent tools against Foreman's command list and capture the gaps as tasks.
  Done when: running `fm radar` on a saved changelog fixture produces captures with source lines, and without the network setting it makes no request.
