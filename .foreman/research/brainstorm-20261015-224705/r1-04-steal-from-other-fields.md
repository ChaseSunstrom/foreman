# Brainstorm — lens: steal from other fields

Lens: steal from other fields. These are all new relative to the lists, and each first version fits in days. Where the pack gave no direct evidence, I mark "assumption".

- **Show per-step splits against your personal best, like a speedrun timer** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the pane already has a per-step bar and a done/left work bar, and the ledger has step times. Nothing compares a step to its history. Same task class, best and median per step, green or red delta (LiveSplit, from speedrunning).
  Done when: a closed task's pane row shows each step's delta against the class best, and a test feeds a fixture ledger and asserts the sign.

- **Spend an autonomy error budget, SRE-style** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user's recurring pain is unattended runs going wrong (the Stop-hook harness hijack, the paid-binary leak). Each project gets a budget of bad outcomes (reverts, guard saves, interventions). Overnight and bypass work stays on while the budget lasts. Once it is spent, Foreman drops to supervised until a clean streak refills it.
  Done when: after N seeded incidents, `fm night` refuses unattended jobs and prints the burn and the refill condition.

- **Diagnose FIX tasks by differential, with per-repo base rates** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: assumption: FIX plans jump to the first cause. Before the first edit, require 3 hypotheses, each with a discriminating command. Record which one won. Next time, the repo's winners (env, stale cache, path, race) come first.
  Done when: `fm task plan` on a FIX rejects fewer than 2 hypotheses, and the closed task logs the winning category that seeds the next ordering.

- **Contact-trace a bad lesson or fix, then issue corrections** — FEATURE — value 4 — effort M — risk low — category: learning integrity
  Why: fixes retire "when they stop working" but nobody reviews what they already touched. Each hint application is logged with session and task. When a hint is retired or a commit is bisected as bad, list every task that consumed it, mark those tasks "exposed", and re-run their proofs (epidemiology, plus a newspaper corrections policy).
  Done when: retiring a fixture hint outputs exposed task ids and re-runs their recorded verify commands.

- **Limit work in progress by review debt (Little's law)** — FEATURE — value 4 — effort S — risk low — category: fleet
  Why: the user asked for many lanes, worktrees and overnight work, but nothing measures how fast they review. Compute throughput and unreviewed-done count from the ledger. Past a threshold, `fm night` and lane dispatch hold, and the morning digest says why.
  Done when: with 5 unreviewed closes in a fixture, dispatch refuses and names the count and the clearing action.

- **Draw control charts for Foreman's own metrics** — FEATURE — value 3 — effort S — risk low — category: self-measurement
  Why: hook latency, interventions per task and idle minutes are already measured, but "got worse" is judged by eye. Apply Western Electric rules (statistical process control, from manufacturing) so only real drift raises a task, not noise.
  Done when: a synthetic series with a step shift fires one alert, and pure noise fires none.

- **Map fault lines from Foreman's own failures** — FEATURE — value 4 — effort M — risk low — category: risk
  Why: behavioural code analysis (hotspots) usually reads git churn. Foreman knows more: which files had reopened tasks, undone closes, red-then-green loops and guard blocks. Inject a one-line warning at edit time for the top fault-line files, with what went wrong last time.
  Done when: editing a file with 2 prior failed closes shows the warning once per session, with the task ids.

- **Record user rulings as precedent, with facts, and cite them** — FEATURE — value 4 — effort M — risk med — category: judgment
  Why: corrections and steers are logged but stored as flat rules. Store each as a holding plus the facts that triggered it. At gray-zone moments (guard, UI layout, scope), cite the closest precedent and say if it is being distinguished. Overruling needs the user's explicit word (stare decisis).
  Done when: a seeded steer is cited on a similar case, and `fm why` shows the cited ruling.

- **Reinforce rules on a forgetting curve** — FEATURE — value 3 — effort M — risk med — category: tokens
  Why: the user wants fewest tokens and everything automatic. Always-on rules cost context whether or not they are being violated. Inject a rule loudly just before its measured violation interval comes due, and quietly or not at all while it holds (spaced repetition). Assumption: violations are attributable per rule.
  Done when: a rule with zero violations in 10 tasks stops injecting, and a violation re-arms it at the next edit.

- **Enter a sterile cockpit during risky phases** — FEATURE — value 3 — effort S — risk low — category: focus
  Why: aviation silences all non-essential chatter during takeoff and landing. During a migration, release or force-push-adjacent step, Foreman suppresses ideas, cards, notices and brainstorm output and shows only the checklist. This addresses the user's complaints about clutter and things going in and out of view.
  Done when: in marked phases the hook outputs only checklist lines, and a test confirms normal output returns after.

- **Wild: Run lanes as an auction with reputation and calibration** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: wild. Before dispatch, each candidate (model, tier, specialist) quotes tokens, minutes and p(pass) from the forecast table. Lowest expected cost wins, then settles against actuals. A Brier-scored reputation per bidder corrects overconfident quotes over time.
  Done when: two stub bidders with fixture histories produce a deterministic winner, and the settlement updates reputation.

- **Wild: Detect strange tool sequences by negative selection** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: wild. Instead of writing more deny rules, learn the "self" of the user's normal tool-call n-grams (tool, path class, command class) per project, as the immune system does. In bypass mode, a very rare sequence gets a one-line pause. Assumption: a few weeks of ledger is enough to train.
  Done when: replaying a ledger with an injected exfil-shaped sequence flags it, and a normal held-out session raises under 1 flag.

- **Wild: Prove the guard on a bounded command grammar** — SECURITY — value 4 — effort M — risk low — category: provable safety
  Why: wild. T-0275 (guard reads what a command runs) shows bypasses are the live risk. Exhaustively enumerate a small grammar (wrappers, quoting, env prefixes, pipes, subshells) over each never-run command and assert the guard never allows it. Report the grammar size and any counterexample.
  Done when: `fm doctor --prove-guard` prints "N variants, 0 allowed", and a deliberately weakened rule yields a counterexample.

- **Wild: Verify receipts offline from a hash-chained ledger** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. "Say tests pass" is Foreman's founding distrust. Chain each ledger line to the previous hash and anchor the head in a git note at each close. Then `fm verify <task>` lets a stranger check, offline, that the evidence preceded the close and is untampered (a transparency log, from cryptography).
  Done when: editing one old ledger line makes `fm verify` fail and name the first broken line.
