# Brainstorm — lens: user value

Ten ideas for the user-value lens. The pack's idea list is very large, so a few of these are second-order twists on neighbouring ideas, and I name the neighbour where that applies. The performance and agents gaps are covered by items 2, 6 and 9.

- **Flag diffs that undo recent closed work** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: assumption: round 1 had follow-up fixes to its own output (T-0812 tier-drift and worktree warnings, T-0817 guard rules), so a later task can silently undo an earlier fix. The nearest existing idea compares queued tasks with each other, not a finishing diff with closed tasks.
  Done when: finishing a task whose diff reverts hunks from a task closed in the last 14 days prints one warning naming that T-id, and a fixture test shows it firing.

- **Run a cheap diff-risk agent before the full done-tail** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: assumption: most S-tier closes are low-risk and pay the full audit cost. A haiku child reads the diff stat plus the task's tier and returns skip, light or full. A "full" verdict can only add checks, never remove them.
  Done when: a docs-only S task closes without the audit lenses, a guard-file edit triggers the full tail, and the bench shows the median close time drop.

- **Run a post-install claim check** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user asked for releases to GitHub main and JARVIS. A release currently says it shipped, not that it works on the target. Each changelog line carries a one-line probe, and `install.sh` runs them at the end and prints "7/7 claims live".
  Done when: installing a build where one claimed feature is broken prints that claim as failed and exits non-zero.

- **Set one spend envelope for a recursive mandate** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the user said "super improve… etc. etc. etc." and "recursively improve", which is open-ended. Today each round needs a new ask. One declaration (hours, dollars or rounds) lets rounds run until the envelope or a convergence rule ends them, and the stop reason is printed. This combines the rounds idea with the budget-broker idea.
  Done when: `fm round --budget 2h` runs rounds back to back, stops with a stated reason (budget, no new ideas or needs the user), and survives `/compact`.

- **Show a before/after of each fixed metric on the real data that exposed it** — FIX — value 4 — effort S — risk low — category: correctness
  Why: the user caught two wrong metrics (track record missed `✗ exit N`; catch rates matched the wrong string). At close, a fix to a reader prints the number it produced before and after on the user's actual store. The user sees the correction, not just "fixed".
  Done when: closing such a fix prints "catch rate 0% → 31% on N stored results".

- **Gate children's spend with a per-lens payoff history** — PERFORMANCE — value 3 — effort M — risk low — category: agents
  Why: every brainstorm child costs money, but lenses differ in how many ideas the user keeps. Track kept versus produced per lens, and let the budget skip lenses at 0% over three rounds. The user can force any lens back on.
  Done when: after three rounds, `fm ideas` reports skipped lenses with their keep rates, and `--lens` overrides.

- **Hand over a single-screen "decide these 3 things" at round start** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: assumption: the 14 captured and deferred clusters (T-0787 to T-0799) and the pending yes for compact output wait for the user, who does not read the queue. One screen lists three decisions, each with a recommended default and an accept key.
  Done when: starting a round prints at most three items with defaults, and accepting one updates the queue and clears it.

- **Wild: Let the user say "keep it like this" about a behaviour** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: the user's drops show they protect things by design (compact output opt-in, heredoc rule). A pin freezes a behaviour. Later self-improvement rounds must bring a replay or bench case to change it, and the pin shows up in the pack as a hard constraint.
  Done when: a round that proposes changing a pinned behaviour is rejected at plan time with the pin's text quoted.

- **Wild: Keep a hot "second opinion" session that reads only the user's words** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: a standing cheap session gets the user's verbatim requests and steers plus the final close-out, never the work. At each close it answers one question: "would this person say yes?" Disagreements are logged as a score, not a block.
  Done when: each closed task has a yes/no/unsure verdict from the session, and the weekly summary shows agreement with the user's later complaints.

- **Wild: Spend leftover quota on a "gift" task** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: assumption: weekly usage often expires unused. Near the end of the window, a lane picks the smallest deferred task with the clearest check, does it in a worktree, and leaves it unmerged with a one-line pitch. The user takes it or deletes it.
  Done when: the near-expiry condition produces exactly one unmerged lane with a pitch line, and deleting it leaves no residue.

- **Wild: Say "nothing changed for you" when nothing did** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: round 1 shipped a lot, but its visible effects (a session title, the monitor, a push) are small. The close card classifies a round's items as user-visible, invisible or hardening-only. The user can stop reading at a glance.
  Done when: the round close card counts each class and links every user-visible item to where it appears.
