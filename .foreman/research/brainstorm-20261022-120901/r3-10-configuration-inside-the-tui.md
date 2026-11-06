# Brainstorm — lens: configuration inside the TUI

- **Generate the settings screen from a typed schema registry** — FEATURE — value 5 — effort L — risk med — category: settings
  Why: pack says "no settings screen inside the app: every setting is hand-edited TOML"; prior ideas mention schemas and in-TUI editing but not a single registry feeding screen, validation, docs, env overrides and `--print-config`.
  Done when: adding one entry to the registry makes a new setting appear in the screen, in `fm code config explain`, and in generated docs, with a test that fails if any of the three drifts.

- **Edit tui.toml and code.toml in place, preserving comments and order** — FIX — value 4 — effort M — risk med — category: persistence
  Why: stdlib has no TOML writer; naive rewrites would wipe a user's hand-written comments, and the pack says all settings are hand-edited today. Assumption: users keep comments in these files.
  Done when: a round-trip test toggles ten settings through the screen and the file diff touches only those lines.

- **Show a live "preview strip" of the real frame under each focused setting** — FEATURE — value 4 — effort M — risk low — category: preview
  Why: theme, layout and motion settings are visual; the TUI already has a theme/layout/motion engine, so the focused row can render a candidate in a thumbnail region without applying it.
  Done when: moving focus across three themes changes the strip's palette while the underlying config file mtime is unchanged.

- **Apply changes with a 10-second confirm-or-revert for anything that can blind the user** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: a theme with unreadable contrast or a keybinding remap could lock the user out of the screen that fixes it; assumption: this is not yet handled.
  Done when: a test applies a black-on-black theme, sends no key, and the previous config is restored after the timeout.

- **Make the settings screen reachable from a reserved, unremappable chord and from `?`** — FIX — value 4 — effort S — risk low — category: keys
  Why: keybinding editing can orphan the entry point; a hardcoded fallback chord guarantees a way back.
  Done when: with all user keys unbound in tui.toml, the reserved chord still opens settings and a reset-keys action.

- **Layer-aware scope picker with provenance chips on every row** — FEATURE — value 4 — effort M — risk low — category: layering
  Why: config is already described as global, project, env layers; each row should show which layer wins and let the save target be chosen. Assumption: layering lands as other ideas propose.
  Done when: a row overridden by an env var shows its source chip and is read-only until the override is named in the UI.

- **Runner editor with a "test this runner" button and keychain-referenced keys** — FEATURE — value 5 — effort M — risk med — category: runners
  Why: runners come only from the built-in registry and code.toml (constraint); editing them in-app needs a probe so a typo is caught before a run. Keys stored by reference, never written into the file.
  Done when: adding a runner with a bad binary path shows a failed probe result inline, and saved TOML contains no secret value.

- **Search-first settings palette ("type what you want to change")** — FEATURE — value 3 — effort S — risk low — category: discovery
  Why: with many settings, fuzzy search over names, descriptions and synonyms ("dim", "faster", "bigger text") beats navigation; reuses the planned command palette.
  Done when: typing "calm" lands on the reduced-motion row, verified by a synonym-table test.

- **Dry-run new config against a recorded event stream before saving** — FEATURE — value 3 — effort M — risk low — category: validation
  Why: the pack's TUI is a reader of an event log, so a candidate config can be rendered headlessly against a sample run and checked for crashes, overflow and contrast.
  Done when: a config that breaks layout at 60 columns is rejected with the failing frame shown.

- **Wild: Hold-to-tune dials with a live ghost of the old value** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; numeric settings (frame rate, animation speed, caps) become a dial you scrub while the real UI responds, with the previous value shown faintly for comparison, snapping back on Esc.
  Done when: scrubbing animation speed changes a running shimmer's period live and Esc restores the original.

- **Wild: Say it in words, get a config diff to approve** — FEATURE — value 4 — effort M — risk med — category: natural-language
  Why: wild; "make it calmer and cheaper" is turned by the configured runner into a proposed patch against the schema, validated, shown as a diff, never applied without a keypress, and limited to schema-known keys.
  Done when: a request produces a diff touching only registry keys, and an out-of-schema suggestion is dropped with a note.

- **Wild: Config time machine with named restore points** — FEATURE — value 3 — effort M — risk low — category: history
  Why: wild; every save writes a snapshot plus a one-line reason ("theme: dusk → paper"), browsable and restorable from the settings screen; builds on the last-good-copy idea but adds history and diffing.
  Done when: after five saves, restoring the second reproduces that file byte for byte.

- **Wild: Pasteable setup code for sharing a look and layout** — FEATURE — value 3 — effort S — risk med — category: sharing
  Why: wild; export theme, layout, keys and motion (never runners' secrets or commands) as a short code; import shows a diff and rejects any key outside the safe allowlist so a shared code cannot add a runner command.
  Done when: importing a code containing a runner entry is refused with the reason, while a theme-only code applies.

- **Warn when a setting is dead, shadowed or conflicting** — CLEAN — value 3 — effort S — risk low — category: lint
  Why: hand-edited TOML accumulates unknown keys and duplicate bindings; a linter pass on open surfaces them with a one-key fix.
  Done when: a file with a misspelled key and two actions on one chord lists both with line numbers.
