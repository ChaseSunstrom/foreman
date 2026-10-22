"""T-1496: every setting Foreman's two UIs read, in one schema: the fm code app's tui.toml (in Foreman's home) and the
foreman-ui mod's userConfig (Claude Code keeps its values in settings.json pluginConfigs). Where the two overlap
(motion, palette) they share one name and one value set; an old word is still read (the mod's "calm" is reduced).

A tui.toml change is made in place: one key's value replaced (or the key added to its table, the table to the file),
comments, order and every other byte kept; it is refused unless load_config takes the new text and the app draws with
it. settings.json is Claude Code's own file, which the guard protects: a plugin change is written only when the guard
would allow that write, and otherwise printed as the change to make. Stdlib only.

T-1510: fm settings diff (the keys the files change from the defaults; a key nothing reads is flagged dead), export
and import (a share code: those keys as one pasteable word, every key and value checked before any is written) and
undo (each set or import is one entry of a history in Foreman's state; undo puts the last one back).

T-1543: settings safety. Each start the app draws with keeps tui.toml as the last good copy (in Foreman's state); one it
can't draw with starts that copy instead and says so, the file left as written. An edit made to tui.toml while the app
runs is read back into it (applied when it can draw with it); a write from the app names the text it last saw, and a
key changed there since is refused, never overwritten unseen. fm settings bisect names the setting that breaks the
screen: the changes from the last good copy tried in halves, each on a temporary file.

T-1656: profiles. [profile.NAME] tables in tui.toml, each a when clause on the terminal (WHEN, matched against facts())
and settings; load_config applies the first one the terminal meets after the file's own, through the same checks (a
profile's theme or palette starts the colours afresh, as the file's own does). fm settings profile lists them."""
import base64
import contextlib
import json
import math
import os
import re
import stat
import sys
import tempfile
import tomllib

SHARED = {
    "motion": {"choices": ("full", "reduced", "off"), "aliases": {"calm": "reduced"},
               "help": "full: everything moves; reduced: less (the app: nothing moves; the pane: the 8 fps clock); "
                       "off: still"},
    "palette": {"choices": ("default", "cb", "riso"), "aliases": {},
                "help": "default: green and red for pass and fail; cb: blue and orange, safe with colour blindness; "
                        "riso: risograph inks, green and fluorescent pink"},
}
PLUGIN = "foreman-ui"
_MOD_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "mods", PLUGIN,
                         ".claude-plugin", "plugin.json")
_PLUGIN_RANGES = {"freshAt": (0, 100), "freshTokens": (0, None)}
_LAYOUT_HELP = {"top": ("panels", "panels across the top"), "columns": ("columns", "panels per column"),
                "widths": ("list", "each column's share of the width"),
                "heights": ("list", '"auto" or a share of the height, per panel per column'),
                "narrow": ("panels", "panels on a narrow terminal"),
                "narrow_heights": ("list", '"auto" or a share of the height per narrow panel'),
                "narrow_below": ("int", "columns below which the narrow layout is used")}


_CONTROL = re.compile(r"[\x00-\x09\x0b-\x1f\x7f-\x9f]")


def _safe(text):
    """`text` with each control character shown as \\xNN (line breaks kept): a message can quote a share code or a
    hand-written file, and the terminal must not act on what they hold."""
    return _CONTROL.sub(lambda m: f"\\x{ord(m.group()):02x}", str(text))


class SettingError(ValueError):
    """A change refused: the value, the file or the guard; nothing was written. Its message is printable (_safe)."""
    def __init__(self, message=""):
        super().__init__(_safe(message))


class GuardRefused(SettingError):
    """The guard's refusal: a grant can lift it (fm settings undo keeps such a change for the next one)."""


def canon(name, value):
    """A shared setting's value in its one vocabulary (an old word mapped), or None for a value it doesn't take."""
    s = SHARED[name]
    if not isinstance(value, str):
        return None
    return value if value in s["choices"] else s["aliases"].get(value)


def _entry(surface, key, type, default, help, group, effect, choices=None, range=None, aliases=None):
    return {"surface": surface, "key": key, "type": type, "default": default, "choices": list(choices) if choices else None,
            "range": range, "aliases": aliases or {}, "group": group, "help": help, "effect": effect}


def app_schema():
    """One entry per tui.toml setting, from fmcodetui.DEFAULTS."""
    import fmcodetui as T
    D = T.DEFAULTS
    app = lambda *a, **k: _entry("app", *a, effect="next run", **k)
    out = [app("theme", "choice", D["preset"], "the app's colours (signal: night with palette cb; riso: risograph "
                                               "inks on paper stock)", "look",
               choices=T.PRESETS),
           app("motion", "choice", D["motion"], SHARED["motion"]["help"], "look", choices=SHARED["motion"]["choices"],
               aliases=SHARED["motion"]["aliases"]),
           app("palette", "choice", D["palette"], SHARED["palette"]["help"], "look",
               choices=SHARED["palette"]["choices"]),
           app("border", "choice", D["border"], "panel borders", "look", choices=T.BORDERS)]
    out += [app(f"colors.{n}", "style", spec, f"the {n} style: a colour (#rrggbb or 0-255) or {{ fg, bg, bold, "
                f"italic, reverse }}", "colors") for n, spec in D["theme"].items()]
    out += [app(f"layout.{k}", _LAYOUT_HELP[k][0], v, _LAYOUT_HELP[k][1], "layout",
                range=(0, None) if _LAYOUT_HELP[k][0] == "int" else None) for k, v in D["layout"].items()]
    seen = {}
    for k, cmd in D["keys"].items():
        seen.setdefault(T.key_name(k), cmd)
    out += [_key_entry(name, cmd) for name, cmd in seen.items()]
    return out


def _key_entry(name, default):
    import fmcodetui as T
    return _entry("app", f"keys.{name}", "choice", default, f"what {name} runs (none: nothing)", "keys", "next run",
                  choices=T.COMMANDS + ["none"])


def mod_manifest():
    """The foreman-ui mod's plugin.json: beside this checkout, else where Claude Code installed it; {} when neither."""
    paths = [_MOD_JSON]
    try:
        with open(os.path.join(claude_dir(), "plugins", "installed_plugins.json"), encoding="utf-8") as f:
            inst = json.load(f).get("plugins") or {}
        paths += [os.path.join(x.get("installPath") or "", ".claude-plugin", "plugin.json")
                  for k, v in inst.items() if k.split("@")[0] == PLUGIN and isinstance(v, list) for x in v
                  if isinstance(x, dict)]
    except (OSError, ValueError, AttributeError):
        pass
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            continue
    return {}


def plugin_schema():
    """One entry per userConfig option of the foreman-ui mod (its plugin.json is the source)."""
    out = []
    for key, spec in (mod_manifest().get("userConfig") or {}).items():
        shared = SHARED.get(key, {})  # its options list the old words too (Claude Code drops a value not in them)
        typ = "choice" if spec.get("options") else spec.get("type", "string")
        out.append(_entry("plugin", key, typ, spec.get("default"), spec.get("description") or spec.get("title", key),
                          "pane", "in seconds", choices=shared.get("choices") or spec.get("options"),
                          range=_PLUGIN_RANGES.get(key), aliases=shared.get("aliases")))
    return out


def schema():
    return app_schema() + plugin_schema()


def find(key, surface=None):
    """The entries a name means: one per surface that has it (keys.X for any key the app reads)."""
    import fmcodetui as T
    got = [e for e in schema() if e["key"] == key and surface in (None, e["surface"])]
    if not got and surface in (None, "app") and key.startswith("keys.") and T.parse_key(key[5:]):
        got = [_key_entry(key[5:], "none")]  # a key the defaults leave unbound
    return got


