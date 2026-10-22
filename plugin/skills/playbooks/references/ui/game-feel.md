<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Game feel: juice with intensity caps

Use when a game or a playful interface needs to feel responsive and physical: hits that land, jumps that pop, buttons that squish, rewards that burst. Applies to Phaser, Pygame, Godot, LÖVE, Unity and canvas or DOM games alike; the engine APIs live in the cards at the end.

The one rule: **juice exaggerates what happened; it never hides what is happening, and it never hurts.** Every effect has a cause in play, a hard ceiling, and a reduced-motion version that keeps its meaning. Each rule below can be marked pass or fail by a reviewer.

1. Write the juice table: one row per gameplay event, every cell filled, before any effect is built.
2. Check every amount against the caps; where `motion.md` names a stricter number, it wins.
3. Build the effects on the capped primitives (`juice.py` or its port), never on raw engine calls.
4. Build each reduced-motion cell as its own path, then run the checks in Check it.

## Precedence

- `motion.md` owns UI chrome: menus, HUD transitions, settings and store screens. Its tokens, its 500 ms ceiling and its reduced-motion path apply there unchanged.
- This file owns in-world feedback (hits, jumps, pickups, explosions) and playful flourishes on controls (a squishy button, a reward burst).
- Where both files name a number for the same thing, **the stricter one wins**. Flashes: `motion.md` allows three a second, this file two, so two. A UI press squash: `motion.md`'s `--pop` (0.96) beats the body squash cap here.
- A `DESIGN.md` Motion knob (`design-direction.md`) may tune the `motion.md` tokens; it never raises a cap in this file.

## The juice table

Before building, write one row per gameplay event that gets juice. It is the storyboard of `motion.md` for a game: a blank cell is a fail, and anything on screen that isn't in the table gets cut.

| Event (cause) | Techniques and amounts | Sound cue | Reduced motion |
|---|---|---|---|
| Player sword hits enemy | hit-stop 60 ms; trauma +0.25; enemy squash 0.8 × 1.25 for 100 ms; 12 sparks | `hit_light` | hit-stop 60 ms; enemy tints white 1 frame then outline; one spark mark fades in place |
| Player takes damage | trauma +0.4; edge tint red 30% alpha; 0.5 s invulnerability shown as an outline | `hurt` | edge tint; outline; no shake |
| Coin pickup | coin stretches 1.2 then pops; 6 sparkles; counter ticks with `--ease-enter` | `coin` (pitch +0–5%) | coin fades in `--dur-exit`; counter changes in place |

Amounts are in the cap units of the next section, so a reviewer checks each cell against one ceiling.

## Caps

Hard ceilings, whatever the art direction, the Effects settings or the excitement of the moment. "Short side" is the viewport's shorter dimension in pixels. The constants in `juice.py` below mirror this table; a change to one changes both.

