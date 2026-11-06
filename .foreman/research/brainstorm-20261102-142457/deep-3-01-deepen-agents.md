# Brainstorm — lens: deepen: agents

- **Fold the agent roster, allowlists and depth caps into one signed `agents.toml`** — CLEAN — value 4 — effort M — risk low — category: agents
  Why: the category lists roster-in-one-table, per-role tool allowlists, depth/width caps and adapter-as-data separately; they are one table. Gen-0 #12 "lean and safe" wants one place to read and diff.
  Done when: `fm doctor` fails if any spawn path (lane, brainstorm child, cold read, drive) reads a role, tool list, depth or model that isn't in `agents.toml`, and a test spawning an undeclared role is refused.

- **Pass a capability token down every spawn, never a shared grant** — SECURITY — value 5 — effort M — risk med — category: agents
  Why: combines "make privileged verbs refuse lane callers" with "cap depth and debit child spend". The token carries remaining depth, dollars, verbs allowed and a push grant (pushes are spent per task, per the steer). A child can only hand down a subset.
  Done when: a lane calling `fm ship` or `fm decide --kind costly` exits nonzero with a `Next:` line, and a child's spend appears as a debit on the parent's budget in `fm cost`.

- **Run `fm lane --plan` as a dry-run that merges in a scratch worktree** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: merges "preview a lane" with "scratch-worktree merge". Parallel Missions 5-8 run in lanes and merge in mission order, so conflicts surface late. The plan lists files each brief will touch, predicted overlaps and a trial merge result.
  Done when: `fm lane --plan T-a T-b` prints overlapping files and `merge: clean|conflict` without touching the live tree (verified by tree hash before and after).

- **Record every agent abstention and skip as a ledger event with a reason** — FIX — value 4 — effort M — risk low — category: agents
  Why: answers the open question about decisions that leave no record. A lane that gives up, a hedge that is cancelled, a lens that goes dry, an allowlist denial: none is visible today. Adjacent drop-one-ledger-class work already shows readers print zeros silently.
  Done when: `fm outcomes` shows a count of agent no-ops by reason, and killing a lane yields one ledger line naming the reason.

- **Give each role a "who checks the checker" pairing, enforced** — SECURITY — value 4 — effort M — risk med — category: agents
  Why: merges the janitor/defender pair, the cold-read Haiku→Sonnet ladder and the open question of proof for the self-change gate. Rule: no role may approve work from its own model family and prompt version. This needs outside signals, per the standing steer.
  Done when: a test where the author and reviewer share a model and prompt hash fails the gate with the named rule.

- **Replay a changed agent prompt against frozen cases before it goes live** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: the shadow-adopt step grown up. It combines with `fm exam` held-out scenarios and `fm eval capture` (T-0035, deferred). A prompt change runs in shadow on the last N finished tasks and goes live only if its pass rate and cost don't regress.
  Done when: editing a role prompt file makes `fm check` print a shadow score against N cases and block when it's below the baseline.

- **Fall back along a ranked model chain, with a daily pin probe feeding it** — FEATURE — value 3 — effort S — risk low — category: agents
  Why: the ranked chain and the daily ID probe (c10) are one feature: the probe decides the chain's order. Each fallback is recorded, so the user sees a quality change.
  Done when: with a fake dead model ID, a child spawn lands on the next entry and the ledger notes `fallback: A→B`.

- **Throttle and hedge lanes by progress signals, not the clock** — PERFORMANCE — value 3 — effort M — risk low — category: agents
  Why: merges progress-based time bounds, hedging stragglers and throttling while the user is active. One scheduler reads "last diff, last test run, last token delta" and the user's input idleness, then pauses, hedges or kills.
  Done when: a lane with no progress signal for K minutes is hedged or killed; a lane pauses on a typed keystroke in a simulated session.

- **Show the agents as a live "who's holding what" board** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: the dossier, the roster and the lane plan are all readable but scattered. The foreman-ui Agents graph exists; add per-agent budget left, tool grants, files claimed and last action.
  Done when: the pane shows those four fields for each live lane, matching `fm lane --json`.

- **Wild: Hold a nightly "mutiny drill" where a red-team agent tries to make a sub-agent break its own allowlist** — SECURITY — value 4 — effort L — risk med — category: agents
  Why: wild. Extends the red-team agent for broken promises: it attacks the roles, not the verbs, with injected text in task briefs and tool output, and reports which allowlist or depth cap held. Fits the deferred injection defenses (T-0791).
  Done when: the drill files a task for each escape it finds, and a planted hole in a test fixture is found.

- **Wild: Let agents bid for a task with a cheap probe run, and let the cheapest passing bid win** — PERFORMANCE — value 3 — effort L — risk med — category: agents
  Why: wild. Turns the reputation auction and per-step effort choice into data. Each model/effort/role runs a 60-second probe, and the duel data (T-1266 ceremony profile) prices the bids. Assumption: probe cost stays below the saving.
  Done when: on a replayed set of 10 tasks, the auction's total cost is lower than the fixed choice with an equal pass rate.

- **Wild: Pre-warm a lane's context (map, lessons, dossier) from queue prediction, as a local cache** — PERFORMANCE — value 2 — effort M — risk low — category: agents
  Why: wild. The next-task prediction exists in `fm next`; the warm lane starts with the dossier already assembled, and discards it if the queue changes.
  Done when: median time from lane start to first edit falls on a bench, and a stale warm dossier is dropped when its inputs' hashes change.

- **Make every multi-agent flow run single-agent in CI on a fake adapter** — CLEAN — value 4 — effort M — risk low — category: agents
  Why: combines the tested single-agent path with the one conformance fake. Blocked tasks T-0335 and T-0336 show adapters are verified live only rarely; a fake gives the same contract for free.
  Done when: one test matrix runs the drive, lane merge and cold read through the fake adapter in both single and multi modes, and any new adapter must pass it.

Next question: which agent behaviors (retry, hedge, fallback, skip) change spend or outcomes in a way the user never sees until the receipt?
Next question: what does a sub-agent do when its tool allowlist blocks the only way to finish, and does Foreman tell the user or just fail the task?
