**Verdict:** approve with nits. I read the diff and the surrounding `fmideas.py`, `fmcore.py` and `test_ideas.py` code. I did not run the tests.

## intent: ok
- LOW — `plugin/lib/fmhooks.py:471,474`. The note tells the model to run `fm mission --request '<their words>'` in single quotes, but `SKILL.md` step 2 uses double quotes. Words like "don't" break the single-quoted form. Fix: use double quotes in the note and keep the two consistent. Confidence: medium.
- The user asked Foreman to do this automatically. The hook only points at `fm mission`, and the model still has to run it. That fits Foreman's design, but it is not literally automatic. Not a defect.

## adversary: ok
- LOW — `plugin/lib/fmmission.py:220`. The file contents are passed through `c.redact` (lines 211–212), but `cmd_mission` prints `res["mission"]` and the `--json` result unredacted. A secret pasted into `--request` or a README therefore reaches stdout and the transcript. Fix: return the redacted text. Confidence: high.
- LOW — `plugin/lib/fmmission.py:112`. `pack_path` is interpolated unquoted into the `fm ideas` line. A state path with a space breaks the line. Fix: use `shlex.quote`. Confidence: medium.

## edge: ok
- MEDIUM — `plugin/lib/fmmission.py:112` with `plugin/lib/fmideas.py:222`. With every extra lens the line has 12 lenses, `--rounds 4` and `--deepen 3`, which is 12×4+3 = 51 child runs. `fmbudget.check` at `fmideas.py:224` could refuse the exact line the tool emits. Fix: print the estimated run count in the mission, or cap the lenses and rounds. I did not read the cap value, so I could not confirm it refuses. Confidence: low.
- LOW — `plugin/lib/fmmission.py:120,188`. The `git` calls have no timeout. Outside a git repo, `ls-files` returns empty and the project is reported as "library or CLI", which is acceptable.
- LOW — `plugin/lib/fmmission.py:199`. The timestamp has one-second resolution, so two runs in the same second overwrite each other's files. Minor.

## operator: ok
- `MASTER.md` and `CHANGELOG.md` are updated. The `HELP_TIERS` entry is added.
- The always-on rules file is untouched. The prompt-hook note is one line longer.
- The pre-audit item (`SKILL.md` versus `test_ideas.py`): `test_ideas.py` does not assert on `SKILL.md` or on `ideas-prompt.md` text. Its default-lens tests are unaffected because `DEFAULT_LENSES` did not change. No edit needed.

## maintainer: changes needed (small)
- MEDIUM — `plugin/lib/fmmission.py:120,188`. These are bare `subprocess.run(["git", ...])` calls, which duplicate `fmcore._git` (`plugin/lib/fmcore.py:~1498`). The same drift was flagged earlier for `fmmap`. Fix: reuse `c._git`. Confidence: medium.
- LOW — `plugin/lib/fmmission.py:209`. The mission file embeds the whole pack, and the pack is also written separately. The content is duplicated. Fix: keep a pointer to the pack file instead.
- LOW — `plugin/lib/fmmission.py:107-111`. The surface regexes can misfire. `.kt` or `.swift` (server code) counts as a mobile app, `.html` or `.css` in a docs folder counts as a web UI, and `.service` counts as a server. Nothing tests these false positives. Fix: require a manifest or directory signal as well, or add a test. Confidence: medium.
- LOW — `plugin/lib/fmideas.py:18`. `LENSES` is unused (only defined). It was already unused, and the new entries add to the dead list.
- Tests: `test_mission_composes_pack_pillars_and_lenses` and `test_open_ended_request_points_at_mission` both exercise real behaviour. The CLI-project test covers the negative case.

## Acceptance criteria
- `fm mission` writes the pack, the mission and the `fm ideas` line with project-specific lenses: met. The code does it (`fmmission.py:181-213`) and the test asserts it, though I did not run it.
- An open-ended or exhaustive prompt's note names `fm mission` first: met. `fmhooks.py:470-474` covers both branches, and the test checks both prompts.

## Not checked
I did not run the tests. I did not read the `fmbudget` cap values. I did not check `fmmap.compact` output size against the 1,200-word pack guidance.
