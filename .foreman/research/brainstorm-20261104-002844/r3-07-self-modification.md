# Brainstorm — lens: self-modification

- **Run the gate from a frozen release copy while a goal edits plugin/** — FIX — value 5 — effort M — risk med — category: self-hosting
  Why: evidence and lease commands already fail inside the builder worktree. Sampo builds itself, so a half-edited hook or `done` gate in the worktree can break the check meant to catch the edit. Assumption: the previous green install generation is still on disk.
  Done when: a scripted goal whose builder breaks `plugin/lib/sampo/` imports still gets a working `fm evidence` and `fm done` verdict from the frozen copy, and the verdict names which copy ran.

- **Tier self-edits by surface, with a different bar for each** — FEATURE — value 4 — effort M — risk med — category: self-edit pipeline
  Why: assumption: wording changes in a skill and logic changes in a hook are currently proposed and judged alike. Wording needs an exam plus a cold read. Gate or hook code also needs the planted-fault tier replay and a probation period.
  Done when: `fm` rejects a hook-code edit that carries only the wording-tier evidence and names the missing tier.

- **Keep a goal-local "tried and failed" file that reloads after compaction** — FEATURE — value 5 — effort S — risk low — category: resume
  Why: resume is the worst area, and compaction drops dead ends, so the agent retries them. The file is written when the same command or approach fails 3 times, and the resume card re-injects it, capped at 15 lines.
  Done when: in a compaction drill, the agent does not repeat a command listed in the file within the next 20 tool calls.

- **Record a self-edit's prediction when it is made and score it at 14 days** — FEATURE — value 4 — effort M — risk low — category: self-edit accountability
  Why: self-edits currently roll back on a worse outcome, but no one records what the edit promised. Each edit would state which false-done class it targets and how many firings it expects, and a miss auto-proposes a revert task.
  Done when: a seeded edit that never fires produces a revert proposal on day 14 showing the original prediction beside the count.

- **Detect a gate clause that keeps being patched and rewrite it** — CLEAN — value 3 — effort S — risk low — category: gate hygiene
  Why: the 6 false dones are unchanged since gen 2, which suggests patches that don't take. A clause edited 3 or more times across generations without moving its false-done count gets flagged for a from-scratch redesign instead of another patch.
  Done when: `fm genesis check` lists any clause with 3 or more edits and an unchanged false-done count.

- **Distil a repo playbook from each finished goal** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: assumption: each goal rediscovers the repo's real gate commands, worktree quirks and slow tests. After close, only the commands that actually ran green are written to a short repo card, which the next goal's planner reads.
  Done when: a second goal in the same repo starts with the first goal's verified gate command and does not rediscover it.

- **Let a goal tune its own caps inside a signed envelope** — FEATURE — value 3 — effort M — risk med — category: goal config
  Why: the stall and spend limits are global, but long goals have different shapes. The agent may adjust stall minutes or proof timeouts only within bounds set at intake. Every change is logged, and widening past the bounds goes to the user's decision sheet.
  Done when: a change within the bounds applies and is logged, and a change outside them is refused with the widening command.

- **Dry-run a candidate self-edit by resuming the live goal's snapshot headless** — FEATURE — value 4 — effort L — risk med — category: self-edit verification
  Why: replaying a hand-written failure doesn't show the edit working on the goal actually in flight. The check restores the live goal's ledgers into a scratch home, resumes under the candidate, and compares the first action with the baseline's.
  Done when: a deliberately broken resume edit is rejected because its first action differs and the diff is printed.

- **Harvest goals that recovered from a fault as positive resume examples** — FEATURE — value 3 — effort M — risk low — category: resume
  Why: the corpus so far holds failures. Real goals that survived a kill or compaction contain the sequence that worked. Those sequences become scenarios the planted-fault tier must still pass.
  Done when: at least 3 recovered-fault scenarios from real ledgers run in the tier, and breaking resume turns them red.

- **Synthesize goal-local macros from repeated command sequences** — FEATURE — value 3 — effort M — risk med — category: self-extension — **wild**
  Why: assumption: builders repeat the same 3-to-5-command proof or build dance dozens of times a goal. Sampo offers `fm do <name>`, which runs under the guard, is scoped to the goal, and expires at close unless the user promotes it.
  Done when: the third identical sequence in a goal prompts a macro, the macro runs through the guard, and it is gone after `fm done`.

- **Keep an out-of-tree witness that re-judges the done verdict** — SECURITY — value 4 — effort L — risk med — category: tamper resistance — **wild**
  Why: the protected core is pinned by hash, but the judge and the judged still live in one tree. A tiny verifier of about 200 lines, installed outside the repo and read-only to the agent, re-derives done from clauses and evidence. A disagreement blocks `fm ship`.
  Done when: a planted self-edit that makes the in-tree gate always pass is caught because the witness disagrees.

- **Make an edit's effect undoable by replaying the ledger without it** — FEATURE — value 3 — effort L — risk high — category: self-edit rollback — **wild**
  Why: today a rollback reverts the code but cannot tell which past verdicts the edit changed. Replaying the ledger with the edit toggled off lists exactly the closes and dones it flipped, so the user sees what to re-check.
  Done when: toggling a test edit off lists the seeded close it had changed, and no others.

- **Show what a self-edit would have changed on the user's last 10 goals** — FEATURE — value 3 — effort M — risk low — category: self-edit preview — **wild**
  Why: the user sees a diff of text but not of behaviour. A preview card says "this edit would have held 2 of your last 10 dones and let none through", computed from the stored clause and evidence records.
  Done when: the card is printed with every self-edit proposal, and its counts match a manual replay on a fixture ledger.

Next question: Which self-edits has Sampo made to itself so far that the user never saw, and would the user have approved each one?
Next question: When the builder edits Sampo's own files during a goal on another repo, which of its checks still run from the edited copy?
