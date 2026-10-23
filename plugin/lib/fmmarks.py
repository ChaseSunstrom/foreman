"""fm marks (T-1555): a project's marks, offline and stdlib only.

    fm marks icons [--out DIR] [--stroke W]   each icon as NAME.svg, and icons.svg holding them all as <symbol>s
    fm marks empty [--out DIR] [--stroke W]   empty-state illustrations built from the same icons
    fm marks wordmark NAME [--out FILE]       the name set beside a monogram tile, in a hue drawn from the name
    fm marks fonts [--subset FONT --text TEXT --out FILE]   the font shelf: vetted pairings against the families
                                              installed here (fc-list), and a subset for self-hosting (fontTools)

Every icon is drawn on one 24-unit grid, 2 units in from each edge, as stroked paths only: one stroke width, round
caps and joins, no fill, currentColor, so the set is consistent by construction and takes its colour from the page.
Nothing is fetched or installed: fc-list and fontTools are used when present and said to be missing when not."""
import html
import os
import shutil
import subprocess

GRID = 24
ICONS = {  # paths on the 24 grid, 2 in from each edge
    "home": "M3 11L12 3l9 8M5 9.5V21h5v-6h4v6h5V9.5",
    "search": "M10.5 4a6.5 6.5 0 1 1 0 13a6.5 6.5 0 1 1 0-13zM15.5 15.5L21 21",
    "settings": "M4 6h9M17 6h3M15 4v4M4 12h3M11 12h9M9 10v4M4 18h11M19 18h1M17 16v4",  # sliders
    "user": "M12 4a4 4 0 1 1 0 8a4 4 0 1 1 0-8zM4 21c0-4.4 3.6-7 8-7s8 2.6 8 7",
    "check": "M4 12.5l5 5L20 6.5",
    "close": "M5 5l14 14M19 5L5 19",
    "plus": "M12 4v16M4 12h16",
    "minus": "M4 12h16",
    "arrow-left": "M20 12H4M10 6l-6 6l6 6",
    "arrow-right": "M4 12h16M14 6l6 6l-6 6",
    "menu": "M3 6h18M3 12h18M3 18h18",
    "trash": "M4 7h16M9 7V4h6v3M6 7l1 14h10l1-14M10 11v6M14 11v6",
    "edit": "M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4",
    "download": "M12 3v12M7 10l5 5l5-5M4 21h16",
    "upload": "M12 21V9M7 14l5-5l5 5M4 3h16",
    "info": "M12 3a9 9 0 1 1 0 18a9 9 0 1 1 0-18zM12 11v6M12 7.5v.5",
    "warning": "M12 3l10 18H2zM12 10v5M12 18v.5",
    "inbox": "M3 13l3-8h12l3 8v7H3zM3 13h5l1 3h6l1-3h5",
    "cloud-off": "M3 3l18 18M7 18h10a4 4 0 0 0 1.5-7.7A6 6 0 0 0 8 8.2M5.6 10.6A4 4 0 0 0 7 18",
}
LINE = 36  # characters of an empty state's line that fit its 240 width at 12px
EMPTY = {  # name: (icon, title, the one line under it, at most LINE characters)
    "no-results": ("search", "Nothing matches", "Try fewer words or another spelling."),
    "empty-inbox": ("inbox", "All clear", "New items will show up here."),
    "offline": ("cloud-off", "You're offline", "Changes sync when you're back."),
    "all-done": ("check", "All done", "Nothing is left to do."),
}
PAIRINGS = [  # (heading, body, why): vetted pairings, each free to self-host
    ("Inter", "Source Serif 4", "a UI sans with a reading serif for long text"),
    ("IBM Plex Sans", "IBM Plex Serif", "one superfamily: matched metrics, a technical voice"),
    ("Noto Sans", "Noto Serif", "every script, so nothing falls back mid-sentence"),
    ("Source Sans 3", "Source Serif 4", "Adobe's matched pair: calm and legible"),
    ("Work Sans", "Lora", "a friendly grotesque over a brushed serif"),
    ("Space Grotesk", "Space Mono", "a technical display with its own mono"),
    ("Fira Sans", "Fira Mono", "a humanist sans and its code face"),
    ("Adwaita Sans", "Adwaita Mono", "GNOME's own pair, already on many Linux desktops"),
]
_attrs = 'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"'


def icon_svg(name, stroke=2.0, size=GRID):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {GRID} {GRID}" '
            f'{_attrs} stroke-width="{stroke:g}" aria-hidden="true"><path d="{ICONS[name]}"/></svg>\n')


def sprite(stroke=2.0):
    """All the icons as <symbol>s in one file: <svg><use href="icons.svg#home"/></svg> draws one."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
            + "".join(f'<symbol id="{n}" viewBox="0 0 {GRID} {GRID}" {_attrs} stroke-width="{stroke:g}">'
                      f'<path d="{d}"/></symbol>\n' for n, d in ICONS.items()) + "</svg>\n")


def empty_svg(name, stroke=2.0):
    """One empty state, 240x180: its icon three times its size on a soft disc (the stroke scaled back, so it matches
    the icons'), a title and one line, in currentColor."""
    icon, title, line = EMPTY[name]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="240" height="180" viewBox="0 0 240 180" role="img" '
            f'aria-label="{html.escape(title)}"><circle cx="120" cy="66" r="50" fill="currentColor" opacity=".08"/>'
            f'<g transform="translate(84 30) scale(3)" {_attrs} stroke-width="{stroke / 3:g}"><path d="{ICONS[icon]}"/>'
            f'</g><text x="120" y="146" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" '
            f'font-weight="600" fill="currentColor">{html.escape(title)}</text><text x="120" y="168" '
            f'text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="currentColor" '
            f'opacity=".7">{html.escape(line)}</text></svg>\n')


