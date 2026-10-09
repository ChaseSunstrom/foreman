# Delegation (reference)

The main thread plans, edits and writes all state. Subagents and fm's child runs are bounded by `fm budget` (T-0227): use them whenever they buy parallelism or fresh eyes — the caps, not abstinence, keep spend in check (T-0364: "default none" left long gates idle and research serial).

Models (T-0373): the main thread (Opus or Fable) plans, judges, merges and writes state; the work it hands out runs on the cheapest model that can do it, passed as the Agent call's `model` (and `effort` where Claude Code offers it):

| Work | Agent | Model |
|---|---|---|
| find where something is, read a long log/changelog and summarize it | `foreman:fm-scout`, or general-purpose with `model: "haiku"` | Haiku |
| recon, research, audits, debugging hypotheses | `foreman:fm-recon` / `fm-reviewer` / `fm-debugger` | Sonnet (their frontmatter) |
| an S task in a builder lane | `foreman:fm-builder` (`fm lane brief` prints `model: "sonnet"`) | Sonnet |
| an M task in a builder lane, an L plan's critique | `foreman:fm-builder`, `fm second plan` | the main model |
| brainstorm lenses, research children, oracle, bench | `fm ideas` / `fm research ask` / … (`--model`) | Sonnet by default |

A cheaper model's output is still checked: the main thread reviews a builder's diff, spot-checks two claims of any report, and re-runs the criteria itself.

Allowed only for:
1. read-only recon of a large codebase area → `foreman:fm-recon`
2. web or documentation research → first `fm recall "<question>"` (it may already be known), then `fm research ask "<question>"` (T-0206: parallel web-only researchers per sub-question, every quoted claim re-fetched and checked, one note saved; ✗ claims are unverified); `foreman:fm-recon` when the answer also needs the codebase
3. dependency or security audits → `foreman:fm-recon`
3b. a failure that keeps coming back → `foreman:fm-debugger` (read-only; ranked hypotheses with discriminating probes, ready for `fm task hypo`)
4. optional independent read-only review of L-tier changes → `foreman:fm-reviewer` (or `/code-review`)

5. the one bounded exception that edits — a builder (T-0234) → `foreman:fm-builder`, below

Contract for every delegation:
- A self-contained brief: the question, scope paths, what to ignore, the output format. Never the conversation history.
- Read-only tools only (the Foreman agents have Read, Grep, Glob and, for recon, WebFetch/WebSearch) — except a builder.
- Output ≤ 400 words, every claim backed by `path:line` or a URL, confidence per finding, an explicit "not checked" list.
- Save the summary: `fm research add <topic> <<'EOF'` … `EOF`. Spot-check at least two claims yourself before relying on them.
- Parallel only with disjoint scopes, at most 3 at once.
- Installed plugins' implementation agents are not used for implementation; their review agents may be used for (4).

Builders (T-0234): an independent S/M task with runnable criteria can be worked by a `foreman:fm-builder` while the main thread does something else (another task, a review). At most two out at once; never two that edit the same files.
1. `fm lane brief ID` writes the builder's brief (the task's request, criteria with verify commands, steps, its contract) and prints the Agent call: `subagent_type: "foreman:fm-builder"`, `isolation: "worktree"`, prompt `Read <brief> and work the task it describes`. It refuses an L task, a task someone is working on, a task with no verify command and a third builder.
2. The builder's first command, `fm focus ID` in its worktree, binds the task there (and records the branch it's on): the guard, evidence and gates are its own. It works test-first, records evidence, runs `fm check --evidence ID` and commits on its branch. Enforced, not only asked: the guard refuses any write outside its worktree but scratch (category `confine`, never grantable; the main checkout never counts as scratch), and from its worktree `fm task done/finish/audit/drop` and every `fm lane` change are refused.
3. When it returns: one `foreman:fm-reviewer` on `git diff HEAD...<branch>`; fix or reject findings (in the worktree, or after the merge); `fm lane merge ID` (T-0377: a --no-ff merge with every changed file judged as the task's own write, so it also works on Foreman's own repo, where the guard refuses a plain `git merge`); `fm lane rm ID` (takes the task back and frees the builder slot; the worktree goes, and its own branch — the one recorded at focus, or `foreman/ID` — once merged, never a branch it switched to or a default branch); `fm focus ID`; re-run its criteria here (fresh evidence on the merged tree); `fm task finish ID` with the review's lenses — no `--commit`, the merge was the commit.
4. A builder that failed or stopped: read its report, `fm lane rm ID` (it refuses uncommitted work: commit it on the branch or remove it there), and work the task in the main thread. A brief that was never launched: `fm lane rm ID` frees its slot.