| Technique | Cap | Reduced-motion fallback |
|---|---|---|
| Screen shake | offset ≤ 2% of short side (14 px at 720p); roll ≤ 2°; one shake gone ≤ 0.5 s after its last hit; continuous shaking ≤ 1 s, then ≥ 0.25 s at rest before it can start again; HUD never shakes | none; a 150 ms edge tint, and vibration if the person has it on |
| Camera kick (recoil, landing dip) | offset ≤ 1% of short side; FOV change ≤ 4°; back at rest ≤ 150 ms; no roll | camera never moves; the weapon sprite or crosshair shows it (tint, size step) |
| Hit-stop | one freeze 30–120 ms; ≤ 200 ms of freeze in any 1 s; input is buffered, never dropped | kept: a pause is stillness, not motion. Its companion shake and flash follow their own rows |
| Anticipation | player actions: wind-up ≤ 100 ms and its first frame drawn in the input frame; enemy telegraphs: ≥ 300 ms and never motion-only (also a colour and a shape or icon) | timing unchanged (it is gameplay); the wind-up is one held pose plus a tint, no backswing travel |
| Squash and stretch | bodies scale 0.75–1.25 per axis; UI controls 0.96–1.04 (`--pop`); area kept (x·y within 0.95–1.05); back at rest ≤ 150 ms; collision shapes never scale | no scale: one pose frame or a shade change for the same duration |
| Element shake (wrong code, locked door) | ≤ `--shift` (8 px) travel, ≤ 3 swings, ≤ `--dur-move` (300 ms); the element only, never the screen | no travel: a tint plus the text that says what was wrong |
| Particles | ≤ 48 per burst; ≤ 400 alive; feedback bursts live ≤ 0.8 s; pooled, never allocated per frame; never drawn over the HUD; ≤ 50% alpha over the player character | one mark (or ≤ 4 sparks with zero velocity) that fades in place in `--dur-exit`; ambient weather stops or freezes |
| Easing | UI uses `motion.md` tokens only; overshoot ≤ 10% (back-out with c = 1.70158 is exactly that); elastic or bounce ≤ 2 visible swings and ≤ `--dur-stage` | overshoot, elastic and bounce become `--ease-enter`; travel × `--travel` (0) |
| Flash (screen or sprite) | ≤ 2 flashes in any 1 s window, all sources on screen counted together, any size; full-screen flash ≤ 30% alpha; no saturated red full-screen flash; damage blink is an outline or steady 50% alpha, not a 10 Hz blink | unchanged (light, not motion); the **Flashing: off** setting turns each flash into an edge tint that fades in `--dur-enter` and out `--dur-exit`, still counted by the gate |
| Sound cue | **off by default**; one cue retriggers at most once per 50 ms; ≤ 8 voices at once; pitch jitter ≤ ±5%; nothing plays before the first input | unchanged: reduced motion never mutes. Every cue already has a visual twin (sound is never the only signal) |
| Vibration | its own setting; scaled by the Screen shake slider; one pulse ≤ 300 ms; ≤ 1 pulse per 100 ms | kept, and may stand in for shake |

Why stricter than WCAG on flashes: WCAG 2.3.1 allows three a second and exempts small areas, but in a game several small flashes stack on one screen, and the area exemption can't be checked by reading code. Two a second, counted together, can.

## Techniques

How to do each one well; the numbers are the Caps table's.

**Anticipation.** A small move against the action before it: crouch before the jump, pull back before the punch. For the player's own actions it must be short, because the person already pressed the button; `motion.md`'s rule holds: feedback starts in the input frame, so the first anticipation frame *is* the response. For enemies it is the opposite: a long, readable wind-up is how the player learns to dodge, so make it longer and give it a second, non-motion channel.

**Squash and stretch.** Scale along the velocity: stretch on the way up, squash on landing, keeping the area so it reads as soft rather than as resizing. It is a render transform on the sprite, applied from the body's state; the physics shape keeps its size, or a squash lets things clip through floors. On UI, a press squash uses `--pop` at `--dur-tap` and releases with `--ease-enter`.

**Hit-stop.** Freeze both parties of an impact for a few frames so the hit reads. Freeze the *simulation*, not the renderer: skip fixed steps in the accumulator (`fm lib show game-loop`) while the freeze lasts, keep drawing, keep reading input into a buffer and apply it on the first step after. Scale the length with the hit (light 40–60 ms, heavy up to the cap) and budget it, or a combo turns into a slideshow. Measure it in simulation ticks so a replay freezes on the same ticks.

**Screen shake (trauma).** Each hit adds *trauma* (0..1); trauma decays at a fixed rate; the shake drawn is trauma² × the cap × the person's shake setting, so small hits stay subtle and stacked hits grow. Offsets come from smooth noise at ~20 Hz, not a fresh random number per frame (which reads as jitter, and varies with frame rate). Apply the offset to the view only: the camera's world position, the HUD, aim and hit detection don't move. The code below enforces every shake cap.

**Camera kick.** A directional nudge that says where force came from: recoil away from the shot, a dip on a heavy landing, a short FOV push on a dash. Kick then spring back with `--ease-enter`; it adds to the shake offset and shares its ceiling (the sum of both stays ≤ 2% of the short side).

