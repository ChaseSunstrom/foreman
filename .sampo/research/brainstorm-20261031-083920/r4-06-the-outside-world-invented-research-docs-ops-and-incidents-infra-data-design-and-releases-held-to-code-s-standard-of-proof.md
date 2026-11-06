# Brainstorm — lens: the outside world (invented): research, docs, ops and incidents, infra, data, design and releases held to code's standard of proof

- **Replay the incident from its signature** — FEATURE — value 5 — effort M — risk med — category: ops
  Why: the pack has "close an incident task only on a replayed signature" as a one-liner, but no mechanism. Assumption: incidents leave a log line, exit code or metric snapshot that can be stored at open.
  Done when: `fm task new --incident` stores the failing signature, and `fm task finish` refuses until a replay command shows the signature absent and a control run shows it can still be detected.

- **Run the runbook as a script in a scratch environment** — FEATURE — value 4 — effort M — risk med — category: ops
  Why: docs and runbooks are proved only by reading. Assumption: runbook steps are fenced shell blocks that can be tagged `fm-run`.
  Done when: `fm prove --runbook docs/ops.md` executes tagged blocks in a throwaway directory and records which step failed and which were skipped as unrunnable.

- **Give each external fact a freshness date and a source hash** — FEATURE — value 4 — effort M — risk low — category: research
  Why: research tasks and docs lean on outside claims (versions, pricing, API behaviour) that change after the task closes. Assumption: facts can be cited as URL plus a fetched-content hash.
  Done when: `fm facts check` re-fetches pinned sources, lists those whose hash changed, and each listed fact names the tasks that relied on it.

- **Diff infra plan against intent before apply** — FEATURE — value 4 — effort M — risk med — category: infra
  Why: a seed row lists infra proof; the pack has no way to tell "plan is empty after apply" from "plan touched what the user meant". Assumption: terraform, compose or k8s dry-run output is available.
  Done when: the infra proof records the planned resource diff, flags resources outside the task's scope paths, and fails a task whose dry-run touches an unlisted resource.

- **Hash a data task's golden sample and guard it** — FEATURE — value 4 — effort M — risk low — category: data
  Why: T-2288 proves migrations up/down/up, but a migration that silently drops rows still passes. Assumption: a small sampled fixture can be stored per table.
  Done when: after the migration round trip, row counts and a checksum of the sampled rows match the pre-migration values, and a planted row loss makes the proof fail.

- **Check a release by installing the built artifact fresh** — FEATURE — value 5 — effort M — risk low — category: releases
  Why: ship is gated by the suite run in the source tree, which can't catch a missing packaged file. Assumption: the project builds a wheel, tarball or install.sh target.
  Done when: `fm prove --release` builds, installs into an empty directory with no repo on the path, runs `fm doctor` there, and fails when a planted file is left out of the manifest.

- **Gate design tasks on a rendered accessibility check** — FEATURE — value 3 — effort M — risk low — category: design
  Why: UI proof is `fm shot` and a look; contrast, tab order and reduced-motion are checkable by machine. Assumption: the web UI renders headlessly.
  Done when: `fm shot --a11y` records contrast ratios and tab order for the page, and a deliberately low-contrast change fails the criterion.

- **Prove the docs' CLI examples against the shipped help** — FEATURE — value 4 — effort S — risk low — category: docs
  Why: "docs against code" is a stated mission item, and flags drift (the plan-gate bug on a flag-led option shows how). Assumption: examples are in code fences beginning with `fm `.
  Done when: every `fm` line in README and MASTER.md is parsed, its verb and flags matched to the real argparse table, and a renamed flag in a fixture doc is reported with a file and line.

- **Mark an outside dependency each proof relied on** — FEATURE — value 3 — effort S — risk low — category: proof
  Why: a green that rests on a network service, a clock or a vendor model should be labelled differently from a local one. Assumption: the evidence record can carry a tag.
  Done when: the unproven rollup prints a "relies on outside" count, and a proof that called a network address is tagged with it.

- **Scan the closed-task log for claims in post-incident notes** — CLEAN — value 2 — effort S — risk low — category: ops
  Why: incident write-ups promise action items that nobody tracks. Assumption: a postmortem has a list of "will do" lines.
  Done when: each action line becomes a task or a recorded "not doing" with a reason, and a postmortem fixture with 3 actions yields 3 entries.

- **Wild: Run a fire drill that breaks something on purpose** — FEATURE — value 4 — effort L — risk high — category: ops
  Why: wild. A runbook is only true if someone has followed it under failure. Assumption: a throwaway copy of the environment is safe to break.
  Done when: the drill breaks a scratch service, a cold child follows only the runbook, and the report says whether service came back.

- **Wild: Ship a claims manifest with every release** — FEATURE — value 4 — effort M — risk low — category: releases
  Why: wild. A release note says "faster", "safer", "fewer bugs" with nothing a stranger can rerun. Assumption: each claim maps to a stored command and a result.
  Done when: `claims.json` in the release lists each claim with its command and measured output, and a stranger running `fm claims verify` offline gets the same verdicts.

- **Wild: Let a design spec fail a build** — FEATURE — value 3 — effort L — risk med — category: design
  Why: wild. A design is usually judged by eye; a token file (spacing, colour, type) could be the spec the page is diffed against. Assumption: the web UI uses tokens that can be read back from computed styles.
  Done when: a page using a colour outside the token file fails `fm prove --design` and names the element.

- **Cap how long a proof can be trusted when its world moves** — FEATURE — value 3 — effort M — risk low — category: proof
  Why: infra and research proofs go stale when the external state changes, not with time. Assumption: each proof can name a state fingerprint (versions, hashes).
  Done when: changing a pinned tool version makes the rollup list the proof as stale, and unchanged inputs keep it fresh.

Next question: Which of these outside-world proofs can run with no network and no secrets, so they work for the privacy-minded user by default?
Next question: When a proof depends on something Foreman can't touch (a cloud account, a vendor dashboard), what is the honest label, and who is allowed to accept it?
