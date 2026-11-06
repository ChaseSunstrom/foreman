**Verdict:** changes needed. I could only read the code, not run it, so every finding below is a code trace and none was executed. Four fixes should land before merge: findings 1 and 2, the "0 files is clean" case (finding 6), and either finding 3 or an explicit doc of its limits. Findings 4 and 5 come second.

## lens: adversary (paths)
- MEDIUM — fmdesign.py:383-398 — `files()` trusts `getsize`, then `lint()` calls `fh.read()` with no limit. A symlink `x.css -> /dev/zero` (or a FIFO) reports size 0, passes the 1 MB cap, and the read never ends. An unreadable file raises `PermissionError`, whose traceback exits 1, the same code as "findings". — fix: require `os.path.isfile(f)`, read `fh.read(MAX_BYTES+1)`, and catch `OSError` per file. — high
- LOW — fmdesign.py:369-391 — paths are not deduplicated. `fm design lint a.css a.css` (or `site site/style.css`) doubles every decl, so three `border-radius: 8px` become six and trigger one-radius. Findings also print twice. — fix: dedupe by `realpath`. — high
- LOW — fmdesign.py:39 — `SKIP_DIRS` omits `build`, `venv`, `out`, `target`, `bower_components`, and there is no cap on file count. — fix: extend the set. — medium

## lens: edge (real-world forms and false positives)
- MEDIUM — fmdesign.py:59,145 — `[^;{}]*` cuts a value at `{`. Five styled-components lines `border-radius: ${t.radii.sm};` / `${t.radii.lg}` all become `"$"` and are flagged "one-radius on all 5 uses". SCSS `#{$r}` becomes `"#"` and Svelte `{r}px` becomes `""`, with the same result. — fix: mark a value dynamic when the cut lands on `{`, and skip dynamic values in the equality rules. — high
- MEDIUM — fmdesign.py:265-269 — flags any identical radius used 5 or more times, including `50%`, `999px` and `2px`. design-direction.md "Defaults to avoid" #4 says 8–12 px, and its premium row sanctions 0–4 px. Five `border-radius: 2px` rules (or five `50%`) are flagged. — fix: fire only for values in about 6–16 px or the matching rem range, and ignore circles and pills. — high
- MEDIUM — fmdesign.py:230,265,271 — Tailwind and Next forms are not read. `rounded-lg` everywhere, `shadow-md` everywhere, `font-sans`, `next/font` `Inter(...)` and a Google Fonts `<link family=Inter>` all pass. Gradients are skipped in `.css` (`@apply from-purple-500 to-blue-500`) and in oklch colours, which Tailwind v4 uses by default. The gradient check runs per line, so `cn("from-purple-500","to-blue-500")` split over two lines is missed. — fix: add class-token counting for `rounded-*` and `shadow-*`, scan `@apply`, and say in the help text what is not covered. — high
- LOW — fmdesign.py:59 — the lookbehind drops SCSS `$var:` declarations. `$f: Inter, sans-serif; body{font-family:$f}` gives the stack `"$f"`, which is not generic, so generic-font silently passes. `$grad` gradients are missed too. — fix: resolve `$name` as `_resolve` does for `var()`. — high
- MEDIUM — fmdesign.py:76-79 — `//` comments are not blanked in `.scss`, `.jsx` or `.tsx`. `// transition: height .3s;` raises layout-animation, and `// never Math.random()` raises unseeded-random. A `// useReducedMotion` comment also turns off reduced-motion for the whole run (line 215). — fix: blank `//` to end of line when it follows start-of-line or whitespace. — high
- MEDIUM — fmdesign.py:342-346 — Math.random is flagged anywhere in jsx, tsx, vue, svelte or html. `const id = Math.random().toString(36)` in an onClick handler, a useEffect, or an html `<script>` is flagged, though the rule says "rendering code". — fix: restrict to calls inside JSX braces or a style template, or drop it for html and for handlers. — medium
- LOW — fmdesign.py:46,197 — `transition: all .3s` passes both motion rules, and `font-size` and `box-shadow` are not in `LAYOUT_PROPS`. motion.md:162 lists all three as fails. — fix: flag `all` under layout-animation or document the gap. — medium
- LOW — fmdesign.py:50,336 — any opacity or colour keyframes at more than 3 Hz are flagged, whatever the area or luminance change. `.dot{animation:dot .3s infinite}` with `50%{opacity:.4}` fires. The longhand `animation-duration` is ignored. — fix: require the keyframes to reach opacity 0 or a colour change, or note the limit. — medium
- LOW — fmdesign.py:303 — img-alt flags `aria-hidden="true"`, `role="presentation"`, `aria-label` and Angular `[alt]="x"`. — fix: accept those attributes. — high
- LOW — fmdesign.py:190 — `_family` counts hue 300 as purple. A hue slider `linear-gradient(#00f,#f0f)` is flagged. — fix: use `< 300` or accept it, since an allow comment exists. — medium

## lens: operator
- LOW — fmdesign.py:419-426 — a path with no UI files prints "clean (0 file(s))" and exits 0. `fm design lint plugin/lib/fmcli.py` does this. — fix: exit 2 with "no UI files under …" when `n == 0`. — high
- LOW — fmdesign.py:99-102 — a same-line allow comment also silences the next line. In `<img src=a.png> <!-- design-lint: allow img-alt why -->` followed by a bare `<img src=b.png>`, the second image is silenced. — fix: extend to the next line only when the comment stands alone on its line. — high

## Acceptance criteria
- Rules fixtures: met by reading. I traced the flash, generic-font and tailwind fixtures and the expected-line logic. Not executed.
- Site clean: not verifiable here. `site/index.html` images have `alt=""`, and no allow comments were added.

## Implicit decisions
- Findings are whole-run (fonts, radius, shadow, reduced-motion, tokens), so linting one component gives false positives.
- Explicit file arguments bypass the `.min.` filter.
- Only gradients are covered for Tailwind.
- `fmcli` imports `fmdesign` eagerly at parser build for the help epilog.

## Not checked
Test execution, the Site test, git diff of unrelated files.

Noticed: none
