"""T-1496: every setting Foreman's two UIs read, in one schema: the fm code app's tui.toml (in Foreman's home) and the
foreman-ui mod's userConfig (Claude Code keeps its values in settings.json pluginConfigs). Where the two overlap
(motion, palette) they share one name and one value set; an old word is still read (the mod's "calm" is reduced).

A tui.toml change is made in place: one key's value replaced (or the key added to its table, the table to the file),
comments, order and every other byte kept; it is refused unless load_config takes the new text and the app draws with
it. settings.json is Claude Code's own file, which the guard protects: a plugin change is written only when the guard
would allow that write, and otherwise printed as the change to make. Stdlib only."""
import json
import math
import os
import re
import tempfile
import tomllib

SHARED = {
    "motion": {"choices": ("full", "reduced", "off"), "aliases": {"calm": "reduced"},
               "help": "full: everything moves; reduced: less (the app: nothing moves; the pane: the 8 fps clock); "
                       "off: still"},
    "palette": {"choices": ("default", "cb"), "aliases": {},
                "help": "default: green and red for pass and fail; cb: blue and orange, safe with colour blindness"},
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


class SettingError(ValueError):
    """A change refused: the value, the file or the guard; nothing was written."""


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
    out = [app("theme", "choice", D["preset"], "the app's colours (signal: night with palette cb)", "look",
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
                          "pane", "next session", choices=shared.get("choices") or spec.get("options"),
                          range=_PLUGIN_RANGES.get(key), aliases=shared.get("aliases")))
    return out


def schema():
    return app_schema() + plugin_schema()


def find(key, surface=None):
    """The entries a name means: one per surface that has it (keys.X for any key the app reads)."""
    import fmcodetui as T
    got = [e for e in schema() if e["key"] == key and surface in (None, e["surface"])]
    if not got and surface in (None, "app") and key.startswith("keys.") and T.parse_key(key[5:]):
        got = [_key_entry(key[5:], None)]
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
    except tomllib.TOMLDecodeError:
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
    """`text` with table.key set to `value`, everything else as it was. `same(a, b)` says two key names are one."""
    import fmcodetui as T
    same = same or (lambda a, b: a == b)
    eol = "\r\n" if "\r\n" in text else "\n"
    lines = text.replace("\r\n", "\n").split("\n")
    keys, heads = _scan(lines)
    hit = [k for k in keys if k[0] == table and k[1] is not None and same(k[1], key)]
    if hit:
        _, _, i, end, col = hit[-1]
        rest = "\n".join([lines[i][col:]] + lines[i + 1:end + 1])
        lead = rest[:len(rest) - len(rest.lstrip(" \t"))] or " "
        whole, tail = _parses("v =" + rest), ""
        for p in (m.start() for m in re.finditer("#", rest) if m.start() >= rest.rfind("\n") + 1):
            if _parses("v =" + rest[:p]) == whole:
                tail = rest[len(rest[:p].rstrip()):]
                break
        lines[i:end + 1] = [lines[i][:col] + lead + T._toml(value) + tail]
    else:
        line = f"{T._toml_key(key)} = {T._toml(value)}"
        mine = [k for k in keys if k[0] == table]
        if mine:
            lines.insert(mine[-1][3] + 1, line)
        elif table in heads:
            lines.insert(heads[table] + 1, line)
        elif table is None and heads:
            lines.insert(min(heads.values()), line)
        else:
            body = "\n".join(lines).rstrip("\n")
            add = ([f"[{T._toml_key(table)}]"] if table else []) + [line]
            lines = ([body, ""] if body and table else [body] if body else []) + add + [""]
    return eol.join(lines)


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


def set_app(key, value, path=None):
    """Set one tui.toml setting in place: (the value written, [other settings it made bad, which the app skips]).
    SettingError (the file untouched) when the name or value is wrong, the file doesn't parse, load_config rejects the
    value or the app can't draw with it."""
    import fmcodetui as T
    import fmcore
    path = path or app_path()
    entries = find(key, "app")
    if not entries:
        raise SettingError(f"{key}: not a setting of the app (fm settings list shows them)")
    value = _check(entries[0], value)
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        text = ""
    except (OSError, UnicodeDecodeError) as e:
        raise SettingError(f"can't read {path}: {e}") from None
    if len(text) > 1_000_000:  # the line scan parses each value as it goes: a settings file, not a data file
        raise SettingError(f"{path} is over 1 MB: edit it by hand")
    if _parses(text) is None:
        raise SettingError(f"{path} isn't valid TOML: fix it first (fm code tui names the line)")
    table, name = _split(key)
    same = (lambda a, b: T.parse_key(a) == T.parse_key(b)) if table == "keys" else None
    new = edit_toml(text, table, name, value, same)
    got = _parses(new)
    placed = (got or {}).get(table, {}) if table else got
    if not isinstance(placed, dict) or not any((same or (lambda a, b: a == b))(k, name) and v == value
                                               for k, v in placed.items()):
        raise SettingError(f"{key}: can't place it in {path} (a [{table}] written another way?); edit it by hand")
    old = set(_load(text, path)[1])
    cfg, errors = _load(new, path)
    errors = [e for e in errors if e not in old]
    # the value itself rejected: refused. Another setting it makes bad (columns that leave widths one short, a theme
    # that leaves a [colors] entry too faint) is skipped by the app as any bad setting is: written, and said
    own = [e for e in errors if e[len(path) + 2:].startswith((f"{key}:", f"{key} ="))]
    if own:
        raise SettingError("; ".join(own))
    try:
        for w, h in ((100, 30), (60, 20)):  # wide and narrow: both layouts
            T.render(T.State(), w, h, cfg)
    except Exception as e:
        raise SettingError(f"{key} = {T._toml(value)}: the app can't draw with it ({type(e).__name__}: {e})") from None
    fmcore.write_atomic(os.path.realpath(path), new)  # a tui.toml linked from a dotfiles repo stays linked
    return value, errors


# ---------------------------------------------------------------- the plugin: Claude Code's settings.json

def claude_dir():
    return os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")


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
    home, cwd, b, meta = os.path.expanduser("~"), os.getcwd(), None, {}
    if p:
        try:
            b, meta = c.active_brief(c.load_briefs(p), getattr(p, "lane", None)), c.read_meta(p)
        except Exception:
            b, meta = None, {}  # unreadable: no grants, the guard decides as with none
    ctx = fmguard.Ctx(cwd=cwd, project_root=fmguard.project_root_for(cwd, home), home=home,
                      foreman_home=c.foreman_home(), state_dir=c.state_dir(), state_fallbacks=c.state_fallbacks(),
                      allow=set(b.meta.get("allow") or []) if b else set(), task_id=b.id if b else None,
                      standing=set(meta.get("standing") or {}), trusted=bool(c.trusted()))
    block = fmguard.check("Write", {"file_path": path}, ctx)
    return fmguard.message(block, ctx) if block else None


def set_plugin(key, value, p=None):
    """Set one of the mod's options in settings.json pluginConfigs when the guard allows that write; SettingError with
    the exact change to make by hand when it doesn't (nothing written)."""
    import fmcore
    entries = find(key, "plugin")
    if not entries:
        raise SettingError(f"{key}: not a setting of the {PLUGIN} pane (fm settings list shows them)")
    value = _check(entries[0], value)
    path, data = claude_settings()
    pid = plugin_id(data)
    how = (f'to set it, edit {path}: pluginConfigs → "{pid}" → options → {json.dumps({key: value})[1:-1]} '
           f"(or Claude Code's /plugin → {PLUGIN} → configure)")
    block = _guard_block(path, p)
    if block:
        raise SettingError(f"plugin {key}: not written, the guard protects {path} ({block}); {how}")
    pc = data.setdefault("pluginConfigs", {})
    cfg = pc.setdefault(pid, {}) if isinstance(pc, dict) else None
    opts = cfg.setdefault("options", {}) if isinstance(cfg, dict) else None
    if not isinstance(opts, dict):
        raise SettingError(f"{path}: pluginConfigs isn't laid out as Claude Code writes it; {how}")
    opts[key] = value
    fmcore.write_atomic(os.path.realpath(path), json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return value


# ---------------------------------------------------------------- reading both, and the command

def rows():
    """Every setting with its value now, its default and where it is stored."""
    import fmcodetui as T
    apath = app_path()
    cfg, _ = T.load_config(apath)
    try:
        spath, data = claude_settings()
    except SettingError:
        spath, data = os.path.join(claude_dir(), "settings.json"), {}
    pid, opts = plugin_id(data), plugin_values(data)

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

    return [dict(e, value=now(e), where=apath if e["surface"] == "app" else f"{spath} pluginConfigs.{pid}.options."
                 f"{e['key']}") for e in schema()]


def _text(r, width=22):
    import fmcodetui as T
    show = lambda v: T._toml(v) if r["surface"] == "app" else json.dumps(v, ensure_ascii=False)
    note = "" if r["value"] == r["default"] else f"  (default {show(r['default'])})"
    return f"{r['key']:<{width}} {show(r['value'])}{note}"


def cmd_settings(args):
    import fmcli
    import fmcodetui as T
    if args.action == "list":
        got = rows()
        if args.json:
            return fmcli.out(args, got, None)
        lines = []
        for surface, title in (("app", "app (fm code; next run)"), ("plugin", f"plugin ({PLUGIN} pane; next session)")):
            mine = [r for r in got if r["surface"] == surface and (args.surface in (None, surface))]
            if mine:
                where = mine[0]["where"] if surface == "app" else mine[0]["where"].rsplit(".", 1)[0]
                lines += [f"{title}: {where}"] + ["  " + _text(r) for r in mine]
        return fmcli.out(args, got, "\n".join(lines) or "no settings found")
    if not args.key:
        raise fmcli.UsageError(f"fm settings {args.action} KEY{' VALUE' if args.action == 'set' else ''}")
    if args.action == "get":
        got = [r for r in rows() if r["key"] == args.key and args.surface in (None, r["surface"])]
        if not got:
            raise fmcli.UsageError(f"{args.key}: no such setting (fm settings list shows them)")
        return fmcli.out(args, got, "\n".join(f"{r['surface']}: {_text(r, 0)}  [{r['where']}]" for r in got))
    if args.value is None:
        raise fmcli.UsageError("fm settings set KEY VALUE")
    entries = find(args.key, args.surface)
    if not entries:
        raise fmcli.UsageError(f"{args.key}: no such setting{f' in the {args.surface}' if args.surface else ''} "
                               "(fm settings list shows them)")
    p = None
    try:
        p = fmcli.resolve(args, create=False)
    except fmcli.UsageError:
        pass  # outside a project: no task grants, the guard decides as with none
    done, refused = [], []
    for e in entries:
        try:
            if e["surface"] == "app":
                v, warn = set_app(args.key, args.value)
                done.append({"surface": "app", "key": args.key, "value": v, "where": app_path(), "warnings": warn,
                             "line": f"app: {args.key} = {T._toml(v)} in {app_path()} (the next fm code run reads it)"
                                     + "".join(f"\n  now skipped: {w}" for w in warn)})
            else:
                v = set_plugin(args.key, args.value, p)
                done.append({"surface": "plugin", "key": args.key, "value": v,
                             "line": f"plugin: {args.key} = {json.dumps(v)} (the next Claude Code session reads it)"})
        except SettingError as x:
            refused.append(f"{e['surface']}: {x}")
    fmcli.out(args, {"set": done, "refused": refused}, "\n".join([d["line"] for d in done] + refused))
    if refused:
        import fmcore
        raise fmcore.PolicyError(f"{len(refused)} of {len(entries)} not written (above)")
    return 0
