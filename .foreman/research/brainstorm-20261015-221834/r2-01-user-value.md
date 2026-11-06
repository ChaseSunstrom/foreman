# Brainstorm — lens: user value

- **Measure user interventions per closed task** — FEATURE — value 5 — effort M — risk low — category: metrics
  Why: the user's steers and "why have you not improved" show they are the feedback loop, and nothing counts how often they have to correct or repeat. Foreman scores its own gates but not the user's effort.
  Done when: `fm stats` prints interventions per closed task (corrections, repeated asks, manual re-runs) for the last 7 and 30 days, and a fixture session with two corrections reports 2.

- **Add an asks ledger that maps each request to its outcome** — FEATURE — value 5 — effort M — risk low — category: traceability
  Why: the pack lists dozens of asks and 30+ "Later from T-07xx" deferrals. The user can't see which of their words became shipped, deferred or dropped work.
  Done when: `fm asks` lists each verbatim ask with its task ids, the commit that shipped it, or "deferred: reason", and a seeded ask with no task shows as "unanswered".

- **Check UI work against the user's stated layout rules before showing it** — FEATURE — value 5 — effort M — risk med — category: ui verification
  Why: the pane went through many reload rounds ("still cluttered", "must be completely filled", "no scaling issues"). Each steer is a testable invariant that was only checked by the user's eyes.
  Done when: steers like "fills the dock exactly" and "no section shifts when content changes" are stored as layout assertions, run at several widths in the pane test, and a deliberate gap fails the check.

- **Seed known fixes from git history on adoption** — FEATURE — value 4 — effort M — risk med — category: onboarding
  Why: T-1032 learns fixes only after a failure and then a success, so a new repo starts empty. Fix commits, reverted commits and CI-config changes already hold obstacle→fix pairs.
  Done when: `fm adopt` on a repo with 20 fix commits drafts at least some hints, marked "unproven" and held out of auto-apply until one real hit.

- **Explain any line with `fm why`** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: users ask for audit logs of multi-agent runs, and Foreman already holds the task, plan and proof. A reader of the diff can't get from a line to the ask that caused it.
  Done when: `fm why path:line` prints the task, the user ask in their words, the plan step and the proof command, and it works on a line changed by a worktree builder.

- **Undo a closed task and learn why** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: the per-step rewind idea stops at one step. When the user dislikes a shipped result, there's no verb that reverts the merge and also records the reason.
  Done when: `fm task undo T-n --why "<reason>"` reverts the merge, reopens the task with the reason attached and stores a veto that the next plan shows. Tests cover a clean revert and a conflicted one.

- **Hold long goals as a mission with success criteria** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: asks like "make foreman genuinely the best" and "recursive brainstorm until dry" span many tasks and sessions. Tasks are tracked, but the goal, its stop test and its progress are not.
  Done when: `fm mission` stores a goal, a measurable stop condition and its child tasks, and a fresh session's start line shows "mission X: 6/11, next T-n".

- **Run a pre-mortem on L tasks from similar closed failures** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: `--why-not-caught` already records why failures slipped. That data isn't read back at plan time.
  Done when: planning an L task shows the three most similar past misses with their "why not caught" lines, and the plan must say how each is avoided.

- **Close with something the user can look at** — FEATURE — value 4 — effort M — risk low — category: receipts
  Why: T-0795 (plain receipts) is deferred, and UI tasks needed repeated reloads to be judged. A one-line "tests passed" doesn't show a pane change.
  Done when: closing a UI task attaches a before/after screenshot pair to the task, and `fm task show` links it.

- **Complaint-triggered self-postmortem** (wild) — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: wild; the user's "why have you not really improved" is the strongest signal in the pack. When a message shows frustration or a repeat correction, Foreman runs a short why-chain on itself and files a task that adds a gate, hint or test, before the reply moves on.
  Done when: a seeded message "you did this wrong again" produces a postmortem file naming the missed rule and a linked task, and the same mistake in a replay is then caught.

- **Review output against a taste profile built from the user's steers** (wild) — FEATURE — value 4 — effort L — risk high — category: personalisation
  Why: wild; assumption: steers like "liked the old plot chart" and "drop the small bars" are consistent enough to be a rubric. A cheap reviewer pass would flag "this looks cluttered" before the user does.
  Done when: on 10 past UI changes the user later corrected, the profile flags at least 6 of them, and it never blocks a close, only annotates.

- **Calibrate with three yes/no questions a week** (wild) — FEATURE — value 3 — effort S — risk low — category: preferences
  Why: wild; assumption: the user would answer a 10-second question. Foreman picks three recent judgement calls ("I deferred X; would you rather I'd built it?") and records the answers as preferences for the next planning round.
  Done when: `fm calibrate` shows three questions from the last week's decisions, and the answers appear in `fm prefs` and bias the next triage.

- **Make README claims into checks** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: the user asked to re-record the demo and refresh pictures by hand. Each README number, command and image is a claim that can go stale.
  Done when: `fm doctor docs` fails when a README command no longer exists, or when a pictured pane differs from a fresh render beyond a set threshold.
