## Verdict
Changes needed. The code works and the 22 cards I sampled are accurate. Detect signals produce false-positive suggestions, and one manifest regex can hang the background `fm map` on a hostile repo. I could not run anything (read-only tools), so none of the findings below was executed.

## intent: changes needed
**MEDIUM** `plugin/lib/fmlib.py:219-257` (ranking) with the card detect lines below
- summary: Broad or ambiguous detect signals, plus sorting by `focus`, suggest cards for repos they don't fit.
- short_summary: suggest ranks cards for repos they don't fit
- failure_scenario:
  - `cloud/aws-iam.md:6` has `file:*.tf`. A GCP or Azure Terraform repo gets `aws-iam [file:*.tf]`, as the Terraform fixture itself does.
  - `data/timescaledb.md:6` lists `dep:psycopg`, `dep:pg` and `file:*.sql`. A plain Postgres repo with `psycopg` and one `.sql` file scores 5 on both `timescaledb` and `postgres`. Focus is 5/7 against 5/11, so `timescaledb` ranks above `postgres`.
  - `testing/test-sharding.md:6`, `tools/github-cli.md:6` and `domains/cron-jobs.md:6` match `.github/workflows/*.yml`, so every GitHub Actions repo gets all three.
  - `tools/node-inspector.md:6` matches `file:package.json`, so every Node repo gets it.
  - `lang/c.md:6` matches `file:Makefile`, so a Go or Python repo with a Makefile gets the C card.
  - `ml/cuda.md:6` matches `file:CMakeLists.txt`, so any CMake repo gets CUDA.
  - `cloud/cloudflare-workers.md:6` matches `dep:hono`, which also runs on Node.
  - `data/parquet-arrow.md:6` matches `dep:arrow`, which is PyPI's date library.
  - `.h` files push C++ repos onto the C card.
- reproducer: commit a `main.tf` containing `provider "google" {}` and run `fm lib suggest`. For the other cases, use a Go repo with a Makefile, or a Python repo using `psycopg` and a `.sql` file.
- fix:
  - Drop the single-signal generic cards (`file:Makefile`, `file:package.json`, `.github/workflows/*`, `file:*.tf` on aws-iam).
  - Require a `dep:` or specific file signal for cards that sit above a base language card.
  - Score a card by its best signal rather than the sum over aliases.
  - Add a lint rule rejecting these generic signals.
- category: false-positive-ranking, verdict: CONFIRMED (by reading the code and cards)

**LOW** `plugin/skills/library/SKILL.md:52` vs `plugin/lib/fmlib.py:18,99-102`
- The doc says 1,200-4,000 chars, 2-5 Verify bullets, a summary of 160 chars or fewer, and 4-7 Review checks. The lint allows 1,000-4,500 chars and checks none of the rest, so a violating card passes `fm lib check`. Fix: enforce the documented limits or relax the doc.

## adversary: changes needed
**MEDIUM** `plugin/lib/fmlib.py:163` (the `go.mod` regex), also `:178` (Package.swift)
- summary: `[\w.-]+\.[\w.-]+/` is ambiguous and backtracks quadratically.
- short_summary: go.mod regex ReDoS in background fm map
- failure_scenario:
  - A cloned repo commits a `go.mod` made of one 400KB line `a.a.a.…` with no `/`.
  - `fm map` runs this regex in a detached process. `compact()` respawns it on every SessionStart because the map never lands (`fmmap.py:188-192`).
  - Each session leaves an orphan process spinning on the CPU. `fm check` also calls `fmmap.load` in the foreground and hangs.
  - Package.swift has the same risk: `[^)]*?` after each `.package(` is quadratic over many unclosed `.package(` calls.
- reproducer: `python3 -c "open('go.mod','w').write('a.'*200000)"`, commit it, then run `fm map --json`.
- fix: use `[\w-]+(?:\.[\w-]+)+/[\w./-]+`, read at most the first ~64KB of each manifest, and skip lines over ~1000 chars. Not run; the quadratic backtracking is from reading the pattern.
- category: regex-dos, verdict: PLAUSIBLE

**LOW** `plugin/lib/fmlib.py:360,391-393`
- summary: A plugin skill's `name` and `description` are printed raw (`c.fit` does not strip control characters).
- short_summary: plugin skill text printed without c.plain
- failure_scenario: an installed plugin's SKILL.md description containing ESC sequences retitles or moves the terminal during `fm lib search` or `show`.
- fix: wrap the text in `c.plain`.
- category: terminal-escape

