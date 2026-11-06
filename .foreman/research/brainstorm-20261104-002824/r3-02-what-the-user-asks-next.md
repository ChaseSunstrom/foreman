# Brainstorm — lens: what the user asks next

- **Draft the "ship the landed commits" ask before the user types it** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: the first user ask listed is "Ship the landed commits to main: T-2848, T-2840…" and the push grant is standing. Shipping after a batch of closes is a repeated ask. Assumption: the ask recurs after most batches.
  Done when: after three or more closes land unshipped, `fm next` prints a ready `fm ship` line naming those task ids, and a test over a fixture ledger shows it appears and then vanishes after the ship.

- **Re-ask detector for drive-wait bugs** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2873, T-2874, T-2900 and T-2901 are four consecutive asks about the drive miscounting running agents. The user had to find each one. Assumption: a fifth variant exists (resume, different shell kinds).
  Done when: a replay test feeds recorded event tails (killed agent, resumed session, a subagent's shells) and the drive's running count matches ground truth in every one.

- **Warn before a local model switch costs 3 minutes** — FEATURE — value 3 — effort S — risk low — category: machines
  Why: steer: a llama-swap switch costs about 3 minutes with no detection, and the user said use qwen3.8-27b first and switch late. Assumption: queued jobs mix models.
  Done when: the night's queue is ordered by resident model and the plan prints "model switches: N", with a test that mixed jobs give N=1.

- **Lint public surfaces for banned names** — CLEAN — value 4 — effort S — risk low — category: steer enforcement
  Why: the user corrected "jarvis" and "Claude as orchestrator" in the scene copy. Steers must become automatic checks per standing rule. Assumption: the same slips recur in the site, README and scenes.
  Done when: `fm genesis sweep` fails on a planted "jarvis" or "Claude orchestrates" in site/ or README and passes on the real tree.

- **Make every moon carry a wildness score before the user sees it** — FEATURE — value 5 — effort M — risk med — category: moons
  Why: the user pushed back twice: "not that wild, I want wild". The wildness gate exists in a steer; the evidence is that moons still read tame. Assumption: a cold-rated score plus a wild-5 anchor set is enough.
  Done when: no moon under wildness 4 appears on the landing or in the tower, and a planted tame moon is held back in a test.

- **Predict the next question from the last close's caveats** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: the asks come in clusters (Moonscale part 1, part 2; model bench part 1, part 2). Part 2 is predictable from part 1's "Left out". Assumption: finish text lists caveats.
  Done when: closing a "part 1" task drafts a dormant "part 2" brief from its deferred remainder, and a test shows the draft cites the caveat line.

- **Pre-flight a request against the open work it duplicates** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the dropped list is full of "already built" and "absorbed by T-2893". Assumption: most drops are catchable at filing.
  Done when: filing a title that matches an open or closed task prints that task's id first, and a replay of the five dropped items flags at least three.

- **Hold the morning card as a sealed forecast** — FEATURE — value 3 — effort M — risk low — category: overnight
  Why: the user sleeps and wants progress by morning. Assumption: a night plan sealed at bedtime can be diffed against the result.
  Done when: bedtime writes a plan file with expected closes and spend, and the morning card shows plan against actual, with a test using a fake ledger.

- **Wild: Rehearse the top predicted task in a scratch worktree overnight** — FEATURE — value 4 — effort L — risk med — category: anticipation
  Why: wild. Idle local-model hours go unused while the user sleeps. Assumption: a draft is cheap to throw away and never lands unasked.
  Done when: by morning a branch holds a draft marked "predicted, not asked" with its Exam output, and nothing is merged to main.

- **Wild: Score a ghost user's three asks each night** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: wild. The tower has no measure of whether its model of the user is right. Assumption: next-day typed asks are a usable answer key.
  Done when: each morning prints "predicted 3, hit N", based only on user-typed asks, and mutes the predictor after 14 days below the recency baseline.

- **Wild: Offer "wilder" as a single key on any moon** — FEATURE — value 3 — effort S — risk low — category: moons
  Why: wild. The user's recurring complaint is tameness; a one-key escalation turns it into steering a local mutator. Assumption: the local 27B can rewrite a moon more extremely.
  Done when: pressing the key produces a new moon with a higher cold wildness score, and the old one is kept with a lineage link.

- **Flag a brief whose premise the machine already changed** — FIX — value 3 — effort S — risk low — category: briefs
  Why: dropped items such as "stale: the list names fm*.py paths, now shims" and "premise already met". Assumption: these are checkable by a path and command check at pickup.
  Done when: picking up a task that cites a missing path or a satisfied Done-when prints the reason before work starts, and a test covers both.

Next question: which of the user's repeated asks (ship, rename wording, drive-wait fixes) can be answered by a read-only zero-token check before a model is ever called?
Next question: when the user says "stop asking me for stuff", which exact prompts did they see just before, so the next brainstorm can find the remaining ones?
