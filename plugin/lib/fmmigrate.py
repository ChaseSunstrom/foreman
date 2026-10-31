"""fm prove --migration's runners (T-2288, T-2386, Mission 7): up, down, up again on a throwaway database, in a copy of the tree.

Plain NAME.up.sql/NAME.down.sql pairs and dbmate files (one file, `-- migrate:up` and `-- migrate:down` sections) run in
process on a throwaway sqlite file; SQL written for Postgres runs on a throwaway cluster in a temp dir (unix socket only,
no TCP) when initdb, pg_ctl and psql are installed. alembic and Django run their own CLI against the throwaway sqlite file
through the tool's own override (a generated alembic ini, a generated Django settings module). The real database is never
reached: the tool's environment has no connection variable and no .env file, and a database that resolves anywhere else is
refused before any migration runs. prisma and rails say what they need. A failure that is the environment's (a missing
module) or the dialect's (Postgres-only SQL and no Postgres here) is unproven, never fail."""
import configparser
import json
import os
import re
import sqlite3
import subprocess
import time

import fmcore as c

MIG_FILES, MIG_BYTES = 500, 1 << 20  # pairs, and bytes per file, a migration run reads
FINISH_T = 120  # seconds the run fm task finish makes may take
APPS_MAX = 20  # Django apps whose migrations are taken to zero
PG_START_T = 60  # seconds Postgres has to initialise and start
# SQL that only Postgres reads: when sqlite rejects it the verdict is the dialect's, not the migration's
PG_ONLY = re.compile(r"(?i)\bcreate\s+(extension|schema|sequence|type\s+\S+\s+as\s+enum|(or\s+replace\s+)?function|materialized)"
                     r"|\b(big|small)?serial\b|\bjsonb\b|\buuid\b|\btimestamptz\b|\bbytea\b|::\s*\w+|\$\$|\bilike\b"
                     r"|\bgen_random_uuid\b|\bconcurrently\b|\bdrop\s+(extension|type|schema|function)\b"
                     r"|\busing\s+(gin|gist|brin)\b|\w\[\]")
PG_HINT = re.compile(r"(?i)postgres|psycopg|asyncpg|pg8000")  # a tree's config that says its database is Postgres
# what a tool says when the environment, not the migration, is wrong
ENV_ERR = re.compile(r"ModuleNotFoundError|ImportError|No module named|command not found|KeyError: '[A-Z][A-Z0-9_]*'|"
                     r"couldn't start")
DB_VAR = re.compile(r"(?i)^(DATABASE|DB_|PG|MYSQL|MARIADB|POSTGRES|SQLALCHEMY|DJANGO_)")  # connection settings: never passed on
DB_URL = re.compile(r"(?i)\b(postgres(ql)?|mysql|mariadb|mssql|oracle|cockroachdb|redshift)(\+\w+)?://")
BOOKKEEPING = {"alembic_version", "django_migrations"}  # the tool's own tables are not the schema
MARKER = re.compile(r"(?mi)^--\s*migrate:(up|down)\b[^\n]*$")
PG_SCHEMA = ("SELECT c.relkind || ' ' || c.relname || ': ' || coalesce((SELECT string_agg(a.attname || ' ' || "
             "format_type(a.atttypid, a.atttypmod) || CASE WHEN a.attnotnull THEN ' not null' ELSE '' END, ', ' ORDER BY "
             "a.attnum) FROM pg_attribute a WHERE a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped), '') FROM "
             "pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND c.relkind IN "
             "('r', 'v', 'm', 'S', 'i') ORDER BY 1")


class Unproven(Exception):
    """The run can't say pass or fail here (a server that won't start, a tool that can't resolve its database)."""


def _env(root, home):
    """The tool's environment: Foreman's minimal one (no credentials), no connection variable, HOME the throwaway folder."""
    import fmfind
    env = {k: v for k, v in fmfind._tool_env(root).items() if not DB_VAR.match(k)}
    env["HOME"] = home
    return env


def _exec(argv, cwd, env, end):
    """(out, err, rc, why) of one run, its time clamped to what is left before end (a clock time)."""
    import fminfra
    return fminfra._run(argv, cwd, env, time.monotonic() + max(1, end - time.time()))


