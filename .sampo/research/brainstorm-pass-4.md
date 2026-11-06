# Brainstorm pass 4 (2026-10-04) — grounded slate

Source: research/brainstorm-20261004-030846 (two lenses — reliability and trust in its own verdicts; user value — × 2 rounds, past passes 1–3; 42 new titles). A cheap probe per the brainstorm skill.

## Grounded and kept (the slate)
1. Guard reads `cd DIR && python3 - <<'EOF'` like a bare `python3 - <<'EOF'` — "teach the guard to read python heredocs as text edits". Reproduced with the exact command blocked this session (4× in fm friction): `_python_units` only treats a heredoc as fed to python when the line *starts* with `python`, so a `cd … &&` prefix sends the body to the text match, and an edit script whose strings hold `import fmcli` is blocked as driving Foreman's modules. The AST check already proves such scripts harmless when it gets to run. FIX S, value 4.
2. Tests can never reach the real `claude` — "lock out the real claude in test harnesses". helpers.py hands tests the full PATH; a stub that fails to exec (no shebang → ENOEXEC) falls through to the real binary, as it did in this session's scratch check ($0.42 of unasked sessions). A lockout `claude` placed right after the test's stub dirs fails loudly instead. FIX S, value 3.
3. Untrusted text followed to its sinks — "check taint at the sinks" (lazy form) + "trigger a security pass from what the diff touches". The adversary lens names untrusted sources but no sinks, and the pre-audit doesn't flag network/ingest code; this session's background security review found three issues (prompt, URL, terminal) the in-loop adversary pass graded low or missed. Add a source→sink checklist to the adversary lens and network/ingest markers to the pre-audit. SECURITY S, value 4.
4. Escapes attributed to the task that closed them — "attribute escapes back" + "score reviewer severity against what escapes later". A FIX/SECURITY request that names a done task (T-0281 named T-0278) logs an escape against it with the lenses that passed it; fm friction lists escapes. Gives reviews a measured recall over time. FEATURE S–M, value 3.

## Grounded and dropped
- Zero-test runs counted as passes — already handled (fmcore R3: exit 0 with no tests becomes exit 5).
- Park the reviewer and start the next task in a lane — merges into T-0234 (implementation subagents in lanes).
- Tainted string types across all sinks — invasive; the lens checklist is the lazy version (item 3).
- Claims half-life, planted defects in review diffs, verdict leases, confidence intervals — kept for later passes (value unclear, cost M–L).
- Show what you can stop worrying about / fold steers / rate a pass in one word — exist (while-you-were-away row, steer log, friction digest).

## Yield
4 grounded ideas of real value (≥ 3): not dry. Build as one batch, then probe pass 5.