**Particles.** Sparks, dust, confetti: they show where and how hard. Spawn from a pool, from their own seeded RNG (never the simulation's, or replays diverge), and draw them in a layer under the HUD. Fewer, bigger, shorter-lived particles read better than many small ones and cost less.

**Easing.** Arrivals decelerate (`--ease-enter`), departures accelerate (`--ease-exit`), things already on screen use `--ease-move`. Playful UI may overshoot (back-out) on a reward or a pickup, once; springs are for gestures and physics, as in `motion.md`. Linear motion is for progress bars and projectiles only.

**Flash.** A white hit-flash for one or two frames on the struck sprite, a tinted full-screen pulse for a big event. Every flash request goes through one gate (`FlashGate` below); a refused flash simply doesn't happen, the rest of the effect still plays.

**Sound cues.** Sound sells impact more than any visual, which is exactly why it must be the person's choice: start muted, offer it once on the title screen or in settings, remember the answer. Vary pitch a little so a repeated cue doesn't drill, limit retriggers so twenty coins make one shimmer, not twenty clicks, and give every cue a visual twin.

## Reduced motion

The rule from `motion.md` carries over: **keep the meaning, drop the travel.** Every row of the juice table has a Reduced cell, and every technique has a fallback in the Caps table; a technique with no fallback is a fail.

- **Source of truth:** the in-game setting wins; its default comes from the platform. Web: `matchMedia('(prefers-reduced-motion: reduce)')` (or `motion.md`'s `reduced()`); iOS `UIAccessibility.isReduceMotionEnabled`; Android "Remove animations" (`ANIMATOR_DURATION_SCALE` = 0). Where the engine can't read it, the first launch opens the Effects panel before play.
- **The Effects panel** is reachable from the title screen and the pause menu and applies without a restart. It has: Motion (Full / Reduced), Screen shake (0–100%), Flashing (On / Off), Vibration (On / Off), Sound (Off by default).
- **One switch per path, not per call site.** Effects read one settings object; reduced motion sets shake scale 0, kick 0, squash off, particle travel 0 and easing overshoot off in one place, like `motion.md`'s token block. A `if reduced:` scattered through gameplay code is a fail.
- **Gameplay is identical in both modes.** Timings, hitboxes, invulnerability windows and telegraph lengths don't change; only their presentation does. A test runs the same seeded replay in both modes and compares the simulation state hashes.
- **Ambient motion** (parallax, swaying grass, weather, idle bobbing on menus) stops or freezes under Reduced, and anything that moves on its own for more than 5 s outside gameplay has a pause control (`motion.md`, WCAG 2.2.2).

## The capped primitives

Engine-free and pure functions of state and time, so they test without a window (`fm lib show game-loop`). Port them line for line; the asserts become the test.

```python
# juice.py: capped game-feel primitives. Render-only, except hit-stop (pass simulation time).
import math, random

SHAKE_MAX_FRAC = 0.02  # offset <= 2% of the viewport's short side
SHAKE_MAX_DEG = 2.0    # roll <= 2 degrees
SHAKE_DECAY = 2.0      # trauma lost per second: full trauma is gone in 0.5 s
SHAKE_ADD_WINDOW = 0.5 # adds are ignored after 0.5 s of shaking, so a run lasts <= 1 s
SHAKE_REST = 0.25      # seconds at rest before a new run may start
SHAKE_HZ = 20.0        # noise rate: a smooth wobble, not per-frame jitter
FLASH_MAX = 2          # flashes in any 1 s window, all sources together
HITSTOP_MAX = 0.12     # one freeze, seconds
HITSTOP_BUDGET = 0.2   # total freeze in any 1 s window

def _noise(x):  # smooth value noise in [-1, 1]
    i = math.floor(x)
    a, b = random.Random(i).uniform(-1, 1), random.Random(i + 1).uniform(-1, 1)
    w = (1 - math.cos((x - i) * math.pi)) / 2
    return a + (b - a) * w

class Shake:
    def __init__(self, seed=0, scale=1.0):  # scale: the Screen shake setting; reduced motion passes 0
        self.scale = min(scale, 1.0) if scale > 0 else 0.0  # NaN or negative -> 0
        self.trauma = self.run = self.t = 0.0
        self.rest = SHAKE_REST
        rng = random.Random(seed)            # its own RNG, never the simulation's
        self.phase = [rng.uniform(0, 1000) for _ in range(3)]

    def add(self, amount):
        if self.run < SHAKE_ADD_WINDOW and (self.trauma > 0 or self.rest >= SHAKE_REST):
            self.trauma = min(1.0, self.trauma + (amount if amount > 0 else 0.0))

    def update(self, dt):
        dt = min(dt, 0.25) if dt > 0 else 0.0  # a stall, rewind or NaN can't break it
        self.t += dt
        if self.trauma > 0:
            self.run += dt
            self.rest = 0.0
            self.trauma = max(0.0, self.trauma - SHAKE_DECAY * dt)
        else:
            self.rest += dt
            if self.rest >= SHAKE_REST:
                self.run = 0.0

    def offset(self, short_side):            # (dx px, dy px, roll degrees) for the view only
        k = self.trauma ** 2 * self.scale
        nx, ny, nr = (_noise(p + self.t * SHAKE_HZ) for p in self.phase)
        a = SHAKE_MAX_FRAC * short_side * k
        return a * nx, a * ny, SHAKE_MAX_DEG * k * nr

class FlashGate:
    def __init__(self):
        self.times = []

    def allow(self, now):                    # call once per flash; False means skip the flash
        self.times = [t for t in self.times if now - t < 1.0]
        if len(self.times) >= FLASH_MAX:
            return False
        self.times.append(now)
        return True

class HitStop:
    def __init__(self):
        self.grants = []                     # (start, seconds)

    def request(self, now, seconds):         # returns the freeze granted, maybe 0
        self.grants = [g for g in self.grants if now - g[0] < 1.0]
        used = sum(s for _, s in self.grants)
        give = max(0.0, min(seconds, HITSTOP_MAX, HITSTOP_BUDGET - used))
        if give:
            self.grants.append((now, give))
        return give

if __name__ == "__main__":                   # asserts use the Caps table's numbers, not the constants
    dt, side = 1 / 60, 720
    s = Shake(seed=1)                        # hammered every frame for 5 s
    peak = roll = run = rest = 0.0
    runs, rests = [], []
    for _ in range(300):
        s.add(1.0); s.update(dt)
        dx, dy, r = s.offset(side)
        peak, roll = max(peak, abs(dx), abs(dy)), max(roll, abs(r))
        if s.trauma > 0:
            if rest: rests.append(rest)
            run, rest = run + dt, 0.0
        else:
            if run: runs.append(run)
            run, rest = 0.0, rest + dt
    assert peak <= 0.02 * side and roll <= 2.0, (peak, roll)
    assert runs and max(runs) <= 1.0 + dt, runs                 # continuous shaking <= 1 s
    assert rests and min(rests) >= 0.25 - 1e-9, rests           # then >= 0.25 s at rest
    one = Shake(); one.add(1.0); n = 0
    while one.trauma > 0:
        one.update(dt); n += 1
    assert n * dt <= 0.5 + dt, n                                 # one shake gone in 0.5 s
    off = Shake(scale=0.0); off.add(1.0); off.update(dt)
    assert off.offset(side) == (0.0, 0.0, 0.0)                   # reduced motion: no travel
    bad = Shake(scale=math.nan); bad.add(math.nan); bad.update(math.nan)
    assert bad.offset(side) == (0.0, 0.0, 0.0) and bad.t == 0.0  # a corrupt setting shakes nothing
    a, b = Shake(seed=7), Shake(seed=7)
    for x in (a, b):
        x.add(0.5); x.update(dt)
    assert a.offset(side) == b.offset(side)                      # same seed, same shake
    g = FlashGate(); ok = [i * dt for i in range(180) if g.allow(i * dt)]
    assert all(sum(1 for t in ok if w <= t < w + 1) <= 2 for w in ok), ok
    h = HitStop()
    assert h.request(0.0, 0.3) <= 0.12
    total = h.grants[0][1] + sum(h.request(i * 0.05, 0.1) for i in range(1, 19))
    assert total <= 0.2 + 1e-9, total                            # <= 200 ms frozen per second
    print("juice caps hold")
```

Pass the settings in once: `Shake(seed, scale=0 if reduced else shake_setting)`. Under **Flashing: off**, still call `FlashGate.allow` and draw the edge tint instead.

## Engine notes

- **Phaser** (`fm lib show phaser`): `this.cameras.main.shake(duration, intensity)` takes intensity as a fraction of the camera size and defaults to 0.05, which is over the cap: pass ≤ 0.02 and ≤ 500 ms, or drive the offset from `Shake`. `this.cameras.main.flash(...)` goes through `FlashGate`. Hit-stop: `this.physics.pause()`, then `this.time.delayedCall(ms, () => this.physics.resume())`; the scene clock keeps running while physics is paused.
- **Pygame** (`fm lib show pygame`): draw the world to its own surface, blit it at `(dx, dy)`, then draw the HUD on top unshaken. Hit-stop skips steps in the fixed-step accumulator.
- **Godot** (`fm lib show godot`): set `Camera2D.offset` in `_process` (render), never in `_physics_process`; a HUD in a `CanvasLayer` doesn't move with the camera. For hit-stop through `Engine.time_scale = 0`, restore it with `get_tree().create_timer(sec, true, false, true)` (the last argument ignores time scale), or the timer never fires.
- **LÖVE** (`fm lib show love2d`): `love.graphics.push()`, `translate(dx, dy)`, draw the world, `pop()`, then the HUD.
- **Unity** (`fm lib show unity`): hit-stop via `Time.timeScale = 0` must restore in a coroutine waiting on `WaitForSecondsRealtime`; plain `WaitForSeconds` never returns while time is stopped. Cinemachine Impulse amplitudes are clamped to the shake cap.
- **DOM and canvas UI** (`fm lib show animation`): squash and element shake use `motion.md`'s tokens through WAAPI or CSS; a canvas confetti loop is a `prefers-reduced-motion` exception with a comment saying why, per `motion.md`.

## Check it

- `python3 juice.py` (or its port's test) prints `juice caps hold`; the constants match the Caps table.
- `grep -rnE "shake\(|\.flash\(|timeScale|time_scale" src` — each hit goes through `Shake`, `FlashGate` or `HitStop`, or passes literal values within the caps.
- `grep -rnE "Math\.random|random\.(random|uniform|randint)|randf|Random\.Range" src` inside effect code — none: effects use their own seeded RNG.
- The juice table exists in the task's brief or PR, every cell filled, and the built game matches it.
- Play the busiest scene with Motion: Reduced, then with Screen shake 0 and Flashing off: each Reduced cell happened, nothing moved that the table says stays still, and the seeded replay's simulation hash equals the full-motion run's.
- Record 10 s of the busiest scene and step it frame by frame (or run it through a photosensitivity analyser such as PEAT): no 1 s window holds more than two flashes.
- Sound starts off on a fresh install; turning it on survives a restart.

## Library cards

`fm lib show game-loop` (fixed step, hit-stop's home), `fm lib show game-physics` (render interpolation, why collision shapes don't squash), `fm lib show phaser`, `fm lib show pygame`, `fm lib show godot`, `fm lib show godot-gdscript`, `fm lib show love2d`, `fm lib show unity`, `fm lib show monogame`, `fm lib show animation` (WAAPI and CSS for playful UI), `fm lib show accessibility`. Add `--section verify` for each card's checks.
