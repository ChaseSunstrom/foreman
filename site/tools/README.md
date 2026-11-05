# site/tools

The one-time port of design direction 12, the illustrated forge (T-2788, ported by T-2851), into the landing site.
Kept as the record of how the site's look was made (T-2904). The direction's own source is in
`design/site/12-forge-illustrated/` (its page, notes and `_src` generator).

- `port.py`: turned direction 12's page into `site/index.html`, `site/forge.css`, `site/forge.js` and the `art` and
  easing groups in `design/sampo/tokens.json`. It ran from a builder's worktree root with its inputs in `.fm-scratch/`:
  `src.html` (12's page), `src.js` (12's script), `old_index.html` (the landing before the port) and `port_css.py`
  (the CSS transform: 12's stylesheet split into fonts, root tokens, body rules and the forge's extra rules).
- `annotate.py`: after the port, added one inline design-lint allow per line of `site/forge.css` that is 12's own art
  timing.
- `writeif.py`: both write an output only when its content changes, so a rerun leaves no churn.

Missing: `port_css.py` went with the builder's worktree and is not in git, so `port.py` does not run as kept. To port
again, rebuild that transform from `port.py`'s use of `port_css.css_part(extra)` (it returns `fonts`, `root`, `body` and
`extra` strings) and the direction's `_src/page.html`, or port by hand from `design/site/12-forge-illustrated/index.html`.