def _say(text, tmp, n=240):
    """A tool's words for a verdict: the throwaway folder named by no path, secrets redacted, three lines."""
    import fminfra
    return fminfra._first((text or "").replace(tmp, "<tmp>"))[:n]


def _read(path):
    if os.path.getsize(path) > MIG_BYTES:
        raise ValueError(f"{os.path.basename(path)} is over {MIG_BYTES} bytes")
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def _schema(db):
    return [f"{t} {n}: {s}" for t, n, s in db.execute(
        "SELECT type, name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name")
        if n not in BOOKKEEPING]


def _file_schema(path):
    db = sqlite3.connect(path)
    try:
        return _schema(db)
    finally:
        db.close()


def _diff(a, b):
    return "; ".join(x[:120] for x in sorted(set(a) ^ set(b))[:5])


def _cycle(r, schema, step, left, ok, words=("up", "down")):
    """up, down, up through step(which) -> None or (why, tool's words, the SQL that failed); schema() lists the objects.
    left(r) names what the down left behind ('' for nothing). Fills r's before and after_* keys and its verdict; words
    are the tool's names for up and down in the messages. A schema that differs is a fail whatever the dialect."""
    r["before"] = schema()
    for which, key in (("up", "after_up"), ("down", "after_down"), ("up", "after_up2")):
        bad = step(which)
        if bad:
            return r | {"verdict": "fail", "why": bad[0], "err": bad[1], "text": bad[2]}
        r[key] = schema()
        if key == "after_down" and left(r):
            return r | {"verdict": "fail", "why": f"{words[1]}: schema after it differs from the start: {left(r)}"}
        if key == "after_up2" and r[key] != r["after_up"]:
            return r | {"verdict": "fail", "why": f"{words[0]}: schema after it differs from the first {words[0]}: "
                        + _diff(r[key], r["after_up"])}
    return r | {"verdict": "pass", "why": ok}


def _judge(r, dialect, why_dialect):
    """r without the raw failure text; a failure that is the environment's or the dialect's (dialect: 'postgres' when the
    failing step was written for it) is unproven."""
    err, text = r.pop("err", ""), r.pop("text", "")
    if r["verdict"] != "fail":
        return r
    if ENV_ERR.search(err):
        return r | {"verdict": "unproven", "why": f"{r['why']} (the environment, not the migration: what the tool imports "
                                                   "isn't installed where fm runs)"}
    if dialect(text):
        return r | {"verdict": "unproven", "dialect": "postgres",
                    "why": f"{r['why']} (dialect: written for Postgres, and {why_dialect}; unproven, not failed)"}
    return r


# --- SQL: NAME.up.sql/NAME.down.sql pairs and dbmate files, on sqlite or a throwaway Postgres

def _pairs(work):
    """(tool, [(label, up sql, down sql or None)]): dbmate files when the tree has any, else the NAME.up.sql pairs."""
    ups, other = [], []
    for d, dirs, names in os.walk(work):
        dirs[:] = sorted(dirs)
        for n in sorted(names):
            path = os.path.join(d, n)
            if n.endswith(".up.sql"):
                ups.append(path)
            elif n.endswith(".sql") and not n.endswith(".down.sql"):
                other.append(path)
    dbmate = []
    for path in other[:MIG_FILES * 4]:
        with open(path, encoding="utf-8", errors="replace") as f:
            if "migrate:up" in f.read(4096):  # dbmate's marker sits at the top of the file
                dbmate.append(path)
    if dbmate:
        out = []
        for path in dbmate[:MIG_FILES]:
            parts = MARKER.split(_read(path))  # [before, "up", up sql, "down", down sql]
            kinds = dict(zip(parts[1::2], parts[2::2]))
            if "up" in kinds:
                out.append((os.path.relpath(path[:-4], work), kinds["up"], kinds.get("down")))
        return "dbmate", out
    out = []
    for up in ups[:MIG_FILES]:
        base, down = up[:-len(".up.sql")], up[:-len(".up.sql")] + ".down.sql"
        out.append((os.path.relpath(base, work), _read(up), _read(down) if os.path.isfile(down) else None))
    return "sql", out


