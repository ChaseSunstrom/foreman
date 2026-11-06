**Verdict: approve with nits.** I found no HIGH issues and no failure of the acceptance criteria. I had no shell, so I read the code and ran nothing. The reproducers below are reasoned, not run.

## lens: adversary
- MEDIUM — plugin/lib/fmplaybooks.py:109-121 (docstring :110-112, module doc :7-9) — the isolation is hygiene, not confinement. `HOME` is the temp dir, but a block can still read or write `~/...` by absolute path, use the network, and run any binary on PATH. There is no `RLIMIT_AS` or `RLIMIT_NPROC`. Reproducer: an unmarked block `open('~/x','w')` is executed by `fm check playbooks`. The guard sees only `fm check playbooks`, and playbooks can be written by lanes and generated drafts. — State it as "trusted like a test" in the docstring and MASTER. Optionally wrap the child in `bwrap` or `unshare -rn` when present, and add the two rlimits in `limit()`. — confidence 0.8
- LOW — fmplaybooks.py:128-131 — the claim that no process outlives the check is too strong. A block that forks and calls `os.setsid()` leaves the process group and survives `killpg`. — Soften the claim. — 0.9
- LOW — fmplaybooks.py:113-115 — `import resource` runs inside `preexec_fn`, after fork. — Import it at module top. — 0.5

Other questions on this lens:
- **Hangs.** The 20 s timeout, the stderr tempfile (no pipe) and `DEVNULL` stdin mean a block cannot hang the gate. Worst case is 20 s per block, run one after another.
- **Where it runs.** It runs only from `fm check playbooks` and the Repo test. Doctor, hooks, the default `fm check` and the guard's read-only list do not call it.

## lens: edge
- MEDIUM — plugin/lib/fmcore.py:22 — `PLUGIN_ROOT` is derived from the file path of the running `fm`. In a lane worktree, a PATH `fm` would lint the main checkout's playbooks, and `fm check playbooks ratchet` would write the main checkout's `ratchet.json`. — Tell lanes to run `python3 plugin/bin/fm check playbooks`, or add a root override. — PLAUSIBLE, 0.5
- MEDIUM — the lane base predates T-1504. Main has nine playbooks the lint never saw: ops/*, context/docs, decks-and-reports, lang/stdlib-python, release/demo-production, ui/data-viz, sound-design, scrollytelling. Three of them have python blocks (sound-design.md:43, docs.md:42, observability.md:43). Any existing playbook that main grew since the base will also exceed its recorded ceiling. — Rerun `test_playbook_check` and `fm check playbooks` on the merged tree before closing. — 0.7
- LOW — fmplaybooks.py:237 — `fm check playbooks ratchet typo` still rewrites `ratchet.json`. — Require `args.words == ["ratchet"]`. — 0.9

## lens: maintainer
- MEDIUM — fmplaybooks.py:188 with `ratchet.json` — the ratchet fails only in the full test or on an explicit run, so a lane finds out at close. The whole file is rewritten with one sorted line per path, so two lanes editing neighbouring playbooks conflict. `lang/python-patterns` and `lang/python-testing` are adjacent at `ratchet.json:348-349`. A shrink is never recorded, so a trimmed playbook can regrow to its old size unflagged. — Fail only past about 10% plus 50 tokens over the record, and let `ratchet` lower ceilings. — 0.7
- LOW — plugin/tests/test_docs.py:94-106 — an older index test enforces the same rule by substring match, while the new code uses a backtick regex, so the two will drift. — Delete the old test, or have it call `fmplaybooks.problems(run=False)`. — 0.8
- LOW — plugin/tests/test_playbook_check.py — no test covers a nested `templates/` file, exit code 1 through the CLI, `ratchet` through the CLI, or output flooding. — Add them. — 0.7

## lens: intent
- LOW — references/verify/verification-loop.md:19 (builder-added item 1) — "stop at the first that fails" is stronger than the source. The source stops only on a failed build (:32), says "fix critical ones" for types, and says nothing for lint. — Reword to "Build first and stop if it fails; then type check and lint, fixing what they report." — 0.9
- LOW — CHANGELOG.md — no entry for the new `fm check playbooks` command, which every task normally gets. — Add a line. — 0.6

## Acceptance criteria
- **Criterion 1: met, by the code and tests as written.** The lint flags an unlisted file, a dead index line, a near-duplicate and a ratchet overrun. I did not run it against the repo's own playbooks.
- **Criterion 2: met, by the code as written; not run.** The numbered-procedure, card-name and python-block checks exist.

Other answers:
- **Index check.** It accepts stage `INDEX.md` files correctly, including nested paths: `references/ui/templates/scene.html` resolves to the ui stage index.
- **Shingle check.** It is deterministic (sorted, set-based) and fast, with about 2,400 pairs on 70 files.
- **Reach.** It reads `target[:120]` correctly, matching a cut path by unique prefix. A path cut inside `/skills/playbooks/references/` is dropped and counts as unread.
- **The 41 no-run marks.** The count is right (13 + 27 + 1). They are all module-level fragments; the one real script is `type-and-colour.md:145`.
- **The 18 playbook edits.** Meaning is kept except verification-loop item 1.

## Implicit decisions
- `sys.executable` runs the blocks, not a literal `python3`.
- Tokens are chars/4, and a playbook with no record passes.
- Duplicate threshold is 0.6 Jaccard over 5-word shingles.
- Backtick-only path matching decides what an index names.

## Not checked
- Sizes in `ratchet.json` against the current files.
- Whether the 25 unmarked python-patterns and python-testing blocks pass (they only define functions).
- Windows behaviour.

**Noticed:**
- no-run python blocks are never compiled; `type-and-colour.md:145` could get `ast.parse` or a self-test.
- `fm lib show` also accepts `plugin:skill` names, which the lint reports as "no such card".
