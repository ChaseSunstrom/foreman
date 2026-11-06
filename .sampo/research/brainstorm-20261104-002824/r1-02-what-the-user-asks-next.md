# Brainstorm — lens: what the user asks next

- **Draft the next ask as a filed, dormant brief** — FEATURE — value 5 — effort M — risk med — category: anticipation core
  Why: the request is "predicts the next request and drafts it on spec in a lane". The user's words show the next ask is usually a sibling of the last one: T-2884 followed by T-2886/2887/2894, and the drive fix followed by a second and third drive fix (T-2900, T-2901, and the "misses running subagents twice more" asks). Assumption: ask history in the ledgers is enough for a table keyed by task kind.
  Done when: after a task closes, `fm next` shows one dormant draft carrying Done-when and Exam lines, and the draft is promoted or discarded by the user's next message, with the outcome logged.

- **Forecast sibling fixes after any FIX closes** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: the drive-counting bug was reported three times in a row (T-0575 pattern, then T-0115, then the union fix) because each fix covered one reader. Assumption: the "twin" scan already built (T-2884) can list sibling readers.
  Done when: closing a FIX prints the other readers of the same signal, each as a candidate task, and a replay of T-2873 yields the T-2901 class as a candidate.

- **Hold a "wild enough" gate on moons before the user sees them** — FEATURE — value 4 — effort M — risk med — category: moons
  Why: the user said "the moons aren't that wild, I want wild" and the standing rule scores wildness 1-5. Assumption: the user will push back again when output feels samey. Anticipate by rejecting any moon whose nearest neighbour in the catalogue scores above a similarity bar.
  Done when: `sampo genesis moon` prints a nearest-neighbour distance and drops candidates under the bar, and a held-out set of the user's rejected moons all fall below it.

- **Pre-warn on the local-model switch cost** — FEATURE — value 4 — effort S — risk low — category: machine model
  Why: a llama-swap switch costs about 3 minutes with no detection, and the user already steered to use qwen3.8-27b first. Assumption: Foreman can note the last model it called per endpoint.
  Done when: a lane that would swap the loaded model prints the cost and batches same-model work first, and the plan order shows fewer switches than FIFO on a test queue.

- **Predict naming and terminology corrections** — FIX — value 4 — effort S — risk low — category: user model
  Why: the user corrected "jarvis", "Claude as orchestrator" and "jeff/jev" within one session. Assumption: those corrections generalise into banned strings per surface.
  Done when: a lint run on site, README and scene text fails on a name from a stored "never show" list, and adding a steer adds a list entry.

- **Flag a brief whose premise the machine has already changed** — FEATURE — value 4 — effort M — risk low — category: problems before they happen
  Why: dropped asks ("not a breakage", "stale: the cold-read list names paths now shims", "premise already met") show filings aging past their facts. Carried gap: every brief's Exam reads live state.
  Done when: at pickup, each open brief's Exam reading runs, and a brief that already passes is parked with the reading shown.

- **Pre-stage the "ship the landed commits" ask** — FEATURE — value 4 — effort S — risk med — category: ship
  Why: the user asked to ship T-2848…T-2858 and the CHANGELOG, a recurring ask under the standing push grant. Assumption: the batch list is derivable from landed, unshipped tasks.
  Done when: a session that has unshipped green closes older than 6 hours shows a drafted ship plan with the task ids, and `fm ship` accepts it unchanged.

- **Forecast the drive's false waits** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: three drive fixes in a row on how it counts running subagents. Assumption: waits longer than twice the median with no ledger activity are the signal.
  Done when: the drive writes a "suspected stuck wait" line to the morning card with the evidence, and a replay of the T-2873 incident raises it.

- **Wild: Seal the user's next three asks before the night starts** — FEATURE — value 4 — effort M — risk low — category: forecasting — wild
  Why: the user sleeps and wants progress by morning; a sealed forecast scored against the morning's first messages gives an honest hit rate. Assumption: scoring by task kind is enough.
  Done when: the morning card shows the sealed list beside what was asked, with hits counted.

- **Wild: Let the predictor write the morning's first message as a draft** — FEATURE — value 3 — effort M — risk med — category: delight — wild
  Why: the user's messages are long, specific bundles ("Model bench part 2: …"). A draft in their compression, edited and sent, teaches the model by the edit.
  Done when: the user's edits to the draft are stored, and the similarity between draft and sent text rises over a week.

- **Wild: Run a rehearsal lane on the top predicted task in a scratch worktree overnight** — FEATURE — value 4 — effort L — risk med — category: unattended — wild
  Why: the user wants major progress by morning, and local models are idle. Assumption: a branch that expires in three days limits harm.
  Done when: in the morning `fm next` shows a rehearsed branch with its tests, kept or discarded by one key, and a discarded one leaves no files outside the scratch tree.

- **Mine the user's pushbacks as negative priors** — FEATURE — value 4 — effort S — risk low — category: user model
  Why: "stop asking me for stuff" led to a standing rule, but earlier the model asked anyway. Pushbacks and drops are the cheapest signal.
  Done when: each pushback is tagged with a class, and a repeat of the class inside 14 days is counted as a miss on the doctor line.

- **Warn when a predicted ask needs a user-only grant** — FEATURE — value 3 — effort S — risk low — category: blockers
  Why: T-0325, T-0352 and T-0418 sit blocked on installs or publishing. Assumption: the blocker is already recorded per task.
  Done when: a draft that depends on a blocked item says so with the one user action that frees it.

Next question: which predictions would the user be annoyed to see even when they're right, and does the ledger record any such reaction?
Next question: how many past asks are there with a clean "before" ledger state, enough to backtest any predictor above a recency baseline?
