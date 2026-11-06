---
id: T-2247
type: SECURITY
tier: L
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T01:03:45Z
updated: 2026-11-06T03:53:58Z
---
# Only the user's own prompts count as steers
## Raw request
> SECURITY (for the user, final report): steer provenance. Any session can write a decision row that reads as a user steer (fm decide ... --cites "user steer"), and steer rows drive the cold read's charter, steer_checks, and (T-2160) every gen-2+ seed, mission pack and drift. Anchor a steer to the user's own words: e.g. only rows the UserPromptSubmit hook records from the user's prompt (with its hash) count as steers, or a steer must quote a user prompt verbatim
## Interpretation
User-approved (2026-10-31): any session can write a decision row that reads as a user steer (fm decide ... 'user steer'), and steer rows drive the cold read's charter, steer_checks and every gen-2+ seed (T-2160). Anchor a steer to the user's own words.
## Assumptions (confidence)
## Acceptance criteria
- [ ] steer_rules and every steer consumer count a decision row as a steer only when it quotes, verbatim (whitespace-normalized, at least 20 characters), text from a prompt the UserPromptSubmit hook recorded from the user; other 'user steer' rows are listed as unverified and drive nothing — verify with `python3 plugin/tests/run.py test_genesis test_core`
- [ ] The prompt record keeps only a hash per prompt plus the prompt text in the project's own state (never sent anywhere), and a session can't add to it through fm verbs — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
Options: 1) verify steers against the user's recorded prompts (verbatim quote); 2) only rows the hook writes itself count; 3) sign steer rows with a key the session can't read. Choice 1: the user's words are the authority, it needs no key management, and old steers that quote a prompt keep working; 2 loses steers written in planning; 3 can't hide a key from a session on the same machine.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Find where UserPromptSubmit records prompts (or add a bounded record of the user's prompts in project state); red tests: a steer row quoting a recorded prompt counts, one with invented words doesn't  <- CURRENT
2. [ ] Make steer_rules (and steer_checks, the cold-read charter, seeds) use only verified steers; list unverified ones
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T01:03:45Z created
- 2026-10-31T08:55:53Z blocked: needs the user: steer provenance touches who may write standing rules (security); final report
- 2026-10-31T13:21:28Z unblocked
- 2026-10-31T13:21:28Z user approved (2026-10-31 13:2xZ: 'feel free to continue, I approve everything'): unblocked to build
- 2026-10-31T13:23:44Z planned from capture
- 2026-10-31T13:23:44Z set approved=True
- 2026-10-31T14:44:36Z blocked: deferred by the user's steer of 2026-10-31 (2): finish round 1 first (Missions 4-8, critiques, drift, sweep, gen-2 seed); no new maintenance tasks until then unless one blocks a Mission; this one blocks none. Resume after gen-2's seed is filed
- 2026-11-06T03:53:58Z unblocked
## Follow-ups captured
