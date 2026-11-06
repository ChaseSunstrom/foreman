# Brainstorm — lens: sci-fi: the 2030 harness that proves every kind of work (UI, data, docs, infra, ops, perf, research, releases) to the standard of a failing test, worked back to what Python and Foreman can do today

- **Make every proof kind emit one signed "proof receipt" record** — FEATURE — value 5 — effort M — risk low — category: proof ledger
  Why: T-2273 (unproven rollup), T-2284/T-2303 (measured perf), T-2288 (migration) each store evidence differently; the rollup must infer from typed vs inconclusive. assumption: no single schema exists yet.
  Done when: `fm task evidence ID --json` returns the same fields (kind, command, ran_at, tree hash, exit, measurements, witness) for a perf, migration and test proof, and the rollup reads only that.

- **Add a docs-against-code proof kind** — FEATURE — value 5 — effort M — risk low — category: docs proof
  Why: Mission 7 names "docs against code"; the seed row says proof kinds for docs/infra/data/perf (3), and only perf and data are built. MASTER.md and README quote commands, flags and counts (e.g. "2058 files").
  Done when: `fm prove --docs README.md` extracts every fenced `fm ...` command and flag mentioned, runs `--help`/dry parse on each, and fails naming the line of a command or flag that no longer exists.

- **Add an infra proof kind: plan, apply to a scratch target, re-plan to empty** — FEATURE — value 4 — effort L — risk med — category: infra proof
  Why: Mission 7 #10 "infra and ops"; migration proof already does up/down/up on a throwaway copy, and the same shape (apply, verify idempotent, revert) fits Dockerfiles, systemd units, CI YAML. assumption: a container runtime or `systemd-analyze`/`actionlint` may be absent, so it must degrade to labelled unproven.
  Done when: `fm prove --infra <path>` on a fixture unit file runs a lint plus an idempotent apply in a temp root and records "unproven: no runtime" when none is installed.

- **Prove "does it do what the user meant" by replaying the ask as an acceptance script** — FEATURE — value 5 — effort L — risk med — category: intent proof
  Why: Mission 7 lists "does it do what the user meant"; the user's own words show repeated plan-gate misses (T-2285) caught only after the fact. assumption: asks can be decomposed into clauses.
  Done when: at task open each clause of the ask gets a row with a runnable check or an explicit "no check possible" label, and `fm task finish` refuses with any row neither run nor labelled.

- **Run a mutation check on each task's new test** — FEATURE — value 4 — effort M — risk low — category: test strength
  Why: `fm task prove` already shows the test fails without the change; this extends it to "fails under 5 plausible wrong changes" so a vacuous assertion is caught (cf. the T-2246 cold-read concerns about metric-gaming).
  Done when: a fixture task with a test of `assert True`-style weakness is reported "weak" by `fm prove --mutate`, and a real test is reported "strong".

- **Close the writer/judge gap with a user-owned checker file** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: answers the earlier question "which verbs have a model on both sides with no user-owned check between them"; steers already say weakness-finding must use signals Foreman didn't author.
  Done when: `fm doctor` lists each verb with a model writer and a model judge, and marks it red unless a check in `.foreman/checks/` the model cannot write is attached.

- **Re-verify old "done" claims on a schedule (proof decay)** — FEATURE — value 4 — effort M — risk low — category: proof freshness
  Why: the unproven rollup counts only static state at close; a proof run last month on a tree that has since changed is silently stale. assumption: evidence stores the tree hash.
  Done when: `fm unproven` shows a "stale" bucket for tasks whose recorded command now fails or whose scope files changed, with the rerun result.

- **Add a research proof kind: every claim carries a source and a re-fetch check** — FEATURE — value 3 — effort M — risk low — category: research proof
  Why: Mission 7 #10 covers research; the brainstorm/research notes feed gen-2 and the frontier digest, with no check that cited facts exist. assumption: notes cite URLs or files.
  Done when: `fm prove --research NOTE.md` fails on a cited file path that doesn't exist or a quoted line that isn't in the cited file.

- **Prove releases by installing the built artifact in a clean venv** — FEATURE — value 4 — effort M — risk med — category: release proof
  Why: `install.sh` and the "works with no claude on PATH" steer; the release gate is the in-tree suite, not the shipped artifact. 
  Done when: `fm prove --release` builds the package, installs into a temp dir with `python3 -I`, and runs `fm doctor` from there with a recorded exit code.

- **Replay the UI proof deterministically with a stored flow and pixel-diff budget** — FEATURE — value 4 — effort M — risk low — category: UI proof
  Why: `fm shot`/`fm flow` exist, but the rollup only says "no visual check"; a stored baseline would turn a screenshot into a failing-test-grade check. 
  Done when: `fm flow check` re-runs a saved flow on the web UI and fails when the diff exceeds the declared threshold, naming the changed region.

- **Wild: Let a proof run a "counterfactual twin" of the repo** — FEATURE — value 4 — effort L — risk med — category: proof
  Why: wild. Extend red-first from tests to everything: revert only the task's change in a worktree and require that the proof (doc check, perf, UI, migration) turns red there, so any proof kind has a falsifiability certificate.
  Done when: for each proof kind a fixture task shows green on the change and red on the reverted tree, recorded as "falsified: yes".

- **Wild: Publish a live "proof ledger" page on the Genesis site** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: wild; `genesis publish` already refreshes site stats daily (T-2326), and the user asked that the site be current. Show proved vs unproven by kind, with the unproven list unhidden.
  Done when: site/genesis shows a per-kind count that equals `fm unproven --json` totals at publish time.

- **Wild: A "chaos proof" lane that tries to break each green claim** — FEATURE — value 4 — effort L — risk med — category: adversarial proof
  Why: wild; fits "agents of agents": a cold child, seeing only the claim and the commands, gets a budget to find an input, state or time skew that makes the proof pass falsely, and files a task if it does.
  Done when: a fixture with a deliberately gameable proof is flagged by the lane, and a sound one is not.

- **Wild: Pre-register the proof before the work begins** — FEATURE — value 4 — effort M — risk low — category: intent proof
  Why: wild; like pre-registered studies, the criteria and measurement commands are hashed at plan acceptance, and any later change to them is shown as an explicit amendment, closing the "finished definition changes mid-goal" question.
  Done when: editing a criterion after focus produces an "amended" mark in `fm task show` and the unproven rollup counts amended proofs separately.

Next question: Which proof kinds can be falsified by reverting the change (red-first), and which can only be observed, so the rollup should label them differently?
Next question: What does the user do with the unproven list today: does anyone read it, and what single action would make it shrink?
