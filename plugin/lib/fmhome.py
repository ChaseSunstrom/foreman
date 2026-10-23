"""fm home export / import (T-1665): Foreman's projects (tasks, archive, research, decisions, ledger, meta) and tui.toml as
one tarball without secrets, checked on import into an empty home.

What travels is an allowlist, the same both ways: per project tasks/, archive/ and research/ markdown, decisions.md,
ledger.jsonl and meta.json cut to the keys in META_KEYS (no grants, autonomy, standing yeses or check commands); plus
tui.toml. Everything else (grants such as trust.json, runner settings such as code.toml, fixes.md's commands, caches,
the registry, home-wide logs) stays on this machine. Sensitive projects stay too. Each text file is redacted
(fmcore.redact, and string values under credential-named JSON keys blanked); binary files can't be and stay.
MANIFEST.json lists each member's sha256 and size.

Import reads the headers one at a time (header records, members, sizes all capped) and refuses the whole file on any
member that isn't a regular file, whose path isn't on the allowlist (absolute, `..`, links included), that the manifest
doesn't vouch for, or a manifest entry with no member. Contents are hashed into a staging folder inside the state
folder; briefs then lose their grants and run marks (fmsync._from_mirror, as a pulled mirror does), meta.json is cut to
META_KEYS again and markdown loses terminal sequences. tui.toml (core config) comes in only when the state is the home's
own. The staged projects folder moves in with one rename; a failure rolls tui.toml back. The manifest checks integrity,
not origin: anyone can write a matching one, so only the user runs `fm home import` (fmguard.USER_ONLY_FM)."""
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import tarfile
import tempfile
import zlib

import fmcore as c
import fmcli
import fmsync

FORMAT = "foreman-home/1"
MANIFEST = "MANIFEST.json"
# import bounds: per member, in all, member count and one header record (a GNU long name or pax header is read whole)
MAX_FILE, MAX_TOTAL, MAX_MEMBERS, MAX_HEADER = 256 << 20, 4 << 30, 500_000, 64 << 10
META_KEYS = ("slug", "path", "created", "last_active", "last_tidy", "next_id", "schema", "sensitive")
_META_DEFAULTS = {"session": {}, "drive": True, "last_tidy": None}  # as fm init writes a new project
_SLUG = re.compile(r"^[A-Za-z0-9][\w.-]*$")
_PROJECT_FILE = re.compile(r"^(?:(?:tasks|archive|research)/(?:[^/]+/)*[^/]+\.md|decisions\.md|ledger\.jsonl|meta\.json)$")
_CRED_KEY = re.compile(r"(?i)(?:api.?key|secret|token|passw(?:or)?d|pwd|credentials?|cookie|authorization|private.?key)$")
_move = os.replace  # one name, so a test can fail the second move


class Refused(Exception):
    pass


def _allowed(name):
    """(slug, path inside the project) for a project file on the allowlist, ("", "tui.toml") for tui.toml, else None."""
    if name == "tui.toml":
        return "", name
    m = re.match(r"^state/projects/([^/]+)/(.+)$", name)
    if m and _SLUG.match(m.group(1)) and _PROJECT_FILE.match(m.group(2)):
        return m.group(1), m.group(2)
    return None


# ---------------------------------------------------------------- what a file may carry

def _blank(obj):
    """obj with string values under credential-named keys blanked, and whether any was."""
    if isinstance(obj, dict):
        out, hit = {}, False
        for k, v in obj.items():
            if isinstance(v, str) and isinstance(k, str) and _CRED_KEY.search(k) and v:
                out[k], hit = "[REDACTED]", True
            else:
                out[k], h = _blank(v)
                hit = hit or h
        return out, hit
    if isinstance(obj, list):
        pairs = [_blank(v) for v in obj]
        return [v for v, _ in pairs], any(h for _, h in pairs)
    return obj, False


def _jsonl(text):
    lines = []
    for line in text.split("\n"):
        try:
            obj = json.loads(line)
        except ValueError:
            obj = None  # not JSON: kept as text, the text redaction still applies
        if isinstance(obj, (dict, list)):
            obj, hit = _blank(obj)
            line = json.dumps(obj, ensure_ascii=False) if hit else line
        lines.append(line)
    return "\n".join(lines)


