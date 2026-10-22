<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Type and colour that read as chosen

Use when a web or app screen gets its type and colour: a new product, a restyle, a dark mode, or "the text looks off". `design-direction.md` picks the stance (the family class, the scale ratio, the ink); this playbook turns that stance into a scale, a pairing, a palette and the proof that they hold. For terminals see `terminal-ui.md`.

Type and colour look default when nothing in them was decided: one sans at whatever size the framework shipped, grey text, a blue button, a dark mode made by inverting. Every rule below is a decision you write down and a reviewer can mark pass or fail. The code side (rem units, font loading, token plumbing, theme switching) lives in the library cards at the end.

## Type scale

A scale is a list of sizes made by multiplying one base by one ratio. Every size in the UI comes from it; nothing in between.

1. **Base is `1rem`** for body text, and the root font size stays the browser's (never `html { font-size: 62.5% }` or a px root). Phones too: body below 16 px is a fail, and form inputs below 16 px make iOS zoom on focus.
2. **One ratio, taken from the direction.** The audacity setting in `design-direction.md` gives the range; pick one value inside it and write it in `DESIGN.md`.

   | Ratio | Name | Feels | Use for |
   |---|---|---|---|
   | 1.2 | minor third | quiet, even | dense tools, settings, long forms |
   | 1.25 | major third | clear, unshowy | most products |
   | 1.333 | perfect fourth | confident | marketing pages, editorial |
   | 1.5 | perfect fifth | loud | landing pages, portfolios |
   | 1.618 | golden ratio | theatrical | posters, events, one-screen launches |

3. **Name steps by number, not by element.** `--step--1`, `--step-0` (body), `--step-1`, … A heading level picks a step; an `h2` is not a size. This lets a card title and a section heading share a step without anyone inventing 19 px.
4. **Seven steps or fewer** in a product UI (one below body, body, up to five above). A screen using more than five distinct sizes has a hierarchy problem that more sizes will not fix.
5. **Adjacent levels in use differ by at least 1.2×.** With a 1.125 or 1.2 ratio, skip a step between heading levels so the gap holds. Weight alone separating two levels is the "flat hierarchy" default and fails.
6. **Steps above body are fluid; body and below are not.** Steps 1 and up scale between a phone ratio and a desktop ratio with `clamp()`, keeping a `rem` term so zoom still works (`fm lib show typography`). Leaving step 1 fixed while step 2 shrinks squeezes the gap between them below 1.2× on phones.
7. **Leading falls as size rises.** Unitless `line-height`: about 1.5 for body, 1.3–1.4 for steps 1–2, 1.1–1.2 for steps 3–4, 1.0–1.1 for display. Display type at 1.5 looks like separate lines, not a heading.
8. **Tracking follows size** (always in `em`, never `px`): text under 14 px +0.01 to +0.02em; body 0; step 3 and up −0.01 to −0.02em; display −0.02 to −0.04em; all-caps labels +0.06 to +0.12em, because capitals set tight crowd into a bar.

Pass: every `font-size` in the components is a `var(--step-N)`, and `DESIGN.md` names the base and the ratio.

## Pairing

The default is one family. A second family is a cost (another file, another voice) and must earn it with a job the first can't do.

- **Valid jobs for a second family:** display headlines with a voice the text face lacks; long-form reading where a serif sets better than the UI sans; numbers and code, where a mono or a family with tabular figures keeps columns straight.
- **Two families must differ on at least two axes:** classification (serif, sans, slab, mono), width (condensed, normal, extended), stroke contrast (even strokes vs thick-thin), and x-height (tall vs short lowercase). Two geometric sans side by side differ on none and read as a mistake. Pass: `DESIGN.md` names the two axes.
- **Each family owns a role,** written down: "serif: headings step 3 and up; sans: everything else; mono: amounts and IDs". A family showing up outside its role fails.
- **At most two families plus a mono,** and at most three weights across the whole UI (two for the trustworthy direction). Check: `grep -rhoE "font-(family|weight):[^;]+" src | sort -u`.
- **Match x-heights where families meet inline** (a mono ID inside a sans sentence, a sans label beside serif text): use `font-size-adjust`, or `size-adjust` in the `@font-face`, so lowercase letters line up instead of the mono looking a size too big.
- **Real styles only.** Set `font-synthesis: none` so the browser can't fake bold or slant a roman into "italic"; load the italic if you use one.
- **Numbers are typography too.** Tables, prices, timers and anything that updates in place get `font-variant-numeric: tabular-nums`; prose may use proportional figures. A column of amounts whose digits don't align fails.

