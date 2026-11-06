# Mission 3 — goal to finish (gen 3, #4)

Task: T-2613 (brief 1).

Parent: gen-3/seed.md row 3 → gen-0.md #4: "Goal to finish. Turn a vague goal into a complete plan: what a finished,
best-in-class version contains, decomposed and ordered. It carries the plan over days, across crashes and
compactions, and knows when it's actually done rather than merely stopped." gen-0's goal, MUSTs and NEVERs are quoted
in the seed and apply here unchanged.

## Capability
A long goal's result read honestly: done, a real miss, or a miss the goal could not have prevented. Grounded first on
the exam, as gen-2's critique asked: `fm exam long grade l001 --agent foreman` today reads "0/6 true done, 5/20
checks" with "false_done": 6 in its JSON. T-2556's hand rerun (research long-false-done) classed the 31 failed
checks of l001 and l002: 17 out of the goal's reach ("the check demands an interface the goal text never states",
e.g. "module 'fmwatch' has no attribute '_shown'", "KeyError: 'read'"), 9 planned but not built, 5 built but
different. T-2557 already refuses a goal session's done claim while a stated Done-when line has no check. Built
too: kill, pause and compaction faults (T-2262), the dropped pinned-value goals at gen, resumes and interventions in
the grade.
What it lacks: the grader reports one false-done number. The exam's reach and Foreman's misses are mixed, so the
end-of-run long tier can't say whether Foreman got better at finishing; T-2556's split exists only as a hand-made
research note.

## Grounding
- Brief 1: fmlong.RUNNER records only the ids that pass (`ok.append(i)`); fmlong._passed returns that set;
  fmlong.grade sets `true_done` and `checks_passed` from it, and `_metrics` derives `false_done` from the session's
  last reply. No failure text is kept, so nothing can class a miss. The goal text is in the key (`key["goal"]`).

## Gaps this Mission targets (coverage: #4)
- verify × headless and judge × exam: a false done is split into misses on names the goal never states and real
  misses, in the grade the end-of-run exam prints.
- Not in this Mission: re-keying the long goals so they state those names (the keys are never rewritten by Foreman;
  re-keying goes to the tool-less child author, and that, with key reach 17 of 31, is carried in the final report),
  and running the long tier's session arms (they wait for the end-of-run exam, the user's steer of 2026-10-31).

## Ideas (from the brainstorm, grounded)
The brainstorm ran: fm mission for #4, then fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen-latest 6,
512 distinct ideas (research/brainstorm-20261102-075728). The three closest to "knows when it's actually done",
grounded against the code:
- "Say what a stop did not complete": partial. An unattended run ends with one line for anything left undone
  (fmhooks session_start, T-1228), and a goal's done claim is refused while a stated Done-when line has no check
  (T-2557). Not filed.
- "Show the 'you said / we built / not proven' receipt at finish": partial. Its own kill test says it is redundant
  if it restates the final report, and the Stop hook already re-verifies the final report's claims (T-0886). Not
  filed.
- "Mark a verdict unstable when it flips done and not-done twice": new; fmmandate.verdict keeps no history of its
  readings. Its kill test needs a flip on record and none is, so it is T-2614, deferred to 2026-12-01.
The rest stay in the brainstorm's index for the next generation's #4 Mission. The one brief below comes from the
exam's own data, which the brainstorm didn't reach: none of its ideas splits the grade's false dones.
### The grader classes its own misses
The runner keeps each failing check's last traceback line. A failure that names a missing attribute, key or import
("has no attribute 'X'", "KeyError: 'X'", "cannot import name 'X'") where X appears nowhere in the goal text is out
of the goal's reach; anything else is a real miss. A false-done goal whose every failed check is out of reach reads
apart. Prior art: SWE-bench's FAIL_TO_PASS vs PASS_TO_PASS split and its later "underspecified" filter (SWE-bench
Verified dropped tasks whose tests need unstated names). Better by: the split is computed per run from the failure
text, so neither the keys nor the goals change.

## Approaches
1. The runner writes each failing id's last traceback line beside the passing ids; grade classes each failed check
   (reach when a named miss is absent from the goal text) and counts false-done goals whose misses are all reach;
   the text says "false done N (M only on names the goal never states)". Likely outcome: l001 reads about half its
   false dones as reach, matching T-2556. Fails if: a failure line is a real bug that happens to name an unstated
   symbol (counted as reach; the rule only counts a name the goal text lacks, so a stated name is always real).
2. use what exists: keep research long-false-done as the split, refreshed by hand each generation. Fails if: the
   end-of-run exam prints one number again, which is what gen-2's critique asked to end.
3. do less: drop goals whose hidden checks use names the goal never states, at gen (as pinned values are dropped).
   Fails if: it changes which goals the exam asks, mid-tower, and hides the misses instead of showing them.

Choice: 1 (80%): the grader already runs every check; keeping its failure line costs one field, and keys and goals
stay untouched.

## Exam
The long tier itself, at zero tokens: regrade the kept runs l001 and l002 (foreman and plain arms) before and after,
and the split must match T-2556's hand classes on the named misses (17 checks out of reach). The session arms run
only at the end-of-run exam (rule 6), where the split is printed. Unit checks: a failing check that names an attribute
absent from the goal reads reach; one whose name the goal states reads real; an assertion failure reads real; a goal
with one real miss among reach misses is a real false done.

## Long-horizon goal (end of run)
The end-of-run long tier prints false dones split into reach and real, so a real false done of 0 is a claim that can
be checked.

## Lean
One field in the runner's output, one regex, one line of text. No new verb, no tokens.

## Tier share
Brief 1 is tier 3: knowing done from stopped needs a ruler that separates the exam's reach from Foreman's misses.

## Done when
`fm exam long grade` prints false dones split into those only on names the goal never states and real ones, and its
JSON carries each failed check's class and line; the regrade of l001 and l002 is recorded before and after in the
critique; the unit checks above pass; MASTER.md (fmlong), CHANGELOG and the genesis skill's exam step (step 4, which gains the long tier's split) say
it.
No site page: the exam page shows the grade line, which carries the split.

## Briefs (fm intake)
```
FEATURE: fm exam long grade splits false dones: the runner keeps each failing check's last traceback line; a failure naming a missing attribute, key or import that the goal text never mentions is out of the goal's reach, anything else is real; a false-done goal whose misses are all out of reach reads apart ("false done N (M only on names the goal never states)"), and the JSON carries each failed check's class and line; MASTER, CHANGELOG and the genesis skill's exam step say it
```