def _meta(text, slug):
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ValueError("meta.json isn't an object")
    meta = dict(_META_DEFAULTS, **{k: obj[k] for k in META_KEYS if k in obj})
    meta["slug"] = slug  # the folder's name, whatever the file says
    if not isinstance(meta.get("next_id"), int) or isinstance(meta.get("next_id"), bool):
        meta.pop("next_id", None)
    if not isinstance(meta.get("path"), str):
        meta.pop("path", None)
    meta["sensitive"] = bool(meta.get("sensitive"))
    return json.dumps(_blank(meta)[0], indent=2, sort_keys=True) + "\n"


def _brief(text):
    try:
        return fmsync._from_mirror(text).render()  # no grants (fmsync.LOCAL_ONLY), run marks or counted audits
    except ValueError:
        return c.plain_lines(c._unmarked(text))  # an archive note without frontmatter


def clean(slug, rel, text, incoming):
    """The text a file may carry out (export) or in (import, incoming=True: the trust boundary)."""
    if rel == "meta.json":
        text = _meta(text, slug)
    elif rel.endswith(".jsonl"):
        text = _jsonl(text)
    elif incoming and rel.startswith(("tasks/", "archive/")):
        text = _brief(text)
    elif incoming and rel.endswith(".md"):
        text = c.plain_lines(text)
    return c.redact(text)


# ---------------------------------------------------------------- export

def _sensitive(project_dir):
    try:
        with open(os.path.join(project_dir, "meta.json"), encoding="utf-8") as f:
            return bool(json.load(f).get("sensitive"))
    except (OSError, ValueError, AttributeError):
        return True  # unreadable meta: treat as sensitive, it stays out


def _candidates(state):
    """(member name, path) for each allowlisted file, (name, why) for each one left out, and how many files of a
    project's state the allowlist leaves (caches, logs, grants)."""
    files, left, other = [], [], 0
    projects = os.path.join(state, "projects")
    for slug in sorted(os.listdir(projects)) if os.path.isdir(projects) else []:
        pdir = os.path.join(projects, slug)
        if os.path.islink(pdir) or not os.path.isdir(pdir) or not _SLUG.match(slug):
            left.append((f"state/projects/{slug}", "not a project folder"))
        elif _sensitive(pdir):
            left.append((f"state/projects/{slug}/", "a sensitive project (fm sensitive on)"))
        else:
            for d, dirs, names in os.walk(pdir):
                dirs[:] = sorted(x for x in dirs if not os.path.islink(os.path.join(d, x)))
                for n in sorted(names):
                    path = os.path.join(d, n)
                    rel = os.path.relpath(path, pdir).replace(os.sep, "/")
                    if _PROJECT_FILE.match(rel) and os.path.isfile(path) and not os.path.islink(path):
                        files.append((f"state/projects/{slug}/{rel}", path))
                    else:
                        other += 1
    return files, left, other


def export(out):
    state, tui = c.state_dir(), os.path.join(c.foreman_home(), "tui.toml")
    out = os.path.abspath(out)
    if os.path.realpath(out).startswith(os.path.realpath(state).rstrip("/") + "/"):
        raise fmcli.UsageError(f"--out {out} is inside the state folder it exports; write it elsewhere")
    if os.path.lexists(out):
        raise fmcli.UsageError(f"{out} exists; remove it or pick another --out")
    files, left, other = _candidates(state)
    if os.path.isfile(tui) and not os.path.islink(tui):
        files.append(("tui.toml", tui))
    notes = []
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(out), prefix=".fm-home-", suffix=".tmp")  # 0600: it's personal data
    manifest = {"format": FORMAT, "exported": c.now(), "files": {}}
    try:
        with os.fdopen(fd, "wb") as raw, tarfile.open(fileobj=raw, mode="w:gz", format=tarfile.PAX_FORMAT) as t:
            for name, path in files:
                slug, rel = _allowed(name)
                why = None
                try:
                    if os.path.getsize(path) > MAX_FILE:
                        why = f"over {MAX_FILE >> 20} MB"
                    else:
                        with open(path, "rb") as f:
                            text = f.read().decode("utf-8")
                        clean_text = clean(slug, rel, text, incoming=False)
                except UnicodeDecodeError:
                    why = "binary (can't be redacted)"
                except ValueError as e:
                    why = f"unreadable JSON ({e})"
                except OSError as e:
                    why = f"unreadable ({e.strerror})"
                if why:
                    left.append((name, why))
                    if rel == "ledger.jsonl":
                        notes.append(f"{name} stays here: {why}")
                    continue
                if rel == "ledger.jsonl" and clean_text != text:
                    notes.append(f"{name}: secrets redacted, so its hash chain (fm verify-ledger) no longer verifies")
                data = clean_text.encode("utf-8")
                _add(t, name, data)
                manifest["files"][name] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
            manifest["left_out"] = [{"path": n, "why": w} for n, w in left]
            _add(t, MANIFEST, json.dumps(manifest, indent=1, sort_keys=True).encode("utf-8"))
        os.replace(tmp, out)
    except BaseException:
        os.unlink(tmp)
        raise
    return manifest, left, other, notes


