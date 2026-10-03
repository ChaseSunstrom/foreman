import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, ResolveInput } from 'claude-code'

import type { FileChurn, FmItem, FmView, LastOutput, LiveAgent, LiveShell, TurnSummary } from '../types'
import {
  C,
  MASCOT_COLORS,
  SIZE_LEGEND,
  about,
  activityCells,
  agentColor,
  TONE_COLOR,
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

// Foreman inside Claude Code. A pure renderer over `fm ui --json` plus what the session's own tool calls show it:
// every rule and gate stays in fm and its classic hooks (which still run under claude -p and older builds); buttons
// only run fm commands or submit a prompt the person pressed for. While work is live a frame clock animates the band,
// the cards and every running tool row; a finished row goes back to the engine, which draws its result as always.
const PANE = 'foreman'
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
const output = atom({ plugin: 'foreman-ui', key: 'output' } as const, null as LastOutput | null)

const LIST = 6
const OUT_LINES = 40 // the pane's Output card: the last lines of the last command
const FRAME_MS = 120
const IDLE_FRAMES = Math.round((15 * 60 * 1000) / FRAME_MS) // a lost turn.complete stops the clock after 15 min
const QUIET_MS = 2 * 60 * 1000 // a running subagent with no tool call this long shows how long it has been quiet
const STOP_MS = 10 * 60 * 1000 // and from here offers Stop
const SHELL_MAX_MS = 2 * 3600 * 1000 // a background command runs at most 2 h; past that its notice was lost
const CHECKPOINT_AT = 85 // context percent at which Foreman checkpoints once, so a compaction resumes exactly
const FRESH = [
  'Foreman task boundary: a task just closed.',
  "Keep: the user's standing requests and preferences, decisions still in force, and what the next queued task needs.",
  "Drop: finished tasks' file contents, diffs, logs and back-and-forth.",
  "Foreman's record (fm state, the briefs) is the source of truth for tasks: after this, check `fm next` and re-read",
  'files before editing them, since what was read earlier may be out of date.',
].join(' ')

/** What changed between two snapshots that deserves a toast. */
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
    if (open.has(c.id)) out.push(c.status === 'done' ? `✔ ${c.id} done` : `${c.id} ${c.status}`)
  }
  const asked = new Set((prev.approvals ?? []).map(x => `${x.task}:${x.allow.join(',')}`))
  for (const x of next.approvals ?? []) {
    if (!asked.has(`${x.task}:${x.allow.join(',')}`)) out.push(`⚠ ${x.task} needs your yes: ${x.allow.join(', ')}`)
  }
  return out
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
  return (text.split('\n').map(l => l.trim()).filter(Boolean).at(-1) ?? '').slice(0, 100)
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
let freshAt = 40 // userConfig: compact at a task boundary from this context percent (0: never)
let mascot = 'blue' // userConfig: the pane's mascot color, or off
let happyUntil = 0 // the mascot jumps for a few seconds after a task closes
let bgLive = 0 // background shells still running: the clock keeps a calm pace for the waiting row
let calm = 0
const turns = new Set<string>()
const starts = new Map<string, number>() // tool_use_id → when it started (ms)
const agentCalls = new Map<string, string>() // running Agent call → its description
const agentOf = new Map<string, string>() // running Agent call → the subagent's id
let turn = { tools: 0, edits: 0, add: 0, del: 0, agents: 0, stepsDone: -1, task: '' }

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
  if (mascot !== 'off') await update($, beat, n => n + 1) // the mascot's idle blink, at the poll's pace
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

