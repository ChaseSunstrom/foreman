# Brainstorm — lens: bold bets

- **Find the one input where the user's words split** — FEATURE — value 5 — effort M — risk med — category: intent
  Why: the request ends with "does it do what the user meant", and T-2613 shows false dones that match the goal's names but not its sense. Two blind tool-less children each read only the user's verbatim words and write a behaviour spec. Foreman searches for a concrete input where the two disagree, runs the built thing on it, and shows the user that one input and output. The user answers once; the answer becomes a steer and a test.
  Done when: on a fixture goal with a planted ambiguity, `fm verify meant` surfaces an input that separates the two readings. A goal with no ambiguity prints "no split found, intent unproven beyond the stated checks".

- **Make red-first work for every proof kind** — FEATURE — value 5 — effort L — risk med — category: proof
  Why: `fm task prove` shows a unit test failing without the change, but UI, docs, data and perf proofs have no parent-commit equivalent. Run each proof against the parent tree and the child tree, store both artifacts side by side (shot, flow trace, doc diff, row diff, timing), and refuse "proven" if the parent was already green.
  Done when: a UI fix task closes with a before shot and an after shot. A fixture task whose proof passes on the parent is rejected as vacuous.

- **Keep an unproven ledger with the cheapest next proof** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: the request says whatever can't be proven gets labelled. Labels in a final report are read once and lost. Each "unproven" becomes a ledger row with its risk, the cheapest action that would prove it, and who can do it, with a burn-down in `fm status`.
  Done when: closing a task with an unproven claim adds a row. `fm unproven` lists rows ranked by risk per proof cost. A later proof flips the row to proven.

- **Replay real usage against the change** — FEATURE — value 5 — effort L — risk med — category: regression
  Why: assumption: unit tests miss behaviours that real inputs exercise. Record the project's own CLI invocations or HTTP requests locally, redacted and never leaving the machine. Replay them on the parent and the child tree, cluster the output diffs, and ask the user only about clusters not explained by the task.
  Done when: a fixture app with a planted unintended side effect shows it as an unexplained cluster. No recorded payload appears in any outbound call (checked in a network namespace).

- **Probe live infra through a read-only valve** — FEATURE — value 4 — effort L — risk high — category: ops
  Why: infra and ops claims ("deployed", "unit is active") are only provable against the real system. A probe lane gets an allowlist of read-only verbs (systemctl status, SELECT, describe, GET) enforced by the guard, and writes evidence with timestamps. Any mutating verb is refused.
  Done when: a probe of a fixture service records its state. A `systemctl restart` through the lane is refused by the guard, with the refusal logged.

- **Prove access control with a two-role matrix** — FEATURE — value 4 — effort M — risk med — category: security
  Why: nothing in the pack proves authorisation. `fm flow` drives the web UI as role A and role B and requests every discovered route. The result is a route × role table of allowed or denied, diffed against the declared policy, with unreachable cells marked unproven.
  Done when: a fixture app with one route missing its check fails the matrix naming that route. A clean app prints a complete table.

- **Run flows through an environment and chaos matrix** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: `fm shot` and `fm flow` verify one viewport and one state. Add dark mode, reduced motion, narrow width, RTL, a non-UTF-8 locale, a slow network and a killed backend, with cheap pixel and DOM checks for each.
  Done when: `fm flow --matrix` produces one shot per cell. A fixture page that overflows at 360px fails that cell only.

- **Execute the docs** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: the README quotes counts such as "2117 files" that went stale and carries fenced commands. Run every fenced command in a fresh clone, check each flag against `--help`, resolve each named path and symbol, and regenerate each documented screenshot with `fm shot` to diff against the committed image.
  Done when: a doc with a renamed flag, a deleted path and a stale screenshot fails on those three items. An unchanged doc passes.

- **Rehearse data changes on a scratch clone** — FEATURE — value 4 — effort M — risk med — category: data
  Why: the data proof kind in the request has no verb. Apply a migration or transform to a copy and compare row counts, nullability, foreign-key orphans, uniqueness and a sample of rows before and after. Run the reverse step to test reversibility.
  Done when: a fixture migration that drops 3 rows is caught with the row ids named. A lossless one prints "reversible: yes, ran it".

- **Check performance claims by growth rate** — FEATURE — value 3 — effort M — risk low — category: performance
  Why: T-2605 compares wall time on a loaded bench, but "faster" can still hide quadratic growth. Run the changed path at n, 2n and 4n, fit the exponent, and refuse "faster" unless the confidence interval excludes zero change. Otherwise it says "inconclusive".
  Done when: a fixture O(n²) function is reported as growing quadratically. A noisy no-op change is reported inconclusive.

- **Show a proof atlas of modules by proof kind** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: assumption: the user can't see where Foreman has never verified anything. The web UI shows a grid of modules by proof kind (test, shot, flow, doc, data, perf, intent) with the last-verified date and a stale banner, and each empty cell links to its unproven-ledger row.
  Done when: the page renders from existing ledgers alone. A module with no proof of a kind shows an empty cell.

- **Convene a think-aloud persona panel (wild)** — FEATURE — value 3 — effort L — risk med — category: usability
  Why: wild. The request asks for UI proof, but a screenshot can pass while the screen is confusing. Local vision-capable personas (novice, rushed, keyboard-only) narrate each step of a flow with its shot. Foreman reports the steps where two or more got lost, as an opinion marked unproven.
  Done when: a fixture flow with an unlabeled button is flagged by at least 2 of 3 personas. The report states that it is a model opinion.

- **Bet against your own claims (wild)** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild; assumption: proof effort is spread evenly. Before verifying, Foreman writes a probability that each claim will fail, using the bets ledger, and spends extra proof on the claims it is least sure of. The finish card lists the bets that were wrong.
  Done when: each claim in a fixture closing report carries a pre-registered probability. A claim flagged high-risk gets a second proof kind.

- **Verify on a real phone over adb (wild)** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild; assumption: web UI bugs often show up only on real hardware. `fm shot --device` opens the page on an attached phone or tablet over adb, captures the screen, and runs the viewport checks on the real browser. With no device attached it says "device proof not available".
  Done when: with a device attached, a shot comes back from it. Without one, the proof is labelled unproven rather than silently skipped.

Next question: Which of the proof kinds in the request has the user actually had to do by hand in the last month, and which of those would they trust a model to judge alone?
Next question: What would a false "proven" cost the user for each proof kind, so the effort goes first to the kinds where a wrong pass is most expensive?
