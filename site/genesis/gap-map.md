# Genesis gap map — generation 1 (2026-10-29)

Built from 13 parallel read-only recon passes (one per §2 capability) over the foreman repo at ae98159e. Every later
idea is checked against this map: an idea that names something under **Exists** is a duplicate unless it extends it.
Tiers: 3 capability, 4 paradigm. Paths are under plugin/lib unless shown.

## Cross-cutting findings (the same hole seen from several capabilities)
- **Advice, not action.** Most parts report or hint and stop: fm burden, fm docs, fm backtest, fmtrials (proposes
  revert), plugins suggest (no callers), fm mission (a hint, never auto-run), fm night --print-timer, fm lane brief
  (prints an Agent line). The gap is the trigger and the closing of the loop, not the parts.
- **Foreman watches itself, not the project.** fm scout's 7 probes look at Foreman/Claude Code (fmscout.py:248-251).
- **Prose, not gates.** "3+ approaches", the tower, the capability map, incident steps live in markdown; the plan gate
  checks only that Interpretation/Approach are non-empty (fmcore.py:2605-2607).
- **No exam exists.** bench/spec-suite is 8 Python tasks; fmbench's planted-bug bench plants `return None` in Python
  only (fmbench.py:1313). Holdout is a per-case hash split (fmbench.py:770, HOLDOUT_EVERY 5). Nothing generates
  multi-language repos with answer keys.
- **Surfaces.** Nearly everything is CLI + Claude Code plugin; fm code, MCP (research/recall read-only) and Desktop
  are rarely wired.

## 1. Initiative
- Exists: fm scout (fmscout.py, Foreman-only probes, MAX_CAPTURES, mandate-aware); fm adopt (fmeco.py:92-150: one-shot
  gates, flake rerun, untested hot files, secrets, deps → briefs); fm deps (pypi/npm/crates); fm docs (paths/commands);
  fm inbox gh (manual); fm night queue job `fm run --fit --max 2`; fm run lanes (PARALLEL_MAX 3).
- Partial: adopt is manual and one-shot; deps covers 3 ecosystems.
- Missing: project probes in scout; bug/security/perf/flake finders; finding → repro/failing test → lane fix pipeline;
  value ranking.
- Gaps: project-scout (3) · finders (3) · find→prove→fix pipeline (4) · value ranking (3) · ecosystems + scout on
  fm code/MCP (3).
- Noticed: probe_doctor may queue Foreman setup failures as tasks in user projects.

## 2. Exhaustive thinking
- Exists: plan gate (presence only); fm second cheapest/devil/pre-mortem (advisory); fm graph blast (only caller
  fmsplit); fm lane race (manual, 2 sides, S/M, scored by verify pass ratio then lines, fmlanes.py:320-442); spikes
  can't merge; tier depth in protocols.json (only the S panel skip enforced).
- Missing: content check of readings/approaches/failure modes; automatic races; L races; blast tied to the plan; a
  scorer that sees design quality.
- Gaps: approaches/readings gate scaled by tier (3) · auto race of N candidates by evidence (4) · blast in plan (3).

## 3. Anticipation
- Exists: fmforesight (present problems only: CI red, model/CC change, blocked pile); user_voice text dump
  (fmideas.py:330-350); misses() (word overlap); lens_rates, taste, precedent, court cases, fm repeats, outcomes.
- Missing: next-request predictor; drafting predictions in lanes; scoring predictions; user/project/machine model.
- Gaps: user/project model (4) · predict-and-draft in a lane, scored (4) · foresight that predicts (3).

## 4. Goal to finish
- Exists: fm mission (prompt only; pillars tell the model to list best-in-class); hook hint for exhaustive asks
  (fmhooks.py:1245-1253); DONE-WHEN → ACs; depends_on + _topo; PreCompact checkpoint + fm resume; Stop drive
  (DRIVE_MAX, no-progress stop, contract bound); forever loop (2 dry rounds); fm mandate (clauses, read by scout and
  night only); fm clauses (word overlap, nudge at focus).
- Missing: a goal ledger (contents list → tasks → done-when → coverage); done-vs-stopped verdict; goal re-injection
  across sessions; epics.
- Gaps: goal ledger (4) · done vs stopped (4) · grounded contents lists (3) · clauses wired to Stop (3) · goal
  carried across days (3).

## 5. Getting the tools it lacks
- Exists: fm plugins find/install/suggest (fmplugins.py:611-857; suggest uncalled); fm mcp new (server + test; register
  only prints); fm ask plugin --pin (USER_ONLY); project skill = recipe (execute.md:40); failure_class detects
  "command not found" only to excuse (fmcli.py:4783).
- Missing: "can't do X" → find-or-build trigger; test-then-use loop for built tools; skill/script scaffold; durable
  install-grant queue.
- Gaps: capability-miss trigger (4) · build-test-use loop (3) · skill new/script scaffold (3) · install-grant queue (3).

## 6. Verifying anything
- Exists: evidence --run/--repeat/--inconclusive/--expect-fail; fm prove (vacuous/--same/--hunks); finish --claim;
  fm check; UI: shot/flow/smoke/critique --brief/stories/design check/img diff; fm data (schema only).
- Missing: data/infra/ops proof kinds; docs-vs-code truth; perf baseline gate; per-domain unproven rollup; intent proof
  beyond an LLM lens.
