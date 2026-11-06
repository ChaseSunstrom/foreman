# Brainstorm — lens: the missing verb (invented): every 'command not found', unsupported file type, failed tool call or repeated manual sequence is a request for a tool

- **Replay the original miss against the new tool** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: the build-test-use loop (seed row, value 3) is unbuilt. T-2278 scaffolds a failing-first test, but nothing checks the tool fixes the call that failed.
  Done when: a recorded miss (command, args, cwd) is re-run after the tool is installed or built, and `fm task finish` refuses to close the miss task unless the replay exits 0.

- **Make the grant card one screen and one word** — FEATURE — value 5 — effort M — risk low — category: consent
  Why: the request says "install grants are queued for me". The pack shows no queue UI. Assumption: a long queue gets rubber-stamped.
  Done when: `fm grants` lists each pending install with what, the miss that caused it, source, version, hash, size and permissions. `fm grants yes N` or `no N` resolves it, and the model cannot run either (guard test).

- **Trial a found tool in a no-network sandbox before asking for the grant** — SECURITY — value 4 — effort L — risk med — category: supply chain
  Why: T-0791 (18 injection and supply-chain ideas) is deferred, and found plugins and MCP servers are untrusted code. Standing rule on downloaded files: empty directory, `python -I`.
  Done when: the grant card shows files touched, network attempts and processes spawned during a sandboxed smoke run, and a tool that tried the network without declaring it is flagged.

- **Mine the event log for repeated manual sequences** — FEATURE — value 4 — effort M — risk low — category: capability-miss
  Why: T-2270 fires on a missing command or module. The lens also counts failed tool calls and repeated hand-run sequences, which the pack doesn't cover.
  Done when: a 3+ command sequence repeated in 3+ sessions yields one task proposing a script, with the sequences quoted.

- **Add a tool ladder before any search** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the "do less" approach. The order is: built-in or installed tool, then a stdlib one-liner, then `fm lib search`, then `fm plugins find`, then build. Steers favour not hand-writing per-language detection.
  Done when: the miss note prints the ladder, and a test shows a stdlib-solvable miss never reaches the install queue.

- **Pin and hash every adopted tool in a lockfile** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: assumption: found tools update silently. The existing ship gate and doctor can verify a lock.
  Done when: `fm doctor` fails when an installed or built tool's hash differs from `tools.lock`, and the diff is shown on update.

- **Promote a built tool only after it has proved itself** — FEATURE — value 3 — effort M — risk low — category: reuse
  Why: T-2278 builds tools and project skills, but the pack shows no path from a one-task script to a lib card. Steers also say the footprint must stay lean.
  Done when: a script used by 3+ tasks with a passing test is offered as a lib card. One unused for 30 days is listed for retirement, and no other tool changes state.

- **Map unsupported file types to converter recipes** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: assumption: sessions hit pdf, xlsx, images and similar. Per the standing rule, the recipes are found from the repo's manifests and stack cards, not hand-written per language.
  Done when: opening an unreadable file type prints the recipe and whether the converter is installed or queued, covered by a fixture test per type.

- **Score miss-handling in the exam** — FEATURE — value 4 — effort M — risk med — category: evaluation
  Why: the steers want signals Foreman didn't author and child-authored scenarios. Scenarios would remove one tool and measure foreman against plain.
  Done when: `fm exam scorecard` prints a find-or-build pass rate, with the scenarios authored by a tool-less child.

- **Show top misses, and what filled them, in the web UI** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: T-2270 records misses, but the user sees them only in a session note. The pack lists the web UI as the only surface.
  Done when: a Misses page lists each tool by session count, status (open, queued, built, adopted) and the task that closed it.

- **Wild: Let the user type "I wish fm could …" and get a morning demo** — FEATURE — value 4 — effort L — risk med — category: delight
  Why: wild. A wish becomes a capability-miss task. An overnight lane searches or builds, tests, and leaves a grant card plus a recorded demo.
  Done when: `fm wish "…"` creates the task, and the next morning `fm grants` shows a candidate with a passing replay.

- **Wild: Export built tools as signed offline bundles** — FEATURE — value 2 — effort L — risk med — category: sharing
  Why: wild. A tool, its test and its provenance go in one file that another Foreman user imports through the same grant queue. It needs no marketplace.
  Done when: `fm tool export` followed by `fm tool import` on a clean checkout runs the test and queues a grant, never self-installs.

- **Wild: Have a cold child invent the missing verbs before the user hits them** — FEATURE — value 3 — effort M — risk med — category: initiative
  Why: wild. A tool-less child reads the repo map and stack cards and lists the five tools a session here will likely lack. They are pre-searched and queued, never installed.
  Done when: `fm tools forecast` lists five items, and the exam shows the share later hit by real misses.

- **Wild: Let the wishlist file itself as a Seed row** — FEATURE — value 2 — effort S — risk low — category: genesis
  Why: wild. A miss that recurs across projects, or across generations, becomes a capability proposal. This matches the standing rule that Seeds retry items a new capability may unblock.
  Done when: a miss seen in 3+ projects produces a Seed row with its evidence.

Next question: Which of Foreman's own commands has a user-written wrapper script or alias, and what miss does that wrapper reveal?
Next question: When a found tool needs a secret or network access, who supplies it, and is that grant kept separate from the install grant?
