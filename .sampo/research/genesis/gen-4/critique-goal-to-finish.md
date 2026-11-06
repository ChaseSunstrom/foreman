# Critique — Mission 3, goal to finish (gen 4, #4)

Tasks: T-2913 (done, merged 2026-11-04 07:27Z, closed 07:59Z). Mission: gen-4/mission-goal-to-finish.md.

## Closed vs planned
- Brief 1 (T-2913) is closed and all four of its criteria are ticked.
- Criteria 1 to 3 are checked by `python3 plugin/tests/run.py test_goal`, which passed (44 tests) after one red run.
- Per criterion 1, a goal that names a file and a section gets one item per numbered entry and one per DONE-WHEN clause.
- Per criterion 2, goal plan never lists two items with the same normalized text.
- Per criterion 3, `--apply` gives a DONE-WHEN clause the check it names, and the verdict names each unmet item.
- Criterion 4 asked for a before and after reading of the live mandate in the task log. The log has no such entry. The evidence line for it is `sampo goal plan` exiting 0, and its output was a note about an unrelated task ("T-1234 was fixed later by T-1235"). The reading exists only because I ran the command today.

## Measures (first readings and due dates)
- Live plan. `sampo goal plan` today lists the 13 capabilities of gen-0 §2 ("Initiative" through "Genesis as a feature"), the three DONE-WHEN clauses, and the standard items, with no duplicate "works on the web UI surface" lines. The brief's headline defect is fixed in the plan output. Before: four copies of one model line and a one-item plan.
- Live verdict. `sampo goal verdict` today still reads "stopped: the goal has no items; clause unaccounted: Genesis: build Foreman into a self-directing harness per research/genesis/gen-0…". The plan lists items but nothing applied them. The Mission's stated purpose was that "the live Genesis goal can tell done from stopped". It cannot yet. The final step, `goal plan --apply` on the live mandate, was never run, or was run and not kept. This is the biggest finding.
- Why that matters: `--apply` is a mutation of the goal that every session reads (statusline, SessionStart note, MCP tool, Smith's prompt). The brief rightly avoided doing that unasked. But the criterion that would have checked "the verdict names the unmet items on this project" was worded as a plan listing, so it passed without it.
- False-done class. The Mission's long-horizon goal: on a replayed long goal pointing at a spec file, the done claim is refused while an entry is unmet, and the "planned but not built" class falls (9 of 31 failed checks over 12 goals in research/long-false-done.md). No replay has run. `sampo genesis status` still shows long-horizon "behind on 6 same goal(s): foreman 0/6 done, checks 4/20, false-done 6" against plain 1/6 done, false-done 5. I did not find a number that moved. Due: the next long-horizon run, which needs a replay that points at a spec file.
- Gen-3's goal-to-finish measures: the gen-3 critique is stored; this Mission did not carry any of them back, and none is named in its file.

## What failed
- A green plan is not a working goal. The criteria tested the reader (parse the doc, dedupe, map checks) and not the thing the user cares about, that the live goal gives a verdict with named misses. The same lesson as gen-3's anticipation critique: tests on synthetic goals prove the logic, the premise needs a reading on live state, and here the live reading was weaker than the claim.
- Proposals the planner still emits are junk. The plan prints "`fm` verbs that create, start, and stop goals (names not yet verified in the repo)" and similar. They are marked "not added", so they do no harm, but they name the old `fm` and verbs that do not exist. The Mission's grounding named this problem ("proposals naming verbs that don't exist") and the model line filter still lets it through as a proposal.
- Every item is a user item with no check except three. The brief said so itself ("leave the other items to their linked tasks"). Today 13 capability items have no link to a task, so even after apply the verdict would say 13 unmet with no path to done.
- The builder lane worked fast (14 minutes, merged in one pass) and the main thread closed 32 minutes later. Nothing went wrong in the hand-off. The gap was the criterion, not the lane.

## What the next Seed should change
- Run `goal plan --apply` on the live mandate as a first step of the next Mission 3 brief, and record the verdict before and after in the log. If a person must approve the mutation, ask once through `sampo ask` and move on.
- Link each capability item to its exam: item "Exhaustive thinking" checks `sampo exam scorecard` row 2, or the capability's own task. A goal whose items have no checks cannot be done.
- Write criteria on the verdict, not the plan: "on this project, `goal verdict` names N unmet items" with N in the criterion and the command in the verify line.
- Strip proposals that name non-existent verbs or the old `fm` name before printing. They teach the reader to ignore the section.
- Build the replay for "done claim refused while a spec entry is unmet". It is the only reading that tests whether the false-done class falls, and no replay exists.