Families are chosen by class, then by licence and language coverage. The names below are open-licensed examples of each class, not recommendations; check that the one you pick covers every language the product ships in.

| Class | Reads as | Examples of the class |
|---|---|---|
| grotesk | plain, industrial, a little quirky | Archivo, Schibsted Grotesk |
| neo-grotesk | neutral, Swiss, corporate | Public Sans, Hanken Grotesk |
| geometric sans | built, modern, round | Jost, Outfit |
| humanist sans | warm, legible, written by a hand | Source Sans 3, Fira Sans |
| transitional serif | sober, bookish, trustworthy | Source Serif 4, Libre Caslon Text |
| old-style serif | literary, old, warm | EB Garamond, Crimson Pro |
| Didone | fashion, luxury, high contrast | Bodoni Moda, Playfair Display |
| slab | sturdy, typewriter, signage | Zilla Slab, Roboto Slab |
| mono | technical, receipts, code | IBM Plex Mono, JetBrains Mono |

## Type as texture

Step back from a page and the text becomes a pattern of greys. A designed page has distinct textures; a default one is a single even grey.

- **The squint test.** Blur a screenshot of the screen by about 8 px (any image tool, or `body { filter: blur(8px) }` in devtools). Pass: you can see at least three different greys of text (a dark heading block, the body, a light band of labels or captions) and tell where the primary action is. One uniform grey fails.
- **Labels are a texture of their own.** Small caps or uppercase at step −1, tracked +0.08em, muted colour: they read as furniture and let the content above them be the content.
- **Weight contrast beats size creep.** Before adding a size, try a weight change of at least 200 (400 against 600 or 700). Two weights 100 apart (400 and 500) look like a rendering error.
- **Density is a voice.** A dense list at 1.3 leading reads as a tool; the same words at 1.7 with wide margins read as a letter. Pick the one the direction asks for and hold it on every screen.

### When the type is the hero

Some directions (Poster, editorial, bold) let a headline do what an image would. Then it follows its own rules:

- **Size:** the display step is at least 6× body on desktop (a 1.25 ratio reaches that at step 8, 6rem). Set it with `clamp()` so it shrinks on phones but stays at least 3× body.
- **Short:** six words or fewer, broken by hand at phrase boundaries (`text-wrap: balance` as the fallback), never mid-phrase.
- **Tight:** leading 0.85–1.0 and tracking −0.02 to −0.04em, so it reads as one shape.
- **Alone:** no image, illustration or second headline competes in the same viewport. Supporting text sits at step 0 or 1, not in between.
- **It fits:** at a 320 px wide viewport there is no horizontal scroll (`document.documentElement.scrollWidth <= 320`) and no word is broken mid-letter. Long words are the usual failure: lower the `clamp()` minimum, don't add `overflow-wrap: anywhere` to a headline.
- **It is text:** real, selectable HTML, not an image or SVG of letters; the floors in `design-direction.md` still apply.

## Measure and leading

- **Measure is 45–75 characters** for running text (about 65 is the target), set as `max-width` in `ch` on the text element itself, not on its container. Captions and side notes 40ch or fewer. Pass: no paragraph on a 1440 px screen is wider than 75ch.
- **Leading grows with measure.** Under 50ch, 1.4 is enough; at 65–75ch use 1.55–1.65, because the eye needs a wider track to find the next line.
- **Paragraphs are separated one way:** a gap of about one line, or a first-line indent, never both.
- **A heading belongs to what follows it:** space above a heading is at least twice the space below it. Equal space above and below makes headings float between sections.
- **Spacing comes in steps too.** Gaps inside a group are smaller than gaps between groups (the "even spacing" default fails); use the spacing tokens from `DESIGN.md`, not new numbers.
- **Line breaks:** `text-wrap: pretty` on paragraphs, `balance` on headings, `lang` set on `<html>` so `hyphens: auto` works where measure is narrow.

## Palette roles

Write colours in **OKLCH** (`oklch(L C h)`: lightness 0–1, chroma, hue angle). Its L is perceptual, so two colours with the same L look equally light whatever their hue, which HSL does not give you (HSL 50% yellow is far lighter than HSL 50% blue). That makes ramps even, makes dark mode a matter of moving L, and makes contrast predictable from the numbers.

