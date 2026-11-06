# Board slate (T-0932, 2026-10-15): every open cluster, grounded by six fm-recon passes

## Building: ten batch briefs, one builder lane each
- T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- T-0955 fm run and night: resilience (crash-loop quarantine), r4-away-queue (systemd-inhibit), cloud-scheduling (night --print-timer)
- T-0956 Closing: r2-close-warning-quality (verdict line), close-out (Landed line), r2-diff-and-release-gates (leftovers scan)
- T-0957 Hooks: r2-session-liveness (idle_stop), plan-mode (permission_mode plan), intake + misc #272 (prompt log with permission mode), r4-digest-unify (what's new after upgrade)
- T-0958 Knowledge out: lessons-native (.claude/rules export), round5-skip #38 (ADR export), r2-deferral-triggers (defer until a file changes)
- T-0959 Brainstorm and cost: r2-child-salvage, r2-brainstorm-pack (manifest), r2-prompt-cache (bust causes), round6-later #27 (friction minutes), simplicity (burden --by-verb)
- T-0960 New verbs: r4-data-safety (fm oops), r2-round-loop-automation (fm round close), r2-cli-ergonomics (fm show), r4-newcomer-gates (fm release-check), r2-sensitive-and-redaction (sensitive suggest), r4-published-metrics (outcomes --readme)
- T-0961 Lanes and internals: r2-state-integrity (pre-merge base), r4-internals-simplify (one _git)
- T-0962 Surfaces: terminal-polish (NO_COLOR, step N/M), ui-later #13 (fm ui --demo), r2-board-ticking (page --picks), r4-team-share (sync join line), r4-editor-ui-surfaces (tmux line), lsp (diagnostics after edit)
- T-0963 Postures and rivals: r4-postures-lite, r2-compact-output-rollout (shadow), r2-verify-command-hygiene, r4-bench-vs-plain (--vs none), lanes-fleet (hollow returns)

## Built this session from the same push
- Stack library (T-0933, T-0941, T-0945), enforcement (T-0947, T-0948, T-0949 building), pane (T-0938, T-0939), guard friction (T-0940), Claude Code 2.1.301 (T-0944), MCP (T-0946 building), fm scout (T-0950 planned: Foreman finds its own work)

## Done already (grounding found them shipped)
- r2-attention-channels (OSC 777, push ask, sessionTitle, fm notify); r4-newcomer-gates CI half (.github/workflows/test.yml exists); r2-compact-spill-store size cap (T-0824)

## Blocked (needs something only the user or another machine has)
- r4-forge-issue-sync outbound: posting to GitHub needs gh auth and a person to approve posts
- r2-install-and-platform: launchd and macOS paths need a Mac to verify
- named-workflows: the workflow file format needs a live Claude Code check before shipping one
- r4-rival-coexist Taskmaster import: needs a real tasks.json to confirm the format

## Skipped, with why
- main-worktree, r4-reversible-install: lanes, fm task revert and uninstall-user already cover them
- r2-exports-and-policy, r2-agent-role-table, r2-misc, r4-i18n-voice, shared-docs: no failing case or request; two sources of truth for docs
- r2-resource-footprint drill, r2-round-scorecard, r2-round-user-summary: covered by doctor's state-size check, fm digest and the close's "Nothing needed" line
- native-verify (a model call on every Stop), r2-token-ledger and r4-memory-knowledge (M with no failing case), r4-keep-or-leave (a nag with nothing to measure yet), r4-tour-learn (fm demo plus bare fm cover it)
- round5/6/7/8 later and skip grab-bags: the value-3 slices are in the batches above; the rest keep their earlier skip reasons
