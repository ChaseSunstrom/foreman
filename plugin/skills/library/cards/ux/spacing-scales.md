---
name: spacing-scales
title: Spacing Scales
area: ux
tags: [ux, spacing, rhythm, tokens, whitespace]
detect: []
related: [css-custom-properties, design-tokens, grid-systems, visual-hierarchy, tailwind]
---
Space comes from a short 4px-based scale, never from ad hoc pixel values.

## Verify
- `grep -rnE "(margin|padding|gap)[a-z-]*: *[0-9]+px" src --include=*.css | grep -vE ": *(0|4|8|12|16|24|32|48|64|96)px"`: lists off-scale values.
- `npx stylelint "src/**/*.css" --config .stylelintrc.spacing.json`: forces tokens. The config holds `{"rules": {"declaration-property-value-allowed-list": {"/^(margin|padding|gap)/": ["/^(var\\(--space-[0-9]+\\)|0|auto)( (var\\(--space-[0-9]+\\)|0|auto))*$/"]}}}`, which also allows `margin: 0 auto`.
- Devtools box model overlay: sibling gaps match across similar components.

## Test first
Fail on any spacing value that is not in the scale.
```python
import re, pathlib
SCALE = {0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128}

def test_spacing_on_scale():
    bad = []
    for f in pathlib.Path("src").rglob("*.css"):
        for m in re.finditer(r"(?:margin|padding|gap)[\w-]*:\s*(\d+)px", f.read_text()):
            if int(m.group(1)) not in SCALE:
                bad.append((str(f), m.group(0)))
    assert not bad, bad
```

## Do
- Base unit 4px; steps 4, 8, 12, 16, 24, 32, 48, 64, 96. Name them `--space-1` to `--space-9` (tokens, not px names).
- Use 8px multiples for layout and 4px only for tight icon-to-label gaps.
- Rule of proximity: space inside a group is at most half the space between groups (8 inside, 24 between).
- Use `gap` on flex and grid containers instead of margins on children.
- Scale padding with type: buttons use 0.5em / 1em so they follow font size; section padding steps up at breakpoints (48 mobile, 96 desktop).
- Use logical properties (`padding-inline`, `margin-block`) so RTL works.

## Avoid
- Odd values (13px, 22px) copied from a design file: round to the nearest step and tell the designer.
- Margins on both neighbours (collapsing surprises): own spacing from one side only.
- Using space tokens for sizes (width, height): spacing tokens are for gaps only.
- More than 9 steps: a scale with every value is no scale.

## Review
- [ ] Every margin, padding and gap resolves to a scale token or 0.
- [ ] Inner group spacing is clearly smaller than the spacing between groups.
- [ ] Spacing uses `gap` and logical properties.
- [ ] The scale is defined once and documented next to the other tokens.
