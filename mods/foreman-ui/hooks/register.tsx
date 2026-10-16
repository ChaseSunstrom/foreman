import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, RenderElement, RenderInput, ResolveInput } from 'claude-code'


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
  clawd,
  elapsed,
  fade,
  hex,
  humanNext,
  layout,
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
import { CHECKPOINT_AT, FRAME_MS, FRESH, IDLE_FRAMES, PANE, QUIET_MS, SHELL_MAX_MS, STOP_MS, TIMELINE_MS, cfg, laneOf, running, starts, ticks, took } from './state'

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
const reviewing = atom({ plugin: 'foreman-ui', key: 'reviewing' } as const, null as string | null) // T-0989: a waiting plan shown in the Task section
import { agentOut, agentRow, bars, editChanges, editRow, mascotTree, meter, miniRail, rail, shellRow, spark } from './rows'
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
    if (closed.length) {
      const t = await $.clock.now()
      const was = prev?.active?.id === closed[0] ? prev.active : null
      const rec = (next.closed ?? []).find(x => x.id === closed[0])
      closing = {
        id: closed[0]!, title: was?.title ?? rec?.title ?? '', grade: rec?.grade, lenses: rec?.lenses,
        proved: was ? was.criteria.length : null, // done means every criterion has its evidence
        minutes: typeof was?.on_task_s === 'number' ? (was.on_task_s * 1000 + Math.max(0, t - lastFull)) / 60000 : null,
        usual: was ? prev?.typical?.[`${was.type}/${was.tier}`] : undefined, at: t,
      }
      if (cfg.motion !== 'off') {
        flashUntil = Math.max(flashUntil, t + CLOSING_MS) // the clock runs until the card has settled away
        await wake($)
      }
    }
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
// A step that just got done glows green and fades over FLASH_MS; the frame clock runs until it has
const flashed = new Map<string, number>() // "T-0007:2" → when it was seen done
const FLASH_MS = 2500
const BG = 0x181a21 // the terminal's background the glow fades into
let flashUntil = 0
// T-0913: the task that just closed, shown for CLOSING_MS at the top of the pane: grade, proof, time against the usual
type Closing = { id: string; title: string; grade?: string | null; lenses?: string[]; proved: number | null; minutes: number | null; usual?: number; at: number }
let closing: Closing | null = null
const CLOSING_MS = 6000
const SWEEP_MS = 900

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
  const now = await $.clock.now()
  const quiet = !turns.size && !starts.size && now >= flashUntil // a step's glow is still fading
  if (quiet && !bgLive && f - lastActive > 2) {
    await update($, frame, n => n + 1) // one last redraw, so what faded (a glow, the done card) is drawn settled
    return sleep()
  }
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
    // Claude Code 2.1.299: turn.start fires for subagents too (with agentId); their progress is the Subagents card's,
    // and resetting here would wipe the main turn's counts mid-turn (T-0944)
    if (e.agentId) return next(e)
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
        <Text weight="bold" color={hex(face.color)}>
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
          <Text weight="bold" color={hex(C.accent2)}>
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
        <Text weight="bold" color={hex(C.accent)}>
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
                  <Text key={j} weight={p.bold ? 'bold' : 'regular'} {...(p.color !== undefined ? { color: hex(p.color) } : {})}>
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
    const shown = (await $.ui.panes().catch(() => [])).some(p => p.id === PANE && p.isShown) // /fm would close it
    return next({ ...e, props: { ...e.props, tail: shown ? '⚠ Foreman needs you: see the pane' : '⚠ Foreman needs you: /fm' } }) // the engine puts the separator before it
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
    // T-0989: with the pane shown it is the one panel: its attention row has what the band would say
    if ((await $.ui.panes().catch(() => [])).some(p => p.id === PANE && p.isShown)) return next(e)
    const sl = signalLine(v) // T-0472: quiet unless something is amber or red

    // Beside a docked pane the band is narrow: each row is one Text that cuts at its end, never mid-word per span.
    const head = narrow ? (
      <Box flexDirection="column" key="fm-band-head">
        {a ? (
          <Text wrap={cut}>
            <Text weight="bold" color={typeColor(a.type)}>
              {a.type}
            </Text>{' '}
            <Text color={hex(C.dim)}>{sizeWord(a.tier)}</Text>{' '}
            <Text weight="bold" color={hex(C.accent)}>
              {a.id}
            </Text>{' '}
            <Text weight="bold">{a.title}</Text>
          </Text>
        ) : (
          <Text weight="bold" color={hex(C.accent)} wrap={cut}>
            Foreman · nothing active
          </Text>
        )}
        {a && a.steps.length > 0 && (
          <Box flexDirection="row" gap={1}>
            {working && <Text color={hex(C.accent)}>{spin(f ?? 0)}</Text>}
            {meter($.ui.resolve(e), e, 'fm-band-bar', width, done / a.steps.length, C.ok, f)}
            <Text wrap={cut}>
              <Text weight="bold">
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
                  <Text weight="bold" color={typeColor(a.type)}>
                    {a.type}
                  </Text>
                  <Text color={hex(C.dim)}>{sizeWord(a.tier)}</Text>
                  <Text weight="bold" color={hex(C.accent)}>
                    {a.id}
                  </Text>
                </Box>
                <Text weight="bold" wrap={cut}>
                  {a.title}
                </Text>
              </Box>
            ) : (
              <Text weight="bold" color={hex(C.accent)} wrap={cut}>
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
              <Text weight="bold">
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

    return (
      <Box flexDirection="column" borderStyle="round" borderColor={hex(working ? pulse(C.accent, f) : C.track)} paddingX={1} key="fm-band">
        {head}
        {(queued > 0 || inboxN > 0) && (
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
        {!working && v.next && (
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
        <Box flexDirection="row" gap={2}>
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
        </Box>
      </Box>
    )
  })

  // T-0989: one panel, sized by the dock. Fixed sections whose heights come from the dock's rows (layout), never from what
  // they hold, so the pane fits one screen and nothing moves as work comes and goes; rules between them, not boxes; each
  // fact shown once. Rasters that move are registered for the 30 fps blit while work is live.
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
    const W = Math.max(24, e.props.bodyColumns - 2) // inside the panel's padding
    const L = layout(e.props.scroll?.bodyRows ?? 40)
    const dim = hex(C.dim)
    const soft = hex(mix(C.dim, C.track, 0.3))
    const touched = await read($, files)
    const base = `${v.root || cfg.root}/` // T-0146: the project's files, relative; scratch files elsewhere aren't counted
    const mine = touched.filter(t => t.path.startsWith(base))
    const subs = await read($, agents)
    const bgShells = await read($, shells)
    const fb = bgShells.length ? await read($, frame) : 0
    const isOn = await read($, sound)
    const cx = await read($, ctx)
    const shownPlan = await read($, reviewing)
    const doneSince = await read($, away)
    const queue = v.queue ?? []
    const inbox = v.inbox ?? []
    const inboxN = v.inbox_total ?? inbox.length
    const checks = v.checks
    const done = a ? a.steps.filter(s => s.done).length : 0
    const proved = a ? a.criteria.filter(x => x.checked).length : 0
    const stageIdx = a ? a.stages.indexOf(a.stage) : -1
    const usual = a ? v.typical?.[`${a.type}/${a.tier}`] : undefined
    const onMin = a && typeof a.on_task_s === 'number' ? (a.on_task_s * 1000 + Math.max(0, clockNow - lastFull)) / 60000 : null
    const passed = checks ? checks.results.filter(r => !r.exit).length : 0
    const failing = !!checks && passed < checks.results.length
    const asks = v.approvals ?? []
    const plans = queue.flatMap(q => (q.plan ? [{ ...q, plan: q.plan }] : []))
    const nowCalls = [...running].filter(([, x]) => !x.agent)
    const days = v.done_days ?? []
    const paused = v.health?.paused_hooks ?? []
    const mascotW = cfg.mascot === 'off' ? 0 : 13 + Math.min(4, subs.filter(s => !s.done).length) * 8
    const headW = Math.max(16, W - mascotW)
    const since = (ms: number) => (ms < 3600000 ? `${Math.max(1, Math.round(ms / 60000))}m ago` : hoursAgo(ms / 3600000))
    const chip = (it: FmItem) => (
      <Box flexDirection="row" gap={1} flexShrink={0}>
        <Text weight="bold" color={typeColor(it.type)}>
          {it.type}
        </Text>
        <Text color={dim}>{sizeWord(it.tier)}</Text>
      </Box>
    )
    // a section: a rule naming it with one line of detail, then exactly `rows` rows, whatever it holds (none: not drawn);
    // what doesn't fit is counted on its last row, never cut silently (T-0146). `tall`: rows its elements take beyond one each
    const section = (key: string, rows: number, label: string, color: number, detail: string, body: RenderElement[], tall = 0) => {
      if (rows <= 0) return null
      const over = body.length + tall > rows
      const shown = over
        ? [...body.slice(0, Math.max(0, rows - 1 - tall)), <Text key={`${key}-more`} color={dim} wrap="truncate-end">{`… ${body.length - Math.max(0, rows - 1 - tall)} more`}</Text>]
        : body
      const pad = Math.max(0, rows - tall - shown.length) // blank rows drawn, not left to the box: the row after stays plain
      const head = detail ? `${label} ${detail} ` : `${label} `
      return (
        <Box key={key} flexDirection="column" flexShrink={0}>
          <Text key={`${key}-rule`} wrap="truncate-end">
            <Text weight="bold" color={hex(color)}>
              {label}
            </Text>
            <Text color={dim}>{detail ? ` ${detail} ` : ' '}</Text>
            <Text color={hex(C.track)}>{'─'.repeat(Math.max(0, W - head.length))}</Text>
          </Text>
          <Box key={`${key}-body`} flexDirection="column" height={rows} overflow="hidden">
            {shown}
            {Array.from({ length: pad }, (_, i) => (
              <Text key={`${key}-pad-${i}`}> </Text>
            ))}
          </Box>
        </Box>
      )
    }

    // ── header: who and how, the task or what's next, and Claude
    const modes: [string, number][] = m
      ? [
          [m.autonomy === 'full' ? 'full auto' : 'standard', m.autonomy === 'full' ? C.accent2 : C.dim],
          ...(m.drive ? [] : ([['drive off', C.warn]] as [string, number][])),
          ...(m.sensitive ? ([['sensitive', C.warn]] as [string, number][]) : []),
          ...(m.trust ? ([['trust on', C.warn]] as [string, number][]) : []),
          ...((m.standing ?? []).length ? ([['standing yes', C.dim]] as [string, number][]) : []),
        ]
      : []
    const header = (
      <Box key="fm-pane-head" flexDirection="row" height={3} overflow="hidden" flexShrink={0}>
        <Box flexDirection="column" flexGrow={1} flexShrink={1} width={headW}>
          <Text key="head-who" wrap="truncate-end">
            <Text weight="bold" color={hex(C.accent)}>
              {moving ? spin(f ?? 0) : '▍'} Foreman
            </Text>
            <Text color={dim}> {v.project}</Text>
            {modes.map(([w, c], i) => (
              <Text key={`mode-${i}`} color={hex(c)}>{` · ${w}`}</Text>
            ))}
          </Text>
          {a ? (
            <Box key="head-task" flexDirection="row" gap={1}>
              {chip(a)}
              <Box flexShrink={0}>
                <Text weight="bold" color={hex(C.accent)}>
                  {a.id}
                </Text>
              </Box>
              <Text weight="bold" wrap="truncate-end">
                {a.title}
              </Text>
            </Box>
          ) : (
            <Text key="head-task" color={dim} wrap="truncate-end">
              Nothing active{live ? ' · working' : ''}
            </Text>
          )}
          {a ? (
            <Box key="head-progress" flexDirection="row" gap={1}>
              {a.steps.length > 0 && meter(ui, e, 'fm-pane-bar', Math.max(6, Math.min(16, headW - 44)), done / a.steps.length, C.ok, f)}
              <Text wrap="truncate-end">
                {a.steps.length > 0 ? <Text weight="bold">{`${done}/${a.steps.length} steps`}</Text> : null}
                {L.task < 8 ? <Text color={dim}>{` · ${a.stage}`}</Text> : null}
                {onMin !== null ? (
                  <Text color={hex(usual !== undefined && onMin > usual ? C.warn : C.dim)}>
                    {` · ${elapsed(onMin * 60000)} on it${usual !== undefined ? ` · usually ${about(usual)}` : ''}`}
                  </Text>
                ) : null}
              </Text>
            </Box>
          ) : (
            <Text key="head-progress" color={dim} wrap="truncate-end">
              {v.next ? `→ ${humanNext(v.next)}` : 'queue and inbox empty'}
            </Text>
          )}
        </Box>
        {mascotTree(ui, e, live ? 'work' : clockNow < happyUntil ? 'happy' : 'idle', live ? (f ?? 0) : idleBeat, subs)}
      </Box>
    )

    // ── one attention row: the most urgent thing, or that nothing needs you
    const attention = (() => {
      const row = (color: number, text: string, lead?: RenderElement | null, tail?: RenderElement | null) => (
        <Box key="fm-pane-attention" flexDirection="row" gap={1} height={1} overflow="hidden" flexShrink={0}>
          {lead}
          <Text color={hex(color)} wrap="truncate-end">
            {text}
          </Text>
          {tail}
        </Box>
      )
      if (err) return row(C.err, `✗ fm: ${err}`)
      if (paused.length) // Foreman's own checks are off: before anything else (T-0087)
        return row(C.warn, `⚠ ${paused.join(', ')} hook${paused.length === 1 ? ' is' : 's are'} paused after failing 3 times in a row · fm doctor`)
      if (asks.length) {
        const x = asks[0]!
        return row(C.warn, `⚠ needs you: ${x.task} ${x.allow.join(', ')} — ${x.why}${asks.length > 1 ? ` · ${asks.length - 1} more` : ''}`)
      }
      if (plans.length) {
        const q = plans[0]!
        return row(
          C.warn,
          `⚠ ${q.id} plan awaits your yes${a ? `: ${q.title}` : ' (below)'}${plans.length > 1 ? ` · ${plans.length - 1} more` : ''}`,
          null,
          <Box key="attention-plan" flexDirection="row" gap={1} flexShrink={0}>
            <Button key={`att-approve-${q.id}`} label="✓ approve" plain onPress={() => act($, ['task', 'set', q.id, 'approved=true'], `✓ ${q.id} plan approved`)} />
            {a && (
              <Button key={`review-${q.id}`} label={shownPlan === q.id ? 'hide' : 'show'} plain dimColor
                onPress={() => update($, reviewing, x => (x === q.id ? null : q.id))} />
            )}
          </Box>,
        )
      }
      if (closing && clockNow - closing.at < CLOSING_MS) {
        const c = closing
        const sweep = (t: number) => Math.min(1, Math.max(0, (t - c.at) / SWEEP_MS))
        if (blit) blit.set('closed-sweep', { columns: 8, rows: 1, draw: fr => progressCells(8, sweep(fr * FRAME_MS), mix(C.ok, C.accent2, 0.6), C.ok, null) })
        const facts = [
          c.proved !== null ? `${c.proved} criteri${c.proved === 1 ? 'on' : 'a'} proven` : '',
          c.minutes !== null ? elapsed(c.minutes * 60000) : '',
          c.usual !== undefined ? `usually ${about(c.usual)}` : '',
        ].filter(Boolean)
        return row(C.ok, `✔ ${c.id} done${closeCard(c)}${facts.length ? ` · ${facts.join(' · ')}` : ''}${c.title ? ` · ${c.title}` : ''}`,
          <Box key="attention-sweep" flexShrink={0}>{meter(ui, e, 'closed-sweep', 8, cfg.motion === 'off' ? 1 : sweep(clockNow), C.ok, null)}</Box>)
      }
      if (failing) return row(C.err, `✗ gates failing: ${checks!.results.filter(r => r.exit).map(r => r.cmd).join(' · ')}`)
      if (doneSince.length) return row(C.ok, `✔ since your last message: ${doneSince.length} done · ${doneSince.slice(-6).join(' ')}`)
      const sl = signalLine(v) // T-0472: usage ahead of pace, tasks blocked …: the band's glyph, here while the pane is open
      if (sl) return row(sl.level === 'red' ? C.err : C.warn, `${sl.level === 'red' ? '●' : '◐'} ${sl.text}`)
      return row(C.dim, '✓ nothing needs you')
    })()

    // ── the task: its plan, rail, steps around the current one, what proves it; a plan waiting for a yes; or recent news
    const fit = <T,>(xs: T[], k: number, at: number) => {
      if (xs.length <= k) return xs
      const s = Math.max(0, Math.min(xs.length - k, at - 1)) // one done step stays in view above the current
      return xs.slice(s, s + k)
    }
    const planQ = plans.find(q => q.id === shownPlan) ?? (a ? undefined : plans[0])
    let task: { label: string; color: number; detail: string; body: RenderElement[]; tall?: number }
    if (planQ) {
      const p = planQ.plan
      task = {
        label: 'Plan',
        color: C.warn,
        detail: `${planQ.id} waits for your yes`,
        body: [
          <Text key="plan-title" weight="bold" wrap="truncate-end">{planQ.title}</Text>,
          ...(p.interpretation ? [<Text key="plan-means" wrap="truncate-end"><Text color={dim}>means </Text>{p.interpretation}</Text>] : []),
          ...(p.approach ? [<Text key="plan-approach" wrap="truncate-end"><Text color={dim}>approach </Text>{p.approach}</Text>] : []),
          ...p.steps.map(s => <Text key={`plan-step-${s.n}`} wrap="truncate-end">○ {s.n}. {s.text}</Text>),
          ...p.criteria.map(c => <Text key={`plan-ac-${c.n}`} color={dim} wrap="truncate-end">○ AC{c.n} {c.text}</Text>),
        ],
      }
    } else if (a) {
      const railRows = stageIdx >= 0 && L.task >= 8 ? 2 : 0
      const left = a.blockers.filter(x => !/^(step \d+ not done|acceptance criterion \d+ not checked)/.test(x)) // the ○ marks say those
      const extras: RenderElement[] = [
        // T-0711 the parts fm task split made; T-0228 the debugging ledger, the oracle, a batch; T-0261 runs that proved nothing
        ...(a.children ?? []).map(k => (
          <Text key={`kid-${k.id}`} color={k.status === 'done' ? dim : k.status === 'active' ? hex(C.accent) : undefined} wrap="truncate-end">
            {k.status === 'done' ? '✓' : k.status === 'active' ? '▸' : '○'} part {k.id} {k.title}
            {k.steps_total ? `  ${k.steps_done}/${k.steps_total}` : ''}
          </Text>
        )),
        ...(a.hypotheses ?? []).map(hy => (
          <Text key={`hyp-${hy.n}`} color={hex(hy.status === 'confirmed' ? C.ok : hy.status === 'ruled out' ? C.dim : C.warn)} wrap="truncate-end">
            {hy.status === 'confirmed' ? '✓' : hy.status === 'ruled out' ? '✗' : '?'} H{hy.n}. {hy.text}
          </Text>
        )),
        ...(a.oracle
          ? [
              <Text key="fm-pane-oracle" color={hex(a.oracle.ambiguities.length ? C.warn : C.dim)} wrap="truncate-end">
                oracle: {a.oracle.examples} example{a.oracle.examples === 1 ? '' : 's'}
                {a.oracle.ambiguities.length ? ` · open: ${a.oracle.ambiguities[0]}` : ' · no open questions'}
              </Text>,
            ]
          : []),
        ...((a.batch ?? []).length ? [<Text key="fm-pane-batch" color={dim} wrap="truncate-end">batch of {(a.batch ?? []).join(', ')}</Text>] : []),
        ...((a.inconclusive ?? 0) > 0
          ? [<Text key="fm-pane-inconclusive" color={hex(C.warn)} wrap="truncate-end">≈ {a.inconclusive} inconclusive run{a.inconclusive === 1 ? '' : 's'}: a sharper check is next</Text>]
          : []),
        ...((a.unverified ?? []).length
          ? [<Text key="fm-pane-unverified" color={dim} wrap="truncate-end">? {(a.unverified ?? []).length} unverified assumption{(a.unverified ?? []).length === 1 ? '' : 's'}: {(a.unverified ?? [])[0]}</Text>]
          : []),
        ...(left.length ? [<Text key="fm-pane-blockers" color={dim} wrap="truncate-end">left before done: {left.join(' · ')}</Text>] : []),
      ]
      const crit = a.criteria.map(c => (
        <Text key={`ac-${c.n}`} color={c.checked ? hex(C.ok) : undefined} wrap="truncate-end">
          {c.checked ? '✓' : '○'} AC{c.n} {c.text}
          {!c.checked && c.verify ? <Text color={soft}>{`  ↳ ${c.verify}`}</Text> : null}
        </Text>
      ))
      const room = Math.max(0, L.task - railRows)
      const nSteps = Math.min(a.steps.length, Math.max(Math.min(3, a.steps.length), room - crit.length - extras.length))
      const nCrit = Math.min(crit.length, Math.max(0, room - nSteps))
      const at = Math.max(0, a.steps.findIndex(s => s.current))
      task = {
        label: 'Task',
        color: C.accent,
        tall: railRows ? 1 : 0, // the rail: its raster and its labels
        detail: [
          `${proved}/${a.criteria.length} proved`,
          ...(a.audits.need ? [`audits ${a.audits.done}/${a.audits.need}`] : []),
          ...(a.steps.length - nSteps + crit.length - nCrit > 0 ? [`${a.steps.length - nSteps + crit.length - nCrit} more not shown`] : []),
        ].join(' · '),
        body: [
          ...(railRows ? [<Box key="fm-pane-rail" flexDirection="column">{rail(ui, e, a.stages, stageIdx, W, ft, blit)}</Box>] : []),
          ...fit(a.steps, nSteps, at).map(s => {
            const lit = flashed.get(`${a.id}:${s.n}`)
            const k = lit === undefined ? 1 : (clockNow - lit) / FLASH_MS
            return (
              <Text key={`step-${s.n}`} wrap="truncate-end"
                color={s.current ? hex(C.accent) : s.done ? hex(k < 1 ? C.ok : C.dim) : undefined}
                backgroundColor={k < 1 ? hex(mix(mix(C.ok, BG, 0.62), BG, k)) : undefined}>
                {s.done ? '✓' : s.current ? (moving ? spin(f ?? 0) : '▸') : '○'} {s.n}. {s.text}
              </Text>
            )
          }),
          ...crit.slice(0, nCrit),
          ...extras,
        ],
      }
    } else {
      const recent = [...(v.recent ?? [])].reverse()
      task = {
        label: 'Recent',
        color: C.dim,
        detail: recent.length ? 'newest first' : 'nothing yet',
        body: recent.map((line, i) => {
          const [, time, rest] = /^(\d\d:\d\d)\s+(.*)$/.exec(line) ?? [null, '', line]
          return (
            <Text key={`r-${i}`} color={hex(fade(Math.max(0, L.task - 1 - i), L.task, 0xc8ccd4))} wrap="truncate-end">
              {time ? <Text color={dim}>{`${time} `}</Text> : null}
              {rest}
            </Text>
          )
        }),
      }
    }

    // ── live: tool calls, subagents and background shells, one row each
    const runningSubs = subs.filter(s => !s.done)
    const liveRows: RenderElement[] = [
      ...nowCalls.map(([id, x], i) => {
        if (x.icon === '⚠')
          return (
            <Text key={`now-${id}`} color={hex(C.warn)} wrap="truncate-end">
              ⚠ {x.verb} · {elapsed(clockNow - x.at)}
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
              <Text color={dim}>{elapsed(clockNow - x.at)}</Text>
            </Box>
          </Box>
        )
      }),
      ...[...runningSubs, ...subs.filter(s => s.done)].map(s => (
        <Box flexDirection="row" gap={1} key={`agent-${s.id}`}>
          <Text color={hex(s.done ? C.dim : agentColor(s.id))}>{s.done ? '✓' : spin((f ?? 0) + s.tools)}</Text>
          <Box flexShrink={0}>
            <Text weight="bold" color={hex(s.done ? C.dim : C.agent)}>
              {s.type}
            </Text>
          </Box>
          <Text wrap="truncate-end" color={s.done ? dim : undefined}>
            {s.description}
          </Text>
          <Box flexShrink={0}>
            <Text color={hex(!s.done && clockNow - (s.lastAt ?? s.startedAt) >= QUIET_MS ? C.warn : C.dim)}>
              {s.done
                ? `done · ${s.tools} tool${s.tools === 1 ? '' : 's'}` // its last action is stale once it ends (T-0146)
                : clockNow - (s.lastAt ?? s.startedAt) >= QUIET_MS
                  ? `quiet ${elapsed(clockNow - (s.lastAt ?? s.startedAt))}`
                  : `${s.tools} tools${s.last ? ` · ${s.last.slice(0, 30)}` : ''} · ${elapsed(clockNow - s.startedAt)}`}
            </Text>
          </Box>
          {!s.done && clockNow - (s.lastAt ?? s.startedAt) >= STOP_MS && (
            <Button key={`stop-${s.id}`} label="■ stop" plain onPress={() => void stopAgent($, s.id)} />
          )}
        </Box>
      )),
      ...bgShells.map((x, i) => (
        <Box flexDirection="row" gap={1} key={`shell-${x.id}`}>
          <Text color={hex(C.accent2)}>{spin(fb + i)}</Text>
          <Text color={hex(C.accent2)}>◷</Text>
          <Text wrap="truncate-end">{x.command}</Text>
          <Box flexShrink={0}>
            <Text color={dim}>{elapsed(clockNow - x.startedAt)}</Text>
          </Box>
        </Box>
      )),
    ]
    const nLive = nowCalls.filter(([, x]) => x.icon !== '⚠').length + runningSubs.length + bgShells.length
    const lastTick = ticks.at(-1)
    if (!liveRows.length)
      liveRows.push(
        <Text key="live-idle" color={dim} wrap="truncate-end">
          {lastTick ? `quiet · last tool call ${since(clockNow - lastTick.at)}` : 'quiet · no tool calls yet'}
        </Text>,
      )

    // ── pulse: 14 days of closed tasks beside the gauges, and the session's tool calls
    const leftW = days.length ? days.length * 2 - 1 : 0
    const gw = Math.max(6, Math.min(14, W - leftW - 2 - 8 - 20))
    const label7 = (s: string) => <Text color={dim}>{s.padEnd(7)}</Text>
    const ctxColor = cx ? (cx.percent >= CHECKPOINT_AT ? C.err : cx.percent >= 60 ? C.warn : C.ok) : C.dim
    const spendFrac = v.budget ? Math.min(1, v.budget.today_usd / Math.max(0.01, v.budget.caps.day)) : null
    const gauges = (
      <Box key="pulse-gauges" flexDirection="column" flexGrow={1} flexShrink={1}>
        <Box key="g-ctx" flexDirection="row" gap={1}>
          {label7('context')}
          {cx ? meter(ui, e, 'fm-pane-ctx', gw, cx.percent / 100, ctxColor, null) : null}
          <Text wrap="truncate-end">{cx ? `${Math.round(cx.percent)}%` : '–'}</Text>
        </Box>
        <Box key="g-spend" flexDirection="row" gap={1}>
          {label7('spend')}
          {spendFrac !== null ? meter(ui, e, 'fm-pane-spend', gw, spendFrac, spendFrac >= 0.9 ? C.warn : C.accent2, null) : null}
          <Text wrap="truncate-end" color={v.budget?.halved || v.budget?.subagents_paused ? hex(C.warn) : undefined}>
            {v.budget ? `$${v.budget.today_usd.toFixed(2)} of $${v.budget.caps.day.toFixed(0)}` : '–'}
          </Text>
        </Box>
        <Box key="g-hooks" flexDirection="row" gap={1}>
          {label7('hooks')}
          {(v.latency ?? []).length > 1 ? spark(ui, e, 'fm-latency', v.latency ?? [], gw) : null}
          <Text wrap="truncate-end" color={hex(v.health?.hook_errors ? C.err : C.dim)}>
            {v.health
              ? `p95 ${v.health.hook_p95_ms ?? '–'} ms · ${v.health.guard_blocks} block${v.health.guard_blocks === 1 ? '' : 's'}${v.health.hook_errors ? ` · ${v.health.hook_errors} error${v.health.hook_errors === 1 ? '' : 's'}` : ''}`
              : '–'}
          </Text>
        </Box>
        <Box key="g-gates" flexDirection="row" gap={1}>
          {label7('gates')}
          <Text wrap="truncate-end">
            {(checks?.results ?? []).map((r, i) => (
              <Text key={`gate-${i}`} color={hex(r.exit ? C.err : r.note ? C.warn : C.ok)}>
                ●
              </Text>
            ))}
            <Text color={hex(failing ? C.err : C.dim)}>
              {checks?.results.length
                ? ` ${passed}/${checks.results.length} · ${checks.at.slice(11, 16)} · a full run ≈ ${elapsed(1000 * checks.results.reduce((t, r) => t + r.s, 0))}`
                : 'none yet: fm check'}
            </Text>
          </Text>
        </Box>
      </Box>
    )
    const spanMs = Math.ceil(Math.min(TIMELINE_MS, Math.max(60000, ticks.length ? clockNow - ticks[0]!.at : TIMELINE_MS)) / 60000) * 60000
    const recentTicks = ticks.filter(t => clockNow - t.at <= spanMs)
    const toolW = Math.max(8, W - 8 - 24)
    const pulseRows: RenderElement[] = [
      <Box key="pulse-top" flexDirection="row" gap={2} height={4} overflow="hidden">
        {days.length > 0 && (
          <Box key="pulse-days" flexDirection="column" flexShrink={0}>
            {bars(ui, e, 'done-days', days, 3, C.accent2, C.ok)}
            <Text color={dim} wrap="truncate-end">
              {`${v.today_done ?? 0} today · ${days.reduce((x, y) => x + y, 0)}/14d`.slice(0, Math.max(1, leftW))}
            </Text>
          </Box>
        )}
        {gauges}
      </Box>,
    ]
    if (L.pulse >= 5) // the tool-call sparkline only when the charts have their four rows besides
      pulseRows.push(
        <Box key="pulse-tools" flexDirection="row" gap={1}>
          {label7('tools')}
          {spark(ui, e, 'fm-tools', bucketize(recentTicks.map(t => t.at), clockNow, spanMs, toolW), toolW)}
          <Text color={dim} wrap="truncate-end">{`${recentTicks.length} call${recentTicks.length === 1 ? '' : 's'} · ${spanMs / 60000}m`}</Text>
        </Box>,
      )

    // ── the queue, then the inbox; a line to capture into it
    const capture = captureBox($, e)
    const queueRows: RenderElement[] = [
      ...(capture ? [capture] : []),
      ...queue.map((q, i) => (
        <Box flexDirection="row" gap={1} key={`q-${q.id}`}>
          <Box flexShrink={0}>
            <Text color={hex(i === 0 ? C.accent2 : C.dim)}>{i === 0 ? '▶' : `${i + 1}.`}</Text>
          </Box>
          {chip(q)}
          {q.steps_total ? meter(ui, e, `q-bar-${q.id}`, 6, (q.steps_done ?? 0) / q.steps_total, C.ok, null) : null}
          <Text wrap="truncate-end" color={q.waits ? hex(C.warn) : i === 0 ? undefined : hex(mix(C.dim, 0xc8ccd4, 0.6))}>
            {q.id} {q.title}
            {q.waits ? `  (${q.waits})` : ''}
          </Text>
          {q.plan && (
            <Button key={`approve-${q.id}`} label="✓ approve" plain onPress={() => act($, ['task', 'set', q.id, 'approved=true'], `✓ ${q.id} plan approved`)} />
          )}
          {v.typical?.[`${q.type}/${q.tier}`] !== undefined && (
            <Box key={`q-typ-${q.id}`} flexShrink={0}>
              <Text color={dim}>{about(v.typical[`${q.type}/${q.tier}`]!)}</Text>
            </Box>
          )}
        </Box>
      )),
      ...inbox.map(it => (
        <Box flexDirection="row" gap={1} key={`in-${it.id}`}>
          <Text color={dim}>⚑</Text>
          {chip(it)}
          <Text wrap="truncate-end">
            {it.id} {it.title}
          </Text>
          {it.age_days !== undefined && (
            // T-0228: the title gives way, never the age
            <Box flexShrink={0} key={`in-age-${it.id}`}>
              <Text color={dim}>{ago(it.age_days)}</Text>
            </Box>
          )}
          <Button key={`start-${it.id}`} label="▸ start" plain dimColor
            onPress={() => void $.prompt.submit({ text: `Plan and start ${it.id} (/foreman:intake).`, asUser: true })} />
          <Button key={`drop-${it.id}`} label="✕ drop" plain dimColor
            onPress={() => act($, ['task', 'drop', it.id, 'dropped from the Foreman pane'], `${it.id} dropped`)} />
        </Box>
      )),
      ...(inboxN > inbox.length ? [<Text key="in-more" color={dim}>{`… ${inboxN - inbox.length} more in the inbox`}</Text>] : []),
    ]
    const spare = L.queue - queueRows.length - 1
    if (a && spare >= 2 && (v.recent ?? []).length)
      queueRows.push(
        <Text key="q-recent" wrap="truncate-end">
          <Text color={soft}>recent </Text>
          <Text color={hex(C.track)}>{'─'.repeat(Math.max(0, W - 7))}</Text>
        </Text>,
        ...[...(v.recent ?? [])].reverse().slice(0, spare).map((line, i) => (
          <Text key={`q-r-${i}`} color={hex(fade(Math.max(0, spare - 1 - i), spare, 0xa0a4ac))} wrap="truncate-end">
            {line}
          </Text>
        )),
      )

    // ── more: one line each, the most useful first, as many as the room holds
    const one = (key: string, word: string, color: number, text: string, textColor: number = C.dim) => (
      <Box key={key} flexDirection="row">
        <Text wrap="truncate-end">
          <Text weight="bold" color={hex(color)}>{word.padEnd(9)}</Text>
          <Text color={hex(textColor)}>{text}</Text>
        </Text>
      </Box>
    )
    const fleet = v.fleet ?? []
    const sk = v.skills // T-0939
    const skillUses = Object.values(sk?.counts ?? {}).reduce((x, y) => x + y, 0)
    const topSkills = Object.entries(sk?.counts ?? {}).sort((x, y) => y[1] - x[1]).slice(0, 4)
    const b = v.budget
    const bs = v.brainstorm
    const moreRows: RenderElement[] = [
      // T-0711: every live session here, one steer for all; one session alone is this one, already above
      ...(fleet.some(s => s.remote || s.error) || fleet.length > 1
        ? [
            one('more-fleet', 'fleet', C.agent, fleet
              .map(s => s.error ? `! ${s.error}` : `${s.remote ? s.remote.toUpperCase() : s.session.slice(0, 8)} ${s.project ?? '-'} ${s.task ?? 'idle'} ${s.context_pct ?? '?'}%${s.mail ? ` ✉${s.mail}` : ''}`)
              .join(' · ')),
            ...(e.surface !== 'mobile'
              ? [<Input key="steer" placeholder="↯ steer every session… (Enter)" submitLabel="Steer" onSubmit={text => void steer($, text)} />]
              : []),
          ]
        : []),
      ...(v.revisit ?? []).slice(0, 1).map(rv =>
        one('more-revisit', 'revisit', C.warn, `${rv.decision} (${rv.why})${(v.revisit ?? []).length > 1 ? ` · ${(v.revisit ?? []).length - 1} more` : ''}`, C.warn)),
      ...((v.vetoes ?? []).length
        ? [one('more-vetoes', 'you said', C.accent, `${v.vetoes![0]}${v.vetoes!.length > 1 ? ` · ${v.vetoes!.length - 1} more` : ''}`)]
        : []),
      ...(mine.length
        ? [one('more-files', 'files', C.edit, `${mine.length} this session · +${mine.reduce((n, t) => n + t.add, 0)} −${mine.reduce((n, t) => n + t.del, 0)} · ${mine.slice(-3).reverse().map(t => shortPath(t.path.slice(base.length), 28)).join(', ')}`)]
        : []),
      ...(b && (b.subagent_tokens > 0 || b.top.length || b.halved || b.subagents_paused)
        ? [one('more-spend', 'spend', C.accent2, [
            `subagents ${tokensWord(b.subagent_tokens)}`,
            ...b.top.slice(0, 3).map(t => `${t.feature} ${t.tokens ? tokensWord(t.tokens) : `$${t.usd.toFixed(2)}`}`),
            ...(b.halved ? [`caps halved: ${b.halved}`] : []),
            ...(b.subagents_paused ? [`waiting: ${b.subagents_paused}`] : []),
          ].join(' · '), b.halved || b.subagents_paused ? C.warn : C.dim)]
        : []),
      ...(sk && (sk.recent.length || sk.unread.length)
        ? [one('more-skills', 'skills', C.agent, [
            `${skillUses} use${skillUses === 1 ? '' : 's'} · 7d`,
            ...(sk.recent[0] ? [`last ${sk.recent[0].name} ${since(Math.max(0, clockNow - Date.parse(sk.recent[0].at)))}`] : []),
            ...(topSkills.length ? [`top ${topSkills.map(([n, k]) => `${n} ×${k}`).join(', ')}`] : []),
            ...(sk.unread.length ? [`${sk.unread.length} cards unread: fm lib show ${sk.unread[0]}`] : []),
          ].join(' · '))]
        : []),
      ...(bs
        ? [one('more-ideas', 'ideas', C.agent, bs.running
            ? `${spin(fb + clockNow / 300)} ${bs.answers}/${bs.expected ?? '?'} answers · ${bs.count} ideas so far${bs.ideas.length ? ` · latest: ${bs.ideas.at(-1)}` : ''}`
            : `${bs.count} ideas · ${bs.grounded ? 'grounded' : hoursAgo(bs.age_h ?? 0)} · fm research show ${bs.name}`)]
        : []),
      ...(v.bench?.last
        ? [one('more-bench', 'bench', C.agent, `${v.bench.last.passed}/${v.bench.last.total} passed · $${v.bench.last.cost_usd.toFixed(2)} · ${v.bench.last.label}${v.bench.last.score != null ? ` · judged ${v.bench.last.score}/5` : ''}`,
            v.bench.last.passed === v.bench.last.total ? C.dim : C.warn)]
        : []),
      ...(v.bench?.verdicts ?? []).slice(0, 1).map((x, i) => one(`more-verdict-${i}`, '', C.dim, `${x.ok ? '✓' : '✗'} ${x.kind}: ${x.verdict ?? ''}`, x.ok ? C.dim : C.warn)),
      ...(v.bench?.evolve ?? []).slice(0, 1).map((x, i) =>
        one(`more-evolve-${i}`, '', C.dim, `${x.kept ? '✓ kept' : '✗ dropped'} ${shortPath(x.target ?? '', 34)} · ${x.why ?? ''}`)),
      ...(v.research ?? []).slice(0, 1).map(r =>
        one(`more-research-${r.name}`, 'research', C.accent2, `${(v.research ?? []).length > 1 ? `${(v.research ?? []).length} asks, newest ` : ''}${r.name.replace(/^ask-/, '').replace(/-\d{8}-\d{4}$/, '')} · ✓${r.verified} ✗${r.not_found} ?${r.unchecked}${(r.conflicts ?? 0) > 0 ? ` · ⟷${r.conflicts} conflicts` : ''}${(r.single ?? 0) > 0 ? ` · ${r.single} single-source` : ''}`,
          r.not_found ? C.warn : C.dim)),
    ]

    return (
      <Box flexDirection="column" key="fm-pane" paddingX={1}>
        {header}
        {attention}
        {section('task', L.task, task.label, task.color, task.detail, task.body, task.tall ?? 0)}
        {section('live', L.live, 'Live', nLive ? C.accent : C.dim, nowCalls.length + subs.length + bgShells.length ? `${nLive} running` : 'quiet', liveRows)}
        {section('pulse', L.pulse, 'Pulse', C.accent2, '', pulseRows, 3)}
        {section('queue', L.queue, 'Queue', C.accent2, `${queue.length} queued · ${inboxN} in inbox`, queueRows)}
        {section('more', L.also, 'More', C.dim, '', moreRows.length ? moreRows : [<Text key="more-none" color={dim}>nothing else to show</Text>])}
        <Box flexDirection="row" gap={2} key="fm-pane-controls" height={1} overflow="hidden" flexShrink={0}>
          <Button key="next" label="next" hotkey="n" plain onPress={() => void $.prompt.submit({ text: '/foreman:next', asUser: true })} />
          <Button key="drive" label={m?.drive ? 'turn drive off' : 'turn drive on'} hotkey="d" plain
            onPress={() => act($, ['drive', m?.drive ? 'off' : 'on'], `drive ${m?.drive ? 'off' : 'on'}`)} />
          <Button key="autonomy" label={m?.autonomy === 'full' ? 'switch to standard' : 'switch to full auto'} plain dimColor
            onPress={() => {
              const level = m?.autonomy === 'full' ? 'standard' : 'full'
              return act($, ['autonomy', level], `autonomy ${level}`)
            }} />
          <Button key="sound" label={isOn ? 'mute' : 'unmute'} plain dimColor
            onPress={async () => {
              await update($, sound, x => !x)
              await $.store.set('sound', await read($, sound))
            }} />
          <Button key="refresh" label="refresh" hotkey="r" plain dimColor onPress={() => refresh($)} />
        </Box>
      </Box>
    )
  })
}
