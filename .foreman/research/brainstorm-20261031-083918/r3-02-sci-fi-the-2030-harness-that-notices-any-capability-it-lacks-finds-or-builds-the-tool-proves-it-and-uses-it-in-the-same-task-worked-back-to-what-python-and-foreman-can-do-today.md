# Brainstorm — lens: sci-fi: the 2030 harness that notices any capability it lacks, finds or builds the tool, proves it and uses it in the same task, worked back to what Python and Foreman can do today

- **Gate every miss on a capability probe, not a failed command** — FEATURE — value 4 — effort M — risk low — category: capability detection
  Why: the trigger (T-2270) fires on a missing command or module; a 2030 harness also notices "can't open this .xlsx", "no network to this host", "no GPU", which fail softly (garbage output, a refusal, a timeout). Assumption: soft misses are the larger class.
  Done when: a fixture where a PDF read returns empty text files a capability-miss named "pdf-text" with the signal that triggered it, and a test fails if the miss list stays empty.

- **Write the miss as an executable spec before searching** — FEATURE — value 5 — effort M — risk low — category: build-test-use
  Why: Mission 6 names a build-test-use loop but T-2278 scaffolds only a failing-first test for a tool; nothing captures the original miss as the acceptance case. Assumption: a miss replayed later is the only test that proves the tool solved the user's problem.
  Done when: `fm task new` from a miss stores the failing command plus input as `miss.case`, and closing the task runs that case through the new tool and records pass/fail.

- **Run the find, build and use stages as one three-state task** — FEATURE — value 4 — effort M — risk med — category: task loop
  Why: the pack lists trigger, scaffold and queue as separate pieces; no single task carries a miss from "found nothing" to "used in anger". Assumption: the loop breaks at the joins.
  Done when: one task shows states found/built, proven, used, and `fm task finish` refuses while the third is empty.

- **Cap build effort by the cost of the workaround** — FEATURE — value 3 — effort S — risk low — category: economics
  Why: building a tool for a one-off is waste; the user's lean-ratchet steer shows footprint matters. Assumption: the miss log can estimate how often the workaround ran.
  Done when: a miss seen once gets a "script in .fm-scratch, not a skill" recommendation, and one seen in 3+ sessions gets "skill or MCP".

- **Hand the user a grant card with the proof already attached** — FEATURE — value 4 — effort M — risk low — category: grants
  Why: installs are queued, never self-granted; the user's cost is deciding. A card carrying the miss, the candidate, its sandbox trial output and the one command to approve makes it a one-word answer. Assumption: trials can run without network.
  Done when: `fm grants` prints each pending item with trial result and exact approve line, and an item with no trial is flagged "unproven".

- **Let a tool declare its needs in a manifest the guard reads** — SECURITY — value 4 — effort M — risk med — category: tool safety
  Why: built scripts and MCP servers run in bypass-ish modes while the guard blocks commands by pattern; a declared manifest (paths, hosts, binaries) turns the guard into allowlist enforcement for tools. Assumption: stdlib scripts can be wrapped by a launcher that enforces it.
  Done when: a built tool that writes outside its declared path is blocked and the block names the manifest line.

- **Show a toolbelt page in the web UI with misses, shelf and queue** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the pack names the web UI as the surface and lists nothing for tools. Assumption: users won't read a ledger file.
  Done when: the page lists open misses, shelf tools with last-use dates, and pending grants, and its counts match the CLI's.

- **Wild: Let the harness rehearse a miss in advance from the plan** — FEATURE — value 3 — effort L — risk med — category: foresight
  Why: wild. At plan time, a tool-less cold child reads the Approach and names the tools the task will probably need; the harness checks each exists and queues finds before the work stalls.
  Done when: a plan naming "convert HEIC photos" yields a pre-miss entry with a candidate before any edit.

- **Wild: Forge a tool from a recorded manual session** — FEATURE — value 4 — effort L — risk med — category: tool synthesis
  Why: wild. The event log already holds the shell sequence the agent improvised; turning a repeated 4-command pipeline into a tested script is the 2030 move. Assumption: the log keeps commands with exit codes.
  Done when: `fm new tool --from-log T-NNNN` emits a script whose test replays the logged inputs and outputs.

- **Wild: Keep a tool "heartbeat" that kills shelf tools which fail their own self-test at session start** — CLEAN — value 3 — effort M — risk low — category: tool health
  Why: wild. Tools rot as their world changes; a shelf that checks itself cheaply means a broken tool files its own repair task with the failing input rather than failing mid-task.
  Done when: breaking a shelf tool's dependency makes the next session start print one line naming it and file one FIX task.

- **Wild: Trade a proven tool between projects via a signed bundle the user must approve** — SECURITY — value 3 — effort L — risk high — category: sharing
  Why: wild. A tool built in repo A that passed its miss case is useful in repo B; a hashed bundle with its tests and birth certificate lets B re-run them before the user grants it.
  Done when: importing a bundle with a tampered test or hash is refused, and an intact one lands in the grant queue unapproved.

- **Score the loop on seeded misses in the exam** — PERFORMANCE — value 4 — effort M — risk low — category: exam
  Why: the standing rules demand weakness-finding by signals Foreman didn't author; a child-written set of "missing tool" scenarios, with foreman vs plain, shows whether the loop beats improvising. Assumption: free arms can check whether the right tool was chosen.
  Done when: `fm exam` reports miss-handling recall and time-to-use per scenario, held out from the builder.

- **Name the search that found nothing, so the next session doesn't repeat it** — FIX — value 3 — effort S — risk low — category: search cache
  Why: `fm plugins find` and `fm lib search` cost tokens each run; a negative result with date and query, expiring after a week, avoids rediscovery. Assumption: repeated searches occur.
  Done when: a second identical find within the window prints "searched <date>, nothing" and makes no search call.

Next question: When a built tool passes its own miss case but the user's next real input differs, who notices, and where does that failure get recorded?
Next question: Which capability misses are being worked around silently inside a model's own reasoning rather than through a command that fails?
