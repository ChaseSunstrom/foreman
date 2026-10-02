import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { FmActive, FmItem, FmView } from '../types'

// Foreman inside Claude Code. A pure renderer over `fm ui --json`: every rule and gate stays in fm and its classic
// hooks (which still run under claude -p and older builds); buttons only run fm commands or submit a prompt the
// person pressed for.
const PANE = 'foreman'
const view = atom({ plugin: 'foreman-ui', key: 'view' } as const, null)
const error = atom({ plugin: 'foreman-ui', key: 'error' } as const, null)

const BAR = 10
const LIST = 6

export function bar(done: number, total: number): string {
  if (total <= 0) return ''
  const cells = Math.min(BAR, total)
  const full = Math.round((done / total) * cells)
  return '▰'.repeat(full) + '▱'.repeat(cells - full)
}

export function taskLine(a: FmActive): string {
  const done = a.steps.filter(s => s.done).length
  const cur = a.steps.find(s => s.current)
  const step = a.steps.length ? ` ${bar(done, a.steps.length)} ${done}/${a.steps.length}` : ''
  return `▌${a.id} ${a.type} ${a.tier} · ${a.stage}${step}${cur ? ` ${cur.text}` : ''}`
}

export function modeLine(v: FmView): string {
  const a = v.active
  const audits = a && a.audits.need ? `audits ${a.audits.done}/${a.audits.need} · ` : ''
  const m = v.mode
  const mode = m ? ` · ${m.autonomy === 'full' ? 'full auto' : 'standard'}${m.drive ? '' : ' · drive off'}` : ''
  return `${audits}q${(v.queue ?? []).length} in${v.inbox_total ?? (v.inbox ?? []).length}${mode}`
}

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

