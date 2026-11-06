# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run the necessity corpus on every new model ID** — FEATURE — value 5 — effort M — risk low — category: obsolescence
  Why: assumption: gates were built against weaker models. Tier xhigh, domain: inversion. The existing ablation idea is a one-off. Here, a new model ID triggers a replay of past catches (guard blocks, failed proofs, plan rejections) with each gate off. Gates the model now passes unaided are listed as retire candidates, with the count of catches replayed.
  Done when: a new model ID in config triggers `fm necessity`, which prints a per-gate table of catches kept vs. missed with a retire-candidate column, and a planted always-needed gate is never listed.

- **Tag every lesson and rule with the model that taught it** — FEATURE — value 4 — effort M — risk low — category: staleness
  Why: assumption: lessons mined from weaker models' mistakes pile up as injected context. Tier high. On a model change they move to a quarantine and return only if a replay shows they still change an outcome.
  Done when: after the configured model changes, `fm lessons` shows the old-model set as quarantined, and a lesson that still catches a replayed failure is restored automatically.

- **Forecast the date Foreman's measured delta reaches zero** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: assumption: a nightly frozen-task suite can run with and without Foreman per backend. Tier extreme. It fits a trend to the delta in verified-close rate and cost, and prints a crossover estimate with an interval. Calibration of Foreman's own bets already exists, so the forecast can be scored later. Wild.
  Done when: `fm delta --forecast` prints a crossover date range from at least 8 nightly points, and a synthetic flat series reports "no crossover".

- **Review any agent's PR with plan, proof and guard checks** — FEATURE — value 5 — effort L — risk med — category: surfaces
  Why: assumption: work is moving to cloud and background agents that run no local hooks, so a hook-based layer sees nothing. Tier massive. A CI app takes any PR, from any agent, and asks for a brief, reruns the proofs, and scans the diff for guard-class effects. Foreman becomes the gate at the merge boundary instead of inside the session.
  Done when: a PR from an agent with no Foreman installed gets a check run listing "brief found/missing", each proof rerun with its result, and flagged effects.

- **Canary the host's hook protocol against beta CLI versions nightly** — FIX — value 4 — effort S — risk low — category: reliability
  Why: Foreman depends on hook payloads and transcript formats owned by hosts (Claude Code, Codex, Gemini). A silent schema change would disable the guard unnoticed. Tier medium. The pack already lists a gate suite; this adds a nightly run against the pre-release channel.
  Done when: a fixture host that renames one hook field makes the canary file a task naming the field within one run.

- **Show a weekly "what Foreman stopped that you'd have wanted" receipt** — FEATURE — value 4 — effort M — risk med — category: honesty
  Why: assumption: the user keeps Foreman only while its catches are felt. This answers the question of who notices a retirement. Tier xhigh. Each catch is graded by what happened next (user overrode, reran manually, or accepted). Eight weeks of near-zero accepted catches triggers a "consider turning this off" line.
  Done when: `fm digest` lists catches by outcome, and a seeded ledger with no accepted catches prints the suggestion.

- **Define and ship the irreducible core** — CLEAN — value 4 — effort L — risk med — category: simplicity
  Why: assumption: what survives a perfect model is authority, an audit trail and proof of claims, not nudges. Tier high. A `core` profile runs only the ledger, the grant store and proof receipts, with a hard line-count and hook-latency budget. Everything else becomes opt-in plugins that carry expiry dates.
  Done when: `fm profile core` runs a full task close with only those three components loaded, and a test fails if the core exceeds its budget.

- **Detect features the host now does natively from live transcripts** — FEATURE — value 3 — effort M — risk low — category: overlap
  Why: the existing idea reads vendor release notes. This reads behaviour instead. It counts sessions where Foreman's plan, worktree or checkpoint gate fired after the host had already done it. Tier medium.
  Done when: `fm doctor` shows a "duplicated by host" row with counts per gate, and a fixture transcript with a native plan yields a nonzero count.

- **Export verified-close data as a training and eval set** — FEATURE — value 4 — effort L — risk high — category: data
  Why: the ledger holds verified outcomes, catches and failures, which is exactly the signal for teaching a model the discipline. Tier massive. Foreman then measures its own shrinking need, and the ledger becomes the part that cannot be replaced. Local-only, redacted, opt-in. Wild.
  Done when: `fm export --evals` writes a redacted JSONL of (brief, trajectory, grade) with no secrets matching the guard's secret scanner, and nothing leaves the host without a setting.

- **Make the ledger an open attestation format other tools can read** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: assumption: if harnesses or CI vendors absorb discipline, the history must outlive Foreman. Tier high. Emit in-toto or git-notes records alongside the hash chain, and keep `fm verify-ledger` able to verify the exported form.
  Done when: an exported attestation for a closed task verifies with a third-party in-toto verifier and with `fm verify-ledger`.

- **Pay a "Foreman-killer" lane to prove a gate unnecessary** — FEATURE — value 3 — effort L — risk med — category: adversarial
  Why: assumption: gates are kept by inertia. Tier extreme. A lane's only goal is to complete a frozen task set with one gate disabled at equal verified outcome. A success becomes a retirement proposal with the evidence attached. Wild.
  Done when: a run on one gate produces either a retire proposal with N matched closes or a record of the failures that justified keeping it.

- **Write the self-dissolution plan on demand** — FEATURE — value 3 — effort M — risk low — category: lifecycle
  Why: tier extreme. `fm retire` lists each remaining function, who could absorb it (host feature, CI, OS sandbox), the migration step and the data export. This makes Foreman's own obsolescence a planned outcome rather than a surprise. Wild.
  Done when: `fm retire` outputs a per-function table with a successor and an export command for every verb, and every command listed exists.

- **Keep shadow mode as the default for new rules** — SECURITY — value 3 — effort S — risk low — category: false-positive cost
  Why: it answers the earlier question about the measured false-positive cost of guard decisions. A new rule only logs its would-be blocks until user overrides, or the lack of them, give it a measured cost. Tier low.
  Done when: a new rule logs "would block" for 7 days, and `fm guard --rules` shows its override rate before enforcement is enabled.

Next question: Which of Foreman's functions would a user still need if the model never made a mistake, and is each one the same on a cloud agent with no hooks?
Next question: What is Foreman's measured delta over a bare host today, per backend, and has anyone recorded it before this?
