# Brainstorm — lens: self-modification: a toolbelt that learns which found or built tools held up, retires the unused and promotes the reused, measured and reversible

- **Keep a toolbelt ledger of every found or built tool** — FEATURE — value 5 — effort M — risk low — category: toolbelt
  Why: Mission 6 #5 builds the trigger (T-2270) and scaffolds (T-2278) but nothing records afterwards whether a tool was used. Assumption: no per-tool use record exists yet.
  Done when: `fm tools ledger` lists each installed/built tool with source, date, grant status, and call count from real sessions, and a test shows a call increments it.

- **Score each tool by held-up rate** — FEATURE — value 5 — effort M — risk low — category: toolbelt
  Why: Mission 8 already scores trigger precision (fm triggers) and model routing from outcomes; tools lack the same loop. Assumption: tool calls can be tied to task outcomes via the event log.
  Done when: `fm tools score` prints per-tool reuse, errors, and share of tasks closed first-time-green that used it, with a fixture test.

- **Propose retiring tools unused for N sessions** — FEATURE — value 4 — effort S — risk low — category: retirement
  Why: The lean ratchet (T-0794 slim Foreman, always-on footprint) warns when footprint grows. Unused tools add descriptions and listings to that footprint. Assumption: installed MCP/skills count toward it.
  Done when: a tool with zero calls across 10 sessions appears in `fm tools retire --dry-run` and in the user's queue, never removed automatically.

- **Make every install and retirement reversible with one command** — FEATURE — value 5 — effort M — risk med — category: reversibility
  Why: Install grants are queued for the user; retirement needs the same discipline. Assumption: install paths vary (plugin, MCP, project skill), so an undo manifest is needed.
  Done when: `fm tools undo ID` restores the pre-install config byte-for-byte, tested for each of the three kinds.

- **Promote a reused built script into a project skill** — FEATURE — value 4 — effort M — risk low — category: promotion
  Why: T-2278 scaffolds scripts and skills separately. A script called in 3+ tasks is a skill candidate. Assumption: call counts from the ledger.
  Done when: the third reuse files one task "promote tool X to skill", which `fm new skill` can complete from the script's docstring and test.

- **Promote a repeatedly built tool to a global library card** — FEATURE — value 3 — effort M — risk med — category: promotion
  Why: `fm lib` has cards per stack. A tool rebuilt across 2+ projects shows a cross-project need. Assumption: the library accepts user-owned cards.
  Done when: a tool present in 2 projects' ledgers is offered as a draft lib card, user-approved before it is written.

- **Re-test tools on every toolbelt change** — FIX — value 4 — effort S — risk low — category: reliability
  Why: Build-test-use runs the test once at creation. Dependency, CLI or API drift breaks tools silently. Assumption: no recurring test run exists.
  Done when: `fm doctor` runs each tool's test and names one that now fails, with a test using a broken fixture tool.

- **Prefer found over built, and record why** — FEATURE — value 3 — effort S — risk low — category: decision log
  Why: The request orders find then build. Without recording the search result, a later retirement can't tell if a better one existed. Assumption: `fm plugins find` output can be stored.
  Done when: each built tool's record holds the search queries and the candidates rejected, and `fm tools show` prints them.

- **Block a tool's reinstall after the user retires it twice** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: Standing rule about the user's veto being learned from; the capability-miss trigger would otherwise re-suggest the same tool. Assumption: retire reasons are captured.
  Done when: after a retire, the miss trigger does not offer that tool again, and says "retired by you on DATE" if asked.

- **Shadow-run a candidate tool before its grant** — SECURITY — value 4 — effort L — risk med — category: safety
  Why: Grants are queued for the user; a found tool is untrusted code. Seeing what it would read and write helps the user approve. Assumption: a sandbox exists or can use the guard's script cache.
  Done when: the grant queue entry shows the files and network a dry run touched, from a real sandboxed run.

- **Wild: Let tools compete in a bake-off** — FEATURE — value 3 — effort L — risk med — category: selection
  Why: wild. When two found tools fit one miss, run both on the same held-out case and keep the one that passes cheaper, per the exam's free-arm idea.
  Done when: `fm tools bakeoff A B` runs both on a fixture and writes a winner with times and cost.

- **Wild: Compost retired tools into lessons** — FEATURE — value 2 — effort M — risk low — category: learning
  Why: wild. A retired tool still taught what the project needed. Store a one-line lesson (need, tool, why dropped) that recall surfaces on a similar miss.
  Done when: a retire writes a lesson that `fm recall` returns on the next matching miss.

- **Wild: Publish a tool-belt report card to the genesis site** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The site already refreshes stats daily from genesis; adding found, built, reused, retired counts makes self-extension visible. Assumption: no private tool names are exposed.
  Done when: site/genesis data has toolbelt counts without names, and the page shows them.

Next question: What does a tool's call look like in the event log today, can it be tied to a task and its outcome, or must the harness add that record first?
Next question: Who judges that a built tool is correct, when the same model wrote both the tool and its test?
