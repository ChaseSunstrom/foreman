**Verdict:** approve with nits. I found no defect in the probe, the hush write or the escaping. I could not run the tests (read-only), so every point below comes from reading the code.

## lens: edge / adversary (probe, hush, escaping, `z`)
- MEDIUM — mods/foreman-ui/hooks/kit.ts:27 — Under riso the pane's `accent` becomes #62A8E5 but `accent2` stays #87AFFF. That is about 1.16:1 contrast and 11° of hue apart, against 39° in the default palette. The app's RISO["night"] has a distinct `accent2` (#FFB511), so "the same inks" holds for only 3 of 4. Tool rows (Running is accent, Reading is accent2), FEATURE and CLEAN chips, and the now/queued counts blur together — add `accent2: 0xffb511` to `PALETTES.riso` (and to the Python/TS equality test, and `PALETTES.default`/`cb` can leave it unset) — high
- LOW — plugin/lib/fmcodetui.py:54 — riso `dim` #6A6252 on `bar` #E3DAC6 is 4.34:1, below the 4.5:1 body-text mark. It affects `bar_dim` (footer hints, "last heard"). The test only enforces the app's 3:1 floor (`_faint`). The paper theme has the same 4.3 ratio, so this follows precedent. Use #655D4E, which gives 4.68 on the bar and 5.6 on the paper — high
- LOW — plugin/lib/fmcodetui.py:1583 — `z` is dispatched before the help branch and after the settings branch. In help it hushes but the overlay stays open, though it says "any key closes". On the settings list (not typing) `z` does nothing, yet the comment says "every screen but where keys are typed". Either close help after a hush or reword the comment. Only main, home and prompt are tested — medium
- LOW — plugin/lib/fmcodetui.py:112 — `SPIN ="…"` is missing a space before `=` (E225) — fix the spacing — high

## lens: design
Riso is a distinct look: cream paper stock, fluorescent pink, green and cornflower. Contrast on the paper theme (bg #F2EDE1):

| Pair | Contrast |
|---|---|
| ink | 13.5:1 |
| said | 6.6:1 |
| ok | 4.75:1 |
| bad | 4.92:1 |
| warn | 5.6:1 (4.72 on bar) |
| accent | 5.5:1 |
| chip texts | 4.75–5.5:1 |

- The `track` and `edge` colours sit at about 1.4–1.6:1, the same as the paper theme (precedent). Night-ink riso on a dark background is 6.0–7.3:1.
- The pane's riso inks are for dark terminals only. On a white terminal accent is 2.5:1, as the default green already is.

## Key questions
- **Probe corruption and key handling:** it cannot corrupt the screen. It runs after cbreak and the alternate screen, and the first full frame repaints cell (1,1). Keys typed during the probe are kept in order and reach `flags["pending"]`. A reply that arrives late is skipped by the `parse_keys` CSI skip.
- **Hang and environments:** `select` bounds the probe to 0.25 s. It needs both ends to be a tty, so pipes and CI write nothing (tested). tmux and screen answer cursor-position queries. Unanswered, it costs one 0.25 s pause plus a visible ▀ at the top-left, and then the track stays flat.
- **Hush write:** it goes through `set_key`, so the guard (fail-closed outside a terminal) and `fmcore.lock` apply. `SettingError` and `LockTimeout` are caught, the screen still hushes, and the message says why.
- **Escaping:** `bad()` and the load-error path cover every `load_config` message. I found no other path that prints raw tui.toml text.
- **Golden frames:** only demo-03.4s changed, and only the spinner glyph (line 20 and the footer). At 3.4 s the old index 4 (⠼) becomes 7 (⠧) at the thinking tempo. That is intended.

## Acceptance criteria
- Hush cycles motion: met, by reading. The pane reads the same `motion` option through `applyOptions`.
- Riso loads in both the app and the pane: met.
- Spinner tempo follows state: met, by reading `agent_state` and `FX.spin`.
- `MotionVisuals` run: not verifiable here.

## Implicit decisions
- One keypress rewrites ~/.claude/settings.json, the whole file with `json.dumps`, plus tui.toml.
- Only ▀ is probed. The probe's total budget is 0.25 s.
- An extension asking for key `z` silently loses it (`setdefault`).
- Riso on the pane changes only ok, err and accent.
- 8-colour terminals may quantise the rail's fg and bg to the same colour.

## Not checked
Visual rendering, the `tsc` and bun runs, and the rail drawing on real terminals.

Noticed: CHANGELOG.md "Unreleased" has no T-1512 entry, though neighbouring features have one.
Noticed: plugin.json options gained "riso" with no version bump (0.18.3). If installed manifests are cached by version, `palette = "riso"` could be dropped.
