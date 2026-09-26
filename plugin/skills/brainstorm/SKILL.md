---
name: brainstorm
description: Use when a request is open-ended with no concrete target ("just get it done", "super improve it", "make it better", "what should we build next?", "brainstorm features") or the Foreman prompt note says so. Builds one context pack, fans out tool-less fm-ideas subagents with different lenses, grounds and scores their ideas against the real code, and turns the best into ordered Foreman briefs.
---

# Foreman: brainstorm

Open-ended requests get ideas from several independent angles before any planning, so the work isn't limited to whatever comes to mind first. State changes go through `fm`.

1. **Classify and capture.** Say "Treating this as open-ended: brainstorming first." `fm capture "<verbatim request>" --type RESEARCH --tier M`, then `fm focus` it.
2. **Context pack** (main thread, ≤ 1,200 words, pasted into every brainstorm brief; the brainstormers have no tools):
   the user's words verbatim and any CONTEXT/MUST/NEVER lines · what the project is (README's first paragraphs) · stack and entry points · top-level tree (depth 2, trimmed) · last 10 commits · test/build status (run them) · open Foreman queue and inbox titles (`fm state`) · known limitations, TODO/FIXME counts, recent failures (`fm log`/ledger) · constraints (budget, what must not change).
3. **Fan out** one `foreman:fm-ideas` subagent per lens, ≤ 3 at a time, at least four lenses:
   `user value` (what users would notice) · `reliability` (bugs, failure modes, robustness) · `performance` · `security and safety` · `simplicity` (delete, consolidate, test gaps) · `bold bets` (ambitious, high-upside).
   Brief: "Lens: <lens>. Context pack: <pack>. Return 5–8 ideas." Pick the lenses that fit the project; say which you skipped.
4. **Merge and ground.** Dedupe across lenses. For each idea, check the premise against the real code and tests (grep, read, run): already done → drop; premise false → drop or fix; unclear → note it. Brainstormers never saw the code, so nothing goes forward ungrounded.
5. **Score** each surviving idea: value 1–5, effort S/M/L, risk low/med/high, confidence. Slate = the best value-for-effort set that fits the request (default ≤ 8 items, at most one L); security findings and baseline-breaking bugs go first.
6. **Record.** `fm research add brainstorm-<date>` with every idea, its lens, grounding result and score. Turn the slate into briefs with one `fm intake` block (tags, `CONTEXT:` lines from the pack); the rest go to the inbox (`fm capture --source followup`).
7. **Autonomy.** Standard: show the slate in ≤ 15 lines (item · why · effort) and ask one yes/no for the whole slate. Full (`fm autonomy` says full): record the choice with `fm decide` and start the queue (`/foreman:next`).
8. Close the brainstorm task with a `self` audit (`fm task audit ID self …`) and `fm task done`.