**Two layers of tokens.** A *ramp* layer holds the raw values, named by hue and lightness (`--n-22` is the neutral at L 0.22). A *role* layer names jobs (`--text`, `--surface`, `--accent`) and points at the ramp. Components use roles only. Pass: no raw colour and no ramp name appears outside the token file.

The roles every product needs:

| Role | Job | Rule |
|---|---|---|
| `--surface`, `--surface-raised`, `--surface-sunken` | page, cards and popovers, wells and table heads | neutrals only; raised and sunken differ from the page by 0.02–0.05 L |
| `--text`, `--text-muted` | body and secondary text | muted is still ≥ 4.5:1 on every surface it can land on |
| `--border` | edges that tell you a control is there (inputs, checkboxes) | ≥ 3:1 on its surfaces |
| `--hairline` | decorative dividers between things that are already distinct | exempt from contrast, so never the only edge of a control |
| `--accent`, `--accent-hover`, `--on-accent` | the primary action, links, current selection | one hue; text on it ≥ 4.5:1 |
| `--accent-subtle`, `--on-subtle` | selected rows, tags, info backgrounds | the accent at high L, low chroma |
| `--focus` | focus ring | ≥ 3:1 against the surface beside it; often the accent |
| `--error`, `--warning`, `--success` | status | reserved: see below |

Rules for the ramps:

- **The neutral ramp is one hue,** tinted slightly (chroma 0.004–0.016) toward the accent or its warm or cool opposite. Pure greys (chroma 0) are allowed when the direction says so. Pass: every `--n-*` token has the same hue.
- **Name neutrals by lightness** (`--n-97`, `--n-55`, `--n-18`), not by index (`gray-100`). The name then tells you the contrast: see the grey shortcut below.
- **No pure black or white text on pure white or black surfaces** unless the direction asks for it (Poster, Riso zine). `#000` on `#FFF` vibrates on screens; body text near L 0.20 on a surface near L 0.98 reads as ink on paper.
- **One accent hue.** It marks the one primary action per view, links and the current selection, and covers 10% of the screen or less in the squint test. A second accent hue is a second direction and fails unless `DESIGN.md` names it.
- **Status colours are reserved.** Red means error, amber means warning, green means success, and nothing else uses them: no red brand header, no green "new" badge, no amber illustration. Each status hue sits at least 30° from the accent hue; if the brand colour is green or red, the accent takes it and that status is carried by icon and text plus a shifted hue (a teal success beside a green brand). "Info" uses the accent-subtle role or a neutral, never a fourth hue.
- **Colour is never the only signal.** Every status also has an icon or a word; every chart series also has a label or a pattern.
- **Stay inside sRGB** unless you design for wide gamut on purpose. Out-of-gamut OKLCH values are clipped by the browser, chroma and contrast drift, and the hex in your proof no longer matches the screen. Lower the chroma until the value fits (`fm design contrast` flags it); wide-gamut colours go in an `@media (color-gamut: p3)` block, with the sRGB value as the default.

## Contrast

The WCAG 2 ratios are the floor. They are pass or fail numbers, so measure them on the built tokens, not on a mock-up.

| Pair | Needs |
|---|---|
| body text, placeholder text, text on an accent fill | 4.5:1 |
| large text (24 px regular, or 18.67 px bold, and up) | 3:1 |
| control edges, icons that carry meaning, chart marks | 3:1 against what touches them |
| focus ring | 3:1 against the surface beside it |
| disabled controls, logos, pure decoration | exempt, which is why they must never carry information |
| Foreman's own rule: body text in dark mode | 7:1 (see Dark mode) |

**Proof the worst surface, not the default one.** Muted text that passes on the page often fails on a sunken table head or a selected row. Check each text role against every surface it can sit on.

**The grey shortcut.** For a neutral (chroma near 0), WCAG relative luminance is L³. So contrast between two greys is `(L1³ + 0.05) / (L2³ + 0.05)`, and you can read the limits straight off the ramp names:

| Surface L | 3:1 needs text L | 4.5:1 needs text L | 7:1 needs text L |
|---|---|---|---|
| 1.00 | ≤ 0.66 | ≤ 0.56 | ≤ 0.46 |
| 0.97 | ≤ 0.64 | ≤ 0.54 | ≤ 0.44 |
| 0.93 | ≤ 0.61 | ≤ 0.51 | ≤ 0.41 |
| 0.22 | ≥ 0.51 | ≥ 0.61 | ≥ 0.73 |
| 0.18 | ≥ 0.49 | ≥ 0.59 | ≥ 0.70 |

