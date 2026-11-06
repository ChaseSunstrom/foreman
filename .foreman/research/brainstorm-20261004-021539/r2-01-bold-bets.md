# Brainstorm — lens: bold bets

- **Make every verdict-judging tool pass a "judge calibration" suite** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: Pass 2 review found two HIGH bugs in `fm task prove` (recorded a pass with nothing proven; a failing check "proved" everything). Judges of evidence (prove, oracle, bench, flake ledger, inconclusive) are the weakest link. Prior ideas covered vacuous verify detection, not a shared fixture bank for all judges.
  Done when: `fm calibrate` runs each judge against known-vacuous, known-failing, and known-good fixtures, and a deliberately broken judge (injected in a test) makes it exit non-zero naming that judge.

- **Collapse the review family into one `fm second` primitive with pluggable seats** — CLEAN — value 4 — effort M — risk med — category: review
  Why: Inbox has installed review skills as lenses, debate pair, shadow plan review, daily second-Foreman review: four items sharing "an independent seat reads X and returns findings with a repro". One primitive (target × seat × budget) halves the surface; some earlier ideas also say merge them.
  Done when: `fm second plan|diff|session --seat <lens|skill|model>` works for all three targets, and the four inbox items are closed as configurations, with a test per target.

- **Require a runnable repro on every reviewer finding, then auto-file it as a failing test** — FEATURE — value 5 — effort M — risk low — category: review
  Why: Every review pass found 3–7 real issues, mostly parser edge cases, and the same classes recur (git exec channels missed by the first pass). A finding without a repro is an opinion; with one it becomes a permanent regression seed. Differs from earlier "seed" ideas by making the repro a precondition for the finding to count.
  Done when: a reviewer finding with no repro command is rejected by `fm audit` as "unproven", and one with a repro lands as a failing test that must go green before the task closes.

- **Add a "premise ledger" for drops and PERF claims, measured at brief time** — FEATURE — value 4 — effort S — risk low — category: premises
  Why: Two recent drops were "premise false" after measurement (ghost background tasks 0/25, replay corpus 0.14 s vs 6.5 s). Work was briefed, then dropped. Measuring the premise first would have saved those briefs.
  Done when: creating a PERF or "fix X is slow/wrong" brief requires a recorded measurement command and its output, and `fm task new` refuses to proceed without one in a test.

- **Wild: Hold a "kill-switch auction" where every command and hook must bid its measured catches to stay** — FEATURE — value 4 — effort L — risk med — category: pruning
  Why: Dozens of verbs were added in a day, nudges are quieted ad hoc, and the user wants "groundbreaking" without bloat. Joins the existing catch reel, ablation, and spend data into a single retire-or-keep score per component. Assumption: usage and catch counts are logged per verb. Wild.
  Done when: `fm auction` ranks all verbs and hooks by catches per token and per second, and a test shows a never-fired verb listed as a retirement candidate with its evidence.

- **Wild: Run a "user-absence rehearsal": a child with only the ledger answers Foreman's own questions as the user would, and the disagreements are scored** — FEATURE — value 4 — effort L — risk med — category: autonomy
  Why: The user wants autonomy and "ping me only when needed", and has steered many times. Measuring how often a ledger-only proxy matches the user's actual past answers gives a number for whether it is safe to stay quiet. Wild.
  Done when: `fm rehearse` replays 20 past user decisions to a child, prints match rate by decision kind, and a test checks the scoring on a fixture of known answers.

- **Add a `fm landscape` scout that outputs diffs against a pinned census, not prose** — FEATURE — value 4 — effort M — risk low — category: research
  Why: The user asked to research what people want harnesses to do. A structured census (feature, source URL, verified quote, Foreman equivalent or gap) makes each run a diff, reusing fmresearch quote checks. Combines three overlapping inbox and brainstorm items.
  Done when: two runs against a stubbed source set print only the added and removed features, each with a quote that passes the verifier.

- **Cross-check research with an independent second retrieval path before it can be cited in a brief** — FEATURE — value 4 — effort M — risk low — category: research
  Why: Research quorum is open. The bold bit: an answer used as an assumption must have two sources that don't share a domain or a quote, otherwise it stays `[assumed]` rather than `[verified]`.
  Done when: a claim with one source or two same-domain sources is recorded `[assumed]`, and a two-domain claim is `[verified]`, tested on stubbed fetches.

- **Wild: Make Foreman's hooks a portable "done needs evidence" core that runs under any harness via a thin shim and MCP** — FEATURE — value 5 — effort L — risk high — category: portability
  Why: User wants better compatibility and the "best plugin possible"; AGENTS.md export and the MCP read-only server are open. The bold step is write-gating: the same brief and evidence rules enforced as MCP tools (`claim_done` rejects without runs). Assumption: other clients honour tool refusals. Wild.
  Done when: an MCP client calling `claim_done` on a task without passing evidence receives a refusal naming the missing criterion, and with evidence it succeeds.

- **Detect "turn ended only to wait" and replace it with a resumable parked state** — PERFORMANCE — value 3 — effort M — risk med — category: drive
  Why: 18 drive turns ended just to wait on a reviewer subagent. Earlier ideas proposed it; the narrow addition is measuring turns, tokens, and cache loss per wait as the acceptance number.
  Done when: a drive with one background reviewer shows zero extra turn-ends in `events.jsonl` over a fixture run, with tokens per wait reported by `fm cost`.

- **Wild: Give each finished task a "counter-brief" — the cheapest different plan that would also have passed — and show it in the proof pack** — FEATURE — value 3 — effort L — risk med — category: learning
  Why: Recall learns what worked, not what else would have. A tool-less child proposes a cheaper alternative, checked against the same criteria via `fm bench` replay. Feeds the tier and avoidance nudges with evidence. Wild.
  Done when: `fm proof ID --counter` lists one alternative with its replayed verdict and cost delta, and a failing alternative is labelled as such.
