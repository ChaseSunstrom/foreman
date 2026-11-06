# Brainstorm — lens: the toolsmith (invented): it builds, tests and keeps its own scripts, project skills and MCP servers, each with a failing-first test and a first real use

- **Pick the form by rule: script, skill, hook or MCP** — FEATURE — value 4 — effort M — risk low — category: toolsmith
  Why: `fm new tool` and `fm new skill` exist (T-2278), but nothing says which a miss deserves. An MCP server adds always-on schema tokens against the lean ratchet. Assumption: builders default to whatever the scaffold offers first.
  Done when: `fm new --for-miss ID` prints the chosen form and a one-line reason, and a fixture miss used once yields a script, not an MCP server.

- **Build hooks and guard rules from repeated corrections** — FEATURE — value 4 — effort M — risk med — category: toolsmith
  Why: the steers show many "never do X again" corrections, and each became a hand-built check (T-2252, T-2327). Assumption: the toolsmith only builds callable tools, never enforcement.
  Done when: a fixture correction repeated in 2 sessions yields a hook or guard rule with a failing-first test and a veto line, and the rule queues behind a user grant.

- **Author each tool's test with a different model than its code** — SECURITY — value 4 — effort S — risk low — category: verification
  Why: the earlier question "which verbs have a model on both sides with no user-owned check" applies directly. The writer's own test shares the writer's blind spots. Assumption: the builder writes both.
  Done when: `fm new tool` records the code model and the test model, and refuses a shelf entry whose test and code share one model unless a user sample is attached.

- **Give every tool a `--selftest` that runs its own failing-first test** — FEATURE — value 3 — effort S — risk low — category: shelf health
  Why: re-testing on environment change needs a uniform entry point. Assumption: tests live beside the tool, not inside it.
  Done when: `tool --selftest` exits 0 on a good tool and nonzero on a mutated copy, and the shelf re-test calls only that.

- **Ablate the shelf in the exam** — PERFORMANCE — value 5 — effort M — risk low — category: measurement
  Why: the standing rule says to use signals Foreman didn't author. No pack idea measures whether built tools help, only whether they pass their own tests. Assumption: shelf-on vs shelf-off runs on the same held-out misses are affordable at Haiku scale.
  Done when: `fm exam` prints solved-rate and cost with the shelf on and off per capability, and a tool that never changes an outcome is flagged.

- **Cap built-tool output and fetch back the rest** — PERFORMANCE — value 3 — effort S — risk low — category: context
  Why: a built parser that dumps 50k lines costs more than the miss did. The compact-output work is already deferred (T-0828). Assumption: tools currently print unbounded text.
  Done when: a fixture tool emitting 10k lines shows a capped summary plus a `--page N` or fetch-back hint, and a test asserts the cap.

- **Generate the permission manifest by tracing the first real use** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: declared effects can lie, and static scans miss runtime paths. Observing the first use (files, network, subprocesses) and diffing it against the declaration is a signal the builder didn't author. Assumption: strace or bwrap is available on the user's Linux box.
  Done when: the first run writes an observed-effects file, and a tool touching an undeclared path fails the diff and goes to the grant queue.

- **Review the diff when a found tool updates, not the whole tool** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: a lockfile with hashes (already proposed) says the code changed but not what changed. Assumption: re-grant currently means a full re-read.
  Done when: bumping a pinned fixture plugin shows a changed-lines card with new network, exec and file calls highlighted, and nothing activates until one word approves.

- **Refuse tool names that shadow a PATH binary or an fm verb** — FIX — value 2 — effort S — risk low — category: safety
  Why: assumption: scaffolds take any NAME, and a shelf `grep` or `git` quietly changes every later session.
  Done when: `fm new tool git` fails with the colliding path, and a namespaced name is accepted.

- **Stamp commits with the miss that caused the tool** — CLEAN — value 2 — effort S — risk low — category: provenance
  Why: a Tool-Miss trailer makes `git blame` answer why a script exists, which retirement and promotion decisions need. Assumption: no trailer convention exists today.
  Done when: commits adding a shelf tool carry `Tool-Miss: T-NNNN`, and `fm doctor` names a shelf tool without one.

- **Wild: Build two independent versions and differential-test them** — FEATURE — value 3 — effort M — risk med — category: N-version
  Why: wild. For parsers and converters, two cold builders working from the same contract disagree exactly where the contract is vague. The disagreements become the held-out cases the user is asked about.
  Done when: a fixture contract yields two implementations, a fuzz diff report lists divergent inputs, and each is resolved into a test.

- **Wild: Shrink every field failure to a minimal fixture** — FEATURE — value 4 — effort M — risk low — category: repair
  Why: wild. When a shelf tool fails on real input, delta-debug the input to the smallest reproducer and commit it as a new failing test before the repair task opens. The pack has "file the failing input" but not shrinking.
  Done when: a planted failure on a 5 MB input produces a reproducer under 1 KB that fails the tool, and the repair task cites it.

- **Wild: Mine the user's shell history locally for tools worth building** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: wild. The user's repeated one-liners are the clearest unspoken capability misses. Reading the history stays on the machine, off by default, and only a pattern count leaves the miner, never the raw lines.
  Done when: with the setting on, `fm tools suggest` lists the top 3 repeated sequences with counts and drafts a failing-first test for one. With it off, nothing reads the history file.

- **Redact secrets from built-tool output before it reaches the transcript** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: assumption: tools that read env files or configs echo tokens. Transcripts and caches may be indexed.
  Done when: a fixture tool printing a fake API key shows `[redacted]` in the session and the event log, and a test asserts it.

Next question: Which of the shelf's tools did the user rewrite or delete by hand, and what would have made the first version right?
Next question: When two projects build different tools for the same miss, who decides which one is canonical, and does the user ever see the choice?
