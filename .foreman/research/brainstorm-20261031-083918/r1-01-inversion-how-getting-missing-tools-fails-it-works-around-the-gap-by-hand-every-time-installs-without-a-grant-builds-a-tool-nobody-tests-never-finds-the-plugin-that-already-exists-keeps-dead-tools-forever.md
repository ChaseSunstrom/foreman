# Brainstorm — lens: inversion: how getting missing tools fails: it works around the gap by hand every time, installs without a grant, builds a tool nobody tests, never finds the plugin that already exists, keeps dead tools forever

- **Log every manual workaround as a capability miss** — FEATURE — value 5 — effort M — risk low — category: detection
  Why: T-2270 fires on a missing command or module, but a session that hand-rolls a `curl | python` parse or a sed loop never errors, so the trigger never sees the gap. Assumption: a hook can spot the same hand-written pipeline shape in 2+ Bash calls or sessions.
  Done when: a fixture session that writes the same ad-hoc script twice yields one find-or-build task naming the repeated shape.

- **Search before build, enforced by a receipt** — FEATURE — value 5 — effort M — risk low — category: discovery
  Why: the request says "finds an existing plugin... or builds one", and `fm new tool` (T-2278) scaffolds with no check that `fm plugins find` or `fm lib search` ran first. Assumption: nothing blocks building today.
  Done when: `fm new tool X` refuses, naming the two search commands, unless a search for X's capability is recorded for the task; the record lists what was found and why each hit was rejected.

- **Make the install-grant queue unforgeable by the agent** — SECURITY — value 5 — effort M — risk med — category: grants
  Why: the user wants grants queued and never self-granted. Steers show the same pattern for `fm mandate set` (T-2252, a user-only verb) and the "bind every consent to a channel the model can't write" idea. Assumption: install paths (pip, npm, `claude mcp add`, writes to settings) aren't all guarded yet.
  Done when: a test where the agent runs `pip install`, `npm i -g`, `claude mcp add` and edits a plugin dir directly is blocked or queued each time, and only a user-run `fm grant` releases it.

- **Quarantine built tools until the test is proven red-first** — SECURITY — value 4 — effort M — risk low — category: testing
  Why: the build-test-use loop is a seed row, and "a tool nobody tests" is the failure. Foreman already holds red-first as a standing discipline for tasks. Assumption: tool scaffolds can be run without the test.
  Done when: a new tool lives in an unusable `candidate/` state and is promoted only after its test failed on the stub and passes on the real file, and `fm` refuses to run a candidate in a session.

- **Run a built tool against a hostile fixture before first use** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: a tool the agent wrote runs with the session's rights, and an MCP server built by `fm mcp new` is a long-lived process. Assumption: no sandbox or network-off run exists for tools.
  Done when: the first run of a built tool happens in a no-network, throwaway-directory sandbox, and a tool that writes outside it or opens a socket is rejected with the offending call listed.

- **Give every acquired tool a use ledger and a death date** — CLEAN — value 4 — effort S — risk low — category: lifecycle
  Why: "keeps dead tools forever" is the named failure, and plugins, skills and MCP servers all add always-on footprint that the lean ratchet (Mission 8/#12) already measures. Assumption: no per-tool use counts are recorded.
  Done when: `fm tools` lists each acquired tool with last-used date and calls in 30 days, and a tool unused for 30 days is queued for the user to retire, never silently deleted.

- **Charge each tool its footprint on the lean ratchet** — PERFORMANCE — value 3 — effort S — risk low — category: footprint
  Why: the ratchet records rules chars, descriptions chars and hook p50 on ship, but a new MCP server's tool descriptions load into every session. Assumption: acquired tools are not attributed separately.
  Done when: `fm doctor` names which acquired tool grew the always-on footprint, and the grant queue shows that cost beside the install request.

- **Re-test acquired tools when their world changes** — FIX — value 3 — effort M — risk low — category: reliability
  Why: a tool tested once goes stale as dependencies and CLI versions move, and "dead tools" includes broken ones. Assumption: tests run at build time only.
  Done when: a weekly zero-token check reruns each tool's test and marks a failing tool "broken" in `fm tools`, and the miss trigger stops pointing at it.

- **Rank grant requests by the work they unblock** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: a queue of bare install lines gets rubber-stamped or ignored. Assumption: requests today carry only the command.
  Done when: each queued grant shows the blocked task ids, how many sessions hit the miss, the source and version, and the rejected alternatives, and the top three are shown first.

- **Remember the user's grant refusals** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: a declined install re-queued every session is the same nuisance as the "steers" the user had to repeat. Assumption: refusals aren't stored as a rule.
  Done when: a refused grant is recorded with its reason, the miss trigger offers the build path or the no-tool path instead, and re-queueing it needs a new reason.

- **Wild: Hold a tool-recall duel against the whole ecosystem** — FEATURE — value 4 — effort L — risk med — category: evaluation
  Why: wild. A tool-less child writes capability-miss scenarios in languages Foreman wasn't written for (the exam rule), and the score is how often `fm plugins find` surfaces an existing tool when one exists, per ecosystem.
  Done when: `fm exam` prints find-recall per ecosystem and lists misses where the agent built something a public tool already did.

- **Wild: Let a built tool graduate into a shared card** — FEATURE — value 3 — effort L — risk med — category: sharing
  Why: wild. A tool used in 3+ projects with a passing test could be offered, with the user's approval, as a `fm lib` card or a published plugin, so the next project finds it instead of rebuilding it.
  Done when: `fm tools promote X` writes a lib card with its test, and `fm lib search` returns it in a second repo.

- **Wild: Rehearse the missing tool as a stub first** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. Before searching or building, the agent writes the call it wishes it had (a one-line fake CLI that returns canned output) so the real need is pinned down, and a found plugin is judged against that call rather than its own README.
  Done when: a task records a wished-for call and a found or built tool is accepted only if it satisfies that call in a test.

- **Wild: Keep a graveyard of tools that were tried and dropped** — CLEAN — value 2 — effort S — risk low — category: memory
  Why: wild. The steers say a failed idea goes to not-yet.md with its blocker. The same applies to rejected plugins: record why each was refused so no session re-evaluates it.
  Done when: `fm plugins find` marks a previously rejected plugin with the reason and date.

Next question: Which install paths (pip, npm, cargo, `claude mcp add`, hand-edited settings, curl-piped scripts) can the guard see today, and which does the agent have that no hook intercepts?
Next question: When a tool was found and used successfully, does the user ever learn it came from outside the repo, and where would they check?
