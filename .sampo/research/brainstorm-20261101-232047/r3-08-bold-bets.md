# Brainstorm — lens: bold bets

- **Verify the plan's dependency claims against the real graph** — FEATURE — value 4 — effort M — risk low — category: plan gate
  Why: assumption: plans name "what this touches" in prose, and `fm graph blast` is only advisory. A claimed edge with no match in the graph, or a graph neighbour the plan never mentions, is how blast radius gets under-counted. Blast-radius gaps ("unknown, not none") are on the list, but nothing diffs a plan's own claims against the graph.
  Done when: a plan listing a module that has no edge to the touched file is refused naming the false edge, and a plan omitting a direct dependent gets a warning naming it.

- **Enforce a plan-declared write fence in the guard** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: assumption: the existing scope checks ("flag hunks no criterion mentions", "unrequested behaviour") act after the fact. The plan could list paths it will not touch, derived from blast neighbours. The guard already sits on every edit, so it can deny out-of-fence writes mid-build and ask for a plan amendment.
  Done when: an Edit outside the fence is denied with the fence line quoted, and `fm plan amend` re-opens it with a logged reason.

- **Measure edge-case recall on real issue-to-fix pairs** — FEATURE — value 5 — effort L — risk med — category: exam
  Why: assumption: the 58 cells can be filled in prose and still prove nothing. A held-out exam takes public bug-fix commits (pre-fix tree, issue text) and scores whether the plan's edge list names what the real fix's tests exercise. The signal is external, as the standing steer on signals Foreman didn't author requires, and it comes per language and bug type.
  Done when: `fm exam run --kind think` prints edge-recall per language for foreman vs plain on at least 20 pairs authored without sight of Foreman's code.

- **Sample one coverage cell live in each real session** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: assumption: a cell filled once rots silently. One cell is drawn at random per session, its expected behaviour (refusal, line, receipt) is checked against what the session path actually did, and the observed result is logged. Over weeks, in-vivo coverage shows which cells never fire.
  Done when: `fm cells live` lists each cell's last observed-vs-expected result, and a cell unobserved for 30 sessions is flagged.

- **Attribute each reopened task to the thinking stage that should have caught it** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: the pack has many "score the miss" ideas but none that labels the stage. A fix-after-done commit or a "T-2525"-style correction is tagged readings / options / edge cases / blast / depth. The tag counts become priority weights for the cells, so the empty ones are filled by evidence of pain.
  Done when: `fm think misses` prints a per-stage count from the last 50 reopens, and `fm cells next` orders empty cells by it.

- **Minimise plans by deleting steps** — PERFORMANCE — value 3 — effort M — risk med — category: plan gate
  Why: assumption: L plans are padded. A lane drops each plan step in turn and re-runs the done-when. Steps whose removal changes no result are flagged as ceremony, which is "do less" enforced by test instead of by taste, and supports the lean ratchet's pay-by-deletion rule.
  Done when: on a recorded L plan, the tool names at least one step whose removal left the done-when green and one whose removal turned it red.

- **Retrieve a worked deliberation as a few-shot exemplar for weak models** — FEATURE — value 4 — effort M — risk low — category: fm code
  Why: assumption: `fm code` on cheap or local models skips readings and options, and scaffolds are listed but not the retrieval. Closed tasks that passed first time and were never reopened become an exemplar bank, matched by task shape. All data stays local.
  Done when: a 4k-context local model given an exemplar produces a plan the gate passes, where it failed without one, on three held-out tasks.

- **Compile the plan to a lane DAG that carries its own falsifier** — FEATURE — value 4 — effort L — risk med — category: lanes
  Why: assumption: today a plan is prose that humans and lanes re-read. Compiling Approach steps into lane briefs, with the falsifier as a mandatory last node, makes "test candidates in parallel lanes and choose by evidence" a mechanism and not a convention.
  Done when: `fm plan run` spawns one lane per approach, each ending in the falsifier command, and records which lane's falsifier held.

- **Make the thinking gate callable as a plan token for hookless harnesses** — FEATURE — value 4 — effort M — risk med — category: devices/harnesses
  Why: Codex, Gemini and opencode lack the Stop and PreToolUse hooks (T-0337, T-0335 are blocked). An MCP `fm_think` call that validates the plan and returns a token, plus a git pre-commit check for that token, gives them a gate through the channel they do support. Whether the token is forgeable is an assumption to test.
  Done when: a commit from a hookless harness without a valid plan token is refused locally, and the same flow passes with one.

- **Assert the plan against every standing steer as code** — FEATURE — value 4 — effort M — risk low — category: steers
  Why: the pack holds about 40 standing rules, such as the round-first hold and the ban on templated cells, and the rule is that each becomes an automatic check. The gap is checking a plan against them before it is accepted. A plan that would break the lean ratchet or push without `fm ship` is flagged with the steer's date.
  Done when: a plan containing a direct `git push` is refused citing the 2026-10-30 push steer, with a fixture per checked steer.

- **Wild: Run a fence tabletop where a child tries to sneak out of the plan** — SECURITY — value 3 — effort M — risk low — category: red team
  Why: wild. A tool-less child sees only the plan and fence and writes the three commands it would use to do forbidden work in scope. Those commands replay against the guard to expose fence and guard holes before a real build finds them.
  Done when: the replay report shows which child commands the guard denied, allowed or misparsed, and each allowed one becomes a failing test.

- **Wild: Reward the planner for questions it correctly did not ask** — FEATURE — value 3 — effort M — risk med — category: stops
  Why: wild, and only partly assumption. The pack scores stops that mattered, but nothing credits an avoided ask that turned out right. When Foreman proceeds on a decide-instead-of-ask receipt and the user never undoes it, that is a point. Stop thresholds then learn from both directions.
  Done when: `fm doctor` shows asked-and-mattered, asked-and-didn't and proceeded-and-held counts per question class.

- **Wild: Write the user's likely first objection into the plan, then check it at close** — FEATURE — value 3 — effort S — risk low — category: plan gate
  Why: wild. A one-line "you'll probably say X" is built from the user's own correction history. At close it is checked against what the user did say. A miss shows the model of the user is wrong, and a hit lets the plan address it up front.
  Done when: plan and close both carry the line, and `fm outcomes` reports a hit rate over 20 tasks.

- **Wild: Run a blind cell-writer and diff it against reality** — CLEAN — value 3 — effort M — risk low — category: coverage
  Why: wild. A tool-less child, given only the grid's row and column names, invents what each of the 58 empty cells ought to hold. Its answers are diffed against code behaviour: matches suggest an existing feature path, misses suggest real gaps, and cells where it claims a capability the repo lacks become tasks.
  Done when: the diff report splits the 58 cells into existing, gap and n/a, each with a grep or test citation.

Next question: Which of the 58 cells has a user correction in the "asked" history that it would have prevented, and do the stage-attributed misses agree with the cell grid's own weighting?
Next question: When no user is present, which deliberation gates currently ask nothing, fail open, and leave no trace the next morning?
