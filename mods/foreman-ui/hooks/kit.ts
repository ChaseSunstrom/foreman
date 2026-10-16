// The visual kit: palette, true-color Raster bars for the terminal and their text twins for other surfaces, the
// spinner, and how each tool call reads while it runs. Pure functions: no $, so every surface and test can use them.

export const C = {
  accent: 0x5fd7d7,
  accent2: 0x87afff,
  ok: 0x87d787,
  warn: 0xffd75f,
  err: 0xff6b6b,
  edit: 0xffaf5f,
  agent: 0xd787ff,
  web: 0x87d7af,
  skill: 0xf5a3c7,
  dim: 0x6c7686,
  muted: 0x9aa3b0, // T-1026: secondary text that still reads; dim is for the least of it
  add: 0xa8d5a2, // diff text: softer than ok/err, which stay on the +/- signs (T-0143: 'weird in contrast')
  del: 0xe0a3a3,
  track: 0x30363f,
  white: 0xffffff,
} as const

export const hex = (c: number) => `#${c.toString(16).padStart(6, '0')}`

const TYPE_COLOR: Record<string, number> = {
  FIX: C.err,
  FEATURE: C.accent2,
  CLEAN: C.accent,
  PERFORMANCE: C.agent,
  SECURITY: C.edit,
  RESEARCH: 0xafafff,
}
export const typeColor = (type: string) => hex(TYPE_COLOR[type] ?? C.dim)

export function mix(a: number, b: number, t: number): number {
  const k = Math.max(0, Math.min(1, t))
  let out = 0
  for (const shift of [16, 8, 0]) {
    const x = (a >> shift) & 0xff
    const y = (b >> shift) & 0xff
    out |= Math.round(x + (y - x) * k) << shift
  }
  return out
}

const DEFAULT_BG = 0x01000000

/** Raster cells as RasterProps wants them: base64 of little-endian u32 [codePoint, fg, bg] per cell. */
export function cells(list: readonly (readonly [string, number] | readonly [string, number, number])[]): string {
  const view = new DataView(new ArrayBuffer(list.length * 12))
  list.forEach(([ch, fg, bg], i) => {
    view.setUint32(i * 12, ch.codePointAt(0) ?? 0x20, true)
    view.setUint32(i * 12 + 4, fg, true)
    view.setUint32(i * 12 + 8, bg ?? DEFAULT_BG, true)
  })
  let bin = ''
  const bytes = new Uint8Array(view.buffer)
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]!)
  return btoa(bin)
}

/** A comet moving along the bar: brightness falls off behind its head. `frame` drives it. */
function glow(i: number, width: number, frame: number): number {
  const head = (frame % (width + 10)) - 5
  const d = head - i
  return d >= 0 && d < 6 ? 1 - d / 6 : 0
}

/** A determinate bar: a from→to gradient over the done part, a dim track after; a comet sweeps it while `frame`. */
export function progressCells(width: number, fraction: number, from: number, to: number, frame: number | null): string {
  const done = Math.round(Math.max(0, Math.min(1, fraction)) * width)
  const out: [string, number][] = []
  for (let i = 0; i < width; i++) {
    const base = i < done ? mix(from, to, width > 1 ? i / (width - 1) : 1) : C.track
    out.push(['━', frame === null ? base : mix(base, C.white, glow(i, width, frame) * (i < done ? 0.55 : 0.35))])
  }
  return cells(out)
}

/** T-1026: parts of a whole side by side, a share of `width` each: any part above zero keeps a cell, the biggest
 * absorbs the rounding; nothing at all, the bare track. */
export function stackCells(parts: readonly { n: number; color: number }[], width: number): string {
  const total = parts.reduce((s, p) => s + Math.max(0, p.n), 0)
  let cum = 0 // cumulative edges, so the rounding never piles up on one part
  const w = parts.map(p => {
    const from = Math.round((cum / Math.max(1, total)) * width)
    cum += Math.max(0, p.n)
    return Math.round((cum / Math.max(1, total)) * width) - from
  })
  parts.forEach((p, i) => {
    if (p.n > 0 && !w[i]) (w[i] = 1), (w[w.indexOf(Math.max(...w))]! -= 1)
  })
  const out: [string, number][] = parts.flatMap((p, i) => Array.from({ length: Math.max(0, w[i]!) }, (): [string, number] => ['━', p.color]))
  while (out.length < width) out.push(['━', C.track])
  return cells(out.slice(0, width))
}

/** T-1026: a task's steps as one bar, a segment each with a gap between when there's room: done ones green, the
 * current one in the accent (a comet sweeps it while `frame`), the ones left on the track. */
export function stepCells(steps: readonly { done: boolean; current: boolean }[], width: number, frame: number | null): string {
  const n = Math.max(1, steps.length)
  const gaps = width / n >= 3
  const out: [string, number][] = []
  for (let i = 0; i < width; i++) {
    const k = Math.floor((i * n) / width)
    const s = steps[k]
    if (gaps && k < n - 1 && Math.floor(((i + 1) * n) / width) !== k) out.push([' ', C.track])
    else if (s?.done) out.push(['━', C.ok])
    else if (s?.current) out.push(['━', frame === null ? C.accent : mix(C.accent, C.white, glow(i, width, frame) * 0.5)])
    else out.push(['━', C.track])
  }
  return cells(out)
}

