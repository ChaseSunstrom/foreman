# Mission — Initiative (gen 1, #1)

Task: T-2120 (brief 1, exam contract repair), T-2121 (brief 2, fm find), T-2122 (brief 3, prove gate), T-2123 (brief 4,
initiative pipeline + skill), T-2124 (brief 5, project scout probes), T-2125 (brief 6, value ranking), T-2126 (brief 7,
#1 held-out exam), T-2127 (brief 8, surfaces)

Self-contained for a fresh `fm run` in ~/.claude/foreman. Parent: gen-1/seed.md → gen-0.md §2 #1, §3.
Ideas: 542 new from `fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen` (brainstorm-20261030-025354, mission
pack research/mission-20261030-025317.md), lenses below; about 120 placed by tier after merging duplicates.

## Capability (gen-0 §2 #1)
In any repo with no request: map it, find the real bugs, security holes, missing or failing tests, slow paths, rotten
deps, docs drift, CI flakes, open issues and missing features, rank them by value, prove each one (repro or failing
test), and fix them on lanes. Language-agnostic. Grows `fm scout` from watching Foreman into watching any project.

## What the G-tower arm taught (Mission 2's critique)
Both session arms found every planted defect and closed no scenario: genesis 13 false alarms, plain 9. Reading the
answers, part of those "false alarms" are true latent defects of the exam's own clean base app (C `label` sprintf with
no capacity, C `dedupe` indexing on negatives, `page` with pg < 1 giving a negative start, `clamp` with lo > hi left
undefined), and the C and Rust READMEs show a broken run command (`shlex.join` quotes the `&&`). So the exam is fixed
first, and the lever for #1 is precision: **report only what is proven**.

## Lenses (pack: fitted + required + invented)
- Required: **inversion** (how initiative fails: floods the inbox, "fixes" what was intended, files Foreman's own setup
  faults as the user's bugs, proves a bug with a test that fails for the wrong reason, scouts a repo the user doesn't
  own); **sci-fi** (the 2030 night shift that hands over a ranked list of proven, fixed defects each morning, worked
  back to deterministic finders + a test judge today); **self-modification** (finders scored on outcomes and muted
  under a precision floor; probe edits gated on a held-out exam).
- Invented: **planted-defect exam** (every finder is measured on renders with known defects and on clean twins before
  it touches a user repo); **false-alarm economics** (an unasked finding costs the user's attention: price it, cap it,
  prove it); **night shift** (what runs unattended between sessions, with what budget and what it may touch).
- Fitted: user value, reliability, simplicity, bold bets, blind spots.

## Gaps closed (gap map #1)
| Gap | Tier | Brief |
|---|---|---|
| The exam punishes true findings: latent base-app defects and a broken README command | 3 | 1 |
| Finders: language-agnostic, deterministic, zero on clean | 3 | 2 |
| find → prove → fix pipeline: a finding is reported only with a red-for-the-right-reason proof | 4 | 3, 4 |
| Project scout: probes over user projects, capped and proven, Foreman's own faults routed to the self-inbox | 3 | 5 |
| Value ranking: severity × proof × reach ÷ effort, per-finder precision from outcomes | 3 | 6 |
| No held-out, child-authored exam for #1 (multi-defect, no request, clean twins) | 3 | 7 |
| Ecosystems + scout on fm code, MCP, site, pane | 3 | 8 |

## Approaches
A. **Chosen — finders propose, a test judges.** Deterministic finders (and later a model finder) emit candidates; a
   candidate becomes a finding only when the prove gate gives it a proof ticket: a test that is red on the untouched
   tree for an assertion reason, red 3 runs of 3, and green once the defect's line is reverted or fixed. Unproven
   candidates are leads (kept, never shown as findings). Precision by construction; recall is the finders' job.
B. A better prompt for a model-only finder (the session arms today). Not the primary: the arms already find 3/3 and
   lose on precision; kept as a feeder into A's gate (brief 4 runs it as one finder).
