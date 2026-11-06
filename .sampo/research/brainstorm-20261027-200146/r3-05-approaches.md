# Brainstorm — lens: approaches

- **Send brainstorm rounds only the delta since the last round** — FEATURE — value 5 — effort S — risk low — category: token cost
  Why: Each lens re-reads the full pack, including the long "Ideas so far" list and the user-words block, every round. Assumption: most of that text is unchanged between rounds.
  Done when: Round 2's child packs are under 30% of round 1's bytes, and no idea the ledger already holds reappears in the output.

- **Split the idea ledger by category so each lens reads only its shard** — PERFORMANCE — value 4 — effort S — risk low — category: token cost
  Why: The pack lists over 300 ideas, and every lens gets all of them. Assumption: a "deepen: performance" lens needs only the performance ideas to avoid repeats.
  Done when: A lens child's pack holds only its category's ideas plus a count of the rest, and the duplicate-idea check still passes.

- **Write parametric playbooks: one template plus a parameter table** — FEATURE — value 4 — effort M — risk low — category: playbook scale
  Why: Assumption: thousands of playbooks are variants of a few shapes (same steps, different tool, path or framework). plugin/skills/ already holds 1229 entries.
  Done when: Ten variants generated from one template pass the same tests, and the file count for that family drops by at least 90%.

- **Load a playbook's body only when its neighbours are also routed** — FEATURE — value 3 — effort M — risk med — category: routing — wild
  Why: Assumption: playbooks used together (for example, a test playbook after an edit playbook) show up in the journal as a co-use graph that can be read locally.
  Done when: After a run that uses A, the neighbour B is in memory before it's asked for, and median time-to-first-token for B drops.

- **Give each playbook a one-line stub that expands only when a live task links to it** — FEATURE — value 4 — effort M — risk low — category: library size — wild
  Why: Only a few playbooks are used in a given week, but all are indexed in full. Assumption: a Wikipedia-style stub (lead sentence plus a link) routes as well as the full body.
  Done when: A catalog of 10,000 stubs fits under 200 KB, and a routed stub expands to its full body in one read.

- **Replace the per-command hooks with a single static router binary** — PERFORMANCE — value 4 — effort M — risk med — category: hook latency
  Why: The PreToolUse:Bash script p95 was about 310 ms against a 300 ms budget, and the hooks are scripts. Assumption: most of the cost is interpreter startup, not the logic.
  Done when: `bench_hooks --runs 20` at load 0.6 per core reports PreToolUse:Bash p95 under 100 ms.

- **Batch-gate queued fixes and bisect only when the batch fails** — PERFORMANCE — value 3 — effort M — risk med — category: gate throughput
  Why: Each fix runs its own gate, and the gate queue serializes them. Assumption: most queued fixes pass, so one batch run covers most of them.
  Done when: Ten fixes gate in one run when all pass, and a planted bad fix in the batch is isolated in at most four extra runs.

- **Move low-risk checks from every tool call to the commit** — FEATURE — value 3 — effort S — risk med — category: do less
  Why: Some hook checks, such as style and doc-link checks, run on every call and cost the most where a per-call hook is slowest. Trade-off: a problem is caught later, at the commit instead of at the edit.
  Done when: The listed checks no longer run on PreToolUse and still fail `fm check` on a planted violation before close.

- **Use the host's native skill matcher and retire Foreman's own routing for skills** — FEATURE — value 3 — effort M — risk med — category: reuse
  Why: Claude Code already matches skills by description. Assumption: Foreman's routing adds little beyond what native matching does for ordinary skills. Trade-off: the gate and proof hooks still need Foreman's own routing.
  Done when: The same 50 requests route to the same skill with native matching as with `fm playbooks route`, and routing accuracy holds.

- **Roll each new playbook out to 1% of routes before it is listed** — FEATURE — value 3 — effort M — risk low — category: safety rollout — wild
  Why: Routing a bad playbook to every request is the failure mode the library scale work risks. Assumption: a small share of traffic gives enough signal to catch a regression.
  Done when: A playbook that fails its proof on the canary share is held back from the full catalog, with the reason recorded.

- **Store cold playbooks as git objects and load them with sparse checkout** — FEATURE — value 2 — effort M — risk med — category: storage — wild
  Why: Git already stores, deduplicates and fetches objects, so Foreman needs no loader of its own. Assumption: sparse checkout is fast enough for a per-request read.
  Done when: A cold playbook loads from a sparse checkout in under 50 ms, and the repo's clone size stays flat as the library doubles.

- **Run each playbook's examples in a network-less namespace** — SECURITY — value 3 — effort S — risk low — category: sandboxing
  Why: Playbook examples run shell commands from the library. Assumption: examples should need no network to prove their claim.
  Done when: An example that tries an outbound request fails inside the namespace, and every existing example still passes there.