The limits are rounded toward the safe side. Tinted neutrals land within a few hundredths of them; saturated colours do not, so the proof is what decides.

**The proof is a check, not an eyeball.** Keep the pairs in the repo and run them in CI, so a token change that breaks contrast fails a build instead of a person:

```bash
fm design contrast tokens/colour.css text/surface-sunken:7 text-muted/surface-sunken border/surface-sunken:3
```

It reads the token file's custom properties (values in `oklch()`, hex, `rgb()` or `hsl()`; roles as `var()` or `light-dark()`; dark overrides in a `.dark`, `[data-theme="dark"]` or `prefers-color-scheme: dark` block), checks each pair in both themes on the sRGB hex the browser paints (WCAG 2.x relative luminance), warns on out-of-gamut values and exits 1 on any failure. A pair is `fg/bg`, `fg/bg:3` or `fg/bg:4.5,7` (light, dark); with no pairs it checks the roles above (text, muted text, border and accent on each surface, text on the accent and subtle fills), body text 7:1 in dark. A value it can't read stops it with the token's name rather than passing silently. A CI without Foreman copies `plugin/lib/fmdesign.py` (stdlib only, Python 3.11 or later) and runs `python3 fmdesign.py contrast …` the same way. Text over images and gradients still needs a scrim and a spot check by eye (`fm lib show color-contrast`).

**A first palette from one colour.** `fm design palette 'oklch(0.45 0.13 258)'` makes every role above in both themes from one seed (hex, `rgb()`, `hsl()` or `oklch()`): neutrals at the seed's hue with a whisper of its chroma, the accent keeping its hue, and each text role moved in lightness until its pairs pass. It prints CSS `light-dark()` roles (`--format dtcg` for Design Tokens JSON, `tailwind` for a v4 `@theme`) and the proof on stderr, so `> tokens/colour.css` keeps only the tokens. It is a start, not a direction: status colours, hover states and the ramp names are yours to add. `fm design extract <ui root>` then writes the token table, with each pair's contrast, into `DESIGN.md`'s Tokens section.

## Dark mode

Dark mode is a second palette designed with the same roles, not the first palette inverted. Inverting turns shadows into glows, makes the accent glare, and drops most pairs below their ratios. Work through it as its own steps:

1. **Fill a dark column** for every role in the table above, picked from the ramp. A role without a dark value is a fail, even if it "looks fine".
2. **Surfaces sit at L 0.14–0.22,** not `#000`: pure black under light text smears for many readers, and it leaves no room below for depth. Pure black is allowed when the direction asks for it (Night arcade, OLED media players).
3. **Elevation goes up in lightness.** Each raised level is 0.03–0.05 L lighter than the one below it; shadows mostly vanish on dark surfaces, so a raised card also gets a 1 px edge a little lighter than itself.
4. **Text sits at L 0.90–0.95,** not `#FFF`, and body text reaches 7:1 on every dark surface. The WCAG 2 formula over-credits dark pairs (mid-grey on black passes 4.5:1 and is still hard to read), so the dark theme gets the stricter number.
5. **The accent moves up and calms down:** raise its L to 0.70–0.80 and cut chroma by a fifth or more, so it doesn't vibrate on the dark ground. Text on the accent fill flips to the dark surface colour.
6. **Status colours are re-picked** at L 0.70–0.80 with the same hues (within 10°, since yellows drift as they lighten); the light-mode red on a dark surface is muddy and usually fails.
7. **Type gets lighter:** light text on dark looks heavier, so drop body weight by about 50 on a variable font (or use its grade axis), add +0.01em tracking on small text, and add 0.05 to body line height if it feels cramped.
8. **Images and illustrations** get a dark version or a gentle dim; logos get a light-on-dark version. A white-boxed PNG on a dark page fails.
9. **Rerun the proof** for every pair in dark, then look at both themes side by side in screenshots, plus forced-colours mode with borders still visible.

Theme switching, the no-flash script and the stored choice are in `fm lib show dark-mode`. With `light-dark()` (below), the theme is just `color-scheme` on the root: `light dark` follows the system, and a stored choice sets `light` or `dark`.

## Worked example

