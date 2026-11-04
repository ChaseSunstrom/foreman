# Critique — Mission 5, staying lean and safe (gen 4, #12)

Tasks: T-2915 (done). Mission: gen-4/mission-staying-lean-and-safe.md.

## Closed vs planned
- Brief 1 (T-2915) is closed and merged, with a follow-up merge for the fmregen bullet. MASTER.md is now an index.
  The File map and Operations bodies moved into seven shards under docs/map (files-1, files-lib-1 to -3, ops-1 to -3).
  MASTER.md keeps one index line per entry with its link. Every other section stayed whole.
- A helper, `core.master_text`, reads MASTER.md and the shards together. Doctor's self-docs and file-map checks,
  the close-time file-map row check, release-check's runnable fences, and the scout and regen readers use it. Nothing
  that read the map lost a line. A test holds a word-multiset comparison: the moved text is the same text, reflowed.
- All four criteria are ticked. A test holds the three size limits: MASTER.md at most 90,000 bytes, each shard at
  most 90,000, and no line over 2,000 characters.
- Planned but not done: the Mission's two side leads. The `sampo burden` reading (77 characters a turn on the working
  copy against 40 on released versions) and the 2.9 GB of exam state went to "Hands to the next generation", as
  planned. They were not touched.

## Measures (first readings and due dates)
- Size. Before: 462,922 bytes, 779 lines, about 115,000 tokens, with 53 lines over 2,000 characters. Today I read
  `wc -c MASTER.md`: 82,232 bytes. `awk 'length>2000'` finds 0 long lines. Shards total 435,840 bytes. The largest
  is 76,047. These are readings of the files, not of a Read call. Moved, as the criteria define.
- Read failures. Before: in the events window, Read on MASTER.md failed 7 times and worked once, while 83 Bash calls
  grepped or sed-cut it (83 of 91 lookups). Planned reading: those two counts after the close, from state/events.jsonl.
  First reading: I have not re-counted them, and the close was only hours ago. Due 2026-11-11, on a week of sessions.
- Orientation in two reads. The Mission's long-horizon goal is a fresh agent that orients in two reads. No fresh-agent
  run has been done. Planned, not measured.
- Doctor stays green with the new reader. The full gate passed at close. That is the safety half of "lean and safe".

## Outside signals
- None. The complaint came from the gen-3 cross-cutting review, which was a Sampo reviewer's, not a user's.

## What failed
- The first claim of "lean" was a size, and size was the right thing to move. But the sum went up. Sections still
  total 435,840 bytes of shards plus 82,232 of index, 518,072 bytes, against 462,922 before. The index lines add
  weight and the text did not shrink. A session that wants one module's entry now reads two files, where it used to
  grep one. The Mission trades a refused Read for an extra hop. Whether that is a win is the open measure, not a fact.
- The rest of the dimension was untouched. The model-facing cost of the map is its size only if sessions read it. The
  83 Bash lookups suggest they grep it, so a cheaper index may change little.
- The shards are alphabetical by module, not by what a task needs. Each of three lib shards runs 65,000 to 76,000
  bytes, still more than 16,000 tokens, so one Read of a shard is still heavy.
- One plan weakness. The Mission's exam was "a read of MASTER.md succeeds", which is a unit test. The harness used
  was `bash` on a file, not the Read tool a model uses with a line cap. I cannot say a real Read succeeds on this
  file without running one, and I was told not to run things here.

## What the next Seed should change
- Count what a lookup costs end to end: tokens spent to get one module's entry, before and after, on ten real lookups
  taken from the events log. That is the true measure, not the file size.
- Add a verb-less pointer: have the global rules say "start with MASTER.md's index, then one shard". The rules line
  written by setup.py:36 still just says "System map".
- Pick up the two held leads as one small Mission: the `sampo burden` 77 against 40 difference, and the 3.2 GB of
  project state (2.9 GB in exam/). Pruning exam state touches the held-out runs, so it needs its own ask.
- Re-read the 14 test files that read MASTER.md for any that now pass vacuously, because they look in the index
  and the line they want is in a shard.