class Lite:
    name = "sqlite"

    def __init__(self, tmp, end):
        self.db = sqlite3.connect(os.path.join(tmp, "migration.db"), isolation_level=None)
        # ATTACH would reach a file outside the throwaway database; the progress handler cuts a runaway statement
        self.db.set_authorizer(lambda act, *a: sqlite3.SQLITE_DENY if act == sqlite3.SQLITE_ATTACH else sqlite3.SQLITE_OK)
        self.db.set_progress_handler(lambda: 1 if time.time() > end else 0, 1000)

    def schema(self):
        return _schema(self.db)

    def run(self, sql):
        try:
            self.db.executescript(sql)
        except sqlite3.Error as e:
            return "interrupted" if "interrupt" in str(e) else c.plain(str(e))[:200]
        return ""

    def close(self):
        self.db.close()


class Pg:
    """A Postgres cluster in <tmp>/pg: initdb, pg_ctl start on a unix socket in that folder and no TCP (listen_addresses
    empty), psql over the socket, pg_ctl stop; the folder goes with the throwaway copy."""
    name = "postgres"

    def __init__(self, bins, tmp, env, end):
        self.bins, self.env, self.end, self.tmp = bins, env, end, tmp
        self.dir = os.path.join(tmp, "pg")
        self.sock, self.data = os.path.join(self.dir, "s"), os.path.join(self.dir, "data")
        self.up = False

    def start(self):
        os.makedirs(self.sock)
        out, err, rc, why = _exec([self.bins["initdb"], "-D", self.data, "-A", "trust", "-N", "--no-locale", "-E", "UTF8"],
                                  self.dir, self.env, time.time() + PG_START_T)
        if rc != 0 or why:
            raise Unproven(f"Postgres couldn't initialise here: {_say(why or err or out, self.tmp)}")
        opts = f"-c listen_addresses='' -c unix_socket_directories={self.sock}"
        argv = [self.bins["pg_ctl"], "-D", self.data, "-w", "-t", str(PG_START_T), "-l", os.path.join(self.dir, "log"),
                "-o", opts, "start"]
        try:  # not _exec: that kills the process group when the run ends, and the server must outlive pg_ctl
            with open(os.path.join(self.dir, "pg_ctl.out"), "w+") as o:
                self.up = True  # a start that half-worked is stopped too
                rc = subprocess.run(argv, cwd=self.dir, env=self.env, stdin=subprocess.DEVNULL, stdout=o,
                                    stderr=subprocess.STDOUT, start_new_session=True, timeout=PG_START_T + 10).returncode
                o.seek(0)
                said = o.read(4000)
        except (OSError, subprocess.SubprocessError) as e:
            raise Unproven(f"Postgres couldn't start here: {_say(str(e), self.tmp)}")
        if rc != 0:
            raise Unproven(f"Postgres couldn't start here: {_say(said, self.tmp)}")

    def psql(self, *args):
        argv = [self.bins["psql"], "-X", "-q", "-h", self.sock, "-d", "postgres", "-v", "ON_ERROR_STOP=1", *args]
        out, err, rc, why = _exec(argv, self.dir, self.env, self.end)
        return out, ("" if rc == 0 and not why else _say(why or err or out or f"exit {rc}", self.tmp))

    def schema(self):
        out, bad = self.psql("-A", "-t", "-c", PG_SCHEMA)
        if bad:
            raise Unproven(f"couldn't read the schema from the throwaway Postgres: {bad}")
        return sorted(l for l in out.splitlines() if l.strip())

    def run(self, sql):
        path = os.path.join(self.dir, "step.sql")
        with open(path, "w", encoding="utf-8") as f:
            f.write(sql)
        return self.psql("-f", path)[1]

    def close(self):
        if self.up:
            try:
                subprocess.run([self.bins["pg_ctl"], "-D", self.data, "-m", "immediate", "stop"], cwd=self.dir, env=self.env,
                               stdin=subprocess.DEVNULL, capture_output=True, timeout=30, start_new_session=True)
            except (OSError, subprocess.SubprocessError):
                pass  # ponytail: a server that won't stop dies when its data folder goes; a PID sweep if one ever lingers


