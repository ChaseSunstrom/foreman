# Brainstorm — lens: unspoken needs

- **Run the user-only steps from one reviewed script** — FEATURE — value 4 — effort S — risk low — category: handoff
  Why: T-0325 (`sudo pacman -S libappindicator-gtk3`), T-0418 (update the installed foreman-ui) and T-0352 (publish Desktop) all wait on commands only the user can run. The final report would list them as prose, and they are never a single action. Assumption: the user would rather read one file and run it than copy three commands.
  Done when: `fm todo --script` writes an executable file with the privileged and outward commands in order, each with a comment naming its task and what it unblocks. The file refuses to run if it is edited after generation.

- **Cut pack text at sentence boundaries and always keep DONE-WHEN** — FIX — value 4 — effort S — risk low — category: pack quality
  Why: the "user's own words" lines end mid-clause ("a test seeds a ledger with …", "the user's own unco…"). The acceptance criterion is the part cut off, and it is the part a brainstormer or builder most needs.
  Done when: a test with a 400-character brief renders a line ending at a sentence boundary that still contains the full `DONE-WHEN:` clause, within the same length cap.

- **Tag each brief's origin and quote only the user's real words as the user's** — FIX — value 4 — effort S — risk low — category: signal purity
  Why: most "asked:" lines (`FEATURE: Add fm todo… DONE-WHEN`) are loop-written briefs, not user requests, so the "unspoken needs" lens reads Foreman's own output as the user's voice. The only real user quotes are a few release/push requests. Assumption: briefs have no origin field today.
  Done when: a fixture with one user-typed and one loop-captured brief yields a pack where only the user-typed one is under "user's own words", and the other appears under "loop-captured".

- **Fence edit-time writes to files dirty before the drive started** — SECURITY — value 4 — effort M — risk med — category: user's tree
  Why: T-1169 only handles this at close, which shows the user edits the same tree while Foreman works. Close-time detection still lets the drive overwrite their uncommitted changes before the commit step. Assumption: PreToolUse can read a dirty-set snapshot taken at focus time.
  Done when: a test dirties `a.py`, focuses a task, and the drive's Edit of `a.py` is denied with the `--with FILE` hint. Edits to clean files pass.

- **Preflight the user's git state before any loop commit, merge or push** — FIX — value 3 — effort S — risk low — category: user's tree
  Why: the release ritual merges in a temp worktree and pushes to main while the user may be mid-rebase, mid-merge or holding `index.lock`. The user asked for "push to main when you get a chance", so the loop pushes unattended. Assumption: no such check exists in the release path.
  Done when: a fixture repo with `.git/rebase-merge/` makes `fm lane merge` and the push step stop with "your repo is mid-rebase" and queue a retry. The run does not fail.

- **Answer "was this already considered?" with `fm why-not "<idea>"`** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the pack shows five ideas dropped for false premises, with the evidence recorded. Brainstormers still re-propose near-copies, and the user can't ask the question themselves. This is the query side of the dropped record, not a new filter.
  Done when: `fm why-not "labelled guard cases"` prints T-1162 as built, and `fm why-not "retry red lane-merge criterion"` prints the drop reason with its evidence. An unknown idea prints "no record".

- **Keep a "noticed, didn't touch" margin file for builders** — FEATURE — value 3 — effort M — risk med — category: capture without bloat
  Why: every builder branch needed 2-6 defect fixes, and adjacent problems get noticed and lost. Capturing each as a brief is how 37 deferred items piled up. Assumption: a capped, expiring file avoids that.
  Done when: `fm margin add "<note>" --file F` appends to `.foreman/margin.md` and notes expire after 14 days. `fm next` shows the count, and `fm margin promote N` turns one into a brief.

- **Lead the return receipt with surprises, not successes** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: `fm away` and `fm todo` exist, but a returning AFK user's first fear is "what did it do that I wouldn't have expected". The receipt should rank pushes, reverts, settings changes, spend over the contract, deletions and guard overrides above routine closes. Assumption: `fm away` currently orders chronologically.
  Done when: a seeded ledger with 20 routine closes and one push to main renders the push as line one under "you might not expect". Routine closes are collapsed into a count.

- **Rank skill descriptions by use and trim the unused from the session listing** — PERFORMANCE — value 3 — effort M — risk med — category: token cost
  Why: `plugin/skills/` holds 1,158 files, and the user wants Foreman fast, token-cheap and usable by small models. Assumption: skill names and descriptions are listed per session and most never fire. The pack doesn't show their size.
  Done when: `fm usage --skills` prints bytes of listed descriptions and the count of skills unused in 60 days. A flag-gated mode lists only used ones plus a pointer to `fm lib`, and the bytes drop by a stated amount in a test.

- **Show the guard's exact passing rewrite beside each refusal** — FEATURE — value 4 — effort M — risk med — category: friction
  Why: 31 refusals in 4 days were mined by hand. The relaxation was reverted because it prevented 0 refusals, so the lever is helping the model fix the command, not loosening the rule. Assumption: for the common split cases a mechanical rewrite exists.
  Done when: for 3 mined refused commands, the refusal text includes a rewritten command that `fm guard try` allows. A test asserts the rewrite passes.

- **Wild: Test the final report on a cold small model** — FEATURE — value 4 — effort M — risk low — category: report quality
  Why: assumption: the user wants to read the report once and know what only they can do. A weak local model given only the report and asked "what must the human do next, in order?" is a cheap proxy for a tired reader.
  Done when: `fm report --check` feeds the report to a configured local model. It flags the report when the model's answer misses any item in `fm todo` and prints which. A fake-model test covers one pass and one fail.

- **Wild: Pick one showcase moment per round for the user to show someone** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user's words never ask for delight. They keep asking for plain, verified results, and the demo SVG shows they care about showing the work. Assumption: one curated 10-second pane clip per round beats a changelog.
  Done when: closing a round writes `showcase/round-N.svg`, picked from the round's closes by a scored rule, and the report links it. The file exists and is under a stated size cap.

- **Wild: Hold a "regret test" before pushing to main** — SECURITY — value 4 — effort M — risk med — category: release trust
  Why: assumption: the user gave standing permission to push but not to be surprised. Before any unattended push, Foreman lists what it would tell the user it did and checks each line against the user's past steers (the revert of the data-only relaxation, the drops). It holds the push if any line resembles a past steer-against.
  Done when: a test seeds a steer "never auto-delete files" and a pending push containing a deletion. The push is held and an entry appears in `fm todo` with the matched steer quoted.
