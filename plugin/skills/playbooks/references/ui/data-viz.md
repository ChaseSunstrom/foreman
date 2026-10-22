<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Data viz: one claim, one axis, colour by job

Use when a screen, report or doc shows numbers as a chart, a sparkline or a big number. It builds on
`type-and-colour.md` (palette roles, reserved status colours, contrast) and `motion.md` (tokens, reduced motion);
those rules hold here unchanged.

## The procedure

1. **Write the claim first.** One sentence the chart must prove ("Signups doubled after the March launch"). It
   becomes the title. Pass: the title is a claim or a question, never a label like "Signups chart".
2. **Pick the form by the job** (table below). Pass: the chart's form is the one its job's row names, or `DESIGN.md`
   says why not.
3. **One value axis.** No chart has two y-axes with different scales: two measures in different units become two
   charts stacked on the same x-axis (small multiples). Bars start at zero; a line may not, and then the axis says so
   with a visible break or a labelled first tick. Pass: the one-axis grep in Checks returns nothing.
4. **Colour by job, from the roles.** Charts use roles, never raw colours:
   - one series → `--accent`; the series the claim is about → `--accent`, every other series → `--text-muted`;
   - `--error`, `--warning`, `--success` only when a value means that state (over budget, failing); a plain
     category is never red, amber or green, because those hues are reserved;
   - more than one category hue → series roles `--series-1` … `--series-6` in the token file, named in `DESIGN.md`,
     `--series-1` being the accent and each at least 30° from every status hue; seven or more categories → group
     the smallest into "Other" or use small multiples;
   - ordered values (low to high) → one hue's lightness steps; values around a meaningful middle (zero, target) →
     two hues either side of a neutral middle.
   Every mark is 3:1 against the surface it sits on, and every series also has a direct label or a pattern: colour
   is never the only signal.
5. **Label directly.** Series names sit at the end of their line; values sit on the bars when there are 12 or fewer.
   A legend only when direct labels would collide. Units are in the axis title or the ticks; numbers use
   `font-variant-numeric: tabular-nums` and the reader's locale.
6. **A table view for every chart.** The same numbers as a real `<table>`, one keypress or click away ("Show as
   table" or a `<details>` under the chart), with units in the headers. The chart itself is a `<figure>` whose
   `<figcaption>` states the claim, or an element with `role="img"` and an `aria-label` that does. Pass: a test
   asserts the table's rows equal the chart's data points.
7. **Motion from the tokens.** Changed values travel with `--dur-move` and `--ease-move`, arriving marks use
   `--dur-enter` and `--ease-enter`, and the whole chart update ends within `--dur-stage`. Under reduced motion values
   change in place without travel (`--travel: 0`; a cross-fade at `--dur-small` at most). No idle or looping motion.
8. **Empty, loading and error states.** No data says so in a sentence ("No orders between 1 and 7 May"), never empty
   axes. Loading follows motion.md's wait thresholds; an error says what failed and offers a retry.

## Form by job

| Job | Use | Avoid |
|---|---|---|
| compare amounts across categories | bars, sorted, horizontal when labels are long | pie with more than 3 slices, 3D |
| change over time | a line (8+ points), bars for a few periods | stacked areas that hide each series |
| part of a whole | one stacked or 100% bar; a pie only for 2–3 parts | a donut with many slices |
| distribution | histogram, box or strip plot | an average alone |
| two measures against each other | scatter | a dual-axis line |
| one number | the number, large, with its comparison ("+12% on last week") | a gauge |
| exact lookup | a table | any chart |

## Checks

- [ ] Each chart's title is a claim or a question.
- [ ] `grep -rnE "twinx\(|secondary_y|yaxis2|y2Axis|independent.*\"y\"|\"y\".*independent" src` returns nothing,
      and `grep -ro "<YAxis" src | sort | uniq -c | grep -vE "^ *1 "` returns nothing (one value axis per file;
      adjust the patterns to your chart library).
- [ ] `grep -rnE "#[0-9a-fA-F]{3,8}\b|oklch\(|rgb\(" src/charts` returns nothing: chart colours come from roles.
- [ ] No category series uses `--error`, `--warning` or `--success`; series roles are named in `DESIGN.md`.
- [ ] The contrast proof in `type-and-colour.md` covers each series role against its surface at 3:1, in both themes.
- [ ] Every chart has a reachable table with the same numbers, and an accessible name stating the claim.
- [ ] Under reduced-motion emulation a data update moves nothing (no `transform` transition runs).

## Library cards

`fm lib show d3` (scales and axes), `fm lib show recharts`, `fm lib show plotly`, `fm lib show matplotlib`,
`fm lib show data-tables` (the table view), `fm lib show color-contrast`, `fm lib show accessibility`,
`fm lib show animation`.
