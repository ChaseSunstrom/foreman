# Brainstorm — lens: the locked door (invented): an install grant is queued for one yes from the user, never self-granted; work goes on around it meanwhile

- **Park the blocked row, keep the lane moving** — FEATURE — value 5 — effort M — risk med — category: grants
  Why: the request says grants are queued, never self-granted; assumption: nothing yet reorders work so the task needing the grant waits while its siblings run.
  Done when: a test queues a grant for task A, and `fm next` returns task B, with A shown as "waiting on grant G-n" and not as stalled.

- **Show every pending grant on one screen with a one-word answer** — FEATURE — value 5 — effort S — risk low — category: grant queue
  Why: the user's rule is "one yes"; assumption: the queue lists items without cost, source, or what is blocked behind each.
  Done when: `fm grants` prints each pending item with name, source, install command, blocked tasks, and `fm grants yes G-n` or `no G-n` records the answer.

- **Vet the candidate before it reaches the queue** — SECURITY — value 5 — effort M — risk med — category: supply chain
  Why: T-0791 (injection and supply-chain defenses) is deferred and `fm plugins find` pulls third-party code; the user's yes is only as good as what they see.
  Done when: a queue entry for a fixture plugin shows its hooks, network calls, requested permissions and publisher, and a fixture with a postinstall network call is flagged red.

- **Try the tool in a sandbox before asking** — FEATURE — value 4 — effort M — risk med — category: build-test-use
  Why: the request says "tests it, and uses it"; assumption: testing a found tool needs it installed, which is the thing needing the grant. A throwaway directory with no network could prove it works first, so the yes is for something already shown to run.
  Done when: a queue entry carries a recorded sandbox run (command, exit code, output tail) for a fixture tool, made without touching the real environment.

- **Make the grant's scope the install's scope** — SECURITY — value 4 — effort M — risk low — category: grants
  Why: the standing push-grant pattern is "set on the one task and spent on use"; assumption: install grants should do the same, not become a blanket yes.
  Done when: approving a grant for tool X lets one named install command run once; a second run, or a different package, is refused by the guard.

- **Use a stand-in while the door is shut** — FEATURE — value 4 — effort M — risk low — category: fallback
  Why: the request says build when you can't find; assumption: a throwaway stdlib script (via T-2278's scaffold) could cover the need today, with the real tool queued for later.
  Done when: for a fixture miss, the agent finishes the task with a scaffolded script and the queue holds the proper tool, and the task notes which one it used.

- **Tell the user when the answer is overdue and what it costs** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: assumption: a queued grant nobody sees silently stalls its tasks; the steer on not stopping for pace implies waiting must not become forgetting.
  Done when: a grant pending past a set age appears first in the session-start line with the number of tasks it holds.

- **Collapse repeated misses into one question** — FEATURE — value 4 — effort S — risk low — category: dedupe
  Why: T-2270 makes a tool missing in 2+ sessions one task; assumption: three sessions can each queue the same install, giving the user three yeses.
  Done when: queuing the same tool twice yields one entry with a count and a list of the sessions that needed it.

- **Remember a no, and its reason** — FEATURE — value 4 — effort S — risk low — category: grant memory
  Why: the standing rule that nothing is killed without a recorded reason; assumption: a declined tool can be proposed again next session.
  Done when: after `fm grants no G-n "reason"`, a later miss for the same tool shows the refusal and proposes an alternative, not a repeat request.

- **Audit what an approved install actually changed** — SECURITY — value 4 — effort M — risk low — category: audit
  Why: the earlier question about numbers never checked by anyone but the code producing them; assumption: nobody compares the install's real effect with what was shown at approval.
  Done when: after an approved fixture install, `fm grants audit G-n` lists files and hooks added and flags any outside the approved list.

- **Wild: Let the user answer a grant by replying to a text** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild; the door only opens for the user, who is often away from the terminal, and a one-line message could carry the answer over a channel the model cannot write to.
  Done when: a reply of "yes G-3" from a configured channel sets the grant, and the same words typed in the agent's own session do not.

- **Wild: Pre-approve a shelf of vetted tools for the user to stock** — FEATURE — value 3 — effort M — risk med — category: pantry
  Why: wild; the user, in a calm moment, ticks a list of commonly missed tools (a linter, a parser, a browser driver) ahead of time, so most doors are open before anyone knocks.
  Done when: ticked items install on a miss without a prompt; unticked ones queue; the list shows how often each was used.

- **Wild: Rehearse the locked door with a planted missing tool** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild; the standing rule wants weaknesses found by signals Foreman didn't author, so a child-authored scenario needs a tool the sandbox lacks and checks that the agent queues, never installs, and finishes the rest.
  Done when: an exam scenario passes only if the grant is queued, nothing was installed, and the unblocked work completed.

- **Wild: Draw the queue as a hallway of doors on the web UI** — FEATURE — value 2 — effort M — risk low — category: ui
  Why: wild; each locked door shows what waits behind it, and opening one animates the blocked tasks flowing through.
  Done when: the web page lists each pending grant as a door with its blocked task count, and approving one updates the page without a reload.

Next question: What does the guard do today when an agent runs an install command through a path the grant queue doesn't know (a build script, a `pip` inside a task's verify command)?
Next question: Who decides that a tool the agent built itself needs no grant, and where does a self-built script cross into needing one?
