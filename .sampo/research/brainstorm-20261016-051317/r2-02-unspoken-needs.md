# Brainstorm — lens: unspoken needs

- **Keep a durable authorization ledger** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the user granted "push to main when you get a chance" twice, in nearly the same words (1.2.31, 1.2.32), and said "don't ask me any more questions or ANYTHING". Each grant lives in one message and expires with it. The ledger would record scope (push, tag, release, delete branches), the project, an expiry and the exact words, and it would refuse anything outside that scope.
  Done when: after one "push to main when done" grant, a second release in the same scope pushes without asking, a force-push or a different remote is refused naming the grant it lacks, and `fm grants` lists the grant with its expiry.

- **Cite every claim in the final report** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the user is AFK and reads one report afterwards, and cannot check a thousand tasks. The review found builders returning "done" without checking and findings with false premises (five dropped items). Each sentence in the report would link to a ledger id, commit or command output, and anything without one would print as "unverified".
  Done when: `fm report` on a fixture run puts a receipt id on every claim sentence, and a claim with no matching ledger row is marked "unverified" in the output.

- **Make the user-only list tick itself** — FEATURE — value 4 — effort S — risk low — category: handoff
  Why: T-0325 (needs `sudo pacman -S libappindicator-gtk3`), T-0418 (update the installed foreman-ui) and T-0352 (publish Desktop) are blocked on the user and sit as prose. `fm yours` would give each item a copy-paste command and a probe, and strike the item through once the probe passes.
  Done when: installing the missing package or updating the UI makes the matching item disappear from `fm yours` on its next run, with no manual close.

- **Dogfood each release on the user's own install** — FIX — value 4 — effort M — risk med — category: release
  Why: the installed foreman-ui is 0.7.0 while the repo is at 0.17.0, so the user never runs what gets shipped. After a release, upgrade this machine through the real marketplace path, run `fm selftest` and a pane screenshot there, and roll back on failure.
  Done when: a release run ends with `fm doctor` reporting installed == released on this machine, and a deliberately broken release candidate is rolled back automatically.

- **Learn which pings are worth sending** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: the user says "I shouldn't need to ask", which implies they also don't want to be pulled in for nothing. Track which notification kinds were acted on within a few minutes and which were ignored, then mute the ignored kinds and promote the acted-on ones. The "approval fatigue" and "push alerts" ideas send pings but don't learn which ones matter.
  Done when: replaying a recorded set of pings where "task closed" was always ignored and "blocked" always acted on stops sending the first kind and keeps the second.

- **Give every user-facing message a stable code** — CLEAN — value 3 — effort M — risk low — category: tests
  Why: baseline went red because `test_builder` asserted prose ("two builders") that T-0089's cap message ("2 builders are already out") had reworded. Tests and docs would reference message codes, so copy can improve freely.
  Done when: rewording any message in a fixture keeps all tests green, and a lint fails on a test that asserts a literal user-facing sentence.

- **Route every path-trust check through one gate** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: reviewers repeatedly found writes outside a folder, symlink escapes and overwritten leases (T-1037 confined `--into`, the demo recorder had to be moved onto "the shared check", lane pre-claims were fixed after the fact). One `trusted_path()` function plus a lint that flags ad-hoc realpath/startswith checks would stop the next feature reinventing it.
  Done when: a lint fails on a new ad-hoc containment check, and a test suite of traversal, symlink and O_EXCL cases passes against every writer that goes through the gate.

- **Show an honest guard coverage map** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: the user runs in bypass mode and relies on the guard, and the review notes the only way to learn what it allows is to write scratch scripts (T-1125, T-1141). Print the danger classes it blocks, each with a one-line demo, and a plainly labelled section for what it does not cover.
  Done when: `fm guard coverage` lists every class with a command that triggers it, and a test fails if a rule exists with no demo entry.

- **Import a rival plugin's rules** — FEATURE — value 3 — effort M — risk low — category: adoption
  Why: assumption: "make it THE plugin" means winning users who already have `AGENTS.md`, `.cursorrules` or another plugin's hooks. Foreman exports hints outward, but nothing maps an existing rule file to Foreman's cards, vetoes and gates, or shows what Foreman lacks relative to it.
  Done when: `fm adopt <file>` on a sample `AGENTS.md` produces the equivalent Foreman rules plus a list of untranslatable lines, and nothing is written without a preview.

- **Cap the mission's spend and show progress per dollar** — FEATURE — value 4 — effort S — risk low — category: cost
  Why: per-task caps exist, but a forever loop runs against a whole-mission budget. The USD budget in this very session shows one is real. Print a running "closed tasks per $" figure and park the loop with a receipt at the ceiling.
  Done when: a mission with a $1 ceiling stops dispatching builders at $1, writes a resume note, and `fm cost` prints a progress-per-dollar figure.

- **Treat capitalised words as priority signals** (wild) — FEATURE — value 3 — effort S — risk low — category: intent
  Why: wild. The user writes "SESSION/EACH SUB AGENT THING" and "ANYTHING" in capitals, which marks what they care about most. Tag emphasised phrases in intake and attach them to the task as a must-satisfy check in review.
  Done when: a request with a capitalised phrase produces a task whose review checklist includes that phrase verbatim, and reviewers flag its absence.

- **Score Foreman nightly against a "THE plugin" rubric** (wild) — FEATURE — value 3 — effort L — risk med — category: strategy
  Why: wild. The mission is to be THE plugin, but nothing defines that. A written rubric (one-command install, zero config, first win under five minutes, no stale install, measured bench win) would be scored every night, and the lowest score sets the next task.
  Done when: `fm rubric` prints a score per criterion with its evidence, and the worst criterion appears as the top queued task the next morning.

- **Audit what would embarrass a stranger on first install** (wild) — CLEAN — value 3 — effort M — risk low — category: polish
  Why: wild. The repo has 1,509 files, root clutter, committed demo recordings, a stale 0.7.0 UI for marketplace users and dozens of "Later from T-…" tasks. A fresh-eyes pass from a clean HOME would produce a ranked list of cringe, such as local paths, dead links, version mismatches and confusing first output.
  Done when: running the audit on a clean clone yields a ranked list, each entry has a fix task or an explicit waiver, and a repeat run after fixes is empty.
