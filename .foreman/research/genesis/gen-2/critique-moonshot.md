# Critique — Mission 8, moonshot (gen 2, #8)

Tasks: T-2563 (done), T-2565 (deferred: the spike's real-session check). Mission: gen-2/mission-moonshot.md.

## Closed vs planned
- The one planned brief, the spike, is built. fmhooks.permission_request now records every prompt a person sees
  (one that fm approve-reads answered is left out) in a capped store, state/anergy.jsonl. post_tool_use closes an
  asked id with the tool's duration_ms. fmanergy.report pairs them offline. It names a class (a tool, or
  Bash(prog sub *) as an allow-rule pattern) that meets four conditions: 5+ timed prompts, a median within 2 s once
  the tool's own run time is taken out, every prompt read-only by fmguard.read_only, and no more than one prompt
  left open. fm doctor shows it as an advisory row, and fm digest adds a line when a class qualifies.
- Not built, as planned: auto-applying a rule (gen-0's NEVER), and T-2561 and T-2562 (held for the user).

## Outside signals
- None yet from real sessions. This session runs in bypass mode, so Claude Code shows it no permission prompts, and
  the store has no rows from a person. The spike's own check needs real prompts: the store should pair at least 90%
  of them, and the report should name a class or say none qualified. It is queued as T-2565, deferred to
  2026-12-01, to run once the store holds 20 or more prompts.
- The test suite drives the real hook functions end to end (permission_request, then post_tool_use with the same
  id) and fm digest through the CLI.

## What failed
- The draft's report would have named a class that people sometimes refuse. A refused prompt never reaches
  PostToolUse, so it only shows up as an untimed row, and the draft counted only timed rows. A refusal is the
  clearest sign that a prompt carries a decision. A class with two or more prompts that never ran (one may still be
  open) is now never named, and a test covers it.
- The Mission's doubt about a slow tool masking a reflex was answered by the payload, not by a reference set:
  PostToolUse carries duration_ms, and the report subtracts it.

## What the next Seed should change
- A moonshot whose evidence only real use can produce gets a deferred check task, with its threshold and revive
  date, filed when the build closes. It must not wait silently for data.
- A spike that reads how people behave says, in its Mission, which session modes it can observe: bypass mode shows
  no prompts.
