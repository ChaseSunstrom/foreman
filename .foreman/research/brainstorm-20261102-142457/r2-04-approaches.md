# Brainstorm — lens: approaches

- **Compute the kernel by greedy removal** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: the pack shows 1,388 skill files of 2,125 and many "Later from" deferrals, but no one has measured what is load-bearing. Approach: a nightly scratch-home script drops one module, skill or hook at a time, keeps the removal if `roundtrip.py`, `fm doctor` and `fm drill` stay green, and prints the fixed point as the kernel. This is empirical, where a hand-drawn Lite list is opinion. The cost is a slow run. It misses anything the gates can't see, so pair it with a real-use veto list.
  Done when: `fm lean kernel` prints a module list and a test shows that installing only that list passes the roundtrip e2e.

- **Shell-equivalence audit for each verb** — FEATURE — value 3 — effort M — risk low — category: lean
  Why: assumption: many verbs wrap git or file reads. A cold tool-less child writes the ≤3-line shell replacement from the verb's help string. If it passes the verb's fixture tests, the verb becomes a deletion candidate. It reuses tools already on the machine, but it can't see hook-time or ledger side effects.
  Done when: running it over every verb produces a table of verb, replacement line and fixture result, with at least one verb marked equivalent or none marked and the reason given.

- **Lean lockfile reviewed like a dependency lock** — CLEAN — value 4 — effort S — risk low — category: lean
  Why: the pack's lean row is pending-measurement and prose-based. A checked-in `lean.lock` holds verb count, flag count, injected tokens, exec-able binaries, effect sites and bytes. `fm ship` fails when it differs from the build unless the commit adds a one-line reason. Cheap and reviewable, but it only records growth, not whether it was earned.
  Done when: a red-first test adds a flag without updating `lean.lock` and `fm ship` refuses with the diff.

- **Run Foreman's own suite under the guard in bypass mode** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: the guard stops commands in bypass mode, but nothing shows Foreman's own test and drive paths stay inside their declared write set. Run the full suite in a bwrap or Landlock sandbox that allows only the repo, tmp and the state dir. Every denial is a finding. It reuses OS tools and adds no new code, at the price of Linux-only coverage.
  Done when: the sandboxed suite run exits green, or each denial is filed as a task naming the writer.

- **Pay-down ledger for additions** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: the steers say growth must be measured, and the lean row only waits. Each merged capability opens a "debt" of its weighted size with a 30-day due date. Deletions repay it, and `fm doctor` shows one line with the balance. This is softer than a hard swap rule and keeps the sweep from turning red. The risk is that it nags with no teeth.
  Done when: a test merges an addition, sees the debt line appear, then merges a deletion and sees it cleared.

- **Safe-by-default install profile with no unattended outward effect** — SECURITY — value 4 — effort M — risk low — category: safety
  Why: assumption: first install enables timers, publishing and the web UI together. The approach is to ship with every outward path off. The user turns each on by name, and `fm doctor` lists what is off and what enabling costs. It is simplest to prove, but it lowers early capability.
  Done when: a fresh-home install test finds no unit, listener, push grant or network call until an explicit `fm enable` runs.

- **Differential ship: compare the pushed tree's effect surface** — SECURITY — value 3 — effort M — risk low — category: safety
  Why: recent commits show ship gates by tests only. Extract an effect surface from each tree (subprocess targets, open modes, socket calls via AST) and diff it against the parent. A new effect needs a reason line. It reuses static analysis instead of runtime tracing, and it can't see dynamic calls.
  Done when: a test that adds a new `subprocess` call to `plugin/lib` makes the diff report it.

- **Wild: a minimiser child with an oracle** — FEATURE — value 3 — effort M — risk med — category: lean — wild
  Why: assumption: LLMs make good delta-debuggers when a hard oracle exists. Instruct a child to cut the install by 30% while keeping roundtrip, doctor, drill and the exam's zero-token arms green. Its patch is a proposal, never merged unreviewed. This is unconventional, but the gates bound the damage.
  Done when: one run yields a patch that removes bytes with all four gates green, or a report of why it couldn't.

- **Wild: random weekly disable of one verb or hook in the drive's own lanes** — PERFORMANCE — value 3 — effort M — risk med — category: lean — wild
  Why: assumption: lanes are a safe testbed. Each week one verb is switched off for lane sessions only, and friction and failures are logged against it. A verb with zero effect after 8 disabled weeks is retired with the evidence. This is a field experiment that uses no usage metrics. It is slow, and low-use verbs may simply never be exercised.
  Done when: the log shows a disabled verb, its lane count and friction count after one week.

- **Wild: hostile-fake-agent footprint golden** — SECURITY — value 3 — effort L — risk med — category: safety — wild
  Why: assumption: no adversarial driver of the real hooks exists. A scripted fake agent tries 50 mischievous tasks (pasted secrets, path escapes, hook floods) in a scratch home. The resulting file, process and network footprint is compared with a checked-in golden. A golden diff catches silent growth and unsafe writes together, but it needs upkeep as features change.
  Done when: the nightly run passes against the golden and a planted extra write is detected.

- **Wild: five-minute "tour of what can hurt you"** — FEATURE — value 2 — effort S — risk low — category: safety — wild
  Why: assumption: the user has never seen the whole risky surface at once. `fm risks` prints each grant, timer, listener, bypass setting and push permission with one command to turn it off, drawn from the live state and not from docs.
  Done when: the output lists every active grant in a fixture home, and each listed off-switch command works.

- **Do less: make "lean" one sentence in `fm doctor` and nothing else** — CLEAN — value 2 — effort S — risk low — category: lean
  Why: the pack already carries many lean metrics with no reader. The least approach is one line, "N verbs, M injected tokens, K unused 30 days," and no new gate until that line changes a decision. It risks staying ignored.
  Done when: `fm doctor` prints that line and an empty-state test passes.

Next question: Which lean or safety signal has the user actually acted on, so the next brainstorm can pick the mechanism that gets read?
Next question: Which part of the 1,388 skill files is ever loaded in a real session, and does anything fail when an unloaded one is removed?
