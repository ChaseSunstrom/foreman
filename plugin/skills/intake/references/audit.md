# Audits (reference)

Before a task is done, independent audits look at the finished change through different lenses, each with its own
prompt and a deliberately different slice of context, so no single framing (least of all the implementer's) decides
what counts as correct. `fm task done` refuses until the tier's audits are recorded after the last change.

| Tier | Required (recorded after the last step evidence and the last file edit) |
|---|---|
| S | `self`: run the checklist below yourself, all five lenses, in the main thread |
| M | `intent` + one of `adversary` / `edge` / `operator` / `maintainer` (pick the riskiest), via `foreman:fm-reviewer` |
| L | all five: `intent`, `adversary`, `edge`, `operator`, `maintainer`, via `foreman:fm-reviewer` (≤ 3 in parallel) |

## Protocol
1. **Freeze the change.** All steps done with evidence, tests green (`fm check`). `fm audit prep ID` saves the diff since the task was focused (untracked files included) and prints step 2's briefs.
2. **Build each lens brief** from the template below (`fm audit prep ID` does this): the lens prompt, its context slice and nothing else. Leave out your plan, rationale and conversation; the point is a fresh view.
3. **Run** each lens as a separate `foreman:fm-reviewer` subagent (read-only). ≤ 3 at a time.
4. **Verify every finding yourself**: reproduce it (run the input, read the line, write the failing test). Auditors can be wrong; unverified findings are neither fixed nor dismissed silently.
5. **Resolve**: real finding in scope → fix it test-first (regression test), re-run the full suite. Real but out of scope → `fm capture --source discovered`. False positive → say why in one line.
6. **Record** each lens: `fm task audit ID <lens> "<how: agent/lens/diff>" "<N findings: F fixed (tests), C captured (ids), X false positive>"`.
7. If a fix changed code after an audit, re-run that lens (fm rejects audits older than the last edit).

## Lens templates (paste into the fm-reviewer brief)

**intent** — context: the user's raw request(s) verbatim, the acceptance criteria, the diff. Nothing else.
> You are checking whether this change does what the user asked. Read the request as the user meant it, not as the implementer interpreted it. Report: anything asked for that is missing or only partly done; anything done that the user didn't ask for and wouldn't expect; acceptance criteria that don't actually capture the request; places where the user would be surprised by the result (defaults, naming, behaviour changes).

**adversary** — context: the diff, the threat model (what must never happen: guard bypass, self-authorization, credential exposure, data loss, running untrusted content), the files the diff calls into.
> You are trying to break or get around this change. Look for alternate spellings and abbreviations of flags, encodings, quoting and shell tricks, environment variables that change behaviour, path tricks (symlinks, `..`, case), races and TOCTOU, input from untrusted places (pasted text, files, web), failure modes that fail open. Give the exact input that breaks it.

**edge** — context: the diff and this environment matrix: no TTY / CI / piped install; missing tools (jq, git, gh, node, a given python); empty, corrupt or concurrent state; two sessions at once; resumed or compacted sessions; non-default git branch or detached HEAD; different HOME / XDG dirs; slow or no network; large inputs; clock and timezone.
> For each environment above that the change touches, say what happens. Report only cases where the behaviour is wrong or unclear, with the path:line that decides it.

**operator** — context: the diff, the install/uninstall/setup scripts it touches, the docs it touches (README, MASTER.md, CHANGELOG), the user's machine facts (enabled plugins, settings changes, git branch and remote).
> You run this on a real machine. Check: install and uninstall still round-trip; defaults are what the docs say; always-on context and startup cost don't grow unnoticed; nothing is installed, enabled or disabled that the user didn't approve; git operations land on the intended branch; versions, file maps and docs match the code.

**maintainer** — context: the diff, the neighbouring code it should match, the tests it adds or changes.
> You will own this code next year. Check: every behaviour change has a test that fails without it; tests assert behaviour, not mocks; no duplication of an existing helper; no dead code or speculative options; naming and error handling match the surroundings; the simplest adequate design was used.

**self** (S tier, main thread) — answer each in one line before `fm task audit ID self …`:
intent: does it do exactly what was asked? · adversary: what input or spelling gets around it? · edge: no TTY, resumed session, missing tool, corrupt state? · operator: branch, install/uninstall, docs, defaults? · maintainer: test that fails without the change, no duplication?

## Session audit (FINAL VERIFY)
When the queue empties, run `operator` and `adversary` over the whole session's diff (`git diff <session base>..HEAD`), because cross-task problems (a branch changed underneath you, docs that drifted over several tasks) are invisible per task. Record with `fm log final_audit '{"lenses":"operator,adversary","result":"…"}'`.
