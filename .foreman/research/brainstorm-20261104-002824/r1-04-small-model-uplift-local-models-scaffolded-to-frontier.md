# Brainstorm — lens: small-model uplift: local models scaffolded to frontier

- **Verify local drafts with the brief's own Exam** — FEATURE — value 5 — effort M — risk low — category: local verifiers
  Why: every brief already carries a runnable Exam that reads live state, and local tokens cost nothing. Sampling N drafts and keeping the first one whose Exam passes lets a 27B reach frontier-grade briefs without a frontier judge.
  Done when: on 20 held-out closed tasks, `sampo louhi` shows the Exam-selected 27B brief pass the Exam at least as often as the single-shot frontier brief, with the token split printed.

- **Force briefs through a grammar** — FIX — value 4 — effort S — risk low — category: constrained output
  Why: T-2893 shows local generation drifting (empty replies cut by length, malformed output). Constraining decoding to the brief schema (Title, Done-when, Exam with `outcome:` and `live:` lines) removes the format failures that make small models look worse than they are.
  Done when: 100 local brief drafts parse with zero format rejections, and a test confirms a grammar-less run fails at least once.

- **Queue local jobs by loaded model** — PERFORMANCE — value 4 — effort M — risk low — category: scheduling
  Why: a switch on the llama-swap endpoint costs about 3 minutes, and the steer says to use the 27B for everything first. A scheduler that batches every pending local job per model, and switches only at a batch boundary, stops the overnight run from thrashing.
  Done when: a mixed 30-job night causes at most 1 model switch, and the receipt prints the switch count and minutes saved.

- **Draft the predicted ask speculatively and verify it cheaply** — FEATURE — value 5 — effort M — risk med — category: anticipation
  Why: this Mission is to predict the next request and draft it on spec. Use the cascade from speculative decoding. A decision model (kev/tev1/d3) says whether a prediction is worth drafting, the 27B drafts it on a branch, and the Exam passing is the only gate before it reaches the morning card.
  Done when: the morning card lists only drafts whose Exam passed, and the abstain rate of the decision model is shown beside the draft count.

- **Pick the scaffold rung per task kind and model** — FEATURE — value 4 — effort M — risk med — category: scaffolding
  Why: T-1266 wants a ceremony profile per task kind from duel data. The ladder here is raw, then exemplars, then grammar, then best-of-N, then critic, then escalate. Each local model gets the cheapest rung that matches its frontier pass rate on that kind.
  Done when: `sampo louhi models` prints a table of kind × model → chosen rung → pass rate vs frontier, and the rung changes when seeded results change.

- **Escalate to frontier only when local models disagree** — PERFORMANCE — value 4 — effort S — risk low — category: cost routing
  Why: the 27B and the 35B MoE are both available and the frontier costs real money against the $200 cap. Agreement between two cheap readers is a signal, so frontier calls happen only on a split.
  Done when: over a held-out set, frontier calls drop by at least half while the final pass rate stays within 2 points of always-frontier.

- **Few-shot from the user's own accepted briefs** — FEATURE — value 4 — effort S — risk low — category: retrieval
  Why: the ledger holds briefs the user accepted and dropped. Embedding retrieval (the planned qwen3-embedding plus a reranker) can pull the 3 nearest accepted briefs and 1 dropped one into the local prompt. That teaches the 27B this user's taste without fine-tuning.
  Done when: an A/B on 20 tasks shows exemplar-primed drafts needing fewer user edits than unprimed ones.

- **Turn each local failure class into a targeted scaffold and a regression case** — CLEAN — value 4 — effort M — risk low — category: failure atlas
  Why: the steer asks to study where the local models fail on Sampo's real work. Each recorded failure class (loop, truncated output, ignored constraint, hallucinated path) gets one named scaffold and one case in the model bench, so fixes are measured rather than anecdotal.
  Done when: the Models section of the site lists at least 5 failure classes, each with a scaffold and a before/after rate.

- **Set the reasoning switch per step** — PERFORMANCE — value 3 — effort S — risk low — category: thinking budget
  Why: T-2893 adds `enable_thinking` and a token budget. Classification and routing steps run with thinking off, and planning and Exam writing run with it on. The setting is picked by the per-step pass rate rather than by hand.
  Done when: a per-step table shows thinking on/off and token cost, and the chosen setting beats the all-on setting on cost at equal pass rate.

- **Wild: Simulate the user and score the simulator** — FEATURE — value 4 — effort L — risk med — category: user model
  Why: wild. The 27B plays this user from their ledger, steers and drops, then writes the next three asks. Each prediction is scored against what was actually typed, and the persona is rewritten from the edit diffs. assumption: ~200 usable ask records exist.
  Done when: the simulator's top-3 hit rate on a held-out week is reported next to the recency baseline, and it is muted if it loses to it.

- **Wild: Pin the user profile as a persistent KV-cache prefix** — PERFORMANCE — value 3 — effort L — risk high — category: local inference
  Why: wild. A digest of steers, repo map and recent ledger sits as a cached prefix on the 27B endpoint, so each anticipation call pays only for its delta. This makes hundreds of overnight predictions affordable. assumption: the llama-swap backend exposes prompt caching.
  Done when: median time-to-first-token on the 20th anticipation call is at least 3× faster than on the first.

- **Wild: Let local models write the test before the code** — FEATURE — value 4 — effort L — risk med — category: execution feedback
  Why: wild. The small model writes a failing test first, then loops writing code against real execution output, retrying unattended all night. Only a green run is shown to the user. This gives small models the red-first discipline Sampo already enforces.
  Done when: on 10 S-sized FIX tasks, the loop closes a measurable share with a passing test and a diff, with zero frontier tokens spent.

- **Compare local+scaffold against frontier and publish the gap** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: the steer is "scaffolded to frontier results", but no number yet shows the distance. A Louhi arm runs each scaffold rung against frontier on identical held-out closed tasks, so each claim of uplift is measured and shown on the Models section.
  Done when: the site shows one row per task kind with frontier pass rate, best local rung pass rate and the gap, regenerated by `sampo louhi`.

Next question: Which of the 27B's failures on Sampo's own work come from the model, and which from a prompt or parser Sampo itself wrote?
Next question: If the decision models abstain most of the time, does the anticipation cascade save anything, or does it only add a hop?
