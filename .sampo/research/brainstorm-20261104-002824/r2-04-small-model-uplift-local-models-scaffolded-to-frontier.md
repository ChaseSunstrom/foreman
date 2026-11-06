# Brainstorm — lens: small-model uplift: local models scaffolded to frontier

- **Draft the predicted ask as a grammar-constrained brief** — FEATURE — value 5 — effort M — risk low — category: local drafting
  Why: the request is to draft the next request "on spec"; models served by llama-swap/Ollama support JSON-schema or GBNF output, and a brief has fixed fields (Done-when, Exam with outcome and live lines, Reads). Ideas so far list "force briefs through a grammar" only as a line, not a pipeline: the grammar is generated from the brief template, so a 27B cannot emit a brief missing its Exam.
  Done when: 50 drafts from qwen3.8-27b all parse with the brief linter, with zero missing Exam or Done-when fields.

- **Verify every local draft by dry-running its own Exam** — FEATURE — value 5 — effort M — risk low — category: verification scaffold
  Why: the carried gap says every brief's Exam reads live state. A draft whose Exam command errors, is vacuous, or already passes on the parent commit is rejected before the user sees it, so a small model's hallucinated commands never reach the queue.
  Done when: a planted draft with a nonexistent `fm` verb in its Exam is rejected, and one whose Exam passes on HEAD is flagged "premise already met".

- **Cite-only slot filling for briefs** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: small models invent file paths and task ids. Give the model a numbered list of real facts (files from fm map, open task ids, verbs from the verb table) and make it fill slots only by index, then render prose mechanically.
  Done when: across 100 drafts, every path and id in the output exists in the repo or the ledger (checked by script).

- **Escalate to frontier only on local disagreement** — PERFORMANCE — value 5 — effort M — risk med — category: routing
  Why: standing steer is local models scaffolded to frontier results, with the user asleep. Sample the 27B three times at differing temperatures; if the structured drafts agree on kind, files and Exam, accept; otherwise spend one frontier call. Cost drops and the frontier is used where it counts.
  Done when: on a held-out set of 30 closed tasks, the escalation rate and the accuracy are reported, and the accuracy is at least that of frontier alone within a stated margin.

- **Queue local jobs by resident model, one swap per night** — PERFORMANCE — value 4 — effort S — risk low — category: scheduling
  Why: the user steer says a llama-swap switch costs about 3 min and /running is not relayed. Sort the night's local jobs by model, run all 27B work first, then one switch to the MoE, never interleaving.
  Done when: a night with mixed jobs logs at most one model switch, shown in the drive receipt.

- **Few-shot from the user's own accepted and dropped briefs** — FEATURE — value 4 — effort M — risk low — category: user model
  Why: the pack's "dropped" and "pushed back" lines show exactly what the user rejects (templated cells, tame moons, jarvis naming). Retrieve the k nearest accepted briefs and the k nearest drops by embedding, and put them in the prompt as positives and negatives.
  Done when: replaying the 8 recorded drops, drafts with negatives never reproduce the dropped pattern, while drafts without them do at least twice.

- **Run a scaffold-ablation league per local model** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the Model bench tasks already exist (T-2886/2894). Add arms: bare, grammar, grammar+verify, grammar+verify+vote, frontier. Publish which rung each model needs per task kind, so the ceremony is picked from data instead of guessed.
  Done when: `sampo louhi models` prints a table of rung by model by task kind, with pass rates on held-out closed tasks.

- **Switch thinking mode per step** — PERFORMANCE — value 3 — effort S — risk low — category: reasoning budget
  Why: T-2893 added a reasoning switch; apply it per step: no thinking for extraction and slot fill, thinking with a large budget for the Exam design and the contradiction check.
  Done when: tokens per draft fall at least 30% against always-thinking, with the verify pass rate unchanged.

- **Skip local drafts when the endpoint is cold or busy** — FIX — value 3 — effort S — risk low — category: reliability
  Why: no /running relay means a draft can block for 3 min on a swap. Use a short timeout probe with a logged outcome, then fall back to the zero-token n-gram predictor rather than hang the drive.
  Done when: with the endpoint stopped, the anticipation tick finishes in under 10 s and writes a "local unavailable" line.

- **Wild: Simulate the user, and score the simulator** — FEATURE — value 4 — effort L — risk med — category: user model
  Why: assumption: a 27B with the user's last 200 asks in a cached KV prefix can write the next message in their voice. Run it each night against the real next ask once it arrives, and keep a running match score. Wild, since it turns the user into a benchmark.
  Done when: a seven-day scoreboard shows the simulator's hit rate on ask kind and cell against the recency baseline.

- **Wild: Make local models write the failing test before the code** — FEATURE — value 4 — effort L — risk med — category: red-first
  Why: the red-first rule exists, and small models are far better at writing a test from a spec than at writing a fix. Split the work: the 27B writes the test, which must fail on HEAD; a second pass writes the fix against it; frontier only reviews.
  Done when: on 20 closed FIX tasks, the local pair produces a test that fails on the parent and passes on the real fix in at least half.

- **Wild: Hold a night league that runs local models on closed tasks and promotes the winner** — FEATURE — value 3 — effort M — risk med — category: self-tuning
  Why: the user is asleep, and quota on the local box is free. Replay yesterday's closed tasks at each rung and model, and pick tomorrow's default from the results, with a morning line saying what changed and why.
  Done when: the morning card names the default model and rung with the margin it won by.

- **Wild: Pin the user profile as a persistent KV-cache prefix** — PERFORMANCE — value 3 — effort M — risk med — category: latency
  Why: assumption: llama.cpp prompt caching can hold a long fixed prefix of the steers, standing intent and brief template. Each draft then pays only for its delta, which makes many cheap sampled drafts affordable for voting.
  Done when: the time to first token of the second draft is under a third of the first on the same prefix.

Next question: which task kinds does the 27B already pass bare, so scaffolding is spent only where it fails?
Next question: when a local draft and a frontier draft disagree, which does the user accept, and does that vary by cell?
