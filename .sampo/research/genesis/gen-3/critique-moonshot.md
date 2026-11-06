# Critique — Mission 8, moonshot (gen 3, #8)

Tasks: T-2687 (the spike, done), T-2688 (M-13's need, done). Mission: gen-3/mission-moonshot.md.

## Closed vs planned
- The spike (T-2687) ran M-12's kill test, and the verdict is not-yet. On 22 failed and 22 era-matched held closes
  (label: a fix or revert within 14 days of the close), no forecaster beat chance: a Haiku planner and a Sonnet cold
  rival reading the brief and diff scored AUC 0.58 and 0.50, and two record-based forecasters (type-and-tier held
  rate, and the held rate of earlier closes on the same files) scored 0.49 and 0.48. The log-weighted pool scored Brier
  0.286 against the best single's 0.275, a margin of -0.011 with a 90% bootstrap interval of -0.039 to +0.016.
  moonshot.md holds M-12 at Stage kill with T-2687 as Evidence; not-yet.md holds its blocker and two tries.
- The script and every model answer are kept in bench/moonshot/ (kill_m12.py, m12-answers.json, m12-result.json), so
  the verdict reruns at no model cost, and M-02's kill script sits beside it.
- M-13 was not spiked: its kill test needs refusals, and the ledger had 55 approvals and none. Grounding found that
  chat-ask declines were already logged (approval_declined, none ever written), but AskUserQuestion answers were not
  logged at all. T-2688 now logs each one as question_answered: default taken, another option, typed, or dismissed.
- The campaign floor for gen 3 is met by M-02 at kill (T-2679), written as "Advanced: M-02 kill (T-2679)" in the Mission.

## Outside signals
- None from a user. The labels are Foreman's own outcome record (fm outcomes), which counts a later FIX naming a task
  or a Revert commit, signals the closing agent didn't author.
- The cold read of moonshot.md refused the first not-yet entry: it said two runs of one design were one approach, not
  two. That was right, and it led to the record-based forecasters as a real second try.

## What failed
- The first run was confounded and nearly filed as the verdict. Its held closes came from closes whose survival window
  had ended, and those were all T-0014 to T-0198, while its failures spanned T-0087 to T-2542. The base rate scored AUC
  0.08, which looked like a strong inverted signal and was only era. Checking each class's id range caught it. A kill
  test now names how its classes were drawn and checks that they share an era before anything is read from it.
- The base rate first counted fates settled after the close it was forecasting (later fixes on older work), a second,
  smaller leak. Run 3 counts only labels settled 14 or more days before the forecast close.
- The forecasters were given too little to have signal. A brief and a diff don't predict a fix in this project. What
  might is at close but unused: the verification grade, the unproven kinds (T-2635), the test evidence. The unblock
  line in not-yet.md names them.
- The pool rule itself is a lesson: a pool can only beat its best member when the members carry independent signal.
  The kill test checked this cheaply before any market was built, which is what it is for.

## What the next Seed should change
- A kill test that compares two classes reports each class's era (id or date range) and fails itself when they don't
  overlap, before any score is read.
- M-12's retry adds one forecaster from what is known at close (verification grade and unproven kinds) to the same
  script; the market is built only if that forecaster alone beats chance.
- M-13's kill test can run once question_answered holds 20 or more rows; a deferred check task should hold that date.
