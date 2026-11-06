# Lineage

## gen-1
- baseline: gen 0 has no graded line from foreman: gen 1 is the baseline
- run s31-006 (agent foreman): train closed 0; reopened: none; held out never used; cost 0.7635
- provisional: until the end-of-run exam on the production model confirms or reverses it; rests on exam run s31-006 only (4 graded lines from foreman, model haiku: a smoke signal, train only; no other signal recorded)
- seed base: gen-1

## gen-2
- baseline: gen 1 has no graded line from foreman: gen 2 is the baseline
- run s32-015 (agent foreman): train closed 3; reopened: none; held out never used; cost 0.1855
- provisional: until the end-of-run exam on the production model confirms or reverses it; rests on exam run s32-015 only (2 graded lines from foreman, model haiku: a smoke signal, train only; no other signal recorded)
- seed base: gen-2

## gen-3
- reverted: reopened untested-c-f2c372, which gen 2 closed
- run s32-015 (agent foreman): gen 3 closed 2 train vs gen 2's 3; reopened: untested-c-f2c372; held out never used; cost 0.0738 vs 0.1855
- provisional: until the end-of-run exam on the production model confirms or reverses it; rests on exam run s32-015 only (2 graded lines from foreman, model haiku: a smoke signal, train only; no other signal recorded)
- seed base: gen-2

## gen-4
- kept: closed 1 more train scenario than gen 3
- run s32-015 (agent foreman): gen 4 closed 3 train vs gen 3's 2; reopened: none; held out never used; cost 0.2177 vs 0.0738
- provisional: until the end-of-run exam on the production model confirms or reverses it; rests on exam run s32-015 only (2 graded lines from foreman, model haiku: a smoke signal, train only; no other signal recorded)
- seed base: gen-4
