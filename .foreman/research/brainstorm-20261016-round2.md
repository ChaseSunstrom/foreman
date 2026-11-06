# Round 2 catalogue: brainstorm-20261016-051317 (218 ideas, 38 clusters)

Format per cluster: ideas, grounding (code or fm command), Status (queued / done / partial / new / false), Score (value 1-5, effort S/M/L, risk), Decision.
Ideas are quoted as short titles; "(x2)" = the same idea phrased twice or more across lenses/rounds.
Grounding was by grep and reads of plugin/lib/*.py, CHANGELOG.md, release.py and mods/foreman-ui. Paths are under ~/.claude/foreman/.

## C1 Registry self-registration (conflict-free shared lists)
Ideas: append-only registry fragments; help tiers/verb registry from per-verb metadata; HELP_TIERS conflicts self-resolving; verbs self-register from drop-ins; split HELP_TIERS into per-verb files; replace HELP_TIERS hand-edits; append-only directories; registry edit-free auto-collect; split registries into per-feature drop-ins; generate HELP_TIERS from per-command files.
Grounding: T-1144 done. CHANGELOG.md:4; plugin/lib/fmcli.py:4361 (HELP_TIERS built at registration, filled at :5543 from `add(..., tier=)`, e.g. :4915).
Status: queued (T-1144, done). Decision: n/a.

## C2 Builder adversarial self-review
Ideas: adversarial self-check before "done" (x3); self-check receipt; self-adversary pass; self-check gate with pre-return checklist.
Grounding: T-1147 done (CHANGELOG.md:5). The contract is plugin/lib/fmlanes.py:135 CONTRACT. A hard "receipt" gate is not enforced, only a Self-review section requested.
Status: queued (T-1147, done). Decision: n/a.

## C3 Builder cwd and lease path normalisation
Ideas: normalise builder cwd and paths (x2); resolve builder paths against worktree root; normalise lease paths to repo root; pin builder cwd and lease paths; resolve cwd to worktree root for every path argument.
Grounding: T-1148 done (CHANGELOG.md:6). fm edit/fm sym already relpath against p.root (fmedit.py:67, fminstr.py:111).
Status: queued (T-1148, done). Decision: n/a.

## C4 Brief index and hot-directory hygiene
Ideas: index briefs so no command parses all (x3); sidecar index of brief headers; stat-keyed frontmatter sidecar; cached parsed brief index; cap lane state parsing with a brief index; archive closed briefs out of the hot directory.
Grounding: T-1140 done (hooks parse only active/verifying briefs, CHANGELOG.md:11). In-process stat-keyed memo T-1082 (fmcore.py:1535-1551). `fm tidy` already archives done tasks. Missing: a cross-process sidecar; cold `fm next` takes about 1.7 s, `fm queue` 0.8 s on 1069 briefs.
Status: partial. Score: value 2, effort M, risk med (stale index bugs). Decision: skip: hooks (the hot path) are already fast; CLI cold start under 2 s.

## C5 Verify command check at add
Ideas: check a verify command when added (x3); dry-run every verify command when added; lint verify commands when added/created (x2); verify-command doctor across the open queue.
Grounding: T-1145 queued. `_lint_verify` (fmcli.py:825) and `lint_verify` (fmcore.py:3147) exist; the queue-wide doctor is part of T-1145's scope.
Status: queued (T-1145). Decision: n/a.

## C6 Guard "why / try"
Ideas: ask the guard would-this-run (x2); `fm guard why` (x4 phrasings); explain a guard decision from CLI/one command; guard what-if playground in pane (wild); interactive guard playground in web UI (wild).
Grounding: T-1146 queued. Today `fm explain block` shows only the last block (CHANGELOG.md:435, fmrecall.py:868). No `fm guard` verb.
Status: queued (T-1146). Decision: n/a (the pane/web playground wilds are skip: pane UI work for a debug tool).

## C7 Builder contract single source / environment contract
Ideas: wrap builders in an environment contract.
Grounding: T-1151 queued (contract is one string, fmlanes.py:135, plus agent file). T-1149 (fm check names files changed during the run) is also queued.
Status: queued (T-1151). Decision: n/a.

## C8 Conflict-history hot spots, forecast and auto-resolve
Ideas: detect shared-registry hot spots from merge history (x2); auto-split shared hot-spot files by a conflict-history report; why-did-the-last-merge-conflict auto-resolver (wild); pre-merge conflict forecast from lane touch-sets (wild).
Grounding: touch-sets are already claimed (T-1068, fmlanes.py:420 preclaim; fmbus lease conflict fmbus.py:506); `_conflict_brief` writes what clashed on a conflicted merge (fmlanes.py:580). `fm map` hotspots come from fix/revert commits, not merge conflicts (fmmap.py:152). Missing: remembering which files conflicted at merge and warning when a new lane's scope includes one.
Status: partial. Score: value 3, effort S, risk low. Decision: build (record conflicted files at `fm lane merge`; `fm lane brief` warns when scope includes a file that conflicted twice or more).

## C9 Lane load gating and scheduling
Ideas: gate builder fan-out on load; throttle lanes by load (x2, plus scale criterion timeouts); per-builder load budget (wild); lane scheduler fusing load, cap and hot spots; yield to the human with renice; brownout mode that sheds features (wild); schedule heavy lanes into learned AFK gaps (wild).
Grounding: `host_strain()` refuses a new lane when load is over 2x CPUs or memory under 512 MB (fmcore.py:356; used fmlanes.py:86, fmhooks.py:2836, fmcli.py:1091); builder cap `builders_cap` fmlanes.py:126. Missing: renice, timeout scaling (folded into C10), brownout.
Status: partial. Score: value 2, effort M, risk med. Decision: skip: the gate exists; the rest is polish.

## C10 Load-aware merge-train retry and flake quarantine
Ideas: re-run only the load-sensitive criterion on lane merge with a load-aware retry; merge train retry load-sensitive criteria once then flag; load-aware merge train with flake quarantine; merge lanes with criteria re-run only on what the merge touched; incremental criteria cache; pin a flake ledger for Foreman's own gates.
Grounding: `_verify` re-runs every criterion once at a fixed 600 s timeout and refuses on the first red (fmlanes.py:478-495). A flake ledger exists for `fm check` (fmcore.py:2394, CHANGELOG.md:680) but `_verify` doesn't use it or `host_strain`. A reused same-tree pass exists in `fm check`, not in lane merge.
Status: partial. Score: value 3, effort S, risk low. Decision: build (one retry of a red criterion when the host was strained or the test is in the flake ledger, scaled timeout, logged as retried).

## C11 Merge safety: transactions, rehearsal, bisect
Ideas: merges transactional with pre-merge ref and one-verb abort; rehearsal merge against main's tip (wild); auto-bisect a red gate to the lane during the merge train (wild).
Grounding: the aborted merge restores its base (fmlanes.py:567); `fm bisect` finds the first bad commit (CHANGELOG.md:317); `fm oops` snapshots. Rehearsal is new.
Status: partial. Score: value 2, effort M, risk med. Decision: skip: restore and bisect exist; rehearsal duplicates the post-merge check.

## C12 Builder stall watchdog
Ideas: no-progress tripwire per builder (x3, including salvage); stuck-builder detector from tool-call shape (bare-stdin hangs, cd loops) (wild); "last words" line that survives SIGKILL (wild).
Grounding: `stopped()` finds lanes whose Claude process has ended and `resume` keeps uncommitted work (fmlanes.py:159-228, T-1028). No hang detection: a live builder that makes no commits, edits or ledger events is never flagged.
Status: partial. Score: value 4, effort M, risk low. Decision: build (flag a live builder whose worktree and ledger show no change for N minutes in `fm lane list` and `fm next`). The last-words wild is skip (resume already saves the work).

## C13 Lane contests, routing, bottleneck
Ideas: pit two cheap builders on one task (wild); score lane outcomes into the model-routing table; tell which lane is the bottleneck in the pane (wild); stable callsign per lane.
Grounding: `fm lane race/score/pick` exist (fmlanes.py:238-378, T-1069); `fm outcomes` tracks results; callsign and bottleneck line absent.
Status: partial (race done). Score: value 2, effort M, risk low. Decision: skip: the core is built; the rest is cosmetic.

## C14 Defect-class memory and builder diff lint
Ideas: lint builder diffs for recurring defect classes before "done"; defect-class memory that feeds builder briefs.
Grounding: reviewer findings are recorded with verdicts (`fm task finding`, CHANGELOG.md:233, `fm usage --agents`), but nothing feeds confirmed finding classes into `fm lane brief` (fmlanes.py:379). `fm map` pre-review lint exists (fmmap.py:541).
Status: new. Score: value 3, effort M, risk low. Decision: build (brief gets a "Defects this project keeps shipping" list from confirmed findings of the last 30 days).

## C15 Skeptic twin, chaos mode, fault-injected fake claude
Ideas: skeptic twin that tries to fail every builder branch (wild); chaos mode for builders (load, stdin, cwd faults) (wild); fake `claude` that misbehaves on script (wild).
Grounding: tests/test_claude.py exists, no scripted-misbehaviour harness; the adversary lens exists at review (`fm audit`).
Status: new. Score: value 2, effort L, risk med. Decision: skip: a testable version (fake claude exiting mid-lane) is covered by C12's tests.

## C16 Heuristic honesty (measured precision labels)
Ideas: replace keyword heuristics with measured accuracy report; label heuristic output with measured precision (x2); approximation honesty with confidence and miss corpus; escalate uncertain heuristics to a cached cheap model.
Grounding: per-lens precision in `fm usage --agents` (CHANGELOG.md:233, 296); guard false positives counted (fmcost.py:691-697). Heuristic outputs elsewhere (fm map, fm relate) carry no label.
Status: partial. Score: value 2, effort M, risk low. Decision: skip: no user decision depends on it.

## C17 Fail-open and degraded-mode honesty
Ideas: recorded, surfaced fail-open budget; `fm state` and list verbs degrade to a partial answer under load.
Grounding: hook breaker with pause (fmhooks.breaker; shown by fm explain, fmrecall.py:908); `fm doctor` check_hook_errors (fmdoctor.py:707) and the pane health line (fmwatch.py:618) already count hook errors.
Status: partial. Score: value 2, effort M, risk med. Decision: skip: surfaced already; degrade-under-load has no demonstrated need.

## C18 Release, version drift and canary
Ideas: installed foreman-ui vs repo release at doctor time; screenshot-gate the pane in the release path; vision child checks pane screenshots; dogfood each release on the user's install; canary HOME tracking main (wild); "new since your installed version" teaser; cut and push a release when the queue drains; version hook payload fixtures against real Claude Code.
Grounding: drift check fmdoctor.py:904; `fm canary` (fmeco.py, fixtures + hook smoke); `fm release-check` in a temp HOME (fmdemo.py:152); release.py one-command release with `--canary`; shot.py (mods/foreman-ui/tools/shot.py). Auto-release on drain is outward, left manual.
Status: partial. Score: value 2, effort M, risk high (outward push). Decision: skip: the pieces exist; auto-release is a user decision.

## C19 Keepsakes and shareables
Ideas: before/after contact sheet per close (wild); `fm postcard` (wild); "last frame" still on `fm ui` exit; "closed with proof" badge (wild); director's-cut 30 s replay at release (wild); jukebox of finished diffs (wild); pin-this-moment bookmark reel; evidence pack for audit; personalised release notes (wild); name the release after the fix (wild).
Grounding: `fm pr` carries proof (CHANGELOG.md:686); `fm page` renders the queue (fmpage.py:133); badge.txt exists in state. No image/SVG keepsake.
Status: new. Score: value 1, effort M, risk low. Decision: skip: does not help an unattended run.

## C20 Personality, sound, voice, identity
Ideas: first close of day text "ding"; mascot sticky note on a nervous file (wild); thank-you note from builder lane (wild); build-weather glyph in statusline (wild); desk lamp from fleet state (wild); apology-free next-move line on failures; errors in the user's own vocabulary (wild); friend-style one-line summary per close; first-time toast per capability; fade quiet cards by recency; living Agents tree whose branches thicken with tokens (wild).
Grounding: mascot, sounds (mods/foreman-ui/sounds/done.wav, needs.wav), Agents node graph (CHANGELOG.md:100-101) exist. Nothing else.
Status: partial. Score: value 1, effort S-M, risk low. Decision: skip: polish.

## C21 Pane layout, idle screen, view model
Ideas: pane idle screen with next three queued cards reorderable by key; one view-model rendered in terminal and HTML; pane in a tmux/zellij split; reconcile pane against ledger with explicit staleness; "state of the union" on bare `fm` after a day's gap; one-page Foreman mode (wild).
Grounding: `fm ui --json` is the single view model (fmwatch.py, ui-demo.json), `fm page`/`fm watch` render it; reconcile done in T-0146 (CHANGELOG); idle line shows what Foreman learned (CHANGELOG.md:29). Gap-based summary is C22.
Status: partial. Score: value 2, effort M, risk low. Decision: skip.

## C22 Return-after-gap summary
Ideas: "what did I miss" receipt after every AFK stretch (wild); pane "while you were away" line or reel (x2); `fm undo --since-afk` (wild); state of the union on bare `fm` after a day (see C21); show what changed while AFK as one expanding line.
Grounding: `fm digest` is a weekly screen (fmcost.py:578); `fm night` runs background work; IDLE_S gap logic exists only for cost accounting (fmcost.py:99). No session-start or on-demand "since you last spoke" summary of closed, blocked, asked and reverted items.
Status: partial. Score: value 4, effort M, risk low. Decision: build (`fm away`, also injected once at session start after a gap; undo is just a listed restore command).

## C23 User-only work checklist and ping quality
Ideas: final report as "what only you can do" checklist with copy-paste commands (wild); make the user-only list tick itself; auto-close blocked tasks whose unblock is user-only into the final report; learn which pings are worth sending; durable authorization ledger.
Grounding: `fm ask` (asks.json, fmcli.py:2726; fmhooks.py:1377) and `fm task block`; full autonomy says "what only the user can do goes in the final report" (fmmission.py:76, fmhooks.py:2755) but no verb assembles it; `fm notify` command exists (fmserve.py:640).
Status: partial. Score: value 4, effort S, risk low. Decision: build (`fm todo`: pending asks, blocked-on-user tasks, decisions flagged costly/outward, each with its command; entries drop when resolved).

## C24 Close honesty: not-verified list, cited claims
Ideas: list what was not verified on every close; cite every claim in the final report; land each close with a one-line friend summary.
Grounding: `fm task finish --claim "checked|inferred|unchecked: ..."` stores typed claims (CHANGELOG.md:244; rendered by fm pr, fmcost.py:800). The close output itself doesn't print criteria checked without a verify command or the unchecked claims.
Status: partial. Score: value 3, effort S, risk low. Decision: build.

## C25 Overnight contract and mission spend envelope
Ideas: say "keep going" once, get a signed overnight contract (wild); treat silence as consent with a receipt (wild); round-level dollar envelope; cap the mission's spend and show progress per dollar; per-engagement spend allocator across projects.
Grounding: `fm budget` has per-command and daily USD limits (fmbudget.py:187-196); per-task `cost_cap` (CHANGELOG.md:47); `fm risk` daily risk budget; `fm autonomy full`; `fm loop on`. Missing: a cap and deadline for a whole run (fm run / loop / drive) with a start and end receipt. fmmission.py has no budget.
Status: partial. Score: value 4, effort M, risk low. Decision: build (`fm contract --until HH:MM --usd N`: the drive, fm run and loop stop at either bound and print a receipt). Silence-as-consent is skip (unsafe).

## C26 Protect the user's hand edits
Ideas: detect the user's hand edits and treat them as protected steers.
Grounding: none found (fmhooks.py:2856 `_ui_changed` is unrelated). Snapshots exist for discarded work (`fm oops`).
Status: new. Score: value 3, effort M, risk med. Decision: build (record dirty files at `fm focus`; a close or lane merge that rewrites a file dirty-at-focus and unchanged by the task is refused with a named list).

## C27 Intent signals: questions, capitals, plain-English routing, ceremony scale
Ideas: treat questions as questions, not tasks; treat capitalised words as priority signals; `fm do "<sentence>"` routing (wild); scale ceremony to blast radius; `fm batch` plan/preview/apply/undo transaction.
Grounding: foreman.md already says a question is answered and work continues; every plain message is intake; `TAG!:`, `NOW:` carry priority (rules); tiers S/M/L plus `fm map` risk (fmmap.py:582); `fm batch` exists but groups requests (a different thing). `fm do` would duplicate hook intake (false premise for that idea).
Status: partial (one idea is a false premise: `fm do`). Score: value 2, effort M, risk med. Decision: skip: handled by rules and hooks.

## C28 Guard feedback loop
Ideas: mark a guard decision wrong in one command (x2, regression case); replay every denial nightly vs current guard (wild); honest guard coverage map; guard near-miss tally in end-of-day line.
Grounding: `fm replay` scores the guard on real past commands (CHANGELOG.md:342) and `fm bench guard --mutate` finds untested rules (CHANGELOG.md:60-62), `fm vetoes`/`fm rule`/`fm taste` take corrections. `fm night` does not run replay (fmnight.py grep: no replay call). No verb stores a "this verdict was wrong" corpus.
Status: partial. Score: value 3, effort M, risk low. Decision: build (two items: `fm guard wrong` appends a labelled case that `fm replay` and the guard tests load; `fm night` runs the replay and captures a FIX on verdict drift). Coverage map and tally are skip.

## C29 Guard hardening extras
Ideas: extract the guard as a standalone package; route every path-trust check through one gate; hook payload fixture versioning.
Grounding: fixtures covered by `fm canary` (fmeco.py); mutation tests exist; packaging not wanted.
Status: partial. Score: value 1, effort L, risk med. Decision: skip.

## C30 Brainstorm and round tooling
Ideas: round checklist page with build/skip marks; persistent capability map diffing over time; mine the workflow's own friction into tasks; skipped-idea resurrection triggers (wild); "do less" sibling for each idea (wild); check each finding's premise before it becomes a task; cache brainstorm output per lens by pack hash (x2); score Foreman nightly against a "THE plugin" rubric.
Grounding: `fm page` with a catalogue (fmpage.py:133, T-0786 done); `fm friction` (fmfriction.py); `fm landscape`; pack hash in the manifest (fmideas.py:681) and `--seen` (fmideas.py:716) but no per-lens cache; stale-plan sweep (fmtidy.stale_plans; fmcost.py:592); `fm bench` rubric judge (fmbench.py:152, 277).
Status: partial. Score: value 2, effort M, risk low. Decision: skip: token saving only.

## C31 Delete verbs by usage
Ideas: delete verbs by usage receipt; auto-open deletion tasks for verbs unused in 60 days (wild); delete-first Fridays (wild); complexity budget blocking merges that grow the verb count (wild); one verb per job duplicate-purpose report.
Grounding: `fm usage` lists skills, playbooks and fm commands used and never used (help text, fmcost.py:928 "fm usage lists as never used"); `fm tidy` removes stale fixes only (fmtidy.py:316). No capture of deletion tasks.
Status: partial. Score: value 3, effort S, risk low. Decision: build (`fm tidy --apply` captures one CLEAN brief per verb unused for 60 days, capped at 3 open). The complexity budget is skip.

## C32 Retire the deferred "Later from T-" tail
Ideas: delete the deferred "Later from T-..." tail (x2); retire it into one dated parking file.
Grounding: 31 deferred briefs titled "Later from T-..." sit in state/projects/foreman-4a056f/tasks and are listed in every mission pack (research/mission-20261015-083935.md:71). No code produces a tail; it is data.
Status: new. Score: value 3, effort S, risk low (never loses text). Decision: build.

## C33 Simplicity wilds, help, states, settings
Ideas: collapse escape-hatch flags into `--because`; every setting with one source and printed effective value; before/after for every setting change; cap default `fm` help at ten lines; merge task states into four words; one-verb mode (wild); README generated from code (wild); `fm explain-less`.
Grounding: `fm help` is tiered (fmcli.py:4915 tier=) but prints about 146 lines; `fm wiring` prints flags, trust, pause, budget (fmcli.py:4915); `fm docs` reports drifted markdown; status words unchanged. `--unverified` and similar flags are separate (fmlanes.py:73).
Status: partial. Score: value 2, effort M, risk med (renames break briefs). Decision: skip.

## C34 Ledger readers
Ideas: collapse the three ledger readers into one shared reader.
Grounding: `c.ledger_events` (fmcore.py:851) reads archives and live; `tail_jsonl` used elsewhere; a few raw readers remain (fmdoctor.py:1142, :1173, fmwatch.py:633). Roughly 3 ad hoc readers, not 3 of the same kind; premise partly stale.
Status: partial. Score: value 1, effort S, risk low. Decision: skip.

## C35 Specs and tracker interop
Ideas: treat a living SPEC.md as a task source; import/export specs from spec-kit and Kiro; two-way sync with Linear, Jira, GitHub Projects; export events as OpenTelemetry (x2 incl. ledger spans); import a rival plugin's rules; Sentry/log alerts to overnight FIX lanes (wild).
Grounding: `fm inbox gh` is read-only GitHub issues (CHANGELOG.md:466); `fm orders` captures on a schedule or file change (fmorders.py); `fm ci-watch` makes FIX from CI failure (CHANGELOG.md:32); `fm export` writes AGENTS.md; plugin/observability/README.md configures Claude Code OTel to telegraf, not Foreman events. No SPEC.md source; no tracker sync.
Status: new (SPEC.md); partial (rest). Score: SPEC.md value 3, effort S, risk low; rest value 1-2, effort L, risk med. Decision: build SPEC.md only (`fm inbox spec FILE` captures each unchecked `- [ ]` item once, text quoted as data); skip: the rest (credentials, outward writes).

## C36 Quality gates and dependency lane
Ideas: Renovate-style dependency upgrade lane; SAST and vulnerability scanners as pluggable gates; gate close on diff coverage; performance-budget gate for the user's project; scope gates to the workspace touched; pin legacy behaviour before the first edit; adopt the dirty tree; run the discipline on non-code work.
Grounding: gates are the project's own commands (`fm check`, fm map gates; `--affected` links tests) so SAST, coverage and perf are configurable already; `fm deps` lists majors behind with the migration question (fmdeps.py) but captures nothing; `fm adopt` baselines an existing repo; start-tree baseline (fmcli.py:1875); legacy-code card exists (skills/library/cards/domains/legacy-code.md); `fm oops` rescues dirty work.
Status: partial. Score: deps lane value 3, effort S, risk low; others value 2. Decision: build deps lane only (`fm deps --capture` queues one CLEAN brief per dependency a major behind, deduplicated); skip: the rest (project's own gate commands cover them).

## C37 PR and handoff
Ideas: write the PR body from the task's proofs; watch the merge after shipping and open a FIX on red; split big diffs into stacked PRs; Foreman as a CI action commenting on PRs (wild); bring-your-own-stakeholder static view (wild); second life for rejected diffs (wild).
Grounding: `fm pr` renders the body with proof (fmcost.py:767, CHANGELOG.md:686); `fm pr threads/train` (CHANGELOG.md:26); `fm ci-watch` (CHANGELOG.md:32); stacked-commit check flag `--stack-check` (fmcli.py:4661); `fm page` is the stakeholder view; rejected diffs are kept by `fm task drop` snapshots (CHANGELOG.md:220). Missing: posting the body to a PR.
Status: partial (most done). Score: post-to-PR value 3, effort S, risk med (outward write). Decision: build (`fm pr ID --post` runs `gh pr comment` with the body on the current branch's PR, only after `fm ask ID remote` style approval).

## C38 Portfolio, wilds and contests
Ideas: nightly league between two Foreman configs (wild); kata gym of seeded bugs (wild); land one proven fix on someone else's repo (wild); audit what would embarrass a stranger on first install; per-verb crash-and-latency ledger with regression gate; Foreman reviews itself against peers; show before/after on setting changes (see C33).
Grounding: `fm bench` duels a rival plugin (fmbench.py:671-746) and seeded-bug review (fmbench.py:954); STRANGER first-use eval (fmbench.py:601); `fm demo` seeded bug (fmdemo.py:1); hook latency p95 in the pane (fmwatch.py:59-62); `fm burden`. Nightly scheduling and external PRs absent.
Status: partial. Score: value 2, effort L, risk med. Decision: skip.

## Tally
Idea count covered: 218 (some titles appear in two clusters where noted).
Clusters 38. By status: queued 6 (C1, C2, C3, C5, C6, C7; C1-C3 are done tasks), done 0 others, partial 27, new 5 (C14, C15, C19, C26, C32; C35 is counted partial though SPEC.md in it is new), false premise 0 whole clusters (one idea inside C27, `fm do`).
Decisions: build 15, skip 17, n/a (queued) 6.

## Intake
FEATURE: Show a return-after-gap summary (`fm away`, also once at session start) of what closed, blocked, was asked, or was reverted since the user last spoke.
DONE-WHEN: a test seeds a ledger with events before and after a simulated gap and `fm away` lists the closed, blocked, pending-ask and reverted items after the gap and nothing before it
FEATURE: Flag a live builder lane that shows no commit, worktree change or ledger event for N minutes in `fm lane list` and `fm next`.
DONE-WHEN: a test with a lane whose worktree mtime and ledger are older than N minutes sees it listed as stalled, and a lane with a fresh edit is not
FEATURE: Add `fm todo`, the list of what only the user can do (pending asks, blocked-on-user tasks, costly or outward decisions), each with its command, dropping entries when resolved.
DONE-WHEN: a test with one pending ask and one user-only block prints both with their commands, and after the ask is granted `fm todo` no longer lists it
FEATURE: Add `fm contract --until HH:MM --usd N` so the drive, `fm run` and the loop stop at the time or spend bound and print a receipt of what ran.
DONE-WHEN: a test with a fake clock and fake spend stops the run at each bound, and the receipt lists the tasks closed, the spend and which bound ended it
FEATURE: Print what was not verified at every task close: criteria with no verify command, unchecked claims, and checks that were skipped.
DONE-WHEN: `fm task finish` on a task with one unchecked claim and one criterion lacking a verify command prints both under "Not verified", and prints none on a fully verified task
FEATURE: Retry a red lane-merge criterion once (with a scaled timeout) when the host was strained or the failing test is in the flake ledger, and log it as retried.
DONE-WHEN: a test with FOREMAN_HOST load set high and a criterion that fails once then passes merges the lane and logs a retry; the same criterion failing twice still refuses
FEATURE: Record files that conflicted at `fm lane merge` and warn in `fm lane brief` when a new lane's scope includes a file that conflicted twice or more.
DONE-WHEN: a test merges two conflicting lanes twice on one file and the next `fm lane brief` for a task scoped to that file prints the warning, and a task on another file prints none
FEATURE: Add `fm guard wrong "<cmd>" --should allow|block` to store a labelled case that `fm replay` and the guard tests load, and have `fm night` run the replay and capture a FIX when verdicts drift.
DONE-WHEN: a test adds a wrong-verdict case, `fm replay` reports it against the current guard, and a seeded drift in `fm night` captures exactly one FIX brief
FEATURE: Capture one CLEAN deletion brief per `fm` verb unused for 60 days from `fm tidy --apply`, at most three open at a time.
DONE-WHEN: a test with usage data showing two stale verbs captures two CLEAN briefs, a second run captures no duplicates, and a fourth stale verb stays uncaptured while three are open
FEATURE: Feed a task's brief with the defect classes confirmed by reviewers in the last 30 days (`fm lane brief` section "Defects this project keeps shipping").
DONE-WHEN: a test with two confirmed findings of one class in the finding records makes `fm lane brief` print that class once with its count, and no section appears when there are none
FEATURE: Add `fm inbox spec FILE` that captures each unchecked `- [ ]` item of a SPEC.md once, quoted as untrusted data.
DONE-WHEN: a test with a spec holding two unchecked and one checked item captures two briefs; running again captures none; a line with an instruction-like text lands quoted
FEATURE: Add `fm deps --capture` that queues one CLEAN brief per dependency a major version behind, without duplicating an existing open brief.
DONE-WHEN: a test with two fake outdated dependencies captures two briefs and a second run captures none
FEATURE: Add `fm pr ID --post` that posts the rendered PR body as a comment on the current branch's PR through gh, only after the remote approval.
DONE-WHEN: with a fake gh on PATH the test sees one `gh pr comment` call carrying the body when approved and no call when not approved
CLEAN: Retire deferred "Later from T-..." briefs into one dated parking file with `fm tidy --apply`, so mission packs stop listing them.
DONE-WHEN: after `fm tidy --apply` on a fixture with three deferred "Later from" briefs they are gone from the queue, their titles are in one parking file with a date, and no text is lost
FEATURE: Refuse a close or lane merge that rewrites a file that was dirty when the task was focused and not changed by the task, naming those files.
DONE-WHEN: a test dirties a file before `fm focus`, edits it as the task, and `fm task finish` refuses naming the file; with the file untouched by the task the close passes
