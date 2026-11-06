**Verdict: approve with nits.** I found no way to make `validate()` reject a scene from real cards. The findings below are about how the room looks, and one doc claim.

I read the code but could not run anything, because I had no shell. The `Lookbook` tests and `fm scene lookbook` itself are unrun, and the camera angles below are my arithmetic, not renders.

## lens: intent
- MEDIUM — plugin/lib/fmscene.py:98 (camera), :68-70 (slots) — The default camera is at z=5.5 looking down -z. It cannot see most side-wall frames. At the 8:5 aspect of `cells`/`turntable` (fmscene.py:651) the horizontal half-angle is about 42.7°. Side frames at z=1.4 and z=4.2 are 4.1 and 1.3 ahead of the camera and 5.85 to the side, so they are at about 55° and 77° off-axis, outside the view. The z=-1.4 frames start at about 45.7° and are mostly out of view. Failure: `--count 12` hangs four frames that `fm scene cells` and `compile` never show, and the other side frames are foreshortened. Fix: pull the camera back and widen it (for example z≈9, fov 70), or put the overflow looks on the back wall in a second row — low confidence on the exact numbers, since this is calculated and not rendered.
- LOW — plugin/lib/fmscene.py:68 and CHANGELOG.md:9 — The docs say the best look hangs "centre back", but the back slots are x = -1.4, 1.4, -4.2, 4.2, so no frame is at x=0. Rank 1 hangs left of centre while the camera targets x=0. `--count 1` gives one off-centre frame. Fix: put a centre slot first (x = 0, ±2.8, ±5.6), or change the docs to "centre-left".
- LOW — plugin/lib/fmscene.py:79-80 and :89 — Frames are not on the walls. The wall surface is at ±6.0 (centre ±6.1, thickness 0.2), and the frame spans 5.8 to 5.9, so there is a 0.1 gap and each frame floats. It shows in `turntable` views. Fix: set the slot offset to ±5.95, or thicken the frame.

## lens: adversary
No findings. Palette entries come from the regex `#[0-9A-Fa-f]{6}` (fmtaste.py:45), so every entry is a 3-tuple in 0-255. Band materials are named "c"+6 hex, 7 characters, so they cannot collide with frame, wall or floor. Look names are `look-*` filenames from the plugin's own cards directory, which starts with a letter, so `NAME` accepts them. Nothing raw reaches the terminal.

## lens: edge
- LOW — plugin/lib/fmscene.py:89,94 — Name safety assumes the card filenames are tame. `look-<slug>-<jj>` must fit `NAME` (at most 64 characters, `[A-Za-z0-9_-]`). A card named `look-a.b.md`, or a slug over about 54 characters, makes `validate` fail with a ValueError, so the whole command exits 2. The shipped cards are fine (the longest is `look-shipping-manifest`). Fix: do not fix, or clean the name with a `re.sub` and a length cap.
- Fewer looks than `--count` is handled. The slice returns fewer names and the output says "N look(s)". Zero looks raises "0 looks: 1 to 12 hang" and exits 2 (fmscene.py:66 and :1504). `rank()` yields each look once, so there are no duplicate names from it. An empty palette gives an empty frame, and the test covers that.

## lens: operator
No findings. The change is one local file write and no network call. MASTER.md, CHANGELOG.md and scene-3d.md match the code, apart from the "centre" wording above.

## lens: maintainer
- LOW — plugin/tests/test_scene.py:170-175 — Only `--count 13` is tested. `--count 0` and the case where the cards number fewer than `--count` have no test. Fix: add `--count 0` to the same assertion.
- LOW — plugin/lib/fmscene.py:83-95 — The slot vectors and the `at`/`size` closures redefined inside the loop are dense but correct. I checked the geometry for all three walls and the frames face inward. I judge the cost acceptable.

## Acceptance criteria
- `fm scene lookbook` prints a scene that `fm scene check` accepts, with a frame per look best first, `--count`, palette bands, walls and floor: **met by the code**, and the `Lookbook` tests cover it, but I could not run them. Not verified: whether all frames are visible (see MEDIUM).

## Implicit decisions
- `--count` defaults to 8 and is capped at 12, the number of shipped cards.
- Bands are colour fields only, with no title or text on the frame.
- The shared `--count` flag is silently ignored by the other showpieces, as `--days` is.
- Band materials are deduplicated by hex colour.
- The room is a U of three walls plus a floor, with three lights (two direct).

## Not checked
Visual output, since I could not render; and the real ledger-ranking path under `self.fm`.

**Noticed:** none
