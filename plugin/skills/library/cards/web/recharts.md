---
name: recharts
title: Recharts
area: web
tags: [recharts, react, charts, svg, responsive, dataviz]
detect: [dep:recharts]
related: [react, d3, testing-library]
---
Recharts: declarative React SVG charts built from composable components over an array of plain data objects.

## Verify
- `npx tsc --noEmit`: data keys and component props type-check.
- `npx eslint .`: lint.
- `npx vitest run`: data-shaping tests and component render tests.
- `npm run build`: production build.

## Test first
Test the data transform, which is where chart bugs live; add a render smoke test with a fixed size.
```tsx
import { render } from "@testing-library/react";
import { LineChart, Line } from "recharts";
import { toSeries } from "./series";

test("sorts by date and fills missing values with null", () => {
  expect(toSeries([{ d: "2024-02-01", v: 2 }, { d: "2024-01-01" }]))
    .toEqual([{ d: "2024-01-01", v: null }, { d: "2024-02-01", v: 2 }]);
});

test("renders a line", () => {
  const { container } = render(
    <LineChart width={300} height={200} data={[{ x: 1, y: 2 }, { x: 2, y: 3 }]}>
      <Line dataKey="y" />
    </LineChart>);
  expect(container.querySelector(".recharts-line")).not.toBeNull();
});
```

## Do
- Wrap charts in `ResponsiveContainer` with a parent that has a definite height (`width="100%" height="100%"` inside a sized div, or a numeric `height`).
- Shape data into a flat array of objects first; point each series at a key with `dataKey`.
- Give each series an explicit, accessible color from your theme tokens; do not rely on defaults for meaning.
- Use `Tooltip`, `Legend` and axis `tickFormatter` to format dates and numbers consistently.
- Set `isAnimationActive={false}` for large data or tests.
- Memoize the data array and custom tooltip or tick components so a parent render does not rebuild the chart.
- Use `connectNulls` or leave gaps deliberately for missing values.
- Provide a text summary or table alternative for screen readers.

## Avoid
- `ResponsiveContainer` inside a zero-height parent: the chart renders nothing and logs a width and height warning. Give the parent a height.
- Passing a new `data` array literal every render: the chart re-animates and flickers. Memoize.
- Defining custom tooltip or tick components inline: remount on each render. Define them outside.
- Thousands of points with animation and dots on: slow. Downsample, drop `dot`, disable animation.
- Mixed types in a numeric axis (strings for numbers): wrong scale. Convert first and set `type="number"` for numeric x axes.
- Relying on color alone to distinguish series: add direct labels or dash patterns.

## Review
- [ ] The chart has a sized container and does not collapse.
- [ ] Data is memoized, sorted and null-safe.
- [ ] Colors come from tokens and series are distinguishable without color.
- [ ] Axes and tooltips format units and dates.
- [ ] Large series are downsampled or animation is off.
