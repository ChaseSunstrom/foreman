**Verdict:** changes needed. Finding 1 is a MEDIUM that breaks the "seed N output passes step's seed-row rules (<= 8 rows)" MUST. I read the code and did not run the tests.

## lens: intent
- MEDIUM — plugin/lib/fmgenesis.py:310,333 — The critique asks are copied into the seed without removing table lines. `carried` strips lines starting with `|` (:318), but `asks` does not. `step` counts every `^| N | mission-x.md |…|` row with `ROW.findall` over the whole seed (:240). A critique's "What the next Seed should change" section often proposes Mission rows, so those rows add to the table. With 8 real rows plus 3 proposed ones, `step` returns `fatal` ("lists 11 Missions"). The tests never put a table in a critique. — Filter `|` lines out of each ask body the way `carried` does, and have `seed()` assert `len(ROW.findall(out)) == len(table) <= 8` before the `put`. — CONFIRMED
- LOW — plugin/lib/fmgenesis.py:231 — The bar for gen N is gen N-1's closed set even when gen N-1 was reverted. The text base is the kept ancestor, but the score to beat is the lower, reverted one. Example: gen-0 closes 10, gen-1 closes 8 and reverts, gen-2 closes 9 and is kept, though it scored below the text it was built on. The brief says "gen N-1", so this matches the request. Whether it was meant that way is a question for the user. — Compare against the base's lines (`_base(lineage, n-1)`), or record this choice in lineage.md. — PLAUSIBLE
- LOW — plugin/lib/fmgenesis.py:314 — The seed's Exam section is hardcoded to `"foreman"`, while `select` takes `--agent`. With any other agent the seed says "No graded line yet." — Pass the agent through to `seed`. — CONFIRMED

## lens: adversary
- No separate findings. Finding 1 also lets model-written critique text change what the seed's table parses as.

## lens: edge
- MEDIUM — plugin/lib/fmexam.py:790 — `gen=fmgenesis.current(p)` is read when the line is graded, not when the agent answered. Answers persist per run and agent (:675, :695), and `fm exam grade` can be rerun at any time (test_exam does this). Regrading gen-1's answers after `gen-2/seed.md` exists files a line as gen 2, with gen 1's closed set. `select 2` then sees a tie with no real gen-2 exam and writes a false "reverted" verdict and decision. — Stamp the generation at `fm exam run`, or take `--gen` and default to the stamp. — PLAUSIBLE
- LOW — plugin/lib/fmgenesis.py:256-264 — `select` reads `lineage.md` and then calls `put`, which locks only the write. Two concurrent `select` calls for different N both read the old file, and the second write drops the first section. The `seed` exists-check (:282) has the same gap. — Do the read and write inside `c.lock(p.dir)`. — PLAUSIBLE
- LOW — plugin/lib/fmgenesis.py:289,318 — If gen-1 reverts, the base is `gen-0` and `text = gen0`. Every later seed then carries all of gen-0's sections, since none are in `MADE`. That is the user's whole prompt, repeated in each seed. — Carry only seed-shaped sections when the base is gen-0, or none. — PLAUSIBLE

## lens: operator
- No model calls, no new hooks. The cost is one `exam.jsonl` parse and one directory listing per call, which is negligible. The `fm genesis select` entries in MASTER.md and CHANGELOG.md are present. The pre-audit "large file" and hotspot flags are dismissed: MASTER.md changed by one line and fmcli.py by three.

## lens: maintainer
- LOW — plugin/tests/test_genesis.py:518 — Nothing tests a critique containing a table (finding 1), the `--agent` flag, a revert whose base is gen-0, or a regrade after a newer seed exists.

## Acceptance criteria
- Grade lines carry `closed` and `gen`: met in code (fmexam.py:772-790, test_exam). Tests not run.
- `select` behaviours: met. Fewer, tie and reopened revert; +2 keeps; +1 on one line asks a rerun and writes nothing; no parent is the baseline; the lineage section and decision are written (:241-267).
- `seed`: partly met. Rows are at most 8 in the tests, but not when a critique carries table rows (finding 1). Empty cells and not-yet items are listed.
- MASTER.md and CHANGELOG.md name `select`: met (counts 1 and 2).

## Implicit decisions
- The generation is read from the newest seed file.
- Multiple graded lines are combined by intersecting their closed sets, and cost is the mean.
- `seed` refuses N<2 and refuses to overwrite.
- Mission slugs come from area headings.
- A ratchet breach is checked before the margin.
- The cap overflow is named in the seed, not dropped.

## Not checked
The test run, and the MASTER.md hunk, which is not in the diff.

**Noticed:** `select 0` writes a meaningless `## gen-0` lineage section and decision. A vacuously closed scenario (nothing keyed, no errors) counts toward selection. Either could be its own task.
