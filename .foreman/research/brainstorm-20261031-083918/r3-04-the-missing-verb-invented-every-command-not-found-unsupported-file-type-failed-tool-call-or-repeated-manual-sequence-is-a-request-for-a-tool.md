# Brainstorm — lens: the missing verb (invented): every 'command not found', unsupported file type, failed tool call or repeated manual sequence is a request for a tool

- **Turn every "command not found" into a ranked shim proposal** — FEATURE — value 5 — effort M — risk med — category: miss capture
  Why: T-2270 fires on a missing command once per session, but the pack shows no capture of the exact argv, cwd and surrounding intent. assumption: the PostToolUse hook sees Bash exit 127 and stderr.
  Done when: a test running `jq-ish-missing foo` writes one miss record (argv, stderr, task id), and `fm misses` lists it with the count and the candidate (installed binary, found plugin, or build).

- **Add `fm verb-vote` for unknown fm verbs and flags** — FEATURE — value 4 — effort S — risk low — category: demand signal
  Why: the user's asks (e.g. `--bench`, `--migration`, `--jobs`) were each a flag fm lacked. assumption: argparse errors are currently discarded.
  Done when: `fm nosuchverb` and `fm task evidence --nosuchflag` append to a vote log, and `fm misses --verbs` prints them by frequency with the nearest existing verb.

- **Mine repeated manual sequences into a proposed verb** — FEATURE — value 5 — effort L — risk med — category: pattern mining
  Why: the same 3-command chains (prove, evidence, finish) recur in the event log. assumption: the event log keeps Bash commands per task.
  Done when: a fixture log with a 4-command chain repeated 3 times yields a proposal naming the chain, its parameters and a failing-first test stub.

- **Map unsupported file types to a peek recipe** — FEATURE — value 4 — effort M — risk low — category: file handling
  Why: Read fails on binaries, PDFs, SQLite, parquet and similar; the lens treats that as a request. assumption: fm has no universal file-to-text verb.
  Done when: `fm peek x.sqlite` and `fm peek x.pdf` emit capped, fenced text using tools found on the machine, or name the one missing converter and queue it as a grant.

- **Wrap an installed binary into a tested verb with `fm wrap BIN`** — FEATURE — value 4 — effort M — risk med — category: tool building
  Why: `fm new tool` scaffolds stdlib scripts, but wrapping an existing CLI's `--help` is the commonest miss. assumption: the scaffold can take a spec.
  Done when: `fm wrap ffprobe` makes a script, a `--describe` output and a failing-first test that passes only with the binary present.

- **Attach a miss's replay to the tool that fills it** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: the build-test-use loop (seed row 3) needs a test of the original miss, not an invented one. assumption: miss records hold the argv.
  Done when: `fm task finish` on a tool task refuses unless its recorded miss argv, run against the tool, no longer exits "not found".

- **Offer a safe replacement verb at every guard block** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: a guard denial is a failed tool call the model then improvises around. assumption: block messages are free text now.
  Done when: each of the top 10 guard blocks prints the allowed alternative as a runnable command, and a test checks each alternative passes the guard.

- **Preflight the toolchain a task's verify commands need** — FIX — value 3 — effort S — risk low — category: preflight
  Why: red verify commands from a missing binary look like failures (see the Baseline-red tasks). assumption: verify commands are parseable for their first word.
  Done when: focusing a task whose verify uses an absent binary reports "missing tool X" instead of a later red run.

- **Collapse a miss that repeats across sessions into one find-or-build task with a cost line** — FEATURE — value 3 — effort S — risk low — category: triage
  Why: T-2270 already creates the task at 2+ sessions; the pack shows no minutes-lost figure. assumption: event timestamps bracket the workaround.
  Done when: the task body shows minutes spent on workarounds and the number of sessions.

- **Wild: Let a recorded shell session become a tool** — FEATURE — value 4 — effort L — risk high — category: tool forging
  Why: wild; the user's manual sequences already sit in logs. assumption: sessions can be replayed in a sandbox.
  Done when: `fm forge --from-session ID` yields a parameterised script and a test that replays it on a fixture, listing every path it touched.

- **Wild: Have a cold child invent the verbs fm will be asked for next** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: wild; the exam already uses tool-less child authors. assumption: a child shown only a repo's stack card can list plausible misses.
  Done when: the child's list is checked against the miss log after a week and a hit rate is printed.

- **Wild: Make `fm can "<thing>"` answer with a path and a price** — FEATURE — value 4 — effort M — risk low — category: pre-miss query
  Why: wild; asking before failing avoids the miss. assumption: the toolbelt, plugin index and lib are searchable offline.
  Done when: `fm can "convert heic to png"` prints the existing verb, installed binary, findable plugin or build estimate, ordered by cost.

- **Wild: Catch command-not-found in the user's own shell** — FEATURE — value 3 — effort M — risk med — category: shell hook
  Why: wild; misses outside the agent's sessions are also requests. assumption: bash `command_not_found_handle` can be installed opt-in, local only.
  Done when: an opted-in shell logs a missing command to the local miss file, and with no opt-in nothing is written.

Next question: Which misses were silently worked around (a heredoc script, a curl pipeline) with no error, and how would fm see them?
Next question: When a built tool is promoted, who confirms it still fills the original miss six weeks later?
