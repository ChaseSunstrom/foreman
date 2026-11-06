# Brainstorm — lens: the outside world (invented): research, docs, ops and incidents, infra, data, design and releases held to code's standard of proof

- **Pin every external fact to a dated, re-fetchable source** — FEATURE — value 5 — effort M — risk low — category: research proof
  Why: the pack lists "citation gate for research" and "pin external facts" only as one-liners; none specifies the mechanism. Research and docs tasks close on prose. Mechanism: a `fm prove --source URL --quote "…"` record stores the URL, fetch date, content hash and the quoted span. `fm doctor` re-fetches on a schedule and flags drift (404, changed hash, quote gone) as "stale source", not as failure.
  Done when: a task citing a URL whose page later drops the quoted text shows up in `fm unproven` as "source drifted" with the old and new hash.

- **Close an incident only on a replayed signature** — FEATURE — value 5 — effort M — risk med — category: ops proof
  Why: ops and incident tasks are named in Mission 7 #10 but T-2273/2284/2303/2288 cover only unproven rollup, perf and data. Mechanism: an incident task captures the failure signature (log line regex, exit code, metric threshold) at open. Closing needs the signature absent over a user-set window, plus a replay of the original trigger on the fixed tree where possible.
  Done when: closing an incident task whose stored signature still appears in the supplied log sample is refused with the matching line quoted.

- **Run infra changes as plan, apply to scratch, re-plan to empty** — FEATURE — value 4 — effort L — risk med — category: infra proof
  Why: the seed row names "infra" as a proof kind with nothing built. It parallels the migration proof (T-2288), which already does up/down/up on a throwaway copy. Support terraform, docker compose, systemd units and shell installers, with the scratch target a container or a `--root` directory. The record carries the diff and the idempotence result.
  Done when: an infra task whose second apply still changes something records "not idempotent" with the diff and cannot close as proven.

- **Extract numbers and commands from docs and execute them** — FEATURE — value 5 — effort M — risk low — category: docs proof
  Why: the standing rule is "docs against code", and the README and MASTER.md carry many concrete claims (counts like "2058 files", command names, flags). A doc claim extractor lists each fenced command and each `fm X` mention. It runs `--help` or dry-runs each and checks that every flag exists. Counts are recomputed.
  Done when: renaming a flag in code makes `fm prove --docs` fail naming the doc file and line that still shows the old flag.

- **Prove a release by installing the built artifact cold** — FEATURE — value 4 — effort M — risk low — category: release proof
  Why: `cc-plugin-release` is a stack card, and install.sh is a headline claim ("works with no claude on PATH"). Build the release tarball, unpack it into an empty directory with a stripped PATH, and run `fm doctor` plus the first-use path. Record a pass or fail with the manifest hash.
  Done when: removing a file from the release manifest makes the cold-install proof fail naming the missing file.

- **Mark each proof with who could have lied** — CLEAN — value 4 — effort S — risk low — category: trust labels
  Why: the earlier question "which verbs have a model on both sides with no user-owned check" is unanswered. Label each evidence record as `ran` (a command's exit), `measured`, `model-judged`, `typed` or `user-attested`. The unproven rollup then splits by label, not just a count.
  Done when: `fm unproven` prints a per-label count, and a task closed on a model-judged record appears under it.

- **Gate a design task on a rendered check** — FEATURE — value 3 — effort M — risk low — category: design proof
  Why: `fm shot` and `fm flow` exist, but the unproven rollup only counts UI changes without a visual check. It never asks whether the shot was compared to anything. Add a spec-linked check: contrast ratios from the pixels, a tab-order walk from `fm flow`, and a pixel diff against a stored baseline with a budget.
  Done when: a change that drops a text contrast below 4.5:1 fails `fm prove --design` with the measured ratio.

- **Give each data task a golden sample that guards later changes** — FEATURE — value 4 — effort M — risk low — category: data proof
  Why: T-2288 proves a migration once. Data pipelines and transforms need a fixed input and output hash, kept with the task and re-run by `fm check` thereafter, so a later edit that changes the output is flagged.
  Done when: editing a transform so one row differs makes the next `fm check` fail naming the golden file and the first differing row.

- **Expire a proof by its dependency, not its age** — FEATURE — value 4 — effort M — risk low — category: proof decay
  Why: "stale proof expiry" was proposed by age alone. A proof is better tied to what it touched: the files, URLs, the toolchain version and the dependency lockfile hash. When one changes, the proof goes "needs re-run" and only then.
  Done when: bumping a lockfile entry flips the one proof that recorded it to "needs re-run" and leaves the others green.

- **Wild: Fire drill — run the runbook** — FEATURE — value 4 — effort L — risk med — category: ops proof
  Why: wild. Docs for recovery (restore, rollback, key rotation) are never executed. A `fm drill` takes the runbook's fenced steps, runs them in a scratch copy after deliberately breaking something, and reports which steps failed or were missing. Assumption: the runbook is written as runnable fenced blocks.
  Done when: a runbook with one wrong path ends the drill reporting that step number and the error.

- **Wild: A claims manifest a stranger can re-verify offline** — FEATURE — value 4 — effort L — risk low — category: release proof
  Why: wild. Every release ships `claims.json`: each public claim (README, site stats, the exam score), its checking command, its pinned inputs and its last result. A stranger runs one command with no network and gets verified, failed or unverifiable per claim.
  Done when: editing a number in the README after release makes the offline verify list that claim as failed.

- **Wild: Prosecutor for the "unprovable" bucket** — FEATURE — value 3 — effort M — risk med — category: unproven
  Why: wild. Claims that cannot be proven are only labelled unproven. A separate tool-less child, given only the claim and not the code, proposes the cheapest observable check that could have proven each, and files the best as a task. This turns the label into a worklist.
  Done when: each claim in `fm unproven` has either a filed candidate check task or a recorded reason none exists.

- **Check the numbers the site shows against the command that makes them** — FIX — value 4 — effort S — risk low — category: site proof
  Why: the user asked "make sure the website is updated, it doesn't look like it has been", and T-2326 refreshes stats daily, but nothing checks the shown figure against its source. Each published stat records its producing command and a time. A check fails when the page value differs from a fresh run.
  Done when: hand-editing a stat in `site/genesis` data makes the check fail naming the stat and both values.

- **Wild: Run a nightly "claims audit" lane and post only the diffs** — FEATURE — value 3 — effort M — risk low — category: continuous proof
  Why: wild. A scheduled lane re-runs the source, docs, release and golden-sample checks, and says nothing when all is unchanged. Only a changed result reaches the user, as one line.
  Done when: a lane run with no changes writes no user-facing message, and one with a drifted source writes exactly one line.

Next question: Which of the proof kinds can be wrongly passed by a task that never touches the thing being proven, and what planted fault would show it?
Next question: When two evidence labels disagree about the same claim (a command passes, a model says no), which one does the closing verb trust, and does the user see the disagreement?
