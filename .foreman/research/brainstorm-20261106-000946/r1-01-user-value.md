# Brainstorm — lens: user value

Lens: user value — what this user actually gets out of Sampo that they didn’t get from plain Claude Code, and whether it shows up in their own words. Their asks keep circling the same need: *prove to me it did what I meant, and stop making me re-ask.* The decider is the lever that finally pays it off.

- **Print "Sampo saved you X minutes this week" — computed, not claimed** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: the user's own words ask for "minutes saved per week" and a cost-of-interruption gauge, but every prior idea only *described* such a number. Value is felt when it's net of false alarms and reproducible: join the decider's verdicts to the ledger's outcome rows (accept / later-fix / undo), count the tasks it closed unprompted, subtract the review minutes the user actually spent (from the finish-card edit distance). Evidence: T-0867 "published held-rate scorecard" is blocked on bench cases; this reuses closed-task outcomes already on disk.
  Done when: `sampo value` prints a weekly minutes-saved number with the per-task receipt behind it, and it reads zero on a run with no closes.

- **The decider's first job is "did this close hold?" — wired to a real path** — FIX — value 5 — effort M — risk med — category: user value
  Why: T-2966 (loop breaker) and the false-done corpus exist, but the decider has no slot that answers the user's recurring pain of re-opening work. This is the one slot the pack implies and nobody has tied to `decide()`: label from the user's own undo (their words literally ask for that), abstain with a named reason, fall back to today's rules. It's the highest-value slot because a wrong close costs the user a re-ask.
  Done when: on `sampo task finish`, the close-verifier emits a typed verdict (holds / will-not-hold / abstained) that appears in the finish card, and a held-out set of the six false dones flips at least 3.

- **One line at session close: "here's what I stopped making you do"** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user's steers are all about Sampo not blocking, not interrupting, not making them re-ask. A close-time line that names the specific hand-steps removed *this session* (vs. a vague dashboard) is the value made visible. Evidence: their words keep asking to "show what I stopped doing" and "print what you no longer have to do."
  Done when: the last line of every finished session lists the top 3 user-hand-steps Sampo took off their plate this run, each linked to the ledger row.

- **Pre-draft the user's pushback, so they correct before I ship** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: the user's best data is their own corrections; they've repeatedly had to file the "I meant X not Y" after the fact. A decider slot that, at close, drafts the one sentence they'd most likely object to lets them veto a *class* before it lands. This is the unspoken need behind "I'll be annoyed if…" at intake.
  Done when: the finish card shows a one-line predicted objection the user can confirm or dismiss with one key, and the ledger records which objections were right.

- **Make "Sampo is earning its tokens?" a number in `sampo doctor`** — FIX — value 4 — effort S — risk low — category: simplicity
  Why: the user steered explicitly: budgets are a backstop, never a cap on getting work done — so the real question is marginal value. A single line, computed from the close-verifier's hit rate minus the review cost, tells them when a capability is dead weight and when it's paying. Ties to their "is Sampo still earning its tokens" ask.
  Done when: `sampo doctor` prints one verdict line per capability (earning / breaking-even / not), backed by the ledger, and the ship gate warns when a capability crosses to "not."

- **A "no model" baseline that the decider must beat, every Rune** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: the user's standing rule is that weakness-finding uses signals Sampo didn't author. The cleanest signal of *user* value is: does the trained model beat plain retrieval (kNN over closed briefs) on the same held-out closes? If not, the model is decoration. This turns "better than what?" into a permanent, cheap gate. Evidence: T-0035 (eval capture from real failures) already collects the cases.
  Done when: every Rune's scorecard shows decider-vs-kNN per slot, and a slot that loses to kNN is auto-flagged for retirement.

- **Cold-start the *user*, not the repo, on a brand-new project** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: the user wants the model generic across every Sampo project, not just this repo. The value on a fresh project is the user's *taste* (how they close, what they undo, their phrase compression), not repo structure. A project-fingerprint that seeds the decider from the user's other projects — weights/priors, never raw text — is the genericity they asked for, made felt on day one.
  Done when: a new project with <20 briefs gets a working close-verifier (abstains mostly but right when it speaks) in minutes, with no project-specific training, and a provenance note showing which sibling priors were used.

- **Let the user's silence be a label, with a visible trust score** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user goes quiet; the pack's own questions ask what that means. Treating "no response in 48h" as a soft "not wanted" — surfaced as a trust score they can override — converts their most common signal into training without a single new label. Their words: "let the user's silence be a label."
  Done when: the ledger carries a silence-derived label class, and the user can flip any one with one key, with the change feeding the next retrain.

- **wild — "What would break if I said no to this steer?" at the moment it's stored** — FEATURE — value 3 — effort M — risk med — category: user value (wild)
  Why: the user files steers constantly but never sees their blast radius. A decider slot that, at steer-store, computes which open tasks and which future closes depend on that steer — and shows the count — makes each steer's value concrete and warns before a steer quietly orphans work. This answers the left-question "what breaks when I say no" from the *user's* side, not the model's.
  Done when: storing a steer prints "N open tasks, M closed tasks rely on this," and removing it re-flags exactly those.

- **wild — The decider drafts the user's *next* steer before it's said** — FEATURE — value 3 — effort L — risk high — category: user value (wild)
  Why: the deepest unspoken need is that Sampo should anticipate their intent, not just react. The user's words show they re-phrase and re-ask a lot; a slot that, after a close, drafts the one steer they'd plausibly want next (in their own compression) and waits for a yes/no is the highest-leverage delight — and it's testable against their actual later steers.
  Done when: on 10 of the user's real past closes, the drafted steer text-matches (similarity > threshold) a steer they actually filed within 3 days, with the ledger recording each hit.

- **wild — A "decider obituary": the model retires a slot itself when it stops earning** — FEATURE — value 2 — effort M — risk low — category: simplicity (wild)
  Why: the user's lean rules punish growth that doesn't earn its tokens. Letting each slot write its own retirement (with the last 14 days of evidence) when its hit-rate drops below the kNN baseline makes Sampo's value self-governing and gives the user a receipt of what was cut. It's the value-honesty flip of their "no idea is killed for ambition" rule: keep ambition, retire only dead weight.
  Done when: a slot that loses to kNN for 2 consecutive Rungs auto-files a retirement with its evidence, and the user sees it in the morning card.

- **One "what I took you to mean" receipt, at every close** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user's most repeated friction is scope/interpretation drift (the "I meant X not Y" class). A one-line receipt at close that states Sampo's interpretation of the ask, beside the user's own words, makes every misread visible in one glance — and is the cheapest training signal the decider can harvest. Their words literally ask to "print what I took you to mean as a diff."
  Done when: every finish card carries a one-line interpretation and the user's original sentence side-by-side, and a mismatch flag appears when edit distance exceeds a threshold.

Next question: what is the *smallest* user-visible action that closes the loop between a decider verdict and the user's trust — a key, a card, a chime — so "value" is felt before it's measured?
Next question: does the user value *less* Sampo (fewer things it decides) or *better* Sampo (more things it decides right) more, and does the pack give evidence for which?