def _check(e, value):
    """The value the entry takes for `value` (a typed word from the command line, or a value), or SettingError."""
    bad = lambda why: SettingError(f"{e['key']} = {value!r}: {why}")
    if e["type"] == "choice":
        v = value if value in (e["choices"] or ()) else e["aliases"].get(value) if isinstance(value, str) else None
        if v is None:
            raise bad(f"one of {', '.join(e['choices'])}")
        return v
    if e["type"] in ("int", "number"):
        if isinstance(value, str):
            try:
                value = int(value) if e["type"] == "int" else float(value)
            except ValueError:
                raise bad("a number") from None
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise bad("a number")
        lo, hi = e["range"] or (None, None)
        if (lo is not None and value < lo) or (hi is not None and value > hi):
            raise bad(f"from {lo}" + (f" to {hi}" if hi is not None else " up"))
        return int(value) if float(value).is_integer() else value
    if e["type"] == "string":
        return str(value)
    if isinstance(value, str):  # a style, list or table: TOML as written, else a plain word ("#4DA3FF")
        try:
            return tomllib.loads(f"v = {value}")["v"]
        except tomllib.TOMLDecodeError:
            return value
        except RecursionError:  # nested past the parser's depth: no setting is
            raise bad("nested too deep") from None
    return value


# ---------------------------------------------------------------- tui.toml in place

_PART = r'(?:"(?:[^"\\]|\\.)*"|\'[^\']*\'|[A-Za-z0-9_-]+)'
_KEY = re.compile(rf"^\s*({_PART}(?:\s*\.\s*{_PART})*)\s*=")
_HEAD = re.compile(r"^\s*(\[\[?)\s*([^\[\]]*?)\s*\]\]?\s*(?:#.*)?$")


def _unquote(k):
    if not re.fullmatch(_PART, k):
        return None  # a dotted key: never the one asked for
    return json.loads(k) if k.startswith('"') else k[1:-1] if k.startswith("'") else k


def _parses(text):
    try:
        return tomllib.loads(text)
    except (tomllib.TOMLDecodeError, RecursionError):
        return None


def _value_end(lines, i, col):
    """The last line of the value that starts at lines[i][col]: a multi-line array or string runs on."""
    for j in range(i, min(len(lines), i + 1000)):  # past that: misread, and set_app's placed check refuses
        got = _parses("v =" + "\n".join([lines[i][col:]] + lines[i + 1:j + 1]))
        if got is not None and list(got) == ["v"]:
            return j
    return i


def _scan(lines):
    """[(table, key, first line, last line, column after =)] and {table: header line}; table None is the top."""
    table, i, keys, heads = None, 0, [], {}
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("["):
            m = _HEAD.match(lines[i])
            table = (m.group(2).strip('"') if m.group(1) == "[" else "[[" + m.group(2)) if m else "?"
            heads.setdefault(table, i)
            i += 1
            continue
        m = _KEY.match(lines[i]) if s and not s.startswith("#") else None
        if not m:
            i += 1
            continue
        end = _value_end(lines, i, m.end())
        keys.append((table, _unquote(m.group(1).strip()), i, end, m.end()))
        i = end + 1
    return keys, heads


def edit_toml(text, table, key, value, same=None):
    """`text` with table.key set to `value` (None: its line removed), everything else as it was. `same(a, b)` says two
    key names are one."""
    import fmcodetui as T
    same = same or (lambda a, b: a == b)
    raw = text.split("\n")
    cr = [x.endswith("\r") for x in raw]  # each line keeps its own ending; a new line takes its neighbour's
    lines = [x[:-1] if c else x for x, c in zip(raw, cr)]
    keys, heads = _scan(lines)

    def insert(at, line):
        lines.insert(at, line)
        cr.insert(at, cr[at - 1] if at else cr[0])
    hit = [k for k in keys if k[0] == table and k[1] is not None and same(k[1], key)]
    if value is None:  # T-1510: undoing a key that wasn't set; not there, nothing to do
        for _, _, i, end, _ in hit[-1:]:
            del lines[i:end + 1], cr[i:end + 1]
    elif hit:
        _, _, i, end, col = hit[-1]
        rest = "\n".join([lines[i][col:]] + lines[i + 1:end + 1])
        lead = rest[:len(rest) - len(rest.lstrip(" \t"))] or " "
        whole, tail = _parses("v =" + rest), ""
        for p in (m.start() for m in re.finditer("#", rest) if m.start() >= rest.rfind("\n") + 1):
            if _parses("v =" + rest[:p]) == whole:
                tail = rest[len(rest[:p].rstrip()):]
                break
        lines[i:end + 1] = [lines[i][:col] + lead + T._toml(value) + tail]
        cr[i:end + 1] = [cr[end]]
    else:
        line = f"{T._toml_key(key)} = {T._toml(value)}"
        mine = [k for k in keys if k[0] == table]
        if mine:
            insert(mine[-1][3] + 1, line)
        elif table in heads:
            insert(heads[table] + 1, line)
        elif table is None and heads:
            insert(min(heads.values()), line)
        else:  # at the end: after the last line that isn't blank, a blank line before a new table
            eol = any(cr)
            while len(lines) > 1 and not lines[-1] and not lines[-2]:
                del lines[-1], cr[-1]
            if lines == [""]:
                lines, cr = [], []
            elif lines[-1]:
                lines, cr = lines + [""], cr[:-1] + [eol, cr[-1]]  # the last line had no line break
            add = ([""] if table and lines else []) + ([f"[{T._toml_key(table)}]"] if table else []) + [line]
            at = len(lines) - 1 if lines else 0
            lines[at:at], cr[at:at] = add, [eol] * len(add)
            if not lines or lines[-1]:
                lines, cr = lines + [""], cr + [False]
    return "\n".join(x + ("\r" if c else "") for x, c in zip(lines, cr))


def _split(key):
    return tuple(key.split(".", 1)) if "." in key else (None, key)


def app_path():
    import fmcodetui
    return fmcodetui.config_path()


def _load(text, where):
    """load_config on `text`: (config, errors without the temp file's name)."""
    import fmcodetui as T
    fd, tmp = tempfile.mkstemp(suffix=".toml")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        cfg, errors = T.load_config(tmp)
    finally:
        os.unlink(tmp)
    return cfg, [e.replace(tmp, where) for e in errors]


def set_app(key, value, path=None, p=None, base=None):
    """Set one tui.toml setting in place: (the value written, [other settings it made bad, which the app skips]).
    SettingError (the file untouched) when the name or value is wrong, the guard refuses the write (inside Claude
    Code), the file doesn't parse, load_config rejects the value or the app can't draw with it. T-1543: `base`, the
    text the caller last read (the fm code app's view): refused too when another program changed this key since."""
    import fmcore
    path, value, table, name = _app_change(key, value, path, p)
    real = os.path.realpath(path)  # a tui.toml linked from a dotfiles repo stays linked
    with fmcore.lock(os.path.dirname(real)):  # another fm settings set between our read and our write
        return _set_app(key, value, path, real, table, name, base)


def preview_app(key, value, path=None, p=None):
    """T-1573: (the value, the config the app would run with it); nothing written. Whatever set_app refuses, the
    guard's refusal included, is refused here: the fm code app shows a look with it only when it could keep it."""
    path, value, table, name = _app_change(key, value, path, p)
    return value, _plan_app(key, value, path, table, name)[1]


def _app_change(key, value, path, p):
    """set_app's checks before the file is read (the name, the value, the guard): (path, the value, table, name)."""
    import fmcodetui as T
    path = path or app_path()
    entries = find(key, "app")
    if not entries:
        raise SettingError(f"{key}: not a setting of the app (fm settings list shows them)")
    value = None if value is None else _check(entries[0], value)  # None: unset (fm settings undo)
    table, name = _split(key)
    _utf8(value, key)
    block = _guard_block(path, p) if in_claude_code() else None
    if block:
        raise GuardRefused(f"app {key}: not written, the guard protects {path} ({block}); to "
                           + ("unset" if value is None else "set") + f" it, edit {path}: "
                           + (f"under [{table}], " if table else "at the top, ")
                           + (f"remove {T._toml_key(name)}" if value is None else
                              f"{T._toml_key(name)} = {T._toml(value)}"))
    return path, value, table, name


