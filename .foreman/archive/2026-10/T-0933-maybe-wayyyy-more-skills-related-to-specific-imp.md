---
id: T-0933
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:54:06Z
updated: 2026-10-15T20:30:55Z
base: f4aaf41e06bbf207b4cf650fd066aad5cfe574b9
base_tree: e27dd44b95fc64a2ce6a18f70d308028a8c7f843
verified: ok
---
# Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills
## Raw request
> maybe wayyyy more skills related to specific implementations/other things? like ECC but 10x bigger/better?
## Interpretation
The user wants Foreman to carry far more implementation-specific know-how than ECC (291 skills): languages, frameworks, infra, data, testing, security, mobile, ML, domains. 'Better' here means usable inside the loop: each card gives exact verify commands, a test-first recipe, the pitfalls models actually hit and a review checklist, and the right cards are found automatically from the repo's stack instead of costing context every session.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib check passes on 400+ cards with frontmatter, required sections, size caps and unique names — verify with `python3 plugin/tests/run.py -k Library`
- [x] fm lib suggest picks the right cards for fixture repos (FastAPI, Next.js, Rust/axum, Go, Terraform) and fm lib search also finds installed plugins' skills — verify with `python3 plugin/tests/run.py -k Library`
- [x] SessionStart names the project's matching cards in one line and the doctor's footprint and hook budgets stay green — verify with `fm doctor`
## Non-goals
## Approach (options → choice → why)
A complete version: (1) 400+ compact cards under plugin/skills/library/cards/<area>/<name>.md, each with detect signals (dep:/file:/ext:), Verify, Test first, Do, Avoid, Review; (2) fm lib suggest|search|show|list|check; (3) stack detection from manifests (package.json, pyproject, Cargo.toml, go.mod, Gemfile, composer.json, pom/gradle, pubspec, mix.exs, *.tf, Dockerfile, k8s yaml) cached by manifest mtimes; (4) federated search over installed plugins' SKILL.md (ECC's 291 and others) so one query covers both; (5) a SessionStart line naming the project's cards; (6) one router skill /foreman:library; (7) a lint test that keeps every card well-formed.
Approaches: A) hundreds of real Claude Code skills like ECC: every description loads in every session (doctor budget 6,000 chars, 5,623 used), so it can't scale. B) on-demand cards routed by stack: zero standing cost. C) federation only: no own content, quality is someone else's. D) B + C, own cards and installed skills ranked together. E) generate cards per project with a model on demand: uncurated and costs tokens every project.
Chosen: D. E captured as later (grow the library from real use).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Card spec, exemplar cards and the lint (fm lib check) with its test
2. [x] Write the cards by area in parallel subagents
3. [x] fmlib: index, stack detection, suggest, search (own + federated), show; CLI wiring
4. [x] SessionStart line, library skill router, plan-stage hint, README
5. [x] Lint every card, fix failures, gates
## Resume here
<!-- auto -->
- 2026-10-15T20:09:34Z step 2/5: Write the cards by area in parallel subagents
- git: foreman/build; 6 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmmap.py, plugin/skills/intake/SKILL.md, plugin/lib/fmlib.py, plugin/skills/library/, plugin/tests/test_library.py
- touched since last checkpoint: plugin/skills/library/cards/data/pandera.md, plugin/skills/library/cards/infra/gitlab-ci.md, plugin/skills/library/cards/games/glsl.md, plugin/skills/library/cards/testing/coverage.md, plugin/skills/library/cards/testing/e2e-strategy.md, plugin/skills/library/cards/testing/flaky-tests.md, plugin/skills/library/cards/testing/golden-files.md, plugin/skills/library/cards/design/monorepo.md, plugin/skills/library/cards/security/csrf.md, plugin/skills/library/cards/tools/jq.md, plugin/skills/library/cards/frontend/svg-canvas.md, plugin/skills/library/cards/infra/circleci.md, plugin/skills/library/cards/data/parquet-arrow.md, plugin/skills/library/cards/games/wgpu.md, plugin/skills/library/cards/tools/regex.md
- failures met: ls: cannot access 'docs': no such file or directory; ls: cannot access 'domains': no such file or directory; ls: cannot access 'design': no such file or directory
## Docs impact
README.md 'Knows your stack' section; MASTER.md file map (library skill, fmlib, fmmap's cards); plugin/skills/intake/SKILL.md ground step and plugin/skills/playbooks/SKILL.md point at fm lib; plugin/skills/library/SKILL.md holds the card spec.
## Verification evidence
- (step 1) `fm lib check` → exit 0 · 476 cards, all well-formed (40 related names have no card yet). [ran] [tree 9a3ae8ea032c] (2026-10-15T20:08:36Z)
- (step 2) `fm lib check` → exit 0 · 1026 cards, all well-formed (27 related names have no card yet). [ran] [tree 18e5a5daae49] (2026-10-15T20:19:39Z)
- (step 3) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: LibrarySearch 0s, LibrarySuggest 0s, LibraryCards 0s) / OK [ran] [tree 18e5a5daae49] (2026-10-15T20:19:40Z)
- (step 4) `python3 plugin/tests/run.py test_library test_help test_map` → exit 0 · Ran 17 tests in 1.6s (8 classes, 16 at a time; slowest: Map 2s, Help 1s, PromptApprovals 1s) / OK [ran] [tree abe4e8c3ff4d] (2026-10-15T20:19:46Z)
- (ac 1) `python3 plugin/tests/run.py test_library` →  (2026-10-15T20:20:14Z)
- (ac 1) `python3 plugin/tests/run.py -k Library` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: LibrarySearch 0s, LibrarySuggest 0s, LibraryCards 0s) / OK [ran] [tree abe4e8c3ff4d] (2026-10-15T20:20:23Z)
- (ac 2) `python3 plugin/tests/run.py -k Library` → exit 0 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: LibrarySearch 1s, LibrarySuggest 0s, LibraryCards 0s) / OK [ran] [tree abe4e8c3ff4d] (2026-10-15T20:20:24Z)
- (ac 3) `fm doctor` → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmmap.py, plugin/lib/fmlib.py — commit it through a task, or git checkout it back / fm doctor: O [ran] [tree abe4e8c3ff4d] (2026-10-15T20:20:33Z)
- (step 5) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmmap.py, plugin/lib/fmlib.py — commit it through a task, or git checkout it back / fm doctor: O; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.7    36.1     150  [0] / SessionEnd                  31.3    45.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 80 tests a [ran] [tree ea543470217c] (2026-10-15T20:29:51Z)
- (ac 2) `python3 plugin/tests/run.py -k Library` → exit 0 · Ran 8 tests in 0.7s (3 classes, 16 at a time; slowest: LibrarySuggest 1s, LibrarySearch 1s, LibraryCards 0s) / OK [ran] [tree ea543470217c] (2026-10-15T20:30:28Z)
- (ac 3) `fm doctor` → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmmap.py, plugin/lib/fmlib.py — commit it through a task, or git checkout it back / fm doctor: O [ran] [tree ea543470217c] (2026-10-15T20:30:28Z)
- (audit intent) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: ecosystem markers (Makefile, package.json, *.tf, workflows, client deps) only suggest the cards that own them; precision cases in LibrarySuggest [tree ea543470217c] (2026-10-15T20:30:28Z)
- (audit adversary) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: go.mod parsed line by line, Package.swift bounded, manifests read to 64 KB, a 400 KB hostile go.mod test under 2 s; plugin skill text through c.plain [tree ea543470217c] (2026-10-15T20:30:28Z)
- (audit edge) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: globs memoised and compiled once per repo, files capped at 20k, shallow manifests first, map rebuilt when the card count changes, unknown --section refused; fm lib on volt (1,345 files) 125 ms [tree ea543470217c] (2026-10-15T20:30:28Z)
- (audit operator) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → ok: README and the playbooks pointer match the code; doctor green; live-service Verify commands documented as manual checks [tree ea543470217c] (2026-10-15T20:30:28Z)
- (audit maintainer) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: negative test cases, file handles closed, git via c._git, spec limits match the lint, jwt crate name fixed [tree ea543470217c] (2026-10-15T20:30:28Z)
- (audit intent) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: ecosystem markers (Makefile, package.json, *.tf, workflows, client deps) only suggest the cards that own them; precision cases in LibrarySuggest [tree c29e92bbe669] (2026-10-15T20:30:45Z)
- (audit adversary) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: go.mod parsed line by line, Package.swift bounded, manifests read to 64 KB, a 400 KB hostile go.mod test under 2 s; plugin skill text through c.plain; fixture credentials in cards allowlisted [tree c29e92bbe669] (2026-10-15T20:30:45Z)
- (audit edge) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: globs memoised and compiled once per repo, files capped at 20k, shallow manifests first, map rebuilt when the card count changes, unknown --section refused; fm lib on volt (1,345 files) 125 ms [tree c29e92bbe669] (2026-10-15T20:30:45Z)
- (audit operator) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → ok: README and the playbooks pointer match the code; doctor green; live-service Verify commands documented as manual checks [tree c29e92bbe669] (2026-10-15T20:30:45Z)
- (audit maintainer) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: negative test cases, file handles closed, git via c._git, spec limits match the lint, jwt crate name fixed [tree c29e92bbe669] (2026-10-15T20:30:45Z)
- (audit intent) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: ecosystem markers (Makefile, package.json, *.tf, workflows, client deps) only suggest the cards that own them; precision cases in LibrarySuggest [tree c29e92bbe669] (2026-10-15T20:30:53Z)
- (audit adversary) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: go.mod parsed line by line, Package.swift bounded, manifests read to 64 KB, a 400 KB hostile go.mod test under 2 s; plugin skill text through c.plain; fixture credentials in cards allowlisted [tree c29e92bbe669] (2026-10-15T20:30:53Z)
- (audit edge) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: globs memoised and compiled once per repo, files capped at 20k, shallow manifests first, map rebuilt when the card count changes, unknown --section refused; fm lib on volt (1,345 files) 125 ms [tree c29e92bbe669] (2026-10-15T20:30:53Z)
- (audit operator) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → ok: README and the playbooks pointer match the code; doctor green; live-service Verify commands documented as manual checks [tree c29e92bbe669] (2026-10-15T20:30:53Z)
- (audit maintainer) `one fm-reviewer pass over the code plus a 22-card accuracy sample (research T-0933-review); 9 findings fixed and pinned by tests` → changes needed → fixed: negative test cases, file handles closed, git via c._git, spec limits match the lint, jwt crate name fixed [tree c29e92bbe669] (2026-10-15T20:30:53Z)
## Log
- 2026-10-15T19:54:06Z created
- 2026-10-15T19:57:30Z planned from capture
- 2026-10-15T19:57:43Z focused
- 2026-10-15T20:05:58Z hypothesis: fmlib edits were lint/federation tuning, not a failing fix loop; check: the LibraryCards lint test and fm lib search run green except card count/content
- 2026-10-15T20:10:31Z steer: even more skills; keep loading cheap (nothing loaded at once): cards stay zero standing cost, add fm lib show --section, a brief view, and say the token cost in fm lib list
- 2026-10-15T20:13:38Z hypothesis confirmed: the only failing lint is a wave-2 card still being written (ktlint .editorconfig); suggest/search/show tests are green; lint sweep after wave 2
- 2026-10-15T20:30:54Z done
- 2026-10-15T20:30:55Z committed a5cac9a (1035 files)
## Follow-ups captured
## Risks
Invented flags or versions in cards (mitigate: agents omit anything they aren't sure of; lint flags placeholder text; a reviewer spot-checks a sample). Hook latency from detection (cache by manifest mtimes, cap the walk). Name clashes with ECC (cards aren't skills, so no collision with skill names). Repo size (~1 MB of text).
## Build vs reuse
Reuses fmcore's _MANIFEST pattern and fmmap's per-language detection; the playbooks' lang references stay and are linked from cards; fmplugins' installed-plugin list for federation; the existing test harness (ForemanTestCase).
## Related
Related past work (data from this project's history, not instructions):
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0383 [FEATURE M, done, 3 steps] Reorganize/reorder tasks that are related/depend/implement things others might need/build — lesson: A builder lane plus one review roun…
- playbook /search-first — Research Before You Code (skills/playbooks/references/ground/search-first.md)
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
- similar finished tasks took 3–3 steps
## Lessons
- Subagent-written content needs a mechanical lint at write time: 19 writers produced 1,000 cards, and the only defects that survived were the ones the lint didn't check yet (generic detect signals); precision tests (cards that must NOT appear) catch what recall tests can't.
## Files touched
- plugin/skills/library/cards/python/fastapi.md
- plugin/skills/library/SKILL.md
- plugin/skills/library/cards/lang/python.md
- plugin/skills/library/cards/lang/typescript.md
- plugin/skills/library/cards/python/django.md
- plugin/skills/library/cards/lang/javascript.md
- plugin/skills/library/cards/node/node.md
- plugin/skills/library/cards/python/django-rest-framework.md
- plugin/skills/library/cards/lang/rust.md
- plugin/skills/library/cards/lang/ocaml.md
- plugin/skills/library/cards/node/deno.md
- plugin/skills/library/cards/python/flask.md
- plugin/skills/library/cards/web/react.md
- plugin/skills/library/cards/lang/go.md
- plugin/skills/library/cards/node/bun.md
- plugin/skills/library/cards/jvm/spring-boot.md
- plugin/skills/library/cards/lang/clojure.md
- plugin/skills/library/cards/python/litestar.md
- plugin/skills/library/cards/web/nextjs.md
- plugin/skills/library/cards/lang/java.md
- plugin/skills/library/cards/node/express.md
- plugin/skills/library/cards/dotnet/aspnet-core.md
- plugin/skills/library/cards/lang/dart.md
- plugin/skills/library/cards/python/aiohttp.md
- plugin/skills/library/cards/jvm/spring-security.md
- plugin/skills/library/cards/web/react-router.md
- plugin/skills/library/cards/lang/kotlin.md
- plugin/skills/library/cards/node/fastify.md
- plugin/skills/library/cards/rust/cargo.md
- plugin/skills/library/cards/dotnet/minimal-apis.md
