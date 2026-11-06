T-2388 review (coordinator, main thread: the pace gate held fm-reviewer subagents).
HIGH fixed: the signal's environment kept every ANTHROPIC_*/CLAUDE_* variable even when it was a credential (ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN reached an arbitrary command): all credential-matching variables stripped (subTests red first).
Checked: the signal runs through c.guard_stored, 120 s, from the repo root; backticks refused; 126/127 and timeouts read broken.
Open (builder): a second fm incident with the same signal opens a duplicate; fm task set ID incident_signal= clears the gate; safe_gaps fails open like fmmiss; 'green twice' counts finish's own run.
