# Brainstorm — lens: unspoken needs

- **Make unattended commits carry their own git author** — FEATURE — value 4 — effort S — risk low — category: safety
  Why: assumption: the drive and lanes commit as the user, so undoing a bad overnight run means reading messages. The T-#### trailers idea only helps if the message survives a rebase or squash.
  Done when: every drive or lane commit has author `Foreman Drive <…>`, and `git log --author=Foreman` lists exactly the unattended commits in a fixture run.

- **Print the exchange rate on every Mission close** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: the steers want growth to earn its place (T-2503), and the user keeps dropping "mostly built" items. Nothing shows whether a safety addition cost more weight than the risk it retired.
  Done when: closing a Mission prints "+N lines, +V verbs, −R retired risks (each linked to a test or ledger event)". A Mission with no risk-retired rows says "unearned" instead of a ratio.

- **Give each sub-agent a one-page dossier** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: "agents" is flagged thin and the pack has no per-specialist view. Assumption: lanes, cold readers and brainstormers are separate roles with no joint accept/reject record.
  Done when: `fm agents dossier NAME` shows scope, tools allowed, last 10 outputs accepted or rejected, and cost per accepted output. A role with zero accepted outputs in 30 days is marked "retire candidate".

- **Show a Posture page in the web UI** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: "ui" is flagged thin and the safety state is scattered across `fm doctor`, grants, the drill and the guard ledger. The user's rule is that one source should say what is true now.
  Done when: `/posture` renders guard last-fired, live grants with expiry, last restore drill and hook freshness. Each row is green, red or "unknown (not measured)", and unknown is never drawn green.

- **Fail the ship gate if the web UI fetches a remote origin** — SECURITY — value 3 — effort S — risk low — category: ui
  Why: assumption: `plugin/templates/web/index.html` is meant to be local-only, but nothing pins that. A CDN font or script would quietly break local-first and add an exfiltration path.
  Done when: a test greps all web templates for `http(s)://` origins other than localhost and fails on a planted one.

- **Cap the lessons store with recall-based eviction** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: T-0217 (lesson confidence) is deferred, and lessons only grow. Assumption: unrecalled lessons still cost injection tokens.
  Done when: a lesson never recalled in 60 days, or recalled but followed by a failure, moves to an `archive/` file. A fixture run shows session-start tokens drop with no change in the pass rate of the recalled set.

- **Refuse any script step that needs sudo or pipes a download to a shell** — SECURITY — value 3 — effort S — risk low — category: safety
  Why: T-0325 needs `sudo pacman`, and the user's rule is that Foreman works without root. Assumption: no automatic check exists that Foreman's own scripts never escalate or fetch.
  Done when: a lint over `install.sh` and `plugin/bin` fails on `sudo`, `curl|sh` or `wget|sh`. Existing uses are listed as printed-for-the-user, not executed.

- **Record a safety-wins tiebreak as a standing decision** — CLEAN — value 3 — effort S — risk low — category: process
  Why: the steers say "never block on the user for process questions" while also demanding lean. Assumption: nothing says which wins when a guard rule adds weight.
  Done when: `fm decide --check` stores "when lean and safe conflict, safe wins and the added weight is logged as a pay-down debt". `fm genesis sweep` reports any growth that claimed the exemption.

- **Wild: Run a "lean twin" every night with half the verbs hidden** — PERFORMANCE — value 3 — effort L — risk med — category: lean
  Why: wild. A twin install with the least-used half of verbs removed runs the zero-token exam arms. Any score drop names the verbs that earned their keep. The rest are deletion proposals with evidence rather than opinion.
  Done when: the nightly report lists verbs whose removal changed zero exam results.

- **Wild: Keep a tripwire file in the state directory** — SECURITY — value 3 — effort S — risk low — category: safety
  Why: wild. Plant `.foreman-canary` in each protected area. If any agent, hook or lane reads or edits it outside a Foreman verb, the guard ledger records who. This catches unexpected sweeps that the command-shape rules miss.
  Done when: a fixture agent running `cat` on the canary produces a ledger line and a one-line `fm doctor` warning.

- **Wild: Stage a monthly "delete one thing" vote with the evidence attached** — FEATURE — value 3 — effort M — risk low — category: lean
  Why: wild. The unspoken need behind the user's repeated drops is a bias toward subtraction. One candidate a month, chosen from usage and exam data, with the revert command printed beside it, makes pruning habitual.
  Done when: `fm tidy` offers exactly one candidate with its last-use date and a ready revert patch.

- **Show agents' trust ranks in the UI as a roster strip** — FEATURE — value 2 — effort S — risk low — category: ui/agents
  Why: a combination of the dossier and Posture ideas. Assumption: the user would act on a quiet role earlier if they could see it.
  Done when: the web UI shows a row per role with accepted-output rate and a "dormant" tag after 30 idle days.

Next question: which safety or lean checks have only ever been run by Foreman on its own repo, and would they behave the same on a repo the user has never opened it in?
Next question: when the user leaves a decision to a default, how do they find out afterwards that it was theirs to make?