// Module variables start over on a reload; the view lives in $.state.
let fmPath: string | null = null
let marks = ''
let isDirty = true
let isBusy = false
let lastFull = 0
let poll: { cancel: () => void } | null = null

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

  on('tool.call', async ($, e, next) => {
    const r = await next(e)
    isDirty = true
    const why = guardReason(r)
    if (why) $.ui.toast(`⛔ Foreman: ${why}`, { timeoutMs: 8000 })
    return r
  })

  on('turn.complete', async ($, e, next) => {
    isDirty = true
    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const v = await read($, view)
    if (e.props.hasSurvey || !v?.project) return next(e)
    const a = v.active
    const asks = v.approvals ?? []
    const plans = (v.queue ?? []).filter(q => q.waits === 'plan approval')
    if (!a && !asks.length && !plans.length && !(v.queue ?? []).length) return next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    const idle = !e.props.isWorking

    return (
      <Box flexDirection="column" key="fm-band">
        <Box flexDirection="row" gap={1}>
          <Text bold color="cyan" wrap="truncate-end" key="task">
            {a ? taskLine(a) : `▌Foreman · ${(v.queue ?? []).length} queued`}
          </Text>
          <Text dimColor wrap="truncate-end" key="mode">
            {modeLine(v)}
          </Text>
        </Box>
        {v.next && (
          <Text dimColor wrap="truncate-end" key="next">
            Next: {v.next}
          </Text>
        )}
        {asks.map(x => (
          <Text color="yellow" wrap="truncate-end" key={`ask-${x.task}`}>
            ⚠ Needs you: {x.task} {x.allow.join(', ')} — {x.why}
          </Text>
        ))}
        {plans.slice(0, 2).map(q => (
          <Box flexDirection="row" gap={1} key={`plan-${q.id}`}>
            <Text color="yellow" wrap="truncate-end">
              ⚠ {q.id} {q.tier} plan awaits approval: {q.title}
            </Text>
            {/* consent is given in the pane, where the plan it approves is shown */}
            <Button key={`review-${q.id}`} label="Review" hotkey="v" onPress={() => void openPane($, true)} />
          </Box>
        ))}
        <Box flexDirection="row" gap={1}>
          <Button key="open" label="Foreman" hotkey="f" onPress={() => void openPane($, true)} />
          {idle && (
            <Button
              key="next"
              label="Next"
              hotkey="n"
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
          <Text dimColor>Not a Foreman project here.{err ? ` (${err})` : ''}</Text>
          <Text dimColor>Ask Claude to set it up, or run /foreman:intake with a request.</Text>
        </Box>
      )
    }
    const a = v.active
    const m = v.mode
    const row = (it: FmItem) => `${it.id} ${it.type} ${it.tier}  ${it.title}${it.waits ? `  (${it.waits})` : ''}`

    return (
      <Box flexDirection="column" key="fm-pane">
        <Box flexDirection="row" justifyContent="space-between">
          <Text bold>{v.project}</Text>
          <Text dimColor>
            {m ? `${m.autonomy} · drive ${m.drive ? 'on' : 'off'}${m.sensitive ? ' · sensitive' : ''}` : ''}
          </Text>
        </Box>
        {err && <Text color="red">fm: {err}</Text>}
        {a ? (
          <Box flexDirection="column" marginTop={1} key="active">
            <Text bold color="cyan" wrap="wrap">
              ▌{a.id} {a.type} {a.tier} {a.title}
            </Text>
            <Text dimColor wrap="wrap">
              {a.stages.map(s => (s === a.stage ? `[${s}]` : s)).join(' › ')}
            </Text>
            {a.steps.map(s => (
              <Text key={`step-${s.n}`} color={s.current ? 'cyan' : undefined} dimColor={s.done} wrap="truncate-end">
                {s.done ? '✓' : s.current ? '▸' : '·'} {s.n}. {s.text}
              </Text>
            ))}
            {a.criteria.map(c => (
              <Text key={`ac-${c.n}`} color={c.checked ? 'green' : undefined} wrap="truncate-end">
                {c.checked ? '✓' : '○'} AC{c.n} {c.text}
              </Text>
            ))}
            <Text dimColor>
              audits {a.audits.done}/{a.audits.need}
              {a.blockers.length ? ` · ${a.blockers.length} blocker(s) before done` : ''}
            </Text>
          </Box>
        ) : (
          <Text dimColor>No active task.</Text>
        )}
        {v.next && (
          <Text wrap="wrap" key="next">
            Next: {v.next}
          </Text>
        )}
        {(v.approvals ?? []).map(x => (
          <Text color="yellow" wrap="wrap" key={`ask-${x.task}`}>
            ⚠ {x.task} needs your yes for {x.allow.join(', ')}: {x.why}
          </Text>
        ))}
        {(v.queue ?? []).flatMap(q => (q.plan ? [{ ...q, plan: q.plan }] : [])).map(q => (
          <Box flexDirection="column" marginTop={1} key={`plan-${q.id}`}>
            <Text bold color="yellow" wrap="wrap">
              ⚠ {q.id} {q.type} {q.tier} plan awaits your approval: {q.title}
            </Text>
            {q.plan.interpretation && <Text wrap="wrap">Means: {q.plan.interpretation}</Text>}
            {q.plan.approach && <Text wrap="wrap">Approach: {q.plan.approach}</Text>}
            {q.plan.steps.map(s => (
              <Text key={`plan-${q.id}-step-${s.n}`} wrap="truncate-end">
                · {s.n}. {s.text}
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
        <Text bold>Queue ({(v.queue ?? []).length})</Text>
        {(v.queue ?? []).slice(0, LIST).map(q => (
          <Text wrap="truncate-end" color={q.waits ? 'yellow' : undefined} key={`q-${q.id}`}>
            {row(q)}
          </Text>
        ))}
        <Text bold>Inbox ({v.inbox_total ?? (v.inbox ?? []).length})</Text>
        {(v.inbox ?? []).slice(0, LIST).map(it => (
          <Box flexDirection="row" gap={1} key={`in-${it.id}`}>
            <Text wrap="truncate-end">{row(it)}</Text>
            <Button
              key={`start-${it.id}`}
              label="Start"
              onPress={() =>
                void $.prompt.submit({ text: `Plan and start ${it.id} (/foreman:intake).`, asUser: true })
              }
            />
            <Button
              key={`drop-${it.id}`}
              label="Drop"
              onPress={() => act($, ['task', 'drop', it.id, 'dropped from the Foreman pane'], `${it.id} dropped`)}
            />
          </Box>
        ))}
        {(v.recent ?? []).length > 0 && <Text bold>Recent</Text>}
        {(v.recent ?? []).slice(-LIST).map((line, i) => (
          <Text dimColor wrap="truncate-end" key={`r-${i}`}>
            {line}
          </Text>
        ))}
        {v.health && (
          <Text dimColor key="health">
            hooks p95 {v.health.hook_p95_ms ?? '–'} ms · guard blocks {v.health.guard_blocks}
            {v.health.hook_errors ? ` · ${v.health.hook_errors} hook error(s)` : ''}
          </Text>
        )}
        <Box flexDirection="row" gap={1} marginTop={1}>
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
