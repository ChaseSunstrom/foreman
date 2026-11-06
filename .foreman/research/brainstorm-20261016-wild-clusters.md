**Note on count:** `ideas.md` holds about 290 distinct titles, not 409. The 409 probably counts lens-file entries. I clustered every title in the file. Titles are shortened and "Wild:" prefixes dropped. Where a title fits two clusters I placed it in one only.

## 1. Clusters

| # | Capability | Titles | Wild | Eff |
|---|---|---|---|---|
| 1 | Re-grade closed work by what happened next | Survival grader/closed work survived; done-claims vs next; one outcome ledger; lines a human saw; self-settling regret ledger; regret ledger of plan alternatives; graveyard of rejected approaches; record dissent, score later; leading-indicator miner; days-since-never-event | 2 | M |
| 2 | Forecast calibration that gates autonomy | Calibration ledger (x3, incl. feeds back); prediction error as slow-down; pit-wall ETA; predict touch-set; early-warning lane score; P-wave before interrupt | 3 | M |
| 3 | Pre-do the likely next task | Prediction draft; pre-run next task (x2); predict next task, pre-brief; predict follow-up; predict next week's asks; n-gram prefetch; intent telemetry; estimate intent from steers | 4 | L |
| 4 | Turn steers and interrupts into typed mistakes and checkers | Compile steer into checker (x2); interrupt = labelled mistake; interrupt autopsy; classify interrupts; frustration as control signal; contradictory steers; approval fatigue; challenge flag buys re-verify; user glossary; house-style card; taste from accept/reject | 3 | M |
| 5 | A user proxy that answers asks | Answer asks from past answers; decision twin overnight; scored user-proxy; delegation policy from asks; twin of the user (x2); rulings as precedent; export rulings to local judge; standing-orders sheet and queued-task contradictions; five-example clarify; canary asks | 4 | L |
| 6 | Replay and backtest any change on old sessions | Counterfactual replay lab/bench; replay past sessions vs rule; cassette shim; per-repo benchmark from git; merge two brains; frozen elder brain; bisect versions; bisect harness; model-check then bisect; synthetic user/soak/worlds; exclude synthetic sessions; shadow-run autonomy | 3 | M |
| 7 | Every self-change is a pre-registered trial | Self-change court; self-edit tournament; pre-register; placebo arm; shadow A/B; Foreman-off twin; ratchet any number; register tunables; hill-climb prompts; harness edits its own hook/harness (x2); unattended experiments pocket; prediction market; moonshot slot; lens survival weights | 4 | L |
| 8 | One risk budget and consent envelope for autonomy | Error budget; risk budget; consent envelope; auditable ladder; quarantine after bad outcome; capability chains; secrets broker; sterile cockpit; load-shedding order; turnaround contract; hold/witness points | 3 | M |
| 9 | Tamper-evident proof and queryable ledgers | Hash-chained manifest; offline receipt verifier; proof ledger; gate tampering; hidden acceptance tests; JSON Schemas; ledger as SQL; type-check the brain; forget on demand | 3 | M |
| 10 | Attack Foreman's own guard and state machine | Bounded exhaustive grammar; obfuscation fuzz; mutation-test gates (x2); self-play red team; fire drill; model-check state machine (x3); negative-selection sequences; drug-safety signals; contact-trace bad lesson; hostile-input pack; fault injection; risky-command overlay; `--dry-run` everywhere; cold-stranger test | 3 | M |
| 11 | Close gate: evidence bundle | Break-it adversary; generated properties; dependents' tests; evidence bundle; behaviour-change review; ablate diff; infer invariants; conserved quantities; bug-class invariant; golden looks; inherited red; machine-facts diff (x2); traced test map; fence-check; volatility halt; trial balance; exit interview; belief ledger; assumption probes; typed holes; old-code oracle; back-translation; incident commander | 3 | L |
| 12 | Lane coordination and merge | Contract-commit forks; integrator agent; nightly merge rehearsal; symbol gossip; lane bulletin; TCAS advisories; fleet Andon; dependent stubs; rebase by intent; review-debt WIP limit; fan-out width; merge/split subagents; stalled-lane handoff; vertical slices; critical-path queue; fresh-agent relay | 3 | L |
| 13 | Markets, seats and routing between agents | Bid market (x3); lane auction; plan auction; lesson auction; task auction; standing seats; bus factor; seat library; sprint-review seat; per-library competence (x2); tic atlas; Thompson bandit; RFC round; racing builders diff; peer-review round robin; patch tree search | 4 | L |
| 14 | Overnight gardening | Garden repos; gardener from forged chores; idle principle consolidation (x2); dream session; time-capsule self-interview; compost worktrees; rehearse failures | 2 | M |
| 15 | Rule and hint hygiene | Rule tribunal (x2); forgetting curve; minimum dose; Haiku-floor gate; lazy consensus; credit assignment; ignored hints; fix contraindications; card examples in CI; `--help` cards; distill judgments to rules | 2 | M |
| 16 | Forge tools from repeated work | Forge tool/verb (x5); codemod; generate MCP/skills; provisioner; golden paths; golden session/playbook (x2); verb nudge; blocked-task probe | 3 | L |
| 17 | Cross-repo and cross-machine memory | Transplant (x2); neighbour-repo search (x2); twin code; fix commons; fleet metrics by git; machine roll call; capability sheet; fresh-machine bootstrap; notes vault; per-blob file notes; re-read tax; failure archetypes | 3 | M |
| 18 | Code-structure intelligence | Import-graph boundaries; fitness functions; blind rebuild; simplification skunkworks; hotspots (x2); fault lines; where agents get lost; scent marks | 3 | M |
| 19 | Debugging discipline | Refuted-hypotheses ledger; hypothesis blackboard; differential diagnosis; record failing run; dev-server tap; reproduce feedback; seance; fingerprint env | 3 | M |
| 20 | Upstream and dependency watch | Upstream issues (x3); dependency diff on bump; trial a dependency; compatibility farm | 2 | S |
| 21 | Backlog and plan integrity | Commander's intent; sweep queued plans; start-ready deferred; fold deferred into epic; punch list; brief golf; focus-drift meter; hold prototype tournament | 2 | S |
| 22 | Pane as instrument | Speedrun splits; control-room SPC (x2); chess eval bar; pane replay archive; push-to-talk; editor language server; animatic; mock layouts; README clean-room walk; README pictures in CI; explorers in the user's app | 3 | M |
| 23 | Metric honesty and spend | Unexplained-spend alarm; Goodhart audit; measurement honesty audit; magic-number owners | 2 | S |
| 24 | Other / one-offs | Refuse volatile storage | 1 | S |

