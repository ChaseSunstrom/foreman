**Verdict: changes needed.** The core works, but the note's "logs keep it redacted" claim is false on one path, and the report-and-file flow puts the task in the wrong project.

I did not run the tests. I read the code at the paths below.

## lens: adversary
- HIGH — ~/.claude/foreman/plugin/lib/fmcore.py:2415 — `add_veto` stores `said` from the raw prompt without `redact`. The hook calls it at fmhooks.py:1082 for any message starting "never", "don't" or "stop". The prompt `never use [REDACTED] again` therefore writes the key into vetoes.json. That contradicts the note's "logs keep it redacted". The Trust test uses a non-correction prompt, so it misses this. — Fix: `redact(...)` inside `add_veto`, and add a test with a "never …" prompt. — high
- MEDIUM — ~/.claude/foreman/plugin/lib/fmdoctor.py:1992 (the `report_wrong` task capture) — The FIX task goes to `c.find_project(os.getcwd())`, but the case goes to Foreman's corpus (`fmreplay.cases_path`, the plugin checkout). Run from another project, that project gets a task saying "correct fmguard.py", which is out of its scope. The case stores an absolute cwd, and writes into `PLUGIN_ROOT` (possibly a plugin cache). `fm guard wrong` shares the corpus and cwd behaviour. — Fix: file the task in `c.find_project(fmreplay._corpus_root())`, as `fmreplay.record` does, and say which corpus was written. — high
- LOW — ~/.claude/foreman/plugin/lib/fmhooks.py:1135 — The note scans `text`, which has `<pasted_content>` blocks stripped (line 1064). The one-off path at line 1061 scans the raw prompt. A pasted block is the likeliest place for a secret. — Fix: use `pl.get("prompt")` in both. — medium

## lens: edge
- MEDIUM — fmhooks.py:1137 and 1217 — The note is about 225 characters (about 245 with two kinds) in a 400-character cap. After "Foreman: " and one or two approval notes, the tail ("rotate it…") is cut. When the cap does bite, the intake, "Urgent: fm checkpoint", override and "Next:" parts are cut. `_same_note` already recorded that state as shown, so it is not repeated next turn. — Fix: shorten the note to about 90 characters, e.g. "Pasted secret (an API key or token): don't repeat or store it; suggest rotating it". — medium
- MEDIUM — fmcore.py:861 — False positives: `token = [REDACTED] and `secret: [REDACTED] (4 or more non-space characters) trigger, and so does `token: [REDACTED] `password: see 1Password` does not (3 characters). Because the note is long and crowds the cap, a false positive costs state output. — Fix: shorter note (above). — high
- LOW — fmcli.py:3094 — `ask_tally` has one slot per project. Two sessions on one project reset each other's count, so A, B, A, B never reaches 3. The model cannot forge `sid`, since it comes from the hook record. — Fix: key counts by session id and keep the last few. — medium
- LOW — fmdoctor.py:1980 — When `drift` returns "unable" (the guard raised), the output says "the guard refuses/allows it today". — Fix: word the "unable" case separately. — medium

## lens: maintainer
- LOW — fmcore.py:866 — `zip` silently truncates if `_SECRET_RES` and `_SECRET_KINDS` drift apart. They are aligned today (6 patterns, 6 names, same order). — Fix: add `assert len(_SECRET_KINDS) == len(_SECRET_RES)`. — high
- LOW — test_guard_hardening.py:1986 — The `--wrong` test depends on the guard blocking `rm -rf ~/.cache/thumbnails`. The intended fix (loosening it) would break the test. — Fix: use a command that is meant to be blocked. — medium
- LOW — fmcli.py:3107 — The fatigue note tells the model how to ask for a wider grant (`--standing`, "covers all the remaining work"). — Fix: add "only for work already in the plan". — low

## Acceptance criteria
- Key-shaped secret gets one note and is never echoed: **partly met**. The note contains only kind names. The secret reaches vetoes.json on the correction path (HIGH finding above).
- Repeated same-category asks give a fatigue note: **met**. Counts are per session, fire from the 3rd ask, and are not decremented on grant, which is right because the count measures asks.
- `fm doctor --wrong` files a labelled case: **met**. It refuses key-shaped literals, deduplicates on `[guard-case ID]` (the same marker `fm replay --cases --capture` uses), and never changes the guard. The allow-label task warns against loosening without the user's yes. The wrong-project placement is the MEDIUM finding.
- The Claude Code doctor skill step: **met**, one line. Only the skill points to it; no guard message does.

## Implicit decisions
- The note is a plain string appended to the hook's context.
- Fatigue threshold is 3.
- The tally lives in meta.json.
- A duplicate case returns the stored one and drops the new `why`.
- Corpus location comes from the cwd's checkout, else `PLUGIN_ROOT`.

## Not checked
I did not run the tests, and the UI files in the diff (fmcodetui.py, site/) are not part of T-1606. The diff baseline bc1b48 also contains other tasks' work: fsck, img, motion, playbooks, and the `plain()` change in fmcore.py:2256.

**Noticed:** none
