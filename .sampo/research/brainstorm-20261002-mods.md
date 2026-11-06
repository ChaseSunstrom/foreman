# Brainstorm 2026-10-02 — mods UI + smarter (T-0082), grounded and scored
Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.

## Slate (briefed)
1. fm ui --json view model (one snapshot for every surface; folds T-0076 steps/criteria/depends) — user value/simplicity — 5 · M · low. Grounded: fm state/queue/next --json exist separately, show --json lacks steps/criteria.
2. Foreman UI mod (Pane dashboard, AbovePrompt band, toasts, /fm, approve/next/drive/inbox buttons) — all lenses — 5 · L · med. Grounded: CC 2.1.287 mods API (Pane/AbovePrompt/Button/$.process.run/$.clock.every/$.prompt.submit); fm watch gather() is the data model to reuse.
3. --section aliases + keep criterion ticks (T-0080, T-0075) — reliability — 4 · S · low. Grounded: Brief.set_section matches exact heading; hit live this session.
4. One-call planning: fm task new --interpretation/--approach — simplicity — 4 · S · low. Grounded: fm task new has --ac/--step only.
5. T-0074 sensitive() regex-literal false positives — 3 · S · low.
6. T-0081 fm check timeout message — 3 · S · low.

## Dropped (grounding)
- In-process tool.call gates/guard in the mod: duplicates fmguard logic in TS (two sources of truth); classic hooks still needed for claude -p.
- prompt.compose "Next:" injection: a per-turn system-prompt change busts the prompt cache for the whole conversation.
- Delete fm watch / state.line / badge.txt: still needed headless and where mods are off.
- Haiku classifier, fork verifier, self-tuning gates: extra model cost; main model classifies, fm-reviewer audits.
- Writer lock, atomic writes, schema stamp: exist (fmcore.lock flock, os.replace, meta schema).
- Learned estimates: exists (fmrecall "similar finished tasks took N–M steps").
- $.prompt.submit drive watchdog: Stop-hook drive already continues; unattended submits risk runaway — a Next button instead.
- Mod/classic parity harness: mod is a pure renderer; a contract test on fm ui --json covers it.
- Raster sparklines, time-travel replay, inline diff review, stage cap, fm help tiers, inbox clustering: low value for effort.

## Follow-ups (inbox)
- Rules diet: drop always-on rule lines a gate already enforces.
- Bash-edit attribution via git snapshot around Bash calls.
- Hook failure circuit breaker with a visible degraded mode (band shows hook errors meanwhile).
