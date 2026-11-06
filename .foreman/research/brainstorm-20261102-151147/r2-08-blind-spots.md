# Brainstorm — lens: blind spots

- **Mark a gauge fix as a break in the series** — FIX — value 4 — effort S — risk low — category: measurement
  Why: T-2667 made `fm burden` count `hook_success` stdout it had missed, so its numbers jump at the fix. Digests and ratchets that compare across that commit would read the jump as growth. Question a brainstorm should have asked: "when a gauge's inputs change, what happens to every trend and ratchet built on it?"
  Done when: a test records burden before and after a channel is added, and the trend reader prints a "series changed at T-2667" marker instead of a delta.

- **Count the demand a duplicate capture shows** — FEATURE — value 3 — effort S — risk low — category: triage
  Why: T-2656 wakes a deferred task when a near-duplicate capture arrives, but the repeat is also a signal that the user keeps wanting it. Question: "what does a repeated ask tell us besides 'already filed'?"
  Done when: `fm next` ranks a deferred task higher after N near-duplicate captures, and prints "asked 3 times" next to it.

- **Express stall and spend caps in the host's own usage units** — FEATURE — value 4 — effort M — risk med — category: spend
  Why: T-2669 stops a run by dollars. On a subscription the binding limit is the usage window, and dollars are only a proxy. Assumption: the user is usage-window limited. Question: "in what unit does the user actually feel running out?"
  Done when: `fm run --stall-window PCT` stops after PCT of a usage window with no task close, and the receipt names the unit.

- **Attribute stall spend per lane** — FIX — value 3 — effort M — risk med — category: spend
  Why: "dollars since the last close" is ambiguous when parallel lanes (Missions 5–8 run in lanes) close tasks at different times. A close in one lane may reset the clock while another lane burns money. Question: "what does each global counter mean when work is concurrent?"
  Done when: a test runs two fake lanes, one closing and one stalled, and the stalled lane's spend still trips the stop.

- **Show everything `fm next` withheld, with the release condition** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: round-first hold, pace, caps and "waits with T-2441" all silently hide work. T-2462 and T-2450 wait on prose conditions the user must remember. Question: "what is invisible to the user because a rule hid it?"
  Done when: `fm next --held` lists each hidden item with the rule that holds it and the condition that releases it.

- **Give each `fm run` stop reason its own exit code** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: a stall stop, a budget cap, a usage-limit wait and a kill all look alike to a wrapper or timer. Question: "can a script tell why the run ended?"
  Done when: a table-driven test asserts a distinct documented exit code for each stop reason, and `fm help run` lists them.

- **Diff the host's event and tool surface against what Foreman subscribes to** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the burden gap was a channel nobody listed. The same class is hook events and tool kinds the host adds that Foreman never reads or guards. Assumption: the installed host can list its events, or a pinned list can be checked in.
  Done when: `fm doctor` prints host events and tools with no subscriber, and a fixture adding a fake event turns it red.

- **Make proof verdicts flake-aware** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: T-2657 records per-test fail rates, but `fm prove` still treats one red-first fail as proof. A flaky test can pass the "fails without the change" check by luck. Question: "who reads the new number?"
  Done when: a proof on a test with a recorded fail rate above 5% reruns N times and reports "flaky: passes 7 of 10", not "proven".

- **Lint hook-path regexes for catastrophic backtracking** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: T-2668 found the nested-`$(` hang by hand. Other modules on the hook path may hold similar patterns, and the time test covers only the guard. Question: "which other parsers on the hook path can hang?"
  Done when: a static pass over every regex in hook-path modules fails on a planted `(a+)+` and passes the tree.

- **(wild) File one planted-flaw brief a week** — FEATURE — value 3 — effort M — risk low — category: grounding
  Why: grounding is spot-checked, and 3 of 4 slate items were already built. A brief with a known false claim, such as a verb that exists, shows whether grounding catches it before the user does.
  Done when: the weekly brief is dropped by grounding with the quoted evidence, and a miss files a FIX against the grounding step.

- **(wild) Swap units in mutants of the cost and time code** — SECURITY — value 3 — effort M — risk low — category: test quality
  Why: dollars, tokens, seconds and characters are all bare numbers, and T-2583 showed a criterion that disagreed with its own example. Mutants that swap or scale a unit show whether any test notices.
  Done when: the mutation run lists each unit swap in `fmcost` and `fmbudget` as caught or surviving, and the survivors are filed.

- **(wild) Mine the user's own correction words for gauge defects** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: phrases like "still prints zero", "misses", "doesn't count" (the T-2667 and `task_done` asks) point to a gauge blind to some input. Assumption: those messages are in the transcripts the steer expander already reads.
  Done when: a message with such words files one sibling-sweep task naming every gauge that reads the same ledger or channel, with the quoted phrase.

- **Separate a failed lens child from a dry one** — FIX — value 3 — effort S — risk low — category: brainstorm
  Why: T-0829 plans to drop lenses that "go dry" from `lens_rates`. A child that was truncated, capped or refused would look identical to one with nothing to say. Assumption: both currently log as zero ideas.
  Done when: `lens_rates` has separate dry and failed counts, a failed lens is rerun once, and a capped fake child never counts as dry.

Next question: which numbers that Foreman prints are compared across versions of the code that produced them, and which of those comparisons would break silently?
Next question: for each unattended stop (stall, cap, kill, limit), what does the user see within the first minute of returning, and who tells them?
