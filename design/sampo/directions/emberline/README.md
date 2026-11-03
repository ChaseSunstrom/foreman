# Emberline: an iron-and-ember monoline mark built for terminals

Feels like: a prompt that has been left running in the forge overnight, and the work is done when you come back.
Look bank: the terminal-ui playbook and svg-icon-system (one grid, one stroke weight, square terminals).

## Concept

The Sampo reduced to a working glyph. The ring is the millstone, drawn in one monoline stroke and open at the lower
right where the mill pours out. Its eye is a block cursor in ember: the forge and the prompt in one shape. Out of the
gap come three square grains, the Sampo's grain, salt and gold, as pixels. A mill that keeps producing while nobody
turns it is exactly the promise of an unattended agent run. Myth comes from the mill, the three outputs and the ember
eye, machine from the cursor, the pixel grains and the stepped motion. The wordmark is lowercase monoline `sampo`
followed by the same block cursor.

## Palette

- Ground: iron `#16181C` on a rounded tile, the same shape a terminal or dock icon sits in.
- Ring, grains and lettering: parchment `#F6F0E4`, the colour of terminal text.
- The cursor and the sparks are ember `#E0601F`, and nothing else is. Ember always means "alive".
- Mono: one ink, no tile. The cursor becomes solid ink, so the mark still works as a single-colour glyph.

## Motion

Everything moves in steps, as a terminal does. The ring steps round once in eight 45 degree jumps (2 s), and the cursor
blinks four times. Then two sparks flick off the gap and the grains pour out one after another, three frames each.
Reduced motion shows the still: a solid cursor and all three grains out. The same glyph can serve as the pane's
"running" indicator.

## Strong

- It is the best at small sizes. Four shapes on a pixel grid make the 16 px icon crisp, and at 16 px it is the most
  recognisable of the three.
- It is native to where Sampo lives: terminal, tmux pane, status line. The grains and the cursor can even be drawn with
  block characters (`▌`, `▪`) in a text UI.
- It is cheap to animate and to reproduce. Each state (idle, running, done) is a small change to one glyph.
- It works on light and dark alike: the tile carries its own ground.

## Weak

- The myth reads least here. Without the story, it is "a ring and a cursor", and the Sampo is only implied.
- An open ring with dots beside it can read as Pac-Man at a glance. The square grains, the cursor eye and the pour
  direction (out of the mouth, not into it) work against that, but the risk is real.
- Square tiles with a monoline glyph are a common dev-tool look, so it is the closest of the three to generic SaaS.
  It relies on ember plus the grains to stand apart.
- There is no bronze, so it drops the hammered-metal warmth that the brand palette promises.
