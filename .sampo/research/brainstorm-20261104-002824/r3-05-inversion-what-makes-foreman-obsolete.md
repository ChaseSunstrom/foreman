# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Bound every predictor by its ceiling before building it** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: The pack lists many predictors (n-grams, follow-up tables, baselines) but nothing that asks whether the user's asks are predictable at all. If they aren't, anticipation is obsolete from day one.
  Done when: `fm anticipate ceiling` reads only the ledgers and prints, per task kind, a hindsight-oracle hit rate next to the recency baseline, and says "not worth building" where the gap is under a stated margin.

- **Measure each warning's lead time over the next tool that would have caught it** — FEATURE — value 4 — effort M — risk low — category: problem flagging
  Why: The request says "flags problems before they happen". A flag the compiler, test run or CI would raise within a minute adds nothing, and that is how flagging becomes obsolete. Assumption: ledger timestamps can be joined to later test, lint and CI failures.
  Done when: each flag type has a median lead time over the first independent detector, and flag types with a median under 60 s are muted with the number shown in `fm doctor`.

- **Shadow-compare each hand-rolled detector with the host's native signal, and delete it when they agree** — CLEAN — value 3 — effort M — risk med — category: drive
  Why: Five tasks in the pack (T-0575, T-0115, T-2873, T-2900, T-2901) each patched the drive's own scan for running subagents. Every patch is a heuristic that goes obsolete once the host's background list is reliable.
  Done when: each heuristic logs agree/disagree against the host list. One at 100% agreement over 30 days files a deletion task that carries those counts.

- **Fold the vocabulary across the Foreman→Sampo rename in the predictor** — FIX — value 3 — effort S — risk low — category: anticipation
  Why: The rename (fm → sampo, `foreman:fm-` → Sampo spellings) splits the ledger's counts between old and new names. A text-keyed predictor trained across that boundary quietly goes stale. The pack also shows an old-name census was needed.
  Done when: a predictor test fed `fm ship` and `sampo ship` rows counts them as one key, using the existing renames map.

- **Detect the predictor feeding on its own output** — FIX — value 4 — effort S — risk low — category: anticipation
  Why: Many ledger rows are Foreman-filed (ci, self, discovered, tower, brainstorm). Predicting "the next ask" from those rows just predicts Foreman. The user-authored-only filter appears in the pack only for the site's hit rate.
  Done when: every prediction shows the share of its evidence rows the user wrote. Above 20% Foreman-authored, it is suppressed and `fm doctor` names the share.

- **Catch rubber-stamping of drafts and of Exam readings** — SECURITY — value 4 — effort M — risk med — category: trust
  Why: The pack asks which Exam readings the user trusts enough to skip the diff. If they accept without reading, a drafted lane commit is effectively unreviewed and review has become obsolete as a control.
  Done when: accept latency is compared with diff size locally. An accept faster than a plausible read, repeated three times, makes the next draft re-run its Exam live and show that reading before it can land.

- **Predict which host-blocked tasks the next upstream release will unblock** — FEATURE — value 4 — effort M — risk low — category: host drift
  Why: T-0325, T-0335–T-0337, T-1217 and T-1366 are blocked on host or OS limits. When the host closes a gap, the workaround becomes obsolete, and the user should hear about it before they trip over it.
  Done when: each blocked task carries a one-line "host gap" probe. A nightly run checks them against the installed CLI version and changelog and drafts the unblock or deletion brief when one flips.

- **Census where asks are typed (CLI, web UI, pasted, voice)** — FEATURE — value 3 — effort S — risk low — category: surfaces
  Why: Anticipation cards are assumed to land at session start in a terminal. If the user's asks migrate to another surface, the card is read by nobody. Assumption: the intake record can carry a source tag.
  Done when: `fm doctor` shows a weekly ask-origin split, and the card follows the surface with the largest share.

- **Skip drafts for asks cheaper to type than to review** — PERFORMANCE — value 3 — effort S — risk low — category: anticipation
  Why: A five-word habitual ask costs the user more to review than to retype. Drafting it only adds reading work. This sharpens the existing "draft only when it beats the queue" idea with an actual cost comparison.
  Done when: the drafter logs estimated review seconds against typing seconds and drafts nothing where review is longer. A test pins both cases.

- **Run a Challenger Foreman nightly against the real one (wild)** — FEATURE — value 4 — effort L — risk med — category: obsolescence
  Why: Earlier ideas compare against hand-picked rivals or ablations. Here a tool-less cold child is given only the host's docs and the user's last week of asks and builds a replacement config. It then runs the held-out scenarios in a scratch home against the live Foreman, and each capability is kept only while it beats the challenger.
  Done when: the morning card shows one line per capability, "beats challenger" or "challenger ties", with the config the child wrote saved to disk.

- **Teach through accepted drafts so the user's own file can replace Foreman (wild)** — FEATURE — value 4 — effort M — risk low — category: exit ramp
  Why: This inverts the product. Each accepted draft also appends one plain-language rule to a file the user owns, such as AGENTS.md. After a month, a replay shows how much of the hit rate that file alone reproduces on the host with Foreman off.
  Done when: the replay prints a "file-only retains N%" figure, and the file reads cleanly with no Foreman verbs in it.

- **Fit a lift-versus-capability curve across the model ladder (wild)** — RESEARCH-style FEATURE — value 4 — effort M — risk low — category: obsolescence
  Why: Time-based forecasts of "when the delta hits zero" need data that doesn't exist yet. The model ladder does exist: local 27B, Haiku 5.5, Sonnet 5.5, Opus 5.5, Fable 5.1. Running the discipline scenarios across it gives a lift curve per capability that can be extrapolated.
  Done when: one table shows each capability's lift at five rungs, with a fitted line and the capability level where the lift reaches zero, and the Models section of the site shows it.

Next question: Which of the user's own asks in the last 90 days would a generic model with no user-model have predicted equally well?
Next question: When a capability is found obsolete, what is the user's preferred exit: deleted quietly, kept as a thin shim, or handed to their own files?
