# Brainstorm — lens: bold bets

- **Arm the mail monitor by resume, and prove it** — FIX — value 5 — effort S — risk low — category: liveness
  Why: the pack lists "arming in a live interactive session is unverified (monitors start only in new sessions)". Today, a wake that silently has no listener is the same as idling.
  Done when: SessionStart sends itself a canary mail, and `fm doctor` reports "armed" only after the monitor line reaches the session. If it isn't armed, Foreman offers a `--resume` restart at the same step and falls back to tmux wake until then.

- **Shadow-run compact output, then switch it on from the measurements** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: it is built and measured at ~1.04M tokens per 30 days saved, but off "until the user says yes", so the saving is zero today.
  Done when: in shadow mode the hook records, without rewriting, how often a later Read, grep or rerun re-fetched the full text of an output it would have cut. `fm doctor` then prints one line ("would have saved N tokens, M re-fetches, enable?"), and a single `fm settings` command flips it.

- **Add `fm round`, a recursive-improvement ledger with a scorecard and revert** — FEATURE — value 5 — effort M — risk med — category: observability
  Why: the user steered that "recursively improve" means finish, review, brainstorm, repeat. The "Round 1 shipped today" section had to be written by hand. Nothing records which tasks made up a round or whether it helped.
  Done when: `fm round close` groups the tasks closed since the last round and records before/after numbers (hook p50 from bench, tokens per task, first-pass rate, doctor status). `fm round show` renders that. `fm round revert N` lists the commits to revert, and its generated "shipped" block feeds the next brainstorm pack automatically.

- **Infer idea ticks from what the user does next** — FEATURE — value 4 — effort M — risk low — category: feedback loop
  Why: "nobody has ticked the board yet". Round 2 had to infer taste from drops and steers by hand.
  Done when: after 7 days, each catalogued idea gets kept, dropped or unknown from keyword overlap with the user's later prompts and closed tasks. `fm research list` shows the inferred state, and a manual tick always wins.

- **Track feature escape rate: hotfixes within 24h of the feature** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: round 1 shows fix chains the same day: T-0777 then its monitors.json key test, T-0786 `fm page` hardening, T-0807 and T-0812 follow-ups. That pattern is the signal that review depth is wrong.
  Done when: `fm doctor --round` lists each feature task with the follow-up fixes touching the same files within 24h. The per-tier count feeds the review-depth choice, and a rate over a threshold is shown at plan time for that tier.

- **Convert deferred clusters into evidence-accruing promotions** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: T-0787 to T-0799 are 13 captured "Later" tasks, each with a stated reason for waiting (no incident, needs a per-project server, mod update blocked). Today someone must remember to reopen them.
  Done when: each deferred task carries a trigger and a counter, for example "supply chain: promote on first guard-detected pipe-to-shell from a fetched file" or "LSP: a project with a running server". `fm tidy` bumps the counters and promotes a task to `planned` with the evidence attached once its trigger is met.

- **Write a by-design register the guard and intake consult** — CLEAN — value 4 — effort S — risk low — category: guard
  Why: the dropped items (heredoc `$_` args, delta reads, test-folder prove) each carry a "by design: …" reason that exists only as free text. The guard's refusal text for those cases can't cite it.
  Done when: `fm decisions` stores the reason keyed to a guard rule id or a request pattern. The same request later gets "declined before: <reason>, evidence <task>" at intake, and a guard refusal on that rule prints the reason.

- **Reinvest measured savings as review effort (wild)** — FEATURE — value 3 — effort M — risk med — category: cost
  Why: compact output, `--affected` checks and the effort routing all save tokens, but the savings show up only as a smaller bill.
  Done when: a per-week "token dividend" is computed from the ledger, and the user can opt in to spending up to X% of it on a higher effort level for the reviewer on M tasks. The close-out line shows the spend and whether the review found anything it otherwise would not have.

- **Run a Foreman wire: a local API gateway for true token truth and wire-level compaction (wild)** — FEATURE — value 4 — effort L — risk high — category: privacy
  Why: today token claims are "measured over 30 days" from transcripts. A loopback proxy (`ANTHROPIC_BASE_URL`) would see real request sizes, cache hits and the cost of each hook's injected text, and could compact any tool result, not just Bash.
  Done when: `fm wire on` starts a local-only proxy that logs sizes and cache-read ratios without storing any prompt text. `fm doctor` shows the cache-hit rate. Turning it off restores direct calls with no residue, and no outbound traffic goes anywhere but the API endpoint.

- **Hardening-debt futures: predict the next hotfix (wild)** — FEATURE — value 3 — effort M — risk med — category: reliability
  Why: the recent commit list is mostly guard and page fixes (path-only ids, home-path spellings, heredoc cases). Bug classes cluster by file, and nothing uses that clustering before a feature ships.
  Done when: before close, a child reads the diff plus the last N hotfix classes for the touched files and writes 3 probes of the same class (spelling variants, quoting, unusual path forms). Each probe runs as a test, and a failure blocks close.

- **Offer a one-line "what changed for me" on every round close** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: round 1 shipped about 15 behaviours, but only things like the compact-output opt-in need a user decision. The rest are invisible.
  Done when: `fm round close` prints at most 5 lines in plain words: what you can now stop doing, what needs one yes, and what got safer. Each line links to its task id.

- **Make the `fm page` board answer back through a local tick file** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: `fm page` renders the board for an Artifact, but ticking requires a round trip through the page, and the pack says no tick has happened.
  Done when: the rendered page includes the exact one-line `fm research tick T-… keep|drop` command for each idea, and a pasted batch of those lines is applied atomically. The result is verified by a test that round-trips the page output.

- **Detect Stop-hook overload and split the verdict** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: Stop now carries the drive, the done-gate and the single PushNotification ask added in round 1, so one hook does three jobs.
  Done when: bench reports Stop p50 and p95 per sub-job, and a regression over 20% fails the existing hook bench gate.
