# Brainstorm — lens: security and safety

- **Tripwire writes to persistence paths** — SECURITY — value 4 — effort S — risk low — category: persistence
  Why: assumption: a run that edits `~/.bashrc`, `.git/hooks/*`, `~/.config/systemd/user/*`, cron, direnv `.envrc` or a `.pth` file is trying to survive past its task. The pack lists T-0791 (injection and supply-chain defenses) as deferred, and none of its ideas name these paths.
  Done when: a run that writes `.git/hooks/pre-commit` is refused by the write hook, and its receipt names the path and the rule.

- **Deny reads of credential stores, not just writes** — SECURITY — value 5 — effort S — risk low — category: secrets
  Why: reads are an exfiltration path, and the guard only judges writes and commands. assumption: `~/.ssh`, `~/.aws`, browser profiles, keyrings and `.netrc` are never needed by a code task.
  Done when: `cat ~/.aws/credentials` from a run is refused with a one-line reason, and the same read from a user shell still works.

- **Plant canary credentials in every run's environment** — SECURITY — value 4 — effort S — risk low — category: secrets
  Why: assumption: a run that references a fake `AWS_SECRET_ACCESS_KEY` has no legitimate reason to, so any use shows injected or exfiltrating intent. This differs from the existing canary files idea, which only detects reads.
  Done when: a run that echoes the canary variable into a command or outbound request halts within one tool call, and the journal records the variable name, not its value.

- **Mint push credentials per run, scoped to `fm/*` branches** — SECURITY — value 5 — effort M — risk med — category: credentials
  Why: a lane with the user's full push token can overwrite `main`. The pack's "Push foreman/build to main so the site publishes" shows pushes to protected branches are routine, so the scoping has to be explicit.
  Done when: a push to `main` from a run's credentials is rejected by the git host, and a push to `fm/<task>` succeeds.

- **Flag fixes that hardcode a test's literal** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: a run can make a test pass by returning the expected literal from the fixture instead of fixing the logic. The pack's "Surface the changed assertion first" idea covers edited tests, but not this case.
  Done when: a fix whose new non-test code contains a string or number that appears only in a test's expected value fails the close check and names the file and line.

- **Check new package names against typosquat lists before a lane installs** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: assumption: a model can invent or misspell a dependency name, and an edit-distance check against the top packages on each registry catches most typosquats. The pack's "pin to a seven-day cooldown" idea doesn't check names.
  Done when: adding `reqeusts` to a manifest is blocked with the nearest real name in the message, and `requests` passes.

- **Turn a leaked secret into a rotation task** — SECURITY — value 4 — effort S — risk low — category: secrets
  Why: the pack already redacts secrets in journals, but a secret that reached a commit or a log still needs rotating. Redaction hides the value and doesn't tell the user to rotate it.
  Done when: a staged diff containing a token-shaped string opens a queued "rotate this credential" task with the secret's type and path, and the value never appears in the task text.

- **Require a human-typed nonce for destructive verbs** — SECURITY — value 5 — effort S — risk low — category: safety — wild
  Why: a model can answer a yes/no prompt, but it can't read a random word that is shown only in the terminal pane. Destructive verbs (`fm undo`, `fm reset`, publish) would ask for that word, which the run can't produce.
  Done when: `fm undo` without the nonce exits non-zero, and entering the nonce shown on the pane completes the undo once.

- **Make the journal one-way: surfaces read it, only the CLI writes** — SECURITY — value 4 — effort M — risk med — category: architecture
  Why: the pack shows several surfaces (web UI, pane, desk, mod) and a local text door and socket. A compromised or spoofed surface should not be able to issue commands. assumption: the surfaces need only read access to the state.
  Done when: a write sent through the web UI's HTTP route or the local socket is rejected, and the same change made through `fm` succeeds and is journaled.

- **Sign a scope contract at queue time** — SECURITY — value 4 — effort M — risk med — category: authorization — wild
  Why: the user approves a queue, but nothing records what the approval covered. A signed contract listing each task's allowed paths, commands and budget would let hooks enforce exactly what was approved, and let the user check it later.
  Done when: a queued task that writes outside its signed path list is refused, and altering the contract file breaks the signature check at the next run.

- **Redirect a suspicious run into a decoy copy** — SECURITY — value 3 — effort L — risk high — category: deception — wild
  Why: assumption: when a run hits a canary or exfiltration-shaped command, halting it tells an attacker what was detected. Instead the run continues in a throwaway copy with fake secrets, so the real files stay untouched and the operator is alerted.
  Done when: a flagged run's read of a canary path returns the decoy value, the real file's hash is unchanged, and the operator gets a notice that the run is in decoy mode.

- **Wild: a tripwire for model confidence without a proof** — SECURITY — value 3 — effort S — risk low — category: honesty — wild
  Why: assumption: when a reply says "no secrets", "tests pass" or "safe to publish" without a command that shows it, that claim is the most likely place for an unverified assumption to slip into a receipt. The pack's "Tag every claim with how it was checked" idea is close but doesn't block the claim.
  Done when: a receipt containing "safe to publish" with no matching command in the journal is held back and the user is asked to check it.
