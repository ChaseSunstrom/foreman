# Brainstorm — lens: blind spots

- **Write the follow-up asks before shipping (pre-mortem)**: FEATURE, value 5, effort M, risk low, category: foresight (wild)
  Why: wild. T-2080, then T-2087 (match the site), then T-2088 and T-2090 (keep it live) were each a follow-up ask a "ship the tower page" pass could have predicted. The question to ask is: "What are the three messages the user sends after this ships?"
  Done when: closing a FEATURE task writes `expected-asks` (≥3 lines), each is marked checked or deferred before close, and a fixture task shows a "doesn't match the site" line failing a check.

- **Queue the siblings of every unpredicted ask**: FEATURE, value 5, effort M, risk low, category: foresight
  Why: "favicon still shows the old logo" was fixed alone, but the same class includes the README logo, og:image, manifest icons and the demo SVG. The question: "What else in this class shares the cause?"
  Done when: logging an unpredicted ask makes a tool-less child list ≥5 same-class candidates, and `fm queue` shows them tagged `sibling-of:T-NNNN`.

- **Flag features that were built but never run**: FEATURE, value 4, effort S, risk low, category: honesty
  Why: T-2077 (run the tower) came after the tower storage was built, so the user had to ask for the first real run. The question: "Has this capability ever run end to end in anger?"
  Done when: `fm genesis status` and `fm doctor` list capabilities with zero real invocations, and the list shrinks after one real run.

- **Re-record the demo when the UI it shows has drifted**: FEATURE, value 4, effort M, risk med, category: surfaces
  Why: the "site's fm code section is stale" ask shows screenshots and recordings (`demo/live.svg`) lag the code, not just the prose. The ask-surface lag measure from T-2073 covers pages, not recordings.
  Done when: changing files that `fmmap.drift` ties to the UI queues a re-record task, and a test shows the stale-demo flag clearing after re-recording.

- **Audit gates and tests for substring matching on prose**: FIX, value 3, effort S, risk low, category: reliability
  Why: the `test_ship` `--check` failure came from a commit hash ending in `add` matching the substring `add a`. The question: "Which checks match free text with `in`?"
  Done when: a scan lists every test or gate that does substring or regex matching on commit text or user prose, and the `test_ship` case uses an anchored match.

- **Batch the tasks that only the user can unblock**: FEATURE, value 4, effort S, risk low, category: queue hygiene
  Why: T-0325 needs `sudo pacman`, T-0352 needs a publish decision, and T-0418 needs an install. They sit "blocked" and nobody asks the user for them.
  Done when: `fm queue --needs-you` prints one card per user-only blocker, each with the exact command or yes/no, and answering a card unblocks its task.

- **Report which project kinds the exam never generates**: FEATURE, value 4, effort M, risk low, category: exam coverage
  Why: the exam covers 6 languages and 11 scenario kinds, but "any project" also means monorepos, docs-only repos, notebooks, infra-as-code, games and mobile. Assumption: none of those have fixtures yet.
  Done when: `fm exam gen --kinds` prints a project-kind × scenario-kind grid with empty cells marked, and Genesis refuses to claim "any project" while cells are empty.

- **Detect new steers that contradict standing ones**: FEATURE, value 4, effort M, risk med, category: charter
  Why: the standing steers include "no idea killed for ambition", "each exam ≥9 scenarios" and "outside signals only", and later steers or cost caps can collide with them. Assumption: no check exists today.
  Done when: adding a steer that conflicts with a stored one prints both with their dates, and a fixture pair (a cost cap vs `≥9 scenarios`) is caught.

- **Run Genesis on a frozen Foreman snapshot and grade it against the hand gen-0**: PERFORMANCE, value 4, effort L, risk med, category: dogfood
  Why: the mission exam says the self-written gen-0 must cover every MUST, NEVER and section of the hand-written one, and `research/genesis/gen-0.md` is that reference. Foreman itself is the one project that has one.
  Done when: `fm genesis selftest` writes gen-0 from "make this great" on a snapshot and prints MUST, NEVER and section coverage against gen-0.md, with scores logged to `exam.jsonl`.

- **Track a miss rate per lens and per stage**: FEATURE, value 3, effort S, risk low, category: observability
  Why: T-2076 feeds misses back, but nothing counts them. T-0829 (drop lenses that go dry) is deferred for lack of this signal.
  Done when: `fm ideas stats` shows, per lens, how many shipped asks it predicted against how many arrived unpredicted, over a trailing 30 days.

- **Learn a polish checklist from the user's own polish asks**: FEATURE, value 4, effort M, risk low, category: taste
  Why: "favicon", "match the site", "motion pass", "shared header" and "fm code section stale" are all one taste: new surfaces inherit the house look and stay current. Assumption: they are only handled one ask at a time.
  Done when: a new page or card fails the done-gate if it misses a checklist item learned from ≥3 past asks, and each item names the ask it came from.

- **Have a skeptical reader review every public page before auto-publish**: SECURITY, value 4, effort M, risk low, category: publishing (wild)
  Why: wild. `fm genesis live on` pushes to main with a standing grant. A tool-less "hostile commenter" child reads the page diff and flags claims no command backs, private paths and embarrassing wording.
  Done when: the publish step blocks on any flagged claim without evidence, and a planted fake pass-rate on a fixture page is caught.

- **Score a forecast of next week's asks against what arrives**: FEATURE, value 3, effort M, risk low, category: foresight (wild)
  Why: wild. Backtesting looks backward; a forecast made before the asks arrive can be scored honestly. Assumption: ask text is stored with timestamps.
  Done when: each Monday writes ≥10 predicted asks, and the following Monday records hits, misses and a calibration number on the Genesis page.

- **Give the user a "what did I forget to ask" card**: FEATURE, value 4, effort S, risk low, category: delight
  Why: the user's list shows they carry the checklist: favicon, stale section, motion, docs. A card could offer one unasked fix per day, taken from drift, the sibling queue and the polish checklist.
  Done when: the session start shows ≤1 line "you didn't ask, but X lags", and taking or dismissing it is recorded so it isn't shown again.

Next question: Which of the user's recurring asks are really one standing instruction ("keep every surface current"), and is that instruction stored anywhere a gate can check?
Next question: What does the first week look like for a stranger project where nothing predicts the user's asks, and how would Genesis know it was surprised?
