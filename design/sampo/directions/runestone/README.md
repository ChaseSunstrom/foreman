# Runestone: a carved rune millstone with a forge-lit core

Feels like: a hearthstone at night, the only light coming from the eye of the mill.
Look bank: look-darkroom (one bright thing on near-black).

## Concept

The Sampo seen from above as the millstone itself. The iron stone carries the millstone's dress, eight furrows
spiralling out from the eye, so it reads as working machinery. Between the furrows sits a ring of eight runes, the
myth's spell cut into the stone. The eye at the centre glows forge-hot, crossed by the rynd, the iron bar that drives a
real millstone. Myth comes from the runes and the glow; machine comes from the dress, the rynd and the turning.

The runes are invented staves, not a real alphabet. One is fehu (wealth). Every form that hate groups have adopted is
left out: sowilo, othala, algiz, tiwaz, the wolfsangel and any three- or four-armed rotational figure.

## Palette

- Stone: iron `#16181C`. Rim: hammered bronze `#B07A3B`. Furrows: a lighter iron `#2E333B`, carved rather than drawn.
- Runes: forge light `#FF9E3D`. The eye is a gradient from white heat `#FFE3A8` through forge light to ember `#E0601F`.
- Wordmark: the capitals SAMPO are carved in bronze, with chiselled serifs. In UI text use the token `bronze`
  (`#7A5020` light, `#D9A870` dark), because brand bronze is only 3.2:1 on parchment and that is for display size only.
- Mono: one ink, the rim, dress, runes and a ringed eye.

## Motion

The stone turns 135 degrees into place over 4 s and eases to a stop. The eye heats up as it turns. The runes light one
after another, 240 ms each, and three embers leave the rim at the end. Reduced motion shows the still: every rune
lit, no sparks.

## Strong

- It is the most mythic of the three: it reads as an artefact, not an app icon, and it is unmistakably the Sampo
  (a mill with a spell in it).
- On dark surfaces the glowing eye is the whole brand: it works as a status light, a favicon and a splash screen.
- The 16 px icon (a bronze ring, six forge ticks and a hot eye) survives where the runes cannot.

## Weak

- The detail goes at small sizes: below 32 px the runes merge into a ring of dots. The 16 px icon is a simplified
  redraw, not a scaled mark.
- It is dark-first. On parchment it becomes a dark disc, heavy next to light UI.
- Runes always carry a risk of reading as generic fantasy or of being misread. The staves are vetted, but a
  reviewer who reads runes should check them once more before launch.
- The serif wordmark doesn't sit easily next to a terminal.
