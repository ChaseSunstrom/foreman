## intent: changes needed

**MEDIUM** — `plugin/lib/fmcli.py:540` (host built by `_create`), with the gate at `plugin/lib/fmcore.py:1449`. An explore item (`TAG?:`) is meant to wait for the user's confirmation. `cmd_batch` doesn't pass `explore` to the host and doesn't refuse explore members. Batching `X?:` with two other items makes a host that is `planned`, tier M, with no approval gate. The item then runs with no confirmation. Urgent priority is dropped the same way, since the host uses the default `priority="normal"`. Fix: refuse members with `meta["explore"]`, or copy `explore` to the host. Carry urgent over with `any(...)`. Confidence: high.

**LOW** — `plugin/lib/fmcli.py:550`. The criterion says "criteria and steps from each", but each member gets one step, its title. A planned member's own steps are dropped, so the host plan loses information the member already had. Fix: copy `b.steps()` as `f"{b.id}: {step}"` when the member has any. Confidence: medium. I did not read `Brief.steps` to confirm its return shape.

**LOW** — `plugin/lib/fmcore.py:1583-1587`. The suggestion appears only for tier S items, and only when `b` is in the top 5 small items of its type. The criterion says "small items", so that reading is defensible. The criterion also isn't tied to a test of the "three or more lead the inbox" threshold. I couldn't verify test coverage here, because I didn't open `test_batch.py`. Confidence: low.

## edge: changes needed

**MEDIUM** — `plugin/lib/fmcli.py:314-315`. `fm task drop HOST --done-in X` goes to `task_done_in` before the dropped branch at 328-329, so `_settle_batch` never runs. The host is dropped but its members keep `batched_in`. `rank_inbox` (`fmcore.py:1157`) and `order_queue` (1171) filter them out, so they are hidden permanently. Nothing lists or unbatches them. Fix: call `_settle_batch(p, h, done=False)` in `task_done_in` when the host has `meta["batch"]`. Alternatively, have the inbox and queue filters ignore `batched_in` when the host is missing, dropped or done. That second option also covers the crash case below. Confidence: high (code path traced).

**LOW** — `plugin/lib/fmcli.py:296-298`. The host is marked done by `mutate` and `_settle_batch` runs afterwards, in a separate lock and save. If the process dies between them, or `find_brief` or a save fails, the host is done and the members keep `batched_in` with status captured. They stay hidden with nothing to release them. The same fix applies: a filter that treats a done or dropped host as no host. Confidence: medium.

**LOW** — `plugin/lib/fmcli.py:526-557`. Two sessions: the check and the mutation share one lock, so a concurrent `fm batch` is safe. The lane check at 528 uses `p.lane`, so a member active in another lane isn't refused as active. The status check still refuses it if it was started. Fine.

## Acceptance criteria
- One host brief from not-yet-started items, with criteria and steps: partly met. Criteria are copied; steps are reduced to one per member.
- Hides members from the inbox and queue: met (`fmcore.py:1157` and `1171`).
- Refuses started members: met (`fmcli.py:529-530`).
- Closes members done-in the host: met on the normal done path (`fmcli.py:297`). Not met when the host is dropped with `--done-in`.
- `fm next` suggests a batch for three or more small items of one type: met (`fmcore.py:1583-1587`).
- `-k test_batch` passes: not verifiable, because I did not run it.

## Not checked
I did not run the tests, read `test_batch.py`, or review the `fmguard.py:1631` change, `execute.md`, or `regen_views`. I assumed `c.lock` is reentrant, as `cmd_intake` relies on the same pattern.