def _pg_bins(env, root):
    """({tool: path}, '') when a throwaway Postgres can run here, else ({}, why not)."""
    import fminfra
    bins = {n: fminfra._which(n, env, root) for n in ("initdb", "pg_ctl", "psql")}
    gone = [n for n, p in bins.items() if not p]
    if gone:
        return {}, f"{', '.join(gone)} isn't installed (on PATH), so no throwaway Postgres can start"
    if os.geteuid() == 0:
        return {}, "Postgres refuses to run as root, so no throwaway Postgres can start"
    return bins, ""


def _sql_tool(root, work, tmp, end):
    tool, pairs = _pairs(work)
    if not pairs:
        return None
    env = _env(root, tmp)
    bins, no_pg = _pg_bins(env, root)
    eng = Pg(bins, tmp, env, end) if bins and PG_ONLY.search(" ".join(t or "" for p in pairs for t in p[1:])) \
        else Lite(tmp, end)
    r = {"tool": tool, "engine": eng.name, "migrations": [p[0] for p in pairs]}

    def step(which):
        for label, up, down in pairs if which == "up" else reversed(pairs):
            sql = up if which == "up" else down
            if sql is None:
                return f"{label}: no down migration (a .down.sql file, or a -- migrate:down section)", "", ""
            err = eng.run(sql)
            if err:
                return (f"{label}: {which} hit the time limit" if err == "interrupted" else
                        f"{label}: {which} failed: {err}"), err, sql
            if time.time() > end:
                return f"{label}: {which} hit the time limit", "", ""
        return None
    try:
        if eng.name == "postgres":
            eng.start()
        r = _cycle(r, eng.schema, step, lambda x: _diff(x["after_down"], x["before"]) if x["after_down"] != x["before"] else "",
                   f"{len(pairs)} migration(s): up, down, up gave the same schema each time")
    except Unproven as e:
        return r | {"verdict": "unproven", "why": str(e), "dialect": "postgres"}
    finally:
        eng.close()
    return _judge(r, lambda sql: eng.name == "sqlite" and bool(PG_ONLY.search(sql)), no_pg)


# --- the repo's own tool, pointed at the throwaway sqlite file

def _sandbox(env, root, cwd, end):
    import fminfra
    return fminfra.sandbox_prefix(env, root, cwd, time.monotonic() + max(1, end - time.time()))


def _call(label, argv, cwd, env, end, tmp):
    out, err, rc, why = _exec(argv, cwd, env, end)
    if rc == 0 and not why:
        return None
    said = _say(why or err.strip() or out.strip() or f"exit {rc}", tmp)
    return f"{label} failed: {said}", said, said  # only a tool's own failure can be the dialect's: text is not empty


def _no_env_files(work):
    """The tool reads no .env of the tree's: it could name the real database."""
    for d, dirs, names in os.walk(work):
        for n in names:
            if n == ".env" or n.startswith(".env."):
                os.remove(os.path.join(d, n))


def _alembic_ini(text, url):
    """The ini text with its sqlalchemy.url line(s) set to url (added under [alembic] when it has none)."""
    line = f"sqlalchemy.url = {url}"
    new, n = re.subn(r"(?m)^[ \t]*sqlalchemy\.url[ \t]*[=:].*$", lambda m: line, text)
    return new if n else re.sub(r"(?m)^\[alembic\][ \t]*$", lambda m: m.group(0) + "\n" + line, text, count=1)


def _need(name, why):
    return {"verdict": "unproven", "why": f"{name} migrations found, but {why}"}


