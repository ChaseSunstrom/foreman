# Brainstorm — lens: local models without limit

- **Groom the deferred backlog on local models** — FEATURE — value 4 — effort M — risk low — category: background volume
  Why: the open work lists 30+ "Later from T-07xx/08xx" items, deferred with a "needs evidence" note. Nobody re-checks whether their premise is still true, and a local model can do that at any volume. Each item gets a premise check against the repo, a duplicate-cluster pass and a local-safe label.
  Done when: one overnight run adds `premise: met|open|stale` and `local_safe: y/n` to every deferred item, and a hand-checked sample of 10 agrees with at least 8.

- **Score tool-call reliability per model and route by it** — FIX — value 5 — effort M — risk low — category: reliability
  Why: failed tool calls are up by half. Smith on local models is a new arm (T-2908), and no record says which model fails on which tool or argument shape. Keep a table of failure rate by model × tool × reasoning switch, and let `fm next` and the drive pick the local model and profile with the lowest rate for each task kind.
  Done when: `sampo louhi models` prints a failure-rate matrix from real runs, and a routing test shows a task kind going to a different profile when its rates are swapped.

- **Classify red CI as flaky or real by rerunning it locally** — FEATURE — value 4 — effort S — risk low — category: triggers
  Why: the request names CI watchers, and a red run that wakes a session overnight is waste if it is flaky. Rerunning the failing tests N times is zero-token volume, and a local model only summarises the failure signature.
  Done when: a recorded flaky run produces a "flaky, 2 of 5 failed" note and no session start, and a real failure starts one with the signature attached.

- **Find the concurrency knee of the local endpoint** — PERFORMANCE — value 3 — effort S — risk low — category: capacity
  Why: "without limit" is only real if throughput is known. A model switch costs ~3 min and nothing measures how many parallel requests the endpoint takes before latency collapses. Assumption: llama-swap serves parallel slots.
  Done when: a bench prints tokens/s and p95 latency at 1, 2, 4 and 8 concurrent requests per profile, and the background queue's default width comes from that table.

- **Keep the embedding index warm from file triggers** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: file triggers are in the request, and local embedders are now pinned in install (qwen3-embedding, bge-m3). A save fires a debounced re-embed of only the changed chunks, keyed by content hash and stamped with the model id. Recall and "where is X" then never read a stale index.
  Done when: editing one file re-embeds only its chunks within 60 s, and a query for the new text returns it with no full rebuild.

- **Run unattended local Smith under a strict Ward profile** — SECURITY — value 5 — effort M — risk med — category: safety
  Why: a weaker model on a trigger-born session has more ways to do harm, and the user wants overnight progress without prompts. The profile is a scratch worktree, no network, no writes outside it, and the Ward's refusal list under both the Sampo and Foreman names. Assumption: Smith can take a per-run profile.
  Done when: an exam scenario where a local Smith tries `git push`, a write outside the worktree and a network call gets three Ward refusals, and the run still finishes its in-scope work.

- **Answer `fm ask` with a provisional local proxy** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: the steers say never block on the user for rules, gates or process, but a trigger-born session can still stall on a question. A local model answers from the steers plus the user's past `fm decide` records, and the answer is tagged provisional and put in the morning list for one-key ratify or reverse. It never answers outward actions or grants.
  Done when: a process question at 3am is answered and logged as provisional, and a grant question stays waiting.

- **Show a one-line local subtitle per lane in the pane** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: lanes and agents are hard to read at a glance, and the drive misjudges them. A small local model turns each lane's last 20 events into one plain sentence every minute, which costs nothing in cloud tokens. Add a counter of "tokens kept off the cloud tonight."
  Done when: the pane shows a sentence under each running lane that changes as its work changes, and the counter matches the ledger's local-token sum.

- **Detect stalls by similarity of successive tool calls** — FIX — value 4 — effort S — risk low — category: drive stops
  Why: drive stops appeared (0 to 0.1) and recent fixes were about miscounting running agents. A stall judge that reads embeddings of the last N tool calls and results is cheaper and more direct than inferring from agent counts. A near-duplicate run means looping, and a flat run with no output means waiting.
  Done when: replayed recorded stalls are flagged within 5 ticks, and a replay of normal busy sessions raises zero false alarms.

- **Map every task kind to the cheapest model that passes** — PERFORMANCE — value 4 — effort M — risk low — category: routing
  Why: the steer is to use qwen3.8-27b for everything first and move to the MoE late, since a switch costs ~3 min. Nothing records where the 27B is not needed. Replay closed tasks with the Exam as the grader at each rung (small decision model, MoE, 27B, cloud) and store the first passing rung per kind.
  Done when: a table of kind → rung exists from at least 30 closed tasks, and the drive's pick follows it.

- **Wild: score each hook event for surprise with a tiny model** — FEATURE — value 3 — effort M — risk med — category: sensors
  Why: wild. A 0.5B model reads every hook event's text and scores its surprise from token logprobs. Spikes flag odd tool results, injected text in an issue body or a changed rule file, a cheap always-on sensor that needs no rules written by hand. Assumption: logprobs are exposed.
  Done when: a planted injected instruction in a fake issue body scores in the top 1% of a day's events and raises a note.

- **Wild: ask a local reader for the questions the docs can't answer** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: wild. At idle hours a local model reads MASTER.md and the README cold and writes the 5 questions it could not answer from them. The questions go to a docs-gap list, and a question repeated across nights becomes a task.
  Done when: the list exists after one night, and a question asked 3 nights running appears as a filed item.

- **Wild: replay the user's last month through the free arm and print the counterfactual** — FEATURE — value 3 — effort L — risk low — category: measurement
  Why: wild. The user wants local models used without limit, but has no number for what a night would do. Replay a month of closed tasks on the local rung and print the share the Exam would have passed and the cloud tokens avoided. That shows what unlimited local work buys.
  Done when: one command prints passed, failed and skipped counts for the month with cloud tokens avoided, and a task's replay can be opened.

- **Pin a resident model pair so background work never swaps** — PERFORMANCE — value 3 — effort S — risk med — category: capacity
  Why: a model switch costs ~3 min and the endpoint's `/running` is not relayed, so the drive cannot see it. If llama-swap can hold two models at once, the 27B and a small decision model stay resident and the queue never waits on a swap. Assumption: GPU memory allows the pair.
  Done when: alternating decision and generation calls for an hour shows no call waiting over 10 s, or the bench records that the pair does not fit and why.

Next question: Which background jobs would the user actually accept from a local model without re-checking, and does any ledger record what they re-did by hand after a night?
Next question: When the local endpoint is busy or cold at trigger time, who decides between waiting, skipping and falling back to cloud, and does that choice appear in the morning card?
