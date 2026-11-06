# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run the bare-model ablation to see what Foreman still adds** — FEATURE — value 5 — effort M — risk low — category: self-obsolescence
  Why: tier xhigh; domain: science (ablation); no pack evidence of an on/off comparison, so assumption: models now plan and prove natively. Prior art: eval ablations exist, but no harness retires its own gates by them. Cheapest experiment: replay 20 closed briefs with plan/prove/guard off; if pass rates match, the thesis fails.
  Done when: `fm ablate --last 20` prints per-gate catches (defects the gate caught that the bare run shipped) and marks gates with zero catches "retire candidate".

- **Price each gate by catches per dollar and auction budget to them** — FEATURE — value 4 — effort L — risk med — category: gate economics
  Why: tier xhigh; domain: markets. Parents: ablation × budgets and contracts. The user's own `--stall-usd` and spend-receipt asks show cost per outcome is what they watch. Prior art: none found for harness gates. Cheapest experiment: compute catches/$ for the proof and plan gates from existing ledgers and see if the spread is over 5x.
  Done when: a receipt row lists each gate's cost, catches and yield, and a gate below the user's floor is skipped on low-risk tasks.

- **Run a reverse auction for each brief across backends** — FEATURE — value 4 — effort L — risk med — category: routing
  Why: tier xhigh; domain: auctions. Foreman already drives Claude Code, Codex, Gemini and `fm code` on any model, so an auction is a natural routing step. Prior art: LLM routers pick by price or classifier, but none bid against a proof. Cheapest experiment: send 10 briefs to two backends, record cost and proof outcome, and check whether a cost-per-pass table beats the user's default pick.
  Done when: `fm run --bid` shows each backend's estimate and the winner, and the receipt compares estimate with actual.

- **Bond every landed change with a warranty window** — FEATURE — value 4 — effort M — risk med — category: accountability
  Why: tier xhigh; domain: markets/law (warranty). Parents: the user-edits-after-landing lessons (c14) and calibration. Prior art: none found for agent work. Cheapest experiment: for the last 30 landed tasks, count later reverts or hand-edits to their lines.
  Done when: a task closed more than N days ago that was later reverted or edited gets a "breached" mark, and `fm outcomes` shows breach rate per backend.

- **Make Foreman's discipline a portable spec any harness can enforce** — FEATURE — value 5 — effort L — risk med — category: protocol
  Why: tier high; domain: standards. If vendors ship native briefs and proofs, a product loses to a protocol, so assumption: Foreman should author the protocol first. Prior art: AGENTS.md and MCP cover context and tools, not evidence-gated closes. Cheapest experiment: write the brief-plus-proof schema in one page and have a second harness read one brief.
  Done when: `fm export --spec` emits a brief and proof record that a non-Foreman script validates.

- **Watch vendor release notes and mark verbs the harness now does natively** — FEATURE — value 3 — effort S — risk low — category: obsolescence watch
  Why: tier low; domain: ecology (competition). The pack's own question, "when a capability is retired, who notices first?", has no answer. Prior art: none found. Cheapest experiment: diff the Claude Code changelog against `fm` verb names once by hand.
  Done when: `fm doctor` lists verbs whose changelog keyword matches appeared in a vendor release, each tagged "check for overlap".

- **Move the guard from command strings to effects at a sandbox boundary** — SECURITY — value 5 — effort L — risk high — category: guard
  Why: tier xhigh; domain: military logistics (perimeter). Cheaper sandboxes make a regex-style guard redundant, and the pack's open question is which surfaces Foreman doesn't control. Prior art: devcontainers and microVM sandboxes, but none prove the policy per effect. Cheapest experiment: run lanes in a network-less container and count which of the guard's blocks it already makes impossible.
  Done when: a lane runs in a disposable sandbox, and `fm guard --coverage` shows blocks split into "sandbox makes moot" and "still needed".

- **Hand the user a signed audit pack a third party can verify** — FEATURE — value 4 — effort M — risk low — category: evidence
  Why: tier high; domain: law (evidence). If the user stops reading diffs, the ledger's hash chain (`verify-ledger`) is the durable value. Prior art: SLSA attestations cover builds, not agent decisions. Cheapest experiment: bundle one task's ledger slice and verify it from a clean directory.
  Done when: `fm audit-pack T-NNNN` writes a file that `fm verify-pack` accepts on a machine with no Foreman home.

- **Prune skills and verbs automatically as models improve** — CLEAN — value 4 — effort M — risk med — category: slimming
  Why: tier medium; domain: evolution (vestigial organs). The pack counts 1388 skill files, and `fm usage --prune` already lists unused verbs. Prior art: none found for skills. Cheapest experiment: count how many skill files have zero loads in 60 days.
  Done when: a weekly job proposes retiring unused skills, each with last use and token cost, and nothing is deleted without approval.

- **Wild: let spare quota run a bounty board overnight** — FEATURE — value 4 — effort L — risk high — category: unattended work
  Why: wild; tier massive; domain: labor markets. Parents: spend receipts × deferred-task wake-ups. The user's `--stall-usd` ask suggests unattended runs are wanted but bounded. Prior art: bug-bounty and Dependabot-style bots. Cheapest experiment: file three small briefs, run one night with a $5 cap, and count tasks landed with proof.
  Done when: a morning receipt shows briefs cleared, spend per close and any left, with every landing proven.

- **Wild: act as escrow between a client and an agent** — FEATURE — value 3 — effort L — risk high — category: contracts
  Why: wild; tier massive; domain: law and markets. Acceptance proofs already exist, so contracts and budgets can release payment only when they pass. Prior art: smart-contract escrow, with none tied to test evidence. Cheapest experiment: write one contract file for a tiny feature and let a stranger's agent attempt it.
  Done when: `fm contract settle` releases budget only if every listed proof passes on a clean checkout.

- **Wild: forecast the cost and finish time of the whole backlog as a futures curve** — FEATURE — value 4 — effort L — risk med — category: prediction
  Why: wild; tier extreme; domain: markets (futures). Calibration of Foreman's own bets already exists. Prior art: planning poker and Monte Carlo burn-up, none grounded in a ledger of agent runs. Cheapest experiment: backtest per-task cost estimates against the last 100 closed tasks.
  Done when: `fm forecast` prints a P50/P90 spend and date for the queue, and backtest error is shown beside it.

- **Wild: sell guard coverage as insurance with a premium and a deductible** — FEATURE — value 3 — effort M — risk med — category: risk pricing
  Why: wild; tier xhigh; domain: insurance. Parents: guard false-positive cost × bonds. This answers the pack's question about which guard decisions have measured false-positive cost. Prior art: none found. Cheapest experiment: tag past blocks as overridden or not and compute the rate per rule.
  Done when: each guard rule shows block count, override rate and the user's chosen risk level, and loosening a high-override rule is suggested.

Next question: what would the user have to see in a month to say "I no longer need Foreman here"? That is the retirement signal no brainstorm has defined.
Next question: which of Foreman's decisions would a vendor's native harness make worse, and is that measurable today?