/** An indeterminate bar for work with no known length: a colored comet over a dim track. */
export function activityCells(width: number, color: number, frame: number): string {
  const out: [string, number][] = []
  for (let i = 0; i < width; i++) out.push(['━', mix(C.track, color, glow(i, width, frame))])
  return cells(out)
}

/** The text twin of a bar, for surfaces without Raster: [done part, rest]. */
export function textBar(width: number, fraction: number): [string, string] {
  const done = Math.round(Math.max(0, Math.min(1, fraction)) * width)
  return ['━'.repeat(done), '─'.repeat(width - done)]
}

export function textComet(width: number, frame: number): [string, string, string] {
  const head = Math.max(0, Math.min(width, (frame % (width + 4)) - 2))
  const len = Math.min(4, width - head)
  return ['─'.repeat(head), '━'.repeat(len), '─'.repeat(width - head - len)]
}

// T-0909: the pane's charts. Each builds Raster cells (row-major) from plain numbers; a text twin draws the same for
// surfaces without Raster. `frame` may be fractional: the pane's 30 fps blit passes time in 120 ms frames.

/** Short stage names, so seven of them fit under a 50-column rail. */
const STAGE_SHORT: Record<string, string> = {
  planning: 'plan', ready: 'ready', executing: 'build', verifying: 'verify', documenting: 'docs', auditing: 'audit', closing: 'close',
}
export const stageShort = (s: string) => STAGE_SHORT[s] ?? s.slice(0, 6)

/** The column of each of `n` nodes on a rail `width` wide: spread evenly, the first at 0 and the last at the end. */
export function nodeAt(n: number, width: number): number[] {
  if (n <= 1) return [0]
  return Array.from({ length: n }, (_, i) => Math.round((i * (width - 1)) / (n - 1)))
}

/** The stage rail: ● stages behind joined by a green→accent gradient, ◉ the current one (breathing while `frame`),
 * ○ the ones ahead on a thin track; while work is live a comet runs from the current node toward the next. */
export function stageCells(n: number, current: number, width: number, frame: number | null): string {
  const at = nodeAt(n, width)
  const cur = at[Math.max(0, Math.min(n - 1, current))] ?? 0
  const next = at[current + 1] ?? cur
  const out: [string, number][] = []
  for (let i = 0; i < width; i++) {
    const node = at.indexOf(i)
    const grad = mix(C.ok, C.accent, width > 1 ? i / (width - 1) : 1)
    if (node >= 0 && node < current) out.push(['●', grad])
    else if (node >= 0 && node === current)
      out.push(['◉', frame === null ? C.accent : mix(C.accent, C.white, 0.15 + 0.35 * ((Math.sin(frame / 2.5) + 1) / 2))])
    else if (node >= 0) out.push(['○', C.dim])
    else if (i < cur) out.push(['━', grad])
    else if (i < next) {
      // the link being worked on: a comet sweeps it toward the next stage
      const span = next - cur - 1
      const d = frame === null ? -1 : ((frame * 0.8) % (span + 5)) - (i - cur - 1)
      out.push(['━', mix(C.track, C.accent, d >= 0 && d < 4 ? 1 - d / 4 : 0.12)])
    } else out.push(['─', C.track])
  }
  return cells(out)
}

export type LabelRun = { text: string; kind: 'gap' | 'done' | 'current' | 'todo' }

/** The rail's labels as runs of one kind each: every stage's short name centred under its node, a name that would
 * touch its neighbour left out (the current one always shown). */
export function stageLabels(stages: readonly string[], current: number, width: number): LabelRun[] {
  const at = nodeAt(stages.length, width)
  const row: LabelRun['kind'][] = Array(width).fill('gap')
  const chars: string[] = Array(width).fill(' ')
  const order = [current, ...stages.map((_, i) => i).filter(i => i !== current)]
  for (const i of order) {
    if (i < 0 || i >= stages.length) continue
    const name = stageShort(stages[i]!)
    const start = Math.max(0, Math.min(width - name.length, at[i]! - Math.floor(name.length / 2)))
    if (row.slice(Math.max(0, start - 1), start + name.length + 1).some(k => k !== 'gap')) continue
    for (let j = 0; j < name.length && start + j < width; j++) {
      chars[start + j] = name[j]!
      row[start + j] = i < current ? 'done' : i === current ? 'current' : 'todo'
    }
  }
  const runs: LabelRun[] = []
  row.forEach((kind, i) => {
    const last = runs.at(-1)
    if (last && last.kind === kind) last.text += chars[i]
    else runs.push({ text: chars[i]!, kind })
  })
  return runs
}

/** The rail's text twin: ● ━ ◉ ─ ○. */
export function stageText(n: number, current: number): string {
  return Array.from({ length: n }, (_, i) => (i < current ? '●' : i === current ? '◉' : '○')).join(' ─ ')
}

/** How many of `times` fall in each of `slots` equal slots of `spanMs` ending at `now`, oldest first. */
export function bucketize(times: readonly number[], now: number, spanMs: number, slots: number): number[] {
  const out = Array(slots).fill(0) as number[]
  const size = spanMs / slots
  for (const t of times) {
    const k = Math.floor((t - (now - spanMs)) / size)
    if (k >= 0 && k < slots) out[k]! += 1
    else if (k === slots) out[slots - 1]! += 1 // now itself
  }
  return out
}