## edge: changes needed
**MEDIUM** `plugin/lib/fmlib.py:231-233` and `plugin/lib/fmmap.py:67,88`
- summary: `match()` runs `fnmatch` per card per file, and `build()` passes every tracked file with no cap.
- short_summary: map build now scans ~1000 cards x all files
- failure_scenario:
  - About 190 cards have glob signals. Roughly 200 basename globs and 90 path globs, each tested against every basename or file, come to about 1-2M `fnmatch` calls on a 7k-file repo.
  - The comment at `fmmap.py:178` already puts the build at 1.5 s on that repo.
  - `fmmap.load` is synchronous in `fm check` and other commands (`fmcli.py:1698`, `3218`, `3411`), so every HEAD move gets slower.
  - SessionStart itself is unaffected: `compact()` only reads `map.json` and `fmlib` is imported only in `build`.
- fix: look up wildcard-free paths in a set, compile each pattern once, cap files to 20000 as `_files` does, and record a before/after timing.
- category: performance, verdict: PLAUSIBLE (no measurement recorded)

**LOW** `plugin/lib/fmmap.py:145,183`
- The map is keyed only on project HEAD and `VERSION`. Cards added after a map was built never reach `lib` until HEAD moves, and more cards are still landing. Fix: store a card-count or newest-mtime fingerprint in the map and compare it.

**LOW** `plugin/lib/fmlib.py:307-317,352-356`
- `fm lib show X --section tests` (a typo) silently prints only the summary line. Fix: error on a wanted section that matches nothing.

**LOW** `plugin/lib/fmlib.py:211`
- Only the first 60 manifests, in alphabetical order, are read. Dependencies from later directories of a large monorepo are dropped.

## operator: ok
- README and the playbooks pointer match the code.
- `check_self_docs` (`fmdoctor.py:678-680`) now scans all card files. I found no backticked `fm <word>` spans in the cards that would fail it.
- Not verified: the doctor's `DESCRIPTIONS_MAX` of 6000 chars with the new `library` description, and the footprint budgets. They need `fm doctor`.

## maintainer: changes needed
**LOW** `plugin/tests/test_library.py:49-57`
- The fixture test asserts only that the expected cards appear in the top 10. Nothing asserts a card is absent, so every false positive above passes (the Terraform fixture already yields `aws-iam`). Fix: add negative cases, such as a Go repo with a Makefile not getting `c`, and a `psycopg` repo ranking `postgres` above `timescaledb`.

**LOW** `plugin/lib/fmlib.py:95,189`
- `open(path).read()` leaks a handle, and each card is read twice (`cards()` then `lint`).
- The `subprocess` call to git duplicates `c._git` (`fmcore.py:2586`).

**LOW** `plugin/skills/library/cards/security/jwt.md:6`
- `dep:jsonwebtoken-rs` is not a crate name (the crate is `jsonwebtoken`). Fix: remove it.

## Acceptance criteria
- **`fm lib check` passes on 400+ cards with the lint rules:** not verifiable here. The code enforces frontmatter, sections, size and unique names. The directory has about 1,000 cards.
- **`fm lib suggest` is right for the fixtures, and search finds plugin skills:** not verifiable here. Recall is tested and the code looks right, but precision is not tested, and the FPs above show it is weak.
- **SessionStart names the cards in one line; doctor green:** the hook only reads `map.json`, and the test asserts `cards: fastapi`. The doctor result was not run.

## Implicit decisions
- Cards with `detect: []` (all `go-context`-style practice cards) are searchable but never suggested.
- A `VERSION` bump to 4 means each project's first session after upgrade has no map line.
- Signal weights are dep 3, file 2, ext 1, with +2 when a language is 20% or more of the files.
- Suggest skips non-language cards whose only signals are language extensions, so `python/asyncio` is never suggested.
- Manifest dependency names are lowercased with `_` turned into `-`.

## Not checked
Roughly 980 of the cards, `fm doctor` and the test run, and the pre-audit "secret-looking" hits. I dismissed those: the only key-like string is AWS's documented `[REDACTED]` in `cards/security/gitleaks.md`.

**Noticed:**
- `SKILL.md:17` and the live-cloud Verify commands (`cards/cloud/aws-iam.md:12-15`, `cards/data/postgres-locking.md:12`, `cards/infra/kubernetes.md:14-16`): turning these into `--ac` criteria would have `fm check` run `aws`, `kubectl` and `psql` against ambient credentials. Worth a guard or doc note.
- `cards/web/nextjs-app-router.md:6`: detect misses `src/app/layout.{js,jsx}` and monorepo `apps/*/app/layout.*`.