// A task just closed: with the context past freshAt, compact so the next task starts on what still matters (T-0098).
async function freshen($: EngineInterface) {
  if (!freshAt) return
  const percent = (await $.session.usage().catch(() => null))?.context.percent
  if (typeof percent !== 'number' || percent < freshAt) return
  $.ui.toast(`Task closed at context ${Math.round(percent)}% · compacting so the next task starts fresh`, { timeoutMs: 8000 })
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

async function openPane($: EngineInterface, focus: boolean) {
  // ~76 columns docked: the cards fit, and the transcript and band keep the rest (T-0122: the share left them ~37)
  return $.ui.open(focus ? { id: PANE, title: 'Foreman', focus: true, columns: 76 } : { id: PANE, title: 'Foreman', columns: 76 })
}

// The frame clock runs only while work is live: a turn, or a tool call (a subagent's included).
async function wake($: EngineInterface) {
  lastActive = await read($, frame)
  if (clock) return
  clock = $.clock.every(FRAME_MS, () => void advance($))
}

async function advance($: EngineInterface) {
  const f = await read($, frame)
  if (starts.size) lastActive = f // a long build is live work: its row keeps moving (finally always clears starts)
  const quiet = !turns.size && !starts.size
  if (quiet && !bgLive && f - lastActive > 2) return sleep()
  if (!bgLive && f - lastActive > IDLE_FRAMES) return sleep()
  if (quiet && bgLive && ++calm % 4) return // only background work: a calmer pace (~2 frames a second)
  await update($, frame, n => n + 1)
}

function sleep() {
  clock?.cancel()
  clock = null
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

/** A bar: a true-color Raster on the terminal, its text twin elsewhere. `fraction` null draws an activity comet. */
function meter(
  $: EngineInterface,
  e: ResolveInput,
  key: string,
  width: number,
  fraction: number | null,
  color: number,
  f: number | null,
) {
  if (e.surface === 'terminal') {
    const { Raster } = $.ui.resolve(e)
    const cells =
      fraction === null ? activityCells(width, color, f ?? 0) : progressCells(width, fraction, mix(color, C.accent2, 0.6), color, f)
    return <Raster key={key} columns={width} rows={1} cells={cells} />
  }
  const { Box, Text } = $.ui.resolve(e)
  if (fraction === null) {
    const [a, b, c] = textComet(width, f ?? 0)
    return (
      <Box key={key} flexDirection="row">
        <Text color={hex(C.track)}>{a}</Text>
        <Text color={hex(color)}>{b}</Text>
        <Text color={hex(C.track)}>{c}</Text>
      </Box>
    )
  }
  const [done, rest] = textBar(width, fraction)
  return (
    <Box key={key} flexDirection="row">
      <Text color={hex(color)}>{done}</Text>
      <Text color={hex(C.track)}>{rest}</Text>
    </Box>
  )
}

/** A sparkline (Raster on the terminal, block characters elsewhere) and a lines-added/removed bar. */
function spark($: EngineInterface, e: ResolveInput, key: string, values: readonly number[], width: number) {
  if (e.surface === 'terminal') {
    const { Raster } = $.ui.resolve(e)
    return <Raster key={key} columns={width} rows={1} cells={sparkCells(values, width)} />
  }
  const { Text } = $.ui.resolve(e)
  return <Text color={hex(C.accent2)}>{sparkText(values, width)}</Text>
}

function churn($: EngineInterface, e: ResolveInput, key: string, f: FileChurn, max: number) {
  if (e.surface === 'terminal') {
    const { Raster } = $.ui.resolve(e)
    return <Raster key={key} columns={10} rows={1} cells={churnCells(f.add, f.del, max, 10)} />
  }
  const { Text } = $.ui.resolve(e)
  return <Text color={hex(C.ok)}>{'━'.repeat(Math.max(1, Math.round((10 * (f.add + f.del)) / Math.max(1, max))))}</Text>
}

/** The mascot: Claude Code's own Claude, dancing while work runs, with a mini Claude per running subagent. */
function mascotTree($: EngineInterface, e: ResolveInput, state: 'work' | 'idle' | 'happy', n: number, subs: LiveAgent[]) {
  if (mascot === 'off') return null
  const color = MASCOT_COLORS[mascot] ?? MASCOT_COLORS.blue!
  const { Box, Text } = $.ui.resolve(e)
  if (e.surface !== 'terminal')
    return <Text color={hex(color)}>{state === 'work' ? (n % 2 ? '(•̀ᴗ•́)و' : '(•̀ᴗ•́)ง') : state === 'happy' ? '\\(^ᴗ^)/' : '(•ᴗ•)'}</Text>
  const running = subs.filter(s => !s.done)
  return (
    <Box key="fm-mascot" flexDirection="row" alignItems="flex-end" gap={1}>
      {running.length > 4 && <Text color={hex(C.dim)}>+{running.length - 4}</Text>}
      {running.slice(0, 4).map((s, i) => (
        <Box key={`mini-${s.id}`} flexDirection="column">
          {miniClawd(Math.floor(n / 4) + i).map((row, j) => (
            <Text key={`mini-${s.id}-${j}`} color={hex(agentColor(s.id))}>
              {row}
            </Text>
          ))}
        </Box>
      ))}
      <Box flexDirection="column">
        {clawd(state, n).map((row, j) => (
          <Text key={`clawd-${j}`} color={hex(color)}>
            {row}
          </Text>
        ))}
      </Box>
    </Box>
  )
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
  freshAt = typeof options.freshAt === 'number' ? options.freshAt : 40
  mascot = typeof options.mascot === 'string' && (options.mascot === 'off' || options.mascot in MASCOT_COLORS) ? options.mascot : 'blue'
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'fm', description: 'Foreman: open or close the dashboard pane' })
    await $.command.register({
      name: 'fm-trust',
      description: 'Foreman: let Claude edit the guard and Claude Code settings (on | off); works only when you type it',
    })
    const stored = await $.store.get('sound').catch(() => undefined)
    if (stored === false) await update($, sound, () => false)
    await refresh($)
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
    turns.add(e.turnId)
    const a = (await read($, view))?.active
    turn = { tools: 0, edits: 0, add: 0, del: 0, agents: 0, stepsDone: a ? a.steps.filter(s => s.done).length : -1, task: a?.id ?? '' }
    await wake($)
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    turns.delete(e.turnId)
    isDirty = true
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
    const face = toolFace(String(e.tool), e)
    starts.set(id, await $.clock.now())
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
      else if (face.add !== undefined && r.deny === undefined && !r.isError) await noteEdit($, face.target, face.add, face.del ?? 0)
      const bg = (r.result as { backgroundTaskId?: unknown } | undefined)?.backgroundTaskId
      if (e.tool === 'Bash' && typeof bg === 'string' && !e.agentId) {
        const startedAt = await $.clock.now()
        const command = String(e.command).split('\n')[0]!.slice(0, 120)
        await noteShells($, list => [...list.filter(x => x.id !== bg), { id: bg, command, startedAt }])
      }
      const res = r.result as { stdout?: unknown; stderr?: unknown; backgroundTaskId?: unknown } | undefined
      if (e.tool === 'Bash' && !e.agentId && !fmCommand(e.command) && res && typeof res.stdout === 'string' && !bg) {
        const all = `${res.stdout}\n${typeof res.stderr === 'string' ? res.stderr : ''}`.replace(/\u001b\[[0-9;:]*[A-Za-z]/g, '')
        const lines = all.split('\n').filter(l => l.trim())
        const last: LastOutput = { command: String(e.command).split('\n')[0]!.slice(0, 160), lines: lines.slice(-200), total: lines.length, ok: !r.isError }
        await update($, output, () => last)
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
      starts.delete(id)
      agentCalls.delete(id)
      agentOf.delete(id)
      isDirty = true
    }
  })

  // T-0123: a finished shell command's output as a summary: how many lines, the ones that matter (failures first, else
  // the tail) in their colours, and where the rest is. An error keeps Claude Code's full text.
  on('ui.render', { component: 'ToolResult' }, async ($, e, next) => {
    if (e.props.tool !== 'Bash' || e.props.isErrored) return next(e)
    const o = (e.props.output ?? {}) as { stdout?: unknown; stderr?: unknown; interrupted?: boolean; backgroundTaskId?: unknown }
    const { Box, Text } = $.ui.resolve(e)
    if (typeof o.backgroundTaskId === 'string')
      return <Text color={hex(C.accent2)}>◷ running in the background · {o.backgroundTaskId}</Text>
    const s = outputSummary(o.stdout, o.stderr)
    if (!s.total) return <Text color={hex(C.dim)}>{o.interrupted ? '■ interrupted' : '✓ no output'}</Text>
    return (
      <Box flexDirection="column" key="fm-output">
        <Text color={hex(C.dim)}>
          <Text color={hex(s.failures ? C.err : C.ok)}>{s.failures ? '✗' : '✓'}</Text> {s.total} line{s.total === 1 ? '' : 's'}
          {s.more ? (s.failures ? ' · the failures' : ` · the last ${s.lines.length}`) : ''}
          {o.interrupted ? ' · interrupted' : ''}
        </Text>
        {s.lines.map((l, i) => (
          <Text key={`out-${i}`} color={hex(TONE_COLOR[l.tone])} wrap="truncate-end">
            {'  '}
            {l.text}
          </Text>
        ))}
        {s.more > 0 && <Text color={hex(C.dim)}>  … {s.more} more · /fm → Output</Text>}
      </Box>
    )
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
    const quiet = ['Read', 'WebFetch', 'WebSearch'].includes(e.props.tool)
    if (quiet && !e.props.isRunning && !e.props.isErrored && !e.props.isInterrupted) {
      const face = toolFace(e.props.tool, e.props.input)
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
    if (!e.props.isRunning || e.props.isErrored || e.props.isInterrupted) return next(e)
    const f = await read($, frame)
    const face = toolFace(e.props.tool, e.props.input)
    const since = starts.get(e.props.tool_use_id)
    const ms = since === undefined ? 0 : (await $.clock.now()) - since
    const agentId = agentOf.get(e.props.tool_use_id)
    const agent = agentId ? (await read($, agents)).find(a => a.id === agentId) : undefined
    const { Box, Text } = $.ui.resolve(e)
    const width = Math.max(30, e.viewport?.columns ?? 100)
    // T-0124: a brainstorm running inside this call shows its progress right here in the chat
    const ideasRun = e.props.tool === 'Bash' && /^ideas\b/.test(fmCommand((e.props.input as { command?: unknown } | null)?.command) ?? '')
    const bs = ideasRun ? (await read($, view))?.brainstorm : null

    const row = (
      <Box flexDirection="row" gap={1} key="fm-tool">
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
        {meter($, e, 'fm-tool-bar', 12, null, face.color, f)}
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

  // The working line keeps its animated word and gains the Foreman step it is on.
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    const a = (await read($, view))?.active
    const cur = a?.steps.find(s => s.current)
    if (!a || !cur) return next(e)
    const done = a.steps.filter(s => s.done).length
    return next({ ...e, props: { ...e.props, suffix: `… · ${a.id} step ${done + 1}/${a.steps.length}: ${cur.text}`.slice(0, 90) } })
  })

  // The line closing a turn says what the turn did.
  on('ui.render', { component: 'TurnDuration' }, async ($, e, next) => {
    const s = (await read($, summaries)).find(x => x.durationMs === e.props.durationMs)
    if (!s || !s.tools) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box flexDirection="row" gap={1} key="fm-turn">
        <Text dimColor>
          ✻ {e.props.word} for {elapsed(e.props.durationMs)}
        </Text>
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
    const idle = !a && !asks.length && !plans.length && !(v.queue ?? []).length && !(v.inbox_total ?? 0)
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
            {meter($, e, 'fm-band-bar', width, done / a.steps.length, C.ok, f)}
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
                <Text bold color={typeColor(a.type)}>
                  {a.type}
                </Text>
                <Text color={hex(C.dim)}>{sizeWord(a.tier)}</Text>
                <Text bold color={hex(C.accent)}>
                  {a.id}
                </Text>
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
            {c && meter($, e, 'fm-band-ctx', 6, c.percent / 100, c.percent >= CHECKPOINT_AT ? C.err : c.percent >= 60 ? C.warn : C.ok, null)}
            {c && <Text color={hex(C.dim)}>{Math.round(c.percent)}%</Text>}
            {m && <Text color={hex(m.autonomy === 'full' ? C.accent2 : C.dim)}>{m.autonomy === 'full' ? 'full auto' : 'standard'}</Text>}
            {m && !m.drive && <Text color={hex(C.warn)}>drive off</Text>}
          </Box>
        </Box>
        {a && (
          <Box flexDirection="row" gap={1}>
            {working && <Text color={hex(C.accent)}>{spin(f ?? 0)}</Text>}
            <Text color={hex(C.dim)}>{a.stage}</Text>
            {a.steps.length > 0 && meter($, e, 'fm-band-bar', width, done / a.steps.length, C.ok, f)}
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

    return (
      <Box flexDirection="column" borderStyle="round" borderColor={hex(working ? pulse(C.accent, f) : C.track)} paddingX={1} key="fm-band">
        {head}
        {(queued > 0 || inboxN > 0) && (
          <Box flexDirection="row" gap={1} key="fm-band-queue-row">
            {!narrow && <Text color={hex(C.dim)}>today</Text>}
            {!narrow && meter($, e, 'fm-band-queue', 10, todayDone / Math.max(1, todayDone + queued + inboxN + (a ? 1 : 0)), C.accent2, null)}
            <Text color={hex(C.dim)} wrap={cut}>
              ✓{todayDone} done · {queued} queued · {inboxN} in inbox
              {upNext && !narrow ? ` · next ${upNext.id} ${upNext.title}` : ''}
            </Text>
          </Box>
        )}
        {m?.trust && (
          <Text color={hex(C.warn)} wrap={cut} key="fm-band-trust">
            ⚠ trust on: Claude may edit the guard and Claude Code settings · /fm-trust off
          </Text>
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

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Button, Text } = $.ui.resolve(e)
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
    const f = live ? await read($, frame) : null
    const idleBeat = live || mascot === 'off' ? 0 : await read($, beat)
    const clockNow = await $.clock.now()
    const a = v.active
    const m = v.mode
    const width = Math.max(10, e.props.bodyColumns - 12)
    const touched = await read($, files)
    const subs = await read($, agents)
    const bgShells = await read($, shells)
    const lastOut = await read($, output)
    const fb = bgShells.length ? await read($, frame) : 0
    const isOn = await read($, sound)
    const queue = v.queue ?? []
    const inbox = v.inbox ?? []
    const recent = (v.recent ?? []).slice(-LIST)
    const checks = v.checks
    const card = (color: number) =>
      ({ flexDirection: 'column', borderStyle: 'round', borderColor: hex(pulse(color, f)), paddingX: 1 }) as const
    const head = (title: string, color: number, count?: string) => (
      <Box flexDirection="row" gap={1}>
        <Text bold color={hex(color)}>
          ▍{title}
        </Text>
        {count !== undefined && <Text color={hex(C.dim)}>{count}</Text>}
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
    const maxChurn = Math.max(1, ...touched.map(t => t.add + t.del))
    const passed = checks ? checks.results.filter(r => !r.exit).length : 0

    return (
      <Box flexDirection="column" key="fm-pane">
        <Box flexDirection="row" justifyContent="space-between">
          <Box flexDirection="column">
            <Box flexDirection="row" gap={1}>
              <Text bold color={hex(C.accent)}>
                {live ? spin(f ?? 0) : '▍'} Foreman
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
            <Text color={hex(C.dim)}>
              <Text color={hex(C.ok)}>✓ {v.today_done ?? 0}</Text> today · {queue.length} queued · {v.inbox_total ?? inbox.length} in inbox
            </Text>
          </Box>
          {mascotTree($, e, live ? 'work' : clockNow < happyUntil ? 'happy' : 'idle', live ? (f ?? 0) : idleBeat, subs)}
        </Box>
        {err && <Text color={hex(C.err)}>fm: {err}</Text>}

        <Box key="card-task" {...card(a ? C.accent : C.track)}>
          {a ? (
            <Box flexDirection="column">
              <Box flexDirection="row" gap={1}>
                {chip(a)}
                <Text bold color={hex(C.accent)}>
                  {a.id}
                </Text>
                <Text bold wrap="wrap">
                  {a.title}
                </Text>
              </Box>
              <Text wrap="wrap">
                {a.stages
                  .map(s => (s === a.stage ? `◉ ${s}` : a.stages.indexOf(s) < a.stages.indexOf(a.stage) ? `● ${s}` : `○ ${s}`))
                  .join('  ')}
              </Text>
              {a.steps.length > 0 && (
                <Box flexDirection="row" gap={1}>
                  {meter($, e, 'fm-pane-bar', Math.min(40, width - 8), done / a.steps.length, C.ok, f)}
                  <Text bold>
                    {done}/{a.steps.length}
                  </Text>
                </Box>
              )}
              {a.steps.map(s => (
                <Text key={`step-${s.n}`} color={s.current ? hex(C.accent) : s.done ? hex(C.dim) : undefined} wrap="truncate-end">
                  {s.done ? '✓' : s.current ? (live ? spin(f ?? 0) : '▸') : '○'} {s.n}. {s.text}
                </Text>
              ))}
              {a.criteria.map(c => (
                <Text key={`ac-${c.n}`} color={c.checked ? hex(C.ok) : undefined} wrap="truncate-end">
                  {c.checked ? '✓' : '○'} AC{c.n} {c.text}
                </Text>
              ))}
              <Text color={hex(C.dim)}>
                audits {'■'.repeat(a.audits.done)}
                {'□'.repeat(Math.max(0, a.audits.need - a.audits.done))} {a.audits.done}/{a.audits.need}
                {a.blockers.length ? ` · ${a.blockers.length} blocker(s) before done` : ''}
              </Text>
              <Text color={hex(mix(C.dim, C.track, 0.4))} wrap="truncate-end">
                sizes: {SIZE_LEGEND}
              </Text>
            </Box>
          ) : (
            <Text color={hex(C.dim)}>No active task.</Text>
          )}
          {v.next && (
            <Text color={hex(C.dim)} wrap="truncate-end">
              → {humanNext(v.next)}
            </Text>
          )}
        </Box>

        {(v.approvals ?? []).length > 0 && (
          <Box key="card-asks" {...card(C.warn)}>
            {head('Needs you', C.warn)}
            {(v.approvals ?? []).map(x => (
              <Text color={hex(C.warn)} wrap="wrap" key={`ask-${x.task}`}>
                ⚠ {x.task} · {x.allow.join(', ')}: {x.why}
              </Text>
            ))}
          </Box>
        )}

        {queue.flatMap(q => (q.plan ? [{ ...q, plan: q.plan }] : [])).map(q => (
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

        {subs.length > 0 && (
          <Box key="card-agents" {...card(C.agent)}>
            {head('Subagents', C.agent, `${subs.filter(s => !s.done).length} running`)}
            {subs.map(s => (
              <Box flexDirection="row" gap={1} key={`agent-${s.id}`}>
                <Text color={hex(s.done ? C.dim : C.agent)}>{s.done ? '✓' : spin((f ?? 0) + s.tools)}</Text>
                <Text bold color={hex(s.done ? C.dim : C.agent)}>
                  {s.type}
                </Text>
                <Text wrap="truncate-end" color={s.done ? hex(C.dim) : undefined}>
                  {s.description}
                </Text>
                <Text color={hex(C.dim)} wrap="truncate-end">
                  {s.tools} tools · {s.last.slice(0, 30)}
                  {!s.done ? ` · ${elapsed(clockNow - s.startedAt)}` : ''}
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
          <Box key="card-shells" {...card(C.accent2)}>
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

        {v.brainstorm && (
          <Box key="card-brainstorm" {...card(v.brainstorm.running ? C.agent : C.track)}>
            {head(
              'Brainstorm',
              C.agent,
              v.brainstorm.running
                ? `${spin(fb + clockNow / 300)} ${v.brainstorm.answers}/${v.brainstorm.expected ?? '?'} answers · ${v.brainstorm.count} ideas so far`
                : `${v.brainstorm.count} ideas · ${v.brainstorm.name.replace('brainstorm-', '')}`,
            )}
            {v.brainstorm.ideas.map((idea, i) => (
              <Text key={`idea-${i}`} color={hex(fade(i, v.brainstorm!.ideas.length, /wild/i.test(idea) ? C.agent : 0xc8ccd4))} wrap="truncate-end">
                {/wild/i.test(idea) ? '✦' : '•'} {idea.replace(/^wild:\s*/i, '').replace(/\s*\(wild\)$/i, '')}
              </Text>
            ))}
          </Box>
        )}

        {lastOut && (
          <Box key="card-output" {...card(lastOut.ok ? C.track : C.err)}>
            {head('Output', lastOut.ok ? C.accent : C.err, `${lastOut.total} lines`)}
            <Text color={hex(C.accent)} wrap="truncate-end">
              $ {lastOut.command}
            </Text>
            {lastOut.total > OUT_LINES && <Text color={hex(C.dim)}>… {lastOut.total - OUT_LINES} earlier lines</Text>}
            {lastOut.lines.slice(-OUT_LINES).map((l, i) => (
              <Text key={`o-${i}`} color={hex(TONE_COLOR[tone(l)])} wrap="truncate-end">
                {l}
              </Text>
            ))}
          </Box>
        )}

        {touched.length > 0 && (
          <Box key="card-files" {...card(C.edit)}>
            {head('Files this session', C.edit, `${touched.length}`)}
            {touched
              .slice(-LIST)
              .reverse()
              .map((t, i) => (
                <Box flexDirection="row" gap={1} key={`file-${i}`}>
                  {churn($, e, `file-bar-${i}`, t, maxChurn)}
                  <Text color={hex(C.ok)}>+{t.add}</Text>
                  <Text color={hex(C.err)}>−{t.del}</Text>
                  <Text wrap="truncate-start">{shortPath(t.path, 40)}</Text>
                </Box>
              ))}
          </Box>
        )}

        <Box key="card-queue" {...card(queue.some(q => q.waits) ? C.warn : C.accent2)}>
          {head('Queue', C.accent2, `${queue.length}`)}
          {queue.length === 0 && <Text color={hex(C.dim)}>empty</Text>}
          {queue.slice(0, LIST).map((q, i) => (
            <Box flexDirection="row" gap={1} key={`q-${q.id}`}>
              <Text color={hex(fade(LIST - 1 - i, LIST, C.accent2))}>{i + 1}.</Text>
              {chip(q)}
              {q.steps_total ? meter($, e, `q-bar-${q.id}`, 6, (q.steps_done ?? 0) / q.steps_total, C.ok, null) : null}
              {v.typical?.[`${q.type}/${q.tier}`] !== undefined && (
                <Text color={hex(C.dim)}>{about(v.typical[`${q.type}/${q.tier}`]!)}</Text>
              )}
              <Text wrap="truncate-end" color={q.waits ? hex(C.warn) : undefined}>
                {q.id} {q.title}
                {q.waits ? `  (${q.waits})` : ''}
              </Text>
            </Box>
          ))}
        </Box>

        <Box key="card-inbox" {...card(C.accent)}>
          {head('Inbox', C.accent, `${v.inbox_total ?? inbox.length}`)}
          {captureBox($, e)}
          {inbox.slice(0, LIST).map(it => (
            <Box flexDirection="row" gap={1} key={`in-${it.id}`}>
              {chip(it)}
              <Text wrap="truncate-end">
                {it.id} {it.title}
              </Text>
              {it.age_days !== undefined && <Text color={hex(C.dim)}>{ago(it.age_days)}</Text>}
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
        </Box>

        {checks && checks.results.length > 0 && (
          <Box key="card-gates" {...card(passed === checks.results.length ? C.ok : C.err)}>
            {head(
              'Gates',
              passed === checks.results.length ? C.ok : C.err,
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
        )}

        <Box key="card-activity" {...card(C.dim)}>
          {head('Activity', C.dim)}
          {recent.map((line, i) => (
            <Text color={hex(fade(i, recent.length))} wrap="truncate-end" key={`r-${i}`}>
              {line}
            </Text>
          ))}
          {v.health && (
            <Box flexDirection="row" gap={1}>
              <Text color={hex(C.dim)}>hooks</Text>
              {(v.latency ?? []).length > 1 && spark($, e, 'fm-latency', v.latency ?? [], 24)}
              <Text color={hex(v.health.hook_errors ? C.err : C.dim)}>
                p95 {v.health.hook_p95_ms ?? '–'} ms · guard blocks {v.health.guard_blocks}
                {v.health.hook_errors ? ` · ${v.health.hook_errors} hook error(s)` : ''}
              </Text>
            </Box>
          )}
        </Box>

        <Box flexDirection="row" gap={2}>
          <Button
            key="next"
            label="next"
            hotkey="n"
            plain
            onPress={() => void $.prompt.submit({ text: '/foreman:next', asUser: true })}
          />
          <Button
            key="drive"
            label={m?.drive ? 'drive off' : 'drive on'}
            hotkey="d"
            plain
            onPress={() => act($, ['drive', m?.drive ? 'off' : 'on'], `drive ${m?.drive ? 'off' : 'on'}`)}
          />
          <Button
            key="autonomy"
            label={m?.autonomy === 'full' ? 'standard autonomy' : 'full auto'}
            plain
            dimColor
            onPress={() => {
              const level = m?.autonomy === 'full' ? 'standard' : 'full'
              return act($, ['autonomy', level], `autonomy ${level}`)
            }}
          />
          <Button
            key="sound"
            label={isOn ? 'sound off' : 'sound on'}
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