// Braille dots from the bottom up, left column then right: each slot rises 1–4 dots with how busy it was
const DOTS_L = [0x40, 0x04, 0x02, 0x01]
const DOTS_R = [0x80, 0x20, 0x10, 0x08]

/** The swim lanes: one braille row per lane, two time slots per cell (so 2 × width slots), each rising 1–4 dots with its
 * count against the busiest slot, in the lane's colour (brighter the busier); a faint baseline where nothing ran. While
 * `frame`, the newest cell glows. */
export function laneCells(lanes: readonly { color: number; slots: readonly number[] }[], width: number, frame: number | null): string {
  const max = Math.max(1, ...lanes.flatMap(l => l.slots))
  const rise = (n: number) => (n > 0 ? Math.max(1, Math.min(4, Math.ceil((4 * n) / max))) : 0)
  const out: [string, number][] = []
  for (const lane of lanes) {
    for (let i = 0; i < width; i++) {
      const l = rise(lane.slots[2 * i] ?? 0)
      const r = rise(lane.slots[2 * i + 1] ?? 0)
      if (!l && !r) {
        out.push(['⣀', mix(C.track, C.dim, 0.6)]) // a floor you can see: the lane runs the whole width
        continue
      }
      const bits = DOTS_L.slice(0, l).reduce((b, x) => b | x, 0) | DOTS_R.slice(0, r).reduce((b, x) => b | x, 0)
      let color = mix(C.track, lane.color, 0.45 + (0.55 * Math.max(l, r)) / 4)
      if (frame !== null && i === width - 1) color = mix(color, C.white, 0.2 + 0.25 * ((Math.sin(frame / 2) + 1) / 2))
      out.push([String.fromCharCode(0x2800 + bits), color])
    }
  }
  return cells(out)
}

/** T-1026: a section divider: a line in the section's colour fading into the track, so sections read apart. */
export function ruleCells(width: number, color: number): string {
  const out: [string, number][] = []
  for (let i = 0; i < width; i++) out.push(['─', mix(mix(C.track, color, 0.85), C.track, width > 1 ? i / (width - 1) : 0)])
  return cells(out)
}

/** T-1023: one row of the Agents Gantt, `width` cells over [t0, t0 + span]: plain before the run started and after it
 * ended, a bar tinted in its colour between (to `now` while it runs), with braille dots where its tool calls (or a
 * brainstorm's answers) landed, two time slots a cell; a running bar's newest cell glows while `frame`. */
export function ganttCells(row: { start: number; end: number | null; marks: readonly number[]; color: number; dim?: boolean },
  t0: number, span: number, width: number, now: number, frame: number | null): string {
  const slots = width * 2
  const at = (t: number) => Math.floor(((t - t0) / Math.max(1, span)) * slots)
  const from = Math.min(slots - 1, Math.max(0, at(row.start))) // a run that starts now still shows
  const to = Math.min(slots - 1, at(row.end ?? now))
  const counts = Array(slots).fill(0) as number[]
  for (const m of row.marks) {
    const k = Math.min(slots - 1, at(m))
    if (k >= 0) counts[k]! += 1
  }
  const max = Math.max(1, ...counts)
  const rise = (n: number) => (n > 0 ? Math.max(1, Math.min(4, Math.ceil((4 * n) / max))) : 0)
  const bar = mix(0x22262d, row.color, row.dim ? 0.16 : 0.3)
  const out: [string, number, number][] = []
  for (let i = 0; i < width; i++) {
    if (2 * i + 1 < from || 2 * i > to) {
      out.push([' ', C.track, DEFAULT_BG])
      continue
    }
    const l = rise(counts[2 * i] ?? 0)
    const r = rise(counts[2 * i + 1] ?? 0)
    const bits = DOTS_L.slice(0, l).reduce((b, x) => b | x, 0) | DOTS_R.slice(0, r).reduce((b, x) => b | x, 0)
    const glow = frame !== null && row.end === null && i === Math.floor(to / 2)
    const fg = glow ? mix(row.color, C.white, 0.2 + 0.25 * ((Math.sin(frame / 2) + 1) / 2)) : row.color
    out.push([bits ? String.fromCharCode(0x2800 + bits) : glow ? '▏' : ' ', fg, glow ? mix(bar, row.color, 0.35) : bar])
  }
  return cells(out)
}

/** Column bars `rows` tall in eighth blocks, `bw` columns per value with a gap between, coloured from→to by height; a
 * zero shows as a dim floor. The newest (last) value is the brightest. */
export function barCells(values: readonly number[], rows: number, from: number, to: number, bw = 1): string {
  const max = Math.max(1, ...values)
  const width = values.length * (bw + 1) - 1
  const out: [string, number][] = []
  for (let r = 0; r < rows; r++) {
    for (let x = 0; x < width; x++) {
      const v = x % (bw + 1) === bw ? -1 : values[Math.floor(x / (bw + 1))]!
      const eighths = v > 0 ? Math.max(1, Math.round((v / max) * rows * 8)) : 0
      const level = Math.max(0, Math.min(8, eighths - (rows - 1 - r) * 8))
      if (v < 0) out.push([' ', C.track])
      else if (!level) out.push(r === rows - 1 && v === 0 ? ['▁', C.track] : [' ', C.track])
      else {
        const newest = Math.floor(x / (bw + 1)) === values.length - 1
        out.push([SPARK[level - 1]!, newest ? mix(to, C.white, 0.25) : mix(from, to, v / max)])
      }
    }
  }
  return cells(out)
}

