# Brainstorm — lens: deepen: install

- **Record every install change in a reversible journal** — FEATURE — value 5 — effort M — risk med — category: install
  Why: uninstall leaves residue and prints "defaultMode = None"; the install ideas about resuming, byte-identical uninstall and remembering reversals all need the same record of what was changed.
  Done when: in a clean HOME, install, then interrupt, then re-run: it resumes at the failed step. After `uninstall`, a hash of `~/.claude` equals the pre-install snapshot.

- **Ship three named postures (Observe, Guide, Enforce) instead of 20 settings** — FEATURE — value 5 — effort M — risk med — category: install
  Why: the default sets bypassPermissions, outputStyle, autocompact 70%, a statusline wrapper and 20 deny rules, which is a large trust ask. Bypass belongs only in Enforce. Observe changes nothing outside the plugin.
  Done when: `fm posture` shows the active posture and its exact settings list. The default install leaves `permissions.defaultMode` untouched and `fm posture enforce` applies it.

- **List the exact changes before applying them (`install.sh --plan`)** — FEATURE — value 4 — effort S — risk low — category: install
  Why: the output says only "Claude Code asks you to confirm once". Print a unified diff of every file the install will touch, then ask. `--yes` skips the prompt.
  Done when: `--plan` writes nothing and prints a diff that matches byte-for-byte what a real run later changes.

- **Make `fm` work in every shell and pass doctor on a fresh install** — FIX — value 5 — effort S — risk low — category: install
  Why: new-user evidence A3 and A8: "command not found" outside Claude sessions, and a fresh install fails its own `fm doctor` for a missing backup. Install a `~/.local/bin/fm` shim that pins the interpreter, and take the first backup at install time.
  Done when: in a clean HOME, `bash -lc 'fm doctor'` exits 0 straight after install, with the summary line first and passing checks collapsed.

- **Gate releases on a clean-HOME install test** — CLEAN — value 4 — effort M — risk low — category: install
  Why: the newcomer problems were found by hand on a fresh install and nothing prevents them from coming back. Run install, doctor, `fm init`, task finish and uninstall in a throwaway HOME, with no model calls, as part of the roundtrip gate.
  Done when: `roundtrip.py` includes the clean-HOME scenario and fails if doctor, PATH or uninstall residue regresses.

- **Publish a marketplace plugin with zero wiring and an `fm wire` ladder** — FEATURE — value 5 — effort L — risk med — category: install
  Why: every rival installs with one marketplace command and adds commands without rewriting `~/.claude`. Make the marketplace install the default, and make each current `~/.claude` change an opt-in `fm wire <step>` with `fm wire --list` and `fm unwire`.
  Done when: `/plugin install` in a clean HOME gives working skills and hooks with `~/.claude/settings.json` unchanged. `fm wire statusline` adds only that step, and `fm unwire statusline` undoes it.

- **Chain the user's statusline and output style instead of replacing them** — FIX — value 4 — effort S — risk low — category: install
  Why: the install replaces the statusline with a wrapper. Instead, store the user's original command, run it, and append Foreman's segment. If the user already has an output style, offer one rather than overwrite it.
  Done when: with a custom statusline installed first, its output still appears unchanged after install and Foreman's segment follows it.

- **Keep a decision ledger that updates never override** — FEATURE — value 4 — effort S — risk low — category: install
  Why: the existing "remember reversals" and "keep settings the user chose" ideas are one mechanism. Store each user's accept, decline or reversal per wire step, and make an update propose only new steps.
  Done when: after a user removes a deny rule, a later `update` does not re-add it and lists it as "skipped (you declined)".

- **Walk a newcomer through a 60-second `fm tour` in a scratch repo** — FEATURE — value 4 — effort M — risk low — category: install
  Why: A1, A5, A6 and A9: the README opens abstractly, `fm init` prints only a slug, and `task finish` is buried. The tour makes a temp repo, detects pytest or unittest, runs one task end to end, and shows the before and after. Reuse `fm check` detection to offer the gate.
  Done when: `fm tour` finishes in a temp repo with one recorded task and prints the three commands to use next. Running it leaves the user's repos untouched.

- **Wild: Add a `foreman` launcher that applies discipline through `--settings`** — FEATURE — value 4 — effort M — risk med — category: install
  Why: the discipline is active only when the user types `foreman` instead of `claude`, so `~/.claude` stays untouched and uninstall is `rm`. `foreman --posture strict` picks a posture per session. Assumption: Claude Code's `--settings` can carry hooks, permissions and the statusline.
  Done when: `foreman` starts a session with hooks and deny rules active, and plain `claude` in the same shell has none of them.

- **Wild: Rehearse an install in a throwaway HOME before touching the real one** — FEATURE — value 3 — effort M — risk low — category: install
  Why: this combines `--plan` with the clean-HOME gate. `install.sh --rehearse` runs the whole install and doctor in a temp HOME, then shows the diff and the doctor result against the user's real settings.
  Done when: the rehearsal reports the doctor result and a settings diff, and the real `~/.claude` hash is unchanged afterwards.

- **Wild: Install by conversation, so the first session asks three questions** — FEATURE — value 4 — effort M — risk med — category: install
  Why: the "agent-readable INSTALL.md" and "named postures" ideas meet here. The user pastes "install Foreman from <url>" and Claude reads INSTALL.md, asks how much trust to grant, how much Foreman may change, and whether the project is private. It then runs `fm wire` with the matching posture and finishes with doctor.
  Done when: in a clean HOME, an agent given only INSTALL.md reaches a passing `fm doctor` and records the user's answers in the decision ledger.

- **Wild: Let trust grants expire (bypass for 7 days, renewed by `fm trust`)** — SECURITY — value 3 — effort M — risk med — category: install
  Why: bypass is the largest trust ask. If it lapses back to the user's prior mode unless renewed, saying yes costs little. Doctor shows the days remaining. Assumption: SessionStart can reset `defaultMode` safely.
  Done when: with bypass granted and the clock moved 8 days ahead, the next session starts in the prior mode and prints one line saying how to renew.

- **Pin an isolated Python so Foreman never shadows the system `python3`** — FIX — value 3 — effort S — risk low — category: install
  Why: the installer puts `python3` in `~/.local/bin` when Python is older than 3.12.7 or missing, which can break other tools. Create a private venv or uv-managed interpreter under the Foreman directory and have the `fm` shim call it by absolute path.
  Done when: after install on a machine with an old system Python, `python3 --version` outside Foreman is unchanged and `fm doctor` passes.
