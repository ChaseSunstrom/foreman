# Crest shots (T-3113)

Taken 2026-11-05 after the merge, with mods/foreman-ui/tools/shot.py: Claude Code 2.1.318 in a tmux harness with the merged mod, in a scratch folder. Images: ~/.claude/foreman/state/projects/foreman-4a056f/research/crest-shots/idle-200.png and ~/.claude/foreman/state/projects/foreman-4a056f/research/crest-shots/narrow-150.png; the working frame is /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/crest-f2.png (scratchpad). The runes render in Konsole through Noto Sans Runic; shot.py now falls back to it too.

## Idle, 200 columns: the ring dim, the mark lit
```
 │                                                                                       ✕
 │ ᚠ·ᚢ·ᚦ·ᚨ·ᚱ·ᚲ·ᚷ·ᚹ·ᚺ·ᚾ·ᛁ·ᛃ·ᛇ·ᛈ·ᛉ·ᛊ·ᛏ·ᛒ·ᛖ·ᛗ·ᛚ·ᛜ·ᛞ·ᛟ·ᚠ·ᚢ·ᚦ·ᚨ·ᚱ·ᚲ·ᚷ·ᚹ·ᚺ·ᚾ·ᛁ·ᛃ·ᛇ·ᛈ·ᛉ·ᛊ·ᛏ·ᛒ·ᛖ·ᛗ
 │ ᚨ                                         ▄▀                                          ᛚ
 │ ᚦ                                        ▀▀▀▀                                         ᛜ
 │ ᚢ                                       ▀▀▀▀▀▀▄                                       ᛞ
 │ ᚠ                                      ▄▄▄▀▀▄▄▄                                       ᛟ
 │ ᛟ                                     ▀▀▀▀▀▀▀▀▀▄                                      ᚠ
 │ ᛞ                                     ▀▀▀▀▀▀▀▀▀▀                                      ᚢ
 │ ᛜ·ᛚ·ᛗ·ᛖ·ᛒ·ᛏ·ᛊ·ᛉ·ᛈ·ᛇ·ᛃ·ᛁ·ᚾ·ᚺ·ᚹ·ᚷ·ᚲ·ᚱ·ᚨ·ᚦ·ᚢ·ᚠ·ᛟ·ᛞ·ᛜ·ᛚ·ᛗ·ᛖ·ᛒ·ᛏ·ᛊ·ᛉ·ᛈ·ᛇ·ᛃ·ᛁ·ᚾ·ᚺ·ᚹ·ᚷ·ᚲ·ᚱ·ᚨ·ᚦ
 │ ⊖ Sampo  crest-demo-015ca9   standard   trust on
```

## Working, three subagents: a hammer each in its own colour (yellow, green, pink), one striking with sparks; the top ring lighting in turn
```
 │                                                                                       ✕
 │ ᚠ·ᚢ·ᚦ·ᚨ·ᚱ·ᚲ·ᚷ·ᚹ·ᚺ·ᚾ·ᛁ·ᛃ·ᛇ·ᛈ·ᛉ·ᛊ·ᛏ·ᛒ·ᛖ·ᛗ·ᛚ·ᛜ·ᛞ·ᛟ·ᚠ·ᚢ·ᚦ·ᚨ·ᚱ·ᚲ·ᚷ·ᚹ·ᚺ·ᚾ·ᛁ·ᛃ·ᛇ·ᛈ·ᛉ·ᛊ·ᛏ·ᛒ·ᛖ·ᛗ
 │ ᚨ                                         ▄▀                                          ᛚ
 │ ᚦ                                        ▀▀▀▀                                         ᛜ
 │ ᚢ                                       ▀▀▀▀▀▀▄                                       ᛞ
 │ ᚠ                              ▄███▄   ▄▄▄▀▀▄▄▄   ▄███▄ · * ·                         ᛟ
 │ ᛟ                                █    ▀▀▀▀▀▀▀▀▀▄    █   ▄███▄                         ᚠ
 │ ᛞ                              ▃▃▃▃▃  ▀▀▀▀▀▀▀▀▀▀  ▃▃▃▃▃ ▃▃▃▃▃                         ᚢ
 │ ᛜ·ᛚ·ᛗ·ᛖ·ᛒ·ᛏ·ᛊ·ᛉ·ᛈ·ᛇ·ᛃ·ᛁ·ᚾ·ᚺ·ᚹ·ᚷ·ᚲ·ᚱ·ᚨ·ᚦ·ᚢ·ᚠ·ᛟ·ᛞ·ᛜ·ᛚ·ᛗ·ᛖ·ᛒ·ᛏ·ᛊ·ᛉ·ᛈ·ᛇ·ᛃ·ᛁ·ᚾ·ᚺ·ᚹ·ᚷ·ᚲ·ᚱ·ᚨ·ᚦ
 │ ⊖ Sampo  crest-demo-015ca9   standard   trust on
```

## Narrow, 150 columns (the pane about 66 wide): the full crest still fits; the compact 3-row mark under 60 columns is covered by the mod tests, since the pane doesn't seat unasked below 144 columns
```
│                                                                ✕
│ ᚠ·ᚢ·ᚦ·ᚨ·ᚱ·ᚲ·ᚷ·ᚹ·ᚺ·ᚾ·ᛁ·ᛃ·ᛇ·ᛈ·ᛉ·ᛊ·ᛏ·ᛒ·ᛖ·ᛗ·ᛚ·ᛜ·ᛞ·ᛟ·ᚠ·ᚢ·ᚦ·ᚨ·ᚱ·ᚲ·ᚷ·ᚹ·
│ ᚨ                              ▄▀                              ᚺ
│ ᚦ                             ▀▀▀▀                             ᚾ
│ ᚢ                            ▀▀▀▀▀▀▄                           ᛁ
│ ᚠ                           ▄▄▄▀▀▄▄▄                           ᛃ
│ ᛟ                          ▀▀▀▀▀▀▀▀▀▄                          ᛇ
│ ᛞ                          ▀▀▀▀▀▀▀▀▀▀                          ᛈ
│ ᛜ·ᛚ·ᛗ·ᛖ·ᛒ·ᛏ·ᛊ·ᛉ·ᛈ·ᛇ·ᛃ·ᛁ·ᚾ·ᚺ·ᚹ·ᚷ·ᚲ·ᚱ·ᚨ·ᚦ·ᚢ·ᚠ·ᛟ·ᛞ·ᛜ·ᛚ·ᛗ·ᛖ·ᛒ·ᛏ·ᛊ·ᛉ·
│ ⊖ Sampo  crest-demo-015ca9   standard   trust on
```

## Seen
- The mark reads muddy at half-block resolution (grey noise at its base): T-3210 redraws it crisp.
