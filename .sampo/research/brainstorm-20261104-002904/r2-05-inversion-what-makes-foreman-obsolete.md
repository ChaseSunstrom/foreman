# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run a "native-parity" probe per verb** — FEATURE — value 5 — effort M — risk low — category: obsolescence
  Why: Mission 4's thrust is proof beyond unit tests; hosts (Claude Code, Codex, Gemini, opencode) keep absorbing plan, hook and verify features. Assumption: no per-verb check yet compares Sampo's result to a host-native run on the same task.
  Done when: `sampo louhi native` prints, for each of ≥10 verbs, "host alone matched / Sampo added / host worse" from a recorded paired run, and the verbs where the host matched are listed first.

- **Stamp every unproven doc claim with a "needs Sampo?" flag** — FEATURE — value 4 — effort M — risk low — category: claims
  Why: 421 docs flag claims no run has checked; a claim a bare agent already satisfies is not Sampo's value. Assumption: claims aren't currently split by who makes them true.
  Done when: each of the 421 claims has a `needs_sampo: yes|no|unknown` field and the report counts each.

- **Turn spec-example criteria into a bare-agent baseline** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: Mission 4 wants spec examples as runnable criteria at plan time. The same criteria, run against an unassisted agent, show which ones Sampo's plan step actually improves. Assumption: the held-out scenario set is large enough to show a difference.
  Done when: a criteria block runs in both arms and the output shows pass rates for each, with the gap per criterion.

- **Auto-draft a retire-when predicate for each verb** — CLEAN — value 4 — effort S — risk low — category: lean
  Why: the earlier lean ideas call for retiring capabilities, but no field says when a verb stops earning its place. Assumption: verb table rows have no sunset field.
  Done when: every verb row carries `retire_when:` naming a measurable condition, and `sampo doctor` lists any whose condition is currently true.

- **Watch host release notes for features that overlap a verb** — FEATURE — value 4 — effort M — risk med — category: drift
  Why: Sampo sits on four hosts that ship weekly, and T-0336 and T-0337 show host behaviour changing under it. Assumption: release notes are fetchable and parseable, with the fetch behind an explicit setting.
  Done when: running the watcher against a saved release-notes file flags at least one verb as "host now does this" with the matching line quoted.

- **Run a monthly bare-model ablation on public surfaces** — PERFORMANCE — value 5 — effort L — risk med — category: necessity
  Why: the standing rule compares foreman vs plain, but the bar moves with each new model. Assumption: the end-of-run exam is the only comparison planned, so a drift in the gap would be missed.
  Done when: a dated scorecard shows foreman-minus-plain per capability across ≥3 model roles, with a trend line over at least two runs.

- **Publish the discipline as a harness-neutral spec** — FEATURE — value 4 — effort L — risk med — category: portability
  Why: the rules say Sampo isn't specific to Claude Code and the surfaces must name roles, not vendors. If a host adopts the spec, Sampo becomes the reference checker rather than the only enforcer. Assumption: no machine-readable spec exists beyond MASTER.md.
  Done when: a `discipline.json` spec validates, and a second harness's output can be checked against it with no Sampo code on the path.

- **Prove the ship gate catches what CI alone would not** — FIX — value 4 — effort M — risk low — category: proof
  Why: the gates (`sampo doctor`, round-trip e2e, hook bench) overlap forge CI. Assumption: no count exists of defects the local gate stopped that CI would have passed.
  Done when: a report over the last 60 days lists closes where the local gate failed and CI would have passed, or states "0 found".

- **Tag lessons that a newer model no longer needs** — FEATURE — value 3 — effort M — risk low — category: lean
  Why: T-0217 gives lessons a confidence; lessons taught by an older model can go stale as models improve. Assumption: lessons record the model that taught them.
  Done when: lessons carry a model tag, and a replay on the newest model role reports which ones changed no outcome.

- **Wild: Self-dissolution plan on demand** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: wild. Assumption: a tool that can say what it would remove is more trusted. `sampo eject` lists each part, its replacement in the host, and what is lost.
  Done when: the command prints a plan for removing every hook and verb, and the plan's dry run leaves a project that builds and passes its tests.

- **Wild: Pay a "Sampo-killer" lane to prove a gate unnecessary** — FEATURE — value 4 — effort L — risk med — category: wild
  Why: wild. A lane is scored for each gate it shows catches nothing over 30 days of replayed tasks, with the claim checked by an independent cold read.
  Done when: one gate is retired or kept on the strength of the lane's replay, with its evidence file cited.

- **Wild: A weekly "what Sampo stopped that you'd have wanted" receipt** — FEATURE — value 4 — effort M — risk low — category: wild
  Why: wild. Value is hard to see when it works silently, which is how a useful layer gets removed. It lists only the blocks, redirects and failed proofs the user didn't override, each with a one-line stake.
  Done when: a receipt over a recorded week lists each save with its command and outcome, or states "no saves".

- **Detect features the host now does natively from live transcripts** — FEATURE — value 4 — effort M — risk med — category: drift
  Why: a host's native plan or verify step may start doing what Sampo's verb does, leaving duplicate steps. Assumption: transcripts show a host-native step beside Sampo's call.
  Done when: on a transcript pair, the detector names the Sampo verb and the host step that repeats it.

Next question: Which of Sampo's gates has never stopped anything the host's own checks would have passed, and does the ledger hold enough closes to say so?
