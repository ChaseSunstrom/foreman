# Brainstorm — lens: unspoken needs

- **Look back at the last Mission's use counts when the next one opens** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the Mission 7 request had to ask by hand to "report Mission 6's two use counts". The user wants proof that built things get called, and shouldn't have to ask.
  Done when: opening a Mission prints one line per capability the previous Mission shipped, giving real session-path calls since its merge (0 is printed as 0), and a fixture with a never-called capability shows "0 calls".

- **Redact ledger records in place with chain-preserving tombstones** — SECURITY — value 4 — effort M — risk med — category: ledger
  Why: the dropped idea about removing `task_done` lines notes that deleting lines breaks the hash chain, which `fm verify-ledger` and `fm drill --restore` report first. Removing a pasted secret or a wrong record needs a way that doesn't look like tampering.
  Done when: `fm ledger redact <id> --reason …` replaces the record body with a tombstone holding its hash, `fm verify-ledger` stays green, and a removed line without a tombstone still fails it.

- **Learn phrasing aliases from every "already built" drop** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: the drops cite existing code (`fm usage --prune`, `check_predictions`, `check_usage_burn`) that earlier searches missed under the slate's wording. The grounding step asks for three phrasings, but nothing remembers which phrasings found the thing.
  Done when: a drop citing `file:symbol` stores the idea's title words as aliases of that symbol, and the next canary search for a re-worded idea returns it in the top 3 (tested on the c16, c17 and c21 drops).

- **Stamp records written under a pinned clock as simulated** — FIX — value 3 — effort S — risk low — category: ledger
  Why: T-2645 added `c.clock()` honouring `FOREMAN_NOW`, plus a doctor warning while it is pinned. A real ledger line written during a pinned session would still be read as true time by every windowed reader afterwards.
  Done when: a record appended with `FOREMAN_NOW` set carries `sim:true`, windowed readers exclude it by default, and a test that pins the clock then reads unpinned sees no leaked record.

- **Log every grounding canary result to measure the search's own recall** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: T-2674 made the grounding step run a canary search before accepting any "not found". Nothing records how often the canary fails to find a planted known item, so the "not found" verdicts can't be trusted or tuned.
  Done when: each grounding pass appends canary hit or miss to a ledger, and `fm doctor` reports the miss rate with its sample size.

- **Mark the pack's sections with the question each one answers for the lens** — CLEAN — value 3 — effort M — risk low — category: pack
  Why: the open question "which pack sections have no measurable effect" is still unanswered, and `plugin/lib` has no per-section attribution. Without a stated purpose per section, ablation results can't be read.
  Done when: each pack section declares a one-line purpose and a lens-relevance tag, and `fm ideas --pack-report` lists sections no kept idea cited.

- **Pre-brief each Mission on which user-owned inputs it will need** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: blocked tasks T-0325 (sudo pacman), T-0352 and T-0418 sat blocked on the user's machine or accounts. The open question "which needs the user's other machines or accounts" shows Foreman only learns this after filing.
  Done when: filing a brief runs a `needs:` check against a host profile, and a brief naming `sudo` or a missing package is filed already marked "needs you: <action>" and does not enter `fm next`'s offer list.

- **Replace "ideas so far" with a verb-and-idea coverage grid** — PERFORMANCE — value 3 — effort M — risk med — category: pack
  Why: the pack's idea list runs to thousands of one-line titles, repeated into every child's context, and the pack never says how many ideas it has or where they cluster. (Assumption: the cost and the repeated near-duplicates are what the user keeps correcting for.)
  Done when: the pack carries a cluster digest with counts and at most 100 lines, and a run with the digest yields no more duplicate ideas than a run with the full list.

- **Wild: write a letter from the Foreman of a year ago and score what it got wrong** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: assumption: the user steers constantly about what they want next, so a sealed letter of "what I expect you'll want in a year" turns steers into a forecast that can be settled, with no new infrastructure.
  Done when: at each generation boundary a sealed note is stored, and one year on `fm letter open` prints it beside the ledger's actual asks with a hit count.

- **Wild: let the user say "I keep…" and have Foreman count it** — FEATURE — value 3 — effort M — risk low — category: unspoken needs
  Why: the user's repeated corrections (arithmetic mismatches, volatile paths, silent cuts) are phrased as complaints about a class. Spotting the class costs them a message each time.
  Done when: a message containing "I keep" or "again" files a sibling sweep over the named class, and the sweep reports how many other instances it found.

- **Wild: prove the first minute after a silent fail-open by deliberately triggering one on install day** — FEATURE — value 3 — effort S — risk med — category: trust
  Why: the question "what does the user see in the first minute after a silent fail-open, and is that moment ever tested" is open. A harmless injected fail-open at install is the only way to test it.
  Done when: `fm doctor --demo-degraded` breaks one hook in a scratch home, the degraded line appears within one prompt, and a test asserts that line's text.

Next question: which of the thousands of ideas in the catalogue has any recorded call from a real session, versus only a test that exercises it?
Next question: when a drop says "already built", did the original search miss because of wording, location or a stale index, and does the fix differ by cause?
