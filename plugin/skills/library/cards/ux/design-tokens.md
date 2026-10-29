---
name: design-tokens
title: Design Tokens
area: ux
tags: [ux, tokens, design-system, css-variables, style-dictionary]
detect: [dep:style-dictionary, dep:@tokens-studio/sd-transforms, file:tokens.json]
related: [design-systems, css-custom-properties, color-palettes, spacing-scales, design-handoff, dark-mode]
---
One JSON source of truth for color, space, type, radius and motion, in three tiers, compiled to CSS and native.

## Verify
- `npx style-dictionary build`: compiles tokens; a broken alias reference fails the build.
- `grep -rnE "#[0-9a-fA-F]{3,8}\b|[0-9]+px" src --include=*.css --include=*.tsx | grep -v "tokens"`: raw values outside the token source.
- `git diff --exit-code dist/tokens.css`: generated output is committed and current.

## Test first
Every alias resolves and every semantic token has a dark value.
```python
import json

def flat(d, p=""):
    for k, v in d.items():
        if isinstance(v, dict) and "value" not in v and "$value" not in v:
            yield from flat(v, f"{p}{k}.")
        else:
            yield p + k, v.get("$value", v.get("value"))

def test_aliases_resolve():
    t = dict(flat(json.load(open("tokens/tokens.json"))))
    for name, val in t.items():
        if isinstance(val, str) and val.startswith("{"):
            assert val[1:-1] in t, f"{name} -> {val}"
```

## Do
- Three tiers: primitive (`blue.500 = oklch(55% .2 260)`), semantic (`color.action = {blue.500}`), component (`button.bg = {color.action}`).
- Name by role and not by value: `color.text.muted`, not `gray-600` in components.
- Follow the W3C Design Tokens format (`$value`, `$type`, `$description`) so tools interoperate.
- Generate CSS custom properties on `:root`, with dark and brand themes as `[data-theme]` overrides of the semantic tier only.
- Cover: color, space (4px scale), font size, line-height, radius, shadow, z-index, duration, easing, breakpoint.
- Version tokens with semver; a rename is a breaking change and gets a deprecation alias for one release.
- Run the build in CI and fail on a diff.

## Avoid
- Components reading primitives directly: a re-brand then touches every file.
- Hand-edited generated CSS.
- Tokens for one-off values; a token used once is a literal with extra steps.
- Names that encode the value (`--space-16`) when the scale may change; use `--space-4`.

## Review
- [ ] Source is one file set; CSS and other outputs are generated from it.
- [ ] No raw hex or px outside the token source and generated files.
- [ ] Themes override only the semantic tier.
- [ ] Renames ship with a deprecation alias and a changelog note.
