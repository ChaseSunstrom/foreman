# Brainstorm — lens: self-modification

- **Replay-tune the gap detector from history** — FEATURE — value 4 — effort M — risk low — category: tool gaps
  Why: the detector for a "missing tool moment" (exit 127, ModuleNotFound, "command not found", a tool the model asks for that isn't registered) is assumed to be hand-written patterns. Self-modification should start there, because every later step depends on it. Assumption: those patterns are code today.
  Done when: the patterns live in one data file. An edit to that file is accepted only if recall on replayed closed-task transcripts rises and false positives on a held-out slice don't.

- **Give small-model self-edits a typed patch language** — SECURITY — value 4 — effort M — risk med — category: edit safety
  Why: the standing steer is for local models to scaffold their way to frontier results. Letting a 4B or 9B emit free-form diffs against protected paths is the risky part. A schema of ops (add card, set search-source order, adjust a retire-when threshold) is checkable before it is applied. Assumption: no such schema exists yet.
  Done when: a patch with an op or target outside the schema is rejected before it touches disk. A valid patch applies and reverts through the same op list.

- **Graft one function instead of installing a plugin** — FEATURE — value 4 — effort L — risk med — category: acquisition
  Why: installs are queued behind user grants, and the rea source showed that found plugins are mostly more surface than needed. Copying only the needed function (MIT or similar licence, provenance recorded, cold-read, hash-pinned) removes the grant for the common case and cuts footprint.
  Done when: on a recorded gap, the loop produces a vendored single-file tool with a provenance header and passing tests, and no install grant is queued.

- **Record forge recipes and re-forge on card change** — FEATURE — value 4 — effort M — risk low — category: reproducibility
  Why: cards are meant to grow every generation, but a forged tool built under an older card keeps its old behaviour. Storing a recipe per tool (card ids, model profile, prompt hash) lets a card edit trigger a rebuild into a scratch dir and a behaviour diff against the tool's own tests.
  Done when: editing one card lists exactly the tools forged from it. `--rebuild` reports pass or fail per tool and promotes nothing automatically.

- **Build a card → tool → skill → hook dependency index** — PERFORMANCE — value 3 — effort M — risk low — category: edit scope
  Why: self-edit gates currently seem to run broad suites (gates: fm doctor, roundtrip, bench_hooks). With 1,396 skills and thousands of coming cards, an edit needs a blast radius so it can run only the affected exams.
  Done when: for a changed card, a command prints the dependents. A test confirms that running only those exams catches a planted regression in each dependent kind.

- **Let a forged tool repair itself, but never its own test** — SECURITY — value 3 — effort M — risk med — category: self-repair
  Why: tools break when a CLI version changes. A repair that may also edit the tool's test is a self-grading loophole, which the standing rule against metric gaming forbids.
  Done when: a repair run can write only the tool's source files. A changed test hash aborts the repair. A planted CLI-flag change is fixed with the test left byte-identical.

- **Turn unknown-verb typos into gap records** — FEATURE — value 3 — effort S — risk low — category: unspoken needs
  Why: the rename left many aliases, and users type verbs that don't exist (the did-you-mean path). A near-miss that has no match is a user-stated need for a capability.
  Done when: an unknown verb typed twice files one gap record with both invocations. A known alias files none.

- **Make grant cards shorter over time, never auto-approving** — SECURITY — value 3 — effort S — risk low — category: install grants
  Why: the user said "stop asking me for stuff", but the install grant is something only they can give. Learning which fields they always glance past can shorten the card. It must not approve anything.
  Done when: the card shrinks after N approvals of the same tool class. A test confirms that no code path writes a grant without a user action.

- **Hot-load a forged tool into the live session** — FEATURE — value 4 — effort M — risk med — category: usability
  Why: building a tool and then not using it until the next restart wastes the point of Mission 7 ("tests it, uses it"). A dispatcher directory plus a one-line, one-time notice makes the tool callable on the next turn.
  Done when: a tool forged at turn N is invoked successfully at turn N+1 of the same session. The notice appears once and is not repeated.

- **Farm gaps by subtraction** — FEATURE — wild — value 4 — effort M — risk low — category: gap discovery
  Why: waiting for user pain finds few gaps. In a sandbox, mask a common tool (jq, rg, shellcheck, which is already a listed missing tool) and replay closed tasks. The tasks that fail or slow down show what an absence costs, which gives synthetic gap records with real stakes.
  Done when: masking a named tool in the sandbox produces a ranked list of replayed tasks that changed outcome. At least one becomes a gap record.

- **Make the forge able to forge itself (a tool quine)** — CLEAN — wild — value 3 — effort L — risk med — category: dogfood
  Why: if the forge's own helper scripts can be rebuilt from their passports by a 27B model, the forge is demonstrably usable by small models. If they can't be rebuilt, it isn't.
  Done when: deleting one forge helper and rebuilding it from its passport and card passes that helper's tests on the local model.

- **Keep tools as passports until first use (lazy forge)** — PERFORMANCE — wild — value 3 — effort M — risk med — category: footprint
  Why: the lean missions track 2.4 GB of state and injected characters. Storing only the passport, test and recipe, then regenerating code on first call and caching it, keeps the shelf light and always matched to the current card set.
  Done when: a shelf of ten tools occupies only passport-sized files before use. The first call rebuilds the tool, passes its test and caches it, and the second call reuses the cache.

- **Forge a replacement for a tool and let the old one retire only if the replacement wins** — FEATURE — wild — value 3 — effort M — risk med — category: tool lifecycle
  Why: tools are retired only when unused. A scheduled duel between the shelf's tool and a freshly forged or found rival, on the tool's own tests plus a held-out set, lets the shelf improve itself instead of only shrinking.
  Done when: the duel promotes a rival only with a strictly higher held-out score and keeps the loser's passport in a fossil file. A tie keeps the incumbent.

Next question: which self-edits to the acquisition loop has the user reverted by hand so far, and can the ledgers say whether the cause was the edit's wording, its gate, or its target?
Next question: when a forged tool and a host-native feature overlap, which side does the acquisition loop's own search miss, and does anything check that search against the host's tool list?
