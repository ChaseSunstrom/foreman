# Brainstorm 2026-10-20: super-improve Foreman, adapted to Claude Code 2.1.304 (T-1252)

Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
simplicity, bold bets, performance), 3 rounds + 3 deepen rounds (cost, benchmarks, trust), past the 5 previous
brainstorms. 368 distinct ideas: research/brainstorm-20261020-084630/ideas.md. Every idea is in one cluster below; the
line numbers are ideas.md's. Grounded with targeted reads and greps (fmcost, fmhooks._auto_evidence/_runner, fmbench
results, the foreman-ui mod, fmscout, the long-session transcripts).

Score: value 1-5 · effort S/M/L · risk · mark.

## C1 Cost attribution and meters (lines 7,14,16,17,29,33,42,50,59,94,103,111,114,115,124,135,141,161,214,252,341,351,356,378)
Ideas: meter the Foreman tax per session; per-turn cost ledger by source; live tax meter; tax receipt; why a turn was
expensive; cost per verified pass; cost as share of plan window; ghost bill; break-even page; per-close discipline cost;
honest bill split; rank fm verbs by tokens returned; budget fm stdout per task; idle footprint.
Grounding: `fm cost` exists (tokens by task, tool-result share, first-reply context) but has no "Foreman's own share"
(skill listing, hook notes, fm output). The long-session tally (this session) found Foreman's part by hand.
Score: 5 · M · low · BUILD (round 1): cost per fully-correct session on the page (S); Foreman's share in fm cost (M).

## C2 Context tax (injections) (5,8,15,19,53,64,72,82,88,109,163,165,195,197,199,200,204,211,212,215,240,247,301,313,330,344,349,350,352,357)
Ideas: suppress notes already in context; deltas only; notes on demand; Foreman diet; self-deleting features; ratchet
injected bytes in CI; collapse skills into a router; take user-only skills out of the listing; squeeze tool output; stub
superseded re-reads; cap subagent reports; terse output; lower effort on bookkeeping turns; two-char dialect; silence
injections in read-only forks; observer mode; golden-file injected text.
Grounding: T-1253 (today) cut the listing 2,730 → <2,000 chars with a budget test; the long-session transcripts show a
"stack card python: its notes were shown earlier" note repeated 5 times and a stack-card suggestion for "spreadsheets"
on an INI task. No byte budget on hook notes exists.
Score: 4 · M · low · BUILD (round 1): a context-tax ratchet over a replayed hook session (per event, bytes), and drop
repeated one-line notes. Router skill: SKIP (routing quality risk; listing already capped). Dialect/observer: later.

## C3 Bookkeeping the model doesn't do (24,43,54,62,79,89,101,154,278,328,348)
Ideas: tick criteria from observed proofs; infer bookkeeping from tool results; record proofs from PostToolUse; Haiku
sidecar; chain bookkeeping in one call; native todo list as step ledger; bind to plan mode.
Grounding: `_auto_evidence` already records a Bash run that is exactly a criterion's verify, and `_runner_evidence` a
same-runner pass for the step; both skip piped commands (`_runner` returns None for `|`), and the long-session agent
piped every run (`… 2>&1 | tail -n 40`), then called fm task evidence 5-12 times a run.
Score: 5 · M · med (a piped exit code is tail's) · BUILD (round 1): count a piped run (to tail/head/grep) as evidence
when its output carries the runner's own pass or fail summary.

## C4 Compaction strategy (6,21,22,32,44,45,46,52,56,57,66,75,90,95,107,119,170,213,221,250,254,296,315,343,347)
Ideas: tune the window by measurement; compact at task seams; when the cache is cold; fresh handoff vs compaction;
re-inject only what was dropped; write the summary from the ledger; fresh-eyes pass; pinned thought; quiz after
compaction; compaction storm soak.
Grounding: T-1242/T-1231 re-inject the active request after compaction; Claude Code exposes no way for a hook to start a
compaction or write its summary; window tuning is per user (CLAUDE_CODE_AUTO_COMPACT_WINDOW).
Score: 3 · M-L · med · LATER (captured): a compaction-storm soak in the bench (cheap on Haiku) and the window sweep.

## C5 Benchmark rigor (18,20,63,70,71,78,97,106,126,127,128,133,139,152,159,160,164,177,201,202,229,243,245,249,255,279,358,359,363,364,367,370,371,372,379,381)
Ideas: ablate components; stamp results with model, CC version, prompt hash; refuse deltas inside noise; sequential
stop; paired runs with intervals; calibrate where plain Claude fails; decompose the long-session premium; equal-dollar
duel; external benchmark subset; private holdout; false-done rate; prompt-injection benchmark; rival plugins (exists:
fm bench duel PLUGIN); pre-registration; signed bundles; claims ledger with expiry; grey out stale claims.
Grounding: results carry model, label, plugin, head; no Claude Code version. Ablation exists for rule/skill files (fm
evolve --drop), not for hook features.
Score: 4 · S-L · low · BUILD (round 1): Claude Code version in every result and on the page (S). LATER: noise bands,
ablation of hook features, equal-dollar duel, false-done benchmark.

## C6 Site and showcase (11,25,26,28,38,40,74,83,96,99,125,130,131,138,144,145,156,168,205,248,264,288,289,311,335,366,375,377,380)
Ideas: figures from results (DONE T-1246); theme flash (DONE T-1246); losses page; saved-first table with reasons;
`fm bench repro`; run-it-yourself; beat-Foreman challenge; failure reel; guard in the browser; layout fuzz.
Grounding: the Benchmarks page now computes its figures; its "Method and limits" covers losses in prose.
Score: 3 · S-M · low · LATER (captured): a generated "Where Foreman loses" section; `fm bench repro`.

## C7 Claude Code version tracking (12,13,23,27,48,49,60,67,73,81,92,137,148,175,176,181,184,227,244,291,292,293,299,361,374)
Ideas: duel/safety corpus per release; nightly roundtrip on the newest build; bisect versions; what a release made
redundant; version ranges per feature; probe facts instead of remembering; self-check on a new version; mod anchor
drift; prove the headless drive under the 2.1.304 Stop rule; 12-per-event hook cap.
Grounding: fmscout files "Adopt Claude Code X" when a newer one ships; CC_TESTED now 2.1.304 (T-1253); the marathon
and long duels ran on 2.1.304 with Stop-hook continuation working; Foreman's hooks are command hooks (the 12-cap is for
prompt/agent hooks).
Score: 3 · S · low · BUILD (round 1, with C5): the bench records the CC version; the headless-drive proof stands on the
long duels. LATER: safety corpus per release.