def _add(t, name, data):
    info = tarfile.TarInfo(name)
    info.size, info.mode, info.mtime = len(data), 0o600, int(datetime.datetime.now().timestamp())
    t.addfile(info, io.BytesIO(data))


# ---------------------------------------------------------------- import

class _CappedInfo(tarfile.TarInfo):
    def _proc_member(self, tf):  # tarfile reads a long-name or pax record whole: check its size first
        if self.type in (tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK, tarfile.XHDTYPE, tarfile.XGLTYPE,
                         tarfile.SOLARIS_XHDTYPE) and self.size > MAX_HEADER:
            raise Refused(f"a {self.size}-byte header record (cap {MAX_HEADER >> 10} KB)")
        return super()._proc_member(tf)


def _check_name(m):
    n = m.name
    if not m.isfile():
        kind = "link" if m.issym() or m.islnk() else "folder" if m.isdir() else "special file"
        raise Refused(f"{n!r} is a {kind}; only regular files are imported")
    parts = n.split("/")
    if n.startswith("/") or "\\" in n or "\0" in n or any(p in ("", ".", "..") for p in parts):
        raise Refused(f"{n!r} is absolute or has a `..`, `.` or empty part")
    if n != MANIFEST and not _allowed(n):
        raise Refused(f"{n!r} isn't state fm home import takes (projects' tasks, archive, research, decisions, ledger, "
                      f"meta; tui.toml)")


def _verified(t):
    """The members and their hashes, every header checked against the manifest before any content is read."""
    members, seen, total = [], set(), 0
    for m in t:  # one at a time: each cap stops the read where it is crossed
        members.append(m)
        if len(members) > MAX_MEMBERS:
            raise Refused(f"over {MAX_MEMBERS} members")
        _check_name(m)
        if m.name in seen:
            raise Refused(f"{m.name!r} appears twice")
        seen.add(m.name)
        total += m.size
        if m.size > MAX_FILE or total > MAX_TOTAL:
            raise Refused(f"{m.name!r} takes it over {MAX_FILE >> 20} MB a file or {MAX_TOTAL >> 30} GB in all")
    man_m = next((m for m in members if m.name == MANIFEST), None)
    if man_m is None:
        raise Refused(f"no {MANIFEST}: not an fm home export")
    try:
        manifest = json.loads(t.extractfile(man_m).read())
        files = manifest["files"]
        if manifest.get("format") != FORMAT or not isinstance(files, dict):
            raise ValueError(f"format {manifest.get('format')!r}")
        sizes = {n: int(e["size"]) for n, e in files.items()}
        hashes = {n: str(e["sha256"]) for n, e in files.items()}
    except (ValueError, KeyError, TypeError, AttributeError, OverflowError, RecursionError) as e:
        raise Refused(f"{MANIFEST} isn't an fm home manifest ({FORMAT}): {e}")
    body = [m for m in members if m.name != MANIFEST]
    for m in body:
        if m.name not in sizes:
            raise Refused(f"{m.name!r} isn't in the manifest")
        if m.size != sizes[m.name]:
            raise Refused(f"{m.name!r} is {m.size} bytes; the manifest says {sizes[m.name]}")
    missing = sorted(set(sizes) - {m.name for m in body})
    if missing:
        raise Refused(f"the manifest lists {len(missing)} file(s) the archive lacks, e.g. {missing[0]!r}")
    return body, hashes


def _empty(state, tui):
    projects = os.path.join(state, "projects")
    return not (tui and os.path.lexists(tui)) and not (os.path.isdir(projects) and os.listdir(projects))


