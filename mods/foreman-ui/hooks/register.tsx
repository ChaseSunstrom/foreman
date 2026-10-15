import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, RenderInput, ResolveInput } from 'claude-code'


import type { FileChurn, FmItem, FmView, LiveAgent, LiveShell, TurnSummary } from '../types'
import {
  C,
  MASCOT_COLORS,
  about,
  hoursAgo,
  tokensWord,
  activityCells,
  bucketize,
  agentColor,
  TONE_COLOR,
  changedLines,
  replyBlocks,
  clean,
  ago,
  churnCells,
  clawd,
  elapsed,
  fade,
  hex,
  humanNext,
  miniClawd,
  mix,
  outputSummary,
  progressCells,
  pulse,
  shortPath,
  sizeWord,
  sparkCells,
  sparkText,
  spin,
  textBar,
  textComet,
  tone,
  toolFace,
  typeColor,
} from './kit'
import { CHECKPOINT_AT, FRAME_MS, FRESH, IDLE_FRAMES, LANES, LIST, PANE, QUIET_MS, SHELL_MAX_MS, STOP_MS, TIMELINE_MS, cfg, laneOf, running, starts, ticks, took } from './state'

const view = atom({ plugin: 'foreman-ui', key: 'view' } as const, null)
const error = atom({ plugin: 'foreman-ui', key: 'error' } as const, null)
const frame = atom({ plugin: 'foreman-ui', key: 'frame' } as const, 0)
const summaries = atom({ plugin: 'foreman-ui', key: 'summaries' } as const, [])
const files = atom({ plugin: 'foreman-ui', key: 'files' } as const, [])
const agents = atom({ plugin: 'foreman-ui', key: 'agents' } as const, [])
const ctx = atom({ plugin: 'foreman-ui', key: 'ctx' } as const, null)
const sound = atom({ plugin: 'foreman-ui', key: 'sound' } as const, true)
const beat = atom({ plugin: 'foreman-ui', key: 'beat' } as const, 0)
const shells = atom({ plugin: 'foreman-ui', key: 'shells' } as const, [])
const away = atom({ plugin: 'foreman-ui', key: 'away' } as const, []) // tasks done since the person last wrote
const resumed = atom({ plugin: 'foreman-ui', key: 'resumed' } as const, null) // T-0145: the resume record acted on
import { agentOut, agentRow, bars, churn, editChanges, editRow, eta, lanes, mascotTree, meter, miniRail, more, rail, shellRow, spark } from './rows'
import type { Motion } from './rows'

// Foreman inside Claude Code. A pure renderer over `fm ui --json` plus what the session's own tool calls show it:
// every rule and gate stays in fm and its classic hooks (which still run under claude -p and older builds); buttons
// only run fm commands or submit a prompt the person pressed for. While work is live a frame clock animates the band,
// the cards and every running tool row; a finished row goes back to the engine, which draws its result as always.
export function toasts(prev: FmView | null, next: FmView): string[] {
  if (!prev?.project || prev.project !== next.project) return []
  const out: string[] = []
  const a = prev.active
  const b = next.active
  if (a && b && a.id === b.id) {
    const was = a.steps.filter(s => s.done).length
    const now = b.steps.filter(s => s.done).length
    if (now > was) {
      const last = b.steps.filter(s => s.done).at(-1)
      out.push(`✓ ${b.id} step ${now}/${b.steps.length}${last ? ` · ${last.text}` : ''}`)
    }
  }
  // Only a task that was open in the last snapshot closed just now (an old closed one edited again is no news).
  const open = new Set([a?.id, ...[...(prev.queue ?? []), ...(prev.inbox ?? [])].map(x => x.id)])
  for (const c of next.closed ?? []) {
    if (open.has(c.id)) out.push(c.status === 'done' ? `✔ ${c.id} done${closeCard(c)}` : `${c.id} ${c.status}`)
  }
  const asked = new Set((prev.approvals ?? []).map(x => `${x.task}:${x.allow.join(',')}`))
  for (const x of next.approvals ?? []) {
    if (!asked.has(`${x.task}:${x.allow.join(',')}`)) out.push(`⚠ ${x.task} needs your yes: ${x.allow.join(', ')}`)
  }
  return out
}

/** T-0473: a close-out's facts after "done": its grade and the lenses it closed with. */
export function closeCard(c: { grade?: string | null; lenses?: string[] }): string {
  const parts = [c.grade, (c.lenses ?? []).join(', ')].filter(Boolean)
  return parts.length ? ` · ${parts.join(' · ')}` : ''
}

/** T-0472: the band's one glyph: the worst signal (red before amber) and how many more, or null when calm. */
export function signalLine(v: FmView | null): { level: 'red' | 'amber'; text: string } | null {
  const sig = v?.signals ?? []
  const worst = sig.find(x => x.level === 'red') ?? sig[0]
  if (!worst) return null
  return { level: worst.level, text: worst.text + (sig.length > 1 ? ` +${sig.length - 1}` : '') }
}

/** The guard's refusal text, when a tool call was refused by Foreman. */
export function guardReason(r: { deny?: string; isError?: true; text?: string }): string | undefined {
  const why = r.deny ?? (r.isError ? r.text : undefined)
  const m = why?.match(/^(?:\S+ hook error: )?Foreman(?: guard)?:\s*([\s\S]*)/) // a refusal leads with it, output never
  return m ? m[1]!.slice(0, 120) : undefined
}

/** The closing line's extra: what the turn did. */
export function summaryText(s: TurnSummary): string {
  const parts = [`${s.tools} tool${s.tools === 1 ? '' : 's'}`]
  if (s.edits) parts.push(`${s.edits} edit${s.edits === 1 ? '' : 's'} +${s.add} −${s.del}`)
  if (s.agents) parts.push(`${s.agents} subagent${s.agents === 1 ? '' : 's'}`)
  if (s.step) parts.push(`✓ ${s.step}`)
  return parts.join(' · ')
}

/** A plain Foreman bookkeeping command (`fm …`, maybe after a `cd`): its row folds to one line once it succeeds.
 * Anything chained, piped, substituted or on a second line keeps the full row, so the fold never hides what ran. */
export function fmCommand(command: unknown): string | null {
  if (typeof command !== 'string') return null
  const m = /^(?:cd\s+[^\s;&|`$<>]+\s*&&\s*)?fm\s+([^;&|`$<>\n\r]+)$/.exec(command.trim())
  return m && m[1]!.length <= 160 ? m[1]!.replace(/\s+/g, ' ') : null
}

/** A Foreman permission request (`fm ask ID cats --why "…"`), in plain words for a note under its dialog. */
export function askNote(command: unknown): string | null {
  if (typeof command !== 'string') return null
  // the reason may hold no quote, $, backtick, backslash or newline: then the whole command is the one ask shown
  const m = /^fm\s+ask\s+(T-\d{4,})\s+([\w\s-]+?)\s+(?:--pin\s+[\w@.:/-]+\s+)?--why\s+(?:"([^"$`\\\n]*)"|'([^'\n]*)')$/.exec(
    command.trim(),
  )
  const why = m ? (m[3] ?? m[4] ?? '') : ''
  if (!m || why.length > 160) return null // too long to show whole: no summary rather than a cut one
  return `⚠ Foreman asks: a yes grants ${m[2]!.trim().split(/\s+/).join(' + ')} for ${m[1]} — ${why.replace(/\s+/g, ' ')}`
}

/** One line for a finished read: how much it read. */
export function readSummary(tool: string, output: unknown): string {
  const o = (output && typeof output === 'object' ? output : {}) as { file?: { numLines?: number; totalLines?: number } }
  if (tool === 'Read' && typeof o.file?.numLines === 'number') {
    const total = o.file.totalLines
    return total && total > o.file.numLines ? `${o.file.numLines} of ${total} lines` : `${o.file.numLines} lines`
  }
  return ''
}

/** The last meaningful line a command printed. */
export function lastLine(output: unknown): string {
  const o = (output && typeof output === 'object' ? output : {}) as { stdout?: unknown; stderr?: unknown }
  const text = [o.stdout, o.stderr].filter(x => typeof x === 'string').join('\n')
  return (text.split('\n').map(l => clean(l).trim()).filter(Boolean).at(-1) ?? '').slice(0, 100)
}

/** Whether something waits on the person: a yes, or a plan to approve. */
const waiting = (v: FmView | null) =>
  !!v && ((v.approvals ?? []).length > 0 || (v.queue ?? []).some(q => q.waits === 'plan approval'))

// Module variables start over on a reload; what a drawing reads lives in $.state.
let fmPath: string | null = null
let marks = ''
let isDirty = true
let isBusy = false
let lastFull = 0
let poll: { cancel: () => void } | null = null
let clock: { cancel: () => void } | null = null
let lastActive = 0 // the frame of the last turn or tool activity
let checkpointed = false
let economyOn = false
let happyUntil = 0 // the mascot jumps for a few seconds after a task closes
let bgLive = 0 // background shells still running: the clock keeps a calm pace for the waiting row
let calm = 0
const turns = new Set<string>()
const agentCalls = new Map<string, string>() // running Agent call → its description
const agentOf = new Map<string, string>() // running Agent call → the subagent's id
let turn = { tools: 0, edits: 0, add: 0, del: 0, agents: 0, stepsDone: -1, task: '' }
let turnStartedAt = 0 // the working line's clock (T-0143)
const seenReplies = new Set<string>() // reply texts drawn during a turn; the newest one's mark animates
let newestReply = ''
const DOING: Record<string, string> = { requesting: 'thinking', thinking: 'thinking', responding: 'writing', 'tool-input': 'preparing a tool call', 'tool-use': 'running tools' }

async function fm($: EngineInterface): Promise<string> {
  if (fmPath) return fmPath
  const given = await $.env.get('FOREMAN_FM')
  const home = (await $.env.get('CLAUDE_CONFIG_DIR')) ?? `${(await $.env.get('HOME')) ?? ''}/.claude`
  const installed = `${home}/foreman/plugin/bin/fm`
  fmPath = given ?? ((await $.fs.exists(installed).catch(() => false)) ? installed : 'fm')
  return fmPath
}

async function run($: EngineInterface, args: string[]) {
  return $.process.run([await fm($), ...args], { timeoutMs: 15000 })
}

async function chime($: EngineInterface, name: 'done' | 'needs') {
  if (await read($, sound)) await $.audio.play({ asset: `sounds/${name}.wav` }).catch(() => undefined)
}

async function refresh($: EngineInterface): Promise<boolean> {
  if (isBusy) {
    isDirty = true
    return false
  }
  isBusy = true
  isDirty = false
  try {
    const r = await run($, ['ui', '--json'])
    if (r.exitCode !== 0) throw new Error(r.stderr.trim().split('\n').at(-1) || `fm ui exited ${r.exitCode}`)
    const next = JSON.parse(r.stdout) as FmView
    const prev = await read($, view)
    const was = prev?.active
    const now = next.active
    if (cfg.motion !== 'off' && was && now && was.id === now.id) { // a glow needs the clock to fade
      const t = await $.clock.now()
      for (const s of now.steps)
        if (s.done && !was.steps.find(x => x.n === s.n)?.done) {
          for (const [k, at] of flashed) if (t - at > FLASH_MS) flashed.delete(k)
          flashed.set(`${now.id}:${s.n}`, t)
          flashUntil = t + FLASH_MS
        }
      if (flashUntil > t) await wake($)
    }
    const lines = toasts(prev, next)
    for (const line of lines) $.ui.toast(line)
    if (lines.some(l => l.startsWith('⚠'))) await chime($, 'needs')
    else if (lines.some(l => l.startsWith('✔'))) await chime($, 'done')
    const closed = lines.map(l => /^✔ (T-\d+) done/.exec(l)?.[1]).filter((x): x is string => !!x)
    if (closed.length) await update($, away, list => [...list, ...closed.filter(x => !list.includes(x))])
    if (lines.some(l => l.startsWith('✔'))) {
      happyUntil = (await $.clock.now()) + 6000
      $.clock.after(500, () => void freshen($)) // outside this dispatch
    }
    await update($, view, () => next)
    await update($, error, () => null)
    lastFull = await $.clock.now()
    return true
  } catch (err) {
    await update($, error, () => String(err instanceof Error ? err.message : err).slice(0, 200))
    return false
  } finally {
    isBusy = false
  }
}

// Cheap in-process checks every 2 s: the context meter, and the paths fm names (fm runs only when one moved).
async function tick($: EngineInterface) {
  await gauge($).catch(() => undefined)
  if (cfg.mascot !== 'off') await update($, beat, n => n + 1) // the mascot's idle blink, at the poll's pace
  if ((await read($, shells)).length) await noteShells($, list => list) // ages out lost ones; a reload re-arms bgLive
  const running = (await read($, agents)).filter(a => !a.done)
  const listed = running.length ? await $.agent.list().catch(() => null) : null
  if (listed) {
    // T-0121: one that ended without its turn.complete (killed, a compaction, a reload) is no longer running in the
    // engine's own list, or not in it at all: it ends here instead of reading as running for hours
    const live = new Set(listed.filter(a => a.status === 'running').map(a => a.id))
    if (running.some(a => !live.has(a.id))) await update($, agents, list => list.map(a => (live.has(a.id) ? a : { ...a, done: true })))
  }
  const v = await read($, view)
  const stamps = await Promise.all(
    (v?.watch ?? []).map(p => $.fs.stat(p).then(s => `${s.mtimeMs}:${s.size}`, () => '-')),
  )
  const now = await $.clock.now()
  const moved = stamps.join('|') !== marks
  marks = stamps.join('|')
  if (isDirty || moved || now - lastFull > 30000) await refresh($)
}

// The context meter; at CHECKPOINT_AT% Foreman checkpoints the active task once, so a compaction loses nothing.
async function gauge($: EngineInterface) {
  const u = await $.session.usage().catch(() => null)
  const eco = economyText(u?.rateLimits ?? [])
  if (eco && !economyOn) $.ui.toast('Usage is high · Foreman economy mode: leaner work until the window resets', { timeoutMs: 10000 })
  economyOn = !!eco
  const percent = u?.context.percent
  if (typeof percent !== 'number') return
  const prev = await read($, ctx)
  if (!prev || Math.round(prev.percent) !== Math.round(percent)) await update($, ctx, () => ({ percent }))
  if (percent < 60) checkpointed = false // a /compact brought it down: the next climb checkpoints again
  if (percent >= CHECKPOINT_AT && !checkpointed && (await read($, view))?.active) {
    checkpointed = true
    const r = await run($, ['checkpoint']).catch(err => ({ exitCode: 1, stderr: String(err), stdout: '' }))
    if (r.exitCode !== 0) checkpointed = false // try again on the next poll
    $.ui.toast(
      r.exitCode === 0
        ? `Context ${Math.round(percent)}% · Foreman checkpointed: /compact resumes at this exact step`
        : `Context ${Math.round(percent)}% · checkpoint failed: ${lastLine({ stderr: r.stderr })}`,
      { timeoutMs: 10000 },
    )
  }
}

// T-0198: the person is usage-sensitive; past these shares of a usage window Claude works leaner until it resets.
const ECONOMY: Record<string, [number, string]> = { seven_day: [80, 'weekly'], five_hour: [90, '5-hour'] }

// The economy section, or null: it names the threshold, not the live figure, so the prompt (and its cache) changes
// only when a window crosses it.
function economyText(limits: readonly { kind: string; percentUsed: number }[]): string | null {
  const hot = limits.filter(l => ECONOMY[l.kind] && l.percentUsed >= ECONOMY[l.kind][0])
  if (!hot.length) return null
  const what = hot.map(l => `${ECONOMY[l.kind][1]} usage is past ${ECONOMY[l.kind][0]}%`).join(' and ')
  return (
    `# Foreman economy mode\nThis account's ${what}. Work leaner until it resets: no brainstorms or multi-round ` +
    `fm ideas, at most one combined reviewer pass per task (none for S), no other subagents unless the task can't ` +
    `go on without one, targeted reads (grep, fm outline, line ranges), fm check --affected while iterating, short ` +
    `replies. Correctness, evidence and the guard's rules don't change.`
  )
}

