# Brainstorm — lens: user value

Most of the remaining space is marginal. After ~275 ideas, the core loop, token cost, safety and trust are well covered. These five are the only ones I'd call new, and only the first is a clear win.

- **Retune ceremony when the model changes** — PERFORMANCE — value 4 — effort M — risk med
  Why: assumption: transcripts record the model ID. Gates and rules were tuned on older models, and gate-yield, `fm whatif` and evals exist but nothing re-runs them when the model changes. The user is token-sensitive, so ceremony a stronger model no longer needs is pure waste.
  Done when: after a recorded model-ID change, `fm doctor` queues one ablation run over the recorded traces. It lists gates and notes that caught nothing under the new model and proposes an advisory demotion behind one yes/no.

- **Show what Foreman has learned about the user, with one-tap forget** — FEATURE — value 3 — effort S — risk low
  Why: Foreman now stores mined corrections, standing approvals, cross-project shared lessons and preferences. The user never runs commands, so they can't inspect or undo any of it. Silent learned state erodes trust.
  Done when: asking "what have you learned about me?" returns one plain list from a single view, with each item's source. Answering "forget 3" deletes it and it stops firing in later injections.

- **Track background processes and ports started during a task** — FIX — value 3 — effort S — risk low
  Why: assumption: dev servers and watchers launched via Bash are left running. Reaping already covers worktrees, temp files and locks, but not processes or ports, which cause "address in use" failures and wasted retry turns.
  Done when: processes started by the task are listed at done, and orphans and stale port holders are killed at task finish. A test starts a fake server and asserts it is gone after `fm task done`.

- **Export a project charter into the repo behind one outward yes** — FEATURE — value 3 — effort M — risk med
  Why: the handbook, gate commands, "start here" files and decisions live only in `~/.claude/foreman`. They are lost on uninstall and invisible to teammates, CI and other tools. Repo instructions already conflict-check against Foreman, so a durable, shared form is the missing piece.
  Done when: `fm charter` writes a bounded (≤ 3 KB) `AGENTS.md` section or `.foreman/charter.md`, redacted and diffable. It only writes after the yes, and a fresh clone with no Foreman state reads the same gates.

- **Import issue and PR threads as briefs** — FEATURE — value 3 — effort M — risk low
  Why: assumption: work often starts from a GitHub issue link. Intake handles pasted errors and TODOs but not linked threads, so the user pastes text by hand and loses the labels, reproduction steps and linked PRs.
  Done when: a prompt containing an issue URL, with `gh` available, creates a brief with the acceptance criteria drawn from the thread. The hook does no network work; `fm` fetches on the model's turn. If `gh` is missing, it degrades to asking for a paste.

- **Turn unexecuted changed lines into queued test tasks** — FEATURE — value 3 — effort M — risk med
  Why: "prove changed lines were executed" only detects the gap. Acting on it is the second-order step, and it closes the FIX and FEATURE coverage hole without the user asking.
  Done when: changed-but-unexecuted hunks at done create one queued brief naming the hunks and their nearest test file. The brief is deduped against existing ones.
