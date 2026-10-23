<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Sound design: off by default, earcons, volume caps

Use when a web or app UI plays sound: notification chimes, confirmations, alerts, timers, ambient beds. Games and
playful UI start from `game-feel.md`, whose sound caps this file shares; the two never disagree.

Sound reaches people who did not choose to look at your screen (the next desk, a meeting, a sleeping child), so
every cue is opt-in and earns its place.

## The procedure

1. **Earn each cue.** List the events that make a sound. A cue is justified only when the person is likely not
   looking (a message arrives, a long job finishes, a timer ends) or the moment needs confirming beyond the screen
   (a payment sent). Never on hover, typing, scrolling or ordinary clicks. Pass: the cue table has five rows or
   fewer and each names its reason.
2. **Off by default, and the person's choice.** Sound starts off on a fresh install, is turned on in settings (and
   may be offered once where the first cue would fire), and the choice survives a restart. Nothing plays before the
   first input; create or resume the `AudioContext` inside that gesture. Pass: a fresh profile makes no sound and
   creates no audio context until sound is enabled.
3. **Design earcons as one family.** One timbre for the product; meaning carried by pitch contour: rising for
   arrival or success, falling for leaving or failure, a repeat for attention. Confirmations last 300 ms or less,
   alerts 1 s or less. Pass: every pair of cues differs in contour, not only in loudness.
4. **Cap the volume.** Every file peaks at −6 dBFS or below, the cues' average levels (RMS, with leading and
   trailing silence trimmed) sit within 6 dB of each other, and in-app volume defaults to 50%, separate from the system's. Fade every cue in and out over at
   least 5 ms so it doesn't click. Pass: `sound_check.py` below exits 0 on the cue folder.
5. **Limit repeats** with game-feel's caps: one cue retriggers at most once per 50 ms, no more than 8 voices play at
   once, pitch jitter stays within ±5%. A burst of twenty notifications plays one cue. Pass: a unit test fires a
   cue twenty times in a loop and counts one play.
6. **Never the only signal.** Every cue has a visual twin (a toast, a badge, a focus change), and screen-reader
   users get an `aria-live` announcement, not a sound. Reduced motion never mutes: motion and sound are separate
   settings.
7. **Ship small.** Cues are decoded once and reused (Web Audio `decodeAudioData`), Opus or AAC with one fallback
   format, and all UI cues together weigh 100 KB or less.
8. **Listen once on real hardware**: laptop speakers and headphones at 50% volume, and say in the task log that you
   did.

## Checking the files

`sound_check.py` reads 16-bit PCM WAV masters (export them before encoding) and fails on a cue whose peak is
too high, that runs too long, or whose average level (RMS) is out of step with the family's. RMS is a rough stand-in
for loudness; when the cues differ a lot in pitch, confirm by ear in step 8.

```python no-run
#!/usr/bin/env python3
"""sound_check.py CUE.wav... — peak, length and RMS spread for UI cues; exits 1 on any failure."""
import array, math, sys, wave

MAX_PEAK_DBFS, MAX_SECONDS, MAX_RMS_SPREAD_DB = -6.0, 1.0, 6.0


def dbfs(x):
    return 20 * math.log10(x / 32768) if x else -math.inf


def measure(path):
    with wave.open(path) as w:
        if w.getsampwidth() != 2:
            raise ValueError("16-bit PCM only")
        seconds = w.getnframes() / w.getframerate()
        samples = array.array("h", w.readframes(w.getnframes()))
    if sys.byteorder == "big":
        samples.byteswap()
    peak = max((abs(s) for s in samples), default=0)
    rms = math.sqrt(sum(s * s for s in samples) / len(samples)) if samples else 0
    return seconds, dbfs(peak), dbfs(rms)


def main(paths):
    fails, levels = [], []
    for p in paths:
        try:
            seconds, peak, rms = measure(p)
        except (OSError, EOFError, ValueError, wave.Error) as e:
            fails.append(f"{p}: unreadable ({e})")
            continue
        print(f"{p}: {seconds * 1000:.0f} ms, peak {peak:.1f} dBFS, RMS {rms:.1f} dBFS")
        if peak > MAX_PEAK_DBFS:
            fails.append(f"{p}: peak {peak:.1f} dBFS is over {MAX_PEAK_DBFS}")
        if seconds > MAX_SECONDS:
            fails.append(f"{p}: {seconds:.2f} s is longer than {MAX_SECONDS} s")
        if rms > -math.inf:
            levels.append(rms)
    if len(levels) > 1 and max(levels) - min(levels) > MAX_RMS_SPREAD_DB:
        fails.append(f"RMS levels spread {max(levels) - min(levels):.1f} dB, over {MAX_RMS_SPREAD_DB}")
    print("\n".join(fails) or "ok")
    return 1 if fails or not paths else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

Confirmations over 300 ms pass this script but fail step 3; keep the cue table's length column honest.

## Checks

- [ ] A fresh profile makes no sound; enabling sound survives a restart.
- [ ] The cue table has five rows or fewer, each with its reason, length and visual twin.
- [ ] `python3 sound_check.py cues/*.wav` exits 0.
- [ ] A test proves twenty rapid fires of one cue play once.
- [ ] Turning on reduced motion leaves sound as it was.
- [ ] All UI cues together are 100 KB or less as shipped.

## Library cards

`fm lib show python-audio` (loading, resampling and measuring audio in Python), `fm lib show browser-storage`
(remembering the choice), `fm lib show accessibility` (live regions, never sound alone), `fm lib show toasts` (the
visual twin).

## UI contract

- motion: n/a: sound doesn't move; each cue's visual twin follows the motion rule.
- contrast: every cue has a visual twin that meets the contrast rule, so nothing is told by sound alone.
- keyboard: the sound toggle and volume are keyboard reachable, with visible focus.
- small screens: the sound controls fit at 360 px, and sound stays off by default at every size.
- states: muted, playing and a failed audio load each have a designed state; an error never only beeps.
