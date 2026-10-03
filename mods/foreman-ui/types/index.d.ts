// The `fm ui --json` view model (v1): one snapshot of a Foreman project, rendered by every surface.
export type FmStep = { n: number; text: string; done: boolean; current: boolean }
export type FmCriterion = { n: number; text: string; verify: string | null; checked: boolean }
export type FmItem = {
  id: string
  type: string
  tier: string
  title: string
  status: string
  waits?: string | null // why it can't run without the user ("plan approval", "pending approval")
  plan?: FmPlan // only while waits is "plan approval": what a yes approves
  steps_done?: number
  steps_total?: number
  age_days?: number
}
export type FmPlan = { interpretation: string; approach: string; steps: FmStep[]; criteria: FmCriterion[] }
export type FmActive = FmItem & {
  stage: string
  stages: string[]
  steps: FmStep[]
  criteria: FmCriterion[]
  audits: { done: number; need: number }
  blockers: string[]
  on_task_s?: number | null // seconds since the task was first focused, when the view was built
}
export type FmApproval = { task: string; allow: string[]; why: string }
export type FmView = {
  v: number
  project: string | null
  root?: string
  mode?: { autonomy: string; drive: boolean; sensitive: boolean; trust?: boolean; standing?: string[] }
  active?: FmActive | null
  next?: string | null
  queue?: FmItem[]
  inbox?: FmItem[]
  inbox_total?: number
  approvals?: FmApproval[]
  closed?: { id: string; status: string }[]
  recent?: string[]
  health?: { hook_p95_ms: number | null; guard_blocks: number; hook_errors: number }
  watch?: string[] // paths whose mtime moves when the record changes
  latency?: number[] // the latest hook run times (ms), oldest first
  checks?: FmChecks | null // the last fm check run
  today_done?: number // tasks closed as done today
  trust_file?: string // where /fm-trust on writes the trust record (Foreman state)
  typical?: Record<string, number> // median minutes focus → done per "TYPE/TIER" (3+ closed tasks)
}
export type FmCheck = { cmd: string; exit: number; s: number; note?: string | null }
export type FmChecks = { at: string; results: FmCheck[] }

// Live data the mod gathers itself from the session's tool calls.
export type FileChurn = { path: string; add: number; del: number; edits: number }
export type LiveAgent = {
  id: string
  type: string
  description: string
  startedAt: number
  lastAt?: number // its latest tool call
  tools: number
  last: string
  done: boolean
}
// A background shell Claude started (or ctrl+b moved there), until its notification or a stop.
export type LiveShell = { id: string; command: string; startedAt: number }
export type Ctx = { percent: number }

// What one turn did, for the line that closes it (matched by its duration).
export type TurnSummary = { durationMs: number; tools: number; edits: number; add: number; del: number; agents: number; step: string }

declare module 'claude-code' {
  interface PluginState {
    'foreman-ui': {
      view: FmView | null
      error: string | null
      frame: number
      summaries: TurnSummary[]
      files: FileChurn[]
      agents: LiveAgent[]
      ctx: Ctx | null
      sound: boolean
      beat: number
      shells: LiveShell[]
      away: string[]
    }
  }
}
