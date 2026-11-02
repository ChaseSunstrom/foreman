# Mission 6 — exhaustive thinking (gen 3, #2)

Task: T-2671 (the Mission's own grounding and filing), T-2672 (brief 1), T-2673 (brief 2), T-2674 (brief 3).

Parent: gen-3/seed.md row 6 → gen-0.md #2 "Exhaustive thinking". gen-0's goal, MUSTs and NEVERs are quoted in the seed
and apply here unchanged.

## Capability
Foreman covers the whole space of a request and says what it left out. Three places still drop part of the space
silently: a brainstorm has no lens that forces every surface-by-actor cell, a printed list cut at N says nothing of the
rest, and grounding accepts a "not found" without checking that its search could find anything at all.

## Grounding
- Brainstorm: fm mission for #2, then fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen-latest 6: 397
  distinct ideas (research/brainstorm-20261102-151147). Three recon passes grounded them in 44 clusters (54 built, 186
  partial, 156 new, 2 false premise; 24 marked build), recorded with fm research add as
  research/brainstorm-20261102-m6.md. Mission 5's critique asked for more grounding: these passes spent 102 to 104 tool
  calls each, against about 8 before.
- Spot check, true: fmideas.LENS_NOTES (fmideas.py:28) holds reframe, flip assumptions, oblique provocation, devil's
  idea, worst-bugs persona and blind spots. No lens crosses surfaces with actors and failure modes cell by cell.
- Spot check, true: 22 of the 41 truncated `join(...[:N])` outputs in fmcli.py print no count of what was cut
  (counted by reading the line and its neighbours for "more", "left out" or a len()).
- Spot check, true: plugin/skills/brainstorm/SKILL.md step 4 asks for three phrasings and help strings before an idea
  counts as new, but runs no canary, so a search that can't find anything reads the same as an idea that isn't built.
- Counted and carried, beside fmcore.stale_refs (fmcore.py:5432): a plan-time check of the briefs' path:line
  citations. It differs from stale_refs, which only re-checks named paths on resume, but today it would catch 3 of 432
  citations (0.7%: a missing file or a line past its end). It stays in the catalogue, marked build, behind the three
  gaps below that each clear more.

## Gaps this Mission targets (coverage: #2)
- find × fm code: a brainstorm can skip whole cells of a request's space without anything noticing.
- understand × CLI: a list cut at N hides the rest, and the reader can't tell there was more.
- verify × fm code: grounding treats an empty search as proof of absence.
- Not in this Mission: the repeat-correction sibling sweep, brief claim resolution at filing and the stop-reason exit
  codes. They are marked build in the catalogue and carried to the next seed.

## Ideas (from the brainstorm, grounded)
- "Brainstorm by morphological grid, one idea per cell" is new. That is brief 1.
- "Print 'N left out' on every truncated list, with the flag that shows them" is partial (19 of 41 sites do). That is
  brief 2.
- "Run a grep canary before accepting any 'not found'" is new. That is brief 3.
- The other 21 build clusters stay in the catalogue with their marks.

## Exam
- Brief 1: `fm ideas --lens grid` sends the grid note, and its prompt names the request's surfaces and actors from the
  pack. A unit check asserts the note asks for one idea per cell.
- Brief 2: each fmcli list that cuts at N ends with "N left out" and the flag that shows them. A test feeds N+3 items to
  each changed site. The count of silent sites goes from 22 to 0.
- Brief 3: test_brainstorm_skill asserts the canary line is there, which proves only the text. Use is measured on the
  next Mission's grounding (Mission 7): its catalogue counts the "new" verdicts that carry a canary result, and the
  critique reports that count against the "new" verdicts in all.

## Long-horizon goal (end of run)
No Foreman output hides part of the space it was asked to cover: every cut says what it cut, and every "not found" was
found able to find.

## Lean
Brief 1 adds one lens note, brief 2 one helper that replaces repeated code, and brief 3 one skill line. No new verb, no
new state file.

## Tier share
All three are tier 2 (S): small, measured gaps, each with its check.

## Done when
- Each brief closes with its own criterion command green on the closing tree.
- Brief 2's outcome: the silent-truncation count, recounted by the same method, goes from 22 to 0.
- Brief 1's outcome: Mission 7's brainstorm runs with `--lens grid`, and its catalogue reports how many grid cells
  produced an idea that survived grounding.
- Brief 3's outcome: Mission 7's catalogue reports how many "new" verdicts carry a canary result.
- All three numbers go into gen-3/critique-exhaustive-thinking.md. A zero in either Mission 7 count is a failure the
  critique names, not a pass.

## Briefs (fm intake)
```
FEATURE: a grid lens in fmideas.LENS_NOTES crosses the request's surfaces with its actors and failure modes and asks for one idea per cell; fm ideas --lens grid selects it and the brainstorm skill names it for exhaustive requests
FIX: every list fm cuts at N says how many it left out and the flag that shows them: one helper in fmcore used by the 22 fmcli sites that cut silently
FEATURE: the brainstorm skill's grounding step runs a canary search for a term known to exist in the same scope before it accepts any "not found", and test_brainstorm_skill asserts it
```
