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
}
export type FmPlan = { interpretation: string; approach: string; steps: FmStep[]; criteria: FmCriterion[] }
export type FmActive = FmItem & {
  stage: string
  stages: string[]
  steps: FmStep[]
  criteria: FmCriterion[]
  audits: { done: number; need: number }
  blockers: string[]
}
export type FmApproval = { task: string; allow: string[]; why: string }
export type FmView = {
  v: number
  project: string | null
  root?: string
  mode?: { autonomy: string; drive: boolean; sensitive: boolean }
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
}

// What one turn did, for the line that closes it (matched by its duration).
export type TurnSummary = { durationMs: number; tools: number; edits: number; add: number; del: number; agents: number; step: string }

declare module 'claude-code' {
  interface PluginState {
    'foreman-ui': { view: FmView | null; error: string | null; frame: number; summaries: TurnSummary[] }
  }
}