def _alembic(root, work, tmp, end):
    ini = os.path.join(work, "alembic.ini")
    if not os.path.isfile(ini):
        return None
    env = _env(root, tmp)
    import fminfra
    exe = fminfra._which("alembic", env, root)
    if not exe:
        return _need("alembic", "the alembic CLI isn't on PATH here: install it, and what the project's env.py imports, in "
                                "the environment fm runs in")
    text, url = _read(ini), "sqlite:///" + os.path.join(tmp, "migration.db")
    gen = os.path.join(work, "fm_prove_alembic.ini")
    with open(gen, "w", encoding="utf-8") as f:
        f.write(_alembic_ini(text, url))
    cp = configparser.ConfigParser(interpolation=None, strict=False)
    try:  # the resolved database: what the ini we just wrote says
        cp.read(gen, encoding="utf-8")
        got = cp.get("alembic", "sqlalchemy.url")
    except (configparser.Error, OSError, UnicodeError):
        got = None
    if got != url:
        return {"verdict": "refused", "why": "alembic's sqlalchemy.url doesn't resolve to the throwaway database: "
                                             "nothing ran"}
    loc = re.search(r"(?m)^script_location[ \t]*[=:][ \t]*(.+?)[ \t]*$", text)
    scripts = os.path.realpath(os.path.join(work, (loc.group(1) if loc else "alembic").replace("%(here)s", work)))
    envpy = _read(os.path.join(scripts, "env.py")) if os.path.isfile(os.path.join(scripts, "env.py")) \
        and os.path.commonpath([scripts, work]) == work else ""
    if DB_URL.search(envpy):
        return {"verdict": "refused", "why": "alembic's env.py names a database by a literal URL, which it would open "
                                             "instead of the throwaway one: nothing ran"}
    _no_env_files(work)
    base = _sandbox(env, root, work, end) + [exe, "-c", "fm_prove_alembic.ini"]
    db = os.path.join(tmp, "migration.db")

    def step(which):
        return _call(f"alembic {which}grade", base + (["upgrade", "head"] if which == "up" else ["downgrade", "base"]),
                     work, env, end, tmp)
    r = _cycle({"engine": "sqlite"}, lambda: _file_schema(db), step,
               lambda x: _diff(x["after_down"], x["before"]) if x["after_down"] != x["before"] else "",
               "alembic: upgrade head, downgrade base, upgrade head gave the same schema each time",
               ("upgrade", "downgrade"))
    pg = bool(PG_HINT.search(text + envpy))
    # ponytail: tools run on sqlite only; a tool failing in a Postgres project is unproven, a throwaway cluster for tools later
    return _judge(r, lambda said: pg and bool(said), "fm prove --migration runs alembic on sqlite only")


def _django_apps(work):
    """Sorted labels of the apps with migrations: a migrations folder holding a migration beside its __init__."""
    out = set()
    for d, dirs, names in os.walk(work):
        dirs[:] = sorted(x for x in dirs if x != "site-packages" and not x.startswith("."))
        if os.path.basename(d) == "migrations" and any(n.endswith(".py") and n != "__init__.py" for n in names):
            out.add(os.path.basename(os.path.dirname(d)))
    return sorted(out)[:APPS_MAX]


def _django_settings(mod, db):
    """A settings module that is the project's own with DATABASES replaced by the one throwaway sqlite file."""
    return (f"from {mod} import *  # noqa\n"
            f"DATABASES = {{'default': {{'ENGINE': 'django.db.backends.sqlite3', 'NAME': {db!r}}}}}\n")


PROBE = ("import django, json; django.setup(); from django.conf import settings as s; "
         "print(json.dumps({k: [v.get('ENGINE'), v.get('NAME')] for k, v in s.DATABASES.items()}))")


