# Audits (reference)

Before a task is done, independent audits look at the finished change through different lenses, each with its own
prompt and a deliberately different slice of context, so no single framing (least of all the implementer's) decides
what counts as correct. `fm task done` refuses until the tier's audits are recorded after the last change.

| Tier | Required (recorded after the last step evidence and the last file edit) |
|---|---|
| S | `self`: run the checklist below yourself, all five lenses, in the main thread |
| M | `intent` + one of `adversary` / `edge` / `operator` / `maintainer` (pick the riskiest), via `foreman:fm-reviewer` |
| L | all five: `intent`, `adversary`, `edge`, `operator`, `maintainer`, in one `foreman:fm-reviewer` pass |

## Protocol
1. **Freeze the change.** All steps done with evidence, tests green (`fm check`). `fm audit prep ID` saves the diff since the task was focused (untracked files included) and prints step 2's briefs, each with this project's past findings for its lens (so save reviews as `<task>-<lens>`).
2. **Build the review brief** from the templates below (`fm audit prep ID` does this): one section per lens, each with its prompt and context slice and nothing else. Leave out your plan, rationale and conversation; the point is a fresh view.
3. **Run** it as one `foreman:fm-reviewer` subagent (read-only) whose prompt just points at the brief file `fm audit prep` wrote (`audits/ID.review.md`); it reads the diff once and reports per lens. Save the reply with `fm research add ID-review --from-agent <its output file>`. For a big or risky L change, `fm audit prep ID --split` writes up to three briefs (adversary+edge, intent+operator, maintainer): run one reviewer per brief in parallel, each with a fresh context, and save each reply. When a finding is disputed or costly to fix, `fm second debate ID --review <saved review>` writes a rebuttal brief: a second reviewer confirms or refutes each finding from the code, and only CONFIRMED findings count. `fm audit prep` also names installed review skills that fit a lens (e.g. a security-review skill for adversary); one run on the diff counts as that lens: `fm task audit ID <lens> "/skill" "<result>"`.
4. **Verify every finding yourself**: reproduce it (run the input, read the line, write the failing test). Auditors can be wrong; unverified findings are neither fixed nor dismissed silently.
5. **Resolve**: real finding in scope → fix it test-first (regression test), re-run the full suite. Real but out of scope → `fm capture --source discovered`. False positive → say why in one line.
6. **Record** each lens: `fm task audit ID <lens> "<how: agent/lens/diff>" "<N findings: F fixed (tests), C captured (ids), X false positive>"`.
7. If a fix changed code after an audit, re-run that lens (fm rejects audits older than the last edit).

8. **Implicit decisions** (T-0637): every lens also lists the defaults the change took without saying so — a library, a name, a schema or file format, a behaviour at the edges — one line each, so a default the user would have chosen differently is visible; real ones go in the brief's Log or `fm decide`.

## Lens templates (paste into the fm-reviewer brief)

**intent** — context: the user's raw request(s) verbatim, the acceptance criteria, the diff. Nothing else.
> You are checking whether this change does what the user asked. Read the request as the user meant it, not as the implementer interpreted it. Report: anything asked for that is missing or only partly done; anything done that the user didn't ask for and wouldn't expect; acceptance criteria that don't actually capture the request, or that check an internal state instead of the observable the user will see; places where the user would be surprised by the result (defaults, naming, behaviour changes).

**adversary** — context: the diff, the threat model (what must never happen: guard bypass, self-authorization, credential exposure, data loss, running untrusted content), the files the diff calls into.
> You are trying to break or get around this change. Look for alternate spellings and abbreviations of flags, encodings, quoting and shell tricks, environment variables that change behaviour, path tricks (symlinks, `..`, case), races and TOCTOU, input from untrusted places (pasted text, files, web), failure modes that fail open. Follow each untrusted input (a web page, a registry's answer, a cloned repo's files, another model's or session's output) to every sink it reaches: the terminal (escape sequences), a model prompt (instructions, fake fences), a URL or network request (scheme, private addresses, redirects), a shell or interpreter, a file path, git config or hooks. Give the exact input that breaks it.

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
