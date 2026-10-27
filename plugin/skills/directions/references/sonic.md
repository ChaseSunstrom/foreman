# Sonic UI recipes

Small sounds can confirm an action the eye missed. They are off by default: a page plays nothing until the person
turns sound on, and the choice is kept for next time. Use this set only when the look you picked calls for it.

## Rules

- Off by default. A visible Sound switch turns it on; store the choice (`localStorage`) and read it on load.
- Never the only signal. Every sound pairs with something on screen: a toast, a state change, a focus move.
- Short and quiet: under 300 ms, peak gain 0.08 or less, no sound on page load or on hover.
- One sound per meaning, the same everywhere: success always sounds like success.
- Synthesised with Web Audio, so there are no files to fetch, license or cache.

## The set

| Name | When | Recipe (frequency Hz, start ms, length ms) |
| --- | --- | --- |
| tap | a button or toggle took the press | 880 at 0 for 30 |
| success | a save, a send, a check that passed | 660 at 0 for 90, 990 at 70 for 140 |
| error | something failed and the page says what | 330 at 0 for 120, 220 at 100 for 180 |
| notify | something arrived that wasn't asked for | 784 at 0 for 80, 988 at 90 for 80, 1175 at 180 for 120 |
| off | sound was just turned off (the last sound it makes) | 440 at 0 for 60, 330 at 50 for 90 |

## The player

```js
const SOUNDS = {
  tap: [[880, 0, 30]],
  success: [[660, 0, 90], [990, 70, 140]],
  error: [[330, 0, 120], [220, 100, 180]],
  notify: [[784, 0, 80], [988, 90, 80], [1175, 180, 120]],
  off: [[440, 0, 60], [330, 50, 90]],
};
let audio = null;
function soundOn() {
  try { return localStorage.getItem("sound") === "on"; } catch { return false; }
}
function play(name) {
  if (!soundOn() || !SOUNDS[name]) return;
  audio ??= new AudioContext(); // created on the first play, which follows a press
  const now = audio.currentTime;
  for (const [hz, at, ms] of SOUNDS[name]) {
    const osc = audio.createOscillator(), gain = audio.createGain();
    const t0 = now + at / 1000, t1 = t0 + ms / 1000;
    osc.type = "sine";
    osc.frequency.value = hz;
    gain.gain.setValueAtTime(0, t0);
    gain.gain.linearRampToValueAtTime(0.08, t0 + 0.008); // a soft attack, no click
    gain.gain.exponentialRampToValueAtTime(0.0001, t1);
    osc.connect(gain).connect(audio.destination);
    osc.start(t0);
    osc.stop(t1 + 0.02);
  }
}
```

The switch is a real control (`<button aria-pressed>` or a checkbox) labelled "Sound", next to the page's other
settings. Turning it off plays `off` once, then sets `localStorage.sound = "off"`.
