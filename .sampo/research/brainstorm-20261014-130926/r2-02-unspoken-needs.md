# Brainstorm — lens: unspoken needs

- **Audit each round's own diff before calling it shipped** — FEATURE — value 4 — effort M — risk low — category: review
  Why: Round 1 landed about 15 behavioural changes in one day, and T-0034 (`fm audit run`, headless read-only lens reviewers) is still deferred. The two metric-reader bugs (`'✗ exit N'` vs `'exit N'`) are the kind of miss a diff-scoped audit finds. Assumption: lens reviewers can be pointed at a commit range.
  Done when: `fm audit run --range <round-start>..HEAD` writes a structured findings file, and run against a fixture range with a planted reader/writer mismatch it reports that mismatch.

- **Make the edit-time test sentinel out of `fm check --affected`** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: T-0214 is deferred, and round 1 already shipped affected-test selection for builders. A debounced PostToolUse run of only the linked tests turns that into feedback within seconds of an edit, not at the step gate. Assumption: the test-to-source map is accurate enough that false triggers stay rare.
  Done when: editing a file with a linked test in a fixture project reports that test's result in the next turn, at most once per 30 s, and editing an unlinked file runs nothing.

- **Give the guard bounded script-file reading** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: T-0275 is deferred, and round 1 only taught the guard about heredocs. `bash x.sh` and `python3 x.py` still run content the guard never sees. Cap it at one level deep and a size limit, and on an unreadable file refuse with a rewrite hint, never silently allow.
  Done when: `bash evil.sh`, where the file holds a denied command, is blocked with the offending line quoted, and a 5 MB or missing script yields the documented refusal.

- **Bound Foreman's disk footprint with a budget and LRU eviction** — CLEAN — value 3 — effort S — risk low — category: state
  Why: round 1 added state/outputs full-text files (opt-in), snapshots and session files. The recent `fm tidy` commits prune by age only, so a burst of big outputs can still fill the disk. Assumption: nobody has set a size limit yet.
  Done when: `fm tidy --budget 200MB` evicts least-recently-read output files first and never evicts one cited by an open task, and `fm doctor` shows the current size against the budget.

- **Prove `fm page` makes zero network requests** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the page is published as an Artifact. Redaction is tested, but the "self-contained" claim isn't. Add a restrictive CSP meta tag (`default-src 'none'`) and a headless-load test that fails on any outbound request.
  Done when: a fixture catalogue's page loads in a headless browser with zero requests, and a test injecting `<img src=http://x>` is blocked or fails the build.

- **Fall back to window-only mode when the tray library is missing** — FIX — value 3 — effort S — risk low — category: desktop
  Why: T-0325 is blocked because the tray icon needs libappindicator-gtk3 on Arch, so a missing optional library blocks the whole feature. Detect it at startup, run without the tray, and have `fm doctor` print the exact install line.
  Done when: Desktop starts and works on a box without the library, and `fm doctor` names the missing package.

- **Add a one-file status segment for tmux and starship** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: the state is only visible inside Claude Code, the band, or the web UI. A zero-spawn read of one derived file (task id, step n/m, needs-you flag) lets tmux `status-right` or a shell prompt show it across panes and SSH. Assumption: the user lives in tmux (the bus already uses it).
  Done when: `fm status --segment` prints under 40 chars in under 10 ms without Python, and the tmux snippet in the docs shows it live.

- **Bootstrap Windows through WSL from one PowerShell line** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: the README rules out native Windows, so anyone on Windows hits a wall at line one. An `install.ps1` that enables or detects WSL, then runs `install.sh` inside it and wires the `fm` shim, covers most of the need without a native port. Assumption: Windows users exist or are wanted.
  Done when: on a clean Windows VM, one `irm … | iex` line ends with `fm doctor` green inside WSL.

- **Run the bench under a throttled-CPU profile** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: round 1 made bench judge by CPU time under load, but hooks run on laptops far slower than this machine. A `--slow` mode (taskset to one core plus nice) gives a worst-case p95 and exposes hooks that only look cheap on fast hardware.
  Done when: `bench_hooks.py --slow` reports per-hook p95 under throttling, and CI fails if any hook exceeds the stated ceiling.

- **Wild: Add an eject test that leaves a project with plain markdown** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: Foreman is large (350 files, 73 skills), and the user keeps asking for slimmer, faster and fewer things. A tested `fm eject` that exports queue, decisions and lessons as plain files removes lock-in fear and so makes adopting everything else less risky. Assumption: wild.
  Done when: eject on a fixture project produces a markdown folder, and re-importing it recreates the same task list.

- **Wild: Hold a "stranger's first ten minutes" replay with a cold child** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: onboarding is only checked by the author. Run a fresh headless Claude with only the README against a toy repo, record each stall and refusal, and file the worst three as tasks. Wild.
  Done when: `fm stranger` writes a transcript summary with the first point of confusion and its cost.

- **Wild: Mount a slow-disk and read-only-home drill** — SECURITY — value 3 — effort M — risk low — category: resilience
  Why: state writes assume a fast, writable disk. A drill that runs the hooks over a latency-injected, full or read-only home shows which ones hang or corrupt state and which fail open silently. Wild.
  Done when: `fm doctor --drill` finishes with a table of hook outcomes for each fault, and none leaves a torn state file.

- **Wild: Turn "etc. etc. etc." into a standing, budgeted mandate** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user repeats "super improve… etc." and says "recursively" because they want rounds to continue without being asked each time. Record the mandate with a dollar cap and a stop rule, run rounds until the stop trips, and send one summary at the end. Assumption: the user wants this and not a prompt per round.
  Done when: `fm mandate "keep improving" --budget 10` runs at least two rounds on a fixture project and stops with a stated reason, and cancelling it works.
