import type { EngineInterface, ResolveInput } from 'claude-code'
import type { FileChurn, LiveAgent } from '../types'
import { C, MASCOT_COLORS, TONE_COLOR, activityCells, agentColor, changedLines, churnCells, clawd, clean, elapsed, hex, miniClawd, mix, outputSummary, progressCells, shortPath, sparkCells, sparkText, textBar, textComet, toolFace } from './kit'
import { DIFF_LINES, OUT_LINES, cfg, took } from './state'
import type { ToolUseRender } from './state'

// T-0130: the transcript's Foreman rows and the small drawings the band and pane share; pure but for the
// atoms they read and the shared timing maps. They take the resolved element table, not $: the engine follows
// $ only into functions declared in the file that uses it.
export type UI = ReturnType<EngineInterface['ui']['resolve']>

/** A bar: a true-color Raster on the terminal, its text twin elsewhere. `fraction` null draws an activity comet. */
export function meter(
  ui: UI,
  e: ResolveInput,
  key: string,
  width: number,
  fraction: number | null,
  color: number,
  f: number | null,
) {
  if (e.surface === 'terminal') {
    const { Raster } = ui
    const cells =
      fraction === null ? activityCells(width, color, f ?? 0) : progressCells(width, fraction, mix(color, C.accent2, 0.6), color, f)
    return <Raster key={key} columns={width} rows={1} cells={cells} />
  }
  const { Box, Text } = ui
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
export function spark(ui: UI, e: ResolveInput, key: string, values: readonly number[], width: number) {
  if (e.surface === 'terminal') {
    const { Raster } = ui
    return <Raster key={key} columns={width} rows={1} cells={sparkCells(values, width)} />
  }
  const { Text } = ui
  return <Text color={hex(C.accent2)}>{sparkText(values, width)}</Text>
}

export function churn(ui: UI, e: ResolveInput, key: string, f: FileChurn, max: number) {
  if (e.surface === 'terminal') {
    const { Raster } = ui
    return <Raster key={key} columns={10} rows={1} cells={churnCells(f.add, f.del, max, 10)} />
  }
  const { Text } = ui
  return <Text color={hex(C.ok)}>{'━'.repeat(Math.max(1, Math.round((10 * (f.add + f.del)) / Math.max(1, max))))}</Text>
}

/** The mascot: Claude Code's own Claude, dancing while work runs, with a mini Claude per running subagent. */
export function mascotTree(ui: UI, e: ResolveInput, state: 'work' | 'idle' | 'happy', n: number, subs: LiveAgent[]) {
  if (cfg.mascot === 'off') return null
  const color = MASCOT_COLORS[cfg.mascot] ?? MASCOT_COLORS.blue!
  const { Box, Text } = ui
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

/** Changed lines of a diff as Foreman text: the file's line number dim, the +/- sign in ok/err, the text in the softer
 * add/del colours (T-0143: the engine's whole-width red and green read 'weird in contrast'). */
export function diffLines(ui: UI, e: ResolveInput, changed: ReturnType<typeof changedLines>, key: string) {
  const { Text } = ui
  const width = String(Math.max(0, ...changed.map(l => l.n))).length
  return changed.map((l, i) => (
    <Text key={`${key}-${i}`} wrap="truncate-end">
      <Text color={hex(C.track)}>{'  │ '}</Text>
      <Text color={hex(C.dim)}>{`${String(l.n).padStart(width)} `}</Text>
      <Text color={hex(l.sign === '+' ? C.ok : C.err)}>{`${l.sign} `}</Text>
      <Text color={hex(l.sign === '+' ? C.add : C.del)}>{l.text}</Text>
    </Text>
  ))
}

export const more = (n: number, what: string) => `… ${n} more ${what}${n === 1 ? '' : 's'}`

/** T-0137/T-0143: a finished shell command as a Foreman row that reads like the running one: its mark, `❯ Ran` and the
 * description (or the command's first line), time and lines; the command under it, dim, whole up to three lines and
 * never silently cut (a chained or multi-line command must not read as a plain one: the T-0095 review's HIGH
 * finding); then the output (failures first when it failed, else the tail), the files it changed, a commit, a
 * timeout. The engine's result block under it is blanked (ToolResult), so nothing draws twice. */
export function shellRow(ui: UI, e: ToolUseRender) {
  const { Box, Text } = ui
  type Out = {
    stdout?: unknown
    stderr?: unknown
    interrupted?: boolean
    backgroundTaskId?: unknown
    timedOutAfterMs?: unknown
    gitOperation?: { commit?: { sha?: unknown; branch?: unknown } }
    bashEditDiff?: { hunks?: unknown; skippedLarge?: unknown; restricted?: unknown } // Claude Code's own, untyped
  }
  const o = (e.props.output && typeof e.props.output === 'object' ? e.props.output : {}) as Out
  const input = (e.props.input ?? {}) as { command?: unknown; description?: unknown }
  const lines = String(input.command ?? '').split('\n').map(clean)
  const desc = typeof input.description === 'string' ? clean(input.description).trim() : ''
  const shown = desc ? lines.slice(0, 3) : lines.slice(1, 3) // without a description the first line is the title
  const bad = !!e.props.isErrored // the exit status decides, not words in the output
  const s = typeof e.props.output === 'string' ? outputSummary(e.props.output, '', OUT_LINES, bad) : outputSummary(o.stdout, o.stderr, OUT_LINES, bad)
  const ms = took.get(e.props.tool_use_id)
  const bg = typeof o.backgroundTaskId === 'string'
  const stopped = e.props.isInterrupted || o.interrupted
  const mark = stopped ? '■' : bg ? '◷' : bad ? '✗' : '✓'
  const meta = [ms !== undefined ? elapsed(ms) : '', bg ? 'in the background' : s.total ? `${s.total} line${s.total === 1 ? '' : 's'}` : '']
  const files = Array.isArray(o.bashEditDiff?.hunks) ? (o.bashEditDiff.hunks as { path?: unknown; hunks?: unknown }[]) : []
  const unshown = [o.bashEditDiff?.skippedLarge, o.bashEditDiff?.restricted].reduce<number>((n, x) => n + (Array.isArray(x) ? x.length : 0), 0)
  let budget = DIFF_LINES
  const commit = o.gitOperation?.commit
  return (
    <Box flexDirection="column" key="fm-shell">
      {/* the mark in a column of its own, so a long title wraps under itself (T-0141) */}
      <Box flexDirection="row" key="fm-shell-head">
        <Text bold color={hex(mark === '✗' ? C.err : mark === '✓' ? C.ok : mark === '◷' ? C.accent2 : C.warn)}>
          {`${mark} `}
        </Text>
        <Text wrap="wrap">
          <Text color={hex(C.accent)}>{`❯ ${stopped ? 'Stopped' : bg ? 'Started' : bad ? 'Failed' : 'Ran'} `}</Text>
          {desc ? <Text>{desc}</Text> : <Text color={hex(C.accent)}>{lines[0] ?? ''}</Text>}
          <Text color={hex(C.dim)}>{meta.filter(Boolean).map(x => ` · ${x}`).join('')}</Text>
        </Text>
      </Box>
      {shown.map((line, i) => (
        <Box flexDirection="row" key={`fm-shell-cmd-${i}`}>
          <Text color={hex(C.track)}>{'  ┆ '}</Text>
          <Text wrap="wrap" color={hex(mix(C.accent, C.dim, 0.55))}>
            {line}
          </Text>
        </Box>
      ))}
      {lines.length > 3 && <Text color={hex(C.dim)}>{`  ┆ ${more(lines.length - 3, 'command line')}`}</Text>}
      {s.lines.map((l, i) => (
        <Text key={`o-${i}`} color={hex(TONE_COLOR[l.tone])} wrap="truncate-end">
          <Text color={hex(C.track)}>{'  │ '}</Text>
          {l.text}
        </Text>
      ))}
      {s.more > 0 && (
        <Text color={hex(C.dim)}>
          {`  └ ${more(s.more, 'line')}`}
          {s.failures ? ' (showing the failures)' : ''}
        </Text>
      )}
      {files.map((f, i) => {
        const changed = changedLines(f.hunks)
        const add = changed.filter(l => l.sign === '+').length
        const take = changed.slice(0, Math.max(0, budget))
        budget -= take.length
        return (
          <Box flexDirection="column" key={`fm-shell-file-${i}`}>
            <Text wrap="truncate-start">
              <Text color={hex(C.edit)}>{'  ✎ '}</Text>
              <Text>{shortPath(clean(String(f.path ?? '')))}</Text>
              <Text color={hex(C.ok)}>{` +${add}`}</Text>
              {changed.length > add && <Text color={hex(C.err)}>{` −${changed.length - add}`}</Text>}
            </Text>
            {diffLines(ui, e, take, `fm-shell-diff-${i}`)}
          </Box>
        )
      })}
      {unshown > 0 && <Text color={hex(C.dim)}>{`  ✎ ${more(unshown, 'file')} changed (too large or private to show)`}</Text>}
      {typeof commit?.sha === 'string' && (
        <Text>
          <Text color={hex(C.accent2)}>{'  ⎇ '}</Text>
          <Text color={hex(C.dim)}>committed </Text>
          <Text color={hex(C.accent)}>{commit.sha.slice(0, 7)}</Text>
          {typeof commit.branch === 'string' && <Text color={hex(C.dim)}>{` on ${clean(commit.branch)}`}</Text>}
        </Text>
      )}
      {typeof o.timedOutAfterMs === 'number' && (
        <Text color={hex(C.warn)}>{`  ◷ timed out after ${elapsed(o.timedOutAfterMs)} · moved to the background`}</Text>
      )}
    </Box>
  )
}

/** T-0141: the changed lines a finished Edit or Write shows, or null when its result has no patch to show */
export function editChanges(tool: string, output: unknown) {
  const o = output as { type?: unknown; content?: unknown; structuredPatch?: unknown; userModified?: unknown } | null
  if ((tool !== 'Edit' && tool !== 'Write') || !o || typeof o !== 'object' || !Array.isArray(o.structuredPatch)) return null
  const created = o.type === 'create' && typeof o.content === 'string'
  const changed = created
    ? changedLines([{ oldStart: 1, newStart: 1, lines: String(o.content).replace(/\n$/, '').split('\n').map(l => `+${l}`) }])
    : changedLines(o.structuredPatch)
  return changed.length ? { changed, created, userModified: o.userModified === true } : null
}

/** T-0141: a finished Edit or Write as a Foreman row: the path, +added −removed, then the changed lines (diffLines).
 * Null without a patch to show: the engine's row then says what happened. */
export function editRow(ui: UI, e: ToolUseRender) {
  const c = editChanges(e.props.tool, e.props.output)
  if (!c) return null
  const { changed, created } = c
  const add = changed.filter(l => l.sign === '+').length
  const del = changed.length - add
  const shown = changed.slice(0, DIFF_LINES)
  const face = toolFace(e.props.tool, e.props.input, cfg.root)
  const { Box, Text } = ui
  return (
    <Box flexDirection="column" key="fm-edit">
      <Box flexDirection="row" gap={1} key="fm-edit-head">
        <Text bold color={hex(C.ok)}>
          ✓
        </Text>
        <Text color={hex(C.edit)}>
          {face.icon} {e.props.tool === 'Write' ? 'Wrote' : 'Edited'}
        </Text>
        <Text wrap="truncate-start">{face.target}</Text>
        <Text>
          <Text color={hex(C.ok)}>+{add}</Text>
          {del > 0 && <Text color={hex(C.err)}> −{del}</Text>}
        </Text>
        {created && <Text color={hex(C.dim)}>new file</Text>}
        {c.userModified && <Text color={hex(C.dim)}>· you changed it</Text>}
      </Box>
      {diffLines(ui, e, shown, 'd')}
      {changed.length > shown.length && <Text color={hex(C.dim)}>{`  └ ${more(changed.length - shown.length, 'changed line')}`}</Text>}
    </Box>
  )
}

export type AgentOut = { status?: unknown; agentType?: unknown; content?: unknown; totalToolUseCount?: unknown; totalDurationMs?: unknown; totalTokens?: unknown }
export const agentOut = (tool: string, output: unknown) =>
  (tool === 'Agent' || tool === 'Task') && output && typeof output === 'object' &&
  ['completed', 'async_launched'].includes(String((output as AgentOut).status))
    ? (output as AgentOut)
    : null

/** T-0148: a subagent call as a Foreman row: its type and task, tools · time · tokens, the first line of its report
 * (the engine drew the name on a highlighted block); a background launch says so. Null for anything else. */
export function agentRow(ui: UI, e: ToolUseRender) {
  const o = agentOut(e.props.tool, e.props.output)
  if (!o) return null
  const input = (e.props.input ?? {}) as { subagent_type?: unknown; description?: unknown }
  const type = clean(String(input.subagent_type ?? o.agentType ?? 'agent')).replace(/^foreman:/, '')
  const bg = o.status === 'async_launched'
  const report = Array.isArray(o.content) ? o.content.map(x => String((x as { text?: unknown }).text ?? '')).join('\n') : ''
  const first = clean(report.split('\n').find(l => l.trim()) ?? '').replace(/[*_`#>]/g, '').trim()
  const n = Number(o.totalToolUseCount) || 0
  const meta = bg
    ? 'in the background'
    : [`${n} tool${n === 1 ? '' : 's'}`, elapsed(Number(o.totalDurationMs) || 0), `${Math.round((Number(o.totalTokens) || 0) / 1000)}k tokens`].join(' · ')
  const { Box, Text } = ui
  return (
    <Box flexDirection="column" key="fm-agent">
      <Box flexDirection="row" key="fm-agent-head">
        <Text bold color={hex(bg ? C.accent2 : C.ok)}>
          {`${bg ? '◷' : '✓'} `}
        </Text>
        <Text wrap="wrap">
          <Text color={hex(C.agent)}>{`◆ ${type} `}</Text>
          <Text>{clean(String(input.description ?? ''))}</Text>
          <Text color={hex(C.dim)}>{` · ${meta}`}</Text>
        </Text>
      </Box>
      {!bg && first && (
        <Text color={hex(C.dim)} wrap="truncate-end">
          <Text color={hex(C.track)}>{'  │ '}</Text>
          {first.slice(0, 200)}
        </Text>
      )}
    </Box>
  )
}
