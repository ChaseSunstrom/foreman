import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, ResolveInput } from 'claude-code'

import type { FmView, TurnSummary } from '../types'
import { C, activityCells, elapsed, hex, mix, progressCells, spin, textBar, textComet, toolFace, typeColor } from './kit'

// Foreman inside Claude Code. A pure renderer over `fm ui --json`: every rule and gate stays in fm and its classic
// hooks (which still run under claude -p and older builds); buttons only run fm commands or submit a prompt the
// person pressed for. While a turn runs, a frame clock animates the band and every running tool row; a finished row
// goes back to the engine, which draws its result (diffs, output) as it always does.
const PANE = 'foreman'
const view = atom({ plugin: 'foreman-ui', key: 'view' } as const, null)
const error = atom({ plugin: 'foreman-ui', key: 'error' } as const, null)
const frame = atom({ plugin: 'foreman-ui', key: 'frame' } as const, 0)
const summaries = atom({ plugin: 'foreman-ui', key: 'summaries' } as const, [])

const LIST = 6
const FRAME_MS = 120
const IDLE_FRAMES = Math.round((15 * 60 * 1000) / FRAME_MS) // a lost turn.complete stops the clock after 15 min

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

// Module variables start over on a reload; what a drawing reads lives in $.state.
let fmPath: string | null = null
let marks = ''
let isDirty = true
let isBusy = false
let lastFull = 0
let poll: { cancel: () => void } | null = null
let clock: { cancel: () => void } | null = null
let lastActive = 0 // the frame of the last turn or tool activity
const turns = new Set<string>()
const starts = new Map<string, number>() // tool_use_id → when it started (ms)
const agentCalls = new Map<string, string>() // running Agent call → its description
const agentOf = new Map<string, string>() // running Agent call → the subagent's id
const agentStats = new Map<string, { tools: number; last: string }>()
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

async function refresh($: EngineInterface) {
  if (isBusy) {
    isDirty = true
    return
  }
  isBusy = true
  isDirty = false
  try {
    const r = await run($, ['ui', '--json'])
    if (r.exitCode !== 0) throw new Error(r.stderr.trim().split('\n').at(-1) || `fm ui exited ${r.exitCode}`)
    const next = JSON.parse(r.stdout) as FmView
    const prev = await read($, view)
    for (const line of toasts(prev, next)) $.ui.toast(line)
    await update($, view, () => next)
    await update($, error, () => null)
    lastFull = await $.clock.now()
  } catch (err) {
    await update($, error, () => String(err instanceof Error ? err.message : err).slice(0, 200))
  } finally {
    isBusy = false
  }
}

// Cheap in-process change check: stat the paths fm names; spawn fm only when one moved (or every 30 s).
async function tick($: EngineInterface) {
  const v = await read($, view)
  const stamps = await Promise.all(
    (v?.watch ?? []).map(p => $.fs.stat(p).then(s => `${s.mtimeMs}:${s.size}`, () => '-')),
  )
  const now = await $.clock.now()
  const moved = stamps.join('|') !== marks
  marks = stamps.join('|')
  if (isDirty || moved || now - lastFull > 30000) await refresh($)
}

async function act($: EngineInterface, args: string[], done: string) {
  const r = await run($, args)
  $.ui.toast(r.exitCode === 0 ? done : `fm ${args[0]}: ${(r.stderr || r.stdout).trim().split('\n').at(-1)}`)
  await refresh($)
}

async function openPane($: EngineInterface, focus: boolean) {
  return $.ui.open(focus ? { id: PANE, title: 'Foreman', focus: true } : { id: PANE, title: 'Foreman' })
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
  if (!turns.size && !starts.size && f - lastActive > 2) return sleep()
  if (f - lastActive > IDLE_FRAMES) return sleep()
  await update($, frame, n => n + 1)
}

function sleep() {
  clock?.cancel()
  clock = null
}

