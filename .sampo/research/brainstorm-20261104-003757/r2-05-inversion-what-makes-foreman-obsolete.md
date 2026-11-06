# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Meter what a missing tool costs before acquiring anything** — FEATURE — value 5 — effort S — risk low — category: observability
  Why: assumption: mission #5 assumes missing tools hurt, but no ledger above prices a stall. Log each "tool missing" moment with the minutes lost, the inline workaround that finished the job, and whether it passed.
  Done when: `sampo gaps --cost` prints per-gap stall minutes and workaround pass rate from a fixture ledger, and a gap with a passing workaround is marked "no acquisition needed".

- **Compare acquire, inline script and bigger model on the same gap** — FEATURE — value 5 — effort M — risk low — category: decision
  Why: a gap only the 4B hits is a model gap, not a tool gap (the pack's small-model steer). Run each gap through three arms (installed tool, 10-line stdlib script, one rung up the model ladder) and record the cheapest verified pass.
  Done when: a gap record carries three arm results and `chosen_by: cheapest-pass`, and a test shows a gap the bigger model solves bare files no tool task.

- **Re-run the gap corpus on every model or host change** — PERFORMANCE — value 4 — effort M — risk low — category: obsolescence
  Why: gaps filed against last month's model may be gone, and the model-ID change trigger exists only for the Ward exam. Replay the saved gap scenarios bare and auto-propose retirement for any tool whose gap now passes.
  Done when: swapping the served model in a fixture triggers a replay and a retire proposal listing the tools whose gap passed bare.

- **Turn each built tool's test into the host-native adoption gate** — FEATURE — value 4 — effort M — risk med — category: replacement
  Why: the pack plans "detect native replacement" but not how to prove a replacement equals the tool. Ship each tool with its conformance test as a portable spec, so any host-native or MCP candidate must pass it before the tool is dropped.
  Done when: a stub native candidate that passes the test is swapped in by `sampo tools adopt`, and one that fails is refused with the failing case.

- **Show the acquisition funnel and treat its worst leak as the next cut** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: nothing above shows where gap, search, build, test, use and retain lose items. Print stage counts per generation and name the leakiest stage.
  Done when: `sampo gaps funnel` prints six counts from the ledger, and a fixture with zero "use" rows names that stage as the leak.

- **Close gaps that never recur** — CLEAN — value 3 — effort S — risk low — category: hygiene
  Why: assumption: most gaps are one-offs, so a 30-day silence means the need left. Auto-close the gap and its queued install grant, and keep a tombstone so a recurrence reopens it.
  Done when: a fixture gap with no hits for 30 days is closed with its grant withdrawn, and a new hit reopens it with its history.

- **Give every tool a no-tool twin card** — FEATURE — value 4 — effort M — risk low — category: small models
  Why: the steer wants small models to match frontier through scaffolding, and a card that reaches the same result with `curl`, `jq` and stdlib Python makes the tool optional. The tool is then kept only if it beats the twin.
  Done when: each acquired tool has a twin card, and the exam shows tool and twin pass rates side by side for one 9B model.

- **Cap installed tools per repo and make each new one retire an old one** — SECURITY — value 3 — effort S — risk low — category: budget
  Why: assumption: acquisition grows without bound unless something is traded away. A slot budget with usage-ranked eviction limits both supply-chain surface and description tokens.
  Done when: adding a tool at the cap fails without naming an eviction, and succeeds when the lowest-use tool is evicted with its undo.

- **Wild: Offer to upstream a built tool and delete the local copy** — FEATURE — value 3 — effort L — risk med — category: ecosystem
  Why: the cleanest obsolescence is the maintainers adopting the tool. Sampo drafts a PR or issue to the upstream project with the tool and its test, queued as a user-only outward action, and tracks the merge.
  Done when: a built tool produces a draft upstream patch in a scratch dir, and a "merged" marker triggers local retirement in a fixture.

- **Wild: Give every tool a fuse that burns down without real calls** — FEATURE — value 3 — effort M — risk low — category: lifecycle
  Why: tools that never fire on a session path are dead weight, and the standing rule is that capabilities must be called by a real session path. Each tool starts with a 21-day fuse and real calls extend it.
  Done when: a fixture tool with no calls is quarantined on day 21 with a one-line receipt, and one call resets the fuse.

- **Wild: Run a nightly "delete the acquisition loop" lane** — FEATURE — value 4 — effort M — risk med — category: self-doubt
  Why: the lens asks what makes #5 itself obsolete. A lane disables search, build and grant for a scratch copy, replays recent gap scenarios, and reports whether the pass rate fell.
  Done when: the morning card prints "#5 earned N of M passes" and reverses to "no loss" on a fixture where the bare model passes everything.

- **Wild: Race a cold apprentice with a blank toolbox against the forge** — FEATURE — value 3 — effort M — risk low — category: exam arm
  Why: it shows when a tool-less small model with a card beats a forged tool. A cold child gets only the task and the twin card, and the forged tool gets the same task. The exam compares cost per verified pass.
  Done when: `sampo exam run` has an `apprentice` arm that prints a per-gap winner on at least three scenarios.

- **Publish the gap corpus as a dated ledger of what models lacked** — DOCS-style FEATURE — value 2 — effort S — risk med — category: docs
  Why: a scrubbed, dated list of gaps shows readers where models and hosts caught up, and it feeds the half-life estimate for every tool. It must be scrubbed of paths, hosts and names before publishing.
  Done when: the site data contains gap classes with open and closed dates, and the leak lint passes on it.

Next question: Which acquired tool has a measured counterfactual win over the bare host, and does any ledger hold that number?
Next question: If the user's host shipped native skill and MCP discovery tomorrow, which of the funnel's six stages would still need Sampo?
