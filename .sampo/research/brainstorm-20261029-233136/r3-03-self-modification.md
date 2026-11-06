# Brainstorm — lens: self-modification

- **Demand a red-then-green scenario for every self-change** — FEATURE — value 5 — effort M — risk low — category: self-mod guard
  Why: assumption: Genesis edits its own templates, exam and lenses from evidence, and a change nobody can show failing before and passing after is a guess. The existing ideas log, sunset or revert changes, but none requires proof of need first.
  Done when: a self-change commit with no scenario that fails on the parent and passes on the child is rejected by `fm genesis`, with the reason printed.

- **Make each self-change predict its effect, then score the forecast** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: assumption: every change names the metric it should move and by how much (e.g. "tower cost per closed scenario −15%"). After N uses, predicted versus actual is compared. A proposer whose forecasts keep missing loses the right to self-apply and must ask the user.
  Done when: the ledger shows predicted and actual per change, and a fixture proposer that is wrong 3 times in a row is moved to ask-first.

- **Require a deletion for every addition** — CLEAN — value 4 — effort S — risk low — category: rule budget
  Why: evidence: the user steered Foreman toward "genuinely smarter" instead of an accreting hardcoded list. Self-written rules only ever grow, and the idea list covers trimming and context tax but not a hard net-zero rule.
  Done when: a self-change that raises the total line or rule count of the templates and rules without removing at least as many is refused.

- **Pin a behavior probe battery and diff it around every self-change** — FEATURE — value 5 — effort M — risk low — category: regression
  Why: assumption: the exam measures capability, but a template edit can silently change nudges, commands issued or token use on tasks the exam never touches. A fixed battery of ~20 prompts on a fixture repo, replayed without a model where possible, gives a side-effect diff.
  Done when: the diff output for a deliberately noisy template edit lists changed behaviors, and a no-op edit gives an empty diff.

- **Ablate one rule per night on a scratch copy** — PERFORMANCE — value 4 — effort M — risk low — category: dead-weight pruning
  Why: assumption: self-written MUSTs, nudges and template sentences pile up and nobody can tell which matter. Deleting one at random and re-running the cheap exam shows which are dead. This differs from re-ablating after a model change because it is continuous and per rule.
  Done when: after a sweep over a fixture ruleset with 2 planted dead rules, both are listed as "no exam effect" and proposed for removal.

- **Declare an editable-surface manifest and enforce it with a hook** — SECURITY — value 5 — effort S — risk low — category: boundary
  Why: evidence: the routing line in `rules/foreman.md` is protected core and needs a candidate plus the user's yes. That boundary is a convention today. A machine-readable list of paths Genesis may edit, may propose to, and may never touch makes it enforceable.
  Done when: a Genesis-authored write to a never-touch path is blocked by the hook, and a write to a propose-only path lands only as a candidate file.

- **Tier self-changes by reversibility** — SECURITY — value 4 — effort M — risk med — category: autonomy tiers
  Why: assumption: one rule for all changes is either too slow or too loose. A tier-1 template wording change auto-applies after the exam. A tier-2 change to the lens set or selection rule also needs a cold `fm second` review. A tier-3 change to the judge, exam or charter needs the user's yes.
  Done when: three fixture changes, one per tier, each take their own path, and the tier-3 change cannot merge without a recorded yes.

- **Mine the tower's own logs for its costliest stage and propose one fix** — FEATURE — value 4 — effort M — risk low — category: self-diagnosis
  Why: evidence: the tower has stage timing and cost per scenario, and the user's steers favour outside signals over self-opinion. The log is such a signal. Genesis targets its single most retried or most expensive stage rather than inventing improvements.
  Done when: on a fixture tower with a planted slow stage, the proposal names that stage and cites the log lines.

- **Let Genesis invent a lens when blind spots cluster** — FEATURE — value 4 — effort M — risk med — category: lens evolution
  Why: evidence: this very pack's lenses include invented ones ("cold-start stranger", "tower archaeology"), and the blind-spots lens collects unpredicted asks. Retiring and reviving lenses exists, but creating one from a miss cluster does not.
  Done when: given 3+ missed asks sharing a theme, Genesis drafts a new lens definition, and it is kept only if it produces an idea a held-out ask later matches.

- **Blind-grade vintage writers against each other on stranger fixtures** — FEATURE — value 4 — effort M — risk low — category: vintage tournament
  Why: assumption: a hall of fame stores old vintages but nothing decides whether the new gen-0 writer is really better. Each vintage writes gen-0 for the same unseen fixtures, and a tool-less child grades them blind against the hand-written gen-0's MUSTs and NEVERs.
  Done when: a new vintage is promoted only if it covers more hand-written MUST/NEVER/section items than the incumbent on fixtures neither saw.

- **Wild: Rebuild-from-gen-0 challenger** — FEATURE — value 5 — effort L — risk med — category: accretion test
  Why: wild, assumption: periodically regenerate the whole rule set from gen-0 and the user's steers alone, with none of the accreted patches, and run both through the exam. If the clean rebuild ties or wins, the accreted version is pruned toward it.
  Done when: a fixture harness carrying 10 junk patches loses to its clean rebuild, and the report lists the patches that never earned their place.

- **Wild: Self-change court** — FEATURE — value 3 — effort M — risk low — category: adversarial review
  Why: wild: for tier-2 and tier-3 changes, three tool-less children play prosecutor (how this goes wrong), defender (what it fixes) and judge (reads both and the exam diff). The transcript is attached to the ledger entry.
  Done when: a planted harmful change is convicted in a fixture run, and the court transcript shows up on the change's page.

- **Wild: Amendment cooling-off for the protected core** — SECURITY — value 3 — effort S — risk low — category: constitution
  Why: wild: any proposed edit to protected core files (routing line, guard) sits as a candidate for 7 days. It is re-shown in each morning digest, and the user's yes only counts after the wait, so an approval given in a rush doesn't ratify it.
  Done when: a candidate approved on day 1 stays inactive until day 7, and any further edit to it resets the clock.

- **Wild: Cross-breed templates between project towers** — FEATURE — value 3 — effort M — risk med — category: gene exchange
  Why: wild, assumption: two towers on different projects each have a winning Seed template. Splicing sections of both and testing the child on a third project's held-out exam might beat either parent, building on the carry-over defaults idea.
  Done when: a spliced template either beats both parents on a third fixture's held-out scenarios and is saved, or loses and its lineage is logged.

Next question: What does Genesis do when its own self-change tools, such as the exam, ledger or manifest hook, are broken or missing, and should it be allowed to modify anything at all in that state?
Next question: Which of the user's steers have been wrongly generalized into a self-written rule, and how would Genesis notice that without the user telling it?
