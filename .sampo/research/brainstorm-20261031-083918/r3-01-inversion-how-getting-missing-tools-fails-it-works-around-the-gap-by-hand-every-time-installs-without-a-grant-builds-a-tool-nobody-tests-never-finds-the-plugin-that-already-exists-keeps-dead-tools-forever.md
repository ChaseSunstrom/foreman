# Brainstorm — lens: inversion: how getting missing tools fails: it works around the gap by hand every time, installs without a grant, builds a tool nobody tests, never finds the plugin that already exists, keeps dead tools forever

- **Shim every package manager in the session** — SECURITY — value 5 — effort M — risk med — category: grants
  Why: the pack covers blocking installs without a grant, but a built script or MCP server can call `pip`, `npm` or `curl | sh` itself at runtime, and a hook can't see that. Assumption: the guard only sees the agent's own Bash calls.
  Done when: a built tool that runs `pip install x` internally is stopped, queued as a grant card, and a test shows the install never ran.

- **Prove the gap is real before searching or building** — FEATURE — value 4 — effort M — risk low — category: miss triage
  Why: a "can't do" is often a missed use of a tool already present. Assumption: nothing checks that a miss is genuine. A cold child, given only the miss and the current toolbelt, tries to do it with existing tools. Only a failure there opens a find-or-build task.
  Done when: a planted miss that `jq`, `sed` or an installed MCP verb already covers closes as "false miss" with the command named, and no tool task is filed.

- **Test whether a shelf tool can be found from its description** — FEATURE — value 4 — effort M — risk low — category: dead tools
  Why: a tool whose description a future session never matches is as dead as an unused one. The pack covers use ledgers and retirement, but not discoverability. A cold child gets the shelf listing and ten past misses and picks a tool for each.
  Done when: `fm tools doctor` prints the discoverability rate per tool and flags any tool missed in all N probes.

- **Run every built tool in a clean room before it counts** — FIX — value 4 — effort S — risk low — category: build-test
  Why: a tool can pass because of the session's cwd, venv, env vars or a file left in `.fm-scratch/`. Assumption: its tests only run in the build environment. Re-run them under `env -i` in a fresh temp dir with only declared inputs.
  Done when: a fixture tool that reads an undeclared env var passes in-session and fails the clean-room run with the variable named.

- **Expire "nothing found" results with index age** — FIX — value 3 — effort S — risk low — category: search
  Why: a negative result from a stale plugin or library index looks the same as "nothing exists" and justifies a needless build. Assumption: `fm plugins find` and `fm lib search` don't date their results. Stamp each result with the index age and re-search when it is older than N days.
  Done when: a find against an index older than the threshold refreshes it first, or says "stale, N days" beside an empty result.

- **Flag a tool that was built but never invoked before its task closed** — CLEAN — value 4 — effort S — risk low — category: silent workaround
  Why: the agent may build a tool to satisfy the loop and then keep working around the gap by hand. At `fm task finish`, compare the tool's creation against the event log's invocations for that task.
  Done when: a task that builds a tool and never calls it is listed in the finish audit as "built, not used", naming the hand-run commands that did the job.

- **Cap the build loop per miss and then ask** — PERFORMANCE — value 3 — effort S — risk low — category: budget
  Why: assumption: nothing bounds the build-test-use loop, so a hard miss can burn a whole session on a one-off need. Set a ceiling in minutes and attempts per miss. When it is hit, the loop parks the row and files one `fm ask` with what it tried.
  Done when: a planted impossible miss stops at the cap with an ask naming the attempts, and the lane moves to the next runnable task.

- **Detect a built tool shadowed by a same-named binary** — FIX — value 3 — effort S — risk low — category: dead tools
  Why: a built script or verb named like an existing PATH binary or skill is never run, so it is dead on arrival. At creation and at doctor time, resolve each shelf name through PATH and the skill listing.
  Done when: a shelf tool named `ls2json` alongside a PATH binary of the same name is reported as shadowed, with the resolution order shown.

- **Rate each grant approval for attention** — SECURITY — value 3 — effort M — risk med — category: grants
  Why: assumption: a long grant queue gets rubber-stamped. Record time-to-answer and whether the card was expanded. A grant answered under a threshold without the diff or sandbox report being opened is marked "unread" in the audit and may be re-asked once.
  Done when: `fm grants` lists "unread approvals" and a test shows a 1-second blanket approve is flagged.

- **Wild: Slip a decoy grant into the queue** — SECURITY — value 3 — effort M — risk med — category: grants
  Why: wild. Occasionally the queue carries a harmless, clearly labelled bad request, such as a lookalike package name. If the user approves it, Foreman reports it gently and tightens its summaries. It measures whether the grant gate works rather than assuming it does.
  Done when: a decoy approved in a test run is logged as "attention miss" and never installs anything.

- **Wild: Write the README first and have a cold model use the tool from it** — FEATURE — value 3 — effort M — risk low — category: build-test
  Why: wild. A tool that only its author can drive is a form of dead tool. A cold Haiku child gets only the `--describe` text and the original miss and must complete it. Failure sends the writer back to the docs, not the code.
  Done when: a tool with an ambiguous usage line fails the cold-use check, and the same tool passes after the doc is fixed.

- **Wild: Replay the whole acquire loop against a seeded broken world** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: wild. Plant all five failures in a throwaway repo: a missing tool, an existing plugin to find, a tempting unauthorized install, an untestable parser request, and a dead shelf entry. Score whether Foreman finds, queues, tests and retires correctly. The scenarios are written by a tool-less child that never sees the code.
  Done when: `fm exam` prints a per-failure-mode pass rate for the acquire loop, with the free arm beside it.

Next question: What does Foreman do when the "tool" it needs is a credential or an account, such as an API key or a login, rather than code, and how does that reach the grant queue?
Next question: Which of the five failure modes has the cheapest tripwire today, and which has none that a model didn't write?
