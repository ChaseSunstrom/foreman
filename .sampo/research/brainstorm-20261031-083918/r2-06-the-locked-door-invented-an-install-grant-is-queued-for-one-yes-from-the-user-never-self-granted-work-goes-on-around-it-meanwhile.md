# Brainstorm — lens: the locked door (invented): an install grant is queued for one yes from the user, never self-granted; work goes on around it meanwhile

- **Write grants to a channel the agent can't reach** — SECURITY — value 5 — effort M — risk med — category: grant integrity
  Why: assumption: the queue is a file or task field; "never self-granted" is only a promise unless the approval path is outside the agent's write access (the same class as the T-2252 USER_ONLY_FM guard fix).
  Done when: a test where a session writes or edits the grant store directly (file, `fm` verb, env var) leaves the grant unapproved and logs a refusal; only a user-run verb flips it.

- **Park the blocked row and pull the next runnable one** — FEATURE — value 5 — effort M — risk low — category: continuity
  Why: T-2270 fires the miss trigger, but the pack shows no rule for what the lane does while the door is shut; `waits_on_user` exists on tasks.
  Done when: a task whose step needs a queued grant is marked `waits_on_grant:<id>`, `fm next` skips it and returns another runnable task, and it re-enters the queue when the grant resolves.

- **Show every pending grant on one screen with a one-word answer** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: assumption: grants are scattered across tasks; the user's asks favor one-line, low-effort control surfaces.
  Done when: `fm grants` lists id, tool, source, scope, what it unblocks and its age, and `fm grants yes|no <id>` resolves it and nothing else can.

- **Vet the candidate before it reaches the queue** — SECURITY — value 4 — effort M — risk med — category: supply chain
  Why: the Injection and supply-chain defences (T-0791, 18 ideas) are still deferred, and `fm plugins find` returns third-party code.
  Done when: each queued grant carries a vetting block (publisher, last release, requested permissions, a scan for network/exec in install scripts) and an unvetted candidate can't be queued.

- **Build a stub in the meantime** — FEATURE — value 4 — effort M — risk med — category: build-test-use
  Why: the mission says to build when nothing is found; while the grant is pending, a stdlib `fm new tool` scaffold needs no grant and unblocks the row.
  Done when: for a missing tool with a pending grant, the lane uses a labelled stand-in, its output is marked "stand-in" in the evidence, and the task can't close as proven until the real tool replaces it or the user accepts the stand-in.

- **Try the candidate in a no-network sandbox before asking** — SECURITY — value 4 — effort L — risk med — category: sandbox
  Why: assumption: the user will approve faster and more safely if the card says "ran the miss's case, passed, touched only X".
  Done when: the grant card shows a sandbox run of the original miss (exit code, files touched, network attempts = 0), and a failed run shows the reason instead of a request.

- **Collapse repeated misses into one question** — FEATURE — value 3 — effort S — risk low — category: queue hygiene
  Why: T-2270 counts a tool missing in 2+ sessions; the queue could still hold duplicates from different tasks and lanes.
  Done when: three tasks missing the same tool produce one grant entry listing all three, and one answer resolves every task.

- **Remember a no, and its reason** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the pack shows the user dropping tasks with reasons; a refused grant that comes back next session is the same annoyance.
  Done when: after `fm grants no <id> --why …`, the same tool isn't requeued for 30 days unless the miss recurs with new evidence, and the refusal shows in the miss note.

- **Time the shut door and show its cost** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: assumption: the user answers faster when told "3 tasks and about 40 minutes wait on this".
  Done when: each grant card shows tasks waiting, lane-minutes idle, and age, and the digest on resume lists grants overdue past a threshold.

- **Audit what an approved install changed** — SECURITY — value 4 — effort M — risk low — category: grant integrity
  Why: a grant says yes to a name, not to a diff; the scope must match the effect.
  Done when: before and after snapshots (PATH, MCP config, plugin dir, hooks) are diffed after an install, and anything outside the granted scope fails the install and rolls it back.

- **Wild: Draw the queue as a hallway of doors in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI — wild
  Why: assumption: a locked door metaphor makes the pending state legible; each door is labelled with the tool and what waits behind it, and opens with one click.
  Done when: the web page renders one door per pending grant, with an open animation on approval and a keyboard-accessible control.

- **Wild: Rehearse the locked door with a planted missing tool** — FEATURE — value 4 — effort M — risk low — category: testing — wild
  Why: the exam already plants faults mid-run; no test shows that the session carries on and never self-grants when a tool is withheld.
  Done when: an exam scenario deletes a tool, and the run passes only if a grant is queued, other work finishes, and no install happens without the user's yes.

- **Wild: Pre-approve a shelf of vetted tools the user stocks in advance** — FEATURE — value 3 — effort M — risk med — category: standing grants
  Why: the user may prefer one session of approvals to many interruptions; a shelf with scope and expiry is a durable grant, and the user-set grant, not the agent, sets it.
  Done when: `fm grants shelf add <tool> --expires …` lets a later miss install without a new queue entry, recorded and revocable in one command.

- **Wild: Let the user answer a grant by replying to a text or mail** — FEATURE — value 3 — effort L — risk high — category: devices — wild
  Why: the user's lanes run unattended; the answer must come over a channel the agent can't write, so the reply must be authenticated (signed code, not bare "yes").
  Done when: a reply carrying the one-time code from the card resolves the grant, while an unsigned or replayed reply is ignored and logged.

Next question: What does the user do when a grant request arrives while they are away for hours, and should unanswered grants ever expire or fall back to a stand-in automatically?
Next question: Which tools has the user ever approved or refused by hand, and could those history rows seed the vetting rules?
