# Brainstorm — lens: security and safety

- **Take a persistence census at every session close** — SECURITY — value 5 — effort M — risk med — category: persistence
  Why: assumption: the pack's immune and tick ideas watch Foreman's own scheduler and units, not what an agent in bypass mode plants for later. Think `.git/hooks`, `core.hooksPath`, shell rc files, `systemd --user` units, crontab, `~/.config/autostart`, `authorized_keys`, npm lifecycle scripts and `.claude/settings`.
  Done when: a fixture session that writes a `pre-commit` hook and a user timer makes `fm doctor` and the close receipt list both by path and hash, and a clean session lists none.

- **Move deletions to a session trash** — SECURITY — value 5 — effort M — risk med — category: reversibility
  Why: the guard blocks, and "neutralize the call" and "undo a landed task" are proposed, but nothing makes the allowed `rm` and `mv` over an existing file recoverable. Assumption: most real damage comes from allowed deletes, not blocked ones.
  Done when: after `rm -r` of a tracked-ignored directory in a test session, `fm trash restore` returns it byte-identical, and the trash is purged after N days.

- **Judge what a command will run, not what it says** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: assumption: the guard reads the command string. An agent can write `x.sh`, then run `bash x.sh`, `make clean` or `npm run reset`, or reach a symlink such as `./data -> $HOME`. The guard should expand a script written this session, Makefile and package targets, and `realpath` the destructive targets before it rules.
  Done when: replay cases for a session-written destructive script, a Makefile target and a symlink-to-HOME `rm -rf` are all blocked, and the benign twin of each passes.

- **Import GTFOBins and LOLBAS as a generated guard exam** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the pack asks for evasion corpora and rival fixes, but names no concrete corpus. Benign binaries that execute code (`find -exec`, `tar --to-command`, `awk system`, `git -c core.sshCommand`, `LD_PRELOAD=`, `BASH_ENV=`) are the standard slip path.
  Done when: `fm exam guard` runs every entry as a case, prints per-binary recall, and any miss files a task naming the binary.

- **Block reads of secret-bearing files and give a redacted view** — SECURITY — value 4 — effort M — risk med — category: secrets
  Why: assumption: the existing secret work covers diffs, ledgers and published data, which is the write side. A model reading `.env`, `~/.aws/credentials` or `~/.ssh/*` into context is exposure before anything is written. The alternative is key names with `***` values.
  Done when: a session `cat ~/.aws/credentials` and a Read of `.env` return the redacted view and one ledger line, and a project can allowlist a path.

- **Hold every publication for a grant bound to the content hash** — SECURITY — value 4 — effort S — risk low — category: outward actions
  Why: the push grant is spent through `fm ship`, but `gh gist create`, `npm publish`, `docker push` and `gh release` publish content too. Sending content outward publishes it, and a deleted copy may still be cached.
  Done when: `npm publish` in a test repo is held until a grant naming the tarball hash is spent once, and a changed tarball is refused.

- **Expire bypass mode with a lease** — SECURITY — value 4 — effort M — risk med — category: privilege
  Why: the guard exists for bypass mode, and bypass currently lasts the whole session. A lease that lapses at task close or after N minutes would force a re-grant for the next task, with the lapse visible on the status line.
  Done when: a test session in bypass loses it at `fm task finish`, and the next unguarded call prompts once.

- **Add a cloud-spend command class with a dollar ceiling** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: assumption: the guard targets destruction. `terraform apply`, `aws ec2 run-instances` and `gcloud` compute creation can burn money with no data loss. "Dry-run infra" is about verification, not about blocking spend.
  Done when: `terraform apply` is held with an estimated cost line unless the task declares a ceiling, and an unknown estimate is treated as unproven.

- **Fence security-testing tasks to an authorized scope file** — SECURITY — value 3 — effort M — risk low — category: authorization
  Why: pentest and CTF work needs clear authorization. A task kind that carries `scope.txt` (hosts, CIDRs, repos) lets the guard refuse `nmap`, `curl` and `sqlmap` against anything outside it.
  Done when: with a scope of `10.0.0.5`, `nmap 10.0.0.6` is blocked with the scope line quoted, and `10.0.0.5` passes.

- **Keep lessons bound to their repo by default** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: assumption: lessons and steers can be promoted across repos "when they recur". A lesson mined from a private repo can name a customer, path or secret, then enter a prompt sent for another repo.
  Done when: a lesson born in repo A never appears in a repo B pack or prompt unless it is marked portable, and a test with a planted marker proves it.

- **Scan allowed outbound text for smuggled secrets** — SECURITY — value 4 — effort M — risk low — category: exfiltration — wild
  Why: assumption: the pack watches blocked egress and model traffic, but not the channels that stay open. Commit messages, PR bodies, search queries and fetched URL query strings can all carry an encoded secret.
  Done when: a session that puts a planted canary in a `curl` query string, a commit subject and a base64 branch name has all three held, and a normal session sees no false hold.

- **Add `fm breach`, a one-command incident button** — SECURITY — value 4 — effort M — risk low — category: incident response — wild
  Why: "HALT file" and "contact tracing" are in the pack, but nothing revokes live grants, kills lanes and snapshots state in one move. The useful new part is the exposure inventory: which credentials and paths the session could reach, with a rotation checklist.
  Done when: running `fm breach` in a test session revokes the publish grant, stops lanes, and prints a reachable-secrets list that includes a planted fake key.

- **Make loosening a guard rule cool off for 24 hours** — SECURITY — value 3 — effort S — risk low — category: guard integrity — wild
  Why: "protect its own configuration" is proposed, but an approved loosening still takes effect at once, so a persuaded session or a panicked user can weaken the guard. Tightening stays instant.
  Done when: `fm guard loosen RULE` schedules the change and prints the effective time, the rule is unchanged for 24 hours, and tightening applies immediately.

- **Hold a canary-reader drill each week** — SECURITY — value 3 — effort S — risk low — category: injection — wild
  Why: assumption: the pack has planted-lie exams, but none on the read-then-act path. This one plants an instruction in a README, an issue body and a tool result, then reports which of the three a real session obeyed, per harness.
  Done when: `fm drill --inject` prints obey/ignore per source and fails the nightly if any source is obeyed.

Answering one earlier question: guard-allowed commands the user undid by hand show up without shell history as `git reflog` resets, files restored out of the session trash, and an `fm task` reopened within a day of a guard allow. The trash idea above would make the second signal exist.

Next question: which agent-plantable persistence or trust surfaces (editor tasks, direnv, git config, package lifecycle hooks) does the guard see as ordinary file writes today?
Next question: when the user loosens or overrides a guard rule, what record shows whether that choice was informed or only a tired click?
