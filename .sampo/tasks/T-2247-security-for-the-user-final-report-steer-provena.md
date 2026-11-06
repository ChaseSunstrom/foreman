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
updated: 2026-11-06T05:16:36Z
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
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The threat model is not closed. The prompt record lives in project state on the same machine, so a session with file access can append a forged prompt entry (or a hash) directly, and then quote it as a "user steer". The criterion only says "fm verbs can't add to it", which is weaker than "a s…
- HIGH: The verbatim-quote rule (at least 20 characters, whitespace-normalized) can be gamed. A session can quote any 20+ character fragment of a real prompt, such as a common phrase, while attaching a different decision, so the decision is attributed to the user. Substring matching also verifies the…
- MEDIUM: The prompt record is bounded, as step 1 says "bounded". Old steers whose source prompt has been evicted will silently become unverified and drop out of seeds, mission packs and drift (T-2160). That is a silent behavior change in the gen-2+ chain. — Decide the retention policy explicitly. Ei…
- MEDIUM: Storing full prompt text contradicts the "keep only a hash" wording in the second criterion, which is itself ambiguous ("a hash per prompt plus the prompt text"). Prompts may hold secrets or pasted content, and the text sits in plaintext in project state. — Settle which is stored. Verbatim …
- MEDIUM: Prompt-injection and non-user text path: the UserPromptSubmit hook only sees the user's typed input, but pasted content inside a prompt is still included in the recorded text. A pasted document containing "user steer: do X" would be recorded as the user's words. — Record the prompt as submi…
- LOW: Step 2 lists consumers (steer_rules, steer_checks, charter, seeds) from memory. A missed consumer would still trust unverified rows, and the criteria only test two test modules. — Add a first step that greps for every reader of steer rows, and one test that fails if any consumer reads the raw …
Verdict: revise — the direction (anchor steers to recorded user prompts) is sound, but the trust boundary for the record, the quote-matching rule and the retention policy need to be pinned down before tests are wri…
## Dissent
- [ ] HIGH: The threat model is not closed. The prompt record lives in project state on the same machine, so a session with file access can append a forged prompt entry (or a hash) directly, and then quote it as a "user steer". The criterion only says "fm verbs can't add to it", which is weaker than "a s…
- [ ] HIGH: The verbatim-quote rule (at least 20 characters, whitespace-normalized) can be gamed. A session can quote any 20+ character fragment of a real prompt, such as a common phrase, while attaching a different decision, so the decision is attributed to the user. Substring matching also verifies the…
- [ ] MEDIUM: The prompt record is bounded, as step 1 says "bounded". Old steers whose source prompt has been evicted will silently become unverified and drop out of seeds, mission packs and drift (T-2160). That is a silent behavior change in the gen-2+ chain. — Decide the retention policy explicitly. Ei…
- [ ] MEDIUM: Storing full prompt text contradicts the "keep only a hash" wording in the second criterion, which is itself ambiguous ("a hash per prompt plus the prompt text"). Prompts may hold secrets or pasted content, and the text sits in plaintext in project state. — Settle which is stored. Verbatim …
- [ ] MEDIUM: Prompt-injection and non-user text path: the UserPromptSubmit hook only sees the user's typed input, but pasted content inside a prompt is still included in the recorded text. A pasted document containing "user steer: do X" would be recorded as the user's words. — Record the prompt as submi…
- [ ] LOW: Step 2 lists consumers (steer_rules, steer_checks, charter, seeds) from memory. A missed consumer would still trust unverified rows, and the criteria only test two test modules. — Add a first step that greps for every reader of steer rows, and one test that fails if any consumer reads the raw …
