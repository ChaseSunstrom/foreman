# Mission 4 — verifying anything (gen 3, #6)

Task: T-2616 (brief 1; found and built while grounding, before this file was put, so the order put → intake → build
was not kept this once).

Parent: gen-3/seed.md row 4 → gen-0.md #6: "Verifying anything. Proof beyond unit tests: UI (`fm shot`, `fm flow`),
data, docs against code, infra and ops, performance, and "does it do what the user meant". Whatever can't be proven
gets labelled as unproven." gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply here unchanged.

## Capability
An unproven label that is itself true. Grounded first on the measures: gen-2's gap map names "intent proof beyond an
LLM lens" as #6's tier-4 gap, and `fm prove --rollup` today counts docs 601 and meaning 571, the two largest classes.
Built: the proof kinds (T-2273 to T-2396), fm prove --docs (T-2381), --infra, --migration, --data, measured perf,
fm spec's example assertions from a wish, the meaning class (T-2393).
What it lacks, found by reading the docs class before trusting it: 416 of its 601 items name CHANGELOG.md first, yet
`fm prove --docs --json` reports no claim from CHANGELOG.md at all, because fmdocs skips history files on purpose
(T-1817: "point-in-time records, not docs"). The kind flagged lines the run that clears it never reads: a green run
there proves nothing. The kind also diffed each task's start against HEAD (its own ponytail note), so a later
task's lines counted against an earlier one.

## Grounding
- Brief 1: fmcore._need_docs takes every `.md` a task touched (`_DOC_FILE`) and diffs `base` to HEAD; fmdocs._markdown
  and its readers skip `_HISTORY` files (changelog, changes, history, news); unproven_summary caches the rollup under
  a key with no rule version, so a rule change would never be recomputed.

## Gaps this Mission targets (coverage: #6)
- verify × CLI and judge × ledger: every unproven docs label names lines a docs proof can check, and only the lines
  the task itself landed.
- Not in this Mission: the 1,582 subcommand and flag claims `fm prove --docs` leaves unproven ("text in a file; a run
  of a documented command proves it (--yes-run)"). Proving them runs this tree's commands, which needs the user's
  `fm prove --yes-run` and is never self-granted: carried to the final report. Intent proof beyond an LLM lens stays
  open (see Ideas).

## Ideas (from the brainstorm, grounded)
The brainstorm ran: fm mission for #6, then fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen-latest 6, 523
distinct ideas (research/brainstorm-20261102-081535). Grounded against the code:
- "Audit what the project says about itself against what it does" (cross-bred): built as fm prove --docs and the docs
  kind; reading its numbers is what found brief 1.
- "Turn the user's sentence into example pairs they confirm, then run them": partial. fm spec writes 3 to 8 concrete
  assertions from a wish and keeps the user's own examples (fmchange.cmd_spec); no plan-time confirmation step. Its
  kill test (mock one sheet; drop it if the user reads only the summary) needs the user present: filed in not-yet.md
  with that blocker and the two approaches tried so far.
- "Make proofs expire when the thing proved changes": partial. A green run clears a kind only when it came after the
  task's last edit, and evidence lines carry tree and world stamps. Its own kill test (have proofs gone stale in the
  last 10 tasks?) ran: 3 of the last 10 had a later commit on their files, and the full gate at each reran the tests
  their proofs rest on, so none went stale. Filed in not-yet.md until a shot or bench proof goes stale.
The rest stay in the brainstorm's index for the next generation's #6 Mission.

## Approaches
1. Skip history files in the docs kind with fmdocs' own rule, diff to the task's own newest id-prefixed commit (HEAD
   when none), and put a rule version in the rollup's cache keys. Likely outcome: the docs class drops by the
   CHANGELOG-only tasks. Fails if: a project keeps real docs in a file named like a changelog (fmdocs already skips
   it, so the two stay consistent).
2. use what exists: have fm prove --docs read CHANGELOG too. Fails if: a changelog's old flags were renamed on purpose
   later; every old entry would read failed.
3. do less: leave the class and explain it in the rollup's text. Fails if: the largest unproven class stays mostly
   noise, and a green run keeps clearing lines it never read.

Choice: 1 (85%): the kind and the run that clears it then read the same files.

## Exam
The live rollup, before and after: docs 601 → 421 (settled under the new rule). The exam kinds that reach #6 (proof
and beyond, T-2394) are unchanged; their session arms run at the end-of-run exam. Unit checks: a task that touched
only CHANGELOG.md isn't listed for docs; a task whose own commit adds no claim isn't charged with a later task's
claim; one whose own commit adds one still is.

## Long-horizon goal (end of run)
Every docs label in the rollup names lines `fm prove --docs` reads; with the user's --yes-run, its subcommand and flag
claims are proven by running them.

## Lean
One filter, one git call per task (memoized), one version constant. No new verb.

## Tier share
Brief 1 is tier 3: an unproven label that can be trusted.

## Done when
The docs kind skips history files and diffs to the task's own commit; the rollup is recomputed after a rule change;
the unit checks pass; the live count is recorded before and after in the critique; MASTER.md (fm prove --rollup) and
CHANGELOG say it. No site page: the proof page reads the rollup.

## Briefs (fm intake)
```
FIX: the docs proof kind counts only what fm prove --docs reads: skip history files (fmdocs' changelog rule), diff a task's start to its own newest id-prefixed commit instead of HEAD, and recompute the cached rollup when a rule changes; MASTER and CHANGELOG say it
```
