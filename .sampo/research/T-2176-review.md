**Verdict:** changes needed. Two tests depend on the machine they run on, and the installer reimplements a PATH-link helper that already exists. I could not run anything (read-only, no shell), so none of this was executed.

## lens: intent
- MEDIUM — plugin/tests/test_setup.py:233-245 — T-2174 asks for a task driven "through brief, evidence and finish", and AC2 says "finish". The test closes the task with `fm task done`, not `fm task finish`. The brief also asks for the guard and drive without CC hooks, and for gemini and opencode wiring. The diff tests none of these, and the installer test only wires a `codex` stub. — Close with `fm task finish`; add a gemini and an opencode stub to the installer test, or say that coverage lives elsewhere — high
- MEDIUM — plugin/tests/test_setup.py:247-252 — AC2 says "fm code finishes on a stub model". The new test only checks that `fm code` with no model fails with "no model". That is the opposite of finishing. Nothing in the diff shows `test_code` runs with `claude` off PATH. — Run one existing stub-model `fm code` test with the no-claude PATH, or reword the AC — medium
- LOW — site/index.html:111,119,290 — The site still says "What it holds Claude to", "Claude resumes at the exact step" and "ask Claude for something". These aren't product lines, but they are copy a harness-neutral reading would change. — Say "the agent" — medium
- LOW — install.sh:223 and INSTALL.md:15,46 — With no Claude Code, the installer's last line still says "start Claude Code in any repo". INSTALL.md step 5 still says to restart Claude Code. — Make the closing line depend on `$CLAUDE` — high

## lens: edge
- MEDIUM — install.sh:175 — `[ -e "$HOME/.local/bin/fm" ] || ln -s …` mishandles a dangling `fm` link. `-e` is false for it, `ln -s` fails with "File exists", and `set -e` aborts before any agent is wired. A working link to another program is left in place with no message. `fmsetup.ensure_fm_link` (plugin/lib/fmsetup.py:56) already handles both cases. The branch also drops that function's "add ~/.local/bin to your PATH" hint (fmsetup.py:179), so the AC's "links fm onto PATH" can come out false. — Call `python3 -c 'import fmsetup; …ensure_fm_link()'` instead, or use `ln -sfn` when the link is dangling, and print the PATH hint — high. Repro: `ln -s /gone ~/.local/bin/fm`, then run `install.sh` with no `claude` on PATH. It exits 1.
- LOW — install.sh:49 — Without Claude Code, `PLUGINS=0` silently drops pass-through flags such as `--security` and `--docs`. — Print a line saying they were ignored — medium

## lens: maintainer
- MEDIUM — plugin/tests/test_setup.py:197-201 — `test_without_any_agent_it_points_at_fm_code` builds its PATH from the real one (lines 173-176). On a machine with `codex`, `gemini` or `opencode` installed, the installer finds a real agent. It then never prints the "No coding agent found" line, and the test fails. — Skip `codex`, `gemini` and `opencode` when copying PATH entries — high
- MEDIUM — plugin/tests/test_setup.py:247-252 — `fm code` with no model is not hermetic. `fmcode.pick_runner` (fmcode.py:1677-1686) tries a local server first, then the first verified runner (codex or gemini) from the copied PATH. A running ollama or an installed `codex` makes the test start a real run instead of exiting "no model". — Drop agent CLIs from the copied PATH, and point the local-server probe at a closed port or stub it — medium
- LOW — plugin/tests/test_site_build.py:262 — `ProductLines` is defined after `if __name__ == "__main__": unittest.main()`. Running the file directly never runs it. — Move the class above the guard — high
- LOW — plugin/tests/test_site_build.py:267-275 — The test checks five exact phrases. It does not cover `plugin/.claude-plugin/plugin.json`, which T-2173 names. That file's description has no Claude Code claim, so it needs no edit. — Not worth a test

## lens: adversary, operator, design
ok. The installer takes no new untrusted input. Quoting is intact, and `ln -s` writes only inside `$HOME`. The default install path (Claude Code present) is unchanged. Marketplace.json and plugin.json need no version bump. The CHANGELOG entry follows the neighbouring bullets with no blank line. I found no cost-at-scale issues.

## Acceptance criteria
- install.sh with no `claude`: met in code. Exit 0, wires the agents it finds and skips the Claude Code steps. The `fm` link is created only under `WIRING=1` and has the dangling-link hole above.
- README, site home page, MASTER §1 and install requirements: met for the headline, title and requirements lines.
- fm works with no claude (init, task new, evidence, finish): partly. The test uses `task done`.
- `fm code` finishes on a stub model: not verifiable from this diff.

## Implicit decisions
- Detection is just `command -v claude`.
- The `fm` link needs wiring on, and `--no-wiring` skips it.
- A missing `claude` with `--build` is a hard error.
- The fine-print wording now says "Anthropic or any agent's maker".

## Not checked
Test execution, screenshots and rendered layout, and the full MASTER.md and README for other Claude Code–specific copy.

**Noticed:** none