def _utf8(value, key):
    try:
        json.dumps(value, ensure_ascii=False).encode("utf-8")
    except UnicodeEncodeError:
        raise SettingError(f"{key}: not text UTF-8 can hold (a lone surrogate)") from None


def _set_app(key, value, path, real, table, name, base=None):
    import fmcore
    text = _read_app(path)
    _conflict([key], text, base, path)
    new, _, errors = _plan_app(key, value, path, table, name, text=text)
    fmcore.write_atomic(real, new)
    return value, errors


APP_MAX = 1_000_000  # bytes of tui.toml read: a settings file, not a data file


def _read_raw(path):
    """tui.toml's bytes and its stat ((b"", None) when there is none). SettingError, its message starting with the
    path, when it can't be read, isn't a regular file (a FIFO would block the reader, /dev/zero never ends) or is over
    APP_MAX: nothing of it is read past that."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)  # a FIFO opens at once rather than wait for a writer
    except FileNotFoundError:
        return b"", None
    except OSError as e:
        raise SettingError(f"{path}: can't read it ({e.strerror or e})") from None
    try:
        with os.fdopen(fd, "rb") as f:
            st = os.fstat(fd)  # the file opened, not whatever the name points at by now
            if not stat.S_ISREG(st.st_mode):
                raise SettingError(f"{path}: not a regular file, not read")
            data = f.read(APP_MAX + 1)
    except OSError as e:
        raise SettingError(f"{path}: can't read it ({e.strerror or e})") from None
    if len(data) > APP_MAX:
        raise SettingError(f"{path}: over {APP_MAX // 1_000_000} MB, not read (edit it by hand)")
    return data, st


def _read_app(path):
    """tui.toml's text ("" when there is none), line breaks read as open() reads them; SettingError (_read_raw) when
    it can't be read."""
    try:
        return _read_raw(path)[0].decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    except UnicodeDecodeError as e:
        raise SettingError(f"{path}: can't read it ({e})") from None


def _plan_app(key, value, path, table, name, text=None):
    """The file (or `text`, as it would be at `path`) with the change made, checked: (its text, the config the app
    loads from it, [other settings it made bad]); SettingError for a file or value set_app refuses."""
    import fmcodetui as T
    if text is None:
        text = _read_app(path)
    if len(text) > APP_MAX:  # the line scan parses each value as it goes: a settings file, not a data file
        raise SettingError(f"{path} is over 1 MB: edit it by hand")
    if _parses(text) is None:
        raise SettingError(f"{path} isn't valid TOML: fix it first (fm code tui names the line)")
    same =(lambda a, b: T.parse_key(a) == T.parse_key(b)) if table == "keys" else None
    new = edit_toml(text, table, name, value, same)
    got = _parses(new)
    placed = (got or {}).get(table, {}) if table else got
    hits = [v for k, v in placed.items() if (same or (lambda a, b: a == b))(k, name)] \
        if got is not None and isinstance(placed, dict) else None
    if hits is None or (hits if value is None else value not in hits):
        raise SettingError(f"{key}: can't {'remove' if value is None else 'place'} it in {path} (a [{table}] written "
                           "another way?); edit it by hand")
    try:
        old = set(_load(text, path)[1])
    except Exception:  # a file the app itself chokes on: whatever the new text reports is new
        old = set()
    try:
        cfg, errors = _load(new, path)
    except Exception as e:
        raise SettingError(f"{key} = {T._toml(value)}: the app can't read the file with it ({type(e).__name__}: {e})") \
            from None
    # the value itself rejected: refused, even when the file already had that key wrong (an error that names no
    # value reads the same before and after). Another setting it makes bad (columns that leave widths one short, a
    # theme that leaves a [colors] entry too faint) is skipped by the app as any bad setting is: written, and said
    own = [e for e in errors if e[len(path) + 2:].startswith((f"{key}:", f"{key} ="))]
    if own:
        raise SettingError("; ".join(own))
    errors = [e for e in errors if e not in old]
    why = render_error(cfg)
    if why:
        raise SettingError(f"{key} = {T._toml(value)}: the app can't draw with it ({why})")
    return new, cfg, errors


def render_error(cfg):
    """Why the fm code app can't draw with `cfg` (wide and narrow: both layouts), or None."""
    import fmcodetui as T
    try:
        for w, h in ((100, 30), (60, 20)):
            T.render(T.State(), w, h, cfg)
    except Exception as e:
        return f"{type(e).__name__}: {e}"
    return None


# ---------------------------------------------------------------- the plugin: Claude Code's settings.json

def _interactive():
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except (AttributeError, ValueError):  # no stdin, or a closed one
        return False


def in_claude_code():
    """Whether the guard decides writes to protected files: in a Claude Code session (its shells set these), and
    wherever stdin and stdout aren't both a terminal, since an agent's shell can blank the variables (fail closed).
    The user's own terminal and the fm code app's settings screen write directly."""
    return bool(os.environ.get("CLAUDECODE") or os.environ.get("CLAUDE_CODE_ENTRYPOINT")) or not _interactive()


def claude_dir():
    """Claude Code's config folder: CLAUDE_CONFIG_DIR when it is inside the home folder, else ~/.claude."""
    home = os.path.realpath(os.path.expanduser("~"))
    d = os.environ.get("CLAUDE_CONFIG_DIR")
    if d and not os.path.realpath(d).startswith(home.rstrip(os.sep) + os.sep):
        raise SettingError(f"CLAUDE_CONFIG_DIR={d} is outside the home folder ({home}): not Claude Code's settings")
    return d or os.path.join(home, ".claude")


