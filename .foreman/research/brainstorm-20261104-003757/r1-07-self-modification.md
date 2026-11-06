# Brainstorm — lens: self-modification

- **Build before you install** — FEATURE — value 5 — effort M — risk low — category: tool acquisition
  Why: The dropped "Missing tool shellcheck" item shows the no-installs rule already makes a find-or-install flow a dead end. Assumption: a stdlib or vendored single-file script covers most such gaps.
  Done when: for a planted missing tool, `sampo` walks a fixed ladder (host-native → stdlib script → vendored single file → queued grant), stops at the first rung that passes its test, and prints which rung it used.

- **Quarantine every acquired tool** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Why: T-0791 (injection and supply-chain defenses) is deferred, and the rea source feed brought in a plugin nobody vetted. Assumption: found plugins, MCP servers and scripts currently run with the session's own rights.
  Done when: a found tool runs its first test in a no-network scratch home under the Ward, its hash and provenance are recorded, and a planted exfiltrating tool fails that run.

- **Write a small-model card for every tool acquired** — FEATURE — value 5 — effort M — risk low — category: small-model cards
  Why: the standing steer asks for thousands of cards, and T-2909 only just built the card store. A tool with no card is useless to a 4B model.
  Done when: each new tool emits a card (call form, 3 examples, 2 failure shapes), and qwen3.5 9B, given only the card, runs the tool correctly on 3 held-out tasks.

- **Keep a skill only if it lifts a local model** — FEATURE — value 5 — effort M — risk med — category: uplift gate
  Why: T-2908 gives Louhi a local-model arm, and the steer says a skill must earn its place. Without a gate, the 1,396 skills grow unchecked.
  Done when: a new skill is admitted only if the local arm with it beats the arm without it on held-out scenarios, and a skill that fails twice is retired with its reason recorded.

- **Retrieve the top skills for a prompt instead of listing them** — PERFORMANCE — value 4 — effort M — risk med — category: skill routing
  Why: 1,396 skill files, plus a steer to reach thousands, cannot all sit in descriptions. Moonscale's embedding funnel already exists to reuse. Assumption: skill descriptions are currently injected rather than retrieved.
  Done when: injected skill text stays under a fixed character budget at 5,000 skills, and top-3 recall on held-out prompts is measured and reported.

- **Dedupe skills with the Moonscale funnel** — CLEAN — value 3 — effort S — risk low — category: skill hygiene
  Why: the cheap-first funnel (exact, embedding, then judge) is built for moons and fits skills equally. Mass skill generation will otherwise produce near-duplicates.
  Done when: running the funnel over plugin/skills reports clusters, and merging one cluster raises no regression in the routing test.

- **Queue grants as one reviewable card** — FEATURE — value 4 — effort S — risk low — category: grants
  Why: the user steered "stop asking me for stuff", but the mission says install grants are queued. Assumption: grants are currently scattered.
  Done when: a single card lists each pending grant (exact command, size, hash, what it unlocks, a demo of the need built from a shim), grants expire after N days, and no prompt fires mid-run.

- **Pre-build tools for the stack before they are needed** — FEATURE — value 4 — effort M — risk low — category: initiative
  Why: the #1 Initiative steer finds ecosystem tools from manifests and stack cards, and missing ones are queued through #5. Assumption: that handoff only happens after a failure.
  Done when: for a repo with a Python manifest, an overnight lane builds or queues the missing linter before any session hits it, and `fm doctor` lists the result.

- **Give each acquired tool a retire-when probe** — CLEAN — value 3 — effort S — risk low — category: tool registry
  Why: the open question about the host adding overlapping features applies to built tools too. Assumption: there is no registry with last-used and upstream-equivalent fields.
  Done when: every built tool has a registry row with tests, last-used date and a probe, and a tool unused for 60 days is flagged.

- **Wild: hold a tool-building tournament** — FEATURE — value 4 — effort L — risk med — category: small-model uplift (wild)
  Why: wild. The 27B, the 9B and a frontier model each build the same missing tool from one spec, and a different model writes the tests. The winner's script is kept, and each loser's failures become cards.
  Done when: one run produces a ranked table, the kept tool passes a held-out test, and at least one card is written from a loser's failure.

- **Wild: evolve playbooks overnight** — FEATURE — value 4 — effort L — risk med — category: skill evolution (wild)
  Why: wild. Playbooks are stored as step lists. A local model mutates one step each night, the exam replays, and a win is kept while a loss is reverted and logged.
  Done when: a playbook's local-arm score rises over 5 nights with every kept mutation traceable, and the held-out score does not fall.

- **Wild: promote repeated shell pipelines into tools** — FEATURE — value 4 — effort M — risk low — category: tool synthesis (wild)
  Why: wild. When any agent runs the same multi-step pipeline 3 times, Sampo drafts a tested script and a card for it. The same agent that ran it then has to run the script and match the output.
  Done when: a planted 3-step pipeline repeated three times yields a script, a test and a card, and the script's output matches the pipeline's.

- **Render one skill per model rung** — FEATURE — value 4 — effort M — risk med — category: scaffolding
  Why: the steer wants 4B to 27B models to match frontier results through scaffolding, and one prose skill won't suit all of them. Assumption: skills are currently written once.
  Done when: one source skill renders as a numbered menu for the 4B and as prose for the 27B, and each rendering is scored on its own model's arm.

- **Vet found plugins with a cold read and vendor them by hash** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: the rea source diff was read by hand and dropped. A found plugin should never auto-update.
  Done when: a found plugin is vendored at a pinned hash, a cold child reports its network, exec and injection surface, and an upstream change raises a diff review instead of updating.

Next question: Which tool gaps in the failure and friction ledgers were closed by a script rather than an install, and does that share justify making the ladder's first rung the default?
Next question: When a skill helps the 27B but hurts the 4B, which model's arm decides whether it is kept?