def _django(root, work, tmp, end):
    manage = os.path.join(work, "manage.py")
    apps = _django_apps(work) if os.path.isfile(manage) else []
    if not apps:
        return None
    env = _env(root, tmp)
    import fminfra
    py = fminfra._which("python3", env, root)
    if not py:
        return _need("django", "python3 (with Django installed) isn't on PATH here")
    mod = re.search(r"DJANGO_SETTINGS_MODULE['\"]\s*,\s*['\"]([\w.]+)['\"]", _read(manage))
    if not mod:
        return _need("django", "manage.py doesn't set DJANGO_SETTINGS_MODULE where fm can read it")
    db = os.path.join(tmp, "migration.db")
    with open(os.path.join(work, "fm_prove_settings.py"), "w", encoding="utf-8") as f:
        f.write(_django_settings(mod.group(1), db))
    env["DJANGO_SETTINGS_MODULE"] = "fm_prove_settings"
    _no_env_files(work)
    pre = _sandbox(env, root, work, end)
    out, err, rc, why = _exec(pre + [py, "-c", PROBE], work, env, end)  # the resolved database, before any migration
    if rc != 0 or why:
        said = _say(why or err or out or f"exit {rc}", tmp)
        return _need("django", f"fm couldn't load the project's settings to check its database ({said})")
    try:
        resolved = json.loads(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        resolved = None
    if resolved != {"default": ["django.db.backends.sqlite3", db]}:
        return {"verdict": "refused", "why": "Django's DATABASES doesn't resolve to the throwaway database: nothing ran"}

    def migrate(label, *args):
        return _call(label, pre + [py, "manage.py", "migrate", *args], work, env, end, tmp)

    def step(which):
        if which == "up":
            return migrate("django migrate")
        for app in reversed(apps):
            bad = migrate(f"django migrate {app} zero", app, "zero")
            if bad:
                return bad
        return None

    def left(x):  # Django's default table names are app_model: the app's own tables must be gone
        mine = tuple(a.lower() + "_" for a in apps)
        return "; ".join(o[:120] for o in x["after_down"] if o.split(" ", 2)[1].lower().startswith(mine))
    r = _cycle({"engine": "sqlite", "migrations": apps}, lambda: _file_schema(db), step, left,
               "django: migrate, migrate APP zero, migrate gave the same schema each time")
    text = "\n".join(_read(os.path.join(d, n)) for d, _, names in os.walk(work) for n in sorted(names)
                     if n.startswith("settings") and n.endswith(".py") and os.path.getsize(os.path.join(d, n)) < MIG_BYTES)
    pg = bool(PG_HINT.search(text))
    return _judge(r, lambda said: pg and bool(said), "fm prove --migration runs Django on sqlite only")


def _prisma(root, work, tmp, end):
    if not os.path.isfile(os.path.join(work, "prisma", "schema.prisma")):
        return None
    return _need("prisma", "prisma migrate needs a database server at DATABASE_URL and its schema engine, and has no down "
                           "step; fm prove --migration never opens a real database or the network: run prisma migrate "
                           "reset against a throwaway one yourself")


def _rails(root, work, tmp, end):
    d = os.path.join(work, "db", "migrate")
    if not os.path.isdir(d) or not any(n.endswith(".rb") for n in os.listdir(d)):
        return None
    return _need("rails", "running them needs bundle install and the app's own database server; fm prove --migration never "
                          "opens a real database or the network: run rails db:migrate, rails db:rollback STEP=n and "
                          "rails db:migrate against a throwaway database yourself")


# (name, runner(root, work, tmp, end) -> result dict, or None when the tree has none of its migrations)
MIG_TOOLS = [("sql", _sql_tool), ("alembic", _alembic), ("django", _django), ("prisma", _prisma), ("rails", _rails)]


def run(root, work, tmp, end):
    """The first tool in MIG_TOOLS that has migrations in the copy at work: its result dict (tool included), or None."""
    for name, tool in MIG_TOOLS:
        try:
            r = tool(root, work, tmp, end)
        except Unproven as e:
            r = {"verdict": "unproven", "why": str(e)}
        except (OSError, ValueError, sqlite3.Error) as e:
            r = {"verdict": "fail", "why": f"{name}: {_say(str(e), tmp)}"}
        if r:
            return {"tool": name} | r
    return None


# --- fm task finish

PATHS = re.compile(r"(^|/)(migrations?|migrate)/|\.(up|down)\.sql$|(^|/)alembic\.ini$|(^|/)alembic/versions/|"
                   r"(^|/)prisma/schema\.prisma$")


def for_task(p, b, say=print):
    """(code, text) for fm task finish, or None: the migrations the task touched, proved in a trusted tree. An untrusted
    tree and an unproven run are said, never a failure and never evidence."""
    import fminfra
    import fmprove
    if not any(PATHS.search(f) for f in fminfra.touched(p, b)):
        return None
    if not (fmprove.trusted(p.root) or fmprove._lane_trusted(p, p.root)):
        say("migration: this task touched migration files; proving them runs the tree's own tool, so it needs your yes "
            "once per tree: fm prove --migration PATH --yes-run")
        return None
    r = fmprove.migration(p.root, True, limit=FINISH_T)
    line = f"{r['verdict']}: {r['why']}"
    if r["verdict"] in ("pass", "fail"):
        return {"pass": 0, "fail": 1}[r["verdict"]], line
    say("migration: " + line)
    return None