An invented product: Tallyhouse, bookkeeping for small workshops. `DESIGN.md` says *trustworthy*, safe audacity: a humanist sans for everything, a mono for amounts, base 1rem, ratio 1.25, weights 400 and 600, one deep navy ink, red kept for errors.

**The scale.** Ratio 1.2 on a 360 px phone, 1.25 on a 1280 px desktop, fluid in between. Body and step −1 stay fixed.

| Step | Use | Desktop | Phone | `font-size` | `line-height` | tracking |
|---|---|---|---|---|---|---|
| −1 | labels, captions, table heads | 12.8 px | 12.8 px | `0.8rem` | 1.5 | +0.02em (caps +0.08em) |
| 0 | body, inputs, table cells | 16 px | 16 px | `1rem` | 1.5 | 0 |
| 1 | card titles, `h4` | 20 px | 19.2 px | `clamp(1.2rem, 1.18rem + 0.09vw, 1.25rem)` | 1.4 | 0 |
| 2 | `h3` | 25 px | 23 px | `clamp(1.44rem, 1.392rem + 0.21vw, 1.563rem)` | 1.3 | 0 |
| 3 | `h2` | 31.3 px | 27.6 px | `clamp(1.728rem, 1.64rem + 0.39vw, 1.953rem)` | 1.2 | −0.01em |
| 4 | `h1` | 39.1 px | 33.2 px | `clamp(2.074rem, 1.93rem + 0.64vw, 2.441rem)` | 1.15 | −0.015em |
| 5 | the dashboard total | 48.8 px | 39.8 px | `clamp(2.488rem, 2.268rem + 0.98vw, 3.052rem)` | 1.05 | −0.02em |

Adjacent levels are 1.25× apart on desktop and 1.2× on phones, so the flat-hierarchy check passes at every width. Step 5 is about 3× body: a confident number, not a poster, which is right for *trustworthy*. The fluid values come from `min + (max − min) × (viewport − 360) / (1280 − 360)`.

**The palette**, in the token file the proof reads. Neutrals at hue 250 (leaning toward the navy), named by lightness; the accent at hue 258; status hues at 27, 65 and 150, all more than 30° from the accent.

```css
/* tokens/colour.css — the only file allowed raw colour values */
:root {
  color-scheme: light dark;
  --n-99: oklch(0.99 0.004 250);  --n-97: oklch(0.97 0.006 250);  --n-93: oklch(0.93 0.008 250);
  --n-87: oklch(0.87 0.010 250);  --n-66: oklch(0.66 0.014 250);  --n-55: oklch(0.55 0.016 250);
  --n-45: oklch(0.45 0.016 250);  --n-27: oklch(0.27 0.012 250);  --n-22: oklch(0.22 0.010 250);
  --n-18: oklch(0.18 0.010 250);
  --blue-95: oklch(0.95 0.020 258); --blue-80: oklch(0.80 0.080 258); --blue-74: oklch(0.74 0.100 258);
  --blue-45: oklch(0.45 0.130 258); --blue-39: oklch(0.39 0.120 258); --blue-30: oklch(0.30 0.060 258);
  --red-72: oklch(0.72 0.140 25);   --red-50: oklch(0.50 0.170 27);
  --amber-80: oklch(0.80 0.130 75); --amber-52: oklch(0.52 0.110 65);
  --green-76: oklch(0.76 0.130 150); --green-50: oklch(0.50 0.110 150);
  --white: oklch(1 0 0);

  /* roles: components use only these */
  --surface:        light-dark(var(--n-97), var(--n-18));
  --surface-raised: light-dark(var(--n-99), var(--n-22));
  --surface-sunken: light-dark(var(--n-93), var(--n-27));
  --text:           light-dark(var(--n-22), var(--n-93));
  --text-muted:     light-dark(var(--n-45), var(--n-66));
  --border:         var(--n-55);  /* the same step works on both grounds */
  --hairline:       light-dark(var(--n-87), var(--n-27));
  --accent:         light-dark(var(--blue-45), var(--blue-74));
  --accent-hover:   light-dark(var(--blue-39), var(--blue-80));
  --on-accent:      light-dark(var(--white), var(--n-18));
  --accent-subtle:  light-dark(var(--blue-95), var(--blue-30));
  --on-subtle:      light-dark(var(--blue-39), var(--blue-80));
  --focus:          var(--accent);
  --error:          light-dark(var(--red-50), var(--red-72));
  --warning:        light-dark(var(--amber-52), var(--amber-80));
  --success:        light-dark(var(--green-50), var(--green-76));
}
:root[data-theme="light"] { color-scheme: light; }
:root[data-theme="dark"]  { color-scheme: dark; }
```