C. Per-language static analysers (semgrep, clippy, eslint, bandit). Not now: each needs an install (that's #5) and
   is one language; the finder interface takes adapters later (captured to Mission 6, tools).
D. Prosecutor and defender agents per finding. A spike (cold refuter): if a defender that can't refute a proven
   finding adds no precision over the proof gate, it isn't built.

## Design
1. **Exam contract repair** (tier 3). README run command `shlex.join(build.split()) + " && ./t"` (the `&&` unquoted);
   the README states the edge contract every language's clean app follows: page n < 1 or size < 1 is empty, clamp
   with lo > hi returns lo, label writes at most `width` columns plus the string and the C one takes a capacity,
   dedupe takes any long (no index by value), total of nothing is 0. Hidden edge tests for each clause run on the
   clean render in all six languages (exam of the exam). Grading: an unkeyed finding whose proof test fails on the
   clean base is an **exam defect** (counted, logged, not a false alarm); without a proof, it stays a false alarm.
   Re-run the oracle, empty and finders arms; the oracle stays 100%.
2. **`fm find [PATH] [--json]`** (tier 3, new fmfind.py). Deterministic, language-agnostic finders over a tree, each a
   function returning candidates `{finder, kind, file, symbol, line, says, probe}`: untested (a public function no
   test names), docs (fmdocs.scan), deps (an import of a package no manifest declares and the stdlib doesn't have,
   fmoutside.dependencies), sql (a query string built by concatenation or interpolation of a parameter), slow (a
   membership test on a list inside a loop over the input), flaky (random/time in a test with no seed), secrets
   (fmsecrets._tree), failing gates (fm adopt's gate run, rerun once: flaky vs fail). Generated and vendored paths are
   fenced out (fmmap's fences). Every finder reports 0 on every clean exam render; recall per finder is measured on the
   planted ones. The exam's finders arm becomes `fm find`.
3. **Prove gate — `fm find prove ID|--all`** (tier 4). For each candidate a proof ticket: the finder's probe or a
   model-written test (tool-less model call with the candidate, the file and the test style; the test runs with
   fmbench.CREDENTIALS stripped) is run on a copy of the untouched tree; the ticket holds the command, exit, the
   failing assertion line and three runs. It is **proven** when red 3/3 for an assertion (not an import, setup, syntax
   or timeout error: classified by the failure text) and green once the candidate's hunk is reverted or the fix
   lands (mutate-to-confirm, through `fm task prove`'s machinery). Kinds a test can't judge (docs drift, an
   undeclared dep, a credential) prove by their own check re-run cold. Unproven → `leads.jsonl`, never an inbox item.
4. **Initiative pipeline + `/foreman:initiative` skill** (tier 4). `fm find --fix` and the skill, for no request or
   "make this great": map (fmmap) → find → prove → rank (brief 6) → one task per proven finding, fixed test-first on
   a lane (`fm run` lanes, PARALLEL_MAX); the proof test is the task's red; the fix's revert must flip it red again.
   A "clean" verdict is first class: a receipt of what ran and found nothing. The model finder (approach B) is one
   finder here, its candidates through the same gate.
5. **Project scout probes** (tier 3). `probe_find` in fmscout runs `fm find` + prove on the user's own project
   (registered and git-owned by the user's identity; else refused), at most 3 captures a day, proven only, each with
   its proof ticket. probe_doctor's failures in a user project go to Foreman's self-inbox, not the project (the gap
   map's "Noticed"). A refutation ledger: a dismissed or reverted finding's fingerprint (finder, file, symbol, says
   normalised) is never filed again.
6. **Value ranking** (tier 3). `fm find --rank`: score = severity (kind weight) × proof strength (proven 1, lead 0.2)
   × reach (callers from fmgraph, hot files) ÷ effort (hunk size); per-finder precision from fm outcomes (kept vs
   dismissed/reverted, prior 0.5 over 10 cases) multiplies in, and a finder under a 0.3 floor is muted with a line in
   `fm find` saying so. Abstains (no capture) below a threshold. The order is what scout captures and the pipeline fixes.
7. **#1 held-out exam** (tier 3). See below. CHILD_KINDS gains `none`: a tool-less child plants 3–4 defects of mixed
   kinds into a module with no request; and `clean`: the render as is, graded on 0 false alarms.
8. **Surfaces** (tier 3). fm code and MCP (`fm find` is a verb any shell agent runs; the MCP tool list gains it), the
   site page (Initiative: what ran, proven vs leads, the exam line), a pane/status line (proven findings waiting),
   MASTER.md, README, CHANGELOG.

## Exam (#1; ≥ 9 scenarios per kind, ≥ 3 held out)
| Kind | Given | Graded on |
|---|---|---|
| I-none | a child-authored project with 3–4 planted defects (bug, vuln, slow, untested, docs, dep), no request | found + fixed test-first over keyed, 0 false alarms |
| I-clean | a clean render, nothing planted, no request | 0 findings filed; a clean receipt |
| I-rank | 3 planted defects of different severity | the proven order puts the vuln and the bug above slow/docs |
Each kind 9 scenarios (6 train, 3 held out; `fm exam gen --author child`), 6 languages. Arms: finders (`fm find`),
foreman (the initiative skill), plain ("" request, no plugin), on the held-out third, with cost.

## Exam of the exam
1. The oracle closes every scenario; empty closes only I-clean; each edge-contract clause has a hidden test the clean
   render passes in all six languages.
2. A proven unkeyed finding that fails on the clean base is reported as an exam defect, not scored against the arm.
3. Held-out ids never appear in a train run or in any Mission's tuning of finders or weights.

## Spikes (tier 4, local, throwaway)
Cold refuter (approach D); a canary mutation planter per language (plant a known defect, check the finders and the
gate catch it before trusting a "clean"); a clean twin of a real repo (Foreman's own tree as the user project);
replay git history (do past `fix:` commits' parents get found?).

## Inbox (tier 1–2, captured)
Attention purse per day; a do-nothing receipt in the digest; veto word per finding class; per-ecosystem precision
scorecard; knapsack over the night's budget; sibling hunt after every fix; first scout run as a dry report.

## Rejected
Scouting repos the user doesn't own; filing upstream issues or PRs (leaves the machine); cloning outside repos as a
benchmark (a NEVER); auto-merging fixes into a user's main (merging stays the user's call).

## Tier share
Built here: 8 briefs, 2 at tier 4 and 6 at tier 3 (100% tier 3–4) plus 4 tier-4 spikes; tier 1–2 go to the inbox.

## Done when
The exam's clean renders pass their edge contract in six languages and the README command runs; `fm find`, `fm find
prove` and `--rank` work and are tested; scout captures only proven findings in a user project, capped, with Foreman's
faults routed to the self-inbox; the `/foreman:initiative` skill works in Claude Code and `fm find` in fm code and MCP;
the #1 exam runs the finders, foreman and plain arms on its held-out third; MASTER.md, README, CHANGELOG and the site's
Initiative page show it.

```
FIX: exam contract — README run command, edge contract followed by every clean app, proven unkeyed = exam defect
FEATURE: fm find — deterministic language-agnostic finders, zero on every clean render
FEATURE: fm find prove — proof tickets: red 3/3 for an assertion, mutate-to-confirm; unproven become leads
FEATURE: initiative pipeline + /foreman:initiative skill — map → find → prove → rank → fix on lanes, clean receipt
FEATURE: scout project probes — proven only, ≤ 3 a day, refutation ledger, Foreman faults to the self-inbox
FEATURE: value ranking — severity × proof × reach ÷ effort, per-finder precision floor
FEATURE: #1 exam — I-none, I-clean, I-rank, child-authored, finders vs foreman vs plain
FEATURE: initiative surfaces — fm code, MCP, site page, pane line, docs
DONE-WHEN: the held-out #1 exam runs all three arms and the clean renders file nothing
```
