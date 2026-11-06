# Brainstorm — lens: unspoken needs

- **Settle deletion and docs bets by non-resurrection** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: open question "what would a bet's settlement look like for work with no later signal". Subtraction is the lean mechanism, and a deletion that nobody notices would count as "survived" by default.
  Done when: a deletion or docs-only task settles as "held" only after 30 days with no revert, no re-added symbol and no new caller, and `fm outcomes` shows these as a separate row.

- **Count a subtraction only if total footprint fell** — FEATURE — value 4 — effort S — risk low — category: lean
  Why: assumption: weight can move instead of shrink. The repo has 1388 skill files, and lines could migrate to skills, site data, fixtures or the state dir. The cold read for metric-gaming may not see that.
  Done when: a fixture diff that deletes 200 lines in `plugin/lib` and adds 200 in `plugin/skills` is reported "relocated, not lean", and the lean row does not credit it.

- **Mute steer expansion for message shapes that never yield a method** — PERFORMANCE — value 3 — effort S — risk low — category: spend
  Why: the live expansion (T-2631) had a 19% method rate, yet every steer-shaped message is expanded in the background.
  Done when: `fm exam steer` prints method rate per message shape, shapes under a set floor skip expansion, and the skip is logged with its shape.

- **Draft a local revert when main goes red after a Foreman push** — SECURITY — value 4 — effort M — risk med — category: ship safety
  Why: the standing push grant lets Foreman push to main without asking. A post-push watch on main's CI is not in the pack.
  Done when: after `fm ship`, a red CI run on that commit produces an unpushed revert commit plus one `Next:` line in `fm next`, and nothing is pushed without a grant.

- **Link each costly decision to the decisions it rested on** — FEATURE — value 3 — effort M — risk low — category: steers
  Why: the "never block on the user" rule means many `fm decide --kind costly` entries stack up, but reversing one doesn't show what depended on it.
  Done when: `fm decide --reverse ID` lists every later decision that cites ID and files one re-open task per dependent.

- **Flag steers the user's recent words quietly contradict** — FEATURE — value 3 — effort M — risk low — category: steers
  Why: assumption: about 40 steers are "still in force", but the user's latest messages may supersede one without saying so. Current checks compare steers to each other and to new requests, not to what the user just said.
  Done when: a nightly pass compares the last 10 user messages with the steers and writes at most one non-blocking `fm next` line quoting both texts.

- **Ratchet the list of user-owned paths Foreman reads** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the user dropped the shell-history replay because it "adds privacy surface". That reads as a standing preference about new data classes. Write paths are inventoried, but read paths outside the repo and state dir are not.
  Done when: the suite fails if Foreman opens a path outside its read allowlist, and adding a path requires a `fm decide` record.

- **Rehearse every ship push against a local bare remote** — FEATURE — value 3 — effort S — risk low — category: ship safety
  Why: pushes are durable and outward-facing, and the grant is spent on use. A dry run should show the exact refspec, tree hash and server hooks before the real push.
  Done when: `fm ship` pushes first to a temp bare mirror and aborts if that tree hash differs from the gated one.

- **Pre-register and rehearse a shedding order for quota pressure** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: the user said never to skip work for budget, so when a cap bites the drive needs a pre-agreed order for what slows first. Otherwise degradation is improvised.
  Done when: a ranked shed list lives in one file, a fake-quota drill sheds in that order, and the guard, ledger and ship gate are never in the list.

- **Wild: Forecast the date the footprint hits a user-set ceiling** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: assumption: a lean target that is only reported after the fact doesn't change behaviour. Growth rate × ceiling gives a date that can sit on `fm doctor`.
  Done when: `fm doctor` prints "at +N files per week, ceiling hit on DATE", and the line turns red under 30 days.

- **Wild: Tune guard block wording by how often the model routes around it** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: open question "if a model is told it is guarded, does its behaviour change" has no measurement. Wording may decide whether the model complies or rephrases the command.
  Done when: two wordings run against the same replay scenarios and the report gives each one's route-around rate, with the lower one becoming the default.

- **Wild: Add a lone-sceptic child who may only argue a lean claim is false** — CLEAN — value 2 — effort S — risk low — category: measurement
  Why: assumption: the cold readers check against MUSTs, and no reader's only job is to disprove "this made Foreman leaner".
  Done when: for a sampled lean task, a tool-less child gets the diff and claim and must quote the line that falsifies it. A quoted line files a task, and no quote is logged as "unfalsified".

- **Wild: Give each retired capability a three-line obituary and a revival test** — CLEAN — value 2 — effort S — risk low — category: lean
  Why: standing rule: "only proven harm or exact duplication removes an idea, with the reason recorded." The same discipline for deleted code would show that lean cuts are reversible on evidence.
  Done when: each subtraction writes an obituary (what it did, why it went, what would bring it back), and `fm tidy` flags any whose revival condition is now true.

Next question: which lean or safe claims in the final report would the user check by hand first, and does Foreman already hold the command that checks them?

Next question: when a lean cut and a safety gate disagree on the same code, which standing rule decides, and is that recorded anywhere a cold reader could cite?
