# Brainstorm — lens: user value

- **Run standing orders on a schedule or condition** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the user's most repeated asks are recurring chores ("Release 1.2.x to GitHub main and JARVIS", dependency checks, cleanup). `fm night` has fixed jobs, but there is no user-authored "when X, do Y" rule.
  Done when: `fm order add "when gates are green on main and CHANGELOG has unreleased lines, propose a release"` fires once on a fixture repo, logs the trigger, and `fm order list` shows the last run.

- **Revert a task along with its dependents** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: assumption: `fm undo` ideas cover snapshots, not "T-0401 was wrong." `fm relate` already knows which tasks build on which, so a revert can be planned across them.
  Done when: `fm revert T-x` on a fixture with two later dependent tasks prints the ordered revert plan, creates a revert task for each, and a gate run passes after applying them.

- **Shrink every FIX repro to a minimal failing case** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: FIX briefs are terse ("login times out on slow wifi"). A minimized repro, kept as a permanent regression test, is stronger proof than a red-to-green run on a sprawling case. This is delta-debugging, which differs from the red-first criteria already proposed.
  Done when: given a 200-line failing input fixture, Foreman records a repro of ≤20 lines that still fails, and it is attached as the task's evidence.

- **Sweep a fix across all my projects** — FEATURE — value 5 — effort L — risk med — category: cross-project
  Why: the user relays the same class of fix to JARVIS and to GitHub main by hand (symlink rm, lane rm caches). Assumption: other projects share the pattern. Foreman could generalize a finished fix into a search signature and queue briefs where it matches.
  Done when: after finishing a fixture task, `fm sweep T-x` lists matching sites in a second registered project and creates one captured brief per site, each citing the source task.

- **Search code and history by meaning, locally** — FEATURE — value 4 — effort L — risk low — category: recall
  Why: `fm recall` and `fm why` work by ids and lexical match. A local embedding index over code, briefs, diffs and decisions would answer "where did we deal with symlinks?" with citations, and keeps data on the owner's machine.
  Done when: the query "where do we handle symlinks in rm" returns the guard code and T-0411's brief in the top 3, with no network calls (verified by blocking egress in the test).

- **Capture TODOs from the user's own edits** — FEATURE — value 3 — effort S — risk low — category: capture
  Why: T-0317 ("There's new bug feedback") shows requests arriving from outside the chat. Only chat-sourced requests are captured today, so a `TODO(fm)` or `FIXME` the user types never reaches the inbox.
  Done when: adding a `# TODO(fm): handle empty config` line produces one inbox brief with file:line, and removing the line closes or marks it stale.

- **Split oversized briefs into a dependency chain at intake** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: `fm batch` merges small requests, but nothing does the opposite. L tasks sit deferred (T-0034, T-0035) because they're too big to start.
  Done when: an L brief with three separable concerns becomes three linked S/M tasks with an order and a plan-level rationale, and the original brief points to them.

- **Turn Claude Code releases into adaptation tasks** — FEATURE — value 4 — effort M — risk low — category: maintenance
  Why: T-0316 and the guard's `bash -lc` miss show breakage arrives from outside. The hook and settings surface is the dependency. Foreman could diff the changelog and schema against its hook contract and queue briefs.
  Done when: given a fixture changelog that renames a hook field, `fm landscape` or a new `fm cc-watch` creates a brief naming the affected `plugin/` files.

- **Generate a hermetic dev environment from what the gates need** — FEATURE — value 3 — effort M — risk med — category: reproducibility
  Why: assumption: the install requires Python 3.12.7 and several tools, and lanes in fresh worktrees repeat setup. Deriving a devcontainer or lockfile from observed gate runs would make lanes and CI identical.
  Done when: the generated environment runs `fm check` green in a clean container, and the generated file lists every tool the gates invoked.

- **Review the user's own commits in the background** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the lenses run only on Foreman's tasks, but the user also edits by hand. A quiet pass over their commits would catch what Foreman would have caught.
  Done when: a manual commit with a seeded off-by-one produces a finding in the inbox within one pass, and commits with no findings produce no output.

- **Wild: Hold a rubber-duck mode** — FEATURE — value 3 — effort S — risk low — category: thinking
  Why: wild; the user's requests are often half-formed ("super recursive brainstorm"). A mode where Foreman only asks clarifying questions and never edits, then condenses the talk into a research note, would help shape them.
  Done when: `fm duck` runs a 5-turn exchange with no file writes outside `research/`, and ends with a saved summary listing open questions.

- **Wild: Fork a UI feature into three prototypes and pick by screenshot** — FEATURE — value 4 — effort L — risk med — category: design
  Why: wild; the user steers hard on a "beautiful UI with smooth animations." Three builder lanes could each build a variant, `fm smoke` captures desktop and phone shots, and the user picks in the app.
  Done when: one command yields three lane branches and a gallery with one screenshot pair each; picking one merges its lane and removes the other two.

- **Wild: Work backwards from a demo date** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: wild; the queue has 20+ items and no notion of "by Friday." A deadline mode would cut scope, order work by what the demo needs, and script the demo run.
  Done when: `fm until "friday demo"` marks queued tasks must, nice or cut with reasons, and produces a demo checklist that `fm smoke` can run.

- **Wild: Hand the user a "pre-mortem" before any L task starts** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: wild; L plans currently ask for approval without showing how they might fail. A short, ranked list of likely failure modes, drawn from past blocked tasks, would make approval informed.
  Done when: an L plan shows three failure modes, each citing a past blocked task, and the user's approval is recorded with the list attached.
