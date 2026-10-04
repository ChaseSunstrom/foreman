# Delegation (reference)

Default: no subagents. The main thread plans, edits and writes all state.

Allowed only for:
1. read-only recon of a large codebase area → `foreman:fm-recon`
2. web or documentation research → first `fm recall "<question>"` (it may already be known), then `fm research ask "<question>"` (T-0206: parallel web-only researchers per sub-question, every quoted claim re-fetched and checked, one note saved; ✗ claims are unverified); `foreman:fm-recon` when the answer also needs the codebase
3. dependency or security audits → `foreman:fm-recon`
4. optional independent read-only review of L-tier changes → `foreman:fm-reviewer` (or `/code-review`)

Contract for every delegation:
- A self-contained brief: the question, scope paths, what to ignore, the output format. Never the conversation history.
- Read-only tools only (the Foreman agents have Read, Grep, Glob and, for recon, WebFetch/WebSearch).
- Output ≤ 400 words, every claim backed by `path:line` or a URL, confidence per finding, an explicit "not checked" list.
- Save the summary: `fm research add <topic> <<'EOF'` … `EOF`. Spot-check at least two claims yourself before relying on them.
- Parallel only with disjoint scopes, at most 3 at once.
- Installed plugins' implementation agents are not used for implementation; their review agents may be used for (4).