// A task just closed: with the context past freshAt percent or freshTokens tokens, compact so the next task starts on
// what still matters (T-0098). Every turn re-reads the whole context, so tokens, not a share of a 1M window, set the
// cost (T-0703).
async function freshen($: EngineInterface) {
  if (!cfg.freshAt && !cfg.freshTokens) return
  const context = (await $.session.usage().catch(() => null))?.context
  const percent = context?.percent, tokens = context?.tokens
  const byPct = !!cfg.freshAt && typeof percent === 'number' && percent >= cfg.freshAt
  const byTokens = !!cfg.freshTokens && typeof tokens === 'number' && tokens >= cfg.freshTokens
  if (!byPct && !byTokens) return
  const at = typeof tokens === 'number' ? `${Math.round(tokens / 1000)}k tokens` : `${Math.round(percent ?? 0)}%`
  $.ui.toast(`Task closed at context ${at} · compacting so the next task starts fresh`, { timeoutMs: 8000 })
  await $.session.compact({ instructions: FRESH }).catch(() => undefined)
}

async function act($: EngineInterface, args: string[], done: string) {
  const r = await run($, args)
  $.ui.toast(r.exitCode === 0 ? done : `fm ${args[0]}: ${(r.stderr || r.stdout).trim().split('\n').at(-1)}`)
  await refresh($)
}

async function capture($: EngineInterface, text: string) {
  const idea = text.trim()
  if (!idea) return
  const r = await run($, ['capture', idea])
  const id = /T-\d{4,}/.exec(r.stdout)?.[0]
  $.ui.toast(r.exitCode === 0 ? `⚑ Captured ${id ?? ''} — ${idea.slice(0, 60)}` : `fm capture: ${lastLine({ stderr: r.stderr })}`)
  await refresh($)
}

// T-0711: one steer for every live session here and on the remotes the user added (fm conductor steer)
async function steer($: EngineInterface, text: string) {
  const said = text.trim()
  if (!said) return
  const r = await run($, ['conductor', 'steer', said])
  $.ui.toast(r.exitCode === 0 ? `↯ ${lastLine({ stdout: r.stdout }) || 'Steer sent'}` : `fm conductor: ${lastLine({ stderr: r.stderr })}`)
  await refresh($)
}

async function openPane($: EngineInterface, focus: boolean) {
  // ~76 columns docked: the cards fit, and the transcript and band keep the rest (T-0122: the share left them ~37)
  return $.ui.open(focus ? { id: PANE, title: 'Foreman', focus: true, columns: 76 } : { id: PANE, title: 'Foreman', columns: 76 })
}

// T-0909: the pane's moving rasters (the rail's comet, the live lane's glow) repaint by blit at ~30 fps while work is
// live, without redrawing the pane; the pane registers them as it draws and the 8 fps frame clock keeps the rest.
const motion: Motion = new Map()
const MOTION_MS = 33
let motionClock: { cancel: () => void } | null = null
const frameAt = (ms: number) => ms / FRAME_MS // time in frames, fractional: what a comet takes
const LANE_COLOR: Record<string, number> = { edit: C.edit, run: C.accent, read: C.accent2, agent: C.agent, web: C.web }
// A step that just got done glows green and fades over FLASH_MS; the frame clock runs until it has
const flashed = new Map<string, number>() // "T-0007:2" → when it was seen done
const FLASH_MS = 2500
const BG = 0x181a21 // the terminal's background the glow fades into
let flashUntil = 0

let painting = false
async function repaint($: EngineInterface) {
  if (painting) return // a slow blit: skip a tick rather than pile them up
  if (!turns.size && !starts.size) {
    motionClock?.cancel() // live work ended: everything settles on the next redraw
    motionClock = null
    return
  }
  painting = true
  try {
    const f = frameAt(await $.clock.now())
    for (const [key, m] of [...motion]) {
      const r = await $.ui.blit({ requestId: PANE, key, columns: m.columns, rows: m.rows, cells: m.draw(f) }).catch(() => ({ deny: 'failed' }))
      if (r && 'deny' in r && r.deny) motion.delete(key) // not mounted (pane closed, redrawn smaller): until it draws again
    }
  } finally {
    painting = false
  }
}

// The frame clock runs only while work is live: a turn, or a tool call (a subagent's included).
async function wake($: EngineInterface) {
  lastActive = await read($, frame)
  if (cfg.motion === 'off') return // T-0912: a still UI; the 2 s poll still brings every change
  if (!motionClock && cfg.motion === 'full') motionClock = $.clock.every(MOTION_MS, () => void repaint($))
  if (clock) return
  clock = $.clock.every(FRAME_MS, () => void advance($))
}

async function advance($: EngineInterface) {
  const f = await read($, frame)
  if (starts.size) lastActive = f // a long build is live work: its row keeps moving (finally always clears starts)
  const quiet = !turns.size && !starts.size && (await $.clock.now()) >= flashUntil // a step's glow is still fading
  if (quiet && !bgLive && f - lastActive > 2) return sleep()
  if (!bgLive && f - lastActive > IDLE_FRAMES) return sleep()
  if (quiet && bgLive && ++calm % 4) return // only background work: a calmer pace (~2 frames a second)
  await update($, frame, n => n + 1)
}

function sleep() {
  clock?.cancel()
  clock = null
  motionClock?.cancel() // T-0909 review: a lost turn.complete must not leave the 30 fps blit running for good
  motionClock = null
}

// A subagent's tool calls carry its id: count them and tie the subagent to the Agent row that started it.
async function noteSubagent($: EngineInterface, agentId: string, last: string) {
  const known = (await read($, agents)).find(a => a.id === agentId)
  const lastAt = await $.clock.now()
  if (known) {
    await update($, agents, list => list.map(a => (a.id === agentId ? { ...a, tools: a.tools + 1, last, lastAt } : a)))
    return
  }
  const info = (await $.agent.list()).find(a => a.id === agentId)
  const call = [...agentCalls].find(([id, d]) => d === info?.description && !agentOf.has(id))
  if (call) agentOf.set(call[0], agentId)
  const fresh: LiveAgent = {
    id: agentId,
    type: info?.type ?? 'subagent',
    description: info?.description ?? '',
    startedAt: lastAt,
    lastAt,
    tools: 1,
    last,
    done: false,
  }
  await update($, agents, list => [...list.filter(a => !a.done).concat(list.filter(a => a.done).slice(-3)), fresh])
}

// Background shells: a Bash call that came back with a task id (run_in_background, ctrl+b, or its timeout) is running
// until its notification arrives, TaskStop stops it, or it is older than any background command may run.
async function noteShells($: EngineInterface, fn: (list: LiveShell[]) => LiveShell[]) {
  const now = await $.clock.now()
  await update($, shells, list => fn(list).filter(x => now - x.startedAt < SHELL_MAX_MS))
  bgLive = (await read($, shells)).length
  if (bgLive) await wake($)
}

/** The pane's Stop on a subagent that has gone quiet: the same TaskStop Claude would call. */
async function stopAgent($: EngineInterface, id: string) {
  await $.tool.call({ tool: 'TaskStop', task_id: id }).catch(() => undefined)
  await update($, agents, list => list.map(a => (a.id === id ? { ...a, done: true } : a)))
}

