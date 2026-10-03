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
  dim: 0x6c7686,
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
export const SIZE_LEGEND = 'small ≤30 lines, 1–2 files · medium several files or a design choice · large cross-cutting or uncertain'

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
