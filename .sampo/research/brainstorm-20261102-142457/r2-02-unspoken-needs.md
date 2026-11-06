# Brainstorm — lens: unspoken needs

- **Probe which sandbox primitives this kernel allows** — FIX — value 4 — effort S — risk low — category: safety
  Why: assumption: the host is `linux-hardened`, which typically disables unprivileged user namespaces, so the bwrap/Landlock/overlay ideas on the slate may silently do nothing here. Nobody has asked, because nothing has failed visibly yet.
  Done when: `fm doctor` prints one row per primitive (userns, Landlock, seccomp, cgroup limits) as available or unavailable on this kernel, and any guard feature that depends on an unavailable one says "not enforced" instead of reporting green.

- **Put a verb catalog in every context pack** — FEATURE — value 5 — effort S — risk low — category: grounding
  Why: the user dropped four slate items as "mostly built" (`fm replay`, `fm usage --prune`, `check_predictions`, `check_usage_burn`), and a brainstorm skill fix was needed for the same cause. Tool-less children cannot grep, so the pack should carry the evidence.
  Done when: a generated pack section lists each verb with its help string and last-used date, and a replayed pack for the c16/c21 items shows those verbs in the pack text.

- **Scrub and cap child scratch directories** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: children run in `/run/user/1000/fm-children-1000` on tmpfs, and their packs contain verbatim steers and task text. Pasted secrets can sit there after the child exits. assumption: no scrubber or size cap runs on that directory today.
  Done when: after a child exits its directory is removed or scrubbed, a size cap holds under a stress test, and a planted fake secret in a pack is not found afterwards.

- **Price the cold-read tax per filed item** — PERFORMANCE — value 3 — effort S — risk low — category: lean
  Why: the standing rules put a Haiku read, then a Sonnet read on any non-pass, on every tower file, against a hard $200 budget. The user has stressed "lean", but no number shows what safety checking costs per item.
  Done when: `fm cost` (or the digest) shows dollars and tokens spent on cold reads per filed item and per generation, with a row for the escalation rate from Haiku to Sonnet.

- **Mark each lean claim with the evidence that earned it** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: the user steered that growth without a measurement waits as "pending", yet many subtractions were proposed from reasoning alone (such as "mostly built"). The pending/measured split is not visible at the point of proposal.
  Done when: every subtraction task carries a tag of measured, reasoned or guessed, and `fm next` orders measured ones first.

- **Run the unattended drive as a separate low-privilege unix user** — SECURITY — value 4 — effort L — risk med — category: safety — wild
  Why: assumption: bypass-mode sessions currently have the owner's whole `$HOME`. The user wants the tower to run unattended and "never block on the user", and the strongest limit on that is the OS, not a hook.
  Done when: a drive run as `fm-guest` closes a task in a scratch repo and a planted read of `~/.ssh` from that user fails.

- **Renew the standing mandate monthly** — FEATURE — value 4 — effort S — risk low — category: authority — wild
  Why: the mandate, the push grant ("push to main at any time") and about forty steers are all durable, and none of them expires. The user has never said "stop", but the grant is open-ended.
  Done when: once a month `fm` shows a one-screen summary (pushes made under the grant, steers that fired, what was built) with a default of "continue", and an unanswered prompt is recorded as continue with no escalation.

- **Detect two steers that conflict, and say which one wins** — FIX — value 4 — effort M — risk med — category: steers
  Why: the "never stop for budget or pace" steer, the "lean substance: growth waits" steer, the `--round-first` hold and the "no new maintenance tasks until round 1 is done" steer can all apply to one task. The user has had to restate rules several times.
  Done when: `fm decide --check` flags a pair of active steers whose scopes overlap and whose effects differ, and `fm why T-xxxx` names the winning steer.

- **Score each lean/safe change against a no-change twin** — PERFORMANCE — value 3 — effort M — risk low — category: measurement
  Why: the user steers "selection uses free arms". A safety rule added in mission #12 has no baseline unless a twin run on the same zero-token scenarios exists to compare with.
  Done when: for one mission #12 change, `fm exam` prints scenario results for with and without it, and the delta decides whether the change stays.

- **Warn when a guard rule is allowed by the same session that edits it** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the guard stops commands in bypass mode, but a session may also edit the guard's own rules or the hooks that call it. assumption: no check forbids this today, and the question has not been asked.
  Done when: a test session editing `plugin/lib` guard rules or `hooks.json` is flagged and held for the user, while edits by the user in a normal session are not.

- **Estimate the size of a change before filing it** — FEATURE — value 3 — effort M — risk low — category: lean
  Why: the open list holds about thirty "Later from…" tasks, each a cluster of ideas with no weight attached. The user cannot judge whether to start one without knowing what it adds to the install.
  Done when: each task carries an estimate of added lines, verbs and injected tokens, derived from similar closed tasks, and `fm next` shows it.

- **Run the owner's first-ever install in a fresh container nightly** — SECURITY — value 3 — effort M — risk low — category: install — wild
  Why: the standing rule says `install.sh` must work with no `claude` on PATH, and the owner's machine is the one place it is never retested. Hardened kernels and tmpfs paths are exactly where a fresh install differs.
  Done when: a nightly job runs `install.sh` and `fm doctor` in an empty container and records pass or the first failing row.

Next question: which of the user's accepted defaults (such as "wait out limits", "keep going") has a cost nobody has priced in dollars or hours?
Next question: which parts of the mandate would the user be unhappy to learn Foreman does without asking, and does anything in the pack show how to find them?
