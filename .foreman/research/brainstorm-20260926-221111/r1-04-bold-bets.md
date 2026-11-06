# Brainstorm — lens: bold bets

- **Offload exploration to a cheap read-only scout** — FEATURE — value 5 — effort M — risk med
  Why: `fm cost` breaks tokens down by tool, and the user says one session burned 20% of the weekly budget. Read/Grep exploration by the main model is the likely sink. Assumption: exploration dominates spend.
  Mechanism: `fm scout "question"` runs a read-only `claude -p --model haiku` and returns at most 300 chars. Each claim carries `file:line` plus a quoted snippet, and `fm` mechanically checks that every quote exists at that line. Unverified claims are dropped.
  Done when: on 10 replayed tasks, main-session Read/Grep tokens fall by ≥30% and every scout citation resolves.

- **Build a task-shaped context pack at focus** — PERFORMANCE — value 5 — effort M — risk low
  Why: start-here files, outline, symbol index and impact all exist but stay separate. The agent still spends turns stitching them together. Assumption: multi-file reads are frequent.
  Mechanism: `fm pack` writes one file of function and class bodies (not whole files). It draws on scope, past touched sets, the failing test and callers from impact. The focus note points to it, and reads of the pack's files are later scored as covered or wasted.
  Done when: median Read calls before the first edit drop ≥40% with no rise in failed gates.

- **Localize regressions by delta-debugging hunks** — FEATURE — value 4 — effort M — risk low
  Why: the bisect-across-finished-tasks idea was already built. Nothing narrows within a single red diff, and tree hashes already identify the last green tree.
  Mechanism: `fm culprit` splits the diff since the last green tree into hunks and applies subsets in a temp copy, using ddmin plus the failing verify command. It outputs the minimal failing hunk set. It is language-agnostic and never touches the working tree.
  Done when: on a seeded 3-hunk regression it names the right hunk in ≤ ⌈log₂ n⌉+2 runs.

- **Apply edits as one atomic transaction with check and auto-revert** — PERFORMANCE — value 4 — effort M — risk med
  Why: multi-file changes take N edit calls plus a check call, and checkpoint/undo needs a yes/no from the user. Assumption: many turns are mechanical edit-and-check loops.
  Mechanism: `fm apply PATCH [--check affected]` applies a unified diff to the tree, runs the affected tests, and auto-reverts on red. Reverting is safe because the transaction is its own and the tree was clean at the start. Add `fm rename OLD NEW`, a word-boundary rename with an impact preview.
  Done when: a 6-file rename runs in 1 call, and a red run leaves a byte-identical tree.

- **Run a pre-mortem at plan time for L and security tasks** — FEATURE — value 4 — effort S — risk low
  Why: audits fire only at done, when fixing is most expensive. Assumption: plans are sometimes wrong in ways cheap critics can predict.
  Mechanism: at `fm focus` for L tier, a tool-less `claude -p` gets the brief plus the impact map. It returns ≤5 failure modes, each with a candidate verify command. These are appended as proposed criteria and the agent accepts or rejects each.
  Done when: replaying past L tasks that later failed audits, ≥40% of the audit findings appear in the pre-mortem.

- **Draft plans for queued tasks while idle** — PERFORMANCE — value 3 — effort M — risk med
  Why: `fm focus` refuses unplanned briefs, so planning latency and tokens land in the live session. Nothing plans ahead yet.
  Mechanism: after `fm task done` or at Stop with a non-empty queue, a detached `claude -p --model` sonnet-tier job drafts the next brief's plan. It uses recall, the nearest past brief, and scope grounding. The plan is stored as `draft:`, and focus revalidates it against the tree hash and marks it accepted.
  Done when: focus-to-first-edit time and tokens drop ≥30% on tasks with a draft, and stale drafts are rejected.

- **Lint new code against sibling conventions** — CLEAN — value 3 — effort M — risk low
  Why: the pack's concern is code that reads like its surroundings. User corrections are mined, but repo idioms are not. Assumption: style corrections recur.
  Mechanism: PostToolUse on an edit computes a small fingerprint of the edited file's siblings (naming case, quote style, comment density, error idiom, import order). It emits one factual note listing deviations, at most once per file.
  Done when: seeded deviations are flagged and clean edits give zero notes across the test corpus.
