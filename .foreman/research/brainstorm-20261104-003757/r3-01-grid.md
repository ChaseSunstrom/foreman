# Brainstorm — lens: grid

- **Pre-check binaries before a Bash call runs** — FEATURE — value 4 — effort S — risk low — category: missing × agent × CLI
  Why: a small model invents commands and flags, and the gap is only seen after exit 127. assumption: a PreToolUse hook can parse the first word of each pipeline stage.
  Done when: `shellcheck x.sh` on a machine without it is stopped before running, with the shelf alternative named, in under 20 ms.

- **Derive tool cards from the tool's real `--help` output** — FIX — value 4 — effort M — risk low — category: wrong × agent × CLI
  Why: cards written from the model's memory of a tool's flags go stale or are wrong, and the small-model card store is brand new. assumption: help text is capturable in the quarantine trial.
  Done when: each tool card's flag list matches the tool's captured `--help` and `--version`, and a flag absent from the help fails the card lint.

- **Park tasks on a typed tool-wait, then wake them on the grant** — FEATURE — value 4 — effort M — risk low — category: missing × unattended × drive
  Why: the user said "stop asking me, keep going", and the drive must not idle on a grant only they can give. assumption: the task graph can carry a wake predicate.
  Done when: a task needing an ungranted tool is skipped with reason `tool-wait:<name>`, the rest of the queue runs, and it is picked up the tick after the grant lands.

- **Make every forged script call the Ward on its own argv** — SECURITY — value 5 — effort M — risk med — category: unsafe × other agents × CLI
  Why: Codex, Gemini and opencode lack Sampo's hooks, so a forged tool run there has no Ward in front of it. assumption: the Ward can be imported as a one-file check.
  Done when: running a forged tool with a Ward-refused argument under a harness with no hooks exits non-zero with the Ward's reason.

- **Read found-tool READMEs only through a tool-less summariser** — SECURITY — value 5 — effort M — risk low — category: unsafe × agent × search
  Why: a found plugin's README is untrusted text that could carry instructions into an agent that can act. assumption: the existing tool-less child runner can emit a fixed schema.
  Done when: a README with a planted "run this" line yields a card without it, and the acting agent's context never holds the raw text.

- **Require a typed result footer from forged tools** — FIX — value 4 — effort S — risk low — category: wrong × unattended × CLI
  Why: a tool that exits 0 with empty output looks like a success in an unattended run. assumption: tools are scripts Sampo generates, so the footer can be a template.
  Done when: a forged tool printing no `ok n=<count> bytes=<n>` footer is recorded as unproven, not passed, in a test.

- **Write a standing grant policy the user edits once** — FEATURE — value 5 — effort M — risk med — category: unclear × user × web UI
  Why: "stop asking me for stuff" plus "no software installs" are policy statements, and today each grant is a one-off prompt. assumption: a small rule grammar (stdlib-only, no network, under N lines) is enough.
  Done when: a stdlib-only 40-line script tool is auto-allowed, a network-using one lands on the grant card, and each decision names the policy line that made it.

- **Show a world-diff on every grant card** — FEATURE — value 4 — effort M — risk low — category: unclear × user × web UI
  Why: a user approving an install cannot see what it does. assumption: the cage trial records file, host and PATH effects.
  Done when: the grant card lists files created, hosts contacted and PATH changes from a recorded trial, and an empty list says "none observed".

- **Check the shelf at lane spawn with a handshake ping** — FIX — value 3 — effort M — risk low — category: missing × other agents × lanes
  Why: a lane or subagent may lack the tool the parent just built (a different allowlist, a different PATH). assumption: lanes get their own env.
  Done when: a lane brief lists only the shelf tools that answered a `--selftest` in that lane's environment.

- **Build a stdlib lint for shellcheck's most common findings** — FEATURE — value 3 — effort M — risk low — category: missing × agent × evidence
  Why: shellcheck was dropped as an install; `bash -n` alone is the stand-in. assumption: a dozen regex-level rules cover most real findings.
  Done when: five planted shell bugs (an unquoted variable, `cd` with no `||`, and so on) are flagged by the script and clean files pass.

- **Wild: Ship each tool as one self-verifying file** — FEATURE — value 3 — effort M — risk low — category: unclear × other agents × portability
  Why: assumption: a single file carrying its spec, passport, tests and Ward check moves between harnesses and machines unchanged.
  Done when: `python3 -I tool.py --selftest` passes on a clean machine with nothing else from Sampo.

- **Wild: Predict tools from a brief with a tool-less child** — FEATURE — value 3 — effort S — risk low — category: missing × agent × intake
  Why: assumption: a cold guess of "tools this task needs", scored against what the task actually used, finds gaps before a run starts.
  Done when: a nightly report gives precision and recall of the guesses against the last 20 closed tasks.

- **Wild: Have a cold author write the test for a tool from its passport alone** — SECURITY — value 3 — effort M — risk low — category: wrong × agent × tests
  Why: assumption: a test written by someone who never saw the code catches the builder's blind spot.
  Done when: the blind test fails on a planted wrong-behaviour mutant of a forged tool that its own test passes.

- **Wild: Race the 27B against a stranger agent on a missing tool** — FEATURE — value 2 — effort L — risk med — category: slow × unattended × exam
  Why: assumption: the not-yet items need a paired exam against the path they replace, and a timed race gives one.
  Done when: the exam prints time-to-usable-tool and the verified-pass cost for each contender on the same gap.

Cells left empty: web UI × agent and web UI × other agents, since neither acts through the web UI. Slow × user in the CLI is empty because the evidence points to grant latency, which the standing policy above already covers.

Next question: when the standing policy auto-allows a tool, how does the user find out a week later which ones are actually in use?
Next question: which acquired tool has already been replaced by a host-native feature, and does anything record it?
