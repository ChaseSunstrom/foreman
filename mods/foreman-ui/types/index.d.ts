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
  children?: { id: string; title: string; status: string; steps_done: number; steps_total: number }[] // T-0711
  on_task_s?: number | null // seconds since the task was first focused, when the view was built
  hypotheses?: FmHypothesis[] // T-0207/T-0228: the debugging ledger
  oracle?: { examples: number; ambiguities: string[] } | null // T-0226: examples from the spec alone
  batch?: string[] // T-0257: the requests this task works as one batch
  inconclusive?: number // T-0255: runs recorded as proving nothing (never counted)
  unverified?: string[] // T-0254: assumptions not tagged [verified: …], the first five
}
export type FmHypothesis = { n: number; status: 'open' | 'ruled out' | 'confirmed'; text: string }
// T-0228: what fm budget, fm bench/evolve and fm research ask add
export type FmBudget = {
  today_usd: number
  subagent_tokens: number
  caps: { day: number; run: number }
  halved: string | null
  subagents_paused?: string | null // T-0320: why subagents wait (usage ahead of pace)
  top: { feature: string; usd: number; runs: number; tokens: number }[]
}
export type FmBench = {
  cases: number
  last: { label: string; passed: number; total: number; cost_usd: number; at?: string | null; score?: number; repeats?: number } | null
  evolve: { kept: boolean | null; branch: string | null; target: string | null; why: string | null; at?: string }[]
  verdicts?: { kind: string; ok: boolean | null; verdict: string | null; at?: string }[] // T-0280: fm bench duel / versions
}
export type FmResearchAsk = { name: string; claims: number; verified: number; not_found: number; unchecked: number; at?: string; conflicts?: number; single?: number }
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
  closed?: { id: string; status: string; title?: string; grade?: string | null; lenses?: string[] }[] // T-0473
  signals?: { level: 'red' | 'amber'; text: string }[] // T-0472: shown as one glyph only when any
  // T-0711: live sessions here and the cached tiles of remotes the user added (fm conductor remote add)
  fleet?: { session: string; project?: string | null; task?: string | null; title?: string | null; context_pct?: number | null
    mail?: number; leases?: number; remote?: string; age_s?: number | null; error?: string }[]
  recent?: string[]
  health?: { hook_p95_ms: number | null; guard_blocks: number; hook_errors: number; paused_hooks?: string[] }
  watch?: string[] // paths whose mtime moves when the record changes
  latency?: number[] // the latest hook run times (ms), oldest first
  checks?: FmChecks | null // the last fm check run
  today_done?: number // tasks closed as done today
  brainstorm?: FmBrainstorm | null // the newest brainstorm (T-0124)
  budget?: FmBudget | null // T-0228: today's spend on child runs and subagents
  bench?: FmBench | null // T-0228: bench cases, the newest run, evolve generations
  research?: FmResearchAsk[] // T-0228: the newest fm research ask notes
  revisit?: { date: string; decision: string; why: string }[] // T-0247: decisions whose revisit trigger fired
  vetoes?: string[] // T-0251: the user's recorded 'never/don't' corrections, newest first (checked before matching calls)
  trust_file?: string // where /fm-trust on writes the trust record (Foreman state)
  /** T-0145: a driven turn ended so this session's mod could reload; the reloaded mod starts the next turn */
  resume_after_reload?: { session: string; at: string; task?: string } | null
  typical?: Record<string, number> // median minutes focus → done per "TYPE/TIER" (3+ closed tasks)
}
// A brainstorm while fm ideas runs (answers in of expected) or after (count, the first ideas).
export type FmBrainstorm = { name: string; running: boolean; answers: number; expected?: number; count: number; ideas: string[]; age_h?: number; grounded?: boolean }
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
      resumed: string | null // the resume record (its `at`) this session already acted on
    }
  }
}
