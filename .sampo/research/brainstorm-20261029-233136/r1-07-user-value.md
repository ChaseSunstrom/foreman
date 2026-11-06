# Brainstorm — lens: user value

- **Write gen-0 from one line or nothing** — FEATURE — value 5 — effort L — risk med — category: genesis core
  Why: Gap map #13 tier 3 is missing; the user's Genesis request starts from a hand-written SEED_PROMPT.md. A stranger project can't use Genesis until Foreman drafts the equivalent itself from "make this great" or an empty prompt.
  Done when: on a held-out generated project, `fm genesis init` with an empty or one-line prompt writes a gen-0 file whose MUSTs, NEVERs and sections cover every item of the hand-written reference, checked by `fm exam grade`.

- **Show a one-screen gen-0 draft for a yes before the tower runs** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: assumption: a self-written gen-0 that silently becomes the contract is the biggest drift risk. The user steered on "genuinely smarter, not hardcoded", and gen-0 is verbatim and read-only once written. A single approval step makes it theirs.
  Done when: `fm genesis init` prints gen-0 as a short digest (MUSTs, NEVERs, sources it drew from) and writes nothing under the tower until the user confirms or passes `--yes`; a test checks that nothing is stored before then.

- **Draw each NEVER and MUST from the user's own corrections** — FEATURE — value 5 — effort M — risk med — category: personalization
  Why: The pack's steers and drops (e.g. "no idea killed for ambition", "weakness-finding by outside signals only") are standing rules that otherwise get retyped each run. The gen-0 writer should lift them in with a citation of where each came from.
  Done when: a gen-0 for this repo contains the standing rules above, each with a link to the originating steer, and a fixture with a planted correction shows it appear in the draft.

- **Auto-start Genesis when the queue runs dry, as a proposal first** — FEATURE — value 4 — effort M — risk high — category: autonomy
  Why: The request says it "starts on its own when the queue runs dry". The routing line in rules/foreman.md is protected core, so it needs a candidate plus the user's yes. Open work here is mostly deferred and blocked items, so "dry" needs a precise definition.
  Done when: with an empty ready queue, `fm loop` writes a one-line proposal and a candidate rules diff and starts nothing until approved; after approval a test shows the tower starting once and not twice.

- **Give each project a capability spec with a held-out exam** — FEATURE — value 5 — effort L — risk med — category: spec and exam
  Why: Gap map says "per-project spec with held-out exam" is missing (tier 3). `fm exam gen` already makes 11 scenario kinds across 6 languages with a held-out third, so the work is deriving the spec from the project and feeding it in.
  Done when: `fm genesis spec` writes a spec for a fixture project, and `fm exam gen` produces at least 9 scenarios with at least 3 held-out from it; the authoring child has no tools.

- **Print a plain status: what Genesis did, what it cost, what it closed** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: The user keeps asking for the tower to be readable (in-depth per-generation views on the page, docs readable in full). A summary per generation (scenarios closed, dollars, minutes, what lost and why) is what a returning user wants first.
  Done when: `fm genesis status` ends with a line per generation reading "closed X of Y, $Z, N min, winner: gen-N", and the same line appears on the site page.

- **Cap a Genesis run with a budget and a stop rule the user sets** — SECURITY — value 4 — effort M — risk low — category: guardrails
  Why: assumption: an unattended tower can burn a week of usage on one project. The environment itself shows a hard USD budget, so a per-run dollar cap and a "stop when a generation closes nothing new" rule are natural.
  Done when: `fm genesis run --budget 10` halts after crossing $10 with the state resumable, and a test with a stubbed cost meter shows it stopping mid-generation.

- **Block selection from winning by editing the exam** — SECURITY — value 4 — effort M — risk med — category: integrity
  Why: The user's steer says weakness-finding uses outside signals only and exam scenarios come from a tool-less author. A rewrite that edits scenarios, keys or the held-out third would otherwise win cheaply.
  Done when: selection hashes exam files and keys at gen start, and a test where a rewrite changes a scenario is rejected with a clear reason.

- **Keep a not-yet ledger and retry it automatically each generation** — FEATURE — value 4 — effort M — risk low — category: ledger
  Why: The user's standing rule: a failed spike gets at least two different approaches, then goes to not-yet.md with its blocker, retried each generation. Gap map lists this as missing (tier 3).
  Done when: a fixture with a failed spike appears in not-yet.md with its blocker, and the next generation's brief lists it with the attempts already made.

- **Wild: let a stranger's repo run "make this great" and return a one-page report card** — FEATURE — value 4 — effort L — risk med — category: demo (wild)
  Why: wild. A single command on any cloned repo that ends in a page with before/after exam scores against plain Claude Code. It doubles as the evidence behind the unbuilt scorecard items (T-0866, T-0867).
  Done when: running it on three public fixture repos produces three pages, each with arm scores and cost.

- **Wild: let the tower interview the user for two minutes when history is thin** — FEATURE — value 3 — effort M — risk low — category: cold start (wild)
  Why: wild. In a fresh repo there are no corrections to learn from, so a tool-less child asks at most five pointed questions (what must never happen, what does "great" mean here) and records answers verbatim as gen-0 MUSTs and NEVERs.
  Done when: in an empty-history fixture, at most five questions are asked, and each answer appears verbatim in gen-0.

- **Wild: carry a personal "taste profile" across projects** — FEATURE — value 4 — effort M — risk med — category: carry-over (wild)
  Why: wild. The request says to carry over winning Seeds, mission templates and lenses as defaults. Going further, a local, inspectable profile of what this user always asks for (site polish, tests first, no hardcoding) lets a new project's gen-0 start where the last ended.
  Done when: a second fixture project's gen-0 includes at least two defaults sourced from the first project's profile, each labelled with its origin, and deleting the profile removes them.

- **Wild: have the weekly site page show "what Genesis learned about you"** — FEATURE — value 2 — effort S — risk low — category: delight (wild)
  Why: wild. The live tower page already updates itself. A short panel listing the standing rules, lenses that paid off and the rewrites that lost makes the system's memory visible and correctable.
  Done when: `fm genesis export` emits that panel and each entry carries a remove control that edits the profile.

Next question: What counts as "queue dry" in a project where most open items are deferred or blocked, and who decides?
Next question: When a self-written gen-0 and the user's later correction disagree, which one wins, and where is that recorded?