// A subagent's tool calls carry its id: count them and tie the subagent to the Agent row that started it.
async function noteSubagent($: EngineInterface, agentId: string, last: string) {
  const s = agentStats.get(agentId) ?? { tools: 0, last: '' }
  agentStats.set(agentId, { tools: s.tools + 1, last })
  if ([...agentOf.values()].includes(agentId)) return
  const info = (await $.agent.list()).find(a => a.id === agentId)
  const call = [...agentCalls].find(([id, d]) => d === info?.description && !agentOf.has(id))
  if (call) agentOf.set(call[0], agentId)
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

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'fm', description: 'Foreman: open or close the dashboard pane' })
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
    if (!e.agentId) {
      await refresh($)
      const a = (await read($, view))?.active
      const now = a && a.id === turn.task ? a.steps.filter(s => s.done).length : -1
      const step = turn.stepsDone >= 0 && now > turn.stepsDone && a ? `${a.id} step ${now}/${a.steps.length}` : ''
      const s: TurnSummary = { durationMs: e.durationMs, tools: turn.tools, edits: turn.edits, add: turn.add, del: turn.del, agents: turn.agents, step }
      await update($, summaries, list => [...list, s].slice(-40))
    }
    return next(e)
  })

  on('tool.call', async ($, e, next) => {
    const id = e.tool_use_id
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
      const r = await next(e)
      const why = guardReason(r)
      if (why) $.ui.toast(`⛔ Foreman: ${why}`, { timeoutMs: 8000 })
      return r
    } finally {
      starts.delete(id)
      agentCalls.delete(id)
      agentOf.delete(id)
      isDirty = true
    }
  })

  // While a tool runs: an animated row (spinner, verb, target, edit delta, activity bar, elapsed). Done: the engine's.
  on('ui.render', { component: 'ToolUse' }, async ($, e, next) => {
    if (!e.props.isRunning || e.props.isErrored || e.props.isInterrupted) return next(e)
    const f = await read($, frame)
    const face = toolFace(e.props.tool, e.props.input)
    const since = starts.get(e.props.tool_use_id)
    const ms = since === undefined ? 0 : (await $.clock.now()) - since
    const agent = agentStats.get(agentOf.get(e.props.tool_use_id) ?? '')
    const { Box, Text } = $.ui.resolve(e)
    const width = Math.max(30, e.viewport?.columns ?? 100)

    return (
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
  })

  // The working line keeps its animated word and gains the Foreman step it is on.
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    const a = (await read($, view))?.active
    const cur = a?.steps.find(s => s.current)
    if (!a || !cur) return next(e)
    const done = a.steps.filter(s => s.done).length
    return next({ ...e, props: { ...e.props, suffix: `… ▸ ${a.id} ${done + 1}/${a.steps.length} ${cur.text}`.slice(0, 90) } })
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

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const v = await read($, view)
    if (e.props.hasSurvey || !v?.project) return next(e)
    const a = v.active
    const asks = v.approvals ?? []
    const plans = (v.queue ?? []).filter(q => q.waits === 'plan approval')
    if (!a && !asks.length && !plans.length && !(v.queue ?? []).length) return next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    const working = e.props.isWorking
    const f = working ? await read($, frame) : null
    const m = v.mode
    const done = a ? a.steps.filter(s => s.done).length : 0
    const cur = a?.steps.find(s => s.current)
    const width = Math.max(10, Math.min(28, e.props.bodyColumns - 60))

    return (
      <Box flexDirection="column" borderStyle="round" borderColor={hex(working ? C.accent : C.track)} paddingX={1} key="fm-band">
        <Box flexDirection="row" justifyContent="space-between">
          <Box flexDirection="row" gap={1}>
            {a ? (
              <>
                <Text backgroundColor={typeColor(a.type)} color="#000000" bold>
                  {` ${a.type} ${a.tier} `}
                </Text>
                <Text bold color={hex(C.accent)}>
                  {a.id}
                </Text>
                <Text bold wrap="truncate-end">
                  {a.title}
                </Text>
              </>
            ) : (
              <Text bold color={hex(C.accent)}>
                ▌Foreman · {(v.queue ?? []).length} queued
              </Text>
            )}
          </Box>
          <Text color={hex(C.dim)}>
            {m ? (m.autonomy === 'full' ? '⚡ full auto' : '◇ standard') : ''}
            {m && !m.drive ? ' · drive off' : ''} · q{(v.queue ?? []).length} · in{v.inbox_total ?? 0}
          </Text>
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
            {cur && <Text wrap="truncate-end">{cur.text}</Text>}
            {a.audits.need > 0 && (
              <Text color={hex(a.audits.done >= a.audits.need ? C.ok : C.dim)}>
                · audits {a.audits.done}/{a.audits.need}
              </Text>
            )}
          </Box>
        )}
        {!working && v.next && (
          <Text color={hex(C.dim)} wrap="truncate-end">
            → {v.next}
          </Text>
        )}
        {asks.map(x => (
          <Text color={hex(C.warn)} wrap="truncate-end" key={`ask-${x.task}`}>
            ⚠ Needs you: {x.task} {x.allow.join(', ')} — {x.why}
          </Text>
        ))}
        {plans.slice(0, 2).map(q => (
          <Box flexDirection="row" gap={1} key={`plan-${q.id}`}>
            <Text color={hex(C.warn)} wrap="truncate-end">
              ⚠ {q.id} {q.tier} plan awaits approval: {q.title}
            </Text>
            {/* consent is given in the pane, where the plan it approves is shown */}
            <Button key={`review-${q.id}`} label="Review" hotkey="v" onPress={() => void openPane($, true)} />
          </Box>
        ))}
        <Box flexDirection="row" gap={1}>
          <Button key="open" label="Dashboard" hotkey="f" plain onPress={() => void openPane($, true)} />
          {!working && (
            <Button
              key="next"
              label="Next"
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
    const a = v.active
    const m = v.mode
    const width = Math.max(10, e.props.bodyColumns - 12)
    const card = (color: number) =>
      ({ flexDirection: 'column', borderStyle: 'round', borderColor: hex(color), paddingX: 1 }) as const
    const done = a ? a.steps.filter(s => s.done).length : 0
    const chip = (type: string, tier: string) => (
      <Text backgroundColor={typeColor(type)} color="#000000">
        {` ${type.slice(0, 4)} ${tier} `}
      </Text>
    )

    return (
      <Box flexDirection="column" key="fm-pane">
        <Box flexDirection="row" justifyContent="space-between">
          <Text bold color={hex(C.accent)}>
            ▌{v.project}
          </Text>
          <Text color={hex(C.dim)}>
            {m ? `${m.autonomy === 'full' ? '⚡ full auto' : '◇ standard'} · drive ${m.drive ? 'on' : 'off'}${m.sensitive ? ' · sensitive' : ''}` : ''}
          </Text>
        </Box>
        {err && <Text color={hex(C.err)}>fm: {err}</Text>}
        <Box key="card-task" {...card(a ? C.accent : C.track)}>
          {a ? (
            <Box flexDirection="column">
              <Box flexDirection="row" gap={1}>
                {chip(a.type, a.tier)}
                <Text bold color={hex(C.accent)}>
                  {a.id}
                </Text>
                <Text bold wrap="wrap">
                  {a.title}
                </Text>
              </Box>
              <Text wrap="wrap">
                {a.stages.map(s => (s === a.stage ? `◉ ${s}` : a.stages.indexOf(s) < a.stages.indexOf(a.stage) ? `● ${s}` : `○ ${s}`)).join('  ')}
              </Text>
              {a.steps.length > 0 && (
                <Box flexDirection="row" gap={1}>
                  {meter($, e, 'fm-pane-bar', Math.min(40, width - 8), done / a.steps.length, C.ok, null)}
                  <Text bold>
                    {done}/{a.steps.length}
                  </Text>
                </Box>
              )}
              {a.steps.map(s => (
                <Text key={`step-${s.n}`} color={s.current ? hex(C.accent) : s.done ? hex(C.dim) : undefined} wrap="truncate-end">
                  {s.done ? '✓' : s.current ? '▸' : '○'} {s.n}. {s.text}
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
            </Box>
          ) : (
            <Text color={hex(C.dim)}>No active task.</Text>
          )}
          {v.next && (
            <Text color={hex(C.dim)} wrap="wrap">
              → {v.next}
            </Text>
          )}
        </Box>
        {(v.approvals ?? []).map(x => (
          <Text color={hex(C.warn)} wrap="wrap" key={`ask-${x.task}`}>
            ⚠ {x.task} needs your yes for {x.allow.join(', ')}: {x.why}
          </Text>
        ))}
        {(v.queue ?? []).flatMap(q => (q.plan ? [{ ...q, plan: q.plan }] : [])).map(q => (
          <Box flexDirection="column" borderStyle="round" borderColor={hex(C.warn)} paddingX={1} key={`plan-${q.id}`}>
            <Text bold color={hex(C.warn)} wrap="wrap">
              ⚠ {q.id} {q.type} {q.tier} plan awaits your approval: {q.title}
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
                label="Approve plan"
                variant="primary"
                onPress={() => act($, ['task', 'set', q.id, 'approved=true'], `✓ ${q.id} plan approved`)}
              />
            </Box>
          </Box>
        ))}
        <Box key="card-queue" {...card(C.track)}>
          <Text bold>Queue · {(v.queue ?? []).length}</Text>
          {(v.queue ?? []).length === 0 && <Text color={hex(C.dim)}>empty</Text>}
          {(v.queue ?? []).slice(0, LIST).map(q => (
            <Box flexDirection="row" gap={1} key={`q-${q.id}`}>
              {chip(q.type, q.tier)}
              <Text wrap="truncate-end" color={q.waits ? hex(C.warn) : undefined}>
                {q.id} {q.title}
                {q.waits ? `  (${q.waits})` : ''}
              </Text>
            </Box>
          ))}
        </Box>
        <Box key="card-inbox" {...card(C.track)}>
          <Text bold>Inbox · {v.inbox_total ?? (v.inbox ?? []).length}</Text>
          {(v.inbox ?? []).slice(0, LIST).map(it => (
            <Box flexDirection="row" gap={1} key={`in-${it.id}`}>
              {chip(it.type, it.tier)}
              <Text wrap="truncate-end">
                {it.id} {it.title}
              </Text>
              <Button
                key={`start-${it.id}`}
                label="Start"
                plain
                onPress={() => void $.prompt.submit({ text: `Plan and start ${it.id} (/foreman:intake).`, asUser: true })}
              />
              <Button
                key={`drop-${it.id}`}
                label="Drop"
                plain
                onPress={() => act($, ['task', 'drop', it.id, 'dropped from the Foreman pane'], `${it.id} dropped`)}
              />
            </Box>
          ))}
        </Box>
        <Box key="card-activity" {...card(C.track)}>
          <Text bold>Activity</Text>
          {(v.recent ?? []).slice(-LIST).map((line, i) => (
            <Text color={hex(C.dim)} wrap="truncate-end" key={`r-${i}`}>
              {line}
            </Text>
          ))}
          {v.health && (
            <Text color={hex(v.health.hook_errors ? C.err : C.dim)}>
              hooks p95 {v.health.hook_p95_ms ?? '–'} ms · guard blocks {v.health.guard_blocks}
              {v.health.hook_errors ? ` · ${v.health.hook_errors} hook error(s)` : ''}
            </Text>
          )}
        </Box>
        <Box flexDirection="row" gap={1}>
          <Button
            key="next"
            label="Next"
            hotkey="n"
            variant="primary"
            onPress={() => void $.prompt.submit({ text: '/foreman:next', asUser: true })}
          />
          <Button
            key="drive"
            label={m?.drive ? 'Drive off' : 'Drive on'}
            hotkey="d"
            onPress={() => act($, ['drive', m?.drive ? 'off' : 'on'], `drive ${m?.drive ? 'off' : 'on'}`)}
          />
          <Button
            key="autonomy"
            label={m?.autonomy === 'full' ? 'Standard autonomy' : 'Full auto'}
            onPress={() => {
              const level = m?.autonomy === 'full' ? 'standard' : 'full'
              return act($, ['autonomy', level], `autonomy ${level}`)
            }}
          />
          <Button key="refresh" label="Refresh" hotkey="r" onPress={() => refresh($)} />
        </Box>
      </Box>
    )
  })
}