/** Time on a task against its usual: filled to `elapsed`, a ┃ ghost where the usual time falls; past it the fill turns
 * amber. Both in minutes. */
export function etaCells(width: number, elapsed: number, usual: number): string {
  const scale = Math.max(elapsed, usual) * 1.15 || 1
  const mark = Math.max(0, Math.min(width - 1, Math.round((usual / scale) * (width - 1))))
  const fill = Math.round((Math.max(0, elapsed) / scale) * width)
  const out: [string, number][] = []
  for (let i = 0; i < width; i++) {
    const lit = i < fill
    if (i === mark) out.push(['┃', lit ? C.white : mix(C.dim, C.white, 0.35)])
    else out.push(['━', !lit ? C.track : i > mark ? C.warn : mix(C.accent2, C.ok, width > 1 ? i / (width - 1) : 1)])
  }
  return cells(out)
}

// Claude Code's own spinner glyphs, breathing out and back: the band and rows match the working line.
const SPIN = ['·', '✢', '✳', '✶', '✻', '✽', '✻', '✶', '✳', '✢']
export const spin = (frame: number) => SPIN[frame % SPIN.length]!

/** What comes next, for a person: fm's next line without the agent's own instructions after it. */
export const humanNext = (next: string) => next.split(' — ')[0]!.replace(/\s*\(procedure:.*$/, '').trim()

export function elapsed(ms: number): string {
  const s = Math.max(0, ms) / 1000
  if (s < 10) return `${s.toFixed(1)}s`
  if (s < 60) return `${Math.round(s)}s`
  if (s >= 3600) return `${Math.floor(s / 3600)}h ${String(Math.floor((s % 3600) / 60)).padStart(2, '0')}m`
  return `${Math.floor(s / 60)}m ${String(Math.round(s % 60)).padStart(2, '0')}s`
}

/** A typical duration in minutes, roughly: ~25m, ~1.5h. */
export const about = (min: number) => (min < 60 ? `~${Math.max(1, Math.round(min))}m` : `~${(min / 60).toFixed(1).replace(/\.0$/, '')}h`)
/** '9h ago', '3d ago' */
export const hoursAgo = (h: number) => (h < 24 ? `${Math.max(1, Math.round(h))}h ago` : `${Math.round(h / 24)}d ago`)
// T-0228: token counts as words a glance reads: 950 · 12k · 4.0M
export const tokensWord = (n: number) => (n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${Math.round(n / 1e3)}k` : `${n}`)

export function shortPath(path: string, max = 48): string {
  if (path.length <= max) return path
  const parts = path.split('/')
  const name = parts.pop() ?? path
  const dir = parts.pop()
  const tail = dir ? `…/${dir}/${name}` : name
  return tail.length <= max ? tail : `…${tail.slice(-(max - 1))}`
}

const lines = (s: unknown) => (typeof s === 'string' && s.length ? s.split('\n').length : 0)
const str = (o: Record<string, unknown>, k: string) => (typeof o[k] === 'string' ? (o[k] as string) : '')

export type Face = { icon: string; verb: string; target: string; color: number; delta?: string; add?: number; del?: number }

/** How a tool call reads while it runs: an icon, a verb, its target, a color, and for edits the line delta. */
/** `cwd`: the session's folder; a path inside it is shown relative to it, as Claude Code's own rows do */
export function toolFace(tool: string, input: unknown, cwd = ''): Face {
  const o = (input && typeof input === 'object' ? input : {}) as Record<string, unknown>
  const raw = str(o, 'file_path') || str(o, 'notebook_path') || str(o, 'path')
  const file = shortPath(cwd && raw.startsWith(`${cwd}/`) ? raw.slice(cwd.length + 1) : raw)
  const first = (s: string) => s.split('\n')[0]!.slice(0, 80)
  switch (tool) {
    case 'Edit':
    case 'MultiEdit': {
      const edits = Array.isArray(o.edits) ? (o.edits as Record<string, unknown>[]) : [o]
      const add = edits.reduce((n, x) => n + lines(x.new_string), 0)
      const del = edits.reduce((n, x) => n + lines(x.old_string), 0)
      return { icon: '✎', verb: 'Editing', target: file, color: C.edit, delta: `+${add} −${del}`, add, del }
    }
    case 'Write':
      return { icon: '✎', verb: 'Writing', target: file, color: C.edit, delta: `+${lines(o.content)}`, add: lines(o.content), del: 0 }
    case 'NotebookEdit':
      return { icon: '✎', verb: 'Editing', target: file, color: C.edit }
    case 'Bash':
      return { icon: '❯', verb: 'Running', target: first(str(o, 'description') || str(o, 'command')), color: C.accent }
    case 'Read':
      return { icon: '◔', verb: 'Reading', target: file, color: C.accent2 }
    case 'Grep':
      return { icon: '⌕', verb: 'Searching', target: first(str(o, 'pattern')), color: C.accent2 }
    case 'Glob':
      return { icon: '⌕', verb: 'Finding', target: first(str(o, 'pattern')), color: C.accent2 }
    case 'WebFetch':
      return { icon: '◍', verb: 'Fetching', target: str(o, 'url').replace(/^https?:\/\//, '').slice(0, 60), color: C.web }
    case 'WebSearch':
      return { icon: '◍', verb: 'Searching the web', target: first(str(o, 'query')), color: C.web }
    case 'Agent':
    case 'Task': {
      const who = str(o, 'subagent_type')
      return { icon: '◆', verb: 'Subagent', target: [who, str(o, 'description')].filter(Boolean).join(': '), color: C.agent }
    }
    case 'AskUserQuestion': // T-0909: it waits on the person; it isn't work running
      return { icon: '⚠', verb: 'Waiting for your answer', target: '', color: C.warn }
    case 'Skill':
      return { icon: '✦', verb: 'Skill', target: str(o, 'skill'), color: C.agent }
    default: {
      const m = /^mcp__(.+?)__(.+)$/.exec(tool)
      return m
        ? { icon: '⬡', verb: m[2]!, target: m[1]!, color: C.web }
        : { icon: '•', verb: tool, target: '', color: C.dim }
    }
  }
}

/** A border that breathes while work is live: track ↔ color on a slow sine; still when `frame` is null. */
/** A panel border in a row's colour, held back over the track so the replies' panels stay the loudest (T-0179). */
export const tint = (color: number): number => mix(C.track, color, 0.5)

export function pulse(color: number, frame: number | null): number {
  if (frame === null) return mix(C.track, color, 0.55)
  return mix(C.track, color, 0.45 + 0.55 * ((Math.sin(frame / 4) + 1) / 2))
}

/** Newest bright, oldest dim: the color of row `i` of `n` (0 = oldest). */
export function fade(i: number, n: number, color: number = C.accent): number {
  return mix(C.dim, color, n > 1 ? i / (n - 1) : 1)
}

const SPARK = '▁▂▃▄▅▆▇█'

/** A sparkline over the last `width` values, each column colored by its height (green → amber → red). */
export function sparkCells(values: readonly number[], width: number): string {
  const vals = values.slice(-width)
  const max = Math.max(1, ...vals)
  const out: [string, number][] = []
  for (let i = 0; i < width; i++) {
    const v = vals[i - (width - vals.length)]
    if (v === undefined) {
      out.push([' ', C.track])
      continue
    }
    const t = v / max
    out.push([SPARK[Math.min(SPARK.length - 1, Math.floor(t * SPARK.length))]!, heat(t)])
  }
  return cells(out)
}

export function sparkText(values: readonly number[], width: number): string {
  const vals = values.slice(-width)
  const max = Math.max(1, ...vals)
  return vals.map(v => SPARK[Math.min(SPARK.length - 1, Math.floor((v / max) * SPARK.length))]).join('')
}

/** green → amber → red as a meter fills. */
export function heat(t: number): number {
  return t < 0.5 ? mix(C.ok, C.warn, t * 2) : mix(C.warn, C.err, (t - 0.5) * 2)
}

/** A two-tone bar for an edit: green for lines added, red for lines removed, scaled to `max` lines. */
export function churnCells(add: number, del: number, max: number, width: number): string {
  const scale = width / Math.max(1, max)
  const a = Math.min(width, Math.round(add * scale) || (add ? 1 : 0))
  const d = Math.min(width - a, Math.round(del * scale) || (del ? 1 : 0))
  const out: [string, number][] = []
  for (let i = 0; i < width; i++) out.push(['━', i < a ? C.ok : i < a + d ? C.err : C.track])
  return cells(out)
}

export function ago(days: number | undefined): string {
  if (days === undefined) return ''
  return days < 1 ? 'today' : `${Math.round(days)}d`
}

/** What a tier letter means, in words people read (S/M/L meant nothing on screen). */
export const SIZE: Record<string, string> = { S: 'small', M: 'medium', L: 'large' }
export const sizeWord = (tier: string) => SIZE[tier] ?? tier

/** T-0989, T-1000, T-1002: the pane's row budget. One panel that fills the dock exactly: the head (its third row the
 * attention row) and the controls take 4 rows; every section but a `bare` one (the task under the head) gets a titled
 * divider, and on a tall dock (40 rows up) a blank row above it, under the head and above the controls. Sections take
 * the rows they hold: each its `min` (2) first, then up to its `cap` in order; a `fixed` one its height, and the
 * `stretch` one (the history) what it holds of the rest; rows still spare go to the `grow` ones (more lanes, taller
 * charts) up to their allowance, then pad the history (or the task). When sections get no rows the least important
 * (last) of them is dropped and the rest placed again, so its divider goes to the others. */
export type Part = { key: string; want: number; cap?: number; min?: number; fixed?: number; stretch?: boolean; bare?: boolean; grow?: number }
export function layout(rows: number, parts: Part[]): { gap: number; rows: Record<string, number> } {
  const h = Math.max(0, Math.floor(rows))
  const gap = h >= 40 ? 1 : 0
  let shown = parts.filter(p => p.want > 0 || p.fixed)
  let out: Record<string, number> = {}
  for (let pass = 0; pass < parts.length + 1; pass++) {
    const titled = shown.filter(p => !p.bare).length
    let r = Math.max(0, h - 4 - 2 * gap - titled * (1 + gap))
    out = {}
    for (const p of shown) if (p.fixed) r -= out[p.key] = Math.min(p.fixed, r)
    const flex = shown.filter(p => !p.fixed && !p.stretch)
    for (const p of flex) r -= out[p.key] = Math.max(0, Math.min(p.want, p.cap ?? p.want, p.min ?? 2, r)) // each its minimum first
    for (const p of flex) { // then up to its cap, in order
      const more = Math.max(0, Math.min(Math.min(p.want, p.cap ?? p.want) - out[p.key]!, r))
      out[p.key] = out[p.key]! + more
      r -= more
    }
    const stretch = shown.find(p => p.stretch)
    if (stretch) r -= out[stretch.key] = Math.min(stretch.want, r) // what it holds
    for (const p of shown) if (p.grow) { // spare rows: more of the charts, up to each one's `grow`
      const more = Math.min(p.grow, r)
      out[p.key] = (out[p.key] ?? 0) + more
      r -= more
    }
    const spare = stretch ?? shown.find(p => p.bare) // then blank rows under the history, or under the task
    if (spare) out[spare.key] = (out[spare.key] ?? 0) + r
    const empty = shown.filter(p => !out[p.key])
    if (!empty.length) break
    const last = empty.at(-1)! // the least important goes first; its divider frees rows for the others
    shown = shown.filter(p => p !== last)
  }
  return { gap, rows: Object.fromEntries(parts.map(p => [p.key, out[p.key] ?? 0])) }
}

/** T-1002: level gauges as tanks side by side, `rows` tall and `width` wide each, `gap` apart: each fills from the
 * bottom in eighths to its fraction, in its colour, over a dim slot that shows where full is. */
export function tankCells(levels: readonly { frac: number; color: number }[], rows: number, width: number, gap: number): string {
  const out: [string, number, number][] = []
  const slot = mix(C.track, 0x1a1d24, 0.35)
  for (let r = 0; r < rows; r++) {
    levels.forEach((l, i) => {
      if (i) for (let g = 0; g < gap; g++) out.push([' ', C.track, DEFAULT_BG])
      const eighths = l.frac > 0 ? Math.max(1, Math.round(Math.min(1, l.frac) * rows * 8)) : 0
      const level = Math.max(0, Math.min(8, eighths - (rows - 1 - r) * 8))
      for (let x = 0; x < width; x++) out.push(level >= 8 ? ['█', l.color, slot] : level ? [SPARK[level - 1]!, l.color, slot] : [' ', l.color, slot])
    })
  }
  return cells(out)
}

// The mascot: Claude Code's own welcome-screen Claude, in block glyphs (9 wide, 3 rows), padded to 11 so it can sway.
const POSES: Record<string, [string, string, string]> = {
  rest: [' ▐▛███▜▌ ', '▝▜█████▛▘', '  ▘▘ ▝▝  '],
  blink: [' ▐█████▌ ', '▝▜█████▛▘', '  ▘▘ ▝▝  '],
  up: ['▗▐▛███▜▌▖', ' ▜█████▛ ', '  ▘▘ ▝▝  '],
  waveL: ['▗▐▛███▜▌ ', ' ▜█████▛▘', '  ▘▘ ▝▝  '],
  waveR: [' ▐▛███▜▌▖', '▝▜█████▛ ', '  ▘▘ ▝▝  '],
  step: [' ▐▛███▜▌ ', '▝▜█████▛▘', '  ▝▝ ▘▘  '],
}
// Working: a little dance, one move every three frames (~360 ms). [pose, sway]
const DANCE: [string, number][] = [
  ['rest', 0], ['waveL', -1], ['rest', 0], ['waveR', 1], ['up', 0], ['step', 0], ['up', 0], ['step', 0],
]
export const MASCOT_COLORS: Record<string, number> = { blue: 0x4f9dff, orange: 0xd97757, purple: 0xa88bfa, green: 0x5fd7a0 }

/** The mascot's three rows: working dances, idle rests and blinks now and then, a finished task cheers. */
export function clawd(state: 'work' | 'idle' | 'happy', beat: number): string[] {
  const [pose, dx] =
    state === 'work' ? DANCE[Math.floor(beat / 3) % DANCE.length]!
    : state === 'happy' ? (['up', beat % 2 ? 1 : -1] as [string, number])
    : [beat % 7 === 3 ? 'blink' : 'rest', 0]
  return POSES[pose]!.map(r => ' '.repeat(1 + dx) + r + ' '.repeat(1 - dx))
}

/** A subagent's mini Claude (7 wide, 2 rows), flapping its arms on its own beat. */
export function miniClawd(beat: number): string[] {
  return beat % 2 ? ['▗▐▛█▜▌▖', ' ▜███▛ '] : [' ▐▛█▜▌ ', '▝▜███▛▘']
}

const MINI_COLORS = [0xff6b9d, 0xffd75f, 0x5fd7a0, 0xc792ea, 0xff9f43, 0x4fd1ff, 0xf368e0, 0x9be15d]
/** A random-looking color that stays the same for one subagent. */
export function agentColor(id: string): number {
  let h = 0x811c9dc5 // FNV-1a: neighbouring ids land far apart
  for (const ch of id) h = Math.imul(h ^ ch.charCodeAt(0), 16777619)
  return MINI_COLORS[(h >>> 0) % MINI_COLORS.length]!
}

// T-0123: a shell command's output as a summary. A line's tone: failures, warnings, passes, the rest.
export type Tone = 'err' | 'warn' | 'ok' | 'plain'
// T-0144: every escape sequence, C0/C1 controls, bidi overrides and zero-width or direction marks
// CSI (7- or 8-bit), the string forms OSC/DCS/SOS/PM/APC up to BEL or ST (a terminal swallows an unterminated one
// the same way), then any other ESC form (charset switches, ESC c, a stray ST)
const ESC_SEQ =
  /(?:\u001b\[|\u009b)[0-?]*[ -\/]*[@-~]|(?:\u001b[\]PX^_]|[\u0090\u0098\u009d-\u009f])[^\u0007\u001b\u009c]*(?:\u0007|\u001b\\|\u009c)?|\u001b[ -\/]*[0-~]/g
/** Text safe to draw: no escape sequences, control or bidi characters (a line could otherwise read as something else
 * or be refused); tabs as two spaces */
export const clean = (t: string) =>
  t.replace(ESC_SEQ, '').replace(/\t/g, '  ').replace(/[\u0000-\u001f\u007f-\u009f\u061c\u200b-\u200f\u202a-\u202e\u2066-\u2069]/g, '')

export function tone(line: string): Tone {
  if (/\b0 (?:errors?|fail(?:s|ed|ures?)?)\b/i.test(line)) return 'ok' // ' 0 fail' read as a failure (live render)
  if (/\b(?:error|errors|failed|failure|failures|fatal|panic(?:ked)?|traceback|exception)\b|✗|✘|\bFAIL\b/i.test(line)) return 'err'
  if (/\bwarn(?:ing)?s?\b|⚠/i.test(line)) return 'warn'
  if (/\b(?:ok|passed|success(?:ful)?|done)\b|✓|✔|\bPASS\b/i.test(line)) return 'ok'
  return 'plain'
}

/** The lines that matter (failures first, else the tail) of stdout and stderr, colour codes stripped. */
/** `failuresFirst` only for a command that failed: a zero exit that mentions an exception (a grep, a listing) succeeded */
export function outputSummary(stdout: unknown, stderr: unknown, keep = 6, failuresFirst = true) {
  const all = [stdout, stderr]
    .filter((x): x is string => typeof x === 'string')
    .join('\n')
    .split('\n')
    .map(l => clean(l.replace(/\r$/, '').split('\r').at(-1) ?? '').trimEnd()) // after a \r: what a terminal shows
    .filter(l => l.trim())
  const bad = failuresFirst ? all.filter(l => tone(l) === 'err') : []
  const pick = bad.length ? bad.slice(0, keep) : all.slice(-keep)
  return {
    lines: pick.map(text => ({ text: text.slice(0, 240), tone: tone(text) })),
    total: all.length,
    more: all.length - pick.length,
    failures: bad.length > 0,
  }
}

/** T-0141: the changed lines of an edit's structuredPatch, numbered as the file is (removals by the old file, additions
 * by the new), unchanged context left out; text cleaned for a Text (tabs as two spaces, no other control characters, no
 * bidi overrides that could make a line read as something else) */
export function changedLines(hunks: unknown): { n: number; sign: '+' | '-'; text: string }[] {
  const out: { n: number; sign: '+' | '-'; text: string }[] = []
  const tidy = (t: string) => clean(t).slice(0, 240)
  for (const h of Array.isArray(hunks) ? (hunks as { oldStart?: unknown; newStart?: unknown; lines?: unknown }[]) : []) {
    let o = typeof h?.oldStart === 'number' ? h.oldStart : 1
    let n = typeof h?.newStart === 'number' ? h.newStart : 1
    for (const l of Array.isArray(h?.lines) ? h.lines : []) {
      if (typeof l !== 'string' || l.startsWith('\\')) continue // '\ No newline at end of file'
      if (l.startsWith('-')) out.push({ n: o++, sign: '-', text: tidy(l.slice(1)) })
      else if (l.startsWith('+')) out.push({ n: n++, sign: '+', text: tidy(l.slice(1)) })
      else (o++, n++)
    }
  }
  return out
}

export type DiffRow = { kind: 'hunk' } | { kind: 'ctx'; n: number; text: string } | { kind: '+' | '-'; n: number; text: string; mid?: [number, number] }

/** T-1031: a patch as rows to draw: `context` lines either side of each change, a break where lines are skipped, and
 * for a changed line (a run of removals followed by as many additions) the whole words that differ, as `mid`. */
export function diffRows(hunks: unknown, context = 1): DiffRow[] {
  const out: DiffRow[] = []
  const tidy = (t: string) => clean(t).slice(0, 240)
  for (const h of Array.isArray(hunks) ? (hunks as { oldStart?: unknown; newStart?: unknown; lines?: unknown }[]) : []) {
    let o = typeof h?.oldStart === 'number' ? h.oldStart : 1
    let n = typeof h?.newStart === 'number' ? h.newStart : 1
    const rows: DiffRow[] = []
    for (const l of Array.isArray(h?.lines) ? h.lines : []) {
      if (typeof l !== 'string' || l.startsWith('\\')) continue // '\ No newline at end of file'
      if (l.startsWith('-')) rows.push({ kind: '-', n: o++, text: tidy(l.slice(1)) })
      else if (l.startsWith('+')) rows.push({ kind: '+', n: n++, text: tidy(l.slice(1)) })
      else rows.push({ kind: 'ctx', n: (o++, n++), text: tidy(l.slice(1)) })
    }
    const near = (i: number) => rows.slice(Math.max(0, i - context), i + context + 1).some(r => r.kind !== 'ctx')
    let last = -1
    rows.forEach((r, i) => {
      if (r.kind === 'ctx' && !near(i)) return
      if ((last >= 0 ? last < i - 1 : out.length > 0) && out.at(-1)?.kind !== 'hunk') out.push({ kind: 'hunk' })
      out.push(r)
      last = i
    })
  }
  for (let i = 0; i < out.length; ) { // pair a run of k removals with the k additions after it
    let k = 0
    while (out[i + k]?.kind === '-') k++
    let m = 0
    while (out[i + k + m]?.kind === '+') m++
    if (k && k === m)
      for (let j = 0; j < k; j++) {
        const a = out[i + j] as { text: string; mid?: [number, number] }
        const b = out[i + k + j] as { text: string; mid?: [number, number] }
        let p = 0
        while (p < a.text.length && p < b.text.length && a.text[p] === b.text[p]) p++
        let s = 0
        while (s < a.text.length - p && s < b.text.length - p && a.text[a.text.length - 1 - s] === b.text[b.text.length - 1 - s]) s++
        while (p > 0 && /\w/.test(a.text[p - 1]!)) p-- // whole words
        while (s > 0 && /\w/.test(a.text[a.text.length - s]!)) s--
        if (p + s >= 3) (a.mid = [p, a.text.length - s]), (b.mid = [p, b.text.length - s])
      }
    i += Math.max(1, k + m)
  }
  return out
}

/** T-0143: one part of a Foreman report line in a reply (Changed:, ✓/✗, ⚑ Captured, ◆ Decided, Next:, ⚠ Needs you) */
export type ReplyPart = { text: string; color?: number; bold?: boolean }
export type ReplyBlock = { kind: 'md'; text: string } | { kind: 'line'; parts: ReplyPart[] } | { kind: 'gap' }

function reportLine(line: string): ReplyPart[] | null {
  const t = line.replace(/`/g, '').trimEnd()
  let m: RegExpExecArray | null
  if ((m = /^Changed: (.+?) — (.+)$/.exec(t)))
    return [{ text: '✎', color: C.edit }, { text: ' changed ', color: C.dim }, { text: m[1]!, color: C.accent }, { text: ` — ${m[2]}`, color: C.dim }]
  if ((m = /^([✓✗]) (.+?)(?: → (.+))?$/.exec(t)))
    return [{ text: m[1]!, color: m[1] === '✓' ? C.ok : C.err }, { text: ` ${m[2]}` }, ...(m[3] ? [{ text: ` → ${m[3]}`, color: C.dim }] : [])]
  if ((m = /^⚑ Captured (T-\d+) — (.+)$/.exec(t)))
    return [{ text: '⚑', color: C.warn }, { text: ' captured ', color: C.dim }, { text: m[1]!, color: C.accent }, { text: ` ${m[2]}` }]
  if ((m = /^◆ Decided: (.+)$/.exec(t))) return [{ text: '◆', color: C.agent }, { text: ' decided ', color: C.dim }, { text: m[1]! }]
  if ((m = /^Next: (.+)$/.exec(t))) return [{ text: '→', color: C.accent }, { text: ' next ', color: C.dim }, { text: m[1]! }]
  if ((m = /^⚠ Needs you: (.+)$/.exec(t)))
    return [{ text: '⚠', color: C.warn }, { text: ' needs you ', color: C.warn }, { text: m[1]!, bold: true }]
  return null
}

/** A reply's text as markdown runs and Foreman report lines (outside code fences), in order; a blank line between
 * two of them stays as a gap (live: the groups ran together without it) */
export function replyBlocks(text: string): ReplyBlock[] {
  const out: ReplyBlock[] = []
  let md: string[] = []
  let fence = false
  let blank = false
  const flush = () => {
    const t = md.join('\n').trim()
    if (t) out.push({ kind: 'md', text: t })
    md = []
  }
  for (const raw of text.split('\n')) {
    if (/^\s*```/.test(raw)) fence = !fence
    const parts = fence ? null : reportLine(raw)
    if (parts) {
      flush()
      if (blank && out.length) out.push({ kind: 'gap' })
      out.push({ kind: 'line', parts })
    } else if (!raw.trim() && !fence) {
      if (md.length) md.push(raw) // a paragraph break inside markdown
      blank = true
      continue
    } else {
      if (!md.length && blank && out.length) out.push({ kind: 'gap' })
      md.push(raw)
    }
    blank = false
  }
  flush()
  return out
}

export const TONE_COLOR: Record<Tone, number> = { err: C.err, warn: C.warn, ok: C.ok, plain: 0xc8ccd4 }
