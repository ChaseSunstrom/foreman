# Brainstorm — lens: the outside world (invented): research, docs, ops and incidents, infra, data, design and releases held to code's standard of proof

- **Close an incident only on a replayed signature** — FEATURE — value 5 — effort M — risk med — category: ops proof
  Why: Open work and seed row name "ops and incidents" as a proof kind with none built; T-2288 shows the pattern (run, don't claim). Assumption: incident tasks carry a log line, metric or error text captured at open.
  Done when: `fm task finish` on an incident-kind task refuses unless `fm prove --incident` replays the stored signature against the fixed tree (or a recorded fixture) and shows it absent, with the failing-before run stored.

- **Run a docs claim extractor against the shipped CLI** — FEATURE — value 5 — effort M — risk low — category: docs proof
  Why: Seed row says "docs against code"; README and MASTER.md quote flags, verbs and numbers. Earlier ideas proposed it, none is built beyond T-2273/2284/2303/2288.
  Done when: `fm prove --docs README.md` executes every fenced `fm ...` command with `--help`/dry-run and every quoted flag, and exits non-zero naming the line of a verb or flag that doesn't exist (tested with a planted stale flag).

- **Pin research claims to dated, hashed sources** — FEATURE — value 4 — effort M — risk med — category: research proof
  Why: "Research" is named in Mission 7 #10, with no proof kind. Rival-plugin imports (T-0869) and frontier digests rest on web claims. Assumption: fetches happen in a user-allowed step.
  Done when: a research note's claims each hold URL, fetch date, content hash and a quoted span; `fm prove --research` re-fetches and reports drifted or missing quotes; an unquoted claim is labelled unproven.

- **Prove infra by plan, scratch apply, empty re-plan** — FEATURE — value 4 — effort L — risk med — category: infra proof
  Why: Mirrors the migration kind (T-2288: up, down, up on a throwaway copy). Assumption: users have terraform/compose/systemd-style configs; kind detected from manifests and stack cards.
  Done when: `fm prove --infra` runs the repo's plan or validate tool, applies to a scratch target (container or tmp root), re-plans to an empty diff, and records the diff; if no scratch target exists it records "unproven: no scratch target".

- **Release proof from the built artifact** — FEATURE — value 5 — effort M — risk low — category: release proof
  Why: Repo ships `install.sh` and a plugin marketplace (cc-plugin-release card); T-2326 shows the site drifted unnoticed. Assumption: release builds an archive.
  Done when: `fm prove --release` builds the artifact, installs it into an empty dir/venv with no repo on PATH, runs `fm doctor` and the first-use path, and records the exit codes; a missing file in the package fails it (planted-omission test).

- **Check every published number against its producing command** — FIX — value 4 — effort S — risk low — category: site truth
  Why: User asked "make sure the website is updated, it doesn't look like it has been" (T-2326); open question "which numbers have never been checked by someone other than the code that produced them".
  Done when: each stat in `site/genesis` data carries a `produced_by` command; `fm doctor` re-runs them and flags any value off by more than its tolerance, shown on the site as a stamp with date.

- **Add a design proof: contrast, tab order, and screenshot diff vs spec** — FEATURE — value 4 — effort M — risk low — category: design proof
  Why: `fm shot`/`fm flow` exist but the unproven rollup counts "UI changes with no visual check", with nothing checking what the screenshot shows. Assumption: a reference image or token file exists.
  Done when: `fm prove --design` fails on a planted low-contrast colour and a broken tab order in the web UI template, and passes the clean tree.

- **Write a runbook as an executable file** — FEATURE — value 4 — effort M — risk med — category: ops docs
  Why: Docs and ops are in scope; recovery steps (baton/ledger/repo disagreement after a kill) are prose nobody runs. Assumption: runbooks live in MASTER.md or docs/.
  Done when: `fm runbook run NAME --scratch` executes each step in a throwaway copy, checks each step's stated expectation, and reports the first step whose result differs from the prose.

- **Wild: Fire drill the runbooks** — FEATURE — value 4 — effort L — risk med — category: ops chaos
  Why: wild — kills a session, corrupts the ledger, fills the disk in a scratch state dir, then follows only the written recovery steps via a cold child and scores whether it recovered.
  Done when: `fm drill` produces a per-scenario pass/fail with the cold child's transcript, run on a throwaway copy only.

- **Wild: Give each release a claims manifest a stranger can re-verify** — FEATURE — value 4 — effort M — risk low — category: release trust
  Why: wild — each release lists "claim → command → expected output → witness class", signed by hash, rerunnable offline with `fm verify manifest.json`.
  Done when: a fresh machine with only the release archive reproduces every non-network claim, and a tampered entry fails by name.

- **Wild: Golden-sample guard for data tasks** — FEATURE — value 3 — effort M — risk low — category: data proof
  Why: wild — extends T-2288 beyond schema; a task that transforms data stores a redacted sample and its expected output, so later changes that alter it fail the guard until the user accepts.
  Done when: changing a transform's output on the stored sample fails `fm check` with a diff, and `fm prove --golden accept` is user-only.

- **Prove an incident postmortem's action items closed** — FEATURE — value 3 — effort S — risk low — category: ops follow-through
  Why: Signal-to-fix loop (Mission 8) opens root-cause FIXes, but nothing checks that "action items" in written postmortems became tasks with evidence. Assumption: postmortems are markdown with an action list.
  Done when: `fm prove --postmortem FILE` lists each action item with its task id and evidence class, and flags any with none.

- **Label each proof with the outside source that could contradict it** — FEATURE — value 3 — effort S — risk low — category: proof labelling
  Why: Unproven rollup counts typed or inconclusive evidence, yet a proof that passes against a mocked outside service counts as green. Assumption: evidence records can carry an `external` field.
  Done when: the rollup shows a separate "proven against a stand-in" count and lists tasks whose evidence used a mock, fixture or cached fetch.

- **Expire a proof when its outside dependency changes** — FEATURE — value 3 — effort M — risk med — category: stale proof
  Why: Docs, research and infra proofs go stale when a tool version, API or page changes, not when time passes.
  Done when: each proof stores a dependency fingerprint (tool versions, source hashes); `fm unproven` re-labels a closed task when the fingerprint differs, with the changed item named.

Next question: Which outside-world proof kinds can run with no network and no real credentials, and which must stay labelled unproven until the user grants them?
Next question: When a proof is stood in by a mock or fixture, who owns keeping the stand-in honest against the real thing?
