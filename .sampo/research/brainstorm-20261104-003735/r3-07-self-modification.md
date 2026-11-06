# Brainstorm — lens: self-modification

- **Freeze a function after its third fix** — CLEAN — value 4 — effort S — risk low — category: self-repair
  Why: the drive's running-agent count has been patched at least five times (T-0575, T-0115, T-2873, T-2900, T-2901), each time in a new way. Nothing noticed the pattern.
  Done when: `sampo doctor` lists any function touched by 3 or more FIX commits in 30 days, and files one redesign task that blocks further point-fixes to it until closed.

- **Pin running processes to immutable code snapshots** — FIX — value 4 — effort M — risk med — category: install safety
  Why: assumption: a self-edit that lands under a live drive or interactive session gives a process half-old, half-new lazily imported modules. This is a plausible cause of the new drive stops and failed tool calls.
  Done when: installs write to a versioned directory and flip a `current` pointer, each process records the version it started on, and a test lands an edit mid-session with no mixed-version import.

- **Learn stall remedies by trial in a scratch clone** — FEATURE — value 5 — effort L — risk med — category: drive recovery — wild
  Why: the gap is that drive stops went from 0 to 0.1. Taxonomies and fixed recovery exist in earlier ideas, but nothing learns which remedy works for which stall class.
  Done when: for a recorded stall, 3 or more candidate unstick actions run in a scratch worktree on the local model. The winner is stored in a remedy table keyed by stall class, and the next stall of that class uses it first.

- **Quarantine memory written by triggered sessions** — SECURITY — value 4 — effort S — risk low — category: injection defense
  Why: assumption: a CI-red or issue-triggered session that writes to `memory/` could persist text the issue author planted. Fences exist for the trigger payload but not for what a session saves afterwards.
  Done when: memory writes from trigger-born sessions go to a `pending/` tier that is not recalled. A write is promoted only after the user confirms it or a second independent session reproduces the claim.

- **Apply a self-edit only when two nights derive the same patch** — SECURITY — value 4 — effort M — risk low — category: self-edit consensus — wild
  Why: assumption: one local model's overnight patch is cheap but can be wrong. Agreement from independent runs is a cheap check that isn't in the earlier gates.
  Done when: a candidate lands only if two runs on different nights, or different models, with no shared draft produce diffs whose normalized AST is identical. Any mismatch goes to the morning card as "disputed."

- **Turn failed tool calls into a replayable fixture bank** — FIX — value 5 — effort M — risk low — category: tool reliability
  Why: the top gap is failed tool calls up by half. A self-edit gate needs a bank of real failures to replay against.
  Done when: each failed call is stored redacted as payload, hook state and expected outcome. `sampo check` replays the bank against a candidate edit and reports the failure rate per 100 calls by edit epoch.

- **Watch host config for hook-table drift** — FEATURE — value 3 — effort S — risk low — category: self-heal
  Why: a double SessionStart injection exists and shims register hooks. A file trigger on host settings and the plugin cache could catch it the moment it happens.
  Done when: changing the hook registration (a duplicate or a missing Ward) fires a trigger within 60 seconds. It writes a proposed fix to the morning card without editing host settings itself.

- **Propose scanner allow-rules from their false-positive dispositions** — CLEAN — value 3 — effort S — risk low — category: lint tuning
  Why: the silent-cut scan failed on the lanes.py twins' `path:line` join, so a human had to dismiss it.
  Done when: each dismissed scanner finding is stored with its reason. After 2 identical dismissals the scanner drafts a narrow allow-rule with a failing-then-passing test, and never widens its own scope.

- **Turn a pushback on triggered output into an expiring mute** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user's habit is "stop asking me, keep going, not that wild." A correction to an unattended result should change the originating trigger without a second request.
  Done when: a user message that cites a triggered output adds a suppression or tuning rule with a 14-day expiry to that trigger. The rule shows on the morning card, and one key makes it permanent.

- **Judge each self-edit with the user's last 30 pushbacks as jurors** — FEATURE — value 4 — effort M — risk low — category: edit review — wild
  Why: the user's own words are the best signal Sampo didn't author. Cold reads currently check against gen-0 rules, not against what actually annoyed the user.
  Done when: a tool-less child sees only the edit's visible effect and the 30 most recent pushbacks. It must name any pushback the effect would likely repeat, quoting the line. A quoted hit blocks an unattended landing.

- **Earn self-edit allowance from clean nights** — SECURITY — value 3 — effort M — risk med — category: autonomy — wild
  Why: autonomy ladders exist per trigger. A single allowance in changed lines per night, earned by consecutive nights with no drive stop and no revert, ties self-modification to demonstrated stability.
  Done when: the allowance starts at 0 lines. It rises with each clean night, resets on a stop or revert, and the ledger shows the balance.

- **Add a landing fence around triggers** — FIX — value 3 — effort S — risk low — category: loop safety
  Why: a self-edit under `plugin/` can trip file watchers and the CI watcher, which can file another self-edit. A self-cause filter is already on the list, but not the landing window itself.
  Done when: every landing stamps an epoch. Events from paths touched by that landing are dropped for N minutes, and a test lands an edit with 2 watchers armed and sees no refire.

Next question: what share of the new drive stops and failed tool calls happened in sessions that began before a self-edit or install landed, and can the ledger tell?
Next question: when a self-edit changes how a trigger fires, who tells the user in the morning card, and in what words?
