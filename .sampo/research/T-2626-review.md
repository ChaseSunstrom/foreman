**Verdict: changes needed.** The floor can be met by a typed line plus any finished task, and it is only enforced after the generation has already passed its own sweep.

## lens: intent
- HIGH — plugin/lib/fmmoonshot.py:152-167 (floor), :25 (_ADV), :136 (_tier) — The floor is satisfied by typing text and pointing at any done task. Proof: add `### M-99 · x` with `Tier: extreme`, with no `fm genesis moonshot rate` run, since `_tier` falls back to the author's tier. Write `Advanced: M-99 full (T-0001)` in gen-3/mission-moonshot.md, where T-0001 is any unrelated done task. Once gen-4 exists, `floor()` returns `[]`. Nothing ties the task to M-99, the claimed stage to the catalogue's `Stage:` line, or a kill stage to a `Kill:` line. The `Kill:` check (:137) passes on the word "viable", which "not viable" also contains. Fix: require the done task to be named in that moonshot's `Evidence:` line, or its brief to cite the M-NN. Require the catalogue stage to be at or past the claimed one. Count a big moonshot only if it has a reviewer tier from the store. Require the kill result to cite a task or evidence. — high
- MEDIUM — plugin/lib/fmmoonshot.py:152 (floor), plugin/lib/fmgenesis.py:3767 (sweep) — The floor applies only to `k < max(gens)`, so gen-N can pass its own sweep, select and review with no big stage. It then turns red when gen-(N+1) is seeded. That makes gen-N+1's sweep fail on gen-N's work, which can only be fixed by backfilling a finished generation. This still assumes a floor checked afterwards, not inside the generation, which is what the steer asked to avoid. Fix: have `sweep(p, n)` require the floor for `n` itself. Keep the retroactive check as a backstop. — high
- LOW — plugin/lib/fmmoonshot.py:105 — The mix is counted on the author's tier only. The summary and page show reviewer counts, but nothing enforces them, so a reviewer-side overflow passes. An author who over-labels is refused even when the reviewer's real mix fits. Fix: count `_tier(r)` too, or say author-only in the docs. — medium
- LOW — plugin/lib/fmmoonshot.py:205, CHANGELOG.md:9, MASTER.md:21 — The docs say "each demotion is logged". The ledger event holds counts only, and the per-item record is in the store. Fix: add `demotions: [{id, from, to, why}]` to the event data. — high

## lens: adversary
- LOW — plugin/lib/fmmoonshot.py:52 — `_key` hashes Tier, Domain and the other defining lines, so changing one word gives a new key. The block is unrated again and re-rolled until the strongest model says "extreme". The "first rating stands" rule holds only for identical text. Fix: also key the store by M-NN and keep the first rating per id. — medium

## lens: edge
- LOW — plugin/lib/fmmoonshot.py:210-243 — The climb offers a big moonshot only if its needs are met. If every open big one has unbuilt needs, the climb contains no big stage. The floor then has no honest path and pushes toward a typed line. Fix: let a built unblocker for an open big moonshot count toward the floor. — medium
- Today's tower is fine. gen-3 has no `moonshot.md`, and `floor()` iterates `3 <= k < 3`, so it is empty. Once gen-4 exists, gen-3 goes red, and that is by design. gen-3's seed predates the campaign lines, so it gets only the hint at fmgenesis.py:856.

## lens: operator
- LOW — plugin/lib/fmmoonshot.py:129-133 — `fmsecond._words(b.title)` is recomputed inside a loop of moonshots times briefs. At 100 moonshots and about 2,400 archived briefs that is about 240k tokenizations per `fm genesis check`, `status`, `export` and `sweep`. Fix: precompute the brief word sets once. — high
- `rate` sends at most 25 blocks per call and does not say how many remain. Fully rating 100 moonshots takes 4 calls to the strongest model, which is modest.

## lens: maintainer
- MEDIUM — plugin/tests/test_moonshot.py:437-451 — The floor test covers only red cases (running, task not done, dropped). No test shows the floor going green with a done task, and none has a typed-line bypass case. Fix: add the green case and a test that rejects an unrelated done task. — high

## lens: design
- LOW — plugin/site/genesis/genesis.js:694 — The first `th` is empty, and 100 rows × 8 columns have no caption or scroll cue. Fix: give the first `th` a label such as "ID". — medium

## Acceptance criteria
- Seed carries the campaign: met by the code (`seed_lines`, fmmoonshot.py:256-284). I did not run the tests.
- `fm genesis check` refusals: met by the code, except that the reviewer-tier rule only matches the word "reviewer" in the Tier line.
- `moonshot rate`: mostly met. Demotions are logged as counts only.
- Climb and floor: met as written, but the floor is weak.
- Export and page: met by the code.
- Suites pass: not verifiable here.

## Implicit decisions
- Floor starts at generation 3 (`CAMPAIGN_FROM`).
- Duplicate threshold is 70% of title words.
- Rating batch is 25 and uses `REVIEW_MODELS[-1]`.
- Mix is counted on the author's tier.
- The store is keyed by a content hash.

## Not checked
I ran no tests and took no screenshots. I did not check the guard protection on `genesis-moonshot-rate.json`.

**Noticed:** none