async function noteEdit($: EngineInterface, path: string, add: number, del: number) {
  await update($, files, list => {
    const was = list.find(f => f.path === path)
    const row: FileChurn = { path, add: (was?.add ?? 0) + add, del: (was?.del ?? 0) + del, edits: (was?.edits ?? 0) + 1 }
    return [...list.filter(f => f.path !== path), row].slice(-12)
  })
}

/** T-0145: Claude Code hot-reloads this mod only when a turn really ends, so a driven turn that changed it ends on
 * purpose and leaves a resume record; the reloaded mod (session.start runs again) starts the next turn itself, once
 * per record and only in the session the record names. */
async function resumeAfterReload($: EngineInterface) {
  const r = (await read($, view))?.resume_after_reload
  if (!r || r.at === (await read($, resumed)) || r.session !== (await $.session.id())) return
  await update($, resumed, () => r.at)
  $.ui.toast('Foreman UI reloaded · the drive continues', { timeoutMs: 6000 })
  void $.prompt.submit({ text: `Continue the Foreman drive: the Foreman UI reloaded${r.task ? ` (${r.task})` : ''}` })
}

/** The quick-capture box (every surface with text input). */
function captureBox($: EngineInterface, e: ResolveInput) {
  if (e.surface === 'mobile') return null
  const { Input } = $.ui.resolve(e)
  return (
    <Input key="capture" placeholder="⚑ capture an idea for later… (Enter)" submitLabel="Capture" onSubmit={text => void capture($, text)} />
  )
}

