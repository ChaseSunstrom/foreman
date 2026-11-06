# Brainstorm — lens: user value

Most of what remains after ~200 ideas is marginal. These seven are the only ones I think add value the list lacks, best first.

- **Let the user attest subjective criteria with one yes/no** — FEATURE — value 4 — effort M — risk low
  Why: the user never runs commands, yet "looks right", "reads well" and "feels faster" can't have a verify command. Those criteria end up weakly graded or padded with vacuous checks. The provenance-labelled evidence idea covers machine evidence, not user-attested evidence.
  Done when: a criterion marked `attest:` cannot pass `fm task done` without a recorded yes from the user's approval prompt, and the evidence is labelled `user`.

- **Redact secrets at capture, at evidence and in the diff** — SECURITY — value 4 — effort S — risk low
  Why: briefs store the user's words verbatim, and pasted errors and logs often contain tokens. Recall, digest, `fm serve` and `fm share` then spread them; only `share` is privacy-filtered. Assumption: no redaction exists at capture.
  Done when: a pasted `AKIA…` or `Bearer …` string is stored as `[redacted:aws-key]` in the brief and log, and `task done` flags a secret-shaped string added in the diff.

- **Park and preempt for urgent requests** — FEATURE — value 3 — effort M — risk med
  Why: there is one active task and new requests go to the inbox. "Prod is broken, drop everything" then waits behind unrelated work. Amendments and abandon cover neither case. Assumption: no preemption path exists.
  Done when: an urgent tagged prompt checkpoints the active task, focuses a new hotfix task, and after that task is done the hook's "Next" note offers to resume the parked one.

- **Bootstrap a minimal gate for projects with none** — FEATURE — value 3 — effort M — risk low
  Why: the verification grade is "weak" by construction where `fm map` finds no tests or gates, and onboarding only describes the project. Assumption: such projects are common among the user's repos.
  Done when: on a repo with no gates, `fm` proposes a syntax, import or smoke command, the user answers one yes/no, and the next task's grade can reach "ok".

- **Detect conflicts between repo instructions and Foreman defaults** — FIX — value 3 — effort S — risk low
  Why: repo CLAUDE.md or AGENTS.md may say "never commit", "run `make test`", or "don't touch vendor/", and Foreman's commit offer, gate detection and scope defaults can silently contradict them. Assumption: no precedence check exists today.
  Done when: a fixture repo saying "do not commit" suppresses the commit offer, and `fm doctor` lists each detected conflict and which side won.

- **Verify UI and HTTP changes with a stdlib fetch-and-assert check** — FEATURE — value 3 — effort M — risk med
  Why: front-end and service tasks are verified only by unit tests, so rendering and route regressions pass. This adds a start-server, `urllib` fetch and `html.parser` selector assertion as a criterion kind. Assumption: a meaningful share of the user's work is web-facing.
  Done when: a criterion `http: GET /x contains #id` runs against a spawned dev server with a timeout, the server is killed by process group, and the result is auto-recorded as evidence.

- **Draft a PR description from the brief behind one outward-facing yes** — FEATURE — value 2 — effort S — risk med
  Why: the brief already holds intent, evidence, files touched and lesson. Commit offers exist, but publishing a branch or PR is a separate outward step that needs its own confirmation.
  Done when: after the user's yes, a PR body (summary, evidence, risks) is generated from the brief with secrets redacted, and nothing is sent before that yes.