## 2. First versions

Status checks used Grep on `plugin/lib`. Anything not marked was not checked.

1. `fm outcomes` gains a 30-day "survived/reverted" column. PARTIAL: `fmoutcomes.py:39`.
2. Add a calibration score to the plan line and refuse auto-run when it is low. PARTIAL: `fmoutcomes.py:134`.
3. A throwaway worktree draft of the top queue item at `fm night`. MISSING, in `fmnight.py`.
4. `fm steers` types each interrupt and drafts one checker. MISSING (not grepped), in `fmfixes.py`.
5. Answer asks only when an identical past ask exists, labelled as a proxy. MISSING (not grepped), in `fmbus.py`.
6. `fm replay --rule X` over the last N sessions. PARTIAL: `fmreplay.py:139`, `fmbench.py:782`.
7. `fm evolve` records a predicted movement and auto-reverts. PARTIAL (not grepped), in `fmevolve.py`.
8. One daily autonomy-spend file read by `fmguard.py`. MISSING (not grepped).
9. Chain each ledger line with the previous line's hash, plus `fm verify-ledger`. MISSING: no hash-chain match, in `fmcore.py:781` (`ledger_tail`).
10. `fm bench guard --mutate` flips one rule at a time. PARTIAL: `--dry-run` exists at `fmguard.py:3183`, `fmbench.py`.
11. `fm check` prints one evidence block at close. PARTIAL (not grepped), in `fmcore.py`.
12. A symbol-claim line on the bus. PARTIAL: `fmcore.py:2410` (andon), `fmbus.py`, `fmlanes.py`.
13. Log bid vs actual per lane. MISSING, in `fmagents.py`.
14. Extend `fm night` with one chore: compost worktrees. PARTIAL: `fmnight.py`, `fmtidy.py`.
15. `fm lib` flags cards or rules never fired in 60 days. PARTIAL (not grepped), in `fmlib.py`.
16. List sequences repeated 3+ times. PARTIAL: `fmrepeats.py` exists, so suggest-only.
17. A shared fix index across local repos. PARTIAL (not grepped), in `fmfixes.py`.
18. Hotspot list from fix-after-edit, shown in plans. PARTIAL: `fmmap.py`, `fmgraph.py`.
19. `fm fix` writes `refuted.md`. PARTIAL (not grepped), in `fmdebug.py`.
20. `fm doctor` lists upstream bugs with the evidence. MISSING, in `fmdoctor.py`.
21. A greeting line for stale deferred items. MISSING (not grepped), in `fmorders.py`.
22. A one-row SPC strip in `rows.tsx`. MISSING (not grepped).
23. `fm cost` flags calls with no matching Foreman task. PARTIAL (not grepped), in `fmcost.py`.
24. A guard refusal for resume state on `/tmp`. Already done by T-0817, so drop it.

## 3. Wildest and most valuable

1. **Cluster 6 (replay and backtest):** Every other self-change idea is only safe once you can test it on real history. `fmreplay.py` is the base.
2. **Cluster 7 (self-change trials):** It makes "learns" provable by turning each rule edit into a measured trial that auto-reverts.
3. **Cluster 4 (steers into checkers):** The user's corrections are Foreman's best free training signal.
4. **Cluster 1 (survival grading):** It replaces "tests passed" with "stayed merged", so every other score has something real to compare against.
5. **Cluster 5 (user proxy):** It cuts interruptions, and it is only safe with cluster 2 gating it.
6. **Cluster 3 (pre-do next task):** It uses idle machine time and shows value the user can see.
7. **Cluster 9 (tamper-evident ledger):** It is cheap, and it makes every claim Foreman reports checkable.
8. **Cluster 10 (attack own guard):** Mutation-testing the gates finds holes before a builder does.

## Risks

- **Overlap:** many titles repeat across rounds, so the "x3" counts are my reading of the titles alone.
- **Existing work:** most titles say "near T-NNNN (done)", so check those tasks before scoping.

## Not checked

- Lens files, because titles were clear enough.
- The `.tsx` files.
- Any status marked "not grepped".

**Noticed:** `ideas.md` reports 409 ideas but lists about 290 titles. Per-lens counts "bold bets: 40" and similar don't add up to the list.