export const register: Register = (on, options) => {
  cfg.freshAt = typeof options.freshAt === 'number' ? options.freshAt : 40
  cfg.freshTokens = typeof options.freshTokens === 'number' ? options.freshTokens : 200000
  cfg.mascot = typeof options.mascot === 'string' && (options.mascot === 'off' || options.mascot in MASCOT_COLORS) ? options.mascot : 'blue'
  // T-0912: full = 30 fps charts by blit; calm = the 8 fps frame clock only; off = no clocks, a still pane
  cfg.motion = options.motion === 'calm' || options.motion === 'off' ? options.motion : 'full'
  on('session.start', async ($, e, next) => {
    cfg.root = typeof e.cwd === 'string' ? e.cwd : ''
    await $.command.register({ name: 'fm', description: 'Foreman: open or close the dashboard pane' })
    await $.command.register({
      name: 'fm-trust',
      description: 'Foreman: let Claude edit the guard and Claude Code settings (on | off); works only when you type it',
    })
    const stored = await $.store.get('sound').catch(() => undefined)
    if (stored === false) await update($, sound, () => false)
    await refresh($)
    await resumeAfterReload($)
    poll?.cancel() // one poller per environment, however often the session starts
    poll = $.clock.every(2000, () => void tick($))
    if ((await read($, view))?.project) void openPane($, false) // seats unasked only on a wide fullscreen terminal
    return next(e)
  })

  on('command.run', { command: 'fm' }, async $ => {
    const shown = (await $.ui.panes()).some(p => p.id === PANE && p.isShown)
    if (shown) {
      await $.ui.close({ id: PANE })
      return { text: 'Foreman pane closed.' }
    }
    await refresh($)
    const opened = await openPane($, true)
    return { text: opened.isPlaced ? 'Foreman pane opened.' : `Foreman pane: ${opened.reason}` }
  })

  // T-0120: only the person's own Enter (or their phone, via the bridge) turns trust on; a prompt the agent scheduled, a
  // skill call or another plugin's run is refused. On writes the record into Foreman state straight from here (no tool
  // call may write there, and fm has no "on"); fm trust then records it in the ledger, and off is fm's.
  on('command.run', { command: 'fm-trust' }, async ($, e) => {
    const kind = e.origin?.kind
    if (kind !== 'composer' && kind !== 'bridge') return { text: 'Foreman: /fm-trust works only when you type it.' }
    const arg = e.args.trim()
    if (arg === 'on') {
      const home = (await $.env.get('CLAUDE_CONFIG_DIR')) ?? `${(await $.env.get('HOME')) ?? ''}/.claude`
      const path = (await read($, view))?.trust_file ?? `${home}/foreman/state/trust.json`
      await $.fs.write(path, JSON.stringify({ on: true, at: new Date(await $.clock.now()).toISOString().slice(0, 19) + 'Z', via: kind }))
    }
    const r = await run($, ['trust', ...(arg === 'off' ? ['off'] : [])])
    isDirty = true
    await refresh($)
    return { text: `${r.stdout.trim() || r.stderr.trim()}`.split('\n').at(-1) ?? '' }
  })

  on('turn.start', async ($, e, next) => {
    if (!turns.size) turnStartedAt = await $.clock.now()
    turns.add(e.turnId)
    const a = (await read($, view))?.active
    turn = { tools: 0, edits: 0, add: 0, del: 0, agents: 0, stepsDone: a ? a.steps.filter(s => s.done).length : -1, task: a?.id ?? '' }
    await wake($)
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    turns.delete(e.turnId)
    isDirty = true
    await update($, frame, n => n + 1) // T-0182 live: a reply drawn live redraws settled (●, its resting border)
    if (e.agentId) await update($, agents, list => list.map(a => (a.id === e.agentId ? { ...a, done: true } : a)))
    else {
      const fresh = await refresh($)
      const v = await read($, view)
      const a = v?.active
      const now = a && a.id === turn.task ? a.steps.filter(s => s.done).length : -1
      const step = turn.stepsDone >= 0 && now > turn.stepsDone && a ? `${a.id} step ${now}/${a.steps.length}` : ''
      const s: TurnSummary = { durationMs: e.durationMs, tools: turn.tools, edits: turn.edits, add: turn.add, del: turn.del, agents: turn.agents, step }
      await update($, summaries, list => [...list, s].slice(-40))
      // Ghost text for the obvious next move; never a suggestion that would answer a question put to the person.
      if (fresh && !e.isAborted && v?.project && !waiting(v) && (a || (v.queue ?? []).length))
        await $.prompt.suggest({ text: '/foreman:next' }).catch(() => undefined)
    }
    return next(e)
  })

  on('tool.call', async ($, e, next) => {
    const id = e.tool_use_id
    let noteTimer: { cancel: () => void } | null = null
    const face = toolFace(String(e.tool), e, cfg.root)
    const at = await $.clock.now()
    starts.set(id, at)
    if (face.icon !== '⚠') ticks.push({ at, lane: laneOf(face.icon) }) // T-0909: the swim lanes (a question isn't work)
    while (ticks.length && (ticks.length > 2000 || at - ticks[0]!.at > 2 * TIMELINE_MS)) ticks.shift()
    running.set(id, { icon: face.icon, verb: face.verb, target: face.target, color: face.color, at, agent: !!e.agentId })
    try {
      if (face.icon === '◆') agentCalls.set(id, String((e as { description?: unknown }).description ?? ''))
      if (e.agentId) await noteSubagent($, e.agentId, `${face.verb} ${face.target}`.trim()).catch(() => undefined)
      else {
        turn.tools += 1
        if (face.add !== undefined) {
          turn.edits += 1
          turn.add += face.add
          turn.del += face.del ?? 0
        }
        if (face.icon === '◆') turn.agents += 1
      }
      await wake($)
      const note = e.tool === 'Bash' ? askNote(e.command) : null
      noteTimer = note ? $.clock.after(150, () => $.ui.notice(id, note)) : null // under the dialog, once it is open
      const r = await next(e)
      const why = guardReason(r)
      if (why) $.ui.toast(`⛔ Foreman: ${why}`, { timeoutMs: 8000 })
      else if (face.add !== undefined && r.deny === undefined && !r.isError) {
        const file = (e as { file_path?: unknown }).file_path // the real path; the files card shows it project-relative
        await noteEdit($, typeof file === 'string' ? file : face.target, face.add, face.del ?? 0)
      }
      const bg = (r.result as { backgroundTaskId?: unknown } | undefined)?.backgroundTaskId
      if (e.tool === 'Bash' && typeof bg === 'string' && !e.agentId) {
        const startedAt = await $.clock.now()
        const command = String(e.command).split('\n')[0]!.slice(0, 120)
        await noteShells($, list => [...list.filter(x => x.id !== bg), { id: bg, command, startedAt }])
      }
      const stopped = ['TaskStop', 'KillShell', 'KillBash'].includes(String(e.tool))
      if (stopped && r.deny === undefined && !r.isError) {
        const input = e as { task_id?: unknown; shell_id?: unknown }
        const gone = String(input.task_id ?? input.shell_id ?? '')
        await noteShells($, list => list.filter(x => x.id !== gone))
      }
      return r
    } finally {
      noteTimer?.cancel()
      const agent = agentOf.get(id)
      if (agent) await update($, agents, list => list.map(a => (a.id === agent ? { ...a, done: true } : a))).catch(() => undefined)
      const began = starts.get(id)
      if (began !== undefined) took.set(id, (await $.clock.now()) - began)
      if (took.size > 400) took.delete(took.keys().next().value!)
      starts.delete(id)
      running.delete(id)
      agentCalls.delete(id)
      agentOf.delete(id)
      isDirty = true
    }
  })

  // T-0137: Claude Code folds commands into one "Running 1 shell command…" line, which hid the live row; a group
  // holding a shell command unfolds, so each command is its own row here. Reads and searches stay folded.
  on('ui.render', { component: 'ToolGroup' }, async ($, e, next) => {
    if (e.props.isExpanded || !e.props.calls.some(x => x.tool === 'Bash')) return next(e)
    return next({ ...e, props: { ...e.props, isExpanded: true } })
  })

  // T-0198: economy mode, one session section after the engine's while a usage window is past its threshold.
  on('prompt.compose', async ($, e, next) => {
    const r = await next(e)
    const text = economyText((await $.session.usage().catch(() => null))?.rateLimits ?? [])
    return text ? { ...r, sections: [...r.sections, { id: 'foreman-ui:economy', text, scope: 'session' }] } : r
  })

  // A background task's notification (idle, or folded into a running turn) names the task that ended.
  on('prompt.submit', async ($, e, next) => {
    const kind = e.origin?.kind
    if ((kind === 'composer' || kind === 'bridge') && (await read($, away)).length) await update($, away, () => [])
    if (kind === 'task-notification') {
      const ended = new Set([...e.text.matchAll(/<task-id>([^<]+)<\/task-id>/g)].map(m => m[1]!.trim()))
      await noteShells($, list => list.filter(x => !ended.has(x.id)))
    }
    return next(e)
  })

  // While a tool runs: an animated row. A Foreman bookkeeping command that succeeded: one quiet line. Else the engine's.
  // T-0141: under an edit row that already shows its diff, the engine's own result block ('⎿ Added 2 lines' and the
  // whole hunk again, on red and green backgrounds) is blanked; an error still draws the engine's
  on('ui.render', { component: 'ToolResult' }, async ($, e, next) => {
    // T-0143: a shell row draws its output, file changes, commit and timeout itself; the engine's block repeated them
    const { Box } = $.ui.resolve(e)
    if (e.props.tool === 'Bash') return <Box key="fm-shell-result" />
    if (!e.props.isErrored && agentOut(e.props.tool, e.props.output)) return <Box key="fm-agent-result" /> // T-0148
    if (e.props.isErrored || !editChanges(e.props.tool, e.props.output)) return next(e)
    return <Box key="fm-edit-shown" />
  })
  on('ui.render', { component: 'ToolUse' }, async ($, e, next) => {
    const sub = e.props.tool === 'Bash' ? fmCommand((e.props.input as { command?: unknown } | null)?.command) : null
    if (sub && !e.props.isRunning && !e.props.isErrored && !e.props.isInterrupted) {
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box flexDirection="row" gap={1} key="fm-quiet">
          <Text color={hex(C.dim)}>⚙ fm {sub}</Text>
          <Text color={hex(mix(C.dim, C.ok, 0.6))} wrap="truncate-end">
            ✓ {lastLine(e.props.output)}
          </Text>
        </Box>
      )
    }
    if (e.props.tool === 'Bash' && !e.props.isRunning) return shellRow($.ui.resolve(e), e)
    const quiet = ['Read', 'WebFetch', 'WebSearch', 'Grep', 'Glob'].includes(e.props.tool)
    if (quiet && !e.props.isRunning && !e.props.isErrored && !e.props.isInterrupted) {
      const face = toolFace(e.props.tool, e.props.input, cfg.root)
      const { Box, Text } = $.ui.resolve(e)
      const more = readSummary(e.props.tool, e.props.output)
      return (
        <Box flexDirection="row" gap={1} key="fm-read">
          <Text color={hex(mix(face.color, C.dim, 0.4))}>{face.icon}</Text>
          <Text color={hex(C.dim)}>{face.verb.replace(/ing\b/, '')}</Text>
          <Text wrap="truncate-start">{face.target}</Text>
          {more ? <Text color={hex(C.dim)}>· {more}</Text> : null}
        </Box>
      )
    }
    const done = !e.props.isRunning && !e.props.isErrored && !e.props.isInterrupted
    const edited = done ? editRow($.ui.resolve(e), e) ?? agentRow($.ui.resolve(e), e) : null
    if (edited) return edited
    if (!e.props.isRunning || e.props.isErrored || e.props.isInterrupted) return next(e)
    const f = await read($, frame)
    const face = toolFace(e.props.tool, e.props.input, cfg.root)
    const since = starts.get(e.props.tool_use_id)
    const ms = since === undefined ? 0 : (await $.clock.now()) - since
    const agentId = agentOf.get(e.props.tool_use_id)
    const agent = agentId ? (await read($, agents)).find(a => a.id === agentId) : undefined
    const { Box, Text } = $.ui.resolve(e)
    const width = Math.max(30, e.viewport?.columns ?? 100)
    // T-0124: a brainstorm running inside this call shows its progress right here in the chat
    const ideasRun = e.props.tool === 'Bash' && /^ideas\b/.test(fmCommand((e.props.input as { command?: unknown } | null)?.command) ?? '')
    const bs = ideasRun ? (await read($, view))?.brainstorm : null

    // T-0179 steer ('the command changes … I want in panels too'): a command, an edit or an agent is a panel from the
    // start, its border pulsing while it runs; reads and searches stay one quiet line
    const boxed = /^(Bash|Edit|MultiEdit|Write|NotebookEdit|Task|Agent)$/.test(e.props.tool)
    const row = (
      <Box flexDirection="row" gap={1} key="fm-tool"
        {...(boxed ? { borderStyle: 'round', borderColor: hex(pulse(face.color, f)), paddingX: 1, width: '100%' } : {})}>
        <Text color={hex(face.color)}>{spin(f)}</Text>
        <Text bold color={hex(face.color)}>
          {face.icon} {face.verb}
        </Text>
        <Text wrap="truncate-end">{face.target.slice(0, Math.max(10, width - 48))}</Text>
        {face.delta && <Text color={hex(C.edit)}>{face.delta}</Text>}
        {agent && (
          <Text dimColor wrap="truncate-end">
            {agent.tools} tools · {agent.last.slice(0, 40)}
          </Text>
        )}
        {meter($.ui.resolve(e), e, 'fm-tool-bar', 12, null, face.color, f)}
        <Text dimColor>{elapsed(ms)}</Text>
      </Box>
    )
    if (!bs?.running) return row
    return (
      <Box flexDirection="column" key="fm-tool-ideas">
        {row}
        <Text color={hex(C.agent)} wrap="truncate-end">
          {'  '}✦ {bs.answers}/{bs.expected ?? '?'} answers · {bs.count} ideas so far{bs.ideas.length ? ` · ${bs.ideas.at(-1)}` : ''}
        </Text>
      </Box>
    )
  })

  // A background task's notification: one Foreman line (ctrl+o still shows the engine's full row).
  on('ui.render', { component: 'UserMessage' }, async ($, e, next) => {
    const origin = e.props.origin as { kind?: string; name?: string } | undefined
    const ours = /^The foreman-ui plugin sent a message:\n/ // how the model reads it; the row may carry that text
    if (((origin?.kind === 'plugin' && origin.name === 'foreman-ui') || ours.test(e.props.text)) && !e.props.isExpanded) {
      // T-0143 live: our own resume prompt drew as a four-line grey block; one quiet line says it
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box flexDirection="row" gap={1} key="fm-resumed">
          <Text color={hex(C.accent)}>↻</Text>
          <Text color={hex(C.dim)} wrap="truncate-end">
            {clean(e.props.text.replace(ours, '').split('\n')[0] ?? '')}
          </Text>
        </Box>
      )
    }
    // T-0182: 'my chats aren't [panelled] either': the person's own prompt is a panel in their colour
    if ((origin?.kind === 'composer' || origin?.kind === 'bridge') && e.props.text.length <= 9000 &&
        !/[\u0000-\u0008\u000b-\u001f\u007f]/.test(e.props.text)) {
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box flexDirection="row" borderStyle="round" borderColor={hex(C.accent2)} paddingX={1} width="100%" key="fm-user">
          <Text bold color={hex(C.accent2)}>
            {'❯ '}
          </Text>
          <Box flexDirection="column" flexShrink={1}>
            <Text wrap="wrap">{e.props.text}</Text>
          </Box>
        </Box>
      )
    }
    if (e.props.origin?.kind !== 'task-notification' || e.props.isExpanded) return next(e)
    const t = e.props.task ?? {}
    const status = t.status ?? 'completed'
    const color = status === 'completed' ? C.ok : status === 'failed' ? C.err : C.warn
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box flexDirection="row" gap={1} key="fm-note">
        <Text color={hex(color)}>{status === 'completed' ? '✓' : status === 'failed' ? '✗' : '■'}</Text>
        <Text color={hex(C.dim)}>background {t.type ?? 'task'} {status}</Text>
        <Text wrap="truncate-end">{e.props.text.split('\n')[0]}</Text>
        {t.durationMs ? <Text color={hex(C.dim)}>· {elapsed(t.durationMs)}</Text> : null}
      </Box>
    )
  })

  // T-0143: the working line is Foreman's ('get rid of … the "Seasoning" thing … and have it be a foreman thing'): an
  // animated mark, the task and step, what the turn is doing, how long it has run. The desktop keeps its own row.
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    if (e.surface !== 'terminal') return next(e)
    const a = (await read($, view))?.active
    const cur = a?.steps.find(s => s.current)
    const f = await read($, frame)
    const ms = turnStartedAt ? (await $.clock.now()) - turnStartedAt : 0
    const doing = e.props.message ?? DOING[e.props.mode] ?? 'working'
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box flexDirection="row" gap={1} key="fm-working">
        <Text color={hex(C.accent)}>{spin(f)}</Text>
        <Text bold color={hex(C.accent)}>
          {a ? a.id : 'Foreman'}
        </Text>
        {a && cur && (
          <Text wrap="truncate-end">
            <Text color={hex(C.dim)}>{`step ${a.steps.filter(s => s.done).length + 1}/${a.steps.length} `}</Text>
            {cur.text}
          </Text>
        )}
        <Text color={hex(C.dim)}>{`· ${doing} · ${elapsed(ms)}`}</Text>
      </Box>
    )
  })

  // T-0143: a reply opens with a Foreman mark (animated on the newest reply while the turn runs) and Foreman's report
  // lines (Changed:, ✓/✗, ⚑ Captured, ◆ Decided, Next:, ⚠ Needs you) are coloured like its rows; the rest stays the
  // engine's markdown ('just your normal text output looks weird with everything else').
  on('ui.render', { component: 'AssistantMessage' }, async ($, e, next) => {
    const text = e.props.text
    // a Markdown element takes ≤10000 characters, tab and newline its only controls: beyond that the engine's own draws
    if (e.surface !== 'terminal' || text.length > 9000 || /[\u0000-\u0008\u000b-\u001f\u007f]/.test(text)) return next(e)
    if (turns.size && e.props.isFirstOfReply && !seenReplies.has(text)) {
      if (seenReplies.size > 400) seenReplies.clear()
      seenReplies.add(text)
      newestReply = text
    }
    const live = turns.size > 0 && e.props.isFirstOfReply && text === newestReply
    const f = live ? await read($, frame) : 0
    const blocks = replyBlocks(text)
    // T-0179: each message is a panel ('can we have each message … look like a panel'): quiet grey, the closing report
    // (Foreman's Changed:/✓/✗/Next: lines) in the accent, pulsing while the reply is live
    const report = blocks.some(b => b.kind !== 'md' && b.kind !== 'gap')
    const border = live ? pulse(C.accent, f) : report ? C.accent : C.dim
    const { Box, Text, Markdown } = $.ui.resolve(e)
    return (
      <Box flexDirection="row" borderStyle="round" borderColor={hex(border)} paddingX={1} width="100%" key="fm-reply">
        {e.props.isFirstOfReply && (
          <Box key="fm-reply-mark">
            <Text color={hex(C.accent)}>{`${live ? spin(f) : '●'} `}</Text>
          </Box>
        )}
        <Box flexDirection="column" flexShrink={1}>
          {blocks.map((b, i) =>
            b.kind === 'gap' ? (
              <Box key={`gap-${i}`}>
                <Text> </Text>
              </Box>
            ) : b.kind === 'md' ? (
              <Markdown key={`md-${i}`} text={b.text} />
            ) : (
              <Text key={`ln-${i}`} wrap="wrap">
                {b.parts.map((p, j) => (
                  <Text key={j} bold={p.bold ?? false} {...(p.color !== undefined ? { color: hex(p.color) } : {})}>
                    {p.text}
                  </Text>
                ))}
              </Text>
            ),
          )}
        </Box>
      </Box>
    )
  })

  // The line closing a turn says what the turn did.
  on('ui.render', { component: 'TurnDuration' }, async ($, e, next) => {
    const s = (await read($, summaries)).find(x => x.durationMs === e.props.durationMs)
    if (!s || !s.tools) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box flexDirection="row" gap={1} key="fm-turn">
        <Text dimColor>✻ worked {elapsed(e.props.durationMs)}</Text>
        <Text color={hex(C.dim)}>· {summaryText(s)}</Text>
      </Box>
    )
  })

  // The footer: a pointer when something waits on the person (the band says the autonomy in words).
  on('ui.render', { component: 'PromptHint' }, async ($, e, next) => {
    const v = await read($, view)
    if (e.props.isDraft || !waiting(v)) return next(e)
    return next({ ...e, props: { ...e.props, tail: '⚠ Foreman needs you: /fm' } }) // the engine puts the separator before it
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const v = await read($, view)
    if (e.props.hasSurvey || !v?.project) return next(e)
    const a = v.active
    const asks = v.approvals ?? []
    const plans = (v.queue ?? []).filter(q => q.waits === 'plan approval')
    const bgs = await read($, shells)
    const doneSince = await read($, away)
    const paused = v.health?.paused_hooks ?? [] // T-0087: hooks the breaker paused after failing in a row
    const idle = !a && !asks.length && !plans.length && !(v.queue ?? []).length && !(v.inbox_total ?? 0) && !paused.length
    if (idle && !bgs.length && !doneSince.length && !v.mode?.trust) return next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    const working = e.props.isWorking
    const f = working || bgs.length ? await read($, frame) : null
    const subsBg = bgs.length ? (await read($, agents)).filter(x => !x.done).length : 0
    const nowMs = bgs.length ? await $.clock.now() : 0
    const c = await read($, ctx)
    const m = v.mode
    const done = a ? a.steps.filter(s => s.done).length : 0
    const cur = a?.steps.find(s => s.current)
    const narrow = e.props.bodyColumns < 90 // beside a docked pane: one column of single lines, details dropped
    const width = narrow ? Math.max(6, Math.min(12, e.props.bodyColumns - 28)) : Math.max(10, Math.min(28, e.props.bodyColumns - 70))
    const queued = (v.queue ?? []).length
    const inboxN = v.inbox_total ?? (v.inbox ?? []).length
    const todayDone = v.today_done ?? 0
    const upNext = (v.queue ?? [])[0] ?? (v.inbox ?? [])[0]
    const usual = a ? v.typical?.[`${a.type}/${a.tier}`] : undefined
    const bandNow = await $.clock.now()
    const cut = 'truncate-end' as const
    // T-0146: with the pane shown, the band keeps the task, what waits and what needs the person; the rest is the pane's
    const paneOpen = (await $.ui.panes().catch(() => [])).some(p => p.id === PANE && p.isShown)
    const sl = signalLine(v) // T-0472: quiet unless something is amber or red

    // Beside a docked pane the band is narrow: each row is one Text that cuts at its end, never mid-word per span.
    const head = narrow ? (
      <Box flexDirection="column" key="fm-band-head">
        {a ? (
          <Text wrap={cut}>
            <Text bold color={typeColor(a.type)}>
              {a.type}
            </Text>{' '}
            <Text color={hex(C.dim)}>{sizeWord(a.tier)}</Text>{' '}
            <Text bold color={hex(C.accent)}>
              {a.id}
            </Text>{' '}
            <Text bold>{a.title}</Text>
          </Text>
        ) : (
          <Text bold color={hex(C.accent)} wrap={cut}>
            Foreman · nothing active
          </Text>
        )}
        {a && a.steps.length > 0 && (
          <Box flexDirection="row" gap={1}>
            {working && <Text color={hex(C.accent)}>{spin(f ?? 0)}</Text>}
            {meter($.ui.resolve(e), e, 'fm-band-bar', width, done / a.steps.length, C.ok, f)}
            <Text wrap={cut}>
              <Text bold>
                {done}/{a.steps.length}
              </Text>{' '}
              {cur?.text ?? ''}
            </Text>
          </Box>
        )}
      </Box>
    ) : (
      <Box flexDirection="column" key="fm-band-head">
        <Box flexDirection="row" justifyContent="space-between">
          <Box flexDirection="row" gap={1} flexShrink={1}>
            {a ? (
              <Box flexDirection="row" gap={1} flexShrink={1}>
                {/* the title gives way first: the id never wraps (seen live: 'T-014' then '1' on the next row) */}
                <Box flexDirection="row" gap={1} flexShrink={0} key="fm-band-id">
                  <Text bold color={typeColor(a.type)}>
                    {a.type}
                  </Text>
                  <Text color={hex(C.dim)}>{sizeWord(a.tier)}</Text>
                  <Text bold color={hex(C.accent)}>
                    {a.id}
                  </Text>
                </Box>
                <Text bold wrap={cut}>
                  {a.title}
                </Text>
              </Box>
            ) : (
              <Text bold color={hex(C.accent)} wrap={cut}>
                Foreman · nothing active
              </Text>
            )}
          </Box>
          <Box flexDirection="row" gap={1} flexShrink={0}>
            {c && <Text color={hex(C.dim)}>context</Text>}
            {c && meter($.ui.resolve(e), e, 'fm-band-ctx', 6, c.percent / 100, c.percent >= CHECKPOINT_AT ? C.err : c.percent >= 60 ? C.warn : C.ok, null)}
            {c && <Text color={hex(C.dim)}>{Math.round(c.percent)}%</Text>}
            {m && <Text color={hex(m.autonomy === 'full' ? C.accent2 : C.dim)}>{m.autonomy === 'full' ? 'full auto' : 'standard'}</Text>}
            {m && !m.drive && <Text color={hex(C.warn)}>drive off</Text>}
            {m?.trust && <Text color={hex(C.warn)}>trust on</Text>}
            {sl && <Text color={hex(sl.level === 'red' ? C.err : C.warn)} wrap={cut}>{sl.level === 'red' ? '●' : '◐'} {sl.text}</Text>}
          </Box>
        </Box>
        {a && (
          <Box flexDirection="row" gap={1}>
            {working && <Text color={hex(C.accent)}>{spin(f ?? 0)}</Text>}
            {/* T-0909: a mini stage rail, the pane's in small */}
            {miniRail($.ui.resolve(e), e, a.stages.length, a.stages.indexOf(a.stage), working ? f : null)}
            <Text color={hex(C.dim)}>{a.stage}</Text>
            {a.steps.length > 0 && meter($.ui.resolve(e), e, 'fm-band-bar', width, done / a.steps.length, C.ok, f)}
            {a.steps.length > 0 && (
              <Text bold>
                {done}/{a.steps.length}
              </Text>
            )}
            {cur && <Text wrap={cut}>{cur.text}</Text>}
            {a.audits.need > 0 && (
              <Text color={hex(a.audits.done >= a.audits.need ? C.ok : C.dim)}>
                · audits {a.audits.done}/{a.audits.need}
              </Text>
            )}
            {typeof a.on_task_s === 'number' && (
              <Text color={hex(C.dim)} wrap={cut}>
                · {elapsed(a.on_task_s * 1000 + Math.max(0, bandNow - lastFull))} on it
                {usual ? ` · usually ${about(usual)}` : ''}
              </Text>
            )}
          </Box>
        )}
      </Box>
    )

    // T-0181: 'the dashboard is duplicated at the bottom of the chat even though there's a pannel on the top right': with
    // the pane shown the band says only what needs the person or just changed, and nothing at all when there's none
    if (paneOpen && !(doneSince.length || bgs.length || paused.length || asks.length || plans.length)) return next(e)
    return (
      <Box flexDirection="column" borderStyle="round" borderColor={hex(working ? pulse(C.accent, f) : C.track)} paddingX={1} key="fm-band">
        {!paneOpen && head}
        {!paneOpen && (queued > 0 || inboxN > 0) && (
          <Box flexDirection="row" gap={1} key="fm-band-queue-row">
            {!narrow && <Text color={hex(C.dim)}>today</Text>}
            {!narrow && meter($.ui.resolve(e), e, 'fm-band-queue', 10, todayDone / Math.max(1, todayDone + queued + inboxN + (a ? 1 : 0)), C.accent2, null)}
            <Text color={hex(C.dim)} wrap={cut}>
              ✓{todayDone} done · {queued} queued · {inboxN} in inbox
              {upNext && !narrow ? ` · next ${upNext.id} ${upNext.title}` : ''}
            </Text>
          </Box>
        )}
        {doneSince.length > 0 && (
          <Text color={hex(C.ok)} wrap={cut} key="fm-band-away">
            ✔ since your last message: {doneSince.length} done · {doneSince.slice(-6).join(' ')}
          </Text>
        )}
        {bgs.length > 0 && (
          <Box flexDirection="row" gap={1} key="fm-band-wait">
            <Text color={hex(C.accent2)}>{spin(f ?? 0)}</Text>
            <Text color={hex(C.accent2)} wrap={cut}>
              ◷ waiting on {bgs.length} background shell{bgs.length === 1 ? '' : 's'}
              {subsBg ? ` and ${subsBg} subagent${subsBg === 1 ? '' : 's'}` : ''}
            </Text>
            <Text wrap={cut}>{bgs[0]!.command}</Text>
            <Text color={hex(C.dim)} wrap={cut}>
              {elapsed(nowMs - bgs[0]!.startedAt)}
              {working ? '' : ' · Claude picks up when they finish'}
            </Text>
          </Box>
        )}
        {!working && !paneOpen && v.next && (
          <Text color={hex(C.dim)} wrap={cut}>
            → {humanNext(v.next)}
          </Text>
        )}
        {paused.length > 0 && (
          <Text color={hex(C.warn)} wrap={cut} key="fm-band-paused">
            ⚠ Foreman's {paused.join(', ')} hook{paused.length === 1 ? ' is' : 's are'} paused: it failed 3 times in a row
            and runs again within 10 min (fm doctor)
          </Text>
        )}
        {asks.map(x => (
          <Text color={hex(C.warn)} wrap={cut} key={`ask-${x.task}`}>
            ⚠ Needs you: {x.task} {x.allow.join(', ')} — {x.why}
          </Text>
        ))}
        {plans.slice(0, 2).map(q => (
          <Box flexDirection="row" gap={1} key={`plan-${q.id}`}>
            <Text color={hex(C.warn)} wrap={cut}>
              ⚠ {q.id} ({sizeWord(q.tier)}) plan awaits approval: {q.title}
            </Text>
            {/* consent is given in the pane, where the plan it approves is shown */}
            <Button key={`review-${q.id}`} label="review" hotkey="v" plain onPress={() => void openPane($, true)} />
          </Box>
        ))}
        {!paneOpen && <Box flexDirection="row" gap={2}>
          <Button key="open" label="dashboard" hotkey="f" plain onPress={() => void openPane($, true)} />
          {!working && (
            <Button
              key="next"
              label="next"
              hotkey="n"
              plain
              onPress={() => void $.prompt.submit({ text: '/foreman:next', asUser: true })}
            />
          )}
        </Box>}
      </Box>
    )
  })

  // T-0909: the pane reads top-down by urgency: what needs the person, then the hero (the task, its stage rail, progress
  // and time against the usual), what runs this moment, the plan in detail, the pulse charts, what's next, and the
  // quieter cards below. Rasters that move are registered for the 30 fps blit while work is live.
  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const ui = $.ui.resolve(e)
    const { Box, Button, Input, Text } = ui
    const v = await read($, view)
    const err = await read($, error)
    if (!v?.project) {
      return (
        <Box flexDirection="column">
          <Text color={hex(C.dim)}>Not a Foreman project here.{err ? ` (${err})` : ''}</Text>
          <Text color={hex(C.dim)}>Ask Claude to set it up, or run /foreman:intake with a request.</Text>
        </Box>
      )
    }
    const live = turns.size > 0 || starts.size > 0
    const clockNow = await $.clock.now()
    const moving = live && cfg.motion !== 'off' // T-0912: motion off draws work still
    const f = moving || clockNow < flashUntil ? await read($, frame) : null // a fading step glow redraws too
    const idleBeat = live || cfg.mascot === 'off' ? 0 : await read($, beat)
    const term = e.surface === 'terminal'
    if (term) motion.clear() // this drawing registers what moves
    // the rasters' time: the blit's clock in full motion (so a redraw never jumps), the frame in calm, none when off
    const ft = !moving ? null : cfg.motion === 'full' ? frameAt(clockNow) : f
    const blit = term && cfg.motion === 'full' ? motion : undefined
    const a = v.active
    const m = v.mode
    const inner = Math.max(24, e.props.bodyColumns - 6) // inside a card: border and padding
    const width = Math.max(10, e.props.bodyColumns - 12)
    const touched = await read($, files)
    const base = `${v.root || cfg.root}/` // T-0146: the project's files, relative; scratch files elsewhere aren't this card's
    const mine = touched.filter(t => t.path.startsWith(base))
    const subs = await read($, agents)
    const bgShells = await read($, shells)
    const fb = bgShells.length ? await read($, frame) : 0
    const isOn = await read($, sound)
    const cx = await read($, ctx)
    const queue = v.queue ?? []
    const inbox = v.inbox ?? []
    const inboxN = v.inbox_total ?? inbox.length
    const recent = (v.recent ?? []).slice(-LIST)
    const checks = v.checks
    // T-0181: 'the pannels color doesnt match': cards are the chat's quiet grey, colour only where it signals (the active
    // task, something waiting on the person, failing gates); each card's heading keeps its colour
    const card = (color: number | null = null) =>
      ({ flexDirection: 'column', borderStyle: 'round', borderColor: hex(color === null ? C.dim : pulse(color, f)), paddingX: 1 }) as const
    const head = (title: string, color: number, count?: string) => (
      <Box flexDirection="row" gap={1}>
        <Text bold color={hex(color)}>
          ▍{title}
        </Text>
        {count !== undefined && <Text color={hex(C.dim)} wrap="truncate-end">{count}</Text>}
      </Box>
    )
    const chip = (it: FmItem) => (
      <Box flexDirection="row" gap={1} flexShrink={0}>
        <Text bold color={typeColor(it.type)}>
          {it.type}
        </Text>
        <Text color={hex(C.dim)}>{sizeWord(it.tier)}</Text>
      </Box>
    )
    const done = a ? a.steps.filter(s => s.done).length : 0
    const proved = a ? a.criteria.filter(x => x.checked).length : 0
    const stageIdx = a ? a.stages.indexOf(a.stage) : -1
    const cur = a?.steps.find(s => s.current)
    const usual = a ? v.typical?.[`${a.type}/${a.tier}`] : undefined
    const onMin = a && typeof a.on_task_s === 'number' ? (a.on_task_s * 1000 + Math.max(0, clockNow - lastFull)) / 60000 : null
    const maxChurn = Math.max(1, ...touched.map(t => t.add + t.del))
    const passed = checks ? checks.results.filter(r => !r.exit).length : 0
    const failing = !!checks && passed < checks.results.length
    const asks = v.approvals ?? []
    const plans = queue.flatMap(q => (q.plan ? [{ ...q, plan: q.plan }] : []))
    const nowCalls = [...running].filter(([, x]) => !x.agent)
    const mascotW = cfg.mascot === 'off' ? 0 : 13 + Math.min(4, subs.filter(s => !s.done).length) * 8
    const heroW = Math.max(16, inner - mascotW)
    // the swim lanes: the last half hour of tool calls, a row per kind that ran
    const laneW = Math.max(10, inner - 6)
    // the window grows with the session, 1 to 30 minutes, so a fresh session's calls spread out instead of piling up
    const spanMin = Math.min(TIMELINE_MS, Math.max(60000, ticks.length ? clockNow - ticks[0]!.at : TIMELINE_MS)) / 60000
    const span = Math.ceil(spanMin) * 60000
    const recentTicks = ticks.filter(t => clockNow - t.at <= span)
    const laneRows = LANES.map(l => ({
      label: l,
      color: LANE_COLOR[l],
      slots: bucketize(recentTicks.filter(t => t.lane === l).map(t => t.at), clockNow, span, laneW * 2),
    })).filter(r => r.slots.some(Boolean))
    const days = v.done_days ?? []
    const gaugeW = Math.max(6, Math.min(16, inner - (days.length ? days.length * 2 + 1 : 0) - 24))

    const gate = checks && checks.results.length > 0 && (
      <Box key="card-gates" {...card(failing ? C.err : null)}>
        {head(
          'Gates',
          failing ? C.err : C.ok,
          `${passed}/${checks.results.length} passed · ${checks.at.slice(11, 16)} · a full run ≈ ${elapsed(1000 * checks.results.reduce((t, r) => t + r.s, 0))}`,
        )}
        {checks.results.map((r, i) => (
          <Box flexDirection="row" gap={1} key={`gate-${i}`}>
            <Text color={hex(r.exit ? C.err : C.ok)}>{r.exit ? '✗' : '✓'}</Text>
            <Text wrap="truncate-end">{r.cmd.slice(0, 60)}</Text>
            <Text color={hex(C.dim)}>{r.s.toFixed(1)}s</Text>
            {r.note ? (
              <Text color={hex(C.warn)} wrap="truncate-end">
                {r.note.slice(0, 40)}
              </Text>
            ) : null}
          </Box>
        ))}
      </Box>
    )

    return (
      <Box flexDirection="column" key="fm-pane">
        {err && <Text color={hex(C.err)}>fm: {err}</Text>}

        {asks.length > 0 && (
          <Box key="card-asks" {...card(C.warn)}>
            {head('Needs you', C.warn, `${asks.length} waiting`)}
            {asks.map(x => (
              <Text color={hex(C.warn)} wrap="wrap" key={`ask-${x.task}`}>
                ⚠ {x.task} · {x.allow.join(', ')}: {x.why}
              </Text>
            ))}
          </Box>
        )}

        {plans.map(q => (
          <Box key={`plan-${q.id}`} {...card(C.warn)}>
            {head(`${q.id} plan awaits your approval`, C.warn)}
            <Text bold wrap="wrap">
              {q.title}
            </Text>
            {q.plan.interpretation && <Text wrap="wrap">Means: {q.plan.interpretation}</Text>}
            {q.plan.approach && <Text wrap="wrap">Approach: {q.plan.approach}</Text>}
            {q.plan.steps.map(s => (
              <Text key={`plan-${q.id}-step-${s.n}`} wrap="truncate-end">
                ○ {s.n}. {s.text}
              </Text>
            ))}
            {q.plan.criteria.map(c => (
              <Text key={`plan-${q.id}-ac-${c.n}`} wrap="truncate-end">
                ○ AC{c.n} {c.text}
              </Text>
            ))}
            <Box flexDirection="row" gap={1}>
              <Button
                key={`approve-${q.id}`}
                label="✓ approve this plan"
                plain
                onPress={() => act($, ['task', 'set', q.id, 'approved=true'], `✓ ${q.id} plan approved`)}
              />
            </Box>
          </Box>
        ))}

        <Box flexDirection="row" justifyContent="space-between" borderStyle="round"
          borderColor={hex(a ? pulse(C.accent, f) : C.dim)} paddingX={1} key="fm-pane-head">
          <Box flexDirection="column" flexGrow={1} flexShrink={1}>
            <Box flexDirection="row" gap={1}>
              <Text bold color={hex(C.accent)}>
                {moving ? spin(f ?? 0) : '▍'} Foreman
              </Text>
              <Text color={hex(C.dim)} wrap="truncate-end">
                {v.project}
              </Text>
            </Box>
            {m && (
              <Box flexDirection="row" gap={1}>
                <Text color={hex(m.autonomy === 'full' ? C.accent2 : C.dim)}>{m.autonomy === 'full' ? 'full auto' : 'standard'}</Text>
                <Text color={hex(m.drive ? C.dim : C.warn)}>· drive {m.drive ? 'on' : 'off'}</Text>
                {m.sensitive && <Text color={hex(C.warn)}>· sensitive</Text>}
                {m.trust && <Text color={hex(C.warn)}>· trust on</Text>}
                {(m.standing ?? []).length > 0 && <Text color={hex(C.dim)}>· standing yes</Text>}
              </Box>
            )}
            {a ? (
              <Box flexDirection="column" key="hero-task">
                <Box flexDirection="row" gap={1} key="hero-title">
                  <Box flexDirection="row" gap={1} flexShrink={0}>
                    {chip(a)}
                    <Text bold color={hex(C.accent)}>
                      {a.id}
                    </Text>
                  </Box>
                  <Text bold wrap="wrap">
                    {a.title}
                  </Text>
                </Box>
                {stageIdx >= 0 && rail(ui, e, a.stages, stageIdx, heroW, ft, blit)}
                {a.steps.length > 0 && (
                  <Box flexDirection="row" gap={1} key="hero-progress">
                    {meter(ui, e, 'fm-pane-bar', Math.max(8, heroW - 14), done / a.steps.length, C.ok, f)}
                    <Text bold>
                      {done}/{a.steps.length}
                    </Text>
                    <Text color={hex(C.dim)}>{Math.round((100 * done) / a.steps.length)}%</Text>
                  </Box>
                )}
                {cur && (
                  <Text wrap="truncate-end" key="hero-step">
                    <Text color={hex(C.accent)}>{moving ? spin(f ?? 0) : '▸'}</Text> step {cur.n} · {cur.text}
                  </Text>
                )}
                {onMin !== null && (
                  <Box flexDirection="row" gap={1} key="hero-time">
                    {usual !== undefined && eta(ui, e, Math.max(8, heroW - 30), onMin, usual)}
                    <Text color={hex(usual !== undefined && onMin > usual ? C.warn : C.dim)} wrap="truncate-end">
                      {elapsed(onMin * 60000)} on it{usual !== undefined ? ` · usually ${about(usual)}` : ''}
                    </Text>
                  </Box>
                )}
              </Box>
            ) : (
              <Text color={hex(C.dim)} key="hero-idle">
                Nothing active{live ? ' · working' : ''}
              </Text>
            )}
            <Text color={hex(C.dim)}>
              <Text color={hex(C.ok)}>✓ {v.today_done ?? 0}</Text> today · {queue.length} queued · {inboxN} in inbox
            </Text>
            {(v.vetoes ?? []).length > 0 && (
              <Text key="fm-pane-vetoes" color={hex(C.dim)} wrap="truncate-end">
                ✋ you said: {v.vetoes![0]}{v.vetoes!.length > 1 ? ` · ${v.vetoes!.length - 1} more` : ''}
              </Text>
            )}
            {(v.revisit ?? []).length > 0 && (
              <Text key="fm-pane-revisit" color={hex(C.warn)} wrap="truncate-end">
                ◆ revisit: {v.revisit![0].decision} ({v.revisit![0].why}){v.revisit!.length > 1 ? ` · ${v.revisit!.length - 1} more` : ''}
              </Text>
            )}
            {v.next && (
              <Text color={hex(C.dim)} wrap="truncate-end">
                → {humanNext(v.next)}
              </Text>
            )}
          </Box>
          {mascotTree(ui, e, live ? 'work' : clockNow < happyUntil ? 'happy' : 'idle', live ? (f ?? 0) : idleBeat, subs)}
        </Box>

        {nowCalls.length > 0 && (
          <Box key="card-now" {...card(C.accent)}>
            {head('Now', C.accent, `${nowCalls.filter(([, x]) => x.icon !== '⚠').length} running`)}
            {nowCalls.slice(0, 4).map(([id, x], i) => {
              if (x.icon === '⚠')
                return (
                  <Text key={`now-${id}`} color={hex(C.warn)} wrap="truncate-end">
                    {'⚠ '}
                    {x.verb} · {elapsed(clockNow - x.at)}
                  </Text>
                )
              if (blit && ft !== null) blit.set(`now-bar-${i}`, { columns: 8, rows: 1, draw: t => activityCells(8, x.color, t + i * 3) })
              return (
                <Box flexDirection="row" gap={1} key={`now-${id}`}>
                  <Box flexShrink={0} flexDirection="row" gap={1}>
                    {meter(ui, e, `now-bar-${i}`, 8, null, x.color, ft === null ? null : ft + i * 3)}
                    <Text color={hex(x.color)}>
                      {x.icon} {x.verb}
                    </Text>
                  </Box>
                  <Text wrap="truncate-end">{x.target}</Text>
                  <Box flexShrink={0}>
                    <Text color={hex(C.dim)}>{elapsed(clockNow - x.at)}</Text>
                  </Box>
                </Box>
              )
            })}
            {nowCalls.length > 4 && <Text color={hex(C.dim)}>{more(nowCalls.length - 4, 'call')}</Text>}
          </Box>
        )}

        {subs.length > 0 && (
          <Box key="card-agents" {...card()}>
            {head('Subagents', C.agent, `${subs.filter(s => !s.done).length} running`)}
            {subs.map(s => (
              <Box flexDirection="row" gap={1} key={`agent-${s.id}`}>
                <Text color={hex(s.done ? C.dim : agentColor(s.id))}>{s.done ? '✓' : spin((f ?? 0) + s.tools)}</Text>
                <Text bold color={hex(s.done ? C.dim : C.agent)}>
                  {s.type}
                </Text>
                <Text wrap="truncate-end" color={s.done ? hex(C.dim) : undefined}>
                  {s.description}
                </Text>
                <Text color={hex(C.dim)} wrap="truncate-end">
                  {s.done
                    ? `done · ${s.tools} tool${s.tools === 1 ? '' : 's'}` // its last action is stale once it ends (T-0146)
                    : `${s.tools} tools · ${s.last.slice(0, 30)} · ${elapsed(clockNow - s.startedAt)}`}
                </Text>
                {!s.done && clockNow - (s.lastAt ?? s.startedAt) >= QUIET_MS && (
                  <Text color={hex(C.warn)}>quiet {elapsed(clockNow - (s.lastAt ?? s.startedAt))}</Text>
                )}
                {!s.done && clockNow - (s.lastAt ?? s.startedAt) >= STOP_MS && (
                  <Button key={`stop-${s.id}`} label="■ stop" plain onPress={() => void stopAgent($, s.id)} />
                )}
              </Box>
            ))}
          </Box>
        )}

        {bgShells.length > 0 && (
          <Box key="card-shells" {...card()}>
            {head('Background shells', C.accent2, `${bgShells.length} running · Claude picks up when they finish`)}
            {bgShells.map((x, i) => (
              <Box flexDirection="row" gap={1} key={`shell-${x.id}`}>
                <Text color={hex(C.accent2)}>{spin(fb + i)}</Text>
                <Text wrap="truncate-end">{x.command}</Text>
                <Text color={hex(C.dim)}>{elapsed(clockNow - x.startedAt)}</Text>
              </Box>
            ))}
          </Box>
        )}

        {failing && gate}

        {a && (
          <Box key="card-task" {...card()}>
            {head('Plan', C.accent, `${done}/${a.steps.length} steps · ${proved}/${a.criteria.length} proved`)}
            {/* T-0181: 'the AC and audits thing not matching': steps and done-when criteria under small labels in one
                glyph column; audits a bar like the steps' */}
            {a.steps.length > 0 && <Text color={hex(C.dim)}>steps</Text>}
            {a.steps.map(s => {
              const lit = flashed.get(`${a.id}:${s.n}`)
              const k = lit === undefined ? 1 : (clockNow - lit) / FLASH_MS
              return (
                <Text
                  key={`step-${s.n}`}
                  color={s.current ? hex(C.accent) : s.done ? hex(k < 1 ? C.ok : C.dim) : undefined}
                  backgroundColor={k < 1 ? hex(mix(mix(C.ok, BG, 0.62), BG, k)) : undefined}
                  wrap="truncate-end"
                >
                  {'  '}
                  {s.done ? '✓' : s.current ? (moving ? spin(f ?? 0) : '▸') : '○'} {s.n}. {s.text}
                </Text>
              )
            })}
            {a.criteria.length > 0 && <Text color={hex(C.dim)}>done when</Text>}
            {a.criteria.map(c => (
              <Box key={`ac-${c.n}`} flexDirection="column">
                <Text color={c.checked ? hex(C.ok) : undefined} wrap="truncate-end">
                  {'  '}
                  {c.checked ? '✓' : '○'} {c.n}. {c.text}
                </Text>
                {!c.checked && c.verify && (
                  <Text color={hex(mix(C.dim, C.track, 0.3))} wrap="truncate-end" key={`ac-verify-${c.n}`}>
                    {'     ↳ '}
                    {c.verify}
                  </Text>
                )}
              </Box>
            ))}
            {/* T-0711: the plan tree — the parts fm task split made, each with its progress */}
            {(a.children ?? []).length > 0 && <Text color={hex(C.dim)}>parts</Text>}
            {(a.children ?? []).map(k => (
              <Text key={`kid-${k.id}`} color={k.status === 'done' ? hex(C.dim) : k.status === 'active' ? hex(C.accent) : undefined} wrap="truncate-end">
                {'  '}
                {k.status === 'done' ? '✓' : k.status === 'active' ? '▸' : '○'} {k.id} {k.title}
                {k.steps_total ? `  ${k.steps_done}/${k.steps_total}` : ''}
              </Text>
            ))}
            {/* T-0228: the debugging ledger, the oracle's open questions and a batch's members, where the task is */}
            {(a.hypotheses ?? []).length > 0 && <Text color={hex(C.dim)}>hypotheses</Text>}
            {(a.hypotheses ?? []).map(hy => (
              <Text
                key={`hyp-${hy.n}`}
                color={hex(hy.status === 'confirmed' ? C.ok : hy.status === 'ruled out' ? C.dim : C.warn)}
                wrap="truncate-end"
              >
                {'  '}
                {hy.status === 'confirmed' ? '✓' : hy.status === 'ruled out' ? '✗' : '?'} H{hy.n}. {hy.text}
              </Text>
            ))}
            {a.oracle && (
              <Text key="fm-pane-oracle" color={hex(a.oracle.ambiguities.length ? C.warn : C.dim)} wrap="truncate-end">
                oracle: {a.oracle.examples} example{a.oracle.examples === 1 ? '' : 's'}
                {a.oracle.ambiguities.length
                  ? ` · ${a.oracle.ambiguities.length} open question${a.oracle.ambiguities.length === 1 ? '' : 's'}: ${a.oracle.ambiguities[0]}`
                  : ' · no open questions'}
              </Text>
            )}
            {(a.batch ?? []).length > 0 && (
              <Text key="fm-pane-batch" color={hex(C.dim)} wrap="truncate-end">
                batch of {(a.batch ?? []).join(', ')}
              </Text>
            )}
            {/* T-0261: a run that proved nothing, and the assumptions the plan rests on unchecked */}
            {(a.inconclusive ?? 0) > 0 && (
              <Text key="fm-pane-inconclusive" color={hex(C.warn)} wrap="truncate-end">
                ≈ {a.inconclusive} inconclusive run{a.inconclusive === 1 ? '' : 's'}: a sharper check is next
              </Text>
            )}
            {(a.unverified ?? []).length > 0 && (
              <Text key="fm-pane-unverified" color={hex(C.dim)} wrap="truncate-end">
                ? {(a.unverified ?? []).length} unverified assumption{(a.unverified ?? []).length === 1 ? '' : 's'}: {(a.unverified ?? [])[0]}
              </Text>
            )}
            {a.audits.need > 0 && (
              <Box flexDirection="row" gap={1} key="fm-pane-audits">
                <Text color={hex(C.dim)}>audits</Text>
                {meter(ui, e, 'fm-pane-audits-bar', 10, a.audits.done / a.audits.need, C.accent2, null)}
                <Text bold>
                  {a.audits.done}/{a.audits.need}
                </Text>
                {a.blockers.length > 0 && (
                  <Text color={hex(C.dim)} wrap="truncate-end">
                    · {a.blockers.length} left before done: {a.blockers[0]}
                  </Text>
                )}
              </Box>
            )}
          </Box>
        )}

        {(laneRows.length > 0 || days.some(Boolean) || cx || v.health) && (
          <Box key="card-pulse" {...card()}>
            {head('Pulse', C.accent2, laneRows.length ? `${recentTicks.length} tool call${recentTicks.length === 1 ? '' : 's'} · last ${span / 60000} min` : 'no tool calls lately')}
            {laneRows.length > 0 && lanes(ui, e, laneRows, laneW, ft, blit)}
            {laneRows.length > 0 && term && (
              <Text color={hex(mix(C.dim, C.track, 0.3))} key="lanes-axis">
                {`${' '.repeat(6)}${span / 60000}m ago`.padEnd(laneW + 3)}now
              </Text>
            )}
            <Box flexDirection="row" gap={2} key="pulse-row">
              {days.length > 0 && (
                <Box flexDirection="column" flexShrink={0} key="pulse-days">
                  {bars(ui, e, 'done-days', days, 3, C.accent2, C.ok)}
                  <Text color={hex(C.dim)}>
                    {days.reduce((x, y) => x + y, 0)} closed · 14d
                  </Text>
                </Box>
              )}
              <Box flexDirection="column" flexGrow={1} key="pulse-gauges">
                {cx && (
                  <Box flexDirection="row" gap={1} key="g-ctx">
                    <Text color={hex(C.dim)}>{'context'.padEnd(7)}</Text>
                    {meter(ui, e, 'fm-pane-ctx', gaugeW, cx.percent / 100, cx.percent >= CHECKPOINT_AT ? C.err : cx.percent >= 60 ? C.warn : C.ok, null)}
                    <Text>{Math.round(cx.percent)}%</Text>
                  </Box>
                )}
                {v.budget && (
                  <Box flexDirection="row" gap={1} key="g-spend">
                    <Text color={hex(C.dim)}>{'spend'.padEnd(7)}</Text>
                    {meter(ui, e, 'fm-pane-spend', gaugeW, Math.min(1, v.budget.today_usd / Math.max(0.01, v.budget.caps.day)), C.accent2, null)}
                    <Text>${v.budget.today_usd.toFixed(2)}</Text>
                  </Box>
                )}
                {v.health && (
                  <Box flexDirection="row" gap={1} key="g-hooks">
                    <Text color={hex(C.dim)}>{'hooks'.padEnd(7)}</Text>
                    {(v.latency ?? []).length > 1 && spark(ui, e, 'fm-latency', v.latency ?? [], gaugeW)}
                    <Text color={hex(v.health.hook_errors ? C.err : C.dim)} wrap="truncate-end">
                      p95 {v.health.hook_p95_ms ?? '–'} ms
                    </Text>
                  </Box>
                )}
                {v.health && (
                  <Text color={hex(v.health.hook_errors || (v.health.paused_hooks ?? []).length ? C.err : C.dim)} wrap="truncate-end" key="g-guard">
                    {'guard'.padEnd(7)} {v.health.guard_blocks} block{v.health.guard_blocks === 1 ? '' : 's'}
                    {v.health.hook_errors ? ` · ${v.health.hook_errors} hook error(s)` : ''}
                    {(v.health.paused_hooks ?? []).length ? ` · paused: ${(v.health.paused_hooks ?? []).join(', ')}` : ''}
                  </Text>
                )}
              </Box>
            </Box>
          </Box>
        )}

        {queue.length > 0 ? (
          <Box key="card-queue" {...card(queue.some(q => q.waits) ? C.warn : null)}>
            {head('Queue', C.accent2, `${queue.length}${queue.length ? ` · ${queue.filter(q => !q.waits).length} ready` : ''}`)}
            {queue.slice(0, LIST).map((q, i) => (
              <Box flexDirection="row" gap={1} key={`q-${q.id}`}>
                <Text color={hex(fade(LIST - 1 - i, LIST, C.accent2))}>{i === 0 ? '▶' : `${i + 1}.`}</Text>
                {chip(q)}
                {q.steps_total ? meter(ui, e, `q-bar-${q.id}`, 6, (q.steps_done ?? 0) / q.steps_total, C.ok, null) : null}
                {v.typical?.[`${q.type}/${q.tier}`] !== undefined && (
                  <Box key={`q-typ-${q.id}`} flexShrink={0}>
                    <Text color={hex(C.dim)}>{about(v.typical[`${q.type}/${q.tier}`]!)}</Text>
                  </Box>
                )}
                <Text wrap="truncate-end" color={q.waits ? hex(C.warn) : i === 0 ? undefined : hex(mix(C.dim, 0xc8ccd4, 0.6))}>
                  {q.id} {q.title}
                  {q.waits ? `  (${q.waits})` : ''}
                </Text>
              </Box>
            ))}
            {queue.length > LIST && <Text color={hex(C.dim)}>{more(queue.length - LIST, 'task')}</Text>}
          </Box>
        ) : null}

        <Box key="card-inbox" {...card()}>
          {queue.length + inboxN > 0 ? head('Inbox', C.accent, `${inboxN}`) : head('Up next', C.accent, 'queue and inbox empty')}
          {captureBox($, e)}
          {inbox.slice(0, LIST).map(it => (
            <Box flexDirection="row" gap={1} key={`in-${it.id}`}>
              {chip(it)}
              <Text wrap="truncate-end">
                {it.id} {it.title}
              </Text>
              {it.age_days !== undefined && (
                // T-0228: the title gives way, never the age ('today' had wrapped to 'to/da/y' in a 70-column pane)
                <Box flexShrink={0} key={`in-age-${it.id}`}>
                  <Text color={hex(C.dim)}>{ago(it.age_days)}</Text>
                </Box>
              )}
              <Button
                key={`start-${it.id}`}
                label="▸ start"
                plain
                dimColor
                onPress={() => void $.prompt.submit({ text: `Plan and start ${it.id} (/foreman:intake).`, asUser: true })}
              />
              <Button
                key={`drop-${it.id}`}
                label="✕ drop"
                plain
                dimColor
                onPress={() => act($, ['task', 'drop', it.id, 'dropped from the Foreman pane'], `${it.id} dropped`)}
              />
            </Box>
          ))}
          {inboxN > Math.min(LIST, inbox.length) && (
            <Text color={hex(C.dim)}>{`… ${inboxN - Math.min(LIST, inbox.length)} more in the inbox`}</Text>
          )}
        </Box>

        {!failing && gate}

        {v.brainstorm && (
          <Box key="card-brainstorm" {...card()}>
            {head(
              'Brainstorm',
              C.agent,
              v.brainstorm.running
                ? `${spin(fb + clockNow / 300)} ${v.brainstorm.answers}/${v.brainstorm.expected ?? '?'} answers · ${v.brainstorm.count} ideas so far`
                : v.brainstorm.grounded // its slate is built: one line however recent (T-0196)
                  ? `${v.brainstorm.count} ideas · grounded`
                  : (v.brainstorm.age_h ?? 0) < 2
                    ? `${v.brainstorm.count} ideas · ${v.brainstorm.name.replace('brainstorm-', '')}`
                    : `${v.brainstorm.count} ideas · ${hoursAgo(v.brainstorm.age_h ?? 0)}`, // an old one is one line (T-0146)
            )}
            {(v.brainstorm.running || (!v.brainstorm.grounded && (v.brainstorm.age_h ?? 0) < 2) ? v.brainstorm.ideas : []).map((idea, i) => (
              <Text key={`idea-${i}`} color={hex(fade(i, v.brainstorm!.ideas.length, /wild/i.test(idea) ? C.agent : 0xc8ccd4))} wrap="truncate-end">
                {/wild/i.test(idea) ? '✦' : '•'} {idea.replace(/^wild:\s*/i, '').replace(/\s*\(wild\)$/i, '')}
              </Text>
            ))}
          </Box>
        )}

        {mine.length > 0 && (
          <Box key="card-files" {...card()}>
            {head('Files this session', C.edit, `${mine.length} · +${mine.reduce((n, t) => n + t.add, 0)} −${mine.reduce((n, t) => n + t.del, 0)}`)}
            {mine
              .slice(-LIST)
              .reverse()
              .map((t, i) => (
                <Box flexDirection="row" gap={1} key={`file-${i}`}>
                  {churn(ui, e, `file-bar-${i}`, t, maxChurn)}
                  <Text color={hex(C.ok)}>+{t.add}</Text>
                  <Text color={hex(C.err)}>−{t.del}</Text>
                  <Text wrap="truncate-start">{shortPath(t.path.slice(base.length), 40)}</Text>
                </Box>
              ))}
            {mine.length > LIST && <Text color={hex(C.dim)}>{`… ${mine.length - LIST} more`}</Text>}
          </Box>
        )}

        {(v.fleet ?? []).some(s => s.remote || s.error) || (v.fleet ?? []).length > 1 ? (
          // T-0711: the fleet deck — every live session here, a tile per remote session, one steer for all; one session
          // alone is this one, already above (T-0909)
          <Box key="card-fleet" {...card()}>
            {head('Fleet', C.agent, `${(v.fleet ?? []).filter(s => !s.error).length}`)}
            {(v.fleet ?? []).slice(0, LIST).map(s => (
              <Box flexDirection="row" gap={1} key={`fleet-${s.remote ?? 'here'}-${s.session}`}>
                <Text color={hex(s.error ? C.warn : s.remote ? C.accent2 : C.agent)}>{s.error ? '!' : '●'}</Text>
                <Box flexShrink={0} key={`fleet-who-${s.remote ?? 'here'}-${s.session}`}>
                  <Text bold color={hex(s.remote ? C.accent2 : C.agent)}>
                    {s.remote ? s.remote.toUpperCase() : s.session.slice(0, 8)}
                  </Text>
                </Box>
                <Text wrap="truncate-end" color={s.error ? hex(C.warn) : undefined}>
                  {s.error ?? `${s.project ?? '-'} · ${s.task ?? 'no task'}${s.title ? ` ${s.title}` : ''}`}
                </Text>
                {!s.error && (
                  <Box flexShrink={0} key={`fleet-ctx-${s.remote ?? 'here'}-${s.session}`}>
                    <Text color={hex(C.dim)}>
                      {`ctx ${s.context_pct ?? '?'}%${s.mail ? ` · mail ${s.mail}` : ''}${s.remote && s.age_s != null ? ` · ${elapsed(s.age_s * 1000)} ago` : ''}`}
                    </Text>
                  </Box>
                )}
              </Box>
            ))}
            {e.surface !== 'mobile' && (
              <Input key="steer" placeholder="↯ steer every session… (Enter)" submitLabel="Steer" onSubmit={text => void steer($, text)} />
            )}
          </Box>
        ) : null}

        {/* T-0228: spend against fm budget's caps, the bench and evolve, research asks — each only when it has news */}
        {v.budget && (v.budget.today_usd > 0 || v.budget.subagent_tokens > 0 || v.budget.halved || v.budget.subagents_paused) && (
          <Box key="card-budget" {...card(v.budget.halved || v.budget.subagents_paused ? C.warn : null)}>
            {head(
              'Spend today',
              C.accent2,
              `$${v.budget.today_usd.toFixed(2)} of $${v.budget.caps.day.toFixed(0)} · subagents ${tokensWord(v.budget.subagent_tokens)}${v.budget.subagents_paused ? ` · waiting: ${v.budget.subagents_paused}` : ''}`,
            )}
            <Box flexDirection="row" gap={1}>
              {meter(ui, e, 'fm-budget-bar', Math.min(30, width - 10), Math.min(1, v.budget.today_usd / Math.max(0.01, v.budget.caps.day)), C.accent2, null)}
              {v.budget.halved && <Text color={hex(C.warn)}>caps halved: {v.budget.halved}</Text>}
            </Box>
            {v.budget.top.map(t => (
              <Text key={`spend-${t.feature}`} color={hex(C.dim)} wrap="truncate-end">
                {'  '}
                {t.feature} · {t.tokens ? tokensWord(t.tokens) : `$${t.usd.toFixed(2)}`} · {t.runs} run{t.runs === 1 ? '' : 's'}
              </Text>
            ))}
          </Box>
        )}

        {v.bench && (
          <Box key="card-bench" {...card()}>
            {head('Bench', C.agent, `${v.bench.cases} case${v.bench.cases === 1 ? '' : 's'}`)}
            {v.bench.last && (
              <Text wrap="truncate-end">
                <Text color={hex(v.bench.last.passed === v.bench.last.total ? C.ok : C.warn)}>
                  {v.bench.last.passed}/{v.bench.last.total} passed
                </Text>
                <Text color={hex(C.dim)}>
                  {' '}
                  · ${v.bench.last.cost_usd.toFixed(2)} · {v.bench.last.label}
                  {v.bench.last.score != null ? ` · judged ${v.bench.last.score}/5` : ''}
                  {v.bench.last.repeats != null ? ` · ${v.bench.last.repeats} repeat${v.bench.last.repeats === 1 ? '' : 's'}` : ''}
                </Text>
              </Text>
            )}
            {(v.bench.verdicts ?? []).map((x, i) => (
              <Text key={`verdict-${i}`} color={hex(x.ok ? C.ok : C.warn)} wrap="truncate-end">
                {x.ok ? '✓' : '✗'} {x.kind}: {x.verdict ?? ''}
              </Text>
            ))}
            {v.bench.evolve.map((x, i) => (
              <Text key={`evolve-${i}`} color={hex(x.kept ? C.ok : C.dim)} wrap="truncate-end">
                {x.kept ? '✓ kept' : '✗ dropped'} {shortPath(x.target ?? '', 34)} · {x.why ?? ''}
              </Text>
            ))}
          </Box>
        )}

        {(v.research ?? []).length > 0 && (
          <Box key="card-research" {...card()}>
            {head('Research', C.accent2, 'quotes checked against their pages')}
            {(v.research ?? []).map(r => (
              <Text key={`research-${r.name}`} wrap="truncate-end">
                <Text color={hex(C.ok)}>✓{r.verified}</Text> <Text color={hex(r.not_found ? C.err : C.dim)}>✗{r.not_found}</Text>{' '}
                <Text color={hex(C.dim)}>?{r.unchecked}</Text> {r.name.replace(/^ask-/, '').replace(/-\d{8}-\d{4}$/, '')}
                {(r.conflicts ?? 0) > 0 && <Text color={hex(C.warn)}> · ⟷{r.conflicts} conflict{r.conflicts === 1 ? '' : 's'}</Text>}
                {(r.single ?? 0) > 0 && <Text color={hex(C.dim)}> · {r.single} single-source</Text>}
              </Text>
            ))}
          </Box>
        )}

        <Box key="card-activity" {...card()}>
          {head('Activity', C.dim, recent.length ? 'newest first' : 'nothing yet')}
          {[...recent].reverse().map((line, i) => {
            const [, time, rest] = /^(\d\d:\d\d)\s+(.*)$/.exec(line) ?? [null, '', line]
            return (
              <Text color={hex(fade(recent.length - 1 - i, recent.length, 0xc8ccd4))} wrap="truncate-end" key={`r-${i}`}>
                {time ? <Text color={hex(C.dim)}>{`${time} `}</Text> : null}
                {rest}
              </Text>
            )
          })}
        </Box>

        <Box flexDirection="row" gap={2} borderStyle="round" borderColor={hex(C.dim)} paddingX={1} key="fm-pane-controls">
          <Button
            key="next"
            label="next"
            hotkey="n"
            plain
            onPress={() => void $.prompt.submit({ text: '/foreman:next', asUser: true })}
          />
          <Button
            key="drive"
            label={m?.drive ? 'turn drive off' : 'turn drive on'}
            hotkey="d"
            plain
            onPress={() => act($, ['drive', m?.drive ? 'off' : 'on'], `drive ${m?.drive ? 'off' : 'on'}`)}
          />
          <Button
            key="autonomy"
            label={m?.autonomy === 'full' ? 'switch to standard' : 'switch to full auto'}
            plain
            dimColor
            onPress={() => {
              const level = m?.autonomy === 'full' ? 'standard' : 'full'
              return act($, ['autonomy', level], `autonomy ${level}`)
            }}
          />
          <Button
            key="sound"
            label={isOn ? 'mute' : 'unmute'}
            plain
            dimColor
            onPress={async () => {
              await update($, sound, x => !x)
              await $.store.set('sound', await read($, sound))
            }}
          />
          <Button key="refresh" label="refresh" hotkey="r" plain dimColor onPress={() => refresh($)} />
        </Box>
      </Box>
    )
  })
}
