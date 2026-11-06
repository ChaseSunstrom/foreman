# Brainstorm — lens: the outside world (invented): research, docs, ops and incidents, infra, data, design and releases held to code's standard of proof

- **Prove docs against code with executable claims** — FEATURE — value 5 — effort M — risk low — category: docs proof
  Why: Mission 7 lists "docs against code" as a proof kind, and the pack shows built proof only for perf (T-2284/T-2303) and data (T-2288). Docs (README, MASTER.md, site stats) are unproven. Assumption: README/MASTER make checkable claims (verb names, flags, counts, "6,400-char budget").
  Done when: `fm prove --docs` extracts backticked `fm` verbs, flags and numbers from README/MASTER, runs each against `fm --help` or the code, and a doc naming a nonexistent verb fails with the file and line.

- **Prove an infra change with a plan, apply and re-plan round trip** — FEATURE — value 4 — effort M — risk med — category: infra proof
  Why: Mission 7 names infra and ops; `fm prove --migration` already does up, down, up on a throwaway copy, so the same shape fits Terraform, Docker, systemd and CI YAML. Assumption: users have such files.
  Done when: `fm prove --infra` validates the config in a scratch environment, applies it, re-plans to an empty diff, and records the result as run evidence; with no scratch target the criterion shows as unproven.

- **Pin every external fact a task relied on to a dated source check** — FEATURE — value 4 — effort M — risk low — category: research proof
  Why: Mission 10 includes research. Research notes feed the frontier digest and brainstorms with no recheck. Assumption: notes cite URLs or versions.
  Done when: `fm research check` re-fetches each cited URL or version (opt-in, network only on explicit setting), flags dead links and changed values, and a note with none is labelled "unsourced" in the unproven rollup.

- **Close an incident task only on a replayed signature** — FEATURE — value 5 — effort M — risk low — category: ops proof
  Why: Signal-to-fix (Mission 8) files a root-cause FIX from a recurring signature, but nothing proves the signature is gone. Assumption: signatures are stored text or regex.
  Done when: an incident task stores its failure signature and a replay command; closing requires the command to fail on the start tree and pass now, else "unproven: no replay".

- **Count the numbers the user sees against their producing command** — FIX — value 4 — effort S — risk low — category: number audit
  Why: An earlier question asks which numbers were never checked by anyone but their producer. T-2326 refreshes site stats daily from the same code that computes them. Assumption: the stats include counts like files, tasks and exam rates.
  Done when: `fm doctor` recomputes each published site stat by an independent shell one-liner (find, git, grep) and warns on any mismatch over a set tolerance.

- **Release proof: install the built artifact into a clean directory and run the first-use path** — FEATURE — value 5 — effort M — risk med — category: release proof
  Why: Mission 10 names releases; the pack shows T-0352 (publish Desktop) blocked and no artifact-level check. Assumption: install.sh and the plugin tarball are what users get.
  Done when: `fm prove --release` installs the packaged artifact into a throwaway HOME, runs `fm doctor` and one task round trip with no `claude` on PATH, and records pass or fail.

- **Verify a design against its spec with a screenshot diff and a contrast and tab-order check** — FEATURE — value 4 — effort M — risk low — category: design proof
  Why: `fm shot` and `fm flow` exist for UI but nothing ties a screenshot to a design intent; the unproven rollup counts only "no visual check". Assumption: the web UI has stable pages.
  Done when: a task can name a baseline shot and a rule set (contrast ratio, focus order); `fm shot --check` fails on either, and a UI task with a shot but no rule is labelled "looked at, not judged".

- **Label every closed task's evidence by who could have lied** — FEATURE — value 5 — effort S — risk low — category: unproven rollup
  Why: The rollup counts typed or inconclusive evidence; the earlier question asks where a writer and a judge are both models. Assumption: evidence records already have a kind field.
  Done when: each rollup entry shows a trust tag (ran by Foreman, ran by the agent, typed, judged by model), and the surfaces show counts per tag.

- **Wild: Run a "fire drill" that breaks something on purpose and checks the docs' recovery steps work** — FEATURE — value 4 — effort L — risk med — category: ops proof
  Why: wild; docs and runbooks (blackstart, T-0798) are never exercised. Assumption: runbooks have copyable commands.
  Done when: `fm drill RUNBOOK` executes its steps in a scratch copy after a planted fault and reports which step failed or went stale.

- **Wild: Give each release a "claims manifest" that a stranger can re-verify offline** — FEATURE — value 4 — effort L — risk low — category: release proof
  Why: wild; the exam, held rate and site stats are claims only the producer verifies. Assumption: a signed bundle of commands and their outputs is feasible.
  Done when: `fm release claims` emits a file with each public claim, its command and its recorded output, and `fm release verify FILE` reruns them on another machine.

- **Wild: Let a data task carry a "golden sample" that guards every later change** — FEATURE — value 3 — effort M — risk low — category: data proof
  Why: wild; T-2288 proves migrations, but data transforms and scripts have no regression anchor. Assumption: small samples can be stored.
  Done when: `fm prove --data` records the hash of a transform's output on a fixed input and later tasks touching the transform fail on a changed hash unless explained.

- **Prove a performance claim holds across noise, not once** — PERFORMANCE — value 3 — effort S — risk low — category: perf proof
  Why: T-2284/T-2303 record medians; noise handling isn't shown. Assumption: runs are few.
  Done when: `--bench` records spread, and a change inside the noise band is labelled "inconclusive", not improved.

Next question: Which proof kinds can a model fake by writing both the claim and the command that "verifies" it, and what check by someone else closes that gap?
Next question: For work with no command at all (design taste, a research conclusion), what is the cheapest honest label and who can lift it?