## C8 Approvals through decider "person" (9,41,47,55,80,91,179,209,290)
Ideas: decider:"person" for fm ask and guard asks; replace the home-grown binding; passkey/physical key; expire asks
tied to dead processes.
Grounding: `decider` is a mod `tool.check` answer; foreman-ui has no tool.check, and the installed foreman-ui is 0.7.0
against the repo's 0.18.2 (updating it needs the user's yes). Foreman binds chat approvals to the asking process
(T-1226/T-1233/T-1236).
Score: 3 · L · med · LATER (captured; needs the mod update the user must approve).

## C9 Guard hardening (34,77,105,146,155,157,162,174,187,207,239,241,265,280,281,282,314,329,376)
Ideas: evasion variants of the 24; honeytokens; export the guard as native deny rules; receipt per refusal (exists:
every refusal names its fix); seal the wiring (exists: core protection); guard in forked/background subagents; state
unreadable; memoize verdicts; audit a cloned repo's own Claude config.
Grounding: the safety bench has 24 dangerous + 25 everyday; fmguard has mutation testing (fm bench guard --mutate).
Score: 4 · M · low · LATER (captured): evasion variants of the 24 as a corpus; cloned-repo config audit.

## C10 Hook performance (85,104,108,217,218,219,220,286,306,326,332,333,334,336)
Grounding: p95 49-67 ms per hook, 274 ms for a Bash script read; pycs precompiled; one dispatcher already.
Score: 2 · M-L · med · SKIP for now (no user-visible cost; revisit if the bench shows hook time).

## C11 CI and portability (10,61,68,69,158,178,180,203,274,287,294,303)
Grounding: T-1249 open (macOS job, experimental); Linux green after T-1248.
Score: 3 · M · low · BUILD (round 2): T-1249 macOS portability.

## C12 Simplicity and footprint (84,86,88,100,188-196,198,302,304,305,307,308,309,312)
Grounding: fm posture lite exists; a 40-line CLAUDE.md variant doesn't.
Score: 3 · M · med · LATER (captured): "Foreman in one CLAUDE.md" for people who won't install; dead-code sweep.

## C13 Unattended economy and cache timing (51,58,93,98,110,117,121,122,123,134,216,222,223,231,233,273,316,331,346)
Grounding: fm contract (T-1158) prices a run; fm ideas runs one claude -p per lens with the whole pack (2,870 words x
9 lenses x 3 rounds this run).
Score: 3 · M · low · LATER (captured): run the lens fan-out as fork subagents of one cached pack.

## C14 Ceremony that adapts (118,136,166,230,232,242,345)
Grounding: unattended FEATURE tasks already skip the recorded red run (T-1231); S tasks auto-close at stop.
Score: 3 · M · med · LATER (captured): ceremony profile per task kind and model, set from duel data.

## C15 Pane and UI delight (31,35,36,37,39,142,182,253,256-263,276,283,285,320,324)
Grounding: T-1217 (pane background) open; the mod update waits on the user.
Score: 2 · S-M · low · LATER (with the mod update).

## C16 Onboarding and user context (120,226,228,234-238,246,260,270,275,284,321)
Grounding: fm away (return summary) and whats-new notes exist; no CLAUDE.md conflict check; no /rewind reconcile.
Score: 3 · M · med · LATER (captured): reconcile after /rewind and /clear; CLAUDE.md conflict check.

## C17 Integrations (116,132,149,150,153,167,171,172,173,186,210,266-268,271,272,277,317-319,322,325,327,337,338)
Grounding: --json on 18 verbs; GitLab mentioned in 4 files; ran-zero-tests is red already (T-1117).
Score: 2 · M-L · med · SKIP for now.

## Slate, round 1 (value for effort)
1. Cost per fully-correct session on the Benchmarks page (C1, S, value 5)
2. The Claude Code version in every bench result and on the page (C5/C7, S, value 3)
3. Piped test runs count as evidence when their output shows the runner's summary (C3, M, value 5)
4. Foreman's own share of the context in fm cost (C1, M, value 4)
5. A context-tax ratchet over a replayed hook session; repeated one-line notes said once (C2, M, value 4)
Round 2: T-1249 macOS CI (C11). The rest captured to the inbox as listed.