- Gaps: proof kinds for data/infra/docs/perf (3) · unproven rollup labelled everywhere (4) · intent proof (4).

## 7. Self-repair and self-improvement
- Exists: capture_friction (fmcli.py:3984); fmfriction.due reflect action; stranger findings → self FIX; fm evolve
  (keeps past fmbench.gate, leaves a branch); fmnight court/lesions/evolve; fmtrials (proposes revert only); backtest
  (report); failures.jsonl (hints only).
- Missing: signal → evolve trigger; failures consumer that fixes; actioned trial verdicts; gate for Python/hook/guard
  self-changes.
- Gaps: signal→fix loop (3) · trials default + actioned (3) · code self-change gate (4).

## 8. Calibrated judgment
- Exists: confidence=N on tasks; fmoutcomes.calibration (Brier, in digest/cost); plan misses → autonomy slow; fm decide
  --kind reversible|costly|outward, --review, --ask (defaults/taste/precedent); guard categories; risk budget 6/day;
  fm research ask.
- Missing: low confidence or [assumed] → research; calibration feedback; irreversible-and-ambiguous classifier;
  decision confidence; --kind verified.
- Gaps: unsure → research trigger (3) · calibration feeds thresholds (3) · irreversible∧ambiguous stop rule (4).

## 9. Orchestration
- Exists: fm lane new/spike/race/pick/brief/resume/merge (fmlanes.py); lane brief prints an Agent line (sonnet, effort
  by tier, fmlanes.py:608-633); fm run spawns `claude -p` (fmserve.py:435-438, :935), --parallel lanes, _integrate
  merges; --models by tier (empty default); stalled()/stopped()/resume --force; fm run stall-kill + resume, usage-limit
  backoff, quarantine; fm budget, --max-usd.
- Partial: no model router (fmcost._by_model reports, nothing consumes); lane recovery needs the main session.
- Gaps: history-based model router with escalation (3) · auto-recovery of Agent lanes (3) · default models (3).

## 10. Beyond code
- Exists: fm research ask (quote-on-page verification, cross-check); research gate; fm docs (report-only); fm release
  (Foreman repo only) / fm ship; fm design lint, looks, scene, visual diff; incident/observability playbooks (prose);
  ~60 infra cards + guard asks on live apply; fm data (read-only); sql/migration playbooks.
- Missing: incident verb/gate; infra tools as proof (terraform validate, hadolint, helm lint, kubectl --dry-run);
  data correctness proof; docs truth; release ritual for other repos.
- Gaps: incident ritual (3) · infra proof (3) · data/migration proof (3) · docs truth (3) · release for any repo (3).

## 11. Self-triggering
- Exists: fm night (flock, budget, orders first, fm run --fit --max 2); --print-timer (prints only); fm orders
  (--every, --on-change sha1; captures only); fm serve (Remote Control unit); fm run (all-projects, inhibit);
  fm ship --watch / fm ci-watch (post-push); fm inbox gh (manual).
- Missing: staged install for one yes; unattended issue/CI polling; trigger table (event → type/tier/route); live
  watcher; L tasks from triggers.
- Gaps: install queue (3) · unattended issue/CI watch (3) · trigger→task routing table (4) · live watcher (3).

## 12. Staying lean and safe
- Exists: fm burden (report, no threshold); --by-verb (unused verbs, advisory); bench_hooks.py per-hook p95 budgets
  (exit 1); check_hook_slo (WARN); injection ceilings 2000/400 chars (FAIL); check_footprint ceilings (rules 80 lines /
  6400 chars, descriptions 6000, SKILL.md 10000); guard protected core, ~12 guard test files, fm canary.
- Missing: generation-over-generation "may not grow" ratchet; subtract-as-you-add balance gate; doctor in merge path.
- Gaps: lean ratchet per generation (3) · add/remove balance gate (3).

## 13. Genesis as a feature
- Exists: fm genesis storage (T-2078: init/put/status); fm mission compose (works with no request); fm ideas falsify,
  crossbreed, misses/questions, --seen; fm loop; fm scout idle; hook routing hint (fmhooks.py:1245); fm evolve (targets
  skills/rules/agents/routing only, train split); fm second roles; fm run.
- Missing: gen-0 writer from one line or nothing; Seed/mission/critique writers with the 8-mission cap; per-project
  capability spec + held-out exam; selection, lineage, carry-over; evolve on templates; drift check vs gen-0;
  one-shot completeness sweep; auto-start from loop/scout; routing change (core → queued for the user).
- Gaps: tower orchestrator (4) · multi-language exam generator with keys and holdout (3) · per-project spec (3) ·
  selection + lineage + carry-over (3) · drift check + sweep command (3).

## Gen 1 ordering (largest gaps first, dependencies honoured)
1. #13 tower + exam generator (everything else is graded by it).
2. #1 project initiative (find → prove → fix), which the exam's no-request scenarios grade.
3. #4 goal ledger and done-vs-stopped.
4. #2 exhaustive thinking gate + auto race.
5. #5 capability-miss trigger + build-test-use.
6. #6/#10 proof kinds (docs truth, data, infra, perf) and the unproven rollup.
7. #7/#8 signal → fix loop, calibrated stop rule.
8. #9/#11/#3/#12 router, triggers + install queue, anticipation model, lean ratchet.
