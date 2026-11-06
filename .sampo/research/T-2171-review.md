Verdict: approve with nits (2 MEDIUM, 3 LOW)
intent MEDIUM: provisional line implied more signals than select reads -> now "rests on exam run X only (...; no other signal recorded)"
intent MEDIUM: nothing writes confirmed/reversed -> captured T-2197 (end-of-run exam writes it; report gate refuses a provisional choice); CHANGELOG says it's manual until then
maintainer LOW: sweep row untested -> GenesisSweep test asserts an unmarked choice turns the genesis check row red
maintainer LOW: marks() skipped '## gen-2 (kept)' headings -> re.match gen-\d+\b like select's stage test
maintainer LOW: old lineage sections fail with no fix named -> message says rerun fm genesis select N or add a provisional line
Noticed: none
