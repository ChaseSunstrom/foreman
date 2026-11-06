# Brainstorm — lens: user value

- **Add a per-session vanilla switch (`fm off --session`)** — FEATURE — value 5 — effort S — risk med — category: safety/trust
  Why: assumption: users stay on a tool they can leave instantly. Eject and fuses exist as ideas, but nothing is scoped to one session and self-restoring. Foreman's hooks, injection and pane all go quiet until Stop, and the guard stays on.
  Done when: after `fm off --session`, a test session injects 0 bytes and the pane is hidden, the guard still blocks a planted `rm -rf ~`, and the next session is back to normal.

- **Give each sub-agent role a tool allowlist and test it** — SECURITY — value 4 — effort M — risk low — category: agents
  Why: assumption: scouts and reviewers are meant to be read-only. The guard covers Bash but nothing checks that a scout can't Write or Edit. Declare tools per role in the agent definitions.
  Done when: a fixture scout told to edit a file is refused by its tool list, and `fm doctor` fails if any read-only role lists a write tool.

- **Cap what a lane can hand back to its planner** — PERFORMANCE — value 4 — effort S — risk low — category: agents
  Why: assumption: lane results re-enter the planner's context at full length, which wastes tokens and passes along injected text. Enforce a summary budget plus a file pointer for the full output.
  Done when: a lane that emits 50k characters returns at most N characters and a path, and the planner's context grows by at most N.

- **Throttle lanes while the user is active** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: assumption: parallel lanes make the machine laggy while the user types. This differs from admission by machine pressure because it follows user presence (recent keystrokes or tool activity). Run 1 lane while the user is active and up to the cap when idle.
  Done when: a simulated active user holds the lane count at 1, and it rises to the cap after the idle threshold.

- **Add a context-weight line for agents, skills and hooks, with dormant-by-default** — PERFORMANCE — value 4 — effort M — risk low — category: lean
  Why: the pack shows 1,388 skill files and agent descriptions loaded each session. Print "Foreman loads X tokens before your first word" and list the agents with zero invocations in 60 days. Dormant ones load by name only.
  Done when: session start prints the token count, and an agent unused for 60 days drops out of the preloaded list while `fm agent NAME` still runs it.

- **Poll the pane on ledger change, not on a timer** — PERFORMANCE — value 3 — effort M — risk low — category: ui
  Why: assumption: the docked pane repaints on an interval. Watch ledger mtime or inotify instead and render only on change. This cuts idle CPU and flicker.
  Done when: an idle session shows 0 pane renders over 60 s and a ledger append renders within 500 ms.

- **Count which pane tabs and web views the user opens, then fold the untouched ones** — CLEAN — value 3 — effort M — risk low — category: ui
  Why: assumption: a pane with Activity, Agents, History and Today charts is heavy for someone who reads only one. Keep the counts local, and collapse a view after 30 unopened days with one key to restore it.
  Done when: a view with zero opens in 30 days renders collapsed, and a key press expands it and resets the counter.

- **Show the exact `fm` command beside every pane row and button** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: assumption: mouse actions the user can't repeat from a script are a leaning trap. A faint "= fm task prove T-1234" label teaches the CLI and makes every action auditable.
  Done when: every actionable pane element has a copy-able command, checked by a test that parses the element table.

- **Preview a lane before spawning it (`fm lane --plan`)** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: assumption: users fear a lane's cost and reach before it runs. Print the files it may touch, the allowlisted tools, the model, a dollar ceiling and the proof it must produce, then require one confirm.
  Done when: `--plan` prints those five fields without starting a process, and the later run stays within the previewed ceiling.

- **Add a shadow-adopt step before a changed agent prompt goes live (wild)** — SECURITY — value 3 — effort L — risk med — category: agents
  Why: assumption: edits to agent definitions are self-change too, but the self-change gate looks at code. Replay 10 closed tasks through the old and new prompt with a zero-cost scorer, and adopt only if no regression appears.
  Done when: a deliberately worse agent prompt is rejected by the replay and a neutral one is accepted.

- **Add an x-ray key that highlights every Foreman-injected line in the transcript (wild)** — FEATURE — value 4 — effort L — risk med — category: ui/transparency
  Why: assumption: "what is Foreman putting in my prompt?" is the core trust question. A toggle tints injected spans by source (lesson, steer, guard note) with byte counts.
  Done when: toggling x-ray on a recorded session marks 100% of injected bytes with their source, and the totals match the hook ledger.

- **Give each agent a résumé in the Agents graph (wild)** — FEATURE — value 3 — effort M — risk low — category: ui/agents
  Why: assumption: the Agents graph shows live state but not worth. Per agent, show runs, cost, accepted-finding rate and last useful day, and click a card to retire it.
  Done when: each agent node shows those four numbers computed from the ledger, and retiring one moves it to dormant.

- **Run a hostile-lane drill that tries to exceed its lane's declared reach (wild)** — SECURITY — value 4 — effort M — risk low — category: agents/safety
  Why: assumption: the declared file scope and tool list are only trusted if something tries to break them. A scripted fake lane writes outside its scope, calls a forbidden tool and returns an oversized blob, and every attempt must be refused and logged.
  Done when: `fm drill --lane-escape` shows 3 of 3 attempts refused, with a ledger line each.

Next question: which Foreman default would the user turn off in the first week if they could do it in one key, and does the current UI make that key discoverable?
Next question: when a lane's scope, budget and tools are declared, who verifies at merge time that the lane actually stayed inside them?
