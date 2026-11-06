# Brainstorm — lens: inversion: how getting missing tools fails: it works around the gap by hand every time, installs without a grant, builds a tool nobody tests, never finds the plugin that already exists, keeps dead tools forever

Lens: inversion. Each idea below targets one way tool acquisition fails. The first ten are ones I'd build; the last three are wild.

- **Detect hand-worked gaps from the event log** — FEATURE — value 5 — effort M — risk med — category: miss detection
  Why: the capability-miss trigger (T-2270) fires on a missing command or module. A manual workaround (a 12-step shell pipeline, a repeated `sed`/`jq` chain, a hand-edited generated file) produces no error, so nothing fires. Assumption: the event log records bash commands with enough detail to cluster them.
  Done when: a fixture session that runs the same 3+ command sequence in 3 tasks yields exactly one find-or-build task naming the sequence, and a session with unrelated commands yields none.

- **Require a search receipt before any `fm new tool`** — FIX — value 4 — effort S — risk low — category: find-before-build
  Why: the scaffolds (T-2278) exist next to `fm plugins find` and `fm lib search`, and nothing forces the search to come first. Assumption: builds can currently start with no search on record.
  Done when: `fm new tool X` with no `fm plugins find`/`fm lib search` event for that miss in the session refuses and prints the two commands; with a receipt it proceeds, and the receipt's reason for rejecting each hit is stored on the tool.

- **Block installs not backed by a user-written grant** — SECURITY — value 5 — effort M — risk med — category: install grants
  Why: the request says "never self-granted", and the guard stops only commands it recognizes. An agent can run `pip install`, `npm i -g`, `claude mcp add` or `curl | sh`, or write the grant file itself. Assumption: the grant file sits at a path the agent can write.
  Done when: a test that runs each installer form through the guard with no grant is refused, and a test where the agent writes the grant file directly is refused because the file isn't in a user-only channel.

- **Make a built tool count only after it passes the original miss, red first** — FEATURE — value 5 — effort M — risk low — category: build-test-use
  Why: the loop is "build, test, use". A tool can ship with a test that never failed or never touched the real case that caused the miss. Assumption: the miss's command and error are stored with the trigger.
  Done when: `fm tool accept NAME` fails unless the recorded test failed before the tool existed and a replay of the original miss now succeeds; a tool whose test is green from the start is rejected.

- **Keep a tool shelf with a use ledger and a retirement proposal** — FEATURE — value 4 — effort M — risk low — category: tool lifecycle
  Why: built scripts, project skills and MCP servers accumulate, and every skill description and rule adds to the lean-ratchet footprint (Mission 8). Nothing now notices a tool that is never called. Assumption: tool calls can be attributed to a shelf entry by name.
  Done when: a tool with 0 uses across N sessions appears in `fm doctor` with a one-command retire; the footprint falls after the retire and the ratchet records it.

- **Queue grants as one card ranked by the work they unblock** — FEATURE — value 4 — effort S — risk low — category: install grants
  Why: the queue holds one row per request, and a user looking at five separate requests answers none. Assumption: a miss can be traced to the tasks waiting on it.
  Done when: `fm grants` prints one card, ordered by the number of blocked tasks, with each item answerable by a single word (yes/no/later) and "no" stored with the reason.

- **Remember refusals so the same tool isn't re-requested** — FIX — value 3 — effort S — risk low — category: install grants
  Why: a repeated miss re-queues the same install the user already refused. Assumption: the queue doesn't dedupe against past refusals.
  Done when: a refused grant is not re-queued for the same tool and version in a later session; it comes back only with new evidence (a different miss), which the card states.

- **Re-test shelf tools when their environment changes** — PERFORMANCE — value 3 — effort M — risk low — category: tool lifecycle
  Why: a script that wraps a CLI or a library breaks silently when the dependency upgrades, and the next session finds a dead tool. Assumption: each tool records the versions it was tested against.
  Done when: changing a recorded dependency version marks the tool "stale" in `fm doctor` and re-runs its test; a failing tool is quarantined, so the miss trigger fires again instead of invoking the dead tool.

- **Run a found plugin in a sandbox trial before it reaches the grant card** — SECURITY — value 4 — effort L — risk med — category: vetting
  Why: a found plugin or MCP server is third-party code that the user is asked to approve blind. Supply-chain defenses sit in T-0791's deferred bundle, so this is not covered yet. Assumption: a no-network sandbox exists or can be built.
  Done when: the card shows what the trial observed (files touched, network attempts, declared tools), and a fixture plugin that tries a network call is flagged.

- **Score miss handling in the exam with planted gaps** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the user's rules want signals Foreman didn't author. Tool acquisition has no exam arm, so a loop that always works around the gap would score fine. Assumption: the exam scenario generator can plant a missing tool.
  Done when: the scorecard reports, per scenario, whether the session found, built or worked around the gap, and a free-arm baseline of "worked around" is printed beside it.

- **Wild: Hold a tool fire drill** — FEATURE — value 3 — effort M — risk med — category: resilience
  Why: wild. Deliberately break a shelf tool in a throwaway copy and see whether the next session notices, quarantines it and re-finds a replacement or silently routes around it.
  Done when: a drill run logs "noticed / quarantined / replaced" for the planted break, and a session that never noticed fails the drill.

- **Wild: Forge a tool from a recorded shell session** — FEATURE — value 4 — effort L — risk med — category: tool generation
  Why: wild. When a user or agent repeats a manual workaround, record the exact commands and turn them into a stdlib script plus a test generated from the recording's input and output. It reduces the build step to review and accept.
  Done when: replaying a recorded 5-command session produces a script whose test passes on the recording's output and fails when the script is altered.

- **Wild: Let a tool negotiate its own retirement** — FEATURE — value 2 — effort S — risk low — category: tool lifecycle
  Why: wild. Each shelf tool carries a one-line "reason to exist" and a death date. At the date it files a retire-or-renew card with its use count, its held-up rate and the cost it adds to the ratchet. If the user does nothing, it is retired, not renewed.
  Done when: a tool past its death date with no user answer is moved to the graveyard, reversibly, and the move is logged.

Next question: Which of Foreman's own verbs does a session now reach for by hand because the verb is missing or too slow, and does the event log show that?
Next question: When a found tool and a built tool both solve a miss, who decides which one stays on the shelf, and on what measured evidence?
