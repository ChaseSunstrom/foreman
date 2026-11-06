# Brainstorm — lens: deepen: self-improvement

- **Close the loop on learned fixes with a Fix Ledger (`fm fixes`)** — FEATURE — value 5 — effort M — risk low — category: self-improvement
  Why: T-1032 records obstacle→fix pairs and offers them next time, but nothing measures whether an offered fix worked. The pack lists "score each hint by outcome" three times in different words, so merge them into one ledger. Each fix carries offered, accepted, first-time-pass and regressed counts. Fixes that stop helping drop out of the offers.
  Done when: a test seeds a fix offered 5 times with 0 passes, runs `fm fixes prune`, and the fix is marked retired and no longer injected, while a 5-for-5 fix is kept.

- **Fingerprint obstacles so repeats are recognised by shape, not text** — FEATURE — value 5 — effort M — risk med — category: obstacle matching
  Why: "Detect repeat obstacles" needs a stable key. Normalise the failing command, the exit code and the stderr tail, stripping paths, pids and timestamps. The key then matches the same trust-prompt stall or missing-`claude` failure across projects. Assumption: today's hints match on free text.
  Done when: two failures differing only in tmp paths and pids produce the same fingerprint, and a different error produces a different one.

- **Pre-empt known obstacles in a PreToolUse step, before the model tries anything** — FEATURE — value 5 — effort M — risk med — category: hooks
  Why: the user asked for "go that path in future with similar issues". When a command's fingerprint matches a high-confidence fix, a hook applies the fix or rewrites the command (for example adding `~/.local/bin` to PATH) and logs that it did. Low-confidence matches stay advisory.
  Done when: a recorded PATH fix is applied automatically to a repeat run in a test, the ledger logs "pre-empted", and a low-confidence fix only prints a hint.

- **Ship fixes as a git-tracked `.foreman/fixes/` pack with provenance and a merge-friendly format** — FEATURE — value 5 — effort M — risk med — category: portability
  Why: the user steered "fixes must travel with git: project fixes in the repo, machine-wide ones in Foreman state". Use one file per fix, keyed by fingerprint, so merges rarely conflict. Each file records its origin task, an evidence count and a scope field (project or machine). Stats stay local in a sidecar, so git diffs hold only the fix itself.
  Done when: a fresh clone with only `.foreman/fixes/` committed offers the fix on a matching failure, and two branches adding different fixes merge with no conflict.

- **Promote fixes up a ladder: hint, then rule or hook, then regression test** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: this folds in "propose a permanent fix" and "auto-drafted regression test". A fix that has worked N times earns a proposal for a path-scoped rule (T-0789). If the root cause is in Foreman, it gets a drafted failing test. The user approves each promotion.
  Done when: a fix with 3 confirmed passes yields a proposal file containing a rule diff and a test stub, and nothing is applied without `fm fixes accept`.

- **Mine the transcript for corrections and repeated requests (`fm learn`)** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: "steered" and "dropped" entries already exist in the pack, but they only feed a prompt. Detect when the same request or correction recurs, and propose a standing rule or a task, with the user's wording kept verbatim. This also covers the "third time" wild idea.
  Done when: three similar corrections across sessions produce one proposed rule that quotes them, and rejecting it stops that cluster from being proposed again.

- **Rank Foreman's own roadmap by evidence (`fm next --why`)** — FEATURE — value 4 — effort S — risk low — category: prioritisation
  Why: more than 25 deferred "Later from T-…" tasks sit in the queue unranked. Score each by user corrections touching it, minutes lost to related obstacles and fix-ledger hits. Surface the top three with the numbers.
  Done when: `fm next --why` prints a score breakdown per deferred task, and a test shows an obstacle on task X's area raising X's rank.

- **Measure improvement with an A/B holdout (`fm improve`)** — FEATURE — value 4 — effort L — risk med — category: evaluation
  Why: the user asked "why have you not really improved all that much?", and nothing currently answers it. Replay captured cases (T-0035) with and without a candidate fix or rule, N times, and report pass rate, turns and tokens. Only changes that win get merged.
  Done when: `fm improve` on a seeded case outputs a before/after table and refuses to promote a change with no measurable gain.

- **Show a visible improvement scoreboard in the pane** — FEATURE — value 3 — effort S — risk low — category: UI
  Why: the user wants to see progress ("show how many complete vs left"). Show obstacles hit, repeats pre-empted, minutes saved (estimated) and fixes retired this week, with a trend sparkline.
  Done when: the pane shows a Learning section from ledger data, which is hidden when empty and fits the dock without overflow.

- **Wild: Run a nightly dojo that replays recorded obstacles in throwaway worktrees** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: wild. Each stored obstacle becomes a reproducible scenario. Overnight, a headless sandbox replays it against the current Foreman and flags fixes that no longer work after upgrades. Failures open tasks. Assumption: obstacles can be captured as replayable scripts, and the nightly cloud routine from T-0793 can host the run.
  Done when: breaking a fix on purpose makes the next dojo run file a task that names that fix.

- **Wild: Ship a public, signed fix exchange between Foreman installs** — FEATURE — value 4 — effort L — risk high — category: community
  Why: wild. Opt-in sharing of anonymised fingerprint→fix pairs, with scores merged across users. A new user starts with the community's solved obstacles, such as the folder-trust stall. It needs signing and review because it is a supply-chain surface (T-0791). Assumption: privacy is satisfied by sharing fingerprints only, with no code or paths.
  Done when: `fm fixes import <pack>` rejects an unsigned pack, installs a signed one as advisory-only, and shows its provenance.

- **Wild: Let a fix fork per project dialect (the same error resolves differently in different repos)** — FEATURE — value 3 — effort M — risk low — category: self-improvement
  Why: wild. The same fingerprint may need different fixes on Arch with a native install versus Ubuntu with a pip install. Key the fix variants by environment signature (OS, install type, stack cards) and pick the best match, falling back to the general one.
  Done when: two variants for one fingerprint exist, and a test on each simulated environment picks the correct variant.

- **Add a "why did this fix fire" receipt** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: automatic behaviour needs auditing, and the research shows users want audit logs of multi-agent runs. Every applied or offered fix writes a one-line receipt with the fingerprint, the evidence and the undo command.
  Done when: after a pre-empt, `fm fixes why` prints the receipt and `fm fixes undo` reverts the change.
