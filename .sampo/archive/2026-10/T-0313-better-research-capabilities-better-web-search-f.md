---
id: T-0313
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-05T18:02:19Z
updated: 2026-10-06T05:44:48Z
explore: true
confirm: true
base: 90604f869c53fea354a1865672eb4bb2ae335ee9
base_tree: d0231d16f774726cb9f17265304318419c6b4800
verified: strong
---
# Research: make fm research ask find and verify information better, from a real trial run
## Raw request
> "better research capabilities, better web search/finding information"
> (fm second session: "better research capabilities, better web search/finding information" — no open item covers research or web search, and nothing visible shows it was completed.)
## Interpretation
Research quality: `fm research ask` (T-0206: planner, parallel web researchers, quote checks) exists but has never run here. Improve it from evidence, not guesses.
## Assumptions (confidence)
## Acceptance criteria
- [x] a trial fm research ask on a real question saves a cited note; each weakness found is fixed test-first or captured — verify with `python3 plugin/tests/run.py -k test_research`
## Non-goals
## Approach (options → choice → why)
(a) Redesign the research pipeline up front; (b) one budgeted trial (`--fanout 2`) on a real question, then fix what it shows. Choice: (b), cheaper and grounded in a real run.
## Risks and rollback
## Execution prompt
## Steps
1. [x] trial run on a real question; list weaknesses
2. [x] fix the top weakness test-first (or capture)
## Resume here
## Docs impact
none: the docs say a quote is checked against its page, which still holds
## Verification evidence
- (step 1) `test $(grep -c '^- [✓✗?]' state/projects/foreman-4a056f/research/ask-for-a-tauri-2-app-built-with-bun-what-do-20261006-0037.md) -ge 10` → exit 0 · (no output) [ran] [tree 5b4a162d382a] (2026-10-06T05:42:18Z)
- (step 2) `python3 plugin/tests/run.py -k test_research` → exit 0 · Ran 23 tests in 2.3s (8 classes, 16 at a time; slowest: Cross 2s, Cache 2s, Ask 1s) / OK [ran] [tree 5b4a162d382a] (2026-10-06T05:42:20Z)
- (ac 1) `python3 plugin/tests/run.py -k test_research` → exit 0 · Ran 23 tests in 2.2s (8 classes, 16 at a time; slowest: Cross 2s, Cache 2s, Ask 1s) / OK [ran] [tree 80256f58c274] (2026-10-06T05:44:47Z)
- (audit intent) `self: intent (the trial was the evidence; the top weakness was false 'not found' on real quotes, 6 of 16) + edge (CJK runs, a word cut short, extra trailing words, all-punctuation quotes stay unchecked)` → verification now marks real quotes found; a cut-short or extra word still fails [tree 80256f58c274] (2026-10-06T05:44:47Z)
- (audit edge) `self: intent (the trial was the evidence; the top weakness was false 'not found' on real quotes, 6 of 16) + edge (CJK runs, a word cut short, extra trailing words, all-punctuation quotes stay unchecked)` → CJK keeps the plain match; markdown escapes, highlighted code and \" quotes tested [tree 80256f58c274] (2026-10-06T05:44:47Z)
## Log
- 2026-10-05T18:02:19Z created
- 2026-10-06T04:07:00Z set approved=True
- 2026-10-06T05:14:12Z planned from capture
- 2026-10-06T05:36:16Z user approved confirm in Claude Code's permission prompt
- 2026-10-06T05:36:18Z focused
- 2026-10-06T05:44:48Z done
- 2026-10-06T05:44:48Z committed 5c9d716 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook /search-first — Research Before You Code (skills/playbooks/references/ground/search-first.md)
- research landscape-20261004: Asked 2026-10-04 · 3 sub-question(s) · 21 claims: 12 quote found, 7 quote not found, 2 unchecked. ✓ means the quoted words are on the cited …
- research brainstorm-20261004-round8: Test oracle (merges "pre-edit test oracle child", "request-to-oracle child", "compile examples in a request into the test", "fork in…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
## Lessons
- Run a feature on a real input before improving it: the trial showed the quote check, not search, was the weak spot (6/16 real quotes failed on markup)
## Files touched
- plugin/tests/test_research.py
- plugin/lib/fmresearch.py
- CHANGELOG.md
