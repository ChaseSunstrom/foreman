**Verdict:** approve with nits. I found no HIGH issues and did not run the tests. I traced each `AUDIT_LENSES` consumer by reading the code.

## lens: intent
- No findings. Both acceptance criteria are covered by code and tests.

## lens: adversary
- LOW — `plugin/lib/fmcli.py:4534-4538` — The screenshot scan covers the whole brief: preamble, raw request and evidence output. It accepts absolute, `~` and `..` paths, so any existing `.png/.jpg/.webp` outside the repo, such as `~/.ssh/x.png`, is listed for the reviewer to Read. Outside-repo paths are a real use case (`shot.py snap OUT.png` writes anywhere), so I wouldn't restrict to the repo. The reviewer is read-only with no network, so the exposure is small. — Fix: skip paths under dot-directories (`~/.ssh`, `.gnupg`, `.config`) and keep the cap of 8. — plausible
- No path for task text to spawn the design reviewer. In `plugin/lib/fmauditrun.py:56`, the `=== review (...) ===` header is the first match in the brief.
  - For M/L tasks the header is line 1.
  - For S tasks only the self block precedes it. Its content is `- `-prefixed lines or static text, so it can't start with `=== review (`.
  - Passing `--lens design` by hand is the user's own act.

## lens: edge
- LOW — `plugin/lib/fmlanes.py:467` (same pattern at `plugin/lib/fmcli.py:4343`) — `_LENS_HEAD` is built from `AUDIT_LENSES`, so adding `design` changes it with no edit to that line. A reply heading like `## Design notes` or `## Design-system` now matches (`(?i)`, `\b` after "design"), even when no design lens ran. After that heading, `reviewer_findings` files later findings under lens `design`, and `fmhooks.py:3613` logs them that way. `## Design notes` did not match before. The `^## design\b` section extraction in `_past_findings` takes in the same headings. Reproduce with `reviewer_findings("## maintainer\n- LOW — a.py:1 — x\n## Design notes\n- LOW — b.py:2 — y")`. The second finding gets lens `design`. — Fix: anchor the match as `\b(?=\s*(?::|$))` so only `## design` or `## design: ok|changes needed` count. — confirmed by reading the code

## lens: operator
- LOW — `plugin/lib/fmcore.py:1095` — The comment names `fmdesign.ui_paths`, which doesn't exist. The function is `fmcore.ui_paths`. — Fix: correct the name. — confirmed
- LOW — `CHANGELOG.md` — The diff has no entry. Recent tasks (T-1499, T-1561) each added one, and the pre-audit flagged it. — Fix: add a line under the top section. — confirmed

## lens: maintainer
- MEDIUM — `plugin/lib/fmcore.py:3322-3331` — `ui_paths` is too broad. It has no skip for generated or vendored files. `fmdesign.py:49-50,630` skips `node_modules`, `vendor`, `dist`, `build`, `out`, `target`, `venv` and `.min.`. A diff touching `dist/app.css`, `vendor/x.html` or a coverage `.html` gets the design lens. Its extension set also drifts from `fmdesign.EXTS` (`:46`). Reproduce with `c.ui_paths(["dist/app.css","node_modules/x/a.html"])`, which returns both. — Fix: share `fmdesign.SKIP_DIRS` and the `.min.` rule, or add them to `_NOT_UI`. — confirmed
- LOW — `plugin/lib/fmcli.py:4534` — The loop variable `m` shadows the `fmmap` map `m` from `:4487`. Nothing reads it afterwards, but the shadowing is fragile. — Fix: rename it to `mt`. — confirmed

## Answers to the key questions
- **`AUDIT_LENSES` consumers:** `design` is not in `REQUIRED_AUDITS`, so the done gate is unchanged. The `--lens` validation (`fmcli.py:497,581,939,5621`) and `add_audit` accept `design`, which is intended. `test_docs:87` and `test_cli:945` are satisfied by the new `**design**` template, which `_LENS_TPL` matches. `fmcode.py:1961` uses fixed keys and is untouched. `fm audit run` previously defaulted to all lenses except `self`, and now uses `DEFAULT_LENSES` plus `design` only for a UI brief.
- **Backend-only diff:** it never gets or pays for the design lens. `fmcli.py:4493` adds it only when `ui_paths` is non-empty. An explicit `--lens` suppresses it, because `or` binds looser than `+`.
- **`ui_paths` scope:** Foreman's own UI files count: `mods/foreman-ui/hooks/{state,kit}.ts`, `register.tsx`, `rows.tsx`, and `fmcodetui.py`. `plugin/templates/brief.md`, `intuition.py`, tests and `hooks.json` are excluded. The narrow gap is `plugin/hooks/statusline`, which has no extension and isn't caught.

## Acceptance criteria
- Reviewer prompt, template and `audit prep` naming the design lens for a UI diff: met. The persona text is in `fm-reviewer.md` and `audit.md`, and `test_audit.DesignLens` covers it.
- `fm audit run` runs the design reviewer only when the brief has the design section: met. `fmauditrun.py:56-58` checks the header, and the tests cover both the UI and non-UI cases.

## Implicit decisions
- The design lens is advisory, so no tier requires it.
- At most 8 screenshots, and only files that exist.
- `ui[:20]` in the brief.
- `.jinja` counts as UI but `.j2` doesn't.
- `.html` anywhere counts as UI.

## Not checked
- I did not run the tests.
- I did not check how a real `claude -p` handles image Reads.
- I did not check doctor's size limit on `fm-reviewer.md`.
- The site and stats data were not reviewed.

**Noticed:** `plugin/hooks/statusline` (no extension) is Foreman's own UI but is never detected as a UI file. `_LENS_HEAD` could be anchored for all lenses; `## Edge cases` has the same misparse today.
