**Verdict:** changes needed. The row budget holds. There is one functional regression (plan approval) and two housekeeping misses (version, types).

**Findings**

- MEDIUM — `register.tsx:1278-1297` (also `:1322`) — Plan approval is only reachable through the attention row, and that row yields to a paused hook, an fm error or a pending `asks` entry. The old UI gave every waiting plan its own approve button.
  - With asks plus a plan, `plans` still fills the Task section (the `!a` case), but no `approve-T-<id>` button is drawn.
  - Only `plans[0]` gets approve and show, so a second waiting plan has no button until the first is approved.
  - Fix: put approve on the Plan section's rule row, or add an "approve" button to the queue rows that have `q.plan`.
  - Reproducer: `world()` with `approvals: [...]` and a queued plan, then `ui.find({key:'approve-T-0009'})` is undefined. I did not run it.
  - Confidence: high.
- MEDIUM — `.claude-plugin/marketplace.json:21` — `foreman-ui` is still `0.8.0` and the old description, while `plugin.json` is now `0.9.0`. Fix: bump both fields together. This answers the pre-audit item: the marketplace file does need an edit.
- MEDIUM — `mods/foreman-ui/types/index.d.ts:131` — it still declares `folded: string[]`, and the new `reviewing` atom (`register.tsx:57`) is not declared. Fix: replace `folded` with `reviewing: string | null`. Confidence: medium, because I could not run the type-check.
- LOW — `register.tsx:1378-1380` — `fit()` and `crit.slice(0, nCrit)` hide steps and criteria with no "… N more", unlike the section's own overflow row. With 6 steps and 4 criteria in a 9-row Task, 3 steps vanish silently. Fix: count them in an extra row.
- LOW — `register.tsx:1607` — the `in-more` row ("… N more in the inbox") is one body element standing for many. If the section cuts it, the "… N more" count undercounts by `inboxN - inbox.length - 1`, and it can only happen when `inboxN` is over 10.
- LOW — Lost without a replacement:
  - The `usage ahead of pace` and `N blocked` signals (`v.signals`) now draw nowhere while the pane is open, because the band returns early.
  - The closed task's title (`c.title`).
  - A gate's `note` text.
  - The `fm lib show NAME` hint, now only "N cards unread".
  - A subagent's last action.
  - Research and bench lists are cut to the first entry (`.slice(0,1)`) with no count.
- LOW — Duplicates:
  - With no active task, the first waiting plan's title shows in the attention row and again in the Plan section.
  - "spend" labels both the Pulse gauge and the More row, though they hold different facts.
- LOW — Dead code. `churn`, `eta` and `lanes` are imported but unused (`register.tsx:58`). `LIST`, `LANES`, `HOLD_MS` and `STEP_MS` in `state.ts` and the `lanes`/`churn`/`eta` helpers in `rows.tsx` have no pane caller.
- LOW — `foreman-ui.test.tsx:1394` and `:1432` assert `props.height` equals `layout()` (and `live-body` height before equals after). The prop is always set to `rows`, so both pass whatever the content does. No test measures drawn rows or wrapping.

**Acceptance criteria**
- AC1 (fixed heights, one panel, no nested borders, spend and closed count once): met by construction. Each section body is `height={rows} overflow="hidden"`, and header, attention and controls are fixed-height too. `layout()` sums are at most `h`, which I checked by hand and the test sweeps 8–120. The border check is real (`borderStyle` finds none). I did not run `claude plugin test .`.
- AC2 (PNGs): `ui-after.png` and `ui-small.png` exist and fit the dock. Long titles end in an ellipsis, not mid-word. Live and Task show large blank gaps, which is the intended fixed-height trade.

**Implicit decisions**
- Dock fallback of 40 rows when `scroll` is missing.
- Pulse needs at least 26 rows and More at least 36.
- The task gets 55% of the shared rows.
- The band disappears entirely while the pane is shown.
- Fold state is dropped (the old `folded` store key is orphaned).

**Not checked:** I did not run the tests or tsc, so wrapping inside Ink at narrow widths is unverified, and neither is mobile or desktop rendering.

**Noticed:** `demo/live.svg` still draws the old bordered cards, and the README caption now misdescribes it.
