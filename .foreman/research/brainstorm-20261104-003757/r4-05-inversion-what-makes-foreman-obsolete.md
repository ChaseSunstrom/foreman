# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Ask the distro's file database first** — FEATURE — value 4 — effort S — risk low — category: tool search
  Why: assumption: on Arch, `pacman -F`, and on other systems `nix-index`, `apt-file` or `brew which-formula`, already map "binary X" to a package with zero model calls and zero network trust. The pack lists search sources but none that the OS already maintains.
  Done when: for 10 missing binaries (e.g. `shellcheck`, `jq`, `rg`), the first-ranked source is the file DB and each resolves to a package name in under 1 s with no network or model call.

- **Add an ephemeral-run rung with no install** — FEATURE — value 4 — effort M — risk med — category: grants
  Why: the pack's pain is the grant queue and the "no software installs" steer. `uvx`, `npx --yes` (hash-pinned), `nix shell` or a throwaway container run a tool once and leave nothing behind, so a gap can close with no grant. assumption: the user allows network pulls into a temp dir.
  Done when: a scenario needing a PyPI CLI completes via the ephemeral rung, `find` shows nothing new installed after, and no grant entry was queued.

- **Forge into the repo's own task runner** — FEATURE — value 4 — effort M — risk low — category: lock-in
  Why: assumption: a tool that only runs via `sampo tool` becomes dead weight the moment Sampo or the host changes. Landing the script as a `just`, Makefile or `package.json` target plus a plain test makes the forge's output survive Sampo's own obsolescence.
  Done when: after a forged tool is promoted, uninstalling Sampo (`PATH` stripped of its dirs) still runs it and its test green from a clean clone.

- **Delegate discovery to the host's native plugin and MCP search** — CLEAN — value 3 — effort S — risk low — category: reuse
  Why: Mission 7 says "finds the plugin, skill or MCP server"; the host already ships marketplaces and registries. Sampo's unique part is quarantine, test and use, not search.
  Done when: `sampo tool find` calls the host's own listing first, falls back to Sampo's search only on zero hits, and an exam arm shows no recall loss on 10 known gaps.

- **Search a local catalog snapshot and strip queries before any network call** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: assumption: a search for "parse proprietary X log format" leaks the project's work. Build a weekly offline index of registry names and descriptions (embedded with the local embedder); network search sends only a generic capability noun.
  Done when: with the network blocked, 8 of 10 historical gaps still return a candidate, and a packet capture of a live search shows no repo path, file name or identifier.

- **Let the user approve a grant from the phone with a one-use token** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: the pack says "install grants queued" and "stop asking me", so a queue only the desk can drain stalls overnight runs. A local push (ntfy self-hosted) with an HMAC action carries yes or no for one tool hash.
  Done when: tapping yes on a notification releases exactly that hash-pinned grant, replaying the tap does nothing, and the grant expires after 24 h.

- **Budget a forged tool's cold start** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: forged tools called from hooks or the drive add latency on top of the hook bench. assumption: Python tools importing heavy modules at top level are the common slow case.
  Done when: `sampo tool bench` reports p95 cold start for each shelf tool, a lint fails promotion above 80 ms for hook-path tools, and one slow tool is fixed by lazy import.

- **Explain any tool on request** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: a shelf grown by thousands of cards and many tools is opaque. `sampo tool why NAME` should print which gap created it, who approved it, last real-path call, what would delete it, and the exact uninstall command.
  Done when: for 5 shelf tools plus 2 binaries Sampo never touched, the output is correct and ends with a runnable removal line (or "not mine").

- **Make the user's own scripts the first shelf** — FEATURE — value 4 — effort M — risk low — category: reuse
  Why: assumption: `~/bin`, `~/.local/bin` and dotfiles hold tools the user already trusts, so building another is the cheapest obsolescence of the forge. Index them with a passport, never modify them.
  Done when: for a gap matching a user script, search returns it before any build or install, and the passport was generated without writing to the script's directory.

- **Wild: run the acquisition loop as a markdown card and compare it with the verbs** — FEATURE — value 3 — effort M — risk low — category: obsolescence test
  Why: wild; assumption: if a card plus bare shell does the gap exam as well as the verb path, the verbs are dead code. Pick the path by data.
  Done when: a cold agent given only the card and a shell matches the verb arm's pass rate on 10 gap scenarios, or the exam prints the gap by stage.

- **Wild: simulate the future host with a stub tool-search server** — FEATURE — value 4 — effort M — risk low — category: obsolescence test
  Why: wild; build a fake MCP "tool-search" server backed by a registry snapshot, give it to the bare arm, and measure what acquisition still adds when the host does discovery itself.
  Done when: `sampo louhi` reports the with/without delta under the stub for 10 gaps, and each leftover win is named by stage (test, quarantine, small-model card).

- **Wild: post the Wanted board as upstream issues for others' agents to fill** — FEATURE — value 2 — effort M — risk med — category: outward
  Why: wild; a gap many users share should be absorbed upstream instead of forged locally. Outward action, so it needs the user's grant, and drafts must carry no repo names.
  Done when: one draft issue is generated from a real gap with a leak scan passing, filed only after approval, and the local entry is marked "awaiting upstream".

Next question: Which of the tools Sampo forged or installed in the last 30 days would the user have written in one inline command, and does any ledger show it?
Next question: If the host shipped tool search and auto-install tomorrow, which single stage of Mission 7 (search, build, test, quarantine, grant, use) would still need Sampo?