def claude_settings():
    path = os.path.join(claude_dir(), "settings.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    except (OSError, ValueError) as e:
        raise SettingError(f"can't read {path}: {e}") from None
    if not isinstance(data, dict):
        raise SettingError(f"{path} isn't a JSON object")
    return path, data


def plugin_id(data):
    """The mod's id as Claude Code names it (foreman-ui@<marketplace>)."""
    for table in ("enabledPlugins", "pluginConfigs"):
        t = data.get(table)
        for k in t if isinstance(t, dict) else ():
            if k.split("@")[0] == PLUGIN:
                return k
    return f"{PLUGIN}@foreman"


def plugin_values(data):
    pc = data.get("pluginConfigs")
    cfg = pc.get(plugin_id(data)) if isinstance(pc, dict) else None
    opts = cfg.get("options") if isinstance(cfg, dict) else None
    return opts if isinstance(opts, dict) else {}


def _guard_block(path, p=None):
    """What the guard says about writing `path` here (the active task's grants, the standing yes, trust), or None."""
    import fmcore as c
    import fmguard
    home, cwd, b, meta, lane = os.path.expanduser("~"), os.getcwd(), None, {}, getattr(p, "lane", None)
    if p:
        try:
            b, meta = c.active_brief(c.load_briefs(p), lane), c.read_meta(p)
        except Exception:
            b, meta = None, {}  # unreadable: no grants, the guard decides as with none
    ctx = fmguard.Ctx(cwd=cwd, project_root=fmguard.project_root_for(cwd, home), home=home,
                      foreman_home=c.foreman_home(), state_dir=c.state_dir(), state_fallbacks=c.state_fallbacks(),
                      allow=set(b.meta.get("allow") or []) if b else set(), task_id=b.id if b else None,
                      standing=set(meta.get("standing") or {}), trusted=bool(c.trusted()),
                      # a builder's lane writes nothing outside its worktree (as the hook confines it)
                      confine=(lane, c.main_worktree(lane)) if lane and b and b.meta.get("builder") else None)
    block = fmguard.check("Write", {"file_path": path}, ctx)
    return fmguard.message(block, ctx) if block else None


def set_plugin(key, value, p=None):
    """Set one of the mod's options in settings.json pluginConfigs (inside Claude Code: when the guard allows that
    write); SettingError with the exact change to make by hand when it doesn't (nothing written)."""
    import fmcore
    entries = find(key, "plugin")
    if not entries:
        raise SettingError(f"{key}: not a setting of the {PLUGIN} pane (fm settings list shows them)")
    value = None if value is None else _check(entries[0], value)  # None: unset (fm settings undo)
    _utf8(value, key)
    path, data = claude_settings()
    pid = plugin_id(data)
    how = (f'to {"unset" if value is None else "set"} it, edit {path}: pluginConfigs → "{pid}" → options → '
           + (f"remove {json.dumps(key)}" if value is None else json.dumps({key: value})[1:-1])
           + f" (or Claude Code's /plugin → {PLUGIN} → configure)")
    block = _guard_block(path, p) if in_claude_code() else None
    if block:
        raise GuardRefused(f"plugin {key}: not written, the guard protects {path} ({block}); {how}")
    real = os.path.realpath(path)  # a settings.json linked from a dotfiles repo stays linked
    with fmcore.lock(os.path.dirname(real)):  # Claude Code doesn't take it: this orders fm's own writers
        path, data = claude_settings()  # again, under the lock
        _write_plugin(data, plugin_id(data), key, value, real, how)
    return value


def _write_plugin(data, pid, key, value, real, how):
    import fmcore
    pc = data.setdefault("pluginConfigs", {})
    cfg = pc.setdefault(pid, {}) if isinstance(pc, dict) else None
    opts = cfg.setdefault("options", {}) if isinstance(cfg, dict) else None
    if not isinstance(opts, dict):
        raise SettingError(f"{real}: pluginConfigs isn't laid out as Claude Code writes it; {how}")
    if value is None:
        opts.pop(key, None)
    else:
        opts[key] = value
    fmcore.write_atomic(real, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def set_key(key, value, surface=None, p=None, base=None):
    """`fm settings set` and the fm code app's :set line (T-1572): `key` set on every surface that has it (or on
    `surface`): ([(surface, value written, warnings)], [why each refused one wasn't written]). T-1510: what it changed
    is one entry of the settings history (fm settings undo). T-1543: `base` as set_app takes it."""
    with _recorded("set") as changes:
        return _set_key(key, value, surface, p, changes, written(), base)


def set_apps(pairs, path=None, p=None, base=None):
    """T-1511: several tui.toml settings [(key, value)] in one write: each checked as set_app checks one (the guard
    too) and placed on the text the one before left, the file written once under its lock, all one entry of the
    history (one undo puts them all back). SettingError, or whatever failed, and nothing written: a panel the fm code
    app moves never leaves new columns with old heights. [(key, value written, warnings)]"""
    import fmcore
    path = path or app_path()
    with _recorded("set") as changes:
        now = written()
        planned = [(key, *_app_change(key, value, path, p)[1:]) for key, value in pairs]
        real = os.path.realpath(path)
        with fmcore.lock(os.path.dirname(real)):
            text, done = _read_app(path), []
            _conflict([key for key, *_ in planned], text, base, path)
            for key, value, table, name in planned:
                text, _, warn = _plan_app(key, value, path, table, name, text=text)
                done.append((key, value, warn))
            fmcore.write_atomic(real, text)
        for key, value, _ in done:
            _change(changes, now, "app", key, value)
    return done


def _change(changes, now, s, key, new):
    """A write added to `changes` with the value it replaced (None: unset, or one the schema refuses, so an undo leaves
    the default rather than a value it can't write); a skipped one kept as `skipped`, for undo to say it isn't put
    back. A value written again as it was isn't a change."""
    k = _norm(key)
    old, _, ok = now.get((s, k), (None, None, False))
    if new != old or not ok:
        changes.append({"surface": s, "key": k, "old": old if ok else None, "new": new,
                        **({"skipped": old} if (s, k) in now and not ok else {})})


def _set_key(key, value, surface, p, changes, now, base=None):
    """set_key's writes; each that changed a value is added to `changes` (_change)."""
    done, refused = [], []
    for e in find(key, surface):
        s = e["surface"]
        try:
            if s == "app":
                done.append(("app", *set_app(key, value, p=p, base=base)))
            else:
                done.append(("plugin", set_plugin(key, value, p), []))
        except SettingError as x:
            refused.append(f"{s}: {x}")
            continue
        _change(changes, now, s, key, done[-1][1])
    return done, refused


# ---------------------------------------------------------------- T-1510: diff, share codes, history and undo

SHARE_MAX = 32_768  # characters of a share code: every setting changed at once is a few KB
SHARE_KEYS = 300  # keys in one: each is checked against the file, render and all (the schema has ~80, keys bound too)
HISTORY_MAX = 50  # changes fm settings undo can walk back


def _norm(key):
    """A keys.X name by the key it means (keys.Z, keys.shift+z: the one curses reports); any other name as it is."""
    import fmcodetui as T
    k = T.parse_key(key[5:]) if key.startswith("keys.") else None
    return f"keys.{T.key_name(k[0])}" if k else key


def written(problems=None):
    """{(surface, setting): (value, its schema entry, whether it is read)} for each key tui.toml and the pane's
    options hold, as written (in the schema's words when it takes them); the entry None for a key nothing reads. A file
    that can't be read adds to `problems`, as do the pane's options when its plugin.json isn't found (nothing to
    check them by)."""
    problems = [] if problems is None else problems
    found, path = [], app_path()
    try:
        raw = tomllib.loads(_read_raw(path)[0].decode("utf-8"))  # T-1543: never a FIFO, a device or past 1 MB
    except SettingError as e:
        problems.append(("app", str(e)))
        raw = {}
    except (ValueError, RecursionError) as e:  # TOMLDecodeError and UnicodeDecodeError are ValueErrors
        problems.append(("app", f"can't read {path}: {e}"))
        raw = {}
    for k, v in raw.items():
        if k == "profile":  # T-1656: not a setting; fm settings profile lists them
            continue
        table = k in ("colors", "layout", "keys") and isinstance(v, dict)
        found += [("app", _norm(f"{k}.{n}"), x) for n, x in v.items()] if table else [("app", k, v)]
    import fmcodetui as T  # what load_config skips past the schema's own check (a colour too faint on the theme)
    unread = False
    try:
        skips = [e[len(path) + 2:] for e in (T.load_config(path)[1] if raw else [])]
    except Exception as e:  # a file the app itself chokes on: none of it is read (the set that repairs it still runs)
        problems.append(("app", f"the app can't read {path} ({type(e).__name__}: {e})"))
        skips, unread = [], True  # every key skipped: an undo removes what the app never read
    try:
        opts = plugin_values(claude_settings()[1])
    except SettingError as e:
        problems.append(("plugin", str(e)))
        opts = {}
    plugin = plugin_schema()
    if opts and not plugin:  # a dead flag needs the list of what the pane reads
        problems.append(("plugin", f"the {PLUGIN} mod's plugin.json isn't found: its options can't be checked"))
    found += [("plugin", k, v) for k, v in opts.items()] if plugin else []
    by = {(e["surface"], e["key"]): e for e in app_schema() + plugin}
    out = {}
    for s, k, v in found:
        e = by.get((s, k)) or next(iter(find(k, s)), None)
        skip = s == "app" and (unread or any(x.startswith((f"{k}:", f"{k} =")) for x in skips))
        try:
            out[s, k] = (_check(e, v), e, not skip) if e and v is not None else (v, e, False)
        except SettingError:
            out[s, k] = (v, e, False)  # as written: the app (or the pane) skips it
    return out


def diff(problems=None):
    """The keys the files change from the defaults: [{surface, key, value, default}], `skipped` on a value the schema
    refuses or the app skips; a key nothing reads as {surface, key, value, dead: True}."""
    return [dict(surface=s, key=k, value=v, **({"default": e["default"]} if e else {"dead": True}),
                 **({} if ok or not e else {"skipped": True}))
            for (s, k), (v, e, ok) in written(problems).items() if not e or not ok or v != e["default"]]


def share_code(rows=None):
    """The changed settings (not the dead or skipped ones) as one pasteable word: base64url of {surface: {key: value}}
    as JSON."""
    got = {}
    for r in diff() if rows is None else rows:
        if not r.get("dead") and not r.get("skipped"):
            got.setdefault(r["surface"], {})[r["key"]] = r["value"]
    code = base64.urlsafe_b64encode(json.dumps(got, separators=(",", ":"), ensure_ascii=False, default=str)
                                    .encode("utf-8")).decode("ascii").rstrip("=")
    if len(code) > SHARE_MAX:
        raise SettingError(f"the changed settings make a code of {len(code)} characters; import takes {SHARE_MAX}")
    return code


def _decode(code):
    """A share code's {surface: {key: value}}: JSON only (nothing in it is run), its size capped; SettingError else."""
    code = "".join(str(code).split())  # a pasted code may wrap
    if len(code) > SHARE_MAX:
        raise SettingError(f"a share code is at most {SHARE_MAX} characters; this one is {len(code)} long")

    def constant(c):
        raise ValueError(f"{c} isn't a value")
    try:
        raw = base64.b64decode(code + "=" * (-len(code) % 4), altchars=b"-_", validate=True)
        got = json.loads(raw.decode("utf-8"), parse_constant=constant)
    except (ValueError, RecursionError) as e:  # binascii.Error and UnicodeDecodeError are ValueErrors
        raise SettingError(f"not a share code (fm settings export makes one): {type(e).__name__}") from None
    if not isinstance(got, dict):
        raise SettingError("not a share code (fm settings export makes one): not a table of settings")
    if sum(len(v) if isinstance(v, dict) else 1 for v in got.values()) > SHARE_KEYS:
        raise SettingError(f"a share code holds at most {SHARE_KEYS} settings")
    return got


def import_code(code, p=None, only=None):
    """A share code's settings (or its `only` surface's), set: every key known and every value checked first (the
    app's as each would land in tui.toml, render and all), else SettingError naming each bad one and nothing written.
    Then each key whose value differs is set through set_key's path (the guard, the locks), all as one history entry:
    ([(surface, key, value written, warnings)], [why each refused one wasn't written], [(surface, key) already so])."""
    bad, plan, text, path = [], {}, None, app_path()
    for surface, items in _decode(code).items():
        if surface not in ("app", "plugin") or not isinstance(items, dict):
            bad.append(f"{surface!r}: not a surface of the share code (app, plugin)")  # repr: no raw escapes printed
            continue
        for key, value in items.items() if only in (None, surface) else ():
            try:
                e = next(iter(find(key, surface)), None) if key.isprintable() else None
                if not e:
                    raise SettingError(f"{key!r}: not a setting of the {surface}")
                if value is None or (e["type"] == "string" and not isinstance(value, str)):
                    raise SettingError(f"{key} = {json.dumps(value)}: not a value it takes")
                value = _check(e, value)
                _utf8(value, key)
                if surface == "app":
                    text = _plan_app(key, value, path, *_split(key), text=text)[0]
                plan[surface, _norm(key)] = value  # keys.enter and keys.ENTER are one key: the last one named wins
            except Exception as x:  # whatever a value makes fail refuses the code: nothing is written yet
                bad.append(f"{surface}: {x}" if isinstance(x, SettingError) else f"{surface}: {key!r}: {type(x).__name__}")
    if bad:
        raise SettingError("not imported, nothing written: " + "; ".join(bad))
    done, refused, same = [], [], []
    with _recorded("import") as changes:
        now = written()
        for (s, k), v in plan.items():
            cur, _, ok = now.get((s, k), (None, None, False))
            if ok and cur == v:  # only the keys that change are written
                same.append((s, k))
                continue
            d, r = _set_key(k, v, s, p, changes, now)
            done += [(s, k, x, w) for _, x, w in d]
            refused += r
    return done, refused, same


def _history_path():
    import fmcore
    return os.path.join(fmcore.state_dir(), "settings", "history.json")


def _history():
    """The undo list: [] when there is none or it is corrupt (a fresh one replaces it); SettingError when it can't be
    read, so the next write doesn't take an unreadable history for an empty one and replace it."""
    path = _history_path()
    try:
        with open(path, encoding="utf-8") as f:
            got = json.load(f)
    except FileNotFoundError:
        return []
    except (ValueError, RecursionError):  # UnicodeDecodeError included
        return []
    except OSError as e:
        raise SettingError(f"can't read the settings history {path}: {e}") from None
    return [h for h in got if isinstance(h, dict) and isinstance(h.get("changes"), list)] if isinstance(got, list) else []


def _keep(hist):
    import fmcore
    fmcore.write_atomic(_history_path(), json.dumps(hist[-HISTORY_MAX:], ensure_ascii=False, default=str) + "\n")


@contextlib.contextmanager
def _recorded(how):
    """The history's lock held; the changes added to the list it yields are one entry (one undo) when it closes."""
    import fmcore
    with fmcore.lock(os.path.dirname(_history_path())):
        changes = []
        try:
            yield changes
        finally:  # what was written is kept, whatever stopped the rest
            try:
                if changes:
                    _keep(_history() + [{"at": fmcore.now(), "how": how, "changes": changes}])
            except (OSError, SettingError) as e:  # the change is written: said, never reported as failed
                print(f"fm settings: written, but undo can't put it back: the history wasn't saved ({_safe(e)})",
                      file=sys.stderr)


def undo(p=None):
    """The last set or import put back, backwards, each through set_app/set_plugin (the guard, the lock). A value
    changed since by other hands is left as it is (dropped from the history); one the guard refuses stays for the next
    undo. ([(surface, key, value now, the value it replaced, a note: a skipped value not put back)], [why each
    wasn't]); SettingError: nothing to undo, or a history it can't read."""
    import fmcore
    with fmcore.lock(os.path.dirname(_history_path())):
        hist = _history()
        if not hist:
            raise SettingError("nothing to undo (fm settings set and import keep the history)")
        last, now = hist[-1], written()
        done, refused, kept = [], [], []
        for c in reversed(last["changes"]):
            try:
                s, k, old, new = c["surface"], c["key"], c.get("old"), c["new"]
                if s not in ("app", "plugin") or not isinstance(k, str):
                    raise KeyError(k)
                cur = now.get((s, k), (None,))[0]
            except (TypeError, KeyError, AttributeError):
                refused.append(f"a history entry fm can't read ({str(c)[:80]}): dropped")
                continue
            if cur != new:
                refused.append(f"{s}: {k} changed since (now {_shown(cur, s)}): left as it is")
                continue
            note = (f"the value before it, {_shown(c['skipped'], s)}, was skipped (not one it reads): unset, not put "
                    "back" if "skipped" in c else "")
            try:
                done.append((s, k, set_app(k, old, p=p)[0] if s == "app" else set_plugin(k, old, p), new, note))
            except GuardRefused as x:
                refused.append(f"{s}: {x}")
                kept.insert(0, c)
            except SettingError as x:  # not a setting any more, or a file it can't place it in: by hand
                refused.append(f"{s}: {x}; dropped from the history")
        try:
            _keep(hist[:-1] + ([dict(last, changes=kept)] if kept else []))
        except OSError as e:  # put back, but still listed: the next undo finds them changed and leaves them
            refused.append(f"undone, but the history wasn't saved ({e})")
    return done, refused


def _shown(v, surface):
    import fmcodetui as T
    return "unset" if v is None else T._toml(v) if surface == "app" else json.dumps(v, ensure_ascii=False)


# ---------------------------------------------------------------- T-1543: last good copy, outside edits, bisect

def good_path():
    """The last tui.toml the fm code app started and drew with, kept in Foreman's state."""
    import fmcore
    return os.path.join(fmcore.state_dir(), "settings", "tui.good.toml")


def _good_text():
    try:
        with open(good_path(), encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None


def _try(text, where):
    """What the app runs with tui.toml as `text` (loaded and drawn from a temporary file): (config, [settings it
    skips], None), or (None, [], why it can't)."""
    try:
        cfg, errors = _load(text, where)
    except Exception as e:  # load_config itself choked
        return None, [], f"can't read it ({type(e).__name__}: {e})"
    why = render_error(cfg)
    return (None, [], f"can't draw with it ({why})") if why else (cfg, errors, None)


def boot(path=None):
    """The config the fm code app starts with: (config, [settings it skips], a note or None, what it read: {path,
    text} for its watch on outside edits). tui.toml when the app can draw with it, kept as the last good copy; else
    that copy, or the defaults when there is none, said in the note; tui.toml is never written."""
    import copy
    import fmcodetui as T
    path = path or app_path()
    try:
        text = _read_app(path)
    except SettingError:
        text = None
    seen = {"path": path, "text": text}
    if text is None:  # unreadable: load_config says why, the defaults show
        return (*T.load_config(path), None, seen)
    cfg, errors, why = _try(text, path)
    if not why:
        _keep_good(text)
        return cfg, errors, None, seen
    good = _good_text()
    cfg, errors, _ = _try(good, good_path()) if good is not None and _parses(good) is not None else (None, [], None)
    how = "the last good settings" if cfg else "the defaults"
    note = _safe(f"started with {how}: {path}: the app {why}; the file is as you left it (fm settings bisect names "
                 "the setting)" + (f"; the last good copy: {good_path()}" if cfg else ""))
    return (cfg, errors, note, seen) if cfg else (copy.deepcopy(T.DEFAULTS), [], note, seen)


def _keep_good(text):
    """tui.toml as the app drew it, kept when it parses and differs from the copy; trouble saving it never stops a
    start."""
    import fmcore
    if _parses(text) is None or _good_text() == text:
        return
    try:
        with fmcore.lock(os.path.dirname(good_path())):
            fmcore.write_atomic(good_path(), text)
    except Exception as e:  # a read-only state folder, a lock held too long
        print(f"fm code: the last good settings weren't kept ({_safe(e)})", file=sys.stderr)


def reread(seen):
    """tui.toml read again for the running app (`seen`: what it last read and the file's stat then; updated): None
    when it is as it was, else (the config to run now, or None to keep the running one, a note saying what changed).
    Read only when its stat changed, so a file it can't read (a FIFO, one past 1 MB, bad UTF-8) is said once."""
    try:
        st = os.stat(seen["path"])  # never blocks, a FIFO's included
        sig = (st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    except OSError:
        sig = None  # gone, or its folder unreadable: _read_app says which
    # ponytail: an edit of the same size within the clock tick of the last read is missed until the file changes again
    if "sig" in seen and sig == seen["sig"]:
        return None
    seen["sig"] = sig
    try:
        text = _read_app(seen["path"])
    except SettingError as e:
        return None, _safe(f"{e}: the running look kept")
    if text == seen["text"]:
        return None
    before, seen["text"] = seen.pop("valid", seen["text"]), text  # the last that parsed: a half-saved file between
    what = f"{seen['path']} changed outside the app"
    if _parses(text) is None:
        seen["valid"] = before
        return None, _safe(f"{what}, but isn't valid TOML: the running look kept (fm code tui names the line)")
    keys = changed(before, text)
    what += f" ({', '.join(keys[:6]) + (', …' if len(keys) > 6 else '') or 'comments only'})"
    cfg, errors, why = _try(text, seen["path"])
    if why:
        return None, _safe(f"{what}, but the app {why}: the running look kept; fm settings bisect names the setting")
    return cfg, _safe(f"{what}: applied" + (f"; skipped: {errors[0]}" if errors else ""))


def _flat(text):
    """{setting: value} of a tui.toml text: a table's keys as table.key, keys.X by the key it means; {} for none."""
    return _flatten(_parses(text or "") or {})


def _flatten(table):
    out = {}
    for k, v in table.items():
        if isinstance(v, dict):
            out.update({_norm(f"{k}.{n}"): x for n, x in v.items()})
        else:
            out[k] = v
    return out


def changed(before, after):
    """The settings two tui.toml texts set differently (added, removed or changed), in the order `after` names them
    (removed ones last)."""
    a, b = _flat(before), _flat(after)
    same = lambda x, y: json.dumps(x, sort_keys=True, default=str) == json.dumps(y, sort_keys=True, default=str)
    return [k for k in dict.fromkeys([*b, *a]) if (k in a) != (k in b) or not same(a[k], b[k])]


def _conflict(keys, text, base, path):
    """SettingError when another program changed one of `keys` in tui.toml (now `text`) since the caller read it as
    `base`: never overwritten unseen. Its other changes stay, as the write is made in place."""
    if base is None or text == base:
        return
    if _parses(text) is None:  # every key would count as changed ("now unset"): the file is what's wrong
        raise SettingError(f"{path} isn't valid TOML (changed since the app read it): fix it first (fm code tui names "
                           "the line)")
    theirs, now = set(changed(base, text)), _flat(text)
    hit = [k for k in keys if _norm(k) in theirs]
    if hit:
        raise SettingError("; ".join(f"{k}: changed in {path} since the app read it (now {_shown(now.get(_norm(k)), 'app')}"
                                     "): not overwritten; set it again to replace it" for k in hit))


def _build(good, bad, keys):
    """tui.toml text: the settings `good` holds ({setting: value}) with `keys` as `bad` has them (removed when it
    hasn't)."""
    # rebuilt from the flattened values, not the file's own text: comments, order and spelling (keys.ENTER is enter, a
    # [colors.ok] table an inline one) go; what load_config reads stays, and bisect checks the full rebuild fails too
    import fmcodetui as T
    flat = dict(good)
    for k in keys:
        if k in bad:
            flat[k] = bad[k]
        else:
            flat.pop(k, None)
    nest = {}
    for k, v in flat.items():
        table, name = _split(k)
        if table is None:
            nest[name] = v
        else:
            if not isinstance(nest.get(table), dict):
                nest[table] = {}
            nest[table][name] = v
    lines = [f"{T._toml_key(k)} = {T._toml(v)}" for k, v in nest.items() if not isinstance(v, dict)]
    for k, v in nest.items():
        if isinstance(v, dict):
            lines += [f"[{T._toml_key(k)}]"] + [f"{T._toml_key(n)} = {T._toml(x)}" for n, x in v.items()]
    return "\n".join(lines) + "\n"


def bisect(path=None):
    """The setting that keeps the fm code app from drawing: tui.toml's changes from the last good copy (the defaults
    when there is none or it doesn't draw either) applied in halves, each try loaded and drawn from a temporary file;
    tui.toml is never written. {key (None: tui.toml draws), value, removed, alone (it breaks the good settings by
    itself), why, base, changed, tries}; SettingError when it can't narrow it to one setting."""
    path = path or app_path()
    text, tries = _read_app(path), [0]
    if _parses(text) is None:
        raise SettingError(f"{path} isn't valid TOML: fix it first (fm code tui names the line)")

    def fails(t):
        tries[0] += 1
        return _try(t, path)[2]
    why = fails(text)
    if not why:
        return {"key": None, "tries": tries[0]}
    good, base = _good_text(), "the last good copy"
    if good is None or _parses(good) is None or fails(good):
        good, base = "", "the defaults"
        if fails(good):
            raise SettingError("the app can't draw with its defaults either: not a setting (an extension?)")
    a, b = _flat(good), _flat(text)
    keys = changed(good, text)
    if not keys or not fails(_build(a, b, keys)):
        raise SettingError(f"{path}: the app {why}, but its settings rebuilt from {base} draw: no one setting to name")
    lo, hi = 0, len(keys)  # the first lo keys draw, the first hi don't
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if fails(_build(a, b, keys[:mid])):
            hi = mid
        else:
            lo = mid
    key = keys[hi - 1]
    alone = hi == 1 or bool(fails(_build(a, b, [key])))
    return {"key": key, "value": b.get(key), "removed": key not in b, "alone": alone, "why": why, "base": base,
            "changed": len(keys), "tries": tries[0]}


def _cmd_bisect(args):
    import fmcli
    if args.key or args.surface:
        raise fmcli.UsageError("fm settings bisect: names the tui.toml setting the fm code app can't draw with")
    got, path = bisect(), app_path()
    k = got["key"]
    if not k:
        return fmcli.out(args, got, f"{path} draws: nothing to bisect")
    what = f"removing {k}" if got["removed"] else f"{k} = {_shown(got['value'], 'app')}"
    return fmcli.out(args, got, _safe(
        f"{what}: the app {got['why']}" + ("" if got["alone"] else " (with the changes before it)")
        + f"\nfound in {got['tries']} tries over the {got['changed']} settings {path} changes from {got['base']}; "
          f"nothing written (fm settings set {k} VALUE, or edit the file)"))


# ---------------------------------------------------------------- T-1656: profiles keyed to the terminal

WHEN = {"ssh": (lambda v: isinstance(v, bool), "true or false: an ssh session"),
        "tmux": (lambda v: isinstance(v, bool), "true or false: inside tmux"),
        "term": (lambda v: isinstance(v, str) and len(v) <= 100, 'TERM as a glob ("xterm-*"), 100 characters at most'),
        "width_below": (lambda v: type(v) is int and v > 0, "a number of columns: the terminal narrower than it"),
        "colors": (lambda v: type(v) is int and v in (0, 8, 256, 24),
                   "the colour depth: 0 (NO_COLOR), 8, 256 or 24 (truecolor)")}


def facts(env=None):
    """The terminal a profile's when clause is matched against: {ssh, tmux, term, width, colors} from `env` (the
    environment by default). The width is COLUMNS (0 is none), else the terminal's on stdout or stderr, else None:
    unknown (no terminal, as in Claude Code), which no width_below meets."""
    from fmcodeterm import colour_depth
    env = os.environ if env is None else env
    cols, width = str(env.get("COLUMNS") or ""), None
    if cols.isascii() and cols.isdigit() and len(cols) <= 6 and int(cols):
        width = int(cols)
    else:
        for fd in (1, 2):
            try:
                width = os.get_terminal_size(fd).columns or None
                break
            except (OSError, ValueError):
                continue
    return {"ssh": any(env.get(k) for k in ("SSH_CONNECTION", "SSH_CLIENT", "SSH_TTY")), "tmux": bool(env.get("TMUX")),
            "term": str(env.get("TERM") or ""), "width": width, "colors": colour_depth(env)}


def _meets(k, v, f):
    import fnmatch
    if k == "width_below":
        return f["width"] is not None and f["width"] < v
    return fnmatch.fnmatchcase(f["term"], v) if k == "term" else f[k] == v


def profile_list(table, f):
    """tui.toml's [profile] table (`table`, as parsed) in the file's order against the facts `f`: [{name, when,
    settings (its table without when; None when it isn't one), sets (their names), matches, problem}]. A profile with no
    when clause, an empty one or a wrong one never matches; its problem says why, ending "passed over"."""
    if table is None:
        return []
    if not isinstance(table, dict):
        return [{"name": "", "when": {}, "settings": None, "sets": [], "matches": False,
                 "problem": "profile: a [profile.NAME] table per profile: passed over"}]
    out, facts_ = [], ", ".join(WHEN)
    for name, p in table.items():
        when = p.get("when") if isinstance(p, dict) else None
        if not isinstance(p, dict):
            why = f"profile.{name}: a table of settings with a when clause"
        elif when is None:
            why = f"profile.{name}: no when clause (when = {{ {facts_} }})"
        elif not isinstance(when, dict):
            why = f"profile.{name}.when: a table of terminal facts ({facts_})"
        elif not when:  # a profile for every terminal is the file's own settings
            why = f"profile.{name}.when: empty: name at least one fact ({facts_})"
        else:
            why = next((f"profile.{name}.when.{k}" + (f" = {repr(v)[:60]}: {WHEN[k][1]}" if k in WHEN else
                                                      f": not a fact ({facts_})")
                        for k, v in when.items() if k not in WHEN or not WHEN[k][0](v)), None)
        mine = {k: v for k, v in p.items() if k != "when"} if isinstance(p, dict) else None
        out.append({"name": name, "when": when if isinstance(when, dict) else {}, "settings": mine,
                    "sets": list(_flatten(mine or {})), "problem": why and f"{why}: passed over",
                    "matches": not why and all(_meets(k, v, f) for k, v in when.items())})
    return out


def _lines(lines):
    """Lines for the terminal, each a file's text made inert: a line break, a control or a bidi character in a profile's
    name (or anything tui.toml holds) shows as its escape, never as a line or a reordering of its own."""
    import fmcodetui as T
    return "\n".join(T._escaped(str(x)) for x in lines)


def overrides(key, path=None):
    """T-1656: after a set of an app `key`: a line per profile in tui.toml (one that can apply) that sets it too."""
    import fmcodetui as T
    k = _norm(key)
    return [f"profile {p['name']} also sets {key}: it overrides on terminals where {T._toml(p['when'])} holds"
            for p in profiles(path)["profiles"] if not p["problem"] and k in p["sets"]]


def profiles(path=None, env=None):
    """fm settings profile: {path, facts, profiles (profile_list), active: the one that applies or None, problems};
    tui.toml read through the bounded reader, as load_config reads it (a FIFO, a device or a file past 1 MB is a
    problem, never read)."""
    path = path or app_path()
    f, problems = facts(env), []
    try:
        raw = tomllib.loads(_read_raw(path)[0].decode("utf-8"))
    except SettingError as e:
        raw, problems = {}, [str(e)]
    except (ValueError, RecursionError) as e:  # TOMLDecodeError and UnicodeDecodeError are ValueErrors
        raw, problems = {}, [f"can't read {path}: {e}"]
    got = profile_list(raw.get("profile"), f)
    return {"path": path, "facts": f, "profiles": got, "active": next((p["name"] for p in got if p["matches"]), None),
            "problems": problems + [p["problem"] for p in got if p["problem"]]}


def _cmd_profile(args):
    import fmcli
    import fmcodetui as T
    if args.key or args.surface:
        raise fmcli.UsageError("fm settings profile: lists tui.toml's [profile.NAME] tables and the one that applies")
    got = profiles()
    f, on, path = got["facts"], got["active"], got["path"]
    yes = lambda b: "yes" if b else "no"
    width = f"{f['width']} columns" if f["width"] is not None else "columns unknown (no terminal)"
    lines = [f"this terminal: ssh {yes(f['ssh'])} · tmux {yes(f['tmux'])} · TERM {f['term'] or 'unset'} · {width} · "
             f"colors {f['colors']}"] + [f"! {x}" for x in got["problems"]]
    if not got["profiles"]:
        lines.append(f"no profiles in {path}: add [profile.NAME] with when = {{ {', '.join(WHEN)} }} and the settings "
                     "it changes")
        return fmcli.out(args, got, _lines(lines))
    lines.append(f"profiles in {path} (the first that matches applies):")
    for p in got["profiles"]:
        lines.append(f"  {p['name']}  when {T._toml(p['when'])}  sets {', '.join(p['sets']) or 'nothing'}"
                     + ("  ← applies" if p["name"] == on and p["matches"] else ""))
    lines.append(f"{on} applies: the fm code app starts with its settings over the file's" if on is not None else
                 "none applies: the fm code app starts with the file's own settings")
    return fmcli.out(args, got, _lines(lines))


# ---------------------------------------------------------------- reading both, and the command

def rows(entries=None, problems=None):
    """Every setting (or `entries`) with its value now, its default and where it is stored; the user's own key
    bindings too. What can't be read is added to `problems` as (surface, line), never hidden behind the defaults."""
    import fmcodetui as T
    problems = [] if problems is None else problems
    apath = app_path()
    cfg, errors = T.load_config(apath)
    problems += [("app", e) for e in errors]
    try:
        spath, data = claude_settings()
    except SettingError as e:
        problems.append(("plugin", str(e)))
        spath, data = os.path.join(os.path.expanduser("~"), ".claude", "settings.json"), {}
    pid, opts = plugin_id(data), plugin_values(data)
    if entries is None:
        entries = schema()
        known = {e["key"] for e in entries}
        entries += [_key_entry(n, "none") for n in dict.fromkeys(T.key_name(k) for k in cfg["keys"])
                    if f"keys.{n}" not in known]

    def now(e):
        table, name = _split(e["key"])
        if e["surface"] == "plugin":
            v = opts.get(name, e["default"])
            return canon(name, v) or v if name in SHARED else v
        if table == "colors":
            return cfg["theme"].get(name)
        if table == "layout":
            return cfg["layout"].get(name)
        if table == "keys":
            return cfg["keys"].get((T.parse_key(name) or [None])[0], "none")
        return cfg["preset"] if name == "theme" else cfg.get(name)

    on = cfg.get("profile") or {}  # T-1656: the value a profile gives this terminal, said as the profile's
    mine = lambda e: {"profile": on["name"]} if e["surface"] == "app" and _norm(e["key"]) in on.get("sets", ()) else {}
    return [dict(e, value=now(e), where=apath if e["surface"] == "app" else f"{spath} pluginConfigs.{pid}.options."
                 f"{e['key']}", **mine(e)) for e in entries]


def skip_note(x, path=None):
    """How a list says what the app does with a bad setting load_config named (`x`, its line): the default shows for
    the file's own; a profile's value skipped leaves the value without it; a profile passed over says so itself."""
    path = path or app_path()
    msg = x[len(path) + 2:] if x.startswith(f"{path}: ") else x
    if not msg.startswith("profile"):
        return " (skipped: the default shows)"
    return "" if x.endswith("passed over") else " (skipped: the value without the profile shows)"


def _text(r, width=22):
    import fmcodetui as T
    show = lambda v: T._toml(v) if r["surface"] == "app" else json.dumps(v, ensure_ascii=False)
    note = "" if r["value"] == r["default"] else f"  (default {show(r['default'])})"
    note += f"  (profile {r['profile']})" if r.get("profile") is not None else ""
    return f"{r['key']:<{width}} {show(r['value'])}{note}"


def cmd_settings(args):
    import fmcli
    import fmcodetui as T
    if args.action == "list":  # T-1511: fm settings list keys (or layout, …): that group alone
        problems, groups = [], list(dict.fromkeys(e["group"] for e in schema()))
        if args.key and args.key not in groups:
            raise fmcli.UsageError(f"fm settings list [{' | '.join(groups)}]: {_safe(args.key)!r} isn't one")
        got = [r for r in rows(problems=problems) if args.key in (None, r["group"])]
        if args.json:
            return fmcli.out(args, got, None)
        lines = []
        for surface, title in (("app", "app (fm code; next run)"), ("plugin", f"plugin ({PLUGIN} pane; in seconds)")):
            mine = [r for r in got if r["surface"] == surface and (args.surface in (None, surface))]
            if mine:
                where = mine[0]["where"] if surface == "app" else mine[0]["where"].rsplit(".", 1)[0]
                on = next((r["profile"] for r in mine if r.get("profile") is not None), None)
                where += f" · profile {on} applies here (fm settings profile)" if on is not None else ""
                lines += [f"{title}: {where}"] + [f"  ! {x}{skip_note(x)}" for s, x in problems
                                                  if s == surface] + ["  " + _text(r) for r in mine]
        return fmcli.out(args, got, _lines(lines) or "no settings found")  # a profile's name is the file's
    if args.action == "profile":  # T-1656
        return _cmd_profile(args)
    if args.action in ("diff", "export", "import", "undo", "bisect"):
        try:
            return _cmd_bisect(args) if args.action == "bisect" else _cmd_history(args)
        except SettingError as e:
            import fmcore
            raise fmcore.PolicyError(str(e)) from None
    if not args.key:
        raise fmcli.UsageError(f"fm settings {args.action} KEY{' VALUE' if args.action == 'set' else ''}")
    if args.action == "get":
        got = rows(find(args.key, args.surface))
        if not got:
            raise fmcli.UsageError(f"{args.key}: no such setting (fm settings list shows them)")
        return fmcli.out(args, got, _lines(f"{r['surface']}: {_text(r, 0)}  [{r['where']}]" for r in got))
    if args.value is None:
        raise fmcli.UsageError("fm settings set KEY VALUE")
    entries = find(args.key, args.surface)
    if not entries:
        raise fmcli.UsageError(f"{args.key}: no such setting{f' in the {args.surface}' if args.surface else ''} "
                               "(fm settings list shows them)")
    got, refused = set_key(args.key, args.value, args.surface, _project(args))
    done, lines = [], []
    for surface, v, warn in got:
        if surface == "app":  # T-1656: a profile that sets the key too wins where it applies: said, never silent
            over = overrides(args.key)
            mine = [f"app: {args.key} = {T._toml(v)} in {app_path()} (the next fm code run reads it)"]
            mine += [f"  now skipped: {w}" for w in warn] + [f"  {o}" for o in over]
            lines += mine
            done.append({"surface": "app", "key": args.key, "value": v, "where": app_path(), "warnings": warn,
                         "overrides": over, "line": "\n".join(mine)})
        else:
            lines.append(f"plugin: {args.key} = {json.dumps(v)} (the pane reads it within seconds)")
            done.append({"surface": "plugin", "key": args.key, "value": v, "line": lines[-1]})
    said = ([_lines(lines)] if lines else []) + [_safe(x) for x in refused]  # a refusal as before (the guard's words)
    fmcli.out(args, {"set": done, "refused": refused}, "\n".join(said))
    if refused:
        import fmcore
        raise fmcore.PolicyError(f"{len(refused)} of {len(entries)} not written (above)")
    return 0


def _project(args):
    import fmcli
    try:
        return fmcli.resolve(args, create=False)
    except fmcli.UsageError:
        return None  # outside a project: no task grants, the guard decides as with none


def _cmd_history(args):
    """fm settings diff | export | import CODE | undo (T-1510)."""
    import fmcli
    import fmcore
    if args.action in ("diff", "export"):
        problems = []
        rows = [r for r in diff(problems) if args.surface in (None, r["surface"])]
        said = [{"surface": s, "problem": x} for s, x in problems if args.surface in (None, s)]
        if args.action == "export":
            for x in said:  # the code alone on stdout, so it can be piped
                print(_safe(f"! {x['surface']}: {x['problem']} (not in the code)"), file=sys.stderr)
            code = share_code(rows)
            return fmcli.out(args, {"code": code, "settings": [r for r in rows if not (r.get("dead") or
                                                                                     r.get("skipped"))],
                                    "problems": said}, code)
        why = lambda r: ("dead: nothing reads it" if r.get("dead") else ("skipped: not a value it takes; " if
                         r.get("skipped") else "") + f"default {_shown(r['default'], r['surface'])}")
        lines = [f"! {x['surface']}: {x['problem']}" for x in said] + [
            f"{r['surface']}: {r['key']} = {_shown(r['value'], r['surface'])}  ({why(r)})" for r in rows]
        return fmcli.out(args, {"changed": rows, "problems": said},
                         _safe("\n".join(lines)) or "every setting at its default")
    if args.action == "import":
        if not args.key:
            raise fmcli.UsageError("fm settings import CODE (fm settings export makes one)")
        done, refused, same = import_code(args.key, _project(args), args.surface)
        data = {"set": [{"surface": s, "key": k, "value": v, "warnings": w} for s, k, v, w in done],
                "same": [{"surface": s, "key": k} for s, k in same], "refused": refused}
        lines = [f"{s}: {k} = {_shown(v, s)}" + "".join(f"\n  now skipped: {x}" for x in w) for s, k, v, w in done]
        lines += [f"already so: {', '.join(f'{s} {k}' for s, k in same)}"] if same else []
    else:
        if args.surface or args.key:
            raise fmcli.UsageError("fm settings undo: puts back the last set or import, on each surface it changed")
        done, refused = undo(_project(args))
        data = {"undone": [{"surface": s, "key": k, "value": v, "was": new, "note": n} for s, k, v, new, n in done],
                "refused": refused}
        lines = [f"{s}: {k} back to {_shown(v, s)} (was {_shown(new, s)})" + (f"; {n}" if n else "")
                 for s, k, v, new, n in done]
    fmcli.out(args, data, _safe("\n".join(lines + refused)) or "nothing to change")
    if refused:
        raise fmcore.PolicyError(f"{len(refused)} not done (above)")
    return 0
