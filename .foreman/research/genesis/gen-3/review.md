# Cross-cutting review — gen-3

Reviewer model: fable
Missions' model: Opus 5.5
Inputs: sha256 3f713f8af9237f2ad1f0b9fd8f19afd9619d349b4b0fae6e00eeea6dd9191e7a
Drawn at: 478e8d3b6a4ca62a856c0edd0ab959e4e006c647
Dropped (no ground in the inputs): 0

Handled is a task id, gap (the next Seed's top gaps) or dismissed: <reason>.

| # | Question | Ground | Finding | Handled |
|---|---|---|---|---|
| 1 | worse | fully closed 2 of 3 | s32-015 foreman gen 3 dropped from gen 2's "fully closed 3 of 3" with "0 false alarms" to 2 of 3 with "2 false alarms"; the only foreman exam line this generation moved, and it moved down. | gap |
| 2 | worse | failed tool calls 1.1 → 1.6 | the friction trend shows failed tool calls up by half, steers tripled ("steers 0.1 → 0.3") and drive stops appearing ("drive stops 0 → 0.1") against the last window, so the session got rougher while the diff added 5249 lines. | gap |
| 3 | worse | true done 0/6 | l001 and l002 foreman arms sit at "true done 0/6, checks 5/20, false done 6" and "checks 4/20" in gen 3 exactly as in gen 2; nothing in this generation touched the long-tier result, only how its failures are labelled (T-2613). | gap |
| 4 | worse | plugin/skills/resume/SKILL.md | the atlas names resume at "2 of 6 needed a later fix or revert", the worst area in the tree, and no commit in this generation touches it. | gap |
| 5 | worse | T-2673 (edge, self) → T-2676 | the left-out scan closed covering fmcli alone and escaped at once into T-2676 to cover every module; a scan that "keeps the count of silent cuts at zero" was shipped while 40 other modules were unscanned. | T-2698 |
| 6 | unearned | 5249 insertions | 111 files and 5249 lines landed with no foreman exam line improving: the s21-013 run still carries only oracle, empty, finders, triggers, lanes and foresight arms, no foreman arm at all. | gap |
| 7 | unearned | plugin/lib/fmsteer.py | 338 new lines plus live expansion of every steer-shaped message "at most 40 a day" landed on a baseline of "19% of held-out clauses covered" with "48 additions the judge called harmful", and T-2627 then reported "none beat the original"; the feature shipped live at the rate the tuning failed to rai… | gap |
| 8 | unearned | plugin/lib/fmmoonshot.py | 318 lines of catalogue, rating and climb machinery landed while the campaign's own evidence is T-2687 "not-yet; no forecaster beats chance" and the lesson that "13 of 20 demoted, none promoted"; the tier mix toward 100 moonshots grows faster than any moonshot survives a kill test. | T-2701 |
| 9 | unearned | bench/moonshot/m12-run1-confounded.json | 449 lines of a run the authors themselves label confounded ("sampling 'held' from closes whose window has ended picked only the oldest tasks") are committed beside the result; a discarded run is repo growth, not evidence. | T-2702 |
| 10 | unearned | MASTER.md | the module index grows again (+28 lines) on a file Read already refuses at "75758 tokens", so the document meant to orient a session cannot be read whole by the session. | gap |
| 11 | mismeasured | 6 lost (4%) | survival counts only "134 finished the window" and reports 4% lost, while "1641 still in it (64 lost so far)" carries ten times as many losses; after T-2610 the headline rate rests on the oldest 8% of closes and "days since a lost task: 0" contradicts it in the same line. | gap |
| 12 | mismeasured | 2 of its 6 false dones | T-2613 reclassifies failed hidden checks as "only on names the goal never states", which lowers the long-tier failure read without the agent closing one more scenario; the grader moved, not the arm. | gap |
| 13 | mismeasured | 29 of 30 held | the FEATURE M record is 578 closes with "548 still in the 30-day window", so every held rate in the track record is computed over about 5% of its bucket and FIX M's "7 of 9 held" is a nine-sample claim. | dismissed: the track record line already prints its sample beside each rate ('22 of 23 held, 433 still in the 30-day window'), so a nine-sample claim reads as nine samples |
| 14 | mismeasured | 13 held out | the steer exam's "19% of held-out clauses covered (6% on train)" has held-out three times train on 13 cases, which is noise, yet the held-out figure is what reaches genesis.json and the Genesis page. | gap |
| 15 | mismeasured | 3 scenarios | s32-015 is "model haiku: a smoke signal" with "held out: found 0/0", so the only foreman grade this generation has no held-out component; nothing graded the production model on a held-out split. | gap |
| 16 | unproven | 44 blocked | the CHANGELOG states the pile line "found 5 still blocked on tasks that closed long ago" on this project, but the steer says on the same 44 "the asks/depends_on grouping found nothing" until reason text was regex-parsed; the number was produced by widening the match after the first read returned ze… | T-2709 |
| 17 | unproven | hit 52% vs 39% | the session-start guess is documented with a worked example before the feature's own floor of "at least 20 scored rows" was shown met; no exam or outcome line reports a scored next-request prediction. | T-2710 |
| 18 | unproven | 22 of 23 projects | fm drill --restore's first run is presented as a pass while one project did not read back; the one that failed is the case a host wipe rehearsal exists for. | T-2711 |
| 19 | unproven | 601 to 421 | the docs proof kind drop is reported as a fix, but 421 "--flag claims" remain that "no fm prove --docs run has checked"; the number fell by narrowing what counts, not by proving anything. | gap |
| 20 | unproven | bench/moonshot/kill_m02.py | a kill test file for M-02 landed with no m02 result file beside it, while the Genesis page now "lists the catalogue, both tiers"; a listed moonshot with an unrun kill test is presentation ahead of proof. | T-2713 |
| 21 | complaint | 75758 tokens | a user who asks the agent to consult MASTER.md watches Read fail on size, and this generation lengthens the file instead of splitting it. | gap |
| 22 | complaint | 1× credentials: '.ssh | a grep for "guard_block" counts in the agent's own ledger was refused as reading a credential, and T-2665 explicitly reverted the fix; the agent is blocked from measuring the guard's own over-refusals by the rule it was measuring. | T-2715 |
| 23 | complaint | 5× Bash: This agent is isolated in the worktree | fm lease and fm task evidence failed five times inside the worktree the harness itself put the agent in, so the evidence step the Stop hook demands ("held a turn for missing evidence") cannot be recorded from where the work happens. | gap |
| 24 | complaint | plugin/tests/test_steer.py | the guard refused the agent writing its own new test file through a Python heredoc, and the hint tells it to use the Edit tool; a harness that blocks the agent from authoring tests for the feature it is building costs a rewrite per file. | T-2717 |
| 25 | complaint | 2,733 chars | SessionStart injects 2,733 characters twice and fm burden now reads "76 characters per turn instead of 48"; the user pays more context every turn while the session-start note gained a prediction line, a pile line and a ship nudge in one generation. | gap |
