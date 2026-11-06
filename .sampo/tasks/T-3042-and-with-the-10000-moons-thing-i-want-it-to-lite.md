---
id: T-3042
type: FEATURE
tier: L
status: planned
priority: normal
scope: []
depends_on: [T-3045, T-3046, T-3047]
source: user
created: 2026-11-04T23:56:57Z
updated: 2026-11-06T03:53:48Z
rival_at: 2026-11-05T00:06:07Z
rival_split: true
group: 10000 moons target
---
# 10,000 moons kept and used, and moons on anything related to Sampo
## Raw request
> and with the 10000 moons thing, I want it to literally output 10000 moons that will be used, not just in total, so the 300 number tat was kept, I want 10000 to be kept, and such, and you can do moons on anything related to sampo, like its problem solving, memory, effeciency, etc.
## Interpretation
Reading A (taken): the funnel's survivors, not the store, must reach 10,000: today 10,007 generated moons leave 292 kept at novelty; the goal, the night's grow job and its gate count kept moons, and every kept moon is exported, listed on the site and drawn on by genesis (nothing dropped to a top slice). Reading B: 10,000 moons each built or kill-tested: not feasible at that count; the climb keeps building the best, and every kept moon is queued for it in turn. Reading C: just raise the store target to ~350,000 so 3% yields 10,000: wasteful; yield goes up instead. And Sampo itself becomes a moon subject: its problem solving, memory, efficiency and every other area of coverage.md, with the 'payoff names only the harness' write rule lifted for those cells.
## Assumptions (confidence)
Local models (this box's gemma, Jarvis's 27B with the stored LLM_API_KEY) do the bulk for free (90%); Haiku only when no local model answers and the budget allows (80%); the wild bar and the high-tier bar stay (90%: the user asked for more kept, not tamer ones); pure-Python linear dedupe is fine to ~50k candidates (measured 12 µs a pair), but the all-pairs family rebuild is not (10 min at 10k).
## Acceptance criteria
- [ ] 10,000 moons kept: the funnel's survivors (kept at novelty) reach 10,000, counted from funnel.jsonl, and every kept moon is in the export — verify with `sampo genesis moonshot --status`
- [ ] The goal counts kept moons, not total, and the 300 number goes up by yield: parts 1 and 2 (T-3045, T-3046) closed — verify with `sampo task show T-3045 && sampo task show T-3046`
- [ ] Moons on anything related to Sampo, and used, not just stored: parts 1 and 3 (T-3045, T-3047) closed — verify with `sampo task show T-3047`
## Non-goals
Building or kill-testing all 10,000 (the climb takes the best in turn); loosening the tier or wild bar; a vector database or numpy (no installs).
## Approach (options → choice → why)
Options: (1) generate ~350,000 at today's 3% yield: days of local compute, mostly waste; (2) raise the yield where the funnel loses most (1,389 write rejects are only a missing 'With this,'; 5,795 kill rejects are one-day-test misses a rewrite can fix; the generator never sees why its cell's moons die), add the Sampo-self grid, and grow until kept reaches 10,000; (3) loosen the kill and tier bars: more kept but tamer, against the wild steer. Choice: (2), with families from links stored at novelty (no all-pairs rebuild) and the whole survivor set exported and drawn on. Why: it meets the count without lowering the bar, and every fix is measurable on the live store.
## Risks and rollback
A repaired kill test that games the judge: repairs are new rows with a parent, judged by the same stages, and the kill judge sees only the rewritten test; a flood of self moons crowding out the user-facing grid: cells are read thinnest first across both grids; rollback: the store is append-only, so reverting the code leaves every row and fate readable.
## Execution prompt
Build steps 1 to 5 test-first in plugin/lib/sampo/moonscale.py (and night.py, the site's Moons page, export) with tests in plugin/tests/test_moons_scale.py (and test_night.py, test_genesis.py or the site tests the export feeds). Live data (state/projects/foreman-4a056f/research/genesis/moons): 10,007 candidates; fates: write rejected 1,614 (1,389 'with_this must start "With this, you can"': most start 'You can see…', 'You can get…', 'With this, you get…'), kill rejected 5,795 (reasons: needs real or production data 1,177, a tool nobody has built 733-1,041, a team 318, live traffic 240, weeks or months 420), tier rejected 2,255 (keep this bar), novelty kept 292. Yield: haiku 8.9%, jarvis+nothink (Qwen 3.8 27B) 1.9%. (1) _clean normalises with_this ('You can X' and 'With this, you get X' become 'With this, you can'/'With this, you get' accepted) and a re-admit pass appends a new write event for old write rejects that now pass (fate is the last event; never rewrite rows). (2) A Sampo grid: areas = coverage.md's '## ' headings (rune.home(p)/coverage.md; strip numbering) plus 'problem solving', 'memory', 'efficiency'; scales: one task, one session, one project, every project, every Sampo user; the cell carries grid='sampo'; _pick reads thinnest first across both grids; admit skips the internal-only payoff rule on sampo cells and accepts 'With this, Sampo can'; the prompt for a sampo cell asks for moonshots about Sampo itself (its problem solving, memory, efficiency, …) with the same wild bar and kill-test rules. (3) Kill repair: a kill-rejected candidate (never one that is itself a repair) gets one rewrite of only its kill test from the cheap model, told the judge's reason and the rule (one person, one day, tools that exist today, synthetic or open data in place of production, a pass or fail bar); stored as a new candidate with parent=<id> and repair='kill' that enters the funnel at write like any row; each cell's generation prompt carries the cell's (or its kind's) top three reject reasons from funnel.jsonl and two kept moons as anchors. (4) grow(keep=N) / CLI --keep N: rounds of grow then funnel until survivors (fate kept at novelty) reach N, or max-calls, budget or FAILS stop it; night_ready grows while survivors < TARGET; night.py's job passes --keep TARGET; families from links: the novelty stage records, for each new survivor, the earlier survivors at or above BAR['family'] in the same scan it already makes (no extra sims), and families() unions stored links (one-time backfill for survivors without links, chunked); show it equals the all-pairs grouping on a fixture and groups 10,000 synthetic survivors in under 10 s. (5) export writes every survivor to moons/catalogue.json (id, title, today, with_this, what, kill, tier, wild, family, grid, cell) beside genesis.json's counts; the site's Moons page pages and searches the catalogue (filters: grid, tier, family); promote draws from all survivors, family leads first by tier and wild, then their variants, recording a 'drawn' event so none is drawn twice. Stores stay append-only. Never print or log LLM_API_KEY; models.secret() already reads it. Read first: moonscale.py's header, admit, _pick, _prompt, grow, the funnel stages, families, export, promote; night.py lines 60-80.
## Steps
1. [ ] part 1: yield and the Sampo grid (child T-3045, M)  <- CURRENT
2. [ ] part 2: count kept moons, families from links (child T-3046, M)
3. [ ] part 3: every kept moon used (child T-3047, M)
4. [ ] fill: grow --keep 10000 on the local models (gemma here, Qwen 3.8 27B on Jarvis) until 10,000 are kept; report the funnel
## Resume here
## Docs impact
CHANGELOG; MASTER.md's moons lines; the night job's help; the site's Moons page.
## Verification evidence
## Log
- 2026-11-04T23:56:57Z created
- 2026-11-05T00:01:38Z planned: it has criteria and steps
- 2026-11-05T00:05:52Z criterion 2 verify: `python3 plugin/tests/run.py test_moonscale` → `python3 plugin/tests/run.py test_moons_scale`
- 2026-11-05T00:05:52Z criterion 3 verify: `python3 plugin/tests/run.py test_moonscale` → `python3 plugin/tests/run.py test_moons_scale`
- 2026-11-05T00:05:53Z criterion 4 verify: `python3 plugin/tests/run.py test_moonscale` → `python3 plugin/tests/run.py test_moons_scale`
- 2026-11-05T00:05:53Z criterion 6 verify: `python3 plugin/tests/run.py test_moonscale` → `python3 plugin/tests/run.py test_moons_scale`
- 2026-11-05T00:05:54Z criterion 5 verify: `python3 plugin/tests/run.py test_moonscale test_genesis_site` → `python3 plugin/tests/run.py test_moons_scale test_genesis`
- 2026-11-05T00:07:37Z set approved=True
- 2026-11-05T00:08:12Z planned from capture
- 2026-11-05T00:08:13Z planned from capture
- 2026-11-05T00:08:14Z planned from capture
- 2026-11-05T00:09:00Z set tier=L, title=10,000 moons kept and used, and moons on anything related to Sampo, scope=[]
- 2026-11-05T00:09:00Z criterion 1 verify: `python3 plugin/tests/run.py test_moons_scale` → `sampo genesis moonshot --status`
- 2026-11-05T00:09:00Z criterion 1 text: Export writes every kept moon to a catalogue file beside genesis.json, not a top slice → 10,000 moons kept: the funnel's survivors (kept at novelty) reach 10,000, counted from funnel.jsonl, and every kept moon is in the export
- 2026-11-05T00:09:00Z criterion 2 verify: `python3 plugin/tests/run.py test_moons_scale test_genesis` → `sampo task show T-3045 && sampo task show T-3046`
- 2026-11-05T00:09:00Z criterion 2 text: The site's Moons page lists every kept moon with search and filters (grid, tier, family), paged → The goal counts kept moons, not total, and the 300 number goes up by yield: parts 1 and 2 (T-3045, T-3046) closed
- 2026-11-05T00:09:01Z criterion 3 verify: `python3 plugin/tests/run.py test_moons_scale` → `sampo task show T-3047`
- 2026-11-05T00:09:01Z criterion 3 text: Promotion draws from every kept moon, family leads first by tier and wildness, then variants, each draw recorded so none is drawn twice → Moons on anything related to Sampo, and used, not just stored: parts 1 and 3 (T-3045, T-3047) closed
- 2026-11-05T00:09:01Z step 1 text: export every survivor (tests first) → part 1: yield and the Sampo grid (child T-3045, M)
- 2026-11-05T00:09:01Z step 2 text: the Moons page lists them (tests first) → part 2: count kept moons, families from links (child T-3046, M)
- 2026-11-05T00:09:01Z step 3 text: promotion draws from all, recorded (tests first) → part 3: every kept moon used (child T-3047, M)
- 2026-11-05T00:52:56Z set depends_on=['T-3045', 'T-3046', 'T-3047']
- 2026-11-05T00:52:56Z blocked: waits on its three parts (T-3045 and T-3046 merge after the network view; T-3047 is back with its builder after review); then the fill to 10,000 runs on the local models
- 2026-11-06T03:53:48Z unblocked
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: Sampo has a "moons" mechanism (a count/limit, previously 300) that is currently reported only as an aggregate total. The user wants it to emit the full list of 10000 individual moons, retained rather than truncated to 300 (probably a cap or keep-limit in `plugin/lib/sampo/` or `plugin/li…
- The "300 kept" is a retention/display cap (e.g. a ring buffer or `[:300]` slice), and the request is to raise it to 10000 and persist every item, with per-dimension moons (problem solving, memory, efficiency) added as new tagged kinds.
- "Moons" is a metric/score unit (like points) and "10000 moons" is a target budget or scale; the user wants the output to show the 10000 individual awards rather than a sum, with the cap on retained entries raised from 300.
- Less likely: it is UI-only (`design/sampo/index.html`, `plugin/web/live/index.html`) and wants the page to render all 10000 moon items rather than a total and a truncated 300.
Approaches:
- Find the "moons" and "300" symbols with grep in `plugin/lib/sampo/` and `plugin/lib/fmcore.py`. Replace the hardcoded cap with a named constant (10000), keep the per-moon records (id, dimension, reason, timestamp) in the existing store, and have `plugin/lib/sampo/cli.py` list them, with the total a…
- Add a `dimension` field on each moon (problem_solving, memory, efficiency, ...) with a registry of dimensions in one module, so new Sampo-related categories are data, not code. The CLI gets a `--by dimension` view, and the existing total derives from the list.
- Make the store append-only (JSONL) with no truncation, and compute the total and per-dimension counts on read. This avoids a cap entirely, so "10000 kept" falls out of retention rather than a limit.
- UI path: have `design/sampo/index.html` or `plugin/web/live/index.html` fetch the full list and virtualize rendering, so 10000 rows don't freeze the page.
Failure modes:
- The 300 is enforced in several places (writer slice, reader slice, UI limit, test fixture in `plugin/tests/test_*sampo*`). Raising only one leaves output still showing 300, so the "total" and the list disagree.
- Persisting 10000 records per session hits the hooks' latency budget (`plugin/tests/bench_hooks.py --runs 20`) if `fmhooks.py` reads and rewrites the full file on each event. Rewriting a JSON blob instead of appending is the likely culprit.
- Existing saved state only holds the aggregate or the last 300, so the old data cannot be backfilled into 10000 individual moons. The migration needs to be explicit rather than silently inventing entries, or `fm doctor`/`fm replay` will flag schema drift.
- Category moons for problem solving, memory and efficiency get awarded without a defined trigger, so they inflate arbitrarily, and the total looks meaningful without being grounded in measured behaviour.
## Dissent
- [x] rival reading: Likeliest: Sampo has a "moons" mechanism (a count/limit, previously 300) that is currently reported only as an aggregate total. The user wants it to emit the full list of 10000 individual moons, retained rather than truncated to 300 (probably a cap or keep-limit in `plugin/lib/sampo/` or `plugin/li… — answered: Grounded: there is no 300 cap; 292 is the funnel's survivors (10,007 generated: 1,614 write, 5,795 kill and 2,255 tier rejects). Emitting all 10,000 is criterion 5 (export every survivor), and keepin…
- [x] rival reading: The "300 kept" is a retention/display cap (e.g. a ring buffer or `[:300]` slice), and the request is to raise it to 10000 and persist every item, with per-dimension moons (problem solving, memory, efficiency) added as new tagged kinds. — answered: No retention cap exists (stores are append-only, nothing truncated); EXPORT_TOP=200 families is the only slice and criterion 5 removes it; the Sampo areas are criterion 4's grid, read from coverage.m…
- [x] rival reading: "Moons" is a metric/score unit (like points) and "10000 moons" is a target budget or scale; the user wants the output to show the 10000 individual awards rather than a sum, with the cap on retained entries raised from 300. — answered: Moons are moonshot ideas, not a score; the count is of kept ideas
- [x] rival reading: Less likely: it is UI-only (`design/sampo/index.html`, `plugin/web/live/index.html`) and wants the page to render all 10000 moon items rather than a total and a truncated 300. — answered: The page is part of it (criterion 5: the Moons page lists every kept moon with search); the count itself is the funnel's
- [x] rival approach: Find the "moons" and "300" symbols with grep in `plugin/lib/sampo/` and `plugin/lib/fmcore.py`. Replace the hardcoded cap with a named constant (10000), keep the per-moon records (id, dimension, reason, timestamp) in the existing store, and have `plugin/lib/sampo/cli.py` list them, with the total a… — answered: No cap to replace (grep found none); the change is yield and the goal's meaning, not a constant
- [x] rival approach: Add a `dimension` field on each moon (problem_solving, memory, efficiency, ...) with a registry of dimensions in one module, so new Sampo-related categories are data, not code. The CLI gets a `--by dimension` view, and the existing total derives from the list. — answered: Taken in spirit: Sampo areas are data (coverage.md headings plus the user's named three), carried in the cell, not hardcoded kinds
- [x] rival approach: Make the store append-only (JSONL) with no truncation, and compute the total and per-dimension counts on read. This avoids a cap entirely, so "10000 kept" falls out of retention rather than a limit. — answered: Already so: candidates.jsonl and funnel.jsonl are append-only and counts are computed on read
- [x] rival approach: UI path: have `design/sampo/index.html` or `plugin/web/live/index.html` fetch the full list and virtualize rendering, so 10000 rows don't freeze the page. — answered: Taken for the page: the Moons page pages and filters the export instead of drawing 10,000 rows at once
## Build vs reuse
Reuses moonscale's own store, funnel stages, _ask (local first, Haiku after), _reps/_nearest and families' union-find; the kill repair follows playbooks small grow's repair pass (it repaired 761 of 1,804 refused cards); coverage.md's headings come from rune's coverage reader; models.secret() for the Jarvis key. Nothing new installed.
