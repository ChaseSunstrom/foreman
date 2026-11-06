# Brainstorm — lens: invented: a tool forge that grows every generation

- **Mine tool gaps from closed-task history** — FEATURE — value 5 — effort M — risk low — category: forge intake
  Why: the pack lists "Missing tool shellcheck" dropped, and steers say tools queue via #5; today gaps are noticed ad hoc. A zero-token scan of closed tasks, Ward blocks, `command not found`, and repeated hand-written shell pipelines yields ranked gap records (need, frequency, last seen).
  Done when: `sampo forge gaps` prints ≥5 ranked gaps from the real ledger, each citing the task ids that evidenced it, and a replay over a planted ledger finds the planted gap.

- **Decide build-versus-find with a priced bake-off** — FEATURE — value 4 — effort M — risk med — category: forge decision
  Why: the request says "finds or builds"; nothing picks between them. Search the plugin catalog and a stdlib-only build budget, and compare candidates on the gap's own test, size, dependencies and maintainer age. Record the reason.
  Done when: for 3 sample gaps `sampo forge decide GAP` emits a verdict file naming the chosen path, the rejected path, and a measured reason; the verdict is reproducible on rerun.

- **Quarantine every candidate in a cage before any grant is queued** — SECURITY — value 5 — effort M — risk low — category: forge safety
  Why: the injection and supply-chain defenses (T-0791) are deferred and the standing intent says installs need grants. Run a found tool under the Ward with no network and a scratch home, with a negative-control test that must fail on a broken copy, and only then queue it.
  Done when: a planted tool that writes outside its scratch dir or phones home is refused and logged, and a good tool passes with its negative control failing as designed.

- **Batch grants into one hash-pinned install plan** — FEATURE — value 4 — effort S — risk low — category: forge grants
  Why: "install grants queued" implies one-at-a-time asks, while the user said "stop asking me for stuff". One reviewable card lists every queued tool with hash, size, licence and what it replaces, spent on use per the push-grant pattern.
  Done when: `sampo forge plan` writes one file listing N tools with hashes; applying it installs exactly those and fails if any hash drifts.

- **Write a small-model card for every forged tool** — FEATURE — value 5 — effort M — risk low — category: forge × cards
  Why: the standing steer is that local models match frontier through scaffolding, and T-2909 builds the card store. A tool a 4B can't call is worthless, so each tool gets a fill-in invocation card (arguments, one worked example, one common error) at forge time.
  Done when: for 5 forged tools, qwen3.5 4B calls each correctly from the card alone in ≥4 of 5 held-out prompts, scored by a tool-call exam arm.

- **Score every tool with a with/without exam arm** — FEATURE — value 5 — effort M — risk med — category: forge measurement
  Why: the not-yet items wait on "an exam arm against the path they replace", and lean substance (T-2503) says unmeasured growth waits. Run the same scenarios with the tool and with an inline script, and report lift and cost.
  Done when: `sampo louhi tools` prints a per-tool lift table over held-out scenarios, and a tool with zero lift is flagged as a retirement candidate.

- **Retire tools that never fire on a real path** — CLEAN — value 4 — effort S — risk low — category: forge pruning
  Why: the reach rule demands every capability be called by a session path, and lean growth must earn its place. Count calls, saves and failures per tool; a tool with no calls in 30 days goes dormant, then to a graveyard with a reason.
  Done when: a tool with zero calls over a simulated 30 days moves to `graveyard/` with a reason line, and `sampo forge revive` restores it byte-identically.

- **Detect a native replacement before building** — FEATURE — value 4 — effort S — risk low — category: forge dedupe
  Why: the host keeps adding features and earlier ideas ask who retires overlapping verbs. Before building, probe the host CLI's help and tool list, and the bare model, for an existing equivalent.
  Done when: asking to forge a tool the host already ships returns "native exists: <name>" with no build started, tested against 3 known-native cases.

- **Promote repeated shell pipelines into tools** — FEATURE — value 4 — effort M — risk med — category: forge mining
  Why: the Moonscale funnel already dedupes by shingles, so the same machinery can cluster the command sequences sessions and lanes retype. Three occurrences of one shape (rule of three) draft a script plus test.
  Done when: a planted history with one pipeline repeated 4 times yields exactly one drafted script with a passing test, and a pipeline repeated twice yields none.

- **Wild: Hold a tool bazaar where local models bid to build** — FEATURE — value 4 — effort L — risk med — category: forge tournament
  Why: wild; assumption: the 27B, 35B MoE and 9B each get the same gap and a card ladder, the Exam picks the smallest model whose build passes, and that model's name is printed on the tool.
  Done when: for one gap, three models each submit a build, the held-out test ranks them, and the winner's profile is recorded as the cheapest sufficient builder.

- **Wild: Let a failed tool grow a sibling** — FEATURE — value 3 — effort M — risk med — category: forge evolution
  Why: wild; the no-idea-killed rule says a failed spike gets two or more approaches. When a forged tool fails in a real path, the failure becomes a new test and a differently-approached variant is built; both compete on the exam arm.
  Done when: a tool with a planted failure produces a sibling with a different approach, and the one that passes the added test is kept while the other is graveyarded with its blocker.

- **Wild: Keep a tool graveyard that teaches** — FEATURE — value 3 — effort S — risk low — category: forge memory
  Why: wild; retired and refused tools stay with their reason, and the forge searches them before building so it never rebuilds a known dead end, with the blocker re-tested when a new capability arrives (the Seed retry rule).
  Done when: requesting a graveyarded tool shows its reason and blocker, and when the blocker predicate flips the item is re-queued automatically.

- **Publish forged tools as host-neutral passports** — FEATURE — value 3 — effort M — risk low — category: forge export
  Why: the standing rule says Sampo isn't Claude-specific, and non-Claude harnesses lack the plugin format. One manifest (command, args schema, test, retire-when, hash) with thin adapters for MCP, skill and plain script.
  Done when: one forged tool installs as a skill in Claude Code and as an MCP server for a second harness from the same passport, each passing the tool's own test.

Next question: When a forged tool is correct but a small model still misuses it, is the fix a better card, a narrower argument schema, or a wrapper script, and which has the best measured lift per character of context?
Next question: What stops a forged tool from silently becoming the thing it was meant to replace (a second, undeclared copy of a host or Sampo verb), and who notices?