def wordmark(name):
    """The project's wordmark: a monogram tile and the name, both in one hue drawn from the name (the same name, the
    same mark), set in the system's UI face."""
    name = " ".join(str(name).split())[:40] or "Untitled"
    hue = sum(map(ord, name)) * 47 % 360
    width = 96 + 25 * len(name)
    first = html.escape(name[0].upper())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="72" viewBox="0 0 {width} 72" role="img" '
            f'aria-label="{html.escape(name)}"><rect x="4" y="4" width="64" height="64" rx="16" '
            f'fill="hsl({hue} 55% 42%)"/><text x="36" y="50" text-anchor="middle" font-family="system-ui, sans-serif" '
            f'font-size="38" font-weight="700" fill="#ffffff">{first}</text><text x="84" y="50" '
            f'font-family="system-ui, -apple-system, \'Segoe UI\', sans-serif" font-size="40" font-weight="700" '
            f'letter-spacing="-0.5" fill="hsl({hue} 45% 22%)">{html.escape(name)}</text></svg>\n')


def installed():
    """The font families installed here (fc-list), or None when fc-list isn't."""
    tool = shutil.which("fc-list")
    if not tool:
        return None
    try:
        out = subprocess.run([tool, ":", "family"], capture_output=True, text=True, timeout=20).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return {f.strip() for line in out.splitlines() for f in line.split(",") if f.strip()}


def shelf(families=None):
    """[{heading, body, why, have: [installed?, installed?]}]: the vetted pairings, each marked by what is installed."""
    families = installed() if families is None else families
    return [{"heading": h, "body": b, "why": w, "have": None if families is None else [h in families, b in families]}
            for h, b, w in PAIRINGS]


def subset(font, text, out):
    """A subset of font holding only text's characters, as WOFF2 when brotli is installed (else the font's own
    format), for self-hosting; needs fontTools, never installed here."""
    try:
        from fontTools import subset as ft
    except ImportError:
        raise RuntimeError("subsetting needs fontTools (pip install fonttools brotli), which isn't installed; "
                           f"the recipe: pyftsubset {font} --text='…' --flavor=woff2 --output-file={out}")
    args = [font, f"--text={text}", f"--output-file={out}", "--layout-features=*"]
    try:
        import brotli  # noqa: F401
        args.append("--flavor=woff2")
    except ImportError:
        pass
    ft.main(args)
    return out


def _write(folder, name, text):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def cmd_marks(args):
    import fmcli
    words = list(args.words or [])
    what = words[0] if words else ""
    stroke = args.stroke if args.stroke is not None else 2.0
    if not 0.5 <= stroke <= 4:
        raise fmcli.UsageError("--stroke takes 0.5 to 4 grid units")
    if what == "icons":
        folder = args.out or "icons"
        paths = [_write(folder, f"{n}.svg", icon_svg(n, stroke)) for n in ICONS] + [_write(folder, "icons.svg",
                                                                                          sprite(stroke))]
        return fmcli.out(args, {"icons": list(ICONS), "files": paths},
                         f"wrote {len(ICONS)} icons and icons.svg to {folder} (24 grid, stroke {stroke:g}, currentColor)")
    if what == "empty":
        folder = args.out or "empty-states"
        paths = [_write(folder, f"{n}.svg", empty_svg(n, stroke)) for n in EMPTY]
        return fmcli.out(args, {"empty": list(EMPTY), "files": paths},
                         f"wrote {len(paths)} empty states to {folder}: {', '.join(EMPTY)}")
    if what == "wordmark":
        if len(words) < 2:
            raise fmcli.UsageError("fm marks wordmark NAME [--out FILE]")
        text = wordmark(" ".join(words[1:]))
        if args.out:
            _write(os.path.dirname(os.path.abspath(args.out)), os.path.basename(args.out), text)
            return fmcli.out(args, {"out": args.out}, f"wrote {args.out}")
        return fmcli.out(args, {"svg": text}, text.rstrip("\n"))
    if what == "fonts":
        if args.subset:
            if not (args.text and args.out):
                raise fmcli.UsageError("fm marks fonts --subset FONT --text TEXT --out FILE")
            try:
                subset(args.subset, args.text, args.out)
            except (RuntimeError, OSError) as e:
                raise fmcli.UsageError(str(e))
            return fmcli.out(args, {"out": args.out}, f"wrote {args.out}: {len(set(args.text))} characters")
        rows = shelf()
        mark = lambda h: "?" if h is None else "✓" if h else "·"  # noqa: E731
        return fmcli.out(args, {"pairings": rows, "fc_list": rows[0]["have"] is not None}, "\n".join(
            [f"Font shelf (✓ installed here, · not{'' if rows[0]['have'] is not None else '; fc-list is missing'}):"]
            + [f"  {mark(r['have'] and r['have'][0])} {r['heading']} + {mark(r['have'] and r['have'][1])} {r['body']}: "
               f"{r['why']}" for r in rows]
            + ["Self-host one: fm marks fonts --subset FONT --text 'the characters you use' --out FILE (fontTools)"]))
    raise fmcli.UsageError("fm marks icons|empty|wordmark NAME|fonts (fm marks -h)")
