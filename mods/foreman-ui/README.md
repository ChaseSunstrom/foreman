# foreman-ui

Foreman inside Claude Code: the docked pane, the band above the prompt, toasts and one-press actions. Tests:
`claude plugin test mods/foreman-ui`.

- `tools/pane_replay.py render|twin FIXTURE` (T-1534): the pane drawn from a recorded `fm ui --json` view with no live
  session, through this mod's test kit; `twin` diffs two runs (`--matrix`: a third in another time zone and locale).
  Synthetic fixtures only in `tests/fixtures/`.
- `tools/shot.py` (T-0131): Claude Code with this mod in a tmux harness of its own, the screen as a PNG.
