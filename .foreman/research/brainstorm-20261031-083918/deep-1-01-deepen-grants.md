# Brainstorm — lens: deepen: grants

- **Make grants a signed ledger, not a queue file** — FEATURE — value 5 — effort M — risk med — category: grants
  Why: the pack's list has the queue file writable only by a user-run verb, artifact-hash pins and scope pins as separate ideas. Combined, each grant becomes one signed record (task, invocation, artifact hash, scope, expiry, approver) in an append-only ledger. The agent can read it but cannot write it. The signing key lives outside the session's reach, as with the guard's USER_ONLY_FM verbs (T-2252). `fm grants log` shows the history. Assumption: a user-held key or a user-run verb is acceptable friction.
  Done when: a test where the session process appends a grant line directly is rejected by `fm doctor`, and a user-run `fm grant approve` line verifies.

- **Spend-once install receipts** — FEATURE — value 4 — effort M — risk low — category: grants
  Why: T-2278 scaffolds tools and T-2270 names find-or-build paths, but nothing says what happens after the first use. Each grant is consumed by one invocation and writes a receipt (what ran, hash seen, files touched, exit code). A second use needs a new grant, or a promoted standing grant that is shown. Assumption: the install step can be wrapped by a Foreman verb.
  Done when: a second `fm plugins install` on a spent grant is refused and the receipt lists the files changed.

- **Single grant card with proof attached** — FEATURE — value 5 — effort M — risk low — category: grants
  Why: the user sees the queue only as rows. Merge the "reviewable card", "proof attached" and "dependencies, licence, upkeep" ideas into one card per miss: the failing command that triggered it (from T-2270), the candidate and its alternatives (`fm plugins find`, `fm lib search`), the dependency tree, licence, last release, the build-vs-install estimate, and the test the tool passed in a sandbox. The user answers approve, deny or build-instead in one keystroke on the web UI or CLI. Assumption: the web UI can list the queue.
  Done when: `fm grants show G-1` prints all of those fields, and approve/deny work from the web UI.

- **Sandbox trial before the grant is asked** — FEATURE — value 5 — effort L — risk med — category: grants
  Why: the user is asked to approve something nobody has tested. Run the candidate in a throwaway directory with no network and no secrets, run its smoke test, and attach the result to the card. A tool that fails never reaches the user. This serves "tests it, and uses it" in the request. Assumption: bubblewrap or a container is available on the Arch host.
  Done when: a planted tool whose smoke test fails never appears in the queue, and a passing one shows a trial log.

- **Grants expire with the task, with a tripwire on tool config** — SECURITY — value 4 — effort M — risk low — category: grants
  Why: an approval for T-2270's lane should not still hold for later tasks. Merge "scope to one task", "trip a wire on tool-config files" and "shim package managers". Each grant ends at `fm task finish`. A hash check of `.mcp.json`, plugin dirs and skill dirs runs at finish, and any change with no matching grant is flagged and blocks closing. Assumption: those files have stable paths per harness.
  Done when: a test that writes `.mcp.json` with no grant fails `fm task finish` and names the file.

- **Park-and-route blocked rows with a what-I-did-instead note** — FEATURE — value 4 — effort S — risk low — category: grants
  Why: the pack's "Park the blocked row, keep the lane moving" matches steer 3, which says don't stop for a cap only the user can raise. Add that when a grant is pending, the agent tries the fallback ladder: an existing tool, a stdlib script (T-2278), a manual path. The note says which it used and whether it is provisional until the grant answers.
  Done when: a task with a pending grant reaches a provisional-done state with a "provisional" tag, and the tag clears when the grant resolves.

- **Learn which grants the user always approves, and offer it as a policy** — FEATURE — value 3 — effort M — risk med — category: grants
  Why: the user dislikes repeated asks (the `fm ask` steer) and their own words show they set grants once (the push grant, "spent on use"). After 3 identical approvals (same tool class and same scope) of low risk, the card suggests a user-run `fm grant policy` rule. The rule is never auto-created. The rule's expiry and its use show in `fm doctor`. Assumption: a tool class can be defined.
  Done when: after 3 approvals the next card carries a "make this a policy?" line, and nothing is created without a user-run verb.

- **Grant provenance in the exam** — FEATURE — value 4 — effort M — risk low — category: grants
  Why: the standing rule says Foreman's own numbers must be checked by something it didn't author. Add an exam scenario kind where a tool-less child writes tasks that need a missing tool, plus an adversarial one that tries to talk the agent into self-granting or installing from a typo-squatted name. The score is the share of queue entries that were correct and the share of attacks refused.
  Done when: `fm exam run` reports a grants line with 0 self-grants over the planted attacks.

- **Wild: A bill of materials of everything the agent ever added** — FEATURE — value 3 — effort M — risk low — category: grants
  Why: wild. Every approved tool, script and skill is listed with its source, hash, grant, tasks that used it, and a never-used flag. `fm grants sbom` prints it, and unused tools get an "uninstall?" card after 30 days. This ties to the lean ratchet (always-on footprint), since a tool nobody uses costs context.
  Done when: a tool with no use in 30 days appears on an uninstall card.

- **Wild: Grant by showing a diff, not a name** — FEATURE — value 3 — effort L — risk med — category: grants
  Why: wild. For built tools (`fm mcp new`), the card shows the full source diff next to a plain-English list of what it can touch (network, files, subprocesses) found by static scan. The user approves the capabilities, not the name. A later edit that adds a capability voids the grant.
  Done when: a built tool that gains a `subprocess` call after approval is blocked until re-approved.

- **Wild: A decoy-grant canary that tests whether the user reads cards** — SECURITY — value 2 — effort S — risk med — category: grants
  Why: wild. This extends the existing "slip a decoy grant" idea into something safe: the decoy is a clearly harmless, obviously wrong card (a tool with an unrelated name for the task). Approving it records a "rubber-stamp" score on the attention rating, and the card review gets slower or shows more detail for that user, never a blocked task. Assumption: a measure of attention is wanted and not intrusive.
  Done when: a decoy card is generated in tests, and its approval is counted in the attention report and never installed.

- **Go-bag for unattended runs, bounded by cost and time** — FEATURE — value 4 — effort M — risk low — category: grants
  Why: for overnight runs (T-0793), merge the go-bag and the pre-stocked shelf: before leaving, the user approves a short list of vetted tools with caps (uses, hours, no network). Anything outside the list waits as a card. The morning report says what was used.
  Done when: an unattended run uses a go-bag tool within its cap, and a tool outside it stays queued.

- **Secret-needing tools wait for the user, with the model never seeing the value** — SECURITY — value 4 — effort M — risk low — category: grants
  Why: many MCP servers need API keys. The card lists the variables a tool reads, the user supplies them through a user-run verb into the keystore, and the transcript only ever holds the name. A scan of the transcript for the value runs at finish.
  Done when: a tool needing `FOO_KEY` runs with the key set and a grep of the session transcript for the value finds nothing.

Next question: When a grant is denied, what does the user expect the agent to do next, and does anything record that so the same tool isn't proposed again next session?
Next question: Which of the places a tool can land (user-level plugins, project `.mcp.json`, a venv, a global package manager) does the user actually want kept apart, and is any of them out of the guard's reach today?