def import_(path):
    """(files imported, files in the archive, notes); Refused, with nothing imported, on any problem."""
    home, state = c.foreman_home(), c.state_dir()
    # tui.toml is core config: only into the home whose state this is (FOREMAN_STATE elsewhere looks empty on its own)
    tui = os.path.join(home, "tui.toml") if os.path.realpath(state) == os.path.realpath(os.path.join(home, "state")) \
        else None
    if not _empty(state, tui):
        raise Refused(f"{home} isn't empty (it has projects or a tui.toml); import goes into an empty home only")
    try:
        t = tarfile.open(path, "r:gz", tarinfo=_CappedInfo)
    except (OSError, tarfile.TarError, EOFError, zlib.error) as e:
        raise Refused(f"{path} isn't a gzip tarball: {e}")
    stage = None
    try:
        with t:
            body, hashes = _verified(t)
            os.makedirs(state, mode=0o700, exist_ok=True)
            stage = tempfile.mkdtemp(dir=state, prefix=".fm-home-import-")  # same filesystem: one rename moves it in
            for m in body:
                data = t.extractfile(m).read(MAX_FILE + 1)
                if hashlib.sha256(data).hexdigest() != hashes[m.name]:
                    raise Refused(f"{m.name!r}: its sha256 hash doesn't match the manifest (changed after export)")
                slug, rel = _allowed(m.name)
                dest = os.path.join(stage, *m.name.split("/"))
                os.makedirs(os.path.dirname(dest), mode=0o700, exist_ok=True)
                with open(dest, "x", encoding="utf-8") as f:
                    f.write(clean(slug, rel, data.decode("utf-8"), incoming=True))
        notes, moved = [], 0
        if not _empty(state, tui):  # another process filled it while this one checked
            raise Refused(f"{home} stopped being empty during the import")
        staged_tui, staged = os.path.join(stage, "tui.toml"), os.path.join(stage, "state", "projects")
        if os.path.exists(staged_tui) and not tui:
            notes.append("tui.toml stays out: this home's state lives elsewhere (FOREMAN_STATE or a fallback)")
        placed = []
        try:
            if os.path.exists(staged_tui) and tui:
                _move(staged_tui, tui)
                placed.append(tui)
                moved += 1
            if os.path.isdir(staged):
                projects = os.path.join(state, "projects")
                if os.path.isdir(projects) and not os.path.islink(projects):
                    os.rmdir(projects)  # empty (checked above); fails if it filled since
                n = sum(len(f) for _, _, f in os.walk(staged))
                _move(staged, projects)
                moved += n
        except OSError:
            for p in placed:
                os.unlink(p)
            raise
        c.regen_registry()
        return moved, len(body), notes
    except Refused:
        raise
    except (OSError, ValueError, OverflowError, RecursionError, tarfile.TarError, EOFError, zlib.error) as e:
        raise Refused(f"{type(e).__name__}: {e}")
    finally:
        if stage:
            shutil.rmtree(stage, ignore_errors=True)


def cmd_home(args):
    if args.action == "export":
        out = args.out or args.file or f"foreman-home-{datetime.date.today().isoformat()}.tar.gz"
        m, left, other, notes = export(out)
        print(f"Exported {len(m['files'])} file(s) to {os.path.abspath(out)} (secrets redacted; a hash per file in "
              f"{MANIFEST}).")
        for n in notes:
            print(f"  ! {n}")
        for name, why in left[:40]:
            print(f"  left out {name}: {why}")
        if len(left) > 40:
            print(f"  … and {len(left) - 40} more (listed in {MANIFEST})")
        print(f"Stays on this machine: {other} project file(s) off the allowlist (caches, logs, grants, fixes.md) and "
              f"the home-wide state (registry, events, budgets, trust); import rebuilds the registry.")
        return 0
    if not args.file:
        raise fmcli.UsageError("fm home import FILE: the tarball fm home export wrote")
    try:
        moved, total, notes = import_(args.file)
    except Refused as e:
        print(f"fm home import: refused, nothing imported: {e}")
        return 1
    print(f"Imported {moved} of {total} file(s) into {c.foreman_home()} (every hash matched its manifest; grants, run "
          f"marks and check commands stripped).")
    for n in notes:
        print(f"  ! {n}")
    return 0
