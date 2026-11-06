# README and website audit (T-3300), 2026-11-06

Seven read-only auditors, one per slice; each claim checked against code and live data. Findings below are verified
by the auditor; "fix" says where the fix goes (docs or code).

## WRONG
1. README.md:175 — install adds `~/.claude/rules/sampo.md`; actually `~/.claude/rules/foreman.md` (setup.py:36,49-50). Fix: docs.
2. README.md:138,176 — installer "puts sampo on your PATH"; `ensure_fm_link` (setup.py:57-75) links only `~/.local/bin/fm`; `sampo` isn't linked on a clean install. Fix: code (link `sampo` too), then docs.
3. README.md:249 + site/assets/diagrams/guard.svg — "Sampo's own code, remote, plugins/MCP, destructive categories come as Claude Code's permission prompt". Only core, remote, plugin, confirm are prompt-only (fmguard.USER_ONLY :84); destructive categories are granted per task by `sampo task set ID --allow CAT`; state-direct, self-authorize, confine, brief can never be granted. Fix: docs + SVG.
4. README.md:258 — young-package note "published in the last 30 days"; code is 14 (deps.YOUNG_DAYS). Fix: docs.
5. README.md:530 — `recall --export-rules` writes `.claude/rules/sampo-lessons/`; it writes `foreman-lessons/` (recall.py:1053). Fix: docs.
6. README.md:485 — mascot options "blue, orange, purple, green or off" with Claude in the corner; options are sampo|blue|orange|purple|green|off, default `sampo` = the crest (mods/foreman-ui plugin.json:22-35). Fix: docs.
7. README.md:502 — motion `calm`; the documented value is `reduced` (calm is an alias). Fix: docs.
8. README.md:526 — "(Rune' done gate)" stray apostrophe; mixes Rune and Genesis names. Fix: docs.
9. README.md:784 — local marketplace "sampo"; it is "foreman" (.claude-plugin/marketplace.json). Fix: docs.
10. README.md:81 vs site/assets/diagrams/loop.svg — "Guard checks every command"; current name is the Ward. Fix: SVG.
11. site/assets/diagrams/guard.svg — "fm oops brings it back"; teach `sampo oops`. Fix: SVG.
12. README.md:21 — anchor `#the-Ward` should be `#the-ward`. Fix: docs.
13. site/genesis — footer "Exported by sampo genesis export" and next "fm genesis sweep 4": teach `sampo rune ...`. Fix: rune.export strings (T-3266 is remaking the page).

## STALE
14. README.md:150 — "tested on 2.1.304"; installed Claude Code is 2.1.318; live.svg caption says 2.1.301. Fix: re-test, update.
15. README.md:474 — compact-at-close names only `freshAt`; `freshTokens` (default 200000) exists. Fix: docs.
16. site/genesis/genesis.json (2026-11-05T05:48Z) — unproven 810 vs live 855, per-kind counts drifted. Fix: re-export (rune.export) on each site build / night.

## MISSING
17. README observability — `sampo watch --web` live page (jobs, local models, GPU, flows; forge/modern toggle) barely mentioned. Fix: docs.
18. README Ward — `confine` and `brief` categories (brief is what new users hit first); scheduling (crontab/at/systemd-run/night --install) guarded as system. Fix: docs.
19. README layout block :775-789 — omits SAMPO.md, MOONSHOT.md, SEED_PROMPT.md, design/, docs/, bench/, research/, mods/, plugins/; Documentation table omits SAMPO.md etc. Fix: docs (decide which are public).
20. README Smith themes :653 — `classic`, `classic_paper` presets missing. Fix: docs.
21. Rune page — no Kalevala, underworld, steer/holdout results (T-3266 covers Kalevala).

## UNVERIFIED (to check in the fix pass)
- "~80 s" suite time (README:763); Smith page anchors exist only after a build; sandbox default domains; model-layer shadow/exam semantics; TUI card/tree rendering details; live-page sections vs README; mod version 2.1.299+.

Pending slices: README Features (286-439), site main page.

## Features slice (README 286-439)
22. WRONG README ~405 — "`sampo lane max N` lets up to six builders work at once": default 2, max 100 (lanes.py BUILDERS/BUILDERS_MAX, T-3297). Fix: docs.
23. WRONG README ~437 — hooks "about 20 ms here": the README's own data.json shows per-hook p95 35-89 ms (Bash script 248.6 ms). Fix: docs (say p50/p95 from data.json, or drop).
24. STALE README ~340 — "Over 1,000 stack cards in 29 areas": 1,227 now (still true; could say 1,200).
- UNVERIFIED: "twenty named looks"; only Ward + write validators synchronous; Moons "100 ideas on six tiers".

## Site main page
25. WRONG site/index.html:412-413 — moonshot chart caption "twenty wildest of 58" is hardcoded; data says 61 (and the generated heading says 61). Fix: fill from genesis.json in build.py.
26. STALE site/index.html:374,454 and build-inserted counts — stats.json from 2026-11-02 (cards 1,219 vs 1,227; tests 5,686 vs ~6,800; tasks, lanes, gates). Fix: rerun site/stats.py on each build/night; footer date follows.
27. STALE _site/ built 2026-11-01, older than site/ sources. Fix: rebuild and publish with the fixes.
