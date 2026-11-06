# Cross-cutting review — gen-4

Reviewer model: fable
Missions' model: Opus 5.5
Inputs: sha256 be8ac729703abbe462d1d6b2e9facde2ecf60119b47b82d7468d8400b330075e
Drawn at: 192dab33599aaf96ccf9e0cd61897d7f5211a1b2
Dropped (no ground in the inputs): 2

Handled is a task id, gap (the next Seed's top gaps) or dismissed: <reason>.

| # | Question | Ground | Finding | Handled |
|---|---|---|---|---|
| 1 | worse | false done 6 | Sampo's own arm reports done falsely on every scenario (l001/l002 foreman: true done 0/6, false done 6, gens 2 and 3) while the plain arm manages 1/6; the discipline layer scores below no layer at all and nothing in the diff touches it. | T-3057 |
| 2 | worse | 0.6 → 1.3 | Failed tool calls per 100 doubled over the pass, most of them the harness's own worktree isolation ("21× Bash cat", 8× sed, 8× python3) refusing its builders' commands. | T-3058 |
| 3 | worse | Bin 226340 -> 33 bytes | site/assets/share.png shrank from a real image to 33 bytes (a symlink); the share card published by Pages now depends on the deploy dereferencing it, and no shipped check proves it does. | T-3059 |
| 4 | worse | T-2992 (adversary, edge, intent) → T-3001 | The repeat-failure firewall itself escaped its close: a defect found after finish in the very task meant to stop repeat failures, with all three lenses having passed it. | T-3060 |
| 5 | worse | fully closed 2 of 3 | s32-015 went 3/3 at gen 2, 2/3 with 2 false alarms at gen 3, 3/3 at gen 4 on the same 3 scenarios; the smoke signal flaps and the generation ships on it anyway. | T-3061 |
| 6 | unearned | 136193 insertions | 974 files and 136k lines in one generation, most of it a package rename that duplicates every fmX.py as sampo/X.py plus a shim, so the library now exists twice in the tree. | T-3062 |
| 7 | unearned | plugin/web/live/live.js | 1,704 lines of browser steering (drive, checkpoint, pause, notes via POST /api/act) landed with a hand-rolled CSRF wall and a stated hole (port forwards read as your uid) while no exam line measures it. | T-3063 |
| 8 | unearned | research/models/bench.jsonl | 2,092 lines of bench output committed into the repo as data; every rerun will grow the diff and nothing reads it at runtime. | T-3064 |
| 9 | unearned | design/sampo/directions/emberline/README.md | Three losing logo directions (emberline, orrery, runestone) with SVGs and READMEs stay in the tree after direction 12 won and shipped under design/sampo/logo. | T-3065 |
| 10 | unearned | plugin/lib/sampo/cli.py | The CLI monolith moved and grew to 8,724 lines in the move; the rename was the chance to split it and instead added verbs users then reach for that don't exist ("fm models", "fm plan", "fm stop"). | T-3066 |
| 11 | mismeasured | 191 finished the window | Outcomes quote "49 of 50 held" style hold rates while 1769 of 1960 closes are still inside the 30-day window and 75 of those already lost; the track record is read on under 10% of closes. | T-3067 |
| 12 | mismeasured | 0.77 on type | The retrieval decider's 0.77 is on the 92% it answers, compared against 0.60 for majority on all 200 briefs; abstentions are dropped from the numerator but not the baseline. | T-3068 |
| 13 | mismeasured | 259/376 (naive 256) | The next-request predictor ties the naive guess on replay (paths 0.088 vs 0.086) yet ships as a scored arm "shown only when it leads"; three rows over naive is noise, not a lead. | T-3069 |
| 14 | mismeasured | p95 315 ms | Live hook p95 is 315 ms over 11,974 runs while the lean gate reads ~36 ms by excluding runs above LOAD_BAR and holding only rises seen in two of three interleaved pairs; the SLO now measures the quiet machine, not the one users have. | T-3070 |
| 15 | mismeasured | 0.64 on tier against 0.12 | A majority baseline of 0.12 on tier is impossible for any class that is actually a majority; the Jeff LoRA result is on one held-out project with a baseline that cannot be right. | T-3071 |
| 16 | unproven | 0 to 3 of 8 | CHANGELOG claims the 12B went from 0 to 3 of 8 fixed once served 32k with reasoning off; the exam line for gpu-gemma12-32k shows fixed 0/3, and jarvis-nothink fixed 0/3. | T-3072 |
| 17 | unproven | AUC 0.55 | The close-holds verifier is wired into task finish on a held-out AUC of 0.55 pooled, one point above chance, with the 0.73 figure coming from one project; it is in shadow because it does not work. | T-3073 |
| 18 | unproven | 400 calls, 0 kept | Small-model cards are presented as "about 1 in 6 passes" with "the first long grow is running"; the only landed number is 400 calls and 0 kept. | T-3074 |
| 19 | unproven | 4 of 10 scenarios | Loop-break shipped against loops ending 4 of 10 scenarios, and the next smith exam (s0-001, gpu-qwen4-32k) is found 1/8, fixed 1/8, closed by missing-tool; no line shows loops fell. | T-3075 |
| 20 | complaint | false done 6 | The user's first question: why does my harness say done on 6 of 6 scenarios it did not finish, for two generations running, while this generation rebranded it and gave it a live page. | T-3076 |
| 21 | complaint | 11× core:interpreter-code-driving-foreman | The guard blocked its own builders 18 times for running python against Sampo's modules, the top-firing rule, and T-2261 about that very rule has sat open in the self-inbox all generation. | T-3077 |
| 22 | complaint | 142,399 chars | SessionStart injected 142k characters over 95 sessions and one stack-card note fired 23 times; the user pays that context every session for notes the friction report itself flags as repeated 3+ times. | T-3078 |
| 23 | complaint | T-2082 Can you add pages for ALL | The site was re-skinned six times (T-2753, T-2759, T-2851, T-2852, T-2957, T-2964) while the user's own asks for feature pages with charts (T-1792, T-2082) stay open. | T-3079 |
