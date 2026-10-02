import { expect, mock, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { bar, guardReason, toasts } from '../hooks/register'
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
    { id: 'T-0007', type: 'FIX', tier: 'M', title: 'Login times out', status: 'active' },
    {
      id: 'T-0009', type: 'FEATURE', tier: 'L', title: 'CSV export', status: 'planned', waits: 'plan approval',
      plan: {
        interpretation: 'export the report table', approach: 'csv module vs pandas: csv module',
        steps: [{ n: 1, text: 'write the exporter', done: false, current: true }],
        criteria: [{ n: 1, text: 'opens in Excel', verify: 'pytest -q', checked: false }],
      },
    },
  ],
  inbox: [{ id: 'T-0011', type: 'CLEAN', tier: 'S', title: 'Merge date helpers', status: 'captured' }],
  inbox_total: 1,
  approvals: [],
  closed: [],
  recent: ['13:12 ⚑ T-0011 captured'],
  health: { hook_p95_ms: 31, guard_blocks: 0, hook_errors: 0 },
  watch: [],
}

const BAND = {
  component: 'AbovePrompt',
  props: { hasSurvey: false, isWorking: false, maxRows: 12, bodyColumns: 100, scroll: { offset: 0, bodyRows: 12 }, view: {} },
} as const
const PANE = {
  component: 'Pane',
  requestId: 'foreman',
  props: { title: 'Foreman', isFocused: true, bodyColumns: 60, placement: 'dock', scroll: { offset: 0, bodyRows: 40 }, view: {} },
} as const

// The world beneath the plugin: fm answers from `views` (last one repeats) and every argv is recorded.
function world(on: On, views: FmView[]) {
  const calls: string[][] = []
  const toasted: string[] = []
  mock.clock(on)
  mock.env(on, { FOREMAN_FM: 'fm', HOME: '/home/u' })
  on('process.run', async ($, e) => {
    calls.push([...e.argv])
    const v = views.length > 1 ? views.shift()! : views[0]
    const stdout = e.argv[1] === 'ui' ? JSON.stringify(v) : 'ok'
    return { value: { exitCode: 0, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }
  })
  on('ui.toast', async ($, e) => {
    toasted.push(e.text)
    return { value: undefined }
  })
  const opened: string[] = []
  on('ui.open', async ($, e) => {
    opened.push(e.id)
    return { value: { isPlaced: true } }
  })
  on('session.start', async ($, e) => ({ cwd: e.cwd }))
  on('command.register', async ($, e) => ({ value: { command: e.name } }))
  on('ui.render', async ($, e) => {
    const { Text } = $.ui.resolve(e)
    return <Text key="engine">engine</Text>
  })
  return { calls, toasted, opened }
}

test('progress bar fills by steps done', () => {
  expect(bar(1, 2)).toBe('▰▱')
  expect(bar(0, 0)).toBe('')
  expect(bar(5, 20)).toBe('▰▰▰▱▱▱▱▱▱▱')
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

test('band shows the task line and next action; a waiting plan is reviewed in the pane, never approved from the band', async ($, on) => {
  const { calls, opened } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface, ...BAND })
    expect(await ui.find({ type: 'Text', text: /T-0007 FIX M · executing ▰▱ 1\/2 raise the timeout/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /Next: T-0007 step 2\/2/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /audits 0\/2 · q2 in1 · standard/ })).toBeDefined()
    expect(await ui.find({ key: 'approve-T-0009' })).toBeUndefined()
    await ui.press({ key: 'review-T-0009' })
    expect(opened).toContain('foreman')
    expect(calls).not.toContainEqual(['fm', 'task', 'set', 'T-0009', 'approved=true'])
    await ui.unmount()
  }
})

test('band stays out of the way outside a Foreman project', async ($, on) => {
  world(on, [{ v: 1, project: null }])
  await $.session.start({ cwd: '/elsewhere', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...BAND })
  expect(await ui.find({ type: 'Text', text: /▌/ })).toBeUndefined()
  expect(await ui.find({ text: 'engine' })).toBeDefined()
  await ui.unmount()
})

test('pane lists steps, criteria, queue and inbox; its buttons run fm', async ($, on) => {
  const { calls } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface, ...PANE })
    expect(await ui.find({ type: 'Text', text: /▸ 2\. raise the timeout/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /○ AC1 slow wifi logs in/ })).toBeDefined()
    expect(await ui.find({ key: 'in-T-0011' })).toBeDefined()
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

test('a guard refusal of a tool call becomes a toast', async ($, on) => {
  const { toasted } = world(on, [VIEW])
  on('tool.call', async () => ({ deny: 'Foreman guard: blocked core: plugin/lib/fmcore.py is protected core.' }))
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Bash', command: 'rm -rf plugin/lib' })
  expect(toasted.some(t => t.startsWith('⛔ Foreman: blocked core'))).toBe(true)
})
