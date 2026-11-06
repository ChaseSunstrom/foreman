# Brainstorm — lens: bold bets

Ideas below are new relative to the pile, and bold means a whole capability. They share one theme: stronger proof than "tests pass" for work that is already finished.

- **Emit a behavior-diff receipt at close** — FEATURE — value 5 — effort L — risk med — category: proof
  Why: assumption: the pack shows evidence grades, mutation proof, tour and pinning for CLEAN tasks, but nothing compares what the program does before and after on real inputs. A task that passes its tests can still change behavior elsewhere.
  Done when: for a seeded task that also changes an unrelated CLI output, `fm task finish` lists that output change as "not in the request" and refuses to close until the user accepts or reverts it.

- **Trace each requirement in a spec file to its evidence** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: assumption: users hand Foreman PRDs and roadmaps (T-0843 "make it THE plugin" is a mandate with no checklist). Close-outs report tasks, not requirements.
  Done when: `fm spec SPEC.md` assigns IDs to requirements and prints a matrix of requirement, task and evidence grade. A requirement with no passing evidence shows as uncovered.

- **Flag convention outliers in the diff** — FEATURE — value 4 — effort M — risk low — category: review
  Why: `fm map` already knows the layout and the tests-to-source links. Static "standards" import exists, but nothing flags that a new file lacks something 19 of its 20 siblings have (an auth decorator, a log call, a test).
  Done when: adding a handler that omits a pattern held by at least 90% of its siblings produces a close warning naming the pattern and one sibling as an example.

- **Calibrate close confidence against code survival** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: the ledger holds 688+ closed tasks and git history. The existing signals are "held rate" and hotfixes within 24h. Survival of the lines at 30 and 90 days is a better label, and nothing scores it.
  Done when: `fm stats --survival` shows the share of each tier's lines still unrewritten after 30 days. Close-out prints "similar tasks stuck N%", computed from that history.

- **Fuzz the changed functions as part of proof** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: mutation proof tests the tests, but no step attacks the new code with generated inputs. A 60-second budget on pure changed functions fits the existing evidence ladder.
  Done when: a seeded off-by-one in a pure function is found by the generated fuzz or property test. The failing input is saved as a regression test and counts as evidence at a named grade.

- **Derive architecture rules from the import graph** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: the map already holds the layout. Layering and cycle checks come from the graph itself, not from hand-written lint config.
  Done when: `fm map --layers` prints the inferred layers. A diff that adds an upward import fails close with the offending edge, and the user can accept it as a documented exception.

- **Backport a verified task with per-branch evidence** — FEATURE — value 3 — effort M — risk med — category: landing
  Why: `fm lane` and the "landing ladder" assume a single main branch. Maintainers of release branches redo the verification by hand each time.
  Done when: `fm backport T-xxxx release/1.2` cherry-picks in a lane and re-runs that task's recorded checks on the target. It reports green or red per branch and never pushes.

- **Scan downstream consumers before changing a public API** — FEATURE — value 3 — effort M — risk low — category: blast radius
  Why: T-0788 proposes LSP references within one repo. Cross-repo tasks are listed as an idea, but finding the consumers is not.
  Done when: a task that renames an exported function lists, from a grep across sibling repos under a configured root, the files that import it. Each hit is offered as a linked child task.

- **Run dependency upgrades as a proven task class** — FEATURE — value 4 — effort M — risk med — category: maintenance
  Why: the pile has "check new dependencies at close" and advisory ranking, but not the upgrade itself. An upgrade is the most repeatable, most checkable chore (changelog read, codemod, behavior diff).
  Done when: `fm upgrade <pkg>` plans from the changelog, applies it in a lane, attaches the behavior-diff receipt and runs the gates. It closes only when all are green.

- **Wild: Run any command as of a past task with `fm at T-xxxx -- <cmd>`** — FEATURE — value 3 — effort M — risk low — category: debugging
  Why: bisect and suspects exist. "It worked last month" still needs a throwaway worktree plus the right lockfile and Python version, which Foreman could rebuild from the ledger.
  Done when: `fm at T-0400 -- pytest -k login` runs in a disposable worktree at that task's close state and leaves the user's tree untouched.

- **Wild: Distil a recorded demo into acceptance tests** — FEATURE — value 4 — effort L — risk high — category: capture
  Why: "turn a screenshot or log into a reproduction criterion" is on the pile. A short recorded terminal or browser trace of the desired behavior carries more: sequence, input and expected output.
  Done when: pasting an asciinema file or browser trace into `fm capture --demo` produces a draft failing test and a stated assumption list. The user confirms each assumption in one line.

- **Wild: Explore on a redacted twin of the repo** — SECURITY — value 2 — effort L — risk high — category: privacy
  Why: assumption: sensitive repos keep cloud-bound brainstorm and review children away from real code. A structure-preserving pseudonymized copy might still let cheap or remote agents explore.
  Done when: a twin of the fixture repo has no original identifiers or string literals. Findings from a run on the twin map back to real file:line, and a leak scan of the twin finds nothing.
