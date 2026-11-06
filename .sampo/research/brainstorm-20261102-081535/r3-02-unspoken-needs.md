# Brainstorm — lens: unspoken needs

I answered one earlier question, then my own ideas. Every idea here is new relative to the "ideas so far" list.

**Earlier question I can answer:** "Which surfaces would the user actually open in a week of real use?" Their own words point to the terminal (`fm`, the foreman-ui pane) and morning notes. Every steer is phrased as a verb or a gauge. So proof should arrive as one terminal line and one file, with any web or phone view optional. This is an inference from the steers, not measured.

- **Cap and rotate the proof artifact store** — FIX — value 4 — effort S — risk low — category: storage
  Why: screenshots, flow traces and proof receipts are about to multiply, and the project already ran into tmpfs runway trouble (`/run/user/1000/fm-children`). Nothing is said to bound artifact growth. Assumption: artifacts currently live unbounded under the state dir.
  Done when: a store over its byte cap deletes the oldest green artifacts first, keeps every red one and every artifact cited by an open task, and `fm doctor` prints size against cap.

- **Hand blocked proofs to a machine that can finish them** — FEATURE — value 4 — effort M — risk med — category: remote proof
  Why: T-0335, T-0336 and T-0337 are blocked because this machine lacks real codex, gemini and opencode. Each is a proof the user can't produce here. The need behind it is to stop being the only machine in the proof path.
  Done when: `fm prove export T-0336` writes a self-contained recipe (commands, expected markers, a result schema); running it elsewhere writes a result file; `fm prove import` attaches that result and flips the claim from unproven to "proven on host X" with the host stamped.

- **Maintain a bug zoo with a recall scoreboard** — FEATURE — value 5 — effort L — risk med — category: prover recall
  Why: provers each get a red fixture, but nobody can say "across all provers we catch 11 of 14 planted flaw classes, up from 9". The standing rule says weakness-finding must use signals Foreman didn't author. Assumption: a single multi-class planted repo doesn't exist yet.
  Done when: a fixture repo plants one flaw per class (UI regression, doc drift, data skew, slow path, infra misconfig, wrong-meaning); `fm exam zoo` prints recall per prover and per class; a drop against the last run fails the ship gate.

- **Check the live site against what was pushed** — FEATURE — value 3 — effort S — risk low — category: publish proof
  Why: the standing rule publishes `site/genesis` to main automatically, and the README makes public claims. Pushed is not served: Pages builds can fail or lag and nobody looks.
  Done when: after `fm genesis live`, a poll of the Pages URL confirms the served data's commit hash matches the pushed one within a time limit, else a WARN names the lag.

- **Pin foreman-ui's render against each host release** — FEATURE — value 4 — effort M — risk med — category: UI proof
  Why: T-1217 (Claude Code paints the pane at #262626) and T-0418 show the mod breaks silently with host internals. A pty snapshot with ANSI colour assertions catches it before the user upgrades.
  Done when: `fm shot --pty` renders the mod under a given Claude Code version and asserts cell colours and the layout of pane regions; a version bump with a diff reports which regions changed.

- **Check pasted claims from another AI against the repo** — FEATURE — value 3 — effort M — risk low — category: meaning
  Why: the harness already treats pasted text as data. Assumption: the user pastes reviews and advice from elsewhere. The unspoken need is to know which of that text is true of this repo before acting.
  Done when: `fm check-paste` extracts repo-checkable statements (file X defines Y, flag Z exists), tests each by grep or AST, and prints each as confirmed, refuted or uncheckable, with the evidence line.

- **Probe noexec, read-only and volatile mounts for every path Foreman runs from** — FIX — value 3 — effort S — risk low — category: ops
  Why: the user runs a hardened kernel and has tmpfs-backed state. A script written to a noexec `/tmp`, or state kept on a volatile mount, fails far from its cause. Assumption: the doctor checks volatility but not exec permission.
  Done when: `fm doctor` tests exec-and-write on each directory Foreman writes scripts to or keeps state in, and names the mount option that breaks it.

- **Run the user's own steers as meaning-checks on a finish claim** — FEATURE — value 4 — effort M — risk med — category: meaning
  Why: "steered:" lines (T-2583's 8+ vs 7 characters, T-2341's re-scope) show repeated slips between a sentence and its literal rules. These slips are what "does it do what the user meant" means in practice. Assumption: a finish card doesn't currently cross-check numbers in criteria against the examples beside them.
  Done when: for any DONE-WHEN containing a numeric threshold and an example, `fm task finish` evaluates the example against the threshold and refuses on a contradiction, naming both.

- **Replay a new verifier over the last 50 closed tasks** — FEATURE — value 4 — effort M — risk low — category: gate calibration
  Why: each verifier added raises the question "would this have flagged anything real, or only noise?". Right now that gets answered only after shipping.
  Done when: `fm prove backtest <prover>` prints how many of the last 50 closed tasks it would have flagged, with their ids, and a prover that flags 0 or over 40 is marked "unproven useful".

- **Show a proof-coverage heat strip per module** — FEATURE — value 3 — effort M — risk low — category: visibility
  Why: `fm map` already lists layout (plugin/skills 1388 files). The user can't see which modules have any non-unit proof at all. Assumption: no per-module proof-kind rollup exists.
  Done when: `fm map --proof` prints each directory with counts of UI, data, docs, perf and meaning proofs, and marks directories with none.

- **Wild: publish a proof expiry tide chart** — FEATURE — value 2 — effort S — risk low — category: delight, trust (wild)
  Why: proofs expire when covered files change, but nobody sees when trust is *lowest*. Assumption: the user would plan a verification session around a forecast.
  Done when: `fm prove tide` lists the next 14 days of expected expiries from file churn rates, with the day carrying the most expiring claims marked.

- **Wild: open the zoo to outside provers** — FEATURE — value 3 — effort L — risk med — category: community (wild)
  Why: the zoo from idea 3 becomes a public benchmark on the Genesis site. Other verifiers submit a result file, and the page shows recall and false alarms. It gives Foreman a signal it didn't author.
  Done when: the site lists at least two provers (Foreman's and one baseline) with recall and false-alarm numbers computed from a result file, regenerated by a script.

- **Wild: a sleep-test for proofs** — FEATURE — value 3 — effort M — risk med — category: trust (wild)
  Why: a proof that passes right now may pass only because of leftover state. Assumption: re-running in a clean copy at an unrelated later time catches this.
  Done when: each night, one random proof from the past week reruns in a fresh clone with its caches cleared; a verdict that flips is recorded and the original claim is re-labelled unproven.

Next question: which proof kinds has the user never once looked at the result of, and would they keep trusting a kind that only ever ran unattended?
Next question: where does a proof's environment (machine, host version, time of day) differ from the user's real day, and which claims break there?
