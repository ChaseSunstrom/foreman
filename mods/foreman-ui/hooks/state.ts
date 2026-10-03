import type { RenderInput } from 'claude-code'

// T-0130: what the hooks, the rows and the pane share: constants, two timing maps and the settings. Atoms stay
// in register.tsx: the engine reads an atom only where it is declared.

export type ToolUseRender = RenderInput<'ToolUse'>

export const PANE = 'foreman'

export const LIST = 6
export const OUT_LINES = 12 // a finished command's row: this many output lines (failures first, else the tail)
export const DIFF_LINES = 8 // a finished edit's row: this many changed lines
export const FRAME_MS = 120
export const IDLE_FRAMES = Math.round((15 * 60 * 1000) / FRAME_MS) // a lost turn.complete stops the clock after 15 min
export const QUIET_MS = 2 * 60 * 1000 // a running subagent with no tool call this long shows how long it has been quiet
export const STOP_MS = 10 * 60 * 1000 // and from here offers Stop
export const SHELL_MAX_MS = 2 * 3600 * 1000 // a background command runs at most 2 h; past that its notice was lost
export const CHECKPOINT_AT = 85 // context percent at which Foreman checkpoints once, so a compaction resumes exactly
export const FRESH = [
  'Foreman task boundary: a task just closed.',
  "Keep: the user's standing requests and preferences, decisions still in force, and what the next queued task needs.",
  "Drop: finished tasks' file contents, diffs, logs and back-and-forth.",
  "Foreman's record (fm state, the briefs) is the source of truth for tasks: after this, check `fm next` and re-read",
  'files before editing them, since what was read earlier may be out of date.',
].join(' ')

/** What changed between two snapshots that deserves a toast. */

export const starts = new Map<string, number>() // tool_use_id → when it started (ms)
export const took = new Map<string, number>() // tool_use_id → how long it ran (ms), for the finished row

/** userConfig and the session's folder, set by register (rows read them). */
export const cfg = { freshAt: 40, mascot: 'blue', root: '' }
