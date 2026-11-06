## adversary: changes needed

**Verdict**

The plain routes are closed. `fm trust on` without the marker is refused by `fm`, and `fm trust on` with the marker is caught by the guard. I found one cheap route that contradicts the documented guard behaviour. It is shorter than a script file and needs only a single Bash call. I read the code and did not run it.

**Findings**

1. **MEDIUM-HIGH** — `plugin/lib/fmguard.py:479` and `:538`. Both checks match literal text, so a quoted or substituted spelling passes both.
   - The marker check is a raw substring test on the unparsed command: `"FOREMAN_TRUST_FROM" in cmd`.
   - The `trust` check needs the first token after `trust` to equal `"on"` (`rest[:1] == ["on"]`), where `rest` comes from `_fm_subcommand`.
   - Scenario: `env FOREMAN_TRUST_""FROM=foreman-ui fm trust "$(echo on)"`.
     - The shell strips the empty quotes, so `env` passes `FOREMAN_TRUST_FROM=foreman-ui` to `fm`. The raw text never contains the contiguous marker name.
     - The first token after `trust` is `$(echo on)`, not `on`, so line 538 does not fire.
     - Line 495 recurses into the substitution but only looks for dangerous writes, and `echo on` has none.
     - `cmd_trust` (`fmcli.py:846`) sees the marker and `args.state == "on"`, and turns trust on (`:854`).
   - Variants that need no quoting trick: `V=on; fm trust $V`, or `fm trust -- on`. These beat line 538 only. They still need the marker, which the quote-split above hides.
   - The docs call a script file the accepted ceiling, but this is one inline command. It contradicts the statement at `fmcli.py:842-843` that the guard refuses any agent command that names the variable or runs `fm trust on`.
   - Fix:
     - Test the marker against dequoted tokens, and for `env` and `VAR=` arguments the part before `=` after dequoting. Fail closed on any token containing `FOREMAN_TRUST` that cannot be resolved statically.
     - For `sub == "trust"`, block unless `rest` is empty or exactly `["off"]`, so any variable, substitution or `--` form is refused.
     - Optionally refuse `fm trust` when the command contains `$(`, a backtick or `$`.
   - Confidence: medium. The tokenizer's dequoting is the part I did not execute.

**Checked and found sound**

- **Mod origin check** (`mods/foreman-ui/hooks/register.tsx:487-489`): only `composer` and `bridge` origins are accepted. `bridge` implies Remote Control, which `fm serve` already guards (`fmguard.py:540`). Whether a `claude -p "/fm-trust on"` subprocess would get a `composer` origin depends on the Claude Code host, so I could not verify it from the code. `_check_claude_config` only looks at the command text, and a slash command inside a prompt is not a tool call. Worth one manual test.
- **`--allow` abbreviation**: argparse abbreviation is off (`fmcli.py:1385`), so `fm --proj … trust on` does not misparse the subcommand.
- **Trust coverage** (`fmguard.py:188-194`): `_trust_covers` excludes `<foreman_home>/state`, `ctx.state_dir`, the fallbacks and tree writes. I found no route from `trust on` to writing meta, so the agent cannot set `meta["trust"]` directly. Because `FOREMAN_STATE` is covered through `ctx.state_dir`, an override does not leak.
- **Trust scope**: trust only waives `core`. The `plugin`, `remote` and `self-authorize` categories still block (`fmguard.py:57-59`).
- **Trust is not a way to turn itself on**: with trust already on, the agent can edit `fmcli.py`. That is by design, since the user turned it on.

**Acceptance criteria**

- "Agent can't turn trust on": not met for the quoted or substituted spelling above. The plain forms are met.
- The mod criterion (typed `/fm-trust` runs `fm trust on` with the marker, a scheduled one is refused): met by the code at `register.tsx:487-494`. I did not run `claude plugin test`.

**Not checked**

- I did not run the test suite.
- I did not read the tokenizer (`_tokens`, `_strip_wrappers`) in detail, so the dequoting claim in finding 1 is unconfirmed.
- I did not review the intent, edge, operator or maintainer lenses.
