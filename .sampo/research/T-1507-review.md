**Verdict: changes needed.** The maths is sound. The problems are in extract's file handling, its speed on hostile input, and how a Tokens-only DESIGN.md interacts with the directions flow. I read the code only and could not run anything, so none of these findings has a reproducer I ran. I give the triggering input for each.

**Maths checked and found correct.** I checked these by hand against the published constants.
- The OKLab→LMS→linear-sRGB matrices (`fmdesign.py:706-710`) and the reverse matrices (`:726-731`) match Ottosson's.
- The sRGB transfer function and its thresholds (`:720`, `:725`) are right.
- The luminance coefficients are right. `_luminance` (`:775`) rounds to 8 bits exactly as `hex_of` does, so a proof is the ratio of the hex that ships.
- Chroma reduction in `_tok` (`:786-798`) stays in gamut after the floor.
- The WCAG contrast formula (`:780`) is right.
- The DTCG, CSS and Tailwind v4 exports are valid. Role names are fixed, and the seed only appears as a computed hex, so there is no quote or brace injection.

## lens: adversary
- MEDIUM — plugin/lib/fmdesign.py:891-893 — `_props` scans the whole block stack with `any(re.match…)` for every declaration, so a 1 MB file is quadratic. `":root{"*80000 + "--a:1;"*80000` is about 6e9 regex calls, so `fm design extract` hangs on a cloned repo. — cap the stack depth, or keep an incremental "inside a non-dark @media" flag — high
- MEDIUM — plugin/lib/fmdesign.py:620,1120,1154 — A DESIGN.md that isn't UTF-8 is decoded with `errors="replace"` and written back, so "other sections byte for byte" is false. A UTF-16 file (PowerShell `>`) or a Latin-1 file is rewritten as mojibake. CRLF files get LF-only lines mixed in. — in `write_section`, decode strictly and refuse non-UTF-8, and detect `\r\n` and keep it — high
- LOW — plugin/lib/fmdesign.py:1154 — `os.replace` swaps a symlinked DESIGN.md for a regular file, and the link target stays stale. — `os.path.realpath(out)` before writing — high
- LOW — plugin/lib/fmdesign.py:1117-1154 — Read-modify-write runs with no `fmcore.lock`. Two concurrent runs, or one racing a hand edit, lose an update. The write itself is atomic. — hold `fmcore.lock` around it — high
- LOW — plugin/lib/fmdesign.py:1081 — A path outside the DESIGN.md folder is written as an absolute path, which can put `/home/<user>/…` into a committed file. — redact or refuse — medium

## lens: edge
- MEDIUM — plugin/lib/fmdesign.py:891 — `stack[-1]` must match ROOTISH, so `:root { --bg:#fff; @media (prefers-color-scheme: dark){ --bg:#111 } }` is dropped. The dark value is lost silently, and contrast is proved for light only. — treat a dark @media nested in a root block as dark — high
- LOW — plugin/lib/fmdesign.py:893 — `!important` is not stripped (`Decl` does strip it). `--text:#fff !important` makes `fm design contrast` exit 2 with "can't read". — strip it — high
- LOW — plugin/lib/fmdesign.py:81-82,694 — Possessive quantifiers need Python 3.11 or later. The advertised "CI copies fmdesign.py" fails at import with `re.error` on 3.10 or older. — state the minimum Python version in the skill and playbook, or use atomic groups — high
- LOW — plugin/lib/fmdesign.py:874 — `html body .btn { --x:… }` and `[data-lang=html]` match ROOTISH, so component-scoped properties are recorded as global tokens. — anchor on the whole selector — medium
- LOW — plugin/lib/fmdesign.py:1034 — `extract` drops `collect`'s skipped list. Files over 1 MB, or beyond 5000 files, vanish with no word to the user. — report them — high

## lens: intent / operator
- MEDIUM — plugin/lib/fmdesign.py:1124 with plugin/lib/fmhooks.py:1856 and plugin/skills/directions/SKILL.md (step 1, "already has a DESIGN.md … wins … stop") — extract creates a title, "No direction recorded yet" and Tokens, and that is all. After it runs, `_design_note` never fires again, and directions step 1 treats the stub as an existing direction and stops. The design-extract skill's step 6 says the opposite. — define "has a direction" as having `## Direction`, and use that in the hook, the directions skill and the playbook — high
- LOW — plugin/skills/directions/SKILL.md (step 1, "replace the file") — A directions run replaces DESIGN.md wholesale and drops the extracted Tokens section. — say "keep Tokens or rerun extract" — high
- LOW — plugin/skills/playbooks/ratchet.json:73 — type-and-colour.md shrank by about 47 lines of script and its ceiling is stale, so it can regrow for free. — run `fm check playbooks ratchet` — medium
- LOW — CHANGELOG.md — No T-1507 entry. — add one — high

## lens: maintainer
- LOW — plugin/tests/test_docs.py:9-11 — `SKILLS` and `USER_ONLY` omit design-extract, so the frontmatter checks skip it. — add it to both — high
- LOW — plugin/tests/test_design_tokens.py:247 — The hostile test has no deep-nesting case. — add one (this is the finding above) — high

## Acceptance criteria
- **Palette: met by the tests, not run.** `Palette` checks the proofs, the 4.5 and 7 floors, and the DTCG, CSS and Tailwind exports. A margin caveat: each text role stops at the first 0.01 lightness step that passes, so ratios sit just above the floor. A browser using the CSS Color 4 matrices could shift one 8-bit channel and land at 4.49. I couldn't verify that. A small margin, for example a target of floor plus 0.03, would remove the risk.
- **Extract and contrast: met by the tests, not run.** The listed gaps above fall outside what the `Extract` tests cover.

## Implicit decisions
- The proof is on the hex, not the painted oklch.
- Gamut is clipped per channel, not CSS gamut-mapped.
- Dark means data-theme, `.dark`, or a `prefers-color-scheme: dark` block.
- The Tokens section owns everything up to the next `#` or `##` heading, including `###` content.
- Output is capped at 500 rows.
- Only five named colours are supported.

## Not checked
Browser rendering, the P3 case, the `fm code` skill listing, and the fixture files. I dismissed the pre-audit "secret" hit (it is the matrix constants) and the "oklch/resolve still named" hits.

**Noticed:** `fm design lint` shares `_blank` and `Source`. A string containing `{` skews its block stack the same way as in `_props`. That is worth a hostile-input test.
