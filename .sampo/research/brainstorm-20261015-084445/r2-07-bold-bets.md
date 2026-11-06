# Brainstorm — lens: bold bets

- **Earn the allowlist instead of defaulting to bypass** — SECURITY — value 5 — effort M — risk med — category: trust
  Why: newcomer evidence A2 says a default install sets `bypassPermissions` plus 20 deny rules. Second-order on "make bypass opt-in": install in normal mode and mine the user's last 30 days of approved Bash and edit prompts. Propose a project-scoped `permissions.allow` list, with every entry showing how many times it was approved. Bypass is offered only after N clean days. Assumption: past approvals are readable from transcripts.
  Done when: in a clean HOME with a seeded transcript of 40 approvals, `fm wire --plan` prints an allowlist with counts, and the install leaves `defaultMode` unchanged.

- **Ship a three-rung install ladder with state-preserving upgrades** — FEATURE — value 5 — effort M — risk low — category: adoption
  Why: rivals are one marketplace command that adds commands without rewriting `~/.claude`. Foreman is 108 verbs with a heavy wiring step. Rung 1, `foreman-gate`, is three hooks that block "done" without evidence and touches no settings. Rung 2 is core: capture, queue, resume. Rung 3 is full. `fm upgrade` moves up a rung and keeps tasks and ledger.
  Done when: `/plugin install foreman-gate` in a clean HOME blocks an evidence-less done claim with zero `~/.claude` edits, and `fm upgrade core` keeps a pre-existing task.

- **Turn the 18 "fixed later" tasks into the first real bench** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the bench has 1 case and 3 court cases at 0/3, with no published evidence. The ledger holds 18 labelled escapes (2.6% of 688) with the original brief, the start tree and the later fix. Replay each as a fail-to-pass case with the gate on and off. This seeds T-0035 with ground truth instead of synthetic cases.
  Done when: `fm bench run --from-escapes` runs 18 cases twice each (gate on and off) and prints the catch counts.

- **Mirror tasks with GitHub Issues, posting evidence as comments** — FEATURE — value 4 — effort M — risk med — category: integrations
  Why: CCPM and Task Master use issues as the audit trail, and the survey lists GitHub/Linear sync as a gap. Each task maps to an issue. Label sets the type. Close-out posts a digest comment (criteria, evidence, commit). Closing the issue marks the task done only if its evidence holds. This is outward-facing, so it needs an explicit per-repo opt-in and the secret scrubber on the comment body.
  Done when: against a fixture repo (mocked `gh`), `fm task finish` posts one comment containing the evidence digest and the redaction test passes.

- **Attribute every `fm` verb call to its caller (Claude, human or hook)** — CLEAN — value 4 — effort S — risk low — category: simplification
  Why: the audit says 46 of 108 verbs were never run by Claude in 11 days. It also warns that some are verbs the user runs by hand, such as the desktop app and JARVIS mail. Deleting or merging from Claude-only counts could break the user's own workflow. Stamp the caller on each invocation and make `fm help --all` and the merge plan read the split.
  Done when: after a mixed session, the census lists each verb with separate claude, human and hook counts, and the planned `fm inspect` merge lists only verbs with zero human use as safe to hide.

- **Add stack presets with fixture repos for ten ecosystems** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: A7 says `fm check` with no gates does not detect unittest or pytest, and `fm repeats` suggests single test modules as gates. Ship a preset table (pytest, unittest, jest/vitest, cargo, go, gradle/maven, dotnet, make, mix, bundler) that detects the runner, a fast gate and a full gate. Each preset is tested against a tiny fixture repo, so detection is verified rather than guessed.
  Done when: for each of the 10 fixtures, `fm check --init` writes the correct gate and a first run goes green.

- **Rank gate-verifier packs from a registry with sandboxing and scorecards** — FEATURE — value 4 — effort L — risk med — category: ecosystem
  Why: ECC and agent-os grow by contributions, while Foreman's lenses and gates are all in-house. Define a small verifier contract: input is a diff and the task, output is pass, fail or not-evaluated plus a reason. Install packs with `fm gate add`. Run them in the existing sandbox with no network by default. Show each pack's catches and false positives from the ledger next to its name. Assumption: three-valued verdicts exist or are cheap to add.
  Done when: a sample a11y pack installs, runs sandboxed on a fixture diff, and `fm gate list` shows its fire count.

- **(wild) Approve a yes/no by replying to an SMS or email** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: assumption: many asks arrive when the user is away from the terminal. Reuse the `fm ask` pending-question ids and bind each reply to one id with a short nonce. The user supplies their own SMTP or ntfy-style endpoint, so nothing goes to any service Foreman picked. Replies are treated as untrusted input and are parsed only as Y, N or a default.
  Done when: a mocked inbound "Y 7f3a" resolves exactly one pending ask, and a replayed or mismatched nonce is rejected.

- **(wild) Run a public "forge a done" challenge that feeds the bench** — SECURITY — value 4 — effort M — risk med — category: proof
  Why: no one has shown the gate cannot be faked, and "regression shop" ideas were never built. Publish a fixture repo and a task. Anyone can try to get Foreman to accept a false done by gaming the evidence. Each successful forge becomes a permanent failing case and a gate fix, and the results table goes on the proof page. Assumption: the gate can be run headlessly with no model calls on submitted transcripts.
  Done when: submitting a recorded forged transcript to `fm bench forge` returns accepted or refused, and one known forge is closed with a regression case.

- **(wild) Race lean, standard and strict profiles on your own idle tasks** — FEATURE — value 4 — effort L — risk med — category: personalisation
  Why: rivals ship profiles (ECC) but pick them blindly. The user's own finished S and M tasks can be replayed in worktrees at idle under each profile. The comparison is cost, wall time and verdict, and the default profile is set from that table. Uses cheap cap flags (`--max-budget-usd`) already shipped.
  Done when: `fm profile race --last 5` prints a three-row table of tokens, minutes and pass/fail per profile, and `fm profile set --from-race` changes the default.

- **Replace the first-run `fm doctor` failure with a one-line verdict** — FIX — value 4 — effort S — risk low — category: first run
  Why: A8 says a fresh install fails its own doctor (missing backup) and prints 40 lines of passes. The first-run doctor should return a single line: green, or the first failing check with its fix command. A missing backup on a project with no state yet is not a failure. The full report stays behind `--all`.
  Done when: in a clean HOME after install, `fm doctor` exits 0 and prints one line.
