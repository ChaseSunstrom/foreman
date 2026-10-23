# DESIGN.md: design-surfaces fixture

## Knobs

Colour: one cool blue accent on near-black.

## Tokens

Written by `fm design extract ui` from the CSS custom properties set in :root, html, :host and @theme (dark: a .dark, [data-theme] or prefers-color-scheme: dark block, or light-dark()) and tailwind.config colours. Rerun it after a token change; it rewrites this section only.

| Token | Kind | Light | Dark | Source |
|---|---|---|---|---|
| `--n-18` | colour | `oklch(0.18 0.010 250)` #0E1216 |  | ui/tokens.css:3 |
| `--surface` | colour | `#f2f5f9` #F2F5F9 | `var(--n-18)` #0E1216 | ui/tokens.css:5 |
| `--surface-raised` | colour | `#fafcfe` #FAFCFE | `#171b1f` #171B1F | ui/tokens.css:6 |
| `--surface-sunken` | colour | `#e4e8ed` #E4E8ED | `#22272c` #22272C | ui/tokens.css:7 |
| `--text` | colour | `#171b1f` #171B1F | `#e4e8ed` #E4E8ED | ui/tokens.css:8 |
| `--text-muted` | colour | `#4f565e` #4F565E | `#8c939b` #8C939B | ui/tokens.css:9 |
| `--border` | colour | `#6b727b` #6B727B |  | ui/tokens.css:10 |
| `--accent` | colour | `#21539c` #21539C | `#83adea` #83ADEA | ui/tokens.css:11 |
| `--on-accent` | colour | `#ffffff` #FFFFFF | `#0e1216` #0E1216 | ui/tokens.css:12 |
| `--accent-subtle` | colour | `#e6effc` #E6EFFC | `#1a2e4c` #1A2E4C | ui/tokens.css:13 |
| `--success` | colour | `#1f7a3d` #1F7A3D | `#6fcf8e` #6FCF8E | ui/tokens.css:14 |
| `--danger` | colour | `#b02b27` #B02B27 | `#ff8a80` #FF8A80 | ui/tokens.css:15 |
| `--warning` | colour | `#8a5a00` #8A5A00 | `#f5c04a` #F5C04A | ui/tokens.css:16 |
| `--font-body` | font | `"Source Sans 3", system-ui, sans-serif` |  | ui/tokens.css:18 |
| `--step-0` | length | `1rem` |  | ui/tokens.css:19 |
| `--odd` | other | `a \| b 'c'` |  | ui/tokens.css:20 |
| `--sneaky` | other | `red; } body { color: red` |  | ui/tokens.css:21 |

Contrast (WCAG 2.x, on the sRGB hex the browser paints):

- `text` on `surface`: 16.29:1 light, 14.95:1 dark (needs 4.5)

## Later

| `--not-a-token` | colour | `#ff0000` #FF0000 |  | elsewhere |