The sRGB hex each ramp value lands on, for design tools: `n-99 #FAFCFE`, `n-97 #F2F5F9`, `n-93 #E4E8ED`, `n-87 #CFD5DB`, `n-66 #8C939B`, `n-55 #6B727B`, `n-45 #4F565E`, `n-27 #22272C`, `n-22 #171B1F`, `n-18 #0E1216`, `blue-45 #21539C`, `blue-74 #83ADEA`, `red-50 #B02B27`, `red-72 #F07F77`. All values are inside sRGB.

**The proof.** Each text role is measured on its worst surface, `--surface-sunken` (`fm design contrast tokens/colour.css text/surface-sunken:7 text-muted/surface-sunken …`):

| Pair | Needs | Light | Dark |
|---|---|---|---|
| `text` on `surface-sunken` | 7 | 14.07 | 12.24 |
| `text` on `surface` | 4.5 (7 in dark) | 15.83 | 15.28 |
| `text-muted` on `surface-sunken` | 4.5 | 6.04 | 4.85 |
| `accent` (links) on `surface-sunken` | 4.5 | 6.13 | 6.55 |
| `on-accent` on `accent` | 4.5 | 7.55 | 8.18 |
| `on-accent` on `accent-hover` | 4.5 | 9.69 | 10.10 |
| `on-subtle` on `accent-subtle` | 4.5 | 8.36 | 7.33 |
| `border` on `surface-sunken` | 3 | 3.95 | 3.10 |
| `focus` on `surface-sunken` | 3 | 6.13 | 6.55 |
| `error` on `surface-sunken` | 4.5 | 5.30 | 5.74 |
| `warning` on `surface-sunken` | 4.5 | 4.60 | 7.93 |
| `success` on `surface-sunken` | 4.5 | 4.64 | 7.36 |

Every pair passes. The tight ones are the ones to watch: dark `text-muted` and dark `border` on the sunken surface, light `warning` and `success`. Darken any surface further and those fail first, so they go in CI. `hairline` is left out on purpose: it fails 3:1 (1.35 light, 1.25 dark), which is fine only while no control relies on it for its edge.

## Checks

Each line is pass or fail on the built screens and the token files.

- [ ] `DESIGN.md` names the base, the ratio, each family with its role, the two axes a second family differs on, and the accent hue.
- [ ] `grep -rnE "font-size:\s*[0-9.]+(px|rem|em)" src | grep -v tokens/` returns nothing: every size is a scale step.
- [ ] `grep -rnE "#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|oklch\(" src --include=*.css --include=*.scss | grep -v tokens/colour` returns nothing: no raw colour outside the token file.
- [ ] `grep -rnE "var\(--(n|blue|red|amber|green)-[0-9]+\)" src | grep -v tokens/` returns nothing: components use roles, not ramp steps (use your ramp's names).
- [ ] At most two families plus a mono and at most three weights in `grep -rhoE "font-(family|weight):[^;]+" src | sort -u`.
- [ ] Every number in a table or that updates in place has `tabular-nums`.
- [ ] Running text is at most 75ch wide on a 1440 px screen; body is at least 16 px on a phone.
- [ ] The squint test shows three or more text greys and one clear primary action; the accent covers 10% of the screen or less.
- [ ] Red, amber and green appear only on error, warning and success, each with an icon or word.
- [ ] `fm design contrast` exits 0 in CI for every text role on every surface it can sit on, in both themes; dark body text is at least 7:1.
- [ ] Every role has a dark value; the dark surfaces are not `#000` and dark text is not `#FFF` unless `DESIGN.md` says why.
- [ ] A type-as-hero headline leaves no horizontal scroll at 320 px and at 200% zoom.

## Library cards

The code side lives in the stack library: `fm lib show typography` (rem sizing, fluid `clamp()`, font loading and fallback metrics), `fm lib show color-contrast` (WCAG pairs, states, forced colours, a contrast unit test), `fm lib show dark-mode` (theme switching without a flash, the stored choice), `fm lib show design-systems` (layered tokens and theming), `fm lib show css-custom-properties` (token plumbing), `fm lib show accessibility-testing` (axe in each theme), `fm lib show visual-regression` (screenshot baselines for both themes).
