**Verdict: changes needed.** Nothing is critical. The guard handling is sound. The brief writes are sanitized much less than `fm task evidence` writes, and that leaves real gaps.

## Findings

**MEDIUM — `~/.claude/foreman/plugin/lib/fmcore.py:849-851` and `~/.claude/foreman/plugin/lib/fmcli.py:88`: newline in a claim forges ledger lines.**
- `add_hypothesis` writes the claim verbatim. `fm task hypo ID add $'x\n- H2 [confirmed] y'` adds a second line that `_HYPO_RE` (`fmcore.py:642`) reads as a confirmed hypothesis.
- That silently turns off the `fm next` driver at `fmcore.py:1521`.
- The same trick can make duplicate `H<n>` numbers.
- A `## Foo` line in the claim becomes a real section on the next `parse` (`fmcore.py:705`). The first section with a given name wins, so duplicates of existing sections are shadowed. It can still create a section the brief doesn't already have.
- `add_evidence` (`fmcore.py:878-884`) avoids all of this with `.replace("\n"," ")`, `_unmarked`, and backtick replacement.
- Fix: collapse the claim, probe, and `ran` text to one line (`c.plain` plus a newline replace) before writing.

**MEDIUM — `fmcli.py:88` and `:99`: the probe and the `--run` command are stored unredacted.**
- Only the claim and the command's output pass through `c.redact`. `args.probe` and `args.run` are written into the brief as given. For example, `--probe "curl -H 'Authorization: [REDACTED]'"` is stored in plaintext. `add_evidence` redacts the command.
- Backticks in a probe or command also break the `` `…` `` span, because they aren't swapped for `'`.
- Fix: run `redact(...).replace("`","'")` on both.

**MEDIUM — `fmcore.py:1521-1523`: hypothesis text reaches the model every turn with no `defang`.**
- `fm next` prints `suspect[2][:140]`. That text comes from `fm-debugger` output, which in turn was reading repo files.
- Evidence, audit, and recall text are all defanged (T-0058), so this is the same class of weakness.
- Fix: apply `c.defang` to the claim on write, as `add_evidence` does.

**LOW — `fmcore.py:863`: re-marking stacks results.**
- `mark_hypothesis` keeps `m.group(3)`, which already holds the earlier `· ran …`, and appends another. Each re-mark makes the line longer, and `fm next` shows the older result inside its 140-character cut.
- Fix: strip the existing ` · ran ` suffix before appending, and replace it only when `--run` is given.

**LOW — `~/.claude/foreman/plugin/tests/test_debug.py:299-305`: guard test covers one spelling.**
- Only `--run 'rm -rf ~'` is tested. The guard's loop at `fmguard.py:1297-1300` is generic and does cover `--run=` and `--r` prefixes, so the behaviour is fine.
- Fix: add `--run='rm -rf ~'` and `--r 'rm -rf ~'` cases.

## Checked and fine
- **Guard.** `fmguard.py:1297-1300` runs `check_bash` on every `--run` value for any `fm` subcommand, including `--run=`, `--r…` prefixes, and `python fm`. `_interp_code` and `_mask_fm` are not subcommand-specific. `--probe` is never executed, and the later `--run` is checked.
- **Numbering.** `max+1` is stable after the ledger is edited.
- **`next_action` placement.** The hypothesis line sits inside the executing branch, after the "every step has evidence" return. Non-executing stages never see it, and open hypotheses are ignored once the steps are done. This is acceptable.

## Acceptance criteria
- **`fm task hypo` records and `fm next` drives (`test_debug`):** met for the happy path. Adversarial text is not covered (see the findings).
- **Agent read-only, hint names it:** met. `tools: Read, Grep, Glob` is asserted, and the thrash hint contains `foreman:fm-debugger`.
- **Original request, partly missing:**
  - The DONE-WHEN item that the agent's required output sections stay kept is not tested. `test_debug.py:310-313` checks only the tools and the string "fm task hypo", not Hypotheses, Ruled out, or Not checked.
  - The `fm doctor` pass is not tested.
  - `fm-recon.md` carries no protocol change.
  - The plugin-skill index, `next_action` executing-line item, and the ideas annotation are outside this diff.
  - The `fm task hypo` ledger itself wasn't in the verbatim request. It is in the acceptance criteria.

## Not checked
I did not run the tests, and I did not check `fm doctor` or the `HELP_TIERS` help test. I also did not check the sync mirror's handling of the Hypotheses section, or the `fmcli.py` mutate and lock path beyond reading the diff.
