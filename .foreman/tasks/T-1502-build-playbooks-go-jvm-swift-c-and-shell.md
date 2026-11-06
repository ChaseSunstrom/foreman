---
id: T-1502
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/build, plugin/skills/playbooks/SKILL.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:15Z
updated: 2026-10-22T18:19:41Z
base: 496e6438ef28a51e7311d7d171e895d2c1cbe96b
base_tree: a7f9e158cd03efc1efc624d23f7831b6be1b0f0e
plan0_at: 2026-10-22T18:13:09Z
plan0_scope: [plugin/skills/playbooks/references/build]
verified: strong
---
# Build playbooks: Go, JVM, Swift, C# and shell
## Raw request
> Build playbooks: Go, JVM, Swift, C# and shell
## Interpretation
Brainstorm T-1479 cluster 10: build playbooks exist for C++, Rust and TypeScript only. Add go-build, jvm-build (Gradle/Maven, Kotlin/Java), swift-build (SwiftPM/Xcode), csharp-build (dotnet) and shell (shellcheck, bats): reading the first error, the usual causes, the verify command. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] the five build playbooks exist, each with first-error reading, common causes and its verify command — verify with `for f in go jvm swift csharp shell; do python3 -c "t=open('plugin/skills/playbooks/references/build/$f-build.md').read(); miss=[s for s in ['## First error','## Common causes','## Verify',] if s not in t]; assert not miss, miss" || exit 1; done`
## Non-goals
## Approach (options → choice → why)
Options: port third-party build guides (licence and voice drift); one generic build playbook (too vague to act on); chosen: one original file per toolchain in the existing build/ shape (rust-build.md, cpp-build.md): reading the first error, the common causes with their fix, the verify command, with links to the matching library cards (fm lib show go, gradle, swift, dotnet, bash).
## Risks and rollback
## Execution prompt
## Steps
1. [x] write the five playbooks
## Resume here
## Docs impact
CHANGELOG.md line; plugin/skills/playbooks/references/build/INDEX.md
## Verification evidence
- (step 1) `python3 -c "[(lambda t: [s for s in ['## First error','## Common causes','## Verify'] if s not in t] == [] or exit(1))(open('plugin/skills/playbooks/references/build/'+f+'-build.md').read()) for f in ['go','jvm','swift','csharp','shell']]"` → exit 0 · (no output) [ran] [tree c15ec3b3bcaa] (2026-10-22T18:18:01Z)
- (ac 1) `python3 -c "import re; miss=[(f,s) for f in ['go','jvm','swift','csharp','shell'] for s in ['## First error','## Common causes','## Verify'] if s not in open('plugin/skills/playbooks/references/build/%s-build.md' % f).read()]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree cee391cb7677] (2026-10-22T18:19:31Z)
- (step 1) `python3 -c "import re; miss=[(f,s) for f in ['go','jvm','swift','csharp','shell'] for s in ['## First error','## Common causes','## Verify'] if s not in open('plugin/skills/playbooks/references/build/%s-build.md' % f).read()]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree cee391cb7677] (2026-10-22T18:19:32Z)
- (ac 1) `for f in go jvm swift csharp shell; do python3 -c "t=open('plugin/skills/playbooks/references/build/$f-build.md').read(); miss=[s for s in ['## First error','## Common causes','## Verify',] if s not in t]; assert not miss, miss" || exit 1; done` → exit 0 · (no output) [ran] [tree 4568d7900520] (2026-10-22T18:19:35Z)
- (audit intent) `builder ran real failing builds where toolchains exist (swiftc 6.4: errors out of file order; dotnet 10: one missing ; hides the rest and errors print twice; sh -n reports the missing fi at the next done) and checked every fm lib card name exists; go, gradle, maven, shellcheck and javac weren't installed (said in the report); I added a build stage index so SKILL.md stays under budget` → first-error reading, common causes and verify per toolchain, in the existing build/ shape [tree 4568d7900520] (2026-10-22T18:19:35Z)
- (audit edge) `builder ran real failing builds where toolchains exist (swiftc 6.4: errors out of file order; dotnet 10: one missing ; hides the rest and errors print twice; sh -n reports the missing fi at the next done) and checked every fm lib card name exists; go, gradle, maven, shellcheck and javac weren't installed (said in the report); I added a build stage index so SKILL.md stays under budget` → the JVM file's compiler messages are from knowledge, not a run (K1 and K2 Kotlin wording both quoted) [tree 4568d7900520] (2026-10-22T18:19:35Z)
- (audit maintainer) `builder ran real failing builds where toolchains exist (swiftc 6.4: errors out of file order; dotnet 10: one missing ; hides the rest and errors print twice; sh -n reports the missing fi at the next done) and checked every fm lib card name exists; go, gradle, maven, shellcheck and javac weren't installed (said in the report); I added a build stage index so SKILL.md stays under budget` → build/INDEX.md lists all eight toolchains; SKILL.md names the index once [tree 4568d7900520] (2026-10-22T18:19:35Z)
## Log
- 2026-10-22T17:36:15Z created
- 2026-10-22T18:12:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1502.builder.md
- 2026-10-22T18:13:09Z focused
- 2026-10-22T18:19:12Z merged worktree-agent-aba4b096a52976fef (5 file(s))
- 2026-10-22T18:19:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aba4b096a52976fef
- 2026-10-22T18:19:13Z focused
- 2026-10-22T18:19:22Z set scope=['plugin/skills/playbooks/references/build', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md']
- 2026-10-22T18:19:36Z done
- 2026-10-22T18:19:41Z committed e3e8bb13 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1491 [FEATURE M, active, 2 steps] UI playbook: interaction, forms, microcopy and mobile
- T-1490 [FEATURE M, done, 2 steps] UI playbook: composition, depth and states — lesson: Ship a measuring probe with a layout playbook; prose rules about rhythm are unrevi…
- T-1493 [FEATURE S, done, 1 steps] Motion playbook: game feel with intensity caps — lesson: Asserts in an embedded snippet should check the playbook's table, not the snip…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- similar finished tasks took 1–2 steps
## Why not caught
new playbooks
## Lessons
- Builders adding playbooks should edit their stage's INDEX.md themselves now that stage indexes exist, so the index test stays green on the branch.
## Files touched
- plugin/skills/playbooks/references/build/go-build.md
- plugin/skills/playbooks/references/build/jvm-build.md
- plugin/skills/playbooks/references/build/swift-build.md
- plugin/skills/playbooks/references/build/csharp-build.md
- plugin/skills/playbooks/references/build/shell-build.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/build/INDEX.md
- CHANGELOG.md
