**Verdict: approve with nits.** I read the code only and ran no tests; this session had no execution tool. The rule is cheap and its fixtures match its intent. It is cascade-blind, though, and the file header promises "precision first", so a few false-positive classes need closing.

## lens: design

- MEDIUM — plugin/lib/fmdesign.py:595-622 — A transition on `*` (or `*, *::before`) never suppresses a finding. Neither does one on the parent of a nested `&:hover` block. For `.btn { transition: color .2s; &:hover { color: red } }`, `base("&:hover")` is `"&"`, which is not in `moves`. `lint` also exits 1 on any finding (line 1319), so these false positives fail the command. Fix: if `"*"` is in `moves`, skip; skip selectors whose base is `&` or starts with `&`. Confidence: high.
- MEDIUM — plugin/lib/fmdesign.py:21-23, 65 — The message doesn't say why the rule fired. `color changes on .btn:hover with no transition` leaves out that matching is by base selector text (`.btn`) and that a transition on `button`, `*` or a parent class doesn't count. A person with a shared-class transition can't see why it fired. The silence route (`design-lint: allow afterglow <why>`) works, but it sits on the declaration's line or the line above. Fix: use the message `... no transition on selector '.btn' found in this run (matched by selector text); add one, or silence with design-lint: allow afterglow <why>`, and add one clause to NOT_COVERED. Confidence: high.
- LOW — plugin/lib/fmdesign.py:603-605 — The "no transition" test looks only at the first token of the value. These count as a transition: `transition: all 0s`, `color 0s`, `0.0s`, bare `0`, and the list `0s, 0s`. `transition-delay`, `transition-timing-function`, `animation-fill-mode` and `animation-play-state` alone also count. `none`, `0s`, `0ms`, `transition-duration: 0s` and `animation: none` do work, and `!important` is stripped. Fix: skip a decl when all its time tokens parse through `_seconds` to 0, and restrict the prefixes to `transition`, `transition-property`, `transition-duration`, `animation` and `animation-name`. Confidence: medium.
- LOW — plugin/lib/fmdesign.py:61-63 — The exemption regex also matches `prefers-reduced-motion: no-preference`. A hover change in that block is skipped even though it is the motion-enabled path. Fix: require `reduce` in the pattern. Confidence: high.
- LOW — plugin/lib/fmdesign.py:49,56 — `[aria-current]`, `[aria-hidden]` and `.is-*` are often set once at page load and never change at runtime. An example is site/style.css:137 `.side a[aria-current="page"]`. It escapes only because `.side a` happens to have a transition. Expect false positives on static state. The message-clarity fix above covers this, and `allow` is the escape.
- LOW — plugin/lib/fmdesign.py:50 — `BY_ID ={...}` lost its space. It is an accidental edit, so restore `BY_ID = {`.
- LOW — plugin/lib/fmdesign.py:65 — Each property is flagged separately, so a hover block that sets both `color` and `background` gives two findings. Fix: report one finding per block.

The selector extraction is sound for plain CSS: comments are blanked at line 137, so the `/* expect */` fixtures work. The other gaps are `:not(:hover)` (matched as state) and `.nav:hover a` (the base is `.nav a`, so a transition on `a` doesn't match). Both are false-positive classes, covered by the same "heuristic" caveat.

**Tests.** plugin/tests/test_motion_verify.py doesn't cover `transition: none`, `0s`, `*`, a selector group, or nesting. In slop.css:7 the `.menu { transition: none }` base is `.menu`, so it never tests the `none` path. Add 3-4 fixture lines for these.

**site/style.css.** The additions at lines 68, 92, 211 and 240 are 150 ms, limited to color, background and opacity, and match the existing easing. They are tasteful and short. They don't need to join the reduced-motion block at line 202, because colour and opacity fades aren't vestibular motion. Adding `transition: none` there is optional. There is no other copy of style.css to keep in sync.

**Default set or advisory.** Keep it in the default set, but only once the `*` and `&` false positives are closed. There is no advisory mode today; `lint` exits 1 on any finding, so a noisy rule would block. If the false-positive fixes don't land, make it opt-in.

## Acceptance criteria
The brief gave me no explicit list. Judged against the task title (a state change with no transition, as a rule in `fm design lint`):
- The rule exists, is registered and has a flag message: met.
- `transition: none` and 0s count as no transition: met for the first-token forms, with the gaps above.
- Reduced-motion exemption: met, with the `no-preference` flaw.
- Fixtures flag and clean cases (slop.css expects lines 2, 4, 5, 6; crafted.css expects none): consistent by reading.

## Implicit decisions
- Matching is by selector text and ignores the cascade.
- Any transition or animation on the element counts, whichever property it covers.
- Five properties are watched: color, background, background-color, transform, opacity.
- JS/JSX sources are skipped.
- Lint exit status is 1 on a finding.

## Not checked
- I ran no tests; the new unit test and the existing test_design_lint.py were not run.
- I looked at no screenshots.
- I did not verify that CHANGELOG.md's line format or the 311 KB size is acceptable.

Noticed: plugin/lib/fmdesign.py has no Tailwind `hover:` or CSS-in-JS coverage for afterglow, and NOT_COVERED doesn't say so; worth its own task.
