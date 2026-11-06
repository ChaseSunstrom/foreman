# Brainstorm — lens: the locked door (invented): an install grant is queued for one yes from the user, never self-granted; work goes on around it meanwhile

- **Pin each grant to the exact artifact hash it approves** — SECURITY — value 5 — effort M — risk low — category: grants
  Why: assumption: a grant says "install X" but the thing fetched later may differ (a plugin updated between ask and yes, a moved tag). Users approve a name, not bytes.
  Done when: a test queues a grant for a plugin at hash A, changes the upstream to hash B, and the install refuses with "approved A, saw B" and re-queues.

- **Make the queue file writable only through a user-run verb** — SECURITY — value 5 — effort M — risk med — category: grants
  Why: the steer "fm mandate set and off are the user's to run" (T-2252) already has a USER_ONLY_FM list; grants are the same class and the pack never shows them on it. Assumption: the grant-approve verb is not yet in that tuple.
  Done when: a guard test shows the agent calling the approve verb (directly, via `bash -c`, or via a script it wrote) is blocked, while the user's own invocation passes.

- **Keep working on a parallel row while a grant waits, and say which one** — FEATURE — value 4 — effort M — risk low — category: waiting
  Why: the request says work goes on around the door. The pack shows `waits_on_user` in `_next_runnable` but no rule that picks the next row *because* a grant is pending.
  Done when: with a grant queued on T-A, `fm next` returns a runnable task that doesn't depend on it, and prints "T-A waits on grant G".

- **Build a stand-in behind the same interface while the door is shut** — FEATURE — value 4 — effort M — risk med — category: waiting
  Why: assumption: many misses (a parser, a linter wrapper) can be faked well enough to finish the surrounding rows. A stub lets the dependent task's tests go red-to-green on the stub and flip to the real tool on approval.
  Done when: a task blocked on a grant closes its stub-backed criteria, and a swap check reruns them against the real tool after approval.

- **Show the pending grants as one card with a one-word answer each** — FEATURE — value 4 — effort S — risk low — category: user-ux
  Why: the user's steers repeatedly ask for less ceremony (fm ask, one-line vetoes). Several queued grants asked separately cost attention.
  Done when: `fm grants` prints each pending item with what it unblocks, source, hash, and size, and `fm grants yes 2` / `no 3` acts on them.

- **Vet a candidate in a no-network sandbox before it reaches the card** — SECURITY — value 4 — effort L — risk med — category: vetting
  Why: the standing intent plus T-0791 (injection and supply-chain defenses, 18 deferred ideas) show the concern. The user shouldn't spend a yes on something that fails on first run.
  Done when: a candidate that opens a socket or writes outside its folder in the trial never reaches the queue, and the card shows the trial result for the ones that do.

- **Scope the grant to one task and one invocation by default** — SECURITY — value 4 — effort M — risk low — category: grants
  Why: the push grant is already "set on the one task and spent on use", so the pattern exists; install grants should reuse it so a yes doesn't become a standing license.
  Done when: after the install runs once for task T, a second task asking for the same tool is queued again unless the user answered "keep".

- **Record every no with its reason and stop re-asking** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: assumption: the capability-miss trigger (T-2270) fires per session, so a refused tool would resurface each time the miss recurs.
  Done when: after `fm grants no 3 "too heavy"`, the same miss in a new session names the refusal and proposes a build instead of re-queuing.

- **Charge the wait: show elapsed days and rows idle per open grant** — FEATURE — value 3 — effort S — risk low — category: waiting
  Why: assumption: a queued grant is silent, so the user can't judge urgency. A line like "grant G has held 2 tasks for 3 days" belongs on the web UI, the pane and the resume digest.
  Done when: `fm status` and the web page list each pending grant with age and the count of tasks it blocks.

- **Audit what an approved install actually changed** — SECURITY — value 4 — effort M — risk low — category: audit
  Why: assumption: approval covers a plugin, but installs can add hooks, MCP servers or permissions beyond the name. Diffing the settings before and after makes a yes verifiable.
  Done when: after an install, a receipt lists new hooks, MCP entries and permission rules, and fails the task if any lies outside the grant's declared scope.

- **Wild: Draw the queue as a hallway of doors in the web UI** — FEATURE — value 2 — effort M — risk low — category: web UI
  Why: wild. Each locked door is a pending grant, with a sign of what's behind it and the rows waiting on it; approving opens the door with a short swing and the waiting rows light up.
  Done when: the web page renders one door per pending grant, and approving one through the UI verb changes it to open and updates the waiting count.

- **Wild: Let the user answer a grant by replying to a text or email** — FEATURE — value 3 — effort L — risk high — category: devices
  Why: wild. A user away from the terminal could say "yes 2" from a phone, but the reply channel must be one the agent cannot write to, with a nonce tied to the hash.
  Done when: a signed reply with the right nonce approves the grant, and a reply forged by the agent's own tools is rejected.

- **Wild: Rehearse the locked door with a planted missing tool** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild. Each generation plants a tool the fixture repo needs, then checks Foreman queues rather than self-installs, keeps working, and swaps in the tool after a simulated yes.
  Done when: an exam scenario passes only if no install ran before the simulated grant and the dependent rows finished after it.

- **Wild: Pre-stock a shelf of vetted tools the user approves once in bulk** — FEATURE — value 3 — effort M — risk med — category: grants
  Why: wild. Common misses (a PDF reader, a SQL linter) recur across projects; one reviewed shelf turns many future doors into open ones, each still pinned by hash.
  Done when: `fm grants shelf` lists vetted items with hashes, and a miss matching a shelf item installs without a new queue entry only for items the user marked stocked.

Next question: Which verbs can an agent session call today that write to a file the user's approval depends on, and has each been tried against the guard from inside a script the agent wrote itself?
Next question: When a grant has waited longer than the work around it can last, what does the lane do — idle, stub, or ask a second way?
